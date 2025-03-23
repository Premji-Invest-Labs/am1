import React from 'react';

const NoResultScreen = () => {
    return (
        <div className="flex items-center justify-center h-full p-5 m-10 border-2 border-dashed border-gray-300 rounded-lg">
            <div className="text-center">
                <h3 className="text-lg font-semibold text-gray-600">
                    No Tasks Found
                </h3>
                <p className="text-sm text-gray-500">
                    Try adjusting your search or filters
                </p>
            </div>
        </div>
    );
};

export default NoResultScreen;
