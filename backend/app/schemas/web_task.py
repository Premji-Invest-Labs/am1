from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class WebCreateTaskRequest(BaseModel):
    """
    Request body for initiating a browser-use task.

    Attributes:
        query (Optional[str]): The natural language query or task to perform in the browser.
    """
    query: Optional[str] = None


class WebCreateTaskResponse(BaseModel):
    """
    Response returned after creating a browser-use task.

    Attributes:
        task_id (Optional[str]): The ID of the created task.
    """
    task_id: Optional[str] = None


class WebTaskRequest(BaseModel):
    """
    Request model to fetch details or status of a browser-use task.

    Attributes:
        task_id (str): The unique identifier of the task.
    """
    task_id: str


class Step(BaseModel):
    """
    Represents an individual step taken by the AI during task execution.

    Attributes:
        id (str): Unique step ID.
        step (int): The step number in the sequence.
        evaluation_previous_goal (str): Evaluation of the previous step's goal.
        next_goal (str): The next goal or action to take.
    """
    id: str
    step: int
    evaluation_previous_goal: str
    next_goal: str


class WebTaskResponse(BaseModel):
    """
    Full response containing task details, status, steps, and metadata.

    Attributes:
        id (str): Unique task ID.
        task (str): The task query string.
        live_url (Optional[str]): URL to the live browser session.
        output (Optional[str]): Final output/result of the task.
        status (str): Task execution status (e.g., 'finished', 'running').
        created_at (datetime): Timestamp when the task was created.
        finished_at (Optional[datetime]): Timestamp when the task finished.
        steps (List[Step]): A list of steps taken to complete the task.
        browser_data (Optional[dict]): Raw browser data (if available).
    """
    id: str
    task: str
    live_url: Optional[str]
    output: Optional[str]
    status: str
    created_at: datetime
    finished_at: Optional[datetime]
    steps: List[Step]
    browser_data: Optional[dict] = None


class WebTaskStatusResponse(BaseModel):
    """
    Response model for task status check.

    Attributes:
        status (str): The current status of the task (e.g., 'pending', 'running', 'finished').
    """
    status: str
