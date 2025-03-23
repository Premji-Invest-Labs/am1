from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from models import Task, TaskCreate
from service import TaskService
from repository import TaskRepository
from database import Database
from dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
async def get_tasks(
    task_service: TaskService = Depends(get_task_service)
) -> List[Task]:
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
    task_data: Dict[str, Any],
    task_service: TaskService = Depends(get_task_service)
) -> Task:
    """Update an existing task"""
    return await task_service.update_task(task_id, task_data)

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
) -> Dict[str, str]:
    """Delete a task"""
    return await task_service.delete_task(task_id)