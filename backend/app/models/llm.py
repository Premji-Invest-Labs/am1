from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum, auto

from app.core.logging import get_logger

logger = get_logger()

class LLMProvider(Enum):
    """Companies providing LLM services"""
    OPENAI = "openai"
    AZURE = "azure"
    GOOGLE = "google"
    META = "meta"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    MISTRAL = "mistral"


class LLMFamily(Enum):
    """Major model families"""
    GPT = "gpt"
    GEMINI = "gemini"
    LLAMA = "llama"
    CLAUDE = "claude"
    MISTRAL = "mistral"


class InputCapability(Enum):
    """Types of inputs the model can understand"""
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    CODE = auto()
    PDF = auto()
    SPREADSHEET = auto()
    DOCUMENT = auto()


class OutputCapability(Enum):
    """Types of outputs the model can generate"""
    TEXT = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    CODE = auto()
    CHART = auto()
    TABLE = auto()


class ModelCapability(Enum):
    """Special capabilities a model may have"""
    FUNCTION_CALLING = auto()
    VISION = auto()
    TOOL_USE = auto()
    REASONING = auto()  # Enhanced thinking capabilities
    DEEP_RESEARCH = auto()  # Ability to research topics in depth
    CANVAS = auto()  # Visual workspace capabilities
    COMPUTER_USING_AGENT = auto()  # Computer-using agent capabilities
    AGENTIC = auto()  # General agentic capabilities
    RAG = auto()  # Retrieval-augmented generation
    FINE_TUNING = auto()  # Can be fine-tuned
    MULTI_MODAL = auto()  # Handles multiple modalities
    PARALLELISM = auto()  # Can process multiple requests in parallel
    STREAMING = auto()  # Supports streaming responses


class Tool(Enum):
    """Tools that the model can use"""
    WEB_SEARCH = auto()
    WEB_BROWSING = auto()
    CODE_INTERPRETER = auto()
    CALCULATOR = auto()
    PLUGIN_ECOSYSTEM = auto()
    FILE_READING = auto()
    FILE_WRITING = auto()
    DATABASE_QUERY = auto()
    API_CALLING = auto()
    SYSTEM_COMMAND = auto()
    DALL_E = auto()  # Image generation with DALL-E
    VISION = auto()  # General vision capabilities
    KNOWLEDGE_GRAPH = auto()  # Knowledge graph integration
    EXTERNAL_MEMORY = auto()  # External memory storage

class HostedCloud(Enum):
    """Hosted cloud for the model"""
    AZURE = auto()
    GCP = auto()
    AWS = auto()
    ON_PREMISE = auto()
    LAPTOP = auto()
    OTHERS = auto()

class ModelRegion(Enum):
    """Region where the model is hosted"""
    US = auto()
    EU = auto()
    ASIA = auto()
    OTHERS = auto()

class ModelCity(Enum):
    """City where the model is hosted"""
    SEATTLE = auto()
    SAN_FRANCISCO = auto()
    CHENNAI = auto()
    PUNE = auto()
    NEW_YORK = auto()
    LONDON = auto()
    FRANKFURT = auto()
    TOKYO = auto()
    SINGAPORE = auto()
    SYDNEY = auto()
    OTHERS = auto()


@dataclass
class LLMModel:
    """Comprehensive model representation"""
    display_name: str  # Human-readable name
    provider: LLMProvider  # Provider company
    family: LLMFamily  # Model family
    input_capabilities: List[InputCapability] = None  # What inputs it can process
    output_capabilities: List[OutputCapability] = None  # What outputs it can generate
    capabilities: List[ModelCapability] = None  # Special capabilities
    parameters: Optional[str] = None  # E.g., "7b", "70b"
    version: Optional[str] = None  # E.g., "3", "4", "3.5"
    variant: Optional[str] = None  # E.g., "mini", "pro", "turbo"
    deployment_id: Optional[str] = None  # could be a date or number or string to identify the deployment in the same version + variant
    tools: List[Tool] = None  # Supported tools
    context_window: Optional[str] = None  # Context window size
    output_tokens: Optional[str] = None  # Number of output tokens
    hosted_cloud: Optional[str] = None  # Hosted cloud
    token_rate_limit: Optional[int] = None  # Rate limit in tokens
    api_rate_limit: Optional[int] = None  # API call rate limit
    rate_limit_in_seconds: Optional[int] = None  # Time period for rate limit
    release_date: Optional[str] = None  # Release date
    knowledge_cutoff_date: Optional[str] = None  # Knowledge cutoff date
    knowledge_source: Optional[str] = None # Knowledge source
    description: Optional[str] = None  # Description
    comments: Optional[str] = None  # Additional comments
    quantization: Optional[str] = None  # Quantization level
    model_region: Optional[str] = None  # Region where the model is hosted
    model_city: Optional[str] = None  # City where the model is hosted
    documentation_url: Optional[str] = None  # Link to documentation
    pricing: Optional[Dict[str, Any]] = None  # Pricing information
    core_languages: Optional[List[str]] = None  # Core languages supported
    supported_languages: Optional[List[str]] = None # All other languages supported to certain extent
    is_json_mode_enabled: Optional[bool] = None  # JSON mode (output json) enabled
    is_serverless: Optional[bool] = None  # Serverless model
    is_load_balanced: Optional[bool] = None  # Load-balanced endpoint for LLM and not a direct LLM model
    is_base_model: Optional[bool] = False  # Base model or Instruction Tuned model
    is_fine_tuned: Optional[bool] = False  # Fine-tuned model
    is_content_filtering_enabled: Optional[bool] = False  # Content filtering enabled such as harmful, inappropriate, etc.
    llm_metadata: Optional[Dict[str, Any]] = None  # Additional metadata
    id: Optional[str] = None  # Unique identifier

    def __post_init__(self):
        """Initialize default values for lists"""
        if self.input_capabilities is None:
            self.input_capabilities = []
        if self.output_capabilities is None:
            self.output_capabilities = []
        if self.capabilities is None:
            self.capabilities = []
        if self.tools is None:
            self.tools = []
        if not self.id:
            self.id = (f"{self.hosted_cloud + '-' if self.hosted_cloud else ''}"
                       f"{'-' + self.provider.value if self.provider.value else ''}"
                       f"{'-' + self.family.value if self.family else ''}"
                       f"{'-' + self.version if self.version else ''}"
                       f"{'-' + self.variant if self.variant is not None else ''}"
                       f"{'-' + self.deployment_id if self.deployment_id else ''}"
                       f"{'-' + self.parameters if self.parameters else ''}"
                       f"{'-' + self.context_window if self.context_window else ''}"
                       f"{'-' + self.quantization if self.quantization else ''}"
                       f"{'-base' if self.is_base_model else '-instructed'}"
                       f"{'-' + self.model_region if self.model_region else ''}").lower()


openai_gpt_4o_v1 = LLMModel(
    display_name="OpenAI GPT-4o",
    provider=LLMProvider.OPENAI,
    family=LLMFamily.GPT,
    version="4",
    variant="o",
    hosted_cloud="OpenAI_Infra",
    input_capabilities=[
        InputCapability.TEXT,
        InputCapability.IMAGE,
        InputCapability.CODE,
        InputCapability.PDF,
    ],
    output_capabilities=[
        OutputCapability.TEXT,
        OutputCapability.CODE,
        OutputCapability.CHART,
    ],
    capabilities=[
        ModelCapability.FUNCTION_CALLING,
        ModelCapability.TOOL_USE,
        ModelCapability.MULTI_MODAL,
        ModelCapability.REASONING,
        ModelCapability.STREAMING,
    ],
    tools=[
        Tool.CODE_INTERPRETER,
        Tool.CALCULATOR,
        Tool.FILE_READING,
        Tool.PLUGIN_ECOSYSTEM,
    ],
    context_window="128k",
    description="OpenAI's multimodal model capable of processing both text and images.",
    documentation_url="https://platform.openai.com/docs/models/gpt-4o",
)

azure_openai_gpt_4o_v1 = LLMModel(
        display_name="Azure OpenAI GPT-4o",
        provider=LLMProvider.OPENAI,
        family=LLMFamily.GPT,
        version="4",
        variant="o",
        input_capabilities=[
            InputCapability.TEXT,
            InputCapability.IMAGE,
            InputCapability.CODE,
            InputCapability.PDF,
        ],
        output_capabilities=[
            OutputCapability.TEXT,
            OutputCapability.CODE,
            OutputCapability.CHART,
        ],
        capabilities=[
            ModelCapability.FUNCTION_CALLING,
            ModelCapability.TOOL_USE,
            ModelCapability.MULTI_MODAL,
            ModelCapability.REASONING,
            ModelCapability.STREAMING,
        ],
        tools=[
            Tool.CODE_INTERPRETER,
            Tool.CALCULATOR,
            Tool.FILE_READING,
            Tool.PLUGIN_ECOSYSTEM,
        ],
        context_window="32k",
        description="OpenAI's multimodal model capable of processing both text and images.",
        documentation_url="https://platform.openai.com/docs/models/gpt-4o",
    )
azure_openai_gpt_4o_lb_v1 = LLMModel(
        display_name="Azure OpenAI GPT-4o-lb",
        provider=LLMProvider.OPENAI,
        family=LLMFamily.GPT,
        version="4",
        variant="o",
        hosted_cloud=HostedCloud.AZURE.__str__().lower(),
        input_capabilities=[
            InputCapability.TEXT,
            InputCapability.IMAGE,
            InputCapability.CODE,
            InputCapability.PDF,
        ],
        output_capabilities=[
            OutputCapability.TEXT,
            OutputCapability.CODE,
            OutputCapability.CHART,
        ],
        capabilities=[
            ModelCapability.FUNCTION_CALLING,
            ModelCapability.TOOL_USE,
            ModelCapability.MULTI_MODAL,
            ModelCapability.REASONING,
            ModelCapability.STREAMING,
        ],
        tools=[
            Tool.CODE_INTERPRETER,
            Tool.CALCULATOR,
            Tool.FILE_READING,
            Tool.PLUGIN_ECOSYSTEM,
        ],
        context_window="32k",
        description="OpenAI's multimodal model capable of processing both text and images.",
        documentation_url="https://platform.openai.com/docs/models/gpt-4o",
    )
# "claude-3-opus": LLMModel(
    #     id="claude-3-opus",
    #     display_name="Claude 3 Opus",
    #     provider=LLMProvider.ANTHROPIC,
    #     family=LLMFamily.CLAUDE,
    #     version="3",
    #     variant="opus",
    #     input_capabilities=[
    #         InputCapability.TEXT,
    #         InputCapability.IMAGE,
    #         InputCapability.CODE,
    #         InputCapability.PDF,
    #     ],
    #     output_capabilities=[
    #         OutputCapability.TEXT,
    #         OutputCapability.CODE,
    #     ],
    #     capabilities=[
    #         ModelCapability.TOOL_USE,
    #         ModelCapability.REASONING,
    #         ModelCapability.MULTI_MODAL,
    #         ModelCapability.STREAMING,
    #     ],
    #     tools=[
    #         Tool.FILE_READING,
    #     ],
    #     context_window=200000,
    #     description="Anthropic's most powerful model with advanced reasoning capabilities.",
    #     documentation_url="https://docs.anthropic.com/claude/docs/models-overview",
    # ),
llama3_2_vision_11b_instruct_q4_K_M_v1 = LLMModel(
        id="llama3.2-vision:11b-instruct-q4_K_M",
        display_name="LLAMA 3.2 Vision 11b Instruct Q4_K_M",
        provider=LLMProvider.META,
        family=LLMFamily.LLAMA,
        version="3",
        variant="2",
        parameters="11b",
        quantization="q4_K_M",
        input_capabilities=[
            InputCapability.TEXT,
            InputCapability.IMAGE,
        ],
        output_capabilities=[
            OutputCapability.TEXT,
        ],
        capabilities=[
            ModelCapability.VISION,
            ModelCapability.MULTI_MODAL,
            ModelCapability.STREAMING,
        ],
        tools=[
            Tool.DALL_E,
            Tool.VISION,
        ],
        context_window="128k",
        is_base_model=False,
        description="LLama 3.2 Vision model with 11 billion parameters for image processing.",
        documentation_url="https://www.llama.com/docs/get-started/",
    )

MODELS = {
    openai_gpt_4o_v1.id: openai_gpt_4o_v1,
    azure_openai_gpt_4o_lb_v1.id: azure_openai_gpt_4o_lb_v1,
    azure_openai_gpt_4o_v1.id: azure_openai_gpt_4o_v1,
    llama3_2_vision_11b_instruct_q4_K_M_v1.id: llama3_2_vision_11b_instruct_q4_K_M_v1
}
logger.info(f"Models: {MODELS}")

def get_model_ids() -> List[str]:
    """Get all model IDs"""
    return list(MODELS.keys())

def get_models() -> List[Dict]:
    """Get all models"""
    return [
        {model.id: model.display_name} for model in MODELS.values()
    ]

def get_model(model_id: str) -> Optional[LLMModel]:
    """Get model by its ID"""
    return MODELS.get(model_id)


def get_default_model() -> LLMModel:
    """Get the default model"""
    return MODELS.get(azure_openai_gpt_4o_lb_v1.id, openai_gpt_4o_v1)


def filter_models_by_capability(capability: ModelCapability) -> List[LLMModel]:
    """Get all models with a specific capability"""
    return [model for model in MODELS.values() if capability in model.capabilities]


def filter_models_by_input(input_type: InputCapability) -> List[LLMModel]:
    """Get all models that support a specific input type"""
    return [model for model in MODELS.values() if input_type in model.input_capabilities]


def filter_models_by_output(output_type: OutputCapability) -> List[LLMModel]:
    """Get all models that support a specific output type"""
    return [model for model in MODELS.values() if output_type in model.output_capabilities]


def filter_models_by_tool(tool: Tool) -> List[LLMModel]:
    """Get all models that support a specific tool"""
    return [model for model in MODELS.values() if tool in model.tools]