import React from 'react';
import { ArrowRightOutlined } from '@ant-design/icons';
import { TASK_CARD_TOOLTIP_TEXT, TASKS_STATUS } from '../../constants';
import { Tooltip } from 'antd';

const DashboardView = ({
    handleCreateNewTask,
    handleTaskCardClick,
    tasksCount,
}) => {
    return (
        <div className="main">
            <div className="flex flex-col gap-20 mt-10">
                <div className="flex flex-col gap-6">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                        <Tooltip title={TASK_CARD_TOOLTIP_TEXT.SUCCESS}>
                            <div
                                className="bg-green-100 shadow-md rounded-lg p-4 cursor-pointer"
                                onClick={() =>
                                    handleTaskCardClick(TASKS_STATUS.SUCCESS)
                                }
                            >
                                <h2 className="text-lg font-bold">
                                    Completed Tasks
                                </h2>
                                <p className="text-2xl font-bold">
                                    {tasksCount[TASKS_STATUS.SUCCESS]}
                                </p>
                            </div>
                        </Tooltip>
                        <Tooltip title={TASK_CARD_TOOLTIP_TEXT.IN_PROGRESS}>
                            <div
                                className="bg-yellow-100 shadow-md rounded-lg p-4 cursor-pointer"
                                onClick={() =>
                                    handleTaskCardClick(
                                        TASKS_STATUS.IN_PROGRESS
                                    )
                                }
                            >
                                <h2 className="text-lg font-bold">
                                    In Progress Tasks
                                </h2>
                                <p className="text-2xl font-bold">
                                    {tasksCount[TASKS_STATUS.IN_PROGRESS]}
                                </p>
                            </div>
                        </Tooltip>

                        <Tooltip title={TASK_CARD_TOOLTIP_TEXT.FAILED}>
                            <div
                                className="bg-red-100 shadow-md rounded-lg p-4 cursor-pointer"
                                onClick={() =>
                                    handleTaskCardClick(TASKS_STATUS.FAILED)
                                }
                            >
                                <h2 className="text-lg font-bold">
                                    Failed Tasks
                                </h2>
                                <p className="text-2xl font-bold">
                                    {tasksCount[TASKS_STATUS.FAILED]}
                                </p>
                            </div>
                        </Tooltip>
                        <Tooltip title={TASK_CARD_TOOLTIP_TEXT.CREATED}>
                            <div
                                className="bg-blue-100 shadow-md rounded-lg p-4 cursor-pointer"
                                onClick={() =>
                                    handleTaskCardClick(TASKS_STATUS.CREATED)
                                }
                            >
                                <h2 className="text-lg font-bold">
                                    Created Tasks
                                </h2>
                                <p className="text-2xl font-bold">
                                    {tasksCount[TASKS_STATUS.CREATED]}
                                </p>
                            </div>
                        </Tooltip>
                    </div>
                </div>
                <Tooltip title={TASK_CARD_TOOLTIP_TEXT.NEW}>
                    <div
                        className="bg-gray-50 shadow-md rounded-lg p-4 cursor-pointer justify-between items-center flex"
                        onClick={handleCreateNewTask}
                    >
                        <div className="flex flex-col gap-2">
                            <h2 className="text-lg font-bold">
                                Create a new task
                            </h2>
                            <p className="text-sm font-bold">
                                Enter your query and upload files to get the
                                response
                            </p>
                        </div>

                        <ArrowRightOutlined className="text-xl pr-10" />
                    </div>
                </Tooltip>
            </div>
        </div>
    );
};

export default DashboardView;
