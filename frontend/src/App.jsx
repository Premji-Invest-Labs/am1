import { useEffect, useState } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { PATH_NAMES } from './constants';
import CreateTaskController from './pages/create-task';
import LayoutController from './components/layout';
import AllTasksController from './pages/all-tasks';
import taskStore from './store';
import TaskDetailControllers from './pages/task-detail';

function App() {
    const [collapsed, setCollapsed] = useState(false);
    const { fetchTasks } = taskStore();
    useEffect(() => {
        fetchTasks(); // Fetch tasks on app startup
    }, []);

    return (
        <Router>
            <LayoutController collapsed={collapsed} setCollapsed={setCollapsed}>
                <Routes>
                    <Route
                        path={PATH_NAMES.DASHBOARD}
                        element={<CreateTaskController />}
                    />
                    <Route
                        path={PATH_NAMES.ALL_TASKS}
                        element={<AllTasksController collapsed={collapsed} />}
                    />

                    {/* for detailed individual task */}
                    <Route
                        path={PATH_NAMES.TASK_DETAIL}
                        element={<TaskDetailControllers />}
                    />
                </Routes>
            </LayoutController>
        </Router>
    );
}

export default App;
