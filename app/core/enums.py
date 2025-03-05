from enum import Enum


class MultiAgentFrameworks(Enum):
    LANGGRAPH = "LangGraph"
    MAGENTIC_ONE = "MagenticOne"


class LLMModels(Enum):
    AZURE_GPT_4O = "azure-gpt-4o"
    AZURE_GPT_4O_MINI = "azure-gpt-4o-mini"
    AZURE_GPT_O1 = "azure-gpt-o1"
    AZURE_GPT_O1_MINI = "azure-gpt-o1-mini"
    OPENAI_GPT_4O = "openai-gpt-4o"
    OPENAI_GPT_4O_MINI = "openai-gpt-4o-mini"
    OPENAI_GPT_O1 = "openai-gpt-o1"
    OPENAI_GPT_O1_MINI = "openai-gpt-o1-mini"
    LLAMA3_11B = "llama3-11b"
