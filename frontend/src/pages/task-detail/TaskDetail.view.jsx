'use client';
import React from 'react';

import dayjs from 'dayjs';
import { Button, Skeleton } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';

import MarkdownRendererController from '../../components/mardown-renderer';
import StatusPillController from '../../components/status-pill';
import { TASKS_STATUS } from '../../constants';

const TaskDetailView = ({ task, refetchTask, handleStartTask }) => {
    return (
        <div className="w-[95%] mx-auto p-6 bg-white rounded-lg shadow-lg border border-gray-200 mt-5">
            {/* Header Section */}
            <div className="flex justify-between items-start mb-4">
                <div>
                    <div className="flex items-center gap-2">
                        <h1 className="text-2xl font-semibold text-gray-800">
                            Task Status :
                        </h1>
                        <StatusPillController
                            status={task?.status || 'Unknown'}
                        />
                    </div>
                    <p className="text-gray-500 text-xs mt-1">
                        Task Id: {task.task_id}
                    </p>
                </div>

                {[TASKS_STATUS.CREATED, TASKS_STATUS.FAILED].includes(
                    task.status
                ) ? (
                    <Button
                        icon={<ReloadOutlined />}
                        className="px-4 py-2 bg-gray-100 border border-gray-300 rounded-md text-sm font-medium hover:bg-gray-200 transition"
                        onClick={() => handleStartTask(task.task_id)}
                    >
                        Restart Task
                    </Button>
                ) : (
                    <Button
                        icon={<ReloadOutlined />}
                        onClick={refetchTask}
                        className="px-4 py-2 bg-gray-100 border border-gray-300 rounded-md text-sm font-medium hover:bg-gray-200 transition"
                    >
                        Refetch Status
                    </Button>
                )}
            </div>

            {/* Task Details */}
            <div className="space-y-2 text-gray-700 mb-4">
                {[
                    { label: 'LLM Model', value: task.llm_model },
                    {
                        label: 'Multi-Agent Framework',
                        value: task.multi_agent_framework,
                    },
                    {
                        label: 'Internet Enabled',
                        value: task.enable_internet ? 'Yes' : 'No',
                    },
                    {
                        label: 'Created At',
                        value: dayjs(task.created_at).format(
                            'MMM DD, YYYY - hh:mm A'
                        ),
                    },
                ].map(({ label, value }) => (
                    <p key={label}>
                        <span className="font-semibold text-gray-900">
                            {label}:
                        </span>{' '}
                        {value}
                    </p>
                ))}

                <p>
                    <div className="font-semibold text-gray-900">
                        Files Included:
                    </div>
                    {task?.input_file_names?.length === 0 ? (
                        <p className="text-xs text-gray-400 italic">
                            No files included
                        </p>
                    ) : (
                        <ul className="list-disc ml-5">
                            {task.input_file_names?.map((file, index) => (
                                <li key={index}>{file}</li>
                            ))}
                        </ul>
                    )}
                </p>
            </div>

            {/* Divider */}
            <hr className="border-gray-300 my-5" />

            {/* Query Section */}
            <h3 className="text-xl font-semibold text-gray-800">Query</h3>
            <div className="mt-3 ml-5">
                <MarkdownRendererController
                    content={
                        task?.query ||
                        "## Invaild query received from backend :'("
                    }
                    type="query"
                />
            </div>

            {/* Divider */}
            <hr className="border-gray-300 my-5" />

            {/* Final Response Section */}
            <h3 className="text-xl font-semibold text-gray-800">
                Final Response
            </h3>
            <div className="mt-3 p-4 bg-gray-100 border border-gray-300 rounded-md">
                {task?.status === TASKS_STATUS.IN_PROGRESS ? (
                    <div className="space-y-4">
                        <p className="text-xs font-semibold text-gray-500  ">
                            Grab a cup of coffee ☕️ while our agents are formulating the
                            perfect response for you{' '}
                            <span className="emoji-animation"> </span>
                        </p>

                        <Skeleton
                            active
                            paragraph={{ rows: 4 }}
                            title={false}
                            className="!mt-0"
                        />
                    </div>
                ) : task.final_response ? (
                    <MarkdownRendererController
                        content={task.final_response}
                        type="response"
                    />
                ) : (
                    <p className="text-gray-500 italic">*No response yet.*</p>
                )}
            </div>
        </div>
    );
};

export default TaskDetailView;
