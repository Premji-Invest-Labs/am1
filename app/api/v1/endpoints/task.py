from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask

from app.repository.database import get_relational_db
from app.schemas.task import TaskRequest
from app.services import task_service

router = APIRouter()


@router.post("/task")
async def create_task(
    task_request: TaskRequest, db: AsyncSession = Depends(get_relational_db)
):
    return task_service.create_task(task_request, db=db)


@router.post("/task/{task_id}/start")
async def start_task(task_id: str, db: AsyncSession = Depends(get_relational_db)):
    return await task_service.start_task(task_id, db)


@router.get("/task/{task_id}")
async def read_task(task_id: str, db: AsyncSession = Depends(get_relational_db)):
    return task_service.get_task_details(task_id, db)


@router.get("/tasks")
async def get_all_tasks(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_relational_db)
):
    return task_service.get_all_tasks(offset, limit, db)
