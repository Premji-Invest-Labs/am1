import { InboxOutlined } from '@ant-design/icons';
import { Upload, Modal } from 'antd';
const { Dragger } = Upload;

const FileUploadModalView = ({
    handleModalClose,
    openFileModal,
    draggerProps,
    handleOkClick,
}) => {
    return (
        <Modal
            title="Upload files here"
            open={openFileModal}
            onOk={handleOkClick}
            onCancel={handleModalClose}
            onClose={handleModalClose}
            okButtonProps={{
                className: 'hover:!bg-gray-400',
                style: {
                    backgroundColor: '#000',
                },
            }}
            cancelButtonProps={{
                className: 'hover:!text-black hover:!border-black',
                style: {
                    backgroundColor: '#fff',
                },
            }}
        >
            <Dragger {...draggerProps}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined style={{ color: '#9CA3AF' }} />
                </p>
                <p className="ant-upload-text">
                    Click or drag file to this area to upload
                </p>
                <p className="ant-upload-hint">
                    Upload all the required files here
                </p>
            </Dragger>
        </Modal>
    );
};

export default FileUploadModalView;
