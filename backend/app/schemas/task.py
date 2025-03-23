from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, HttpUrl

from app.core.enums import MultiAgentFrameworks
from app.models.llm import LLMModel, get_default_model


class TaskRequest(BaseModel):
    task_id: Optional[str] = None
    query: Optional[str] = None
    multi_agent_framework: Optional[str] = MultiAgentFrameworks.AM1.value
    llm_model: Optional[str] = get_default_model().id
    enable_internet: Optional[bool] = True


class LiveStreamResponse(BaseModel):
    web_surfer_url: Optional[HttpUrl] = None
    file_surfer_url: Optional[HttpUrl] = None
    coder_url: Optional[HttpUrl] = None
    executor_url: Optional[HttpUrl] = None
    video_surfer_url: Optional[HttpUrl] = None
    mas_stream_url: Optional[HttpUrl] = None
    agent_conversations: Optional[Dict] = None

class TaskOutput(BaseModel):
    final_response: Optional[str] = None
    output_file_urls: Optional[Dict] = None


class TaskResponse(BaseModel):
    task_id: str
    status: Optional[str] = None
    task_request: TaskRequest
    input_file_names: List[str] = []
    task_output: Optional[TaskOutput] = None
    live_stream_response: Optional[LiveStreamResponse] = None
    task_metadata: Optional[Dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ChatRequest(BaseModel):
    query: str
    file_hashes: List[str]
    conversation_session_id: str
    compare: bool = False
    stream: bool = False
    enable_internet: Optional[bool] = None
    enable_cot: Optional[bool] = True
    use_chat_history: Optional[bool] = True
    all_chunks_in_context: Optional[bool] = None


class ChatResponse(BaseModel):
    conversation_session_id: str
    chat_responses: List[Dict]
    metadata: Dict


class LLMFileInput(BaseModel):
    file_hash: Optional[str] = None
    file_name: Optional[str] = None
    file_extension: Optional[str] = None
    file_size: Optional[int] = None
    file_local_path: Optional[str] = None
    file_cloud_url: Optional[str] = None


class AgenticTaskRequest(BaseModel):
    task_id: Optional[str] = None
    query: str
    llm_model: str = get_default_model().id
    enable_internet: bool = True
    files: Optional[List[LLMFileInput]] = None
    conversation_session_id: Optional[str] = None
    dialogue_id: Optional[str] = None
    stream: Optional[bool] = False
    metadata: Optional[Dict] = None
