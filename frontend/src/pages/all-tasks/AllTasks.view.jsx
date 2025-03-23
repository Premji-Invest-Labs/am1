import React, { useMemo } from 'react';
import { Button, Segmented } from 'antd';
import { TASKS_STATUS } from '../../constants';
import {
    AllCommunityModule,
    ClientSideRowModelModule,
    ModuleRegistry,
} from 'ag-grid-community';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-quartz.css';

import { AgGridReact } from 'ag-grid-react';
import { paginationPageSizeSelector } from './constants';
import NoResultScreen from './NoResultScreen';
import taskStore from '../../store';
import { getTaskCountByStatus } from '../../utils';

ModuleRegistry.registerModules([AllCommunityModule, ClientSideRowModelModule]);

const AllTasksView = ({
    collapsed,
    activeTab,
    onFilterTextBoxChanged,
    quickFilterText,
    gridRef,
    defaultColDef,
    autoSizeStrategy,
    rowData,
    colDefs,
    handleTabClick,
}) => {
    const { tasks } = taskStore();
    const tasksCount = getTaskCountByStatus(tasks);
    const tabOptions = useMemo(
        () => [
            { label: 'All', value: 'all' },
            ...Object.entries(TASKS_STATUS).map(([key, value]) => ({
                label: `${key
                    .replace(/_/g, ' ') // Replace underscores with spaces
                    .toLowerCase() // Convert everything to lowercase
                    .replace(/\b\w/g, (char) => char.toUpperCase())} ${
                    // Capitalize first letter
                    tasksCount[value] ? `(${tasksCount[value]})` : ''
                }`,
                value,
            })),
        ],
        []
    );

    return (
        <div>
            <div className={`   w-full ${collapsed ? 'mx-auto' : 'px-1'}`}>
                <div className="flex   flex-wrap gap-4 justify-between items-center pb-4 pt-2  ">
                    <Segmented
                        options={tabOptions}
                        onChange={handleTabClick}
                        value={activeTab}
                    />

                    <div className="relative flex items-center">
                        <svg
                            className="absolute left-2 w-4 h-4 text-gray-500"
                            viewBox="0 0 16 16"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M11.5014 7.00039C11.5014 7.59133 11.385 8.1765 11.1588 8.72246C10.9327 9.26843 10.6012 9.7645 10.1833 10.1824C9.76548 10.6002 9.2694 10.9317 8.72344 11.1578C8.17747 11.384 7.59231 11.5004 7.00136 11.5004C6.41041 11.5004 5.82525 11.384 5.27929 11.1578C4.73332 10.9317 4.23725 10.6002 3.81938 10.1824C3.40152 9.7645 3.07005 9.26843 2.8439 8.72246C2.61776 8.1765 2.50136 7.59133 2.50136 7.00039C2.50136 5.80691 2.97547 4.66232 3.81938 3.81841C4.6633 2.97449 5.80789 2.50039 7.00136 2.50039C8.19484 2.50039 9.33943 2.97449 10.1833 3.81841C11.0273 4.66232 11.5014 5.80691 11.5014 7.00039ZM10.6814 11.7404C9.47574 12.6764 7.95873 13.1177 6.43916 12.9745C4.91959 12.8314 3.51171 12.1145 2.50211 10.9698C1.49252 9.8251 0.957113 8.33868 1.0049 6.81314C1.05268 5.28759 1.68006 3.83759 2.75932 2.75834C3.83857 1.67908 5.28856 1.0517 6.81411 1.00392C8.33966 0.956136 9.82608 1.49154 10.9708 2.50114C12.1154 3.51073 12.8323 4.91862 12.9755 6.43819C13.1187 7.95775 12.6773 9.47476 11.7414 10.6804L14.5314 13.4704"
                                fill="currentColor"
                            />
                        </svg>
                        <input
                            type="text"
                            id="filter-text-box"
                            placeholder="Search task..."
                            onChange={onFilterTextBoxChanged}
                            className="pl-8 pr-4 py-2 text-sm border border-gray-300 rounded-md outline-none bg-transparent"
                        />
                    </div>
                </div>

                <div className="ag-theme-quartz h-[75vh]">
                    <AgGridReact
                        theme="legacy"
                        ref={gridRef}
                        columnDefs={colDefs}
                        rowData={rowData}
                        defaultColDef={defaultColDef}
                        rowHeight={80}
                        autoSizeStrategy={autoSizeStrategy}
                        pagination
                        paginationPageSize={10}
                        paginationPageSizeSelector={paginationPageSizeSelector}
                        quickFilterText={quickFilterText}
                        detailRowAutoHeight
                        noRowsOverlayComponent={NoResultScreen}
                        overlayLoadingTemplate={
                            '<span class="ag-overlay-loading-center">Loading...</span>'
                        }
                    />
                </div>
            </div>
        </div>
    );
};

export default AllTasksView;
