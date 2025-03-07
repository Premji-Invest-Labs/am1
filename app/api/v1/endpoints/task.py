from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.database import get_relational_db
from app.schemas.task import TaskRequest
from app.services import task_service

router = APIRouter()


@router.post("/task")
async def create_task(
    task_request: TaskRequest, db: AsyncSession = Depends(get_relational_db)
):
    """Create a new task.

    Args:
        task_request (TaskRequest): The data required to create the task.
        db (AsyncSession): The database session, injected via Depends.

    Returns:
        JSON response: The created task object with its details.

    """
    return task_service.create_task(task_request, db=db)


@router.post("/task/{task_id}/start")
async def start_task(task_id: str, db: AsyncSession = Depends(get_relational_db)):
    """Start a specific task by its ID.

    Args:
        task_id (str): The ID of the task to start.
        db (AsyncSession): The database session, injected via Depends.

    Returns:
        JSON response: The updated task object after it has been started.

    """
    return await task_service.start_task(task_id, db)


@router.get("/task/{task_id}")
async def read_task(task_id: str, db: AsyncSession = Depends(get_relational_db)):
    """Retrieve the details of a specific task by its ID.

    Args:
        task_id (str): The ID of the task to retrieve.
        db (AsyncSession): The database session, injected via Depends.

    Returns:
        JSON response: The task details.

    """
    return task_service.get_task_details(task_id, db)


@router.get("/tasks")
async def get_all_tasks(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_relational_db)
):
    """Retrieve a list of all tasks with pagination.

    Args:
        offset (int): The number of tasks to skip before returning results.
        limit (int): The maximum number of tasks to return.
        db (AsyncSession): The database session, injected via Depends.

    Returns:
        JSON response: A list of tasks.

    """
    return task_service.get_all_tasks(offset, limit, db)
