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
from autogen_ext.models.llama.config import LLAMA_LLM_MODELS
from autogen_magentic_one.agents.file_surfer import FileSurfer
from autogen_magentic_one.agents.multimodal_web_surfer import MultimodalWebSurfer
from autogen_magentic_one.agents.orchestrator import LedgerOrchestrator
from autogen_magentic_one.agents.user_proxy import UserProxy
from autogen_magentic_one.messages import BroadcastMessage
from autogen_magentic_one.utils import LogHandler, create_completion_client_from_env
from fastapi import HTTPException

from app.core.settings import settings
from app.maf.maf import MultiAgentFramework
from app.schemas.task import AgenticTaskRequest


class MagenticOne(MultiAgentFramework):
    def __init__(self):
        self.ist_timezone = pytz.timezone("Asia/Kolkata")
        self.logger = logging.getLogger(__name__)

    async def _setup_architecture(self, **kwargs: Any):
        self.logger.info("Setting up multi-agent architecture.")
        initial_query: str = kwargs.get("initial_query")
        llm_model: str = kwargs.get("llm_model")
        hil_mode: bool = kwargs.get("hil_mode", False)
        enable_internet: bool = kwargs.get("enable_internet", False)
        save_screenshots: bool = kwargs.get("save_screenshots", False)
        input_files: list = kwargs.get("input_files", [])
        if not input_files and not enable_internet:
            raise ValueError(
                "At least one of input_files or enable_internet must be True."
            )
        _start_time = dt.now(self.ist_timezone)
        now = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
        logs_dir = os.path.join(
            "logs", f"{re.sub(r'[^a-zA-Z0-9]', '_', initial_query)[:20]}-{now}"
        )
        os.makedirs(logs_dir, exist_ok=True)
        logger = logging.getLogger(EVENT_LOGGER_NAME)
        logger.setLevel(logging.INFO)
        log_file = os.path.join(logs_dir, f"log-{now}.jsonl")
        log_handler = LogHandler(filename=log_file)
        logger.handlers = [log_handler]
        # Create the runtime.
        runtime = SingleThreadedAgentRuntime()

        client = self.__create_client(llm_model=llm_model)

        await FileSurfer.register(
            runtime, "file_surfer", lambda: FileSurfer(model_client=client)
        )
        file_surfer = AgentProxy(AgentId("file_surfer", "default"), runtime)

        await UserProxy.register(
            runtime,
            "UserProxy",
            lambda: UserProxy(description="The current user interacting with you."),
        )
        user_proxy = AgentProxy(AgentId("UserProxy", "default"), runtime)

        agent_list = []
        if input_files:
            agent_list.append(file_surfer)
        if hil_mode:
            agent_list.append(user_proxy)
        if enable_internet:
            await MultimodalWebSurfer.register(
                runtime, "WebSurfer", MultimodalWebSurfer
            )
            web_surfer = AgentProxy(AgentId("WebSurfer", "default"), runtime)
            agent_list.append(web_surfer)
        max_time = 15 * 60
        max_rounds = 40
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
        runtime.start()

        if enable_internet:
            actual_surfer = await runtime.try_get_underlying_agent_instance(
                web_surfer.id, type=MultimodalWebSurfer
            )
            await actual_surfer.init(
                model_client=client,
                downloads_folder=logs_dir,
                start_page="https://www.bing.com",
                browser_channel="chromium",
                headless=True,
                debug_dir=logs_dir,
                to_save_screenshots=save_screenshots,
            )
        _end_time = dt.now(self.ist_timezone)
        logger.info(
            f"Multi-Agent Architecture Setup time: {(_end_time - _start_time).total_seconds()} s"
        )
        return runtime, logs_dir, log_file, max_time, max_rounds, now

    def __create_client(self, llm_model):
        # Create an appropriate client
        print(llm_model)
        if llm_model.__contains__("azure"):
            raise ValueError("Azure GPT-4o is not supported.")
        if llm_model.__contains__("openai"):
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
            # os.environ["OPENAI_API_KEY"] = (
            #     ""
            # )
            print(settings.OPENAI_API_KEY)
            self.logger.info(f"Using OpenAI API key: {os.environ['OPENAI_API_KEY']}")
            client = create_completion_client_from_env(model="gpt-4o")
        elif llm_model in LLAMA_LLM_MODELS:
            os.environ["CHAT_COMPLETION_PROVIDER"] = "ollama"
            client = create_completion_client_from_env(
                model="llama3.2-vision:11b-instruct-q4_K_M"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid LLM model.")
        return client

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

    async def start_task(self, agentic_task_request: AgenticTaskRequest):
        self.logger.info(
            f"Starting multi-agent task with query: {agentic_task_request.query[:100]}"
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
            content = ORCHESTRATOR_INIT_PROMPT2.format(
                initial_query=agentic_task_request.query, now=now
            )
            response = await self._execute(content, runtime)
            self.logger.info(f"Response from the framework: {response}")
            final_response = self.__extract_final_response_from_log_file(
                log_file, agentic_task_request.task_id
            )
            if final_response:
                status = "success"
            else:
                status = "failure"
            return final_response, status
        except Exception as e:
            self.logger.error(
                f"Error occurred while starting the task: {agentic_task_request.task_id} | {e!s}"
            )
            raise e
