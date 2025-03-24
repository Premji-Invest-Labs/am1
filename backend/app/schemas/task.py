from datetime import datetime

from pydantic import BaseModel, HttpUrl

from app.core.enums import MultiAgentFrameworks
from app.models.llm import get_default_model

class MafInstructions(BaseModel):
    min_duration: int = 60 * 1 # in Seconds
    max_duration: int = 60 * 30  # in Seconds
    minimum_words: int = 1
    maximum_words: int = 5000
    max_replans: int = 0

class TaskRequest(BaseModel):
    task_id: str | None = None
    query: str | None = None
    multi_agent_framework: str | None = MultiAgentFrameworks.AM1.value
    llm_model: str | None = get_default_model().id
    enable_internet: bool | None = True
    maf_instructions: MafInstructions | None = None
    email_output: bool = False


class LiveStreamResponse(BaseModel):
    web_surfer_url: HttpUrl | None = None
    file_surfer_url: HttpUrl | None = None
    coder_url: HttpUrl | None = None
    executor_url: HttpUrl | None = None
    video_surfer_url: HttpUrl | None = None
    mas_stream_url: HttpUrl | None = None
    agent_conversations: dict | None = None

class TaskOutput(BaseModel):
    final_response: str | None = None
    output_file_urls: dict | None = None


class TaskResponse(BaseModel):
    task_id: str
    status: str | None = None
    task_request: TaskRequest
    input_file_names: list[str] = []
    task_output: TaskOutput | None = None
    live_stream_response: LiveStreamResponse | None = None
    task_metadata: dict | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class ChatRequest(BaseModel):
    query: str
    file_hashes: list[str]
    conversation_session_id: str
    compare: bool = False
    stream: bool = False
    enable_internet: bool | None = None
    enable_cot: bool | None = True
    use_chat_history: bool | None = True
    all_chunks_in_context: bool | None = None


class ChatResponse(BaseModel):
    conversation_session_id: str
    chat_responses: list[dict]
    metadata: dict


class LLMFileInput(BaseModel):
    file_hash: str | None = None
    file_name: str | None = None
    file_extension: str | None = None
    file_size: int | None = None
    file_local_path: str | None = None
    file_cloud_url: str | None = None


class AgenticTaskRequest(BaseModel):
    task_id: str | None = None
    query: str
    llm_model: str = get_default_model().id
    enable_internet: bool = True
    files: list[LLMFileInput] | None = None
    conversation_session_id: str | None = None
    dialogue_id: str | None = None
    stream: bool | None = False
    metadata: dict | None = None
