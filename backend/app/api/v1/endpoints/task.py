from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.task import TaskRequest, TaskResponse
from app.services import task_service

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task_request: TaskRequest, db: AsyncSession = Depends(get_db)):
    """Create a new task."""
    return await task_service.create_task(task_request, db)


@router.post("/{task_id}/upload", response_model=TaskResponse)
async def upload_file_to_task(
    task_id: str,
    input_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Upload file to an existing task."""
    return await task_service.upload_file_to_task(task_id, input_file)


@router.post("/{task_id}/start", response_model=TaskResponse)
async def start_task(task_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Start an existing task."""
    return await task_service.start_task(task_id, background_tasks, db)


@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: str):
    """Retrieve details of a specific task."""
    return await task_service.get_task_details(task_id)


@router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a paginated list of tasks."""
    return await task_service.get_all_tasks(offset, limit, db)
