import React, {
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from 'react';
import { useSearchParams } from 'react-router-dom';
import AllTasksView from './AllTasks.view';
import { allTaskColDef } from './constants';
import taskStore from '../../store';
import { TASKS_STATUS } from '../../constants';

const AllTasksController = ({ collapsed }) => {
    const gridRef = useRef(null);
    const { tasks } = taskStore();
    const [searchParams] = useSearchParams();

    const [quickFilterText, setQuickFilterText] = useState('');
    const [colDefs] = useState(allTaskColDef);
    const hasSetInitialTab = useRef(false); // Ref to ensure initial tab logic runs only once

    // Determine initial tab only once when the component mounts
    const [activeTab, setActiveTab] = useState(() => {
        const urlStatus = searchParams.get('status');
        if (!urlStatus) return 'all'; // If no param, default to 'all' immediately

        if (!hasSetInitialTab.current) {
            hasSetInitialTab.current = true; // Mark that we've set the initial tab
            const validStatuses = new Set(Object.values(TASKS_STATUS));
            return validStatuses.has(urlStatus) ? urlStatus : 'all';
        }
        return 'all';
    });

    // Sort tasks only once when `tasks` changes
    const sortedTasks = useMemo(() => {
        if (!tasks?.length) return [];
        return [...tasks].sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
    }, [tasks]);

    const rowData = useMemo(() => {
        if (!tasks?.length) return [];

        const filteredTasks =
            activeTab === 'all'
                ? tasks
                : tasks.filter(
                      (task) =>
                          task.status?.toLowerCase() === activeTab.toLowerCase()
                  );

        return filteredTasks.sort(
            (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );
    }, [tasks, activeTab]);
    const handleTabClick = useCallback((status) => {
        setActiveTab(status);
    }, []);

    const onFilterTextBoxChanged = (e) => setQuickFilterText(e.target.value);

    const defaultColDef = useMemo(
        () => ({
            resizable: false,
            movable: true,
            lockVisible: true,
            sortable: true,
            resizable: true,
        }),
        []
    );

    const autoSizeStrategy = useMemo(
        () => ({
            type: 'fitGridWidth',
        }),
        []
    );

    return (
        <AllTasksView
            collapsed={collapsed}
            quickFilterText={quickFilterText}
            onFilterTextBoxChanged={onFilterTextBoxChanged}
            rowData={rowData}
            handleTabClick={handleTabClick}
            gridRef={gridRef}
            defaultColDef={defaultColDef}
            autoSizeStrategy={autoSizeStrategy}
            activeTab={activeTab}
            colDefs={colDefs}
            setActiveTab={setActiveTab}
        />
    );
};

export default AllTasksController;
