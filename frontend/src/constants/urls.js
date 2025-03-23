// export const BASE_URL = 'http://127.0.0.1:8000';
export const BASE_URL = 'https://localhost:8000';
// export const BASE_URL = 'https://0.0.0.0:8000';

export const URLS = {
    ALL_TASKS: '/task/?offset=0&limit=100',
    CREATE_TASK: '/task/',
    UPLOAD_FILE: '/task/%TASK_ID%/upload',
    START_TASK: '/task/%TASK_ID%/start',
    GET_TASK: '/task/%TASK_ID%',
};
