import httpx
from fastapi import APIRouter, HTTPException

from app.external.browser_use_client import (
    create_task,
    get_task_status,
    get_task_details,
    wait_for_completion
)
from app.schemas.web_task import (
    WebCreateTaskRequest,
    WebCreateTaskResponse,
    WebTaskResponse,
    WebTaskStatusResponse
)

router = APIRouter(
    prefix="/web_task",
    tags=["Web Tasks"],
    responses={404: {"description": "Not found"}}
)


@router.post("/create-task", response_model=WebCreateTaskResponse, status_code=201,
             summary="Create a new browser-use task")
async def api_create_task(req: WebCreateTaskRequest):
    """
    Creates a new browser automation task based on a natural language query.

    Args:
        req (WebCreateTaskRequest): Contains the query/instruction for the browser task.

    Returns:
        WebCreateTaskResponse: Contains the generated task ID.
    """
    try:
        task_id = await create_task(req.query)
        return {"task_id": task_id}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/task/{task_id}/status", response_model=WebTaskStatusResponse, summary="Get the current status of a task")
async def api_get_task_status(task_id: str):
    try:
        status = await get_task_status(task_id)

        # If status is a plain string, wrap it
        if isinstance(status, str):
            return {"status": status}

        return status
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/task/{task_id}/details", response_model=WebTaskResponse, summary="Get full details of a task")
async def api_get_task_details(task_id: str):
    """
    Retrieves all metadata, steps, and output related to a specific task.

    Args:
        task_id (str): The ID of the task.

    Returns:
        WebTaskResponse: Task info including status, steps, and result.
    """
    try:
        return await get_task_details(task_id)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/task/{task_id}/wait-completion", response_model=WebTaskResponse,
            summary="Poll and wait until task is complete")
async def api_wait_for_completion(task_id: str):
    """
    Polls the task status until it's in a terminal state (finished, failed, or stopped),
    and returns the final output.

    Args:
        task_id (str): The ID of the task.

    Returns:
        WebTaskResponse: Final task result and steps.
    """
    try:
        return await wait_for_completion(task_id)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
