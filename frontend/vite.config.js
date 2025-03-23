import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tailwindcss from '@tailwindcss/vite';
import fs from 'fs';

export default defineConfig({
    plugins: [react(), tailwindcss()],
    server: {
        https: {
            key: fs.readFileSync('/etc/ssl/certs/pi-localhost.key'),
            cert: fs.readFileSync('/etc/ssl/certs/pi-localhost.crt'),
            // key: fs.readFileSync('../.certs/server.key'),
            // cert: fs.readFileSync('../.certs/server.crt'),
        },
        host: 'localhost',
        port: 3000, // Change this if needed
    },
});
