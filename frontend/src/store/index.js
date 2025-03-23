import { create } from 'zustand';
import axios from 'axios';
import { getAllTasks } from '../apiClient';

const taskStore = create((set, get) => ({
    tasks: [],
    loading: false,
    error: null,

    // Fetch  all tasks
    fetchTasks: async () => {
        set({ loading: true, error: null });
        const response = await getAllTasks();
        if (response.length > 0) {
            set({ tasks: response, loading: false });
        } else {
            set({ error: response.message, loading: false });
        }
    },

    addTask: (task) => set((state) => ({ tasks: [...state.tasks, task] })),
    removeTask: (id) =>
        set((state) => ({
            tasks: state.tasks.filter((task) => task.id !== id),
        })),
    updateTask: (id, updatedTask) =>
        set((state) => ({
            tasks: state.tasks.map((task) =>
                task.id === id ? updatedTask : task
            ),
        })),
}));

export default taskStore;
