from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.core.enums import MultiAgentFrameworks
from app.core.logging import get_logger, logger_file_name
from app.maf.impl.magentic_one import MagenticOne
from app.models.task import Task
from app.schemas.task import AgenticTaskRequest, TaskRequest

logger = get_logger(logger_file_name)

# Create sync engine and sessionmaker
sync_engine = create_engine(
    "postgresql://postgres:user@am1_postgres_db:5432/am1", echo=True
)
SyncSession = sessionmaker(sync_engine, autoflush=False, autocommit=False)


def create_task(task_request: TaskRequest, db: SyncSession):
    """Create a task synchronously."""
    logger.info(f"Received db type: {type(db)}")
    try:
        # Ensure query is provided
        if not task_request.query:
            raise HTTPException(status_code=400, detail="Query is required")

        # Get the multi-agent framework and LLM model
        multi_agent_framework = task_request.multi_agent_framework
        llm_model = (
            task_request.llm_model if task_request.llm_model else "openai-gpt-4o-mini"
        )

        # Validate multi-agent framework
        if multi_agent_framework not in [
            maf_name.value for maf_name in MultiAgentFrameworks.__members__.values()
        ]:
            logger.error(
                "Received invalid multi-agent framework: %s", multi_agent_framework
            )
            raise HTTPException(
                status_code=400, detail="Invalid multi-agent framework provided"
            )

        # Create the task instance
        task = Task(
            query=task_request.query,
            multi_agent_framework=multi_agent_framework,
            llm_model=llm_model,
            enable_internet=task_request.enable_internet,
        )

        # Begin transaction with sync session
        with db.begin():
            db.add(task)  # Add the task to the session

        # Commit the changes and return the task ID
        db.commit()

        return {"task_id": str(task.task_id)}

    except SQLAlchemyError as db_err:
        # Rollback if there's an error
        logger.exception(f"Database error during task creation: {db_err}")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Database error occurred during task creation"
        )

    except Exception as e:
        # Catch other errors
        logger.exception(f"Unexpected error creating task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")


async def start_task(task_id: str, db: SyncSession):
    """Start a task processing synchronously."""
    try:
        # Fetch the task from the database
        task = db.query(Task).filter(Task.task_id == task_id).first()

        # If task is not found, raise 404 error
        if not task:
            logger.error(f"Task with ID {task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info(f"Task with ID {task_id} found: {task}")

        # Initialize the corresponding framework based on the task's multi_agent_framework
        if task.multi_agent_framework == MultiAgentFrameworks.MAGENTIC_ONE.value:
            maf = MagenticOne()
        else:
            logger.error(
                f"Unsupported framework: {task.multi_agent_framework} for task ID {task_id}"
            )
            raise HTTPException(
                status_code=400, detail="Unsupported multi-agent framework"
            )

        # Create the request object for the agentic task
        agentic_task_request = AgenticTaskRequest(
            task_id=task_id,
            query=task.query,
            llm_model=task.llm_model,
            enable_internet=task.enable_internet,
        )

        # Start the task via the framework and capture the response
        response, status = await maf.start_task(agentic_task_request)
        update_task_details(
            task_id=task_id, final_response=response, status=status, db=db
        )
        # Return the response from the framework
        return {"response": response}

    except HTTPException as http_err:
        # If it's an HTTP exception (like task not found or unsupported framework), log and raise it
        logger.error(f"HTTP Error for task ID {task_id}: {http_err!s}")
        raise http_err

    except Exception as e:
        # General error handling (log it and return a generic error response)
        logger.exception(f"Error starting task with ID {task_id}: {e!s}")
        raise HTTPException(status_code=500, detail="Failed to start task")


def get_task_details(task_id: str, db: SyncSession):
    """Retrieve a task by its ID synchronously."""
    try:
        # Use SQLAlchemy ORM to retrieve a single task by its ID
        task = db.query(Task).filter(Task.task_id == task_id).first()

        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            return {"error": "Task not found", "task_id": task_id}

        logger.info(f"Retrieved task with ID {task_id} from database.")

        # Convert ORM object to a dictionary (Ensure Task model has necessary attributes)
        return {
            "task": {
                "id": task.task_id,
                "query": task.query,
                "status": task.status,
                "multi_agent_framework": task.multi_agent_framework,
                "llm_model": task.llm_model,
                "final_response": task.final_response,
                "created_at": (
                    task.created_at.isoformat() if task.created_at else None
                ),
                "updated_at": (
                    task.updated_at.isoformat() if task.updated_at else None
                ),
            }
        }

    except Exception as e:
        logger.exception(f"Error fetching task with ID {task_id}: {e!s}")
        return {"error": "Failed to fetch task", "message": str(e)}


def get_all_tasks(offset: int, limit: int, db: SyncSession):
    """Retrieve all tasks synchronously with pagination."""
    try:
        # Use SQLAlchemy ORM to retrieve tasks with pagination
        tasks = db.query(Task).limit(limit).offset(offset).all()

        logger.info(
            f"Retrieved {len(tasks)} tasks from database (limit={limit}, offset={offset})"
        )

        # Convert ORM objects to dictionaries (Ensure Task model has necessary attributes)
        return {
            "tasks": [
                {
                    "id": task.task_id,
                    "query": task.query,  # Replace with actual attributes in your Task model
                    "status": task.status,
                    "multi_agent_framework": task.multi_agent_framework,
                    "llm_model": task.llm_model,
                    "final_response": task.final_response,
                    "created_at": (
                        task.created_at.isoformat() if task.created_at else None
                    ),
                    "updated_at": (
                        task.updated_at.isoformat() if task.updated_at else None
                    ),
                }
                for task in tasks
            ]
        }

    except Exception as e:
        logger.exception(f"Error fetching tasks: {e!s}")
        return {"error": "Failed to fetch tasks", "message": str(e)}


def update_task_details(
    task_id: str, final_response: str, status: str, db: SyncSession
):
    """Update task details synchronously."""
    try:
        # Step 1: Retrieve the task by ID
        task = db.query(Task).filter(Task.task_id == task_id).first()

        # Step 2: Check if task exists
        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            return {"error": "Task not found", "task_id": task_id}

        # Step 3: Update task fields with provided values
        updated_data = {
            "final_response": final_response,
            "status": status,
        }

        for key, value in updated_data.items():
            if hasattr(task, key):
                setattr(task, key, value)
                logger.info(f"Updated {key} for task ID {task_id}.")
            else:
                logger.warning(f"Invalid field '{key}' for task update.")

        # Step 4: Commit the changes to the database
        db.commit()

        # Log the successful update
        logger.info(f"Successfully updated task with ID {task_id}.")

        # Step 5: Return updated task as dictionary
        return {
            "task": {
                "id": task.task_id,
                "query": task.query,  # Replace with actual attributes from the Task model
                "status": task.status,
                "multi_agent_framework": task.multi_agent_framework,
                "llm_model": task.llm_model,
                "final_response": task.final_response,
                "created_at": (
                    task.created_at.isoformat() if task.created_at else None
                ),
                "updated_at": (
                    task.updated_at.isoformat() if task.updated_at else None
                ),
            }
        }

    except Exception as e:
        # Step 6: Error handling - Capture the exception and log it.
        logger.exception(f"Error updating task with ID {task_id}: {e!s}")
        return {"error": "Failed to update task", "message": str(e)}
