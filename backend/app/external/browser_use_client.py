import asyncio
import json
import os
from typing import List

import httpx
from dotenv import load_dotenv

from app.core.logging import get_logger

load_dotenv()

API_KEY = os.getenv("BROWSER_USE_API_KEY")
BASE_URL = "https://api.browser-use.com/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BROWSER_USE_TIMEOUT_IN_SECONDS = 60
if not API_KEY:
    raise ValueError("Missing BROWSER_USE_API_KEY in environment variables.")

logger = get_logger()


async def create_task(instructions: str) -> str:
    """Create a new browser automation task"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/run-task",
            headers=HEADERS,
            json={"task": instructions},
            timeout=BROWSER_USE_TIMEOUT_IN_SECONDS,
        )
        response.raise_for_status()
        return response.json()["id"]


async def get_task_status(task_id: str) -> dict:
    """Get current task status"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/task/{task_id}/status",
            headers=HEADERS,
            timeout=BROWSER_USE_TIMEOUT_IN_SECONDS,
        )
        response.raise_for_status()
        return response.json()


async def get_task_details(task_id: str) -> dict:
    """Get full task details including output"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/task/{task_id}",
            headers=HEADERS,
            timeout=BROWSER_USE_TIMEOUT_IN_SECONDS,
        )
        response.raise_for_status()
        return response.json()


async def wait_for_completion(task_id: str, poll_interval: int = 2) -> dict:
    """Poll task status until completion, print unique steps"""
    unique_steps: List[dict] = []

    while True:
        details = await get_task_details(task_id)
        steps = details.get("steps", [])

        for step in steps:
            if step not in unique_steps:
                logger.info(json.dumps(step, indent=4))
                unique_steps.append(step)

        status = details.get("status")
        if status in {"finished", "failed", "stopped"}:
            return details

        await asyncio.sleep(poll_interval)
