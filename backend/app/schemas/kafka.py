from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.enums import TaskStatus


class KafkaTaskRequest(BaseModel):
    task_id: str
    task_type: str
    payload: Optional[dict] = None
    created_at: datetime = datetime.now()
    status: str = TaskStatus.IN_PROGRESS.value


class KafkaTaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
