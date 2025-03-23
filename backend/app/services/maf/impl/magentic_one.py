import json
import logging
import os
import re
from datetime import datetime as dt
from typing import Any

import pytz
from autogen_core import (
    EVENT_LOGGER_NAME,
    AgentId,
    AgentProxy,
    SingleThreadedAgentRuntime,
    TopicId,
)
from autogen_core.models import UserMessage
from autogen_magentic_one.agents.file_surfer import FileSurfer
from autogen_magentic_one.agents.multimodal_web_surfer import MultimodalWebSurfer
from autogen_magentic_one.agents.orchestrator import LedgerOrchestrator
from autogen_magentic_one.agents.user_proxy import UserProxy
from autogen_magentic_one.messages import BroadcastMessage
from autogen_magentic_one.utils import LogHandler, create_completion_client_from_env
from fastapi import HTTPException

from app.core.enums import TaskStatus
from app.core.logging import get_logger
from app.core.settings import settings
from app.schemas.task import AgenticTaskRequest, TaskResponse
from app.services.maf.maf import MultiAgentFramework


class MagenticOne(MultiAgentFramework):
    def __init__(self):
        self.ist_timezone = pytz.timezone("Asia/Kolkata")
        self.logger = get_logger()

    async def _setup_architecture(self, **kwargs: Any):
        self.logger.info("Setting up multi-agent architecture.")

        # Extract parameters
        initial_query: str = kwargs.get("initial_query")
        llm_model: str = kwargs.get("llm_model")
        hil_mode: bool = kwargs.get("hil_mode", False)
        enable_internet: bool = kwargs.get("enable_internet", False)
        save_screenshots: bool = kwargs.get("save_screenshots", False)
        input_files: list = kwargs.get("input_files", [])

        # Log the parameters to help debug "NoneType" issues
        self.logger.info(
            f"Received parameters -> initial_query: {initial_query!r}, "
            f"llm_model: {llm_model!r}, hil_mode: {hil_mode}, "
            f"enable_internet: {enable_internet}, save_screenshots: {save_screenshots}, "
            f"input_files: {input_files}"
        )

        # If initial_query might be None, either raise an error or set a default
        if initial_query is None:
            self.logger.warning("No initial_query was provided — defaulting to empty string.")
            initial_query = ""

        # Check if we have at least input_files or internet
        if not input_files and not enable_internet:
            raise ValueError(
                "At least one of input_files or enable_internet must be True."
            )

        # Start timing
        _start_time = dt.now(self.ist_timezone)
        now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create logs dir using sanitized query
        sanitized_query = re.sub(r'[^a-zA-Z0-9]', '_', initial_query)[:20]
        logs_dir = os.path.join("logs", f"{sanitized_query}-{now}")
        os.makedirs(logs_dir, exist_ok=True)
        self.logger.info(f"Logs directory created at: {logs_dir}")

        # Configure event logger
        event_logger = logging.getLogger(EVENT_LOGGER_NAME)
        event_logger.setLevel(logging.INFO)
        log_file = os.path.join(logs_dir, f"log-{now}.jsonl")
        log_handler = LogHandler(filename=log_file)
        event_logger.handlers = [log_handler]
        self.logger.info(f"Event logs will be written to: {log_file}")

        # Create the runtime
        runtime = SingleThreadedAgentRuntime()
        self.logger.info("SingleThreadedAgentRuntime created.")

        # Create the LLM client
        client = self.__create_client(llm_model=llm_model)
        self.logger.info("Model client created.")

        # Register FileSurfer
        await FileSurfer.register(
            runtime, "file_surfer", lambda: FileSurfer(model_client=client)
        )
        file_surfer = AgentProxy(AgentId("file_surfer", "default"), runtime)
        self.logger.info("FileSurfer agent registered.")

        # Register UserProxy
        await UserProxy.register(
            runtime,
            "UserProxy",
            lambda: UserProxy(description="The current user interacting with you."),
        )
        user_proxy = AgentProxy(AgentId("UserProxy", "default"), runtime)
        self.logger.info("UserProxy agent registered.")

        # Build the agent list
        agent_list = []
        if input_files:
            agent_list.append(file_surfer)
        if hil_mode:
            agent_list.append(user_proxy)

        if enable_internet:
            await MultimodalWebSurfer.register(runtime, "WebSurfer", MultimodalWebSurfer)
            web_surfer = AgentProxy(AgentId("WebSurfer", "default"), runtime)
            agent_list.append(web_surfer)
            self.logger.info("MultimodalWebSurfer agent registered.")

        # Set max_time, max_rounds, etc.
        max_time = 25 * 60
        max_rounds = 120

        # Register LedgerOrchestrator
        await LedgerOrchestrator.register(
            runtime,
            "Orchestrator",
            lambda: LedgerOrchestrator(
                agents=agent_list,
                model_client=client,
                max_rounds=max_rounds,
                max_time=max_time,
                max_replans=1,
                max_stalls_before_replan=0,
                return_final_answer=True,
            ),
        )
        self.logger.info("LedgerOrchestrator registered.")

        # Start the runtime
        runtime.start()
        self.logger.info("Agent runtime started.")

        # Initialize WebSurfer if enabled
        if enable_internet:
            actual_surfer = await runtime.try_get_underlying_agent_instance(
                web_surfer.id, type=MultimodalWebSurfer
            )
            self.logger.info("Initializing MultimodalWebSurfer with headless browser.")
            await actual_surfer.init(
                model_client=client,
                downloads_folder=logs_dir,
                start_page="https://www.bing.com",
                browser_channel="chromium",
                headless=True,
                debug_dir=logs_dir,
                to_save_screenshots=save_screenshots,
            )

        # Log completion and timing
        _end_time = dt.now(self.ist_timezone)
        setup_time = (_end_time - _start_time).total_seconds()
        self.logger.info(f"Multi-Agent Architecture Setup time: {setup_time} s")

        # Return useful context
        return runtime, logs_dir, log_file, max_time, max_rounds, now
    def __create_client(self, llm_model):
        try:
            # Create an appropriate client
            print(llm_model)
            if llm_model.lower().__contains__("azure"):
                os.environ["CHAT_COMPLETION_PROVIDER"] = settings.CHAT_COMPLETION_PROVIDER
                os.environ["AZURE_OPENAI_API_KEY"] = settings.AZURE_OPENAI_API_KEY
                os.environ["AZURE_OPENAI_ENDPOINT"] = settings.AZURE_OPENAI_ENDPOINT
                os.environ["OPENAI_API_VERSION"] = settings.OPENAI_API_VERSION
                os.environ["AZURE_CLIENT_ID"] = settings.AZURE_CLIENT_ID
                os.environ["AZURE_TENANT_ID"] = settings.AZURE_TENANT_ID
                os.environ["AZURE_CLIENT_SECRET"] = settings.AZURE_CLIENT_SECRET
                client = create_completion_client_from_env(model="gpt-4o")
            if llm_model.lower().__contains__("openai"):
                os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
                # os.environ["OPENAI_API_KEY"] = (
                #     ""
                # )
                self.logger.info("Using OpenAI API key in environment")
                client = create_completion_client_from_env(model="gpt-4o")
            # elif llm_model in LLAMA_LLM_MODELS:
            elif llm_model.lower().__contains__("llama3"):
                os.environ["CHAT_COMPLETION_PROVIDER"] = "ollama"
                client = create_completion_client_from_env(
                    model="llama3.2-vision:11b-instruct-q4_K_M"
                )
            else:
                raise HTTPException(status_code=400, detail="Invalid LLM model.")
            return client
        except Exception as e:
            self.logger.exception(f"Error occurred while creating client | {e!s}")
            raise e

    async def _execute(self, content: str, runtime):
        self.logger.info("Executing orchestration.")
        # Replaced BroadcastMessage with ChatMessage
        # message = ChatMessage(content=content, sender="user", recipient="file_surfer_agent", timestamp=dt.now())
        message = BroadcastMessage(
            content=UserMessage(content=content, source="user"), request_halt=False
        )
        topic_id = TopicId(type="default", source="default")
        agent_id = AgentId(type="UserProxy", key="default")
        await runtime.publish_message(
            message=message, topic_id=topic_id, sender=agent_id
        )
        await runtime.stop_when_idle()

    def __extract_final_response_from_log_file(self, log_file, task_id):
        self.logger.info(
            f"Extracting orchestrator's final answer from log file for {task_id}"
        )
        final_answer = ""
        try:
            with open(log_file) as f:
                data = f.read()
                if data:
                    final_answers = [
                        json.loads(line).get("message", "")
                        for line in data.split("\n")
                        if line.strip()
                        and "Orchestrator (final answer)"
                        in json.loads(line).get("source", "")
                    ]
                    if len(final_answers):
                        final_answer = final_answers[-1].strip()
            if not final_answer:
                self.logger.warning(f"No final answer found in logs for {task_id}")
            else:
                self.logger.info(
                    f"Final answer from log file for {task_id}: {final_answer}"
                )
        except Exception as e:
            self.logger.error(
                f"Error occurred while extracting final answer from log file for {task_id} | {e!s}"
            )
        return final_answer

    async def start_task(self, agentic_task_request: AgenticTaskRequest) -> TaskResponse:
        self.logger.info(
            f"Starting Magentic multi-agent task with query: {agentic_task_request.query[:100]}"
        )
        try:
            (
                runtime,
                logs_dir,
                log_file,
                max_time,
                max_rounds,
                now,
            ) = await self._setup_architecture(
                initial_query=agentic_task_request.query,
                llm_model=agentic_task_request.llm_model,
                hil_mode=False,
                enable_internet=agentic_task_request.enable_internet,
                save_screenshots=True,
                input_files=agentic_task_request.files,
            )
            ORCHESTRATOR_INIT_PROMPT2 = """
            Date and time today is : {now}. Use it only if it is relevant.  
            User wants you to perform the following task:
            User Query: {initial_query}
            """
            if agentic_task_request.files:
                file_paths = str([file.file_local_path for file in agentic_task_request.files])
                ORCHESTRATOR_INIT_PROMPT2 += f"\n\nUser has also provided the following files: {file_paths}"

            content = ORCHESTRATOR_INIT_PROMPT2.format(
                initial_query=agentic_task_request.query, now=now
            )
            response = await self._execute(content, runtime)
            self.logger.info(f"Response from the framework: {response}")
            final_response = self.__extract_final_response_from_log_file(
                log_file, agentic_task_request.task_id
            )
            if final_response:
                status = TaskStatus.SUCCESS.value
            else:
                status = TaskStatus.FAILED.value
            self.logger.info(f"TaskID Completed | Status: {status}, Final Response: {final_response}")
            return final_response, status
        except Exception as e:
            self.logger.error(
                f"Error occurred while starting the task: {agentic_task_request.task_id} | {e!s}"
            )
            raise e
