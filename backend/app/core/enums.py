from enum import Enum


class MultiAgentFrameworks(Enum):
    LANGGRAPH = "LangGraph"
    MAGENTIC_ONE = "MagenticOne"
    AG2 = "AG2"
    AM1 = "AM1"

class TaskStatus(Enum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    CREATED = "created"
    FAILED = "failed"
    PARTIAL_SUCCESS = "partial_success"
