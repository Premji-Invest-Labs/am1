import React from 'react';
import StatusPillView from './StatusPill.view';

const StatusPillController = ({ status }) => {
    const statusStyles = {
        success: 'bg-green-100 text-green-700 border border-green-300',
        in_progress: 'bg-blue-100 text-blue-700 border border-blue-300',
        failure: 'bg-red-100 text-red-700 border border-red-300',
        created: 'bg-gray-100 text-gray-700 border border-gray-300',
        partial_success:
            'bg-yellow-100 text-yellow-700 border border-yellow-300',
    };

    const statusStyle = statusStyles[status] || statusStyles.default;

    return <StatusPillView status={status} statusStyle={statusStyle} />;
};

export default StatusPillController;
