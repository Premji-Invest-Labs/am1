import logging
import os

from dotenv import load_dotenv

from app.core.enums import TaskStatus
from app.core.logging import get_logger
from app.schemas.task import AgenticTaskRequest, TaskResponse
from app.services.maf.maf import MultiAgentFramework
from autogen import AssistantAgent, UserProxyAgent, LLMConfig, ChatResult
from autogen.agents.experimental import DeepResearchAgent

load_dotenv()


OAI_CONFIG_LIST = [
  {
    "model": "gpt-4o",
    "api_key": os.environ.get("OPENAI_API_KEY")
  }
]

class AG2(MultiAgentFramework):
    def __init__(self):
        self.name = "AG2"
        self.logger = get_logger()
        # self.llm_config = LLMConfig.from_json(path="OAI_CONFIG_LIST")
        self.llm_config = LLMConfig(config_list=OAI_CONFIG_LIST)

    async def start_task(self, agentic_task_request: AgenticTaskRequest) -> TaskResponse:
        self.logger.info(
            f"Starting AG2 multi-agent system | task: {agentic_task_request.task_id} with query: {agentic_task_request.query[:100]}"
        )
        response = await self._execute(agentic_task_request.task_id, agentic_task_request.query)
        if response:
            status = TaskStatus.SUCCESS.value
        else:
            status = TaskStatus.FAILED.value
        return response, status

    async def _execute(self, task_id: str, user_query: str) -> str:
        return await self._func3(task_id, user_query)

    async def _func1(self, task_id: str, user_query: str):
        with self.llm_config:
                assistant = AssistantAgent("assistant")
        user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False})
        chat_result: ChatResult = user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
        # This initiates an automated chat between the two agents to solve the task
        self.logger.info(f"TaskID: {task_id}, Chat result: {chat_result}")
        return chat_result.summary

    async def _func2(self, task_id: str, user_query: str):
        from autogen import ConversableAgent

        with self.llm_config:
            # Create an AI agent
            assistant = ConversableAgent(
                name="assistant",
                system_message="You are an assistant that responds concisely.",
                human_input_mode="NEVER"
            )

            # Create another AI agent
            fact_checker = ConversableAgent(
                name="fact_checker",
                system_message="You are a fact-checking assistant.",
                human_input_mode="NEVER"
            )

        # Start the conversation
        chat_result: ChatResult = assistant.initiate_chat(
            recipient=fact_checker,
            message=user_query,
            max_turns=2
        )
        self.logger.info(f"TaskID: {task_id}, Chat result: {chat_result}")
        return chat_result.summary

    async def _func3(self, task_id: str, user_query: str):
        # from autogen import LLMConfig

        # llm_config = LLMConfig(
        #     config_list=[{"api_type": "openai", "model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}],
        # )
        import json
        agent = DeepResearchAgent(
            name="DeepResearchAgent",
            llm_config=json.loads(self.llm_config.model_dump_json()),
            # is_termination_msg=f"When you think you have either found answer for query or are in a loop/not making progress: {user_query}, end it!"
        )

        # message = "What was the impact of DeepSeek on stock prices and why?"

        result = agent.run(
            message=user_query,
            tools=agent.tools,
            max_turns=2,
            user_input=False,
            summary_method="reflection_with_llm",
        )

        self.logger.info(f"TaskID: {task_id}, Chat result: {result}")
        return result.summary