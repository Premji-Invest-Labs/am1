from fastapi import Depends
from database import Database
from repository import TaskRepository
from service import TaskService
from typing import Callable, Iterator
from config import settings

def get_database() -> Database:
    """Get database instance"""
    return Database(settings.DATABASE_URL)

def get_task_repository(
    db: Database = Depends(get_database)
) -> TaskRepository:
    """Get task repository instance"""
    return TaskRepository(db)

def get_task_service(
    repository: TaskRepository = Depends(get_task_repository)
) -> TaskService:
    """Get task service instance"""
    return TaskService(repository)