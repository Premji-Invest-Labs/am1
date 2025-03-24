import { Button } from 'antd';
import { ExpandAltOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import taskStore from '../../store';
const ActionsCellRenderer = (props) => {
    const navigate = useNavigate();

    const handleOpenTask = (value) => {
        navigate(`/task/${props.data.task_id}`); // Navigate to detail page
    };

    return (
        <div className="flex justify-center h-full items-center   gap-2">
            <Button
                onClick={handleOpenTask}
                icon={<ExpandAltOutlined />}
                className="h-fit px-4 border border-gray-300 rounded-md shadow-sm bg-white hover:bg-gray-100"
            >
                Open Task
            </Button>
        </div>
    );
};

export default ActionsCellRenderer;
