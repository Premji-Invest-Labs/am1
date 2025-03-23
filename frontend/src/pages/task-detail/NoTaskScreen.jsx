import React from 'react';

const NoTaskScreen = () => {
    return (
        <div className="flex items-center flex-col w-full justify-center h-full mb-10">
            <div className="flex items-center gap-2">
                <h1 className="text-2xl font-semibold text-gray-800">
                    Once you create a task, all the details corresponding to
                    that will be shown here
                </h1>
            </div>
        </div>
    );
};

export default NoTaskScreen;
