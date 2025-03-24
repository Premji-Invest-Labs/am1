export const PATH_NAMES = {
    DASHBOARD: '/',
    CREATE_TASK: '/create-task',
    ALL_TASKS: '/all-tasks',
    TASK_GENERATION: '/task-generation',
    TASK_DETAIL: '/task/:id',
    TASK_DETAIL_BASE: '/task/',
};

export const CREATE_TASK_BUTTONS = {
    WITH_FILE: 'Continue with file',
    WITHOUT_FILE: 'Continue without file',
};

export const LLM_MODELS = [
    {
        key: 'azure-open-ai',
        value:"azure-openai-gpt-4o",
        label: 'Azure Open AI : GPT-4o',
        title: '',
    },
    {
        key: 'open-ai',
        value:"openai-gpt-4o",
        label: 'Open AI : GPT-4o',
        title: '',
    },
];

export const MULTI_AGENT_FRAMEWORKS = [
    {
        key: 'AM1',
        label: 'AM1',
        value: 'AM1',
        title: '',
    },
    {
        key: 'AG2',
        label: 'AG2',
        value: 'AG2',
        title: '',
    },
    {
        key: 'MagenticOne',
        label: 'Magentic One',
        value: 'MagenticOne',
        title: '',
    },
    {
        key: 'LangGraph',
        label: 'LangGraph',
        value: 'LangGraph',
        title: '',
    },
];

export const TASKS_STATUS = {
    SUCCESS: 'success',
    IN_PROGRESS: 'in_progress',
    FAILED: 'failure',
    CREATED: 'created',
    PARTIAL_SUCCESS: 'partial_success',
};

export const TASK_CARD_TOOLTIP_TEXT = {
    SUCCESS: 'Click to view the completed tasks',
    IN_PROGRESS: 'Click to view the tasks in progress',
    FAILED: 'Click to view the failed tasks',
    CREATED: 'Click to view the created tasks',
    NEW: 'Click to create a new task',
};

export const PATH_NAMES_HEADER_MAPPING = {
    [PATH_NAMES.DASHBOARD]: 'Home',
    [PATH_NAMES.CREATE_TASK]: 'Create Task',
    [PATH_NAMES.ALL_TASKS]: 'All Tasks',
    [PATH_NAMES.TASK_GENERATION]: 'Task Generation',
    [PATH_NAMES.TASK_DETAIL_BASE]: 'Task Detail',
};

export const MODEL_PARAMS_TOOLTIP_TEXT = {
    MAF: 'Multi Agent Framework',
    LLM: 'LLM Model',
};

export const CREATE_TASK_SOURCES = {
    ATTACHMENT: 'Attachment',
    SUBMIT: 'Submit',
};

export const DUMMY_TASK_ID = 'dummy_1234';
