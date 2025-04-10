import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,  // Force Vite to use port 3000
    strictPort: true,  // Don't fallback to 5173
    proxy: {
      '/api': 'http://localhost:8000'  // Ensure this matches your backend
    }
  }
})