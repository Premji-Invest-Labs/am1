from datetime import datetime
from typing import Any

from models import TaskCreate


class TaskRepository:
    def __init__(self, database):
        self.db = database

    async def get_all_tasks(self) -> list[dict[str, Any]]:
        """Fetch all tasks from the database"""
        async with self.db.connection() as conn:
            rows = await conn.fetch(
                """
                SELECT id, title, description, is_completed, created_at, updated_at
                FROM tasks
                ORDER BY created_at DESC
                """
            )
            return [dict(row) for row in rows]

    async def get_task_by_id(self, task_id: int) -> dict[str, Any] | None:
        """Fetch a task by its ID"""
        async with self.db.connection() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, title, description, is_completed, created_at, updated_at
                FROM tasks
                WHERE id = $1
                """,
                task_id
            )
            return dict(row) if row else None

    async def create_task(self, task: TaskCreate) -> dict[str, Any]:
        """Create a new task"""
        async with self.db.connection() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO tasks (title, description, is_completed, created_at)
                VALUES ($1, $2, $3, $4)
                RETURNING id, title, description, is_completed, created_at, updated_at
                """,
                task.title,
                task.description,
                task.is_completed,
                datetime.now()
            )
            return dict(row)

    async def update_task(self, task_id: int, task_data: dict[str, Any]) -> dict[str, Any] | None:
        """Update an existing task"""
        # Build the dynamic update query
        set_values: list[str] = []
        params: list[Any] = []
        param_index: int = 1

        for key, value in task_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                set_values.append(f"{key} = ${param_index}")
                params.append(value)
                param_index += 1

        # Add updated_at timestamp
        set_values.append(f"updated_at = ${param_index}")
        params.append(datetime.now())
        param_index += 1

        # Add task_id as the last parameter
        params.append(task_id)

        if not set_values:
            return None

        query = f"""
            UPDATE tasks
            SET {', '.join(set_values)}
            WHERE id = ${param_index}
            RETURNING id, title, description, is_completed, created_at, updated_at
        """

        async with self.db.connection() as conn:
            row = await conn.fetchrow(query, *params)
            return dict(row) if row else None

    async def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        async with self.db.connection() as conn:
            result = await conn.execute(
                """
                DELETE FROM tasks
                WHERE id = $1
                """,
                task_id
            )
            # Parse the DELETE result ('DELETE 1' means one row was deleted)
            return "DELETE 1" in result