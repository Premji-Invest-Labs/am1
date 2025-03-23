import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import taskStore from '../../store';
import TaskDetailView from './TaskDetail.view';
import { Button, Spin } from 'antd';
import { getTask, startTask } from '../../apiClient';
import { DUMMY_TASK_ID } from '../../constants';
import NoTaskScreen from './NoTaskScreen';

const TaskDetailController = () => {
    const { id } = useParams();

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const [currTask, setCurrTask] = useState(null);

    const [taskLoading, setTaskLoading] = useState(false);

    // Function to fetch task data
    const fetchTask = useCallback(async () => {
        setLoading(true);
        const response = await getTask(id);
        if (response) {
            setCurrTask(response);
        } else {
            setError(response?.message || 'Failed to fetch task');
        }
        setLoading(false);
    }, [id]);

    // Funciton to start task
    const handleStartTask = async (taskId) => {
        setTaskLoading(true);
        await startTask(taskId);
        await fetchTask();
        setTaskLoading(false);
    };

    useEffect(() => {
        if (id && id !== DUMMY_TASK_ID) fetchTask();
    }, [id, fetchTask]);

    if (loading) return <p>Loading...</p>;
    if (id === DUMMY_TASK_ID) return <NoTaskScreen />;

    if (error) {
        return (
            <div>
                <p>{error}</p>
                <Button onClick={() => window.location.reload()}>Retry</Button>
            </div>
        );
    }

    if (!currTask) return <p>No task found.</p>;

    return (
        <Spin spinning={taskLoading} tip="Recreating task...">
            <TaskDetailView
                handleStartTask={handleStartTask}
                refetchTask={fetchTask}
                task={currTask}
            />
        </Spin>
    );
};

export default TaskDetailController;
