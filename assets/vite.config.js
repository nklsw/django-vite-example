import { defineConfig } from 'vite';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss()],
  
  // Simple static paths instead of env variables
  root: resolve('./src'),
  base: '/static/',
  
  build: {
    // Single output location
    outDir: resolve('../assets_dist'),
    emptyOutDir: true,
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        main: resolve('./src/js/main.js'),
        styles: resolve('./src/css/main.css')
      }
    }
  },
  
  // Fixed development server settings
  server: {
    host: '0.0.0.0',
    port: 5173,
    origin: 'http://localhost:5173'
  }
});