import os

from fastapi import BackgroundTasks, HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.enums import MultiAgentFrameworks, TaskStatus
from app.core.logging import get_logger
from app.models.task import Task
from app.repository.task_repository import TaskRepository
from app.schemas.task import (
    AgenticTaskRequest,
    LiveStreamResponse,
    LLMFileInput,
    TaskOutput,
    TaskRequest,
    TaskResponse,
)
from app.services.maf.impl.am1 import BrowserUse

logger = get_logger()

task_repository = TaskRepository()

# # Create sync engine and sessionmaker
# sync_engine = create_engine(
#     "postgresql://postgres:user@am1_postgres_db:5432/am1", echo=True
# )
# SyncSession = sessionmaker(sync_engine, autoflush=False, autocommit=False)


async def create_task(task_request: TaskRequest, db: AsyncSession) -> TaskResponse:
    """Create a task synchronously."""
    if task_request.task_id:
        update_data = {
            "query": task_request.query,
            "multi_agent_framework": task_request.multi_agent_framework,
            "llm_model": task_request.llm_model,
            "enable_internet": task_request.enable_internet,
        }
        task_response = await update_task(task_request.task_id, update_data)
        logger.info(f"Task {task_request.task_id} updated")
        return task_response
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
            status=TaskStatus.CREATED.value,
            task_metadata={}
        )
        created_task = await task_repository.create(task)

        # async with db.acquire() as conn:
        #     async with conn.transaction():
        #         task = await conn.fetchrow(
        #             """INSERT INTO tasks (query, multi_agent_framework, llm_model, enable_internet)
        #                VALUES ($1, $2, $3, $4) RETURNING task_id""",
        #             task_request.query, multi_agent_framework, llm_model, task_request.enable_internet
        #         )
        task_response = TaskResponse(
            task_id=str(created_task.task_id),
            status=created_task.status,
            task_request=TaskRequest(
                query=task_request.query,
                multi_agent_framework=task_request.multi_agent_framework,
                llm_model=task_request.llm_model,
                enable_internet=task_request.enable_internet,
            ),
            input_file_names=created_task.input_file_names,
            task_metadata=created_task.task_metadata,
            created_at=created_task.created_at.isoformat() if created_task.created_at else None,
            updated_at=created_task.updated_at.isoformat() if created_task.updated_at else None,
        )
        logger.info(f"Created task {task_response.task_id}")
        return task_response

    except SQLAlchemyError as db_err:
        # Rollback if there's an error
        logger.error(f"Database error during task creation: {db_err}")
        # db.rollback()
        raise HTTPException(
            status_code=500, detail="Database error occurred during task creation"
        )

    except Exception as e:
        # Catch other errors
        logger.exception(f"Unexpected error creating task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")


async def start_task(task_id: str, background_tasks: BackgroundTasks, db: AsyncSession) -> TaskResponse:
    """Start a task processing synchronously."""
    try:
        # # Fetch the task from the database
        # stmt = select(Task).where(Task.task_id == task_id)
        #
        # # Execute the statement asynchronously
        # result = await db.execute(stmt)
        #
        # # Fetch the first result
        # task = result.scalars().first()
        task = await task_repository.get(task_id)
        # task = db.query(Task).filter(Task.task_id == task_id).first()
        # async with db.acquire() as conn:
        #     task = await conn.fetchrow("SELECT * FROM tasks WHERE task_id = $1", task_id)

        # If task is not found, raise 404 error
        if not task:
            logger.error(f"Task with ID {task_id} not found")
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info(f"Task with ID {task_id} found: {task}")

        background_tasks.add_task(execute_task, task, db)
        # update_task_details(
        #     task_id=task_id, final_response=response, status=status, db=db
        # )
        update_data = {
            "status": TaskStatus.IN_PROGRESS.value,
        }
        await update_task(str(task_id), update_data)
        # await update_task_details(task_id, response, status, db)

        # Return the response from the framework
        task_response = TaskResponse(
            task_id=task.task_id.__str__(),
            status=TaskStatus.IN_PROGRESS.value,
            task_request=TaskRequest(
                query=task.query,
                multi_agent_framework=task.multi_agent_framework,
                llm_model=task.llm_model,
                enable_internet=task.enable_internet,
            ),
            input_file_names=task.input_file_names,
            task_metadata=task.task_metadata,
            created_at=task.created_at.isoformat() if task.created_at else None,
            updated_at=task.updated_at.isoformat() if task.updated_at else None,
        )
        logger.info(f"Started task with ID {task_id}.")
        return task_response

    except HTTPException as http_err:
        # If it's an HTTP exception (like task not found or unsupported framework), log and raise it
        logger.error(f"HTTP Error for task ID {task_id}: {http_err!s}")
        raise http_err

    except Exception as e:
        # General error handling (log it and return a generic error response)
        logger.error(f"Error starting task with ID {task_id}: {e!s}")
        raise HTTPException(status_code=500, detail="Failed to start task")


async def execute_task(task: TaskResponse, db: AsyncSession):
    logger.info(f"Executing task with ID {task.task_id} in background. MAS Framework: {task.multi_agent_framework}")
    # Initialize the corresponding framework based on the task's multi_agent_framework
    if task.multi_agent_framework == MultiAgentFrameworks.MAGENTIC_ONE.value:
        from app.services.maf.impl.magentic_one import MagenticOne
        maf = MagenticOne()
    elif task.multi_agent_framework == MultiAgentFrameworks.AG2.value:
        from app.services.maf.impl.ag2 import AG2
        maf = AG2()
    elif task.multi_agent_framework == MultiAgentFrameworks.AM1.value:
        from app.services.maf.impl.am1 import AM1
        maf = AM1()
    else:
        logger.error(
            f"Unsupported framework: {task.multi_agent_framework} for task ID {task.task_id}"
        )
        raise HTTPException(
            status_code=400, detail="Unsupported multi-agent framework"
        )
    # Create the request object for the agentic task
    agentic_task_request = AgenticTaskRequest(
        task_id=task.task_id.__str__(),
        query=task.query,
        llm_model=task.llm_model,
        enable_internet=task.enable_internet,
    )
    if task.input_file_names:
        local_file_dir = os.path.join("uploads", task.task_id.__str__())
        # os.makedirs(local_file_dir, exist_ok=True)
        agentic_task_request.files=[LLMFileInput(file_name=_file, file_local_path=f"{local_file_dir}/{_file}") for _file in
               task.input_file_names] if task.input_file_names else None

    # Start the task via the framework and capture the response
    # response, status = await maf.start_task(agentic_task_request)
    task_response: TaskResponse = await maf.start_task(agentic_task_request)
    logger.info(f"Task with ID {task.task_id} finished. Status: {task_response.status}\n"
                f"Response: {task_response.task_output.final_response if task_response.task_output else None}")
    update_data = {
        "status": task_response.status,
        "final_response": task_response.task_output.final_response if task_response.task_output else None,
        "task_metadata": task_response.task_metadata,
    }
    await update_task(task.task_id, update_data)

def get_web_surfer_url(task: Task):
    web_surfer_url = None
    if task.multi_agent_framework == MultiAgentFrameworks.AM1.value and task.enable_internet and task.task_metadata:
        browser_use_task_id = task.task_metadata.get("browser_use_task_id")
        if browser_use_task_id:
            logger.info(f"Task is using BrowserUse framework: {browser_use_task_id} | {task.task_id} ")
            web_surfer_url = task.task_metadata.get("web_surfer_url")
            if web_surfer_url:
                logger.info(f"Web Surfer URL found in task metadata: {web_surfer_url}")
                return web_surfer_url
            browser_use = BrowserUse()
            browser_use_task_response = browser_use.get_task_details(browser_use_task_id)
            print(f"BrowserUse task response: {browser_use_task_response}")
            web_surfer_url = browser_use_task_response.get("live_url")
        else:
            logger.error(f"BrowserUse task ID not found in task metadata: {task.task_id}")
            return None
    return web_surfer_url

async def get_task_details(task_id: str) -> TaskResponse:
    """Retrieve a task by its ID asynchronously."""
    try:
        # Retrieve the task by ID
        task: type[Task] | None = await task_repository.get(task_id)

        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(f"Retrieved task with ID {task_id} from database.")

        # Convert ORM object to TaskResponse
        task_response = TaskResponse(
            task_id=task.task_id.__str__(),
            status=task.status,
            task_request=TaskRequest(
                task_id=task.task_id.__str__(),
                query=task.query,
                multi_agent_framework=task.multi_agent_framework,
                llm_model=task.llm_model,
                enable_internet=task.enable_internet,
            ),
            task_output=TaskOutput(
                final_response=task.final_response,
                output_file_urls=None,
            ),
            live_stream_response=LiveStreamResponse(
                web_surfer_url=get_web_surfer_url(task)
            ),
            input_file_names=task.input_file_names,
            task_metadata=task.task_metadata,
            created_at=task.created_at.isoformat() if task.created_at else None,
            updated_at=task.updated_at.isoformat() if task.updated_at else None,
        )
        logger.info(f"Retrieved task with ID {task_id} from database. {task_response}")
        return task_response
    except Exception as e:
        logger.error(f"Error fetching task with ID {task_id}: {e!s}")
        raise HTTPException(status_code=500, detail="Failed to fetch task")


async def get_all_tasks(offset: int, limit: int, db: AsyncSession) -> list[TaskResponse]:
    try:
        # query = "SELECT * FROM tasks LIMIT $1 OFFSET $2"
        # async with db.acquire() as conn:
        #     results = await conn.fetch(query, limit, offset)  # ✅ Pass limit and offset correctly
        #     tasks = [dict(row) for row in results]
        #     logger.info(f"Fetched {len(tasks)} tasks from database.")
        #     return tasks
        sql_query = select(Task).offset(offset).limit(limit)
        result = await db.execute(sql_query)
        items = result.scalars().all()
        tasks_list = [
            TaskResponse(
                task_id=task.task_id.__str__(),
                status=task.status,
                task_request=TaskRequest(
                    task_id=task.task_id.__str__(),
                    query=task.query,
                    multi_agent_framework=task.multi_agent_framework,
                    llm_model=task.llm_model,
                    enable_internet=task.enable_internet,
                ),
                task_output=TaskOutput(
                    final_response=task.final_response,
                    output_file_urls=None,
                ),
                live_stream_response=LiveStreamResponse(
                    web_surfer_url=get_web_surfer_url(task)
                ),
                input_file_names=task.input_file_names,
                task_metadata=task.task_metadata,
                created_at=task.created_at.isoformat() if task.created_at else None,
                updated_at=task.updated_at.isoformat() if task.updated_at else None,
            )
            for task in items
        ]
        logger.info(f"Retrieved {len(tasks_list)} tasks with offset={offset} and limit={limit}")
        return tasks_list
    except Exception as e:
        logger.error(f"Error fetching all tasks from database: {e!s}")
        return {"error": "Failed to fetch tasks", "message": str(e)}


# async def get_all_tasks_old_v2(offset: int, limit: int, db: AsyncSession):
#     """Retrieve all tasks asynchronously with pagination."""
#     try:
#         # Use SQLAlchemy ORM to retrieve tasks with pagination
#         logger.info(
#             f"Retrieving tasks async from database (limit={limit}, offset={offset})"
#         )
#         from sqlalchemy.future import select
#
#         query = select(Task).offset(offset).limit(limit)
#         # logger.info(f"SQL query to execute: {query}")
#         logger.info(
#             f"SQL query to execute: {query.compile(db.get_bind(), compile_kwargs={'literal_binds': True})!s}"
#         )
#         result = await db.execute(query)  # Execute asynchronously
#         tasks = result.scalars().all()  # Extract results
#
#         logger.info(
#             f"Retrieved {len(tasks)} tasks from database (limit={limit}, offset={offset})"
#         )
#
#         # Convert ORM objects to dictionaries (Ensure Task model has necessary attributes)
#         tasks_list = [
#             {
#                 "id": task.task_id,
#                 "query": task.query,  # Replace with actual attributes in your Task model
#                 "status": task.status,
#                 "multi_agent_framework": task.multi_agent_framework,
#                 "llm_model": task.llm_model,
#                 "final_response": task.final_response,
#                 "created_at": (
#                     task.created_at.isoformat() if task.created_at else None
#                 ),
#                 "updated_at": (
#                     task.updated_at.isoformat() if task.updated_at else None
#                 ),
#             }
#             for task in tasks
#         ]
#         logger.info(f"Retrieved {len(tasks_list)} tasks from database.")
#         return tasks_list
#     except Exception as e:
#         logger.error(f"Error fetching tasks: {e!s}", exc_info=True)
#         return {"error": "Failed to fetch tasks", "message": str(e)}


# async def get_all_tasks_old(offset: int, limit: int, db: AsyncSession):
#     """Retrieve all tasks asynchronously with pagination."""
#     try:
#         # Use SQLAlchemy ORM to retrieve tasks with pagination
#         logger.info(
#             f"Retrieving tasks async from database (limit={limit}, offset={offset})"
#         )
#         # Correct way to execute a query
#         async with db.acquire() as connection:
#             # Make sure to await the fetch
#             result = await connection.fetch("SELECT * FROM tasks")
#             # Convert to list of dicts
#             resp = [dict(row) for row in result]
#             logger.info(f"Fetched {len(resp)}\n{resp} tasks from database.")
#
#         from sqlalchemy.future import select
#
#         query = select(Task).offset(offset).limit(limit)
#         logger.info(f"SQL query to execute: {query}")
#         result = await db.execute(query)  # Execute asynchronously
#         tasks = result.scalars().all()  # Extract results
#
#         logger.info(
#             f"Retrieved {len(tasks)} tasks from database (limit={limit}, offset={offset})"
#         )
#
#         # Convert ORM objects to dictionaries (Ensure Task model has necessary attributes)
#         tasks = {
#             "tasks": [
#                 {
#                     "id": task.task_id,
#                     "query": task.query,  # Replace with actual attributes in your Task model
#                     "status": task.status,
#                     "multi_agent_framework": task.multi_agent_framework,
#                     "llm_model": task.llm_model,
#                     "final_response": task.final_response,
#                     "created_at": (
#                         task.created_at.isoformat() if task.created_at else None
#                     ),
#                     "updated_at": (
#                         task.updated_at.isoformat() if task.updated_at else None
#                     ),
#                 }
#                 for task in tasks
#             ]
#         }
#         logger.info(f"Retrieved {len(tasks)} tasks from database.")
#         return tasks
#     except Exception as e:
#         logger.error(f"Error fetching tasks: {e!s}")
#         return {"error": "Failed to fetch tasks", "message": str(e)}
#

# async def update_task_details(
#         task_id: str, final_response: str, status: str, db: AsyncSession
# ) -> TaskResponse:
#     """Update task details asynchronously."""
#     try:
#         # Retrieve the task by ID
#         task = await db.get(Task, task_id)
#
#         if task is None:
#             logger.warning(f"Task with ID {task_id} not found.")
#             raise HTTPException(status_code=404, detail="Task not found")
#
#         # Update task fields with provided values
#         task.final_response = final_response
#         task.status = status
#
#         # Commit the changes to the database
#         await db.commit()
#         await db.refresh(task)
#
#         # Log the successful update
#         logger.info(f"Successfully updated task with ID {task_id}.")
#
#         # Return updated task as TaskResponse
#         return TaskResponse(
#             task_id=task.task_id.__str__(),
#             query=task.query,
#             final_response=task.final_response,
#             status=task.status,
#             multi_agent_framework=task.multi_agent_framework,
#             llm_model=task.llm_model,
#             enable_internet=task.enable_internet,
#             input_file_names=task.input_file_names,  # TODO: Update if necessary
#             agent_conversations=None,  # TODO: Update if necessary
#             output_file_urls=None,  # TODO: Update if necessary
#             task_metadata=task.task_metadata,
#             created_at=task.created_at.isoformat() if task.created_at else None,
#             updated_at=task.updated_at.isoformat() if task.updated_at else None,
#         )
#     except Exception as e:
#         # Error handling - Capture the exception and log it.
#         logger.error(f"Error updating task with ID {task_id}: {e!s}")
#         raise HTTPException(status_code=500, detail="Failed to update task")


async def update_task(task_id: str, update_data: dict):
    updated_task = await task_repository.update(task_id=task_id, update_data=update_data)
    task_response = TaskResponse(
        task_id=str(updated_task.task_id),
        status=updated_task.status,
        task_request=TaskRequest(
            query=updated_task.query,
            multi_agent_framework=updated_task.multi_agent_framework,
            llm_model=updated_task.llm_model,
            enable_internet=updated_task.enable_internet,
        ),
        task_output=TaskOutput(
            final_response=updated_task.final_response,
            output_file_urls=None,
        ),
        input_file_names=updated_task.input_file_names,
        task_metadata=updated_task.task_metadata,
        created_at=updated_task.created_at.isoformat() if updated_task.created_at else None,
        updated_at=updated_task.updated_at.isoformat() if updated_task.updated_at else None,
    )
    logger.info(f"Updated task with ID {task_id} from database | {task_response}")
    return task_response

async def upload_file_to_task(task_id: str, input_file: UploadFile, db: AsyncSession) -> TaskResponse:
    # return TaskResponse(task_id=task_id, input_file_names=[input_file.filename])
    # Fetch the task from the database
    task = await get_task_details(task_id, db)
    input_file_names = task.input_file_names + [input_file.filename] if task.input_file_names else [input_file.filename]

    # Create a folder with name task_id and save the file
    folder_path = os.path.join("uploads", task_id)
    os.makedirs(folder_path, exist_ok=True)

    # Save the file in the created folder
    file_path = os.path.join(folder_path, input_file.filename)
    with open(file_path, "wb") as file:
        file.write(await input_file.read())
        task = await update_task(task_id=task_id,
                                 update_data={"input_file_names": input_file_names})
    task_response = TaskResponse(
        task_id=task.task_id.__str__(),
        status=task.status,
        task_request=TaskRequest(
            query=task.query,
            multi_agent_framework=task.multi_agent_framework,
            llm_model=task.llm_model,
            enable_internet=task.enable_internet,
        ),
        task_output=TaskOutput(
            final_response=task.final_response,
            output_file_urls=None,
        ),
        input_file_names=task.input_file_names,
        task_metadata=task.task_metadata,
        created_at=task.created_at.isoformat() if task.created_at else None,
        updated_at=task.updated_at.isoformat() if task.updated_at else None,
    )
    logger.info(f"Uploaded task with ID {task_id} successfully.")
    return task_response
