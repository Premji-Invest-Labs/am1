export const StatusCellRenderer = ({ value }) => {
    // Ensure value is a string and handle null/undefined cases
    const status = value ? value.toString() : '';

    const tagStyles = {
        base: 'inline-flex items-center rounded-full px-3 py-1 text-sm font-medium border',
        success: 'bg-green-100 text-green-700 border-green-300',
        failure: 'bg-red-100 text-red-700 border-red-300',
        created: 'bg-yellow-100 text-yellow-700 border-yellow-300',
        in_progress: 'bg-blue-100 text-blue-700 border-blue-300',
        empty: 'bg-gray-100 text-gray-400 border-gray-300', // Subtle style for missing status
    };

    const circleStyles = {
        base: 'w-2 h-2 rounded-full mr-2',
        success: 'bg-green-500',
        failure: 'bg-red-500',
        created: 'bg-yellow-500',
        in_progress: 'bg-blue-500',
        empty: 'bg-gray-400',
    };

    return (
        <div
            className={`${tagStyles.base} ${
                tagStyles[status] || tagStyles.empty
            }`}
        >
            {status && (
                <div
                    className={`${circleStyles.base} ${
                        circleStyles[status] || circleStyles.empty
                    }`}
                ></div>
            )}
            <span className="capitalize">
                {status ? status.replace('_', ' ') : 'No Status'}
            </span>
        </div>
    );
};
