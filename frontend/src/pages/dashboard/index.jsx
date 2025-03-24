import React from 'react';
import DashboardView from './Dashboard.view';
import { useNavigate } from 'react-router-dom';
import { PATH_NAMES } from '../../constants';
import taskStore from '../../store';
import { getTaskCountByStatus } from '../../utils';

const DashboardController = () => {
    const navigate = useNavigate();
    const handleCreateNewTask = () => {
        navigate(PATH_NAMES.CREATE_TASK);
    };
    const { tasks } = taskStore();
    const tasksCount = getTaskCountByStatus(tasks);

    const handleTaskCardClick = (status) => {
        const searchParams = new URLSearchParams({
            status,
        }).toString();

        navigate({
            pathname: PATH_NAMES.ALL_TASKS,
            search: `?${searchParams}`,
        });
    };

    return (
        <DashboardView
            handleCreateNewTask={handleCreateNewTask}
            handleTaskCardClick={handleTaskCardClick}
            tasksCount={tasksCount}
        />
    );
};

export default DashboardController;
