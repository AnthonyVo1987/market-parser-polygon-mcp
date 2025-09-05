import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // Bundle analysis - activated by ANALYZE env var or production build
    (process.env.ANALYZE || process.env.NODE_ENV === 'production') && visualizer({
      filename: 'dist/bundle-analysis.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
      template: 'treemap' // or 'sunburst', 'network'
    })
  ].filter(Boolean),
  server: {
    port: 3000,
    host: true,
    warmup: {
      clientFiles: ['./src/main.tsx', './src/App.tsx']
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  optimizeDeps: {
    // Pre-bundle these dependencies for faster cold starts
    include: [
      'react',
      'react-dom',
      'react-markdown'
    ],
    // Exclude problematic dependencies if needed
    exclude: []
  }
})