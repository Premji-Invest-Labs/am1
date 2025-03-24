import { uploadFile } from '../../../apiClient';
import FileUploadModalView from './FileUploadModal.view';
import { useState } from 'react';

const FileUploadModalController = ({
    handleModalClose,
    openFileModal,
    handleFileSubmit,
    taskId,
}) => {
    const [fileList, setFileList] = useState([]);

    const handleUpload = async () => {
        try {
            const uploadPromises = fileList.map(async (file) => {
                const formData = new FormData();
                formData.append('input_file', file.originFileObj); // Ensure the key matches API expectations

                const response = await uploadFile(taskId, formData);
                if (response) {
                    return response;
                } else {
                    return null;
                }
            });

            const results = await Promise.all(uploadPromises);
            handleFileSubmit(results.filter(Boolean));
            handleModalClose();
        } catch (error) {
            console.error('Upload error:', error);
        }
    };
    const draggerProps = {
        name: 'file',
        multiple: true,
        beforeUpload: (file) => {
            return false;
        },
        onChange(info) {
            const newFileList = [...info.fileList];

            // Update status for newly added files
            newFileList.forEach((file) => {
                if (!file.status) {
                    file.status = 'ready';
                }
            });

            setFileList(newFileList);

            if (info.file.status === 'ready') {
            }
        },
        onDrop(e) {
            console.log('Dropped files', e.dataTransfer.files);
        },
        fileList: fileList,
    };
    return (
        <FileUploadModalView
            handleModalClose={handleModalClose}
            openFileModal={openFileModal}
            handleFileSubmit={handleFileSubmit}
            draggerProps={draggerProps}
            fileList={fileList}
            handleOkClick={handleUpload}
        />
    );
};

export default FileUploadModalController;
