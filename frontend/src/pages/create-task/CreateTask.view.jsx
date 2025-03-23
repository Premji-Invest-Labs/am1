import React from 'react';
import { Input, Button, Select, Tooltip } from 'antd';
import {
    PaperClipOutlined,
    SendOutlined,
    GlobalOutlined,
} from '@ant-design/icons';
import {
    LLM_MODELS,
    MODEL_PARAMS_TOOLTIP_TEXT,
    MULTI_AGENT_FRAMEWORKS,
} from '../../constants';
const { TextArea } = Input;

const CreateTaskView = ({
    handleModelChange,
    tasksInput,
    handleQueryTextChange,
    handleInternetSwitch,
    handleSubmit,
    handleAttachmentButtonClick,
}) => {
    const { query: queryText, enableInternet: isInternetEnabled } = tasksInput;

    return (
        <div className="gap-20 flex flex-col items-center justify-center mt-40">
            <h1 className="text-2xl font-bold text-center text-gray-600">
                How can I help you today?
            </h1>

            <div className="flex flex-1 items-center p-5 bg-gray-100 rounded-3xl w-2/3 flex-col min-w-[300px]">
                <div className="flex w-full items-center gap-1">
                    <TextArea
                        className="w-full flex-1 mt-1 bg-gray-100 border-none text-base resize-none"
                        value={queryText}
                        onChange={handleQueryTextChange}
                        placeholder="Enter your query here"
                        autoSize={{ minRows: 1, maxRows: 6 }}
                        style={{
                            minWidth: '0',
                            border: 'none',
                            background: 'transparent',
                            boxShadow: 'none',
                            display: 'flex',
                            alignItems: 'center',
                        }}
                    />
                    <Tooltip title="Click to start the task">
                        <Button
                            onClick={handleSubmit}
                            className="text-gray-800 p-1.5 bg-gray-100 border-none rounded-lg hover:!text-gray-600 hover:!border-gray-200 !transition-colors hover:!bg-none"
                        >
                            <SendOutlined size={26} className="!text-current" />
                        </Button>
                    </Tooltip>
                </div>

                <div className="flex flex-wrap  justify-between items-center gap-4 mt-5 w-full">
                    <div className="flex items-center gap-2">
                        <Tooltip title="Click to attach files">
                            <div
                                className="p-2 border-2 border-white rounded-full bg-white cursor-pointer transition-colors flex items-center justify-center w-10 h-8 hover:text-gray-800"
                                onClick={handleAttachmentButtonClick}
                            >
                                <PaperClipOutlined size={20} />
                            </div>
                        </Tooltip>
                        <Tooltip
                            title={`Click here to ${
                                isInternetEnabled ? 'disable' : 'enable'
                            } internet for this task`}
                        >
                            <Button
                                className={`   p-1.5 border-none flex items-center gap-2 rounded-full transition-colors
                                    ${
                                        isInternetEnabled
                                            ? '!text-[#4096ff] hover:!text-[#4096ff] !bg-blue-50 hover:!bg-blue-100 hover:!border-blue-100    !border-blue-100'
                                            : '!text-gray-800 hover:!text-gray-600 !bg-white hover:!bg-gray-200 hover:!border-gray-100'
                                    }`}
                                onClick={handleInternetSwitch}
                            >
                                <GlobalOutlined
                                    style={{
                                        fontSize: '18px',
                                        color: 'inherit',
                                    }}
                                />
                                Search
                            </Button>
                        </Tooltip>
                    </div>
                    <div className="flex gap-4">
                        <Tooltip title={MODEL_PARAMS_TOOLTIP_TEXT.LLM}>
                            <Select
                                defaultValue={LLM_MODELS[0].value}
                                options={LLM_MODELS}
                                disabled={LLM_MODELS.length === 1}
                                onChange={handleModelChange}
                                className="[&_.ant-select-selection-item]:text-xs"
                            />
                        </Tooltip>
                        <Tooltip title={MODEL_PARAMS_TOOLTIP_TEXT.MAF}>
                            <Select
                                defaultValue={MULTI_AGENT_FRAMEWORKS[0].value}
                                options={MULTI_AGENT_FRAMEWORKS}
                                disabled={MULTI_AGENT_FRAMEWORKS.length === 1}
                                onChange={handleModelChange}
                                className="[&_.ant-select-selection-item]:text-xs"
                            />
                        </Tooltip>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CreateTaskView;
