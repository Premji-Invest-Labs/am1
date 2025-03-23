import React, { useState } from 'react';
import CreateTaskView from './CreateTask.view';
import FileUploadModalController from '../../components/modals/file-upload-modal';
import {
    CREATE_TASK_SOURCES,
    LLM_MODELS,
    MULTI_AGENT_FRAMEWORKS,
    PATH_NAMES,
} from '../../constants';
import { createTask, startTask } from '../../apiClient';
import { useNavigate } from 'react-router-dom';
import { Spin } from 'antd';
import NotificationController from '../../components/notification';
import { checkIfAnyValueIsUpdated } from '../../utils';
import taskStore from '../../store';

const CreateTaskController = () => {
    const [openFileModal, setOpenFileModal] = React.useState(false);
    const [tasksInput, setTasksInput] = React.useState({
        query: '',
        model: LLM_MODELS[0].value,
        enableInternet: true,
        maf: MULTI_AGENT_FRAMEWORKS[0].value,
    });
    const [createdTasksInput, setCreatedTasksInput] = useState({
        query: '',
        model: LLM_MODELS[0].value,
        enableInternet: true,
        maf: MULTI_AGENT_FRAMEWORKS[0].value,
    });
    const [loading, setLoading] = React.useState(false);
    const [taskId, setTaskId] = React.useState('');
    const navigate = useNavigate();
    const { openNotification, contextHolder } = NotificationController();
    const { fetchTasks } = taskStore();

    const handleCreateTask = async (source = CREATE_TASK_SOURCES.SUBMIT) => {
        if (
            !tasksInput.query.trim() &&
            source !== CREATE_TASK_SOURCES.ATTACHMENT
        ) {
            openNotification(
                'warning',
                'Invalid Input',
                'Please enter your query before continuing'
            );
            return;
        }
        let payload = {
            query: tasksInput.query,
            enable_internet: tasksInput.enableInternet,
            multi_agent_framework: tasksInput.maf,
            llm_model: tasksInput.model,
        };

        if (taskId) {
            payload = { ...payload, task_id: taskId };
        }

        setCreatedTasksInput(tasksInput);
        const response = await createTask(payload);
        if (response?.task_id) {
            setTaskId(response.task_id);
            return response?.task_id;
        }
    };
    const handleStartTask = async (taskId) => {
        const startTaskResponse = await startTask(taskId);
        if (startTaskResponse) {
            fetchTasks();
            navigate(`${PATH_NAMES.TASK_DETAIL_BASE}${taskId}`);
        } else {
            openNotification('error', 'Error', 'Failed to start task');
        }
    };
    const handleSubmit = async () => {
        setLoading(true);
        // task id is present as well as post creation no input value should be updated then start, else create new
        if (
            !!taskId &&
            !checkIfAnyValueIsUpdated(createdTasksInput, tasksInput)
        ) {
            await handleStartTask(taskId);
        } else {
            const taskId = await handleCreateTask();

            if (taskId) {
                await handleStartTask(taskId);
            } else if (!!tasksInput.query.trim()) {
                openNotification('error', 'Error', 'Failed to create task');
            }
        }
        setLoading(false);
    };
    const handleAttachmentButtonClick = () => {
        if (!tasksInput?.query?.length) {
            openNotification(
                'warning',
                'Empty Input',
                'Please enter your query before continuing'
            );
        } else if (
            !(
                !!taskId &&
                !checkIfAnyValueIsUpdated(createdTasksInput, tasksInput)
            )
        ) {
            handleCreateTask(CREATE_TASK_SOURCES.ATTACHMENT);
            setOpenFileModal(true);
        }
    };

    const handleModelChange = () => {};

    const handleModalClose = () => {
        setOpenFileModal(false);
    };

    const handleQueryTextChange = (e) => {
        setTasksInput({ ...tasksInput, query: e.target.value });
    };

    const handleFileSubmit = (fileList) => {
        setTasksInput({ ...tasksInput, fileList });
        setOpenFileModal(false);
        handleSubmit();
    };
    const handleInternetSwitch = () => {
        setTasksInput({
            ...tasksInput,
            enableInternet: !tasksInput.enableInternet,
        });
        openNotification(
            'info',
            `Internet ${
                tasksInput.enableInternet ? 'disabled' : 'enabled'
            } for the query`,
            '',
            1
        );
    };

    return (
        <>
            {contextHolder}
            <Spin spinning={loading} tip="Creating task...">
                <CreateTaskView
                    handleModelChange={handleModelChange}
                    tasksInput={tasksInput}
                    handleQueryTextChange={handleQueryTextChange}
                    handleInternetSwitch={handleInternetSwitch}
                    handleSubmit={handleSubmit}
                    handleAttachmentButtonClick={handleAttachmentButtonClick}
                />
                <FileUploadModalController
                    handleModalClose={handleModalClose}
                    openFileModal={openFileModal}
                    handleFileSubmit={handleFileSubmit}
                    taskId={taskId}
                />
            </Spin>
        </>
    );
};

export default CreateTaskController;
