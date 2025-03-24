import React from 'react';

// Utility function to format the status
const formatStatus = (status) => {
    return status
        .replace(/_/g, ' ') // Replace underscores with spaces
        .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitalize the first letter of each word
};

const StatusPillView = ({ status, statusStyle }) => {
    const formattedStatus = status ? formatStatus(status) : 'Pending';

    return (
        <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${statusStyle}`}
        >
            {formattedStatus}
        </span>
    );
};

export default StatusPillView;
