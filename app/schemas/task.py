from pydantic import BaseModel

from app.core.enums import LLMModels, MultiAgentFrameworks


class TaskRequest(BaseModel):
    query: str = None
    multi_agent_framework: str | None = MultiAgentFrameworks.MAGENTIC_ONE.value
    llm_model: str | None = LLMModels.OPENAI_GPT_4O_MINI.value
    enable_internet: bool | None = True


class TaskResponse(BaseModel):
    task_id: str
    final_response: str | None = None
    status: str | None = None
    agent_conversations: dict | None = None
    output_file_urls: dict | None = None
    metadata: dict | None = None


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
    file_hash: str
    file_name: str
    file_extension: str
    file_size: int
    file_local_path: str
    file_cloud_url: str


class AgenticTaskRequest(BaseModel):
    task_id: str | None = None
    query: str
    llm_model: str = LLMModels.OPENAI_GPT_4O_MINI.value
    enable_internet: bool = True
    files: list[LLMFileInput] | None = None
    conversation_session_id: str | None = None
    dialogue_id: str | None = None
    stream: bool | None = False
    metadata: dict | None = None
