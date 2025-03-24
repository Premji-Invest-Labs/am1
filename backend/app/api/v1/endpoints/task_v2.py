from typing import Any

from dependencies import get_task_service
from fastapi import APIRouter, Depends
from models import Task, TaskCreate
from service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[Task])
async def get_tasks(
    task_service: TaskService = Depends(get_task_service)
) -> list[Task]:
    """Get all tasks"""
    return await task_service.get_all_tasks()

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    """Get a specific task by ID"""
    return await task_service.get_task(task_id)

@router.post("/", response_model=Task, status_code=201)
async def create_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    """Create a new task"""
    return await task_service.create_task(task)

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_data: dict[str, Any],
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    """Update an existing task"""
    return await task_service.update_task(task_id, task_data)

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> dict[str, str]:
    """Delete a task"""
    return await task_service.delete_task(task_id)