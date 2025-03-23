import {
    DUMMY_TASK_ID,
    PATH_NAMES,
    PATH_NAMES_HEADER_MAPPING,
    TASKS_STATUS,
} from '../constants';

export const getTaskCountByStatus = (tasks) => {
    if (!tasks?.length) return {};

    return tasks.reduce(
        (acc, task) => {
            const status = task.status?.toLowerCase();
            if (status === TASKS_STATUS.SUCCESS) {
                acc.success++;
            } else if (status === TASKS_STATUS.IN_PROGRESS) {
                acc.inProgress++;
            } else if (status === TASKS_STATUS.FAILED) {
                acc.failure++;
            } else if (status === TASKS_STATUS.CREATED) {
                acc.created++;
            } else if (status === TASKS_STATUS.PARTIAL_SUCCESS) {
                acc.partialSuccess++;
            }
            return acc;
        },
        { success: 0, in_progress: 0, failure: 0, created: 0 }
    );
};

export const getPageHeading = (pathname) => {
    const header = PATH_NAMES_HEADER_MAPPING[pathname];
    if (header) {
        return header;
    }
    if (pathname.includes(PATH_NAMES.TASK_DETAIL_BASE)) {
        return PATH_NAMES_HEADER_MAPPING[PATH_NAMES.TASK_DETAIL_BASE];
    }
};

const dummyTasks = [
    {
        task_id: DUMMY_TASK_ID,
        query: 'Dummy Task',
    },
];

export const getTasksMenuItems = (tasks) => {
    const taskArr = tasks?.length ? tasks : dummyTasks;

    const sortedTasks = taskArr.sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );

    return sortedTasks.map((task) => ({
        key: `${PATH_NAMES.TASK_DETAIL_BASE}${task.task_id}`,
        label: task.query || 'untitled task',
        task_id: task.task_id,
    }));
};

export const checkIfAnyValueIsUpdated = (prevValues, currValues) => {
    // If types are different, values are different
    if (typeof prevValues !== typeof currValues) return true;

    // Handle null cases
    if (prevValues === null || currValues === null) {
        return prevValues !== currValues;
    }

    // Handle arrays
    if (Array.isArray(prevValues) && Array.isArray(currValues)) {
        if (prevValues.length !== currValues.length) return true;
        return prevValues.some((value, index) =>
            checkIfAnyValueIsUpdated(value, currValues[index])
        );
    }

    // Handle objects
    if (typeof prevValues === 'object' && typeof currValues === 'object') {
        const prevKeys = Object.keys(prevValues);
        const currKeys = Object.keys(currValues);

        // Check if keys are different
        if (prevKeys.length !== currKeys.length) return true;

        // Check each key-value pair recursively
        return prevKeys.some(
            (key) =>
                !currKeys.includes(key) ||
                checkIfAnyValueIsUpdated(prevValues[key], currValues[key])
        );
    }

    // Handle primitive values
    return prevValues !== currValues;
};
