from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select

from app.core.logging import get_logger
from app.db.database import get_db
from app.models.task import Task


class TaskRepository:
    def __init__(self):
        # self.db: AsyncSession = get_db()
        self.logger = get_logger()

    async def create(self, task: Task) -> type[Task] | None:
        # self.db.add(task)
        # await self.db.commit()
        # await self.db.refresh(task)
        # return await self.get(task.task_id)
        try:
            async for session in get_db():
                session.add(task)
                await session.commit()
                await session.refresh(task)
                self.logger.info(f"Task {task.task_id} created successfully.")
                return await self.get(task.task_id)
        except Exception as e:
            self.logger.error(f"Error creating task: {e}")
            return None

    async def get(self, task_id: str) -> type[Task] | None:
        # result = await self.db.execute(select(Task).filter(Task.task_id == task_id))
        # return result.scalars().first()
        # async for session in get_db():
        #     task = session.query(Task).filter(Task.task_id == task_id).first()
        #     self.logger.info(f"get task {task_id} from db {task}")
        #     return task
        async for session in get_db():
            # For SQLAlchemy 1.4+ with async sessions, use select instead of query

            # Using select and execute for async sessions
            result = await session.execute(select(Task).filter(Task.task_id == task_id))
            task = result.scalars().first()
            return task

    async def update(self, task_id: str, update_data: dict) -> type[Task] | None:
        """Generic function to update any field(s) in a task.

        Args:
            task_id (str): The ID of the task to update.
            update_data (Dict): Dictionary of fields to update.

        Returns:
            TaskResponse: The updated task response.

        """
        try:
            self.logger.info(f"Updating task {task_id}. Update Data: {update_data}")
            async for session in get_db():
                # Import select if not already imported
                from sqlalchemy import select

                # Fetch the task from the database
                result = await session.execute(select(Task).filter(Task.task_id == task_id))
                task = result.scalars().first()

                if not task:
                    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

                # Update fields
                for field, value in update_data.items():
                    if hasattr(task, field):
                        setattr(task, field, value)

                task.updated_at = datetime.utcnow()

                # Commit changes
                await session.commit()
                await session.refresh(task)

                # Fetch the updated task
                result = await session.execute(select(Task).filter(Task.task_id == task_id))
                updated_task = result.scalars().first()

                self.logger.info(f"Task {task_id} updated successfully.")
                return updated_task

        except HTTPException as e:
            raise e  # Preserve known HTTP errors
        except Exception as e:
            self.logger.error(f"Error updating task {task_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to update task")

    async def delete(self, task_id: str) -> bool | None:
        """Delete a task from the database.

        Args:
            task_id (str): The ID of the task to delete.

        Returns:
            bool: True if task was deleted successfully.

        """
        try:
            async for session in get_db():
                from sqlalchemy import select

                # Fetch the task from the database
                result = await session.execute(select(Task).filter(Task.task_id == task_id))
                task = result.scalars().first()

                if not task:
                    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

                # Delete the task
                await session.delete(task)
                await session.commit()

                self.logger.info(f"Task with ID {task_id} deleted successfully.")
                return True

        except HTTPException as e:
            raise e  # Preserve known HTTP errors
        except Exception as e:
            self.logger.error(f"Error deleting task {task_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete task")

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[type[Task]]:
        """Get all tasks with pagination.

        Args:
            offset (int): Number of records to skip.
            limit (int): Maximum number of records to return.

        Returns:
            list[Type[Task]]: List of task objects.

        """
        try:
            async for session in get_db():
                from sqlalchemy import select

                # Execute the query with pagination
                result = await session.execute(select(Task).offset(offset).limit(limit))
                return result.scalars().all()

        except Exception as e:
            self.logger.error(f"Error retrieving tasks: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve tasks")