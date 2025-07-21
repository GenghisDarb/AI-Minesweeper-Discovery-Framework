import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()], // Added React plugin for JSX support
  root: './', // Updated root to point to the new index.html
  build: {
    outDir: 'dist', // Output directory for the build
  },
});
