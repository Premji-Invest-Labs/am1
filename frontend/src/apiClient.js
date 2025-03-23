import axios from 'axios';
import { BASE_URL, URLS } from './constants/urls';

export const createTask = async (payload) => {
    try {
        const URL = `${BASE_URL}${URLS.CREATE_TASK}`;
        const response = await axios.post(URL, payload);

        if (response.status === 201) {
            return response.data;
        }
        return null;
    } catch (err) {
        console.error(err);
        return err;
    }
};

export const startTask = async (taskId) => {
    try {
        const URL = `${BASE_URL}${URLS.START_TASK.replace(
            '%TASK_ID%',
            taskId
        )}`;
        const response = await axios.post(URL);
        if (response.status === 200) {
            return response.data;
        }
        return null;
    } catch (err) {
        console.error(err);
        return err;
    }
};

export const getTask = async (taskId) => {
    try {
        const URL = `${BASE_URL}${URLS.GET_TASK.replace('%TASK_ID%', taskId)}`;
        const response = await axios.get(URL);
        if (response.status === 200) {
            return response.data;
        }
        return null;
    } catch (err) {
        console.error(err);
        return err;
    }
};

export const getAllTasks = async () => {
    try {
        const URL = `${BASE_URL}${URLS.ALL_TASKS}`;
        const response = await axios.get(URL);
        if (response.status === 200) {
            return response.data;
        }
        return null;
    } catch (err) {
        console.error(err);
        return err;
    }
};

export const uploadFile = async (taskId, file) => {
    try {
        const URL = `${BASE_URL}${URLS.UPLOAD_FILE.replace(
            '%TASK_ID%',
            taskId
        )}`;
        const response = await axios.post(URL, file, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        if (response.status === 200) {
            return response.data;
        }
        return null;
    } catch (err) {
        console.error('Upload error:', err);
        return err;
    }
};
