import json
import os
import time
from typing import Dict, Any

import requests

from app.core.enums import TaskStatus, MultiAgentFrameworks
from app.core.logging import get_logger
from app.repository.task_repository import TaskRepository
from app.schemas.task import AgenticTaskRequest, TaskResponse, TaskRequest, TaskOutput, LiveStreamResponse
from app.services.maf.maf import MultiAgentFramework


class AM1(MultiAgentFramework):
    def __init__(self):
        self.name = "AG2"
        self.logger = get_logger()
        self.task_repository = TaskRepository()

    async def start_task(self, agentic_task_request: AgenticTaskRequest) -> TaskResponse:
        self.logger.info(
            f"Starting AG2 multi-agent system | task: {agentic_task_request.task_id} with query: {agentic_task_request.query[:100]}"
        )
        await self._setup_architecture(agentic_task_request.task_id, agentic_task_request.query)
        task_response: TaskResponse = await self._execute(agentic_task_request.task_id, agentic_task_request.query)
        return task_response

    async def _setup_architecture(self, task_id, query):
        pass

    async def _execute(self, task_id, query) -> TaskResponse:
        self.logger.info(f"Executing task: {task_id} in AM1 for {query[:100]}")
        response = ""
        browser_use = BrowserUse()
        browser_task_id = browser_use.create_task(instructions=query)
        self.logger.info(f"BrowserUse response: {browser_task_id}")
        task = await self.task_repository.get(task_id)
        await self.task_repository.update(task_id, {
            "task_metadata": task.task_metadata.update({"browser_task_id": browser_task_id})
        })
        browser_use_task_response: Dict = browser_use.get_task_details(browser_task_id)
        # yield str(task_response)
        self.logger.info(f"Task response: {browser_use_task_response}")
        if not task.task_metadata:
            task.task_metadata = {}
        updated_task = await self.task_repository.update(task_id, {
            "task_metadata": task.task_metadata.update({"web_surfer_url": browser_use_task_response.get("live_url")})
        })
        browser_use_task_response = browser_use.wait_for_completion(browser_task_id)
        # yield str(task_response)
        status = TaskStatus.SUCCESS.value if browser_use_task_response.get("status") == "finished" \
            else TaskStatus.FAILED.value if browser_use_task_response.get("status") == "failed" \
            else TaskStatus.IN_PROGRESS.value
        task_response = TaskResponse(
            task_id=updated_task.task_id.__str__(),
            status=status,
            task_request=TaskRequest(
                task_id=updated_task.task_id.__str__(),
                query=query,
                multi_agent_framework=updated_task.multi_agent_framework,
                llm_model=updated_task.llm_model,
                enable_internet=updated_task.enable_internet
            ),
            input_file_names=task.input_file_names,
            task_output=TaskOutput(
                final_response=browser_use_task_response.get("output"),
                output_file_urls=browser_use_task_response.get("output_files")
            ),
            live_stream_response=LiveStreamResponse(
                web_surfer_url=task.task_metadata.update({"web_surfer_url": browser_use_task_response.get("live_url")}),
            ),
            task_metadata=updated_task.task_metadata,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        self.logger.info(f"Task response: {task_response}")
        return task_response

class BrowserUse:
    API_KEY = os.getenv("BROWSER_API_KEY")
    BASE_URL = 'https://api.browser-use.com/api/v1'
    HEADERS = {'Authorization': f'Bearer {API_KEY}'}
    def __init__(self):
        pass

    # async def browser_use(self, task, llm_config, browser, agent_kwargs):
    #     pass
    #
    # @staticmethod
    # def _get_controller(self, llm_config):
    #     pass

    def create_task(self, instructions: str):
        """Create a new browser automation task"""
        response = requests.post(f'{self.BASE_URL}/run-task', headers=self.HEADERS, json={'task': instructions})
        return response.json()['id']

    def get_task_status(self, task_id: str):
        """Get current task status"""
        response = requests.get(f'{self.BASE_URL}/task/{task_id}/status', headers=self.HEADERS)
        return response.json()

    def get_task_details(self, task_id: str) -> Dict[str, Any]:
        """Get full task details including output"""
        response = requests.get(f'{self.BASE_URL}/task/{task_id}', headers=self.HEADERS)
        return response.json()

    def wait_for_completion(self, task_id: str, poll_interval: int = 2):
        """Poll task status until completion"""
        count = 0
        unique_steps = []
        while True:
            details = self.get_task_details(task_id)
            new_steps = details['steps']
            # use only the new steps that are not in unique_steps.
            if new_steps != unique_steps:
                for step in new_steps:
                    if step not in unique_steps:
                        print(json.dumps(step, indent=4))
                unique_steps = new_steps
            count += 1
            status = details['status']

            if status in ['finished', 'failed', 'stopped']:
                return details
            time.sleep(poll_interval)