from typing import Any

from fastapi import HTTPException
from models import Task, TaskCreate
from repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def get_all_tasks(self) -> list[Task]:
        """Get all tasks with business logic applied"""
        try:
            tasks_data: list[dict[str, Any]] = await self.repository.get_all_tasks()
            return [Task(**task) for task in tasks_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {e!s}")

    async def get_task(self, task_id: int) -> Task:
        """Get a specific task with business logic applied"""
        try:
            task_data: dict[str, Any] | None = await self.repository.get_task_by_id(task_id)
            if not task_data:
                raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
            return Task(**task_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch task: {e!s}")

    async def create_task(self, task: TaskCreate) -> Task:
        """Create a new task with business logic applied"""
        try:
            task_data: dict[str, Any] = await self.repository.create_task(task)
            return Task(**task_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create task: {e!s}")

    async def update_task(self, task_id: int, task_data: dict[str, Any]) -> Task:
        """Update a task with business logic applied"""
        try:
            # First check if the task exists
            existing_task: dict[str, Any] | None = await self.repository.get_task_by_id(task_id)
            if not existing_task:
                raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

            # Then update it
            updated_task: dict[str, Any] | None = await self.repository.update_task(task_id, task_data)
            if not updated_task:
                raise HTTPException(status_code=500, detail="Failed to update task")

            return Task(**updated_task)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update task: {e!s}")

    async def delete_task(self, task_id: int) -> dict[str, str]:
        """Delete a task with business logic applied"""
        try:
            # First check if the task exists
            existing_task: dict[str, Any] | None = await self.repository.get_task_by_id(task_id)
            if not existing_task:
                raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

            # Then delete it
            result: bool = await self.repository.delete_task(task_id)
            if not result:
                raise HTTPException(status_code=500, detail="Failed to delete task")

            return {"message": f"Task with ID {task_id} deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete task: {e!s}")
