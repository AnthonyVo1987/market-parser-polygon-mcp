import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load environment variables from root directory
  const env = loadEnv(mode, process.cwd(), '')

  // Environment detection
  const isProduction = mode === 'production'
  const isDevelopment = mode === 'development'
  const isBuild = command === 'build'
  
  return {
    // Build configuration
    root: '.', // Root is project root
    publicDir: 'public',
    
    plugins: [
      react(),
      // PWA functionality with auto-update strategy
      VitePWA({
        registerType: 'autoUpdate',
        workbox: {
          globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2,webmanifest,json}'],
          cleanupOutdatedCaches: true,
          sourcemap: isProduction,
          runtimeCaching: [
            {
              urlPattern: new RegExp(`^http://127\.0\.0\.1:8000\/api\/`),
              handler: 'NetworkFirst',
              options: {
                cacheName: 'api-cache',
                networkTimeoutSeconds: 10,
                cacheableResponse: {
                  statuses: [0, 200]
                }
              }
            },
            {
              urlPattern: /\/manifest\.webmanifest$/,
              handler: 'StaleWhileRevalidate',
              options: {
                cacheName: 'manifest-cache'
              }
            }
          ]
        },
        includeAssets: ['favicon.ico'],
        manifest: {
          name: 'Market Parser OpenAI Chat',
          short_name: 'MarketParser',
          description: 'AI-powered financial market analysis chat application with real-time data from Polygon.io',
          theme_color: '#000000',
          background_color: '#ffffff',
          display: 'standalone',
          scope: '/',
          start_url: '/',
          orientation: 'portrait-primary',
          icons: [
            {
              src: 'pwa-192x192.png',
              sizes: '192x192',
              type: 'image/png',
              purpose: 'any'
            },
            {
              src: 'pwa-512x512.png',
              sizes: '512x512', 
              type: 'image/png',
              purpose: 'any'
            },
            {
              src: 'pwa-192x192.png',
              sizes: '192x192',
              type: 'image/png',
              purpose: 'maskable'
            }
          ]
        },
        // Development options
        devOptions: {
          enabled: isDevelopment,
          type: 'module'
        }
      }),
      // Bundle analysis - environment-aware configuration
      (env.ANALYZE || isProduction) && visualizer({
        filename: 'dist/bundle-analysis.html',
        open: !isBuild, // Only auto-open in development
        gzipSize: true,
        brotliSize: true,
        template: 'treemap', // treemap, sunburst, network
        title: `Bundle Analysis - ${mode.toUpperCase()}`,
        sourcemap: isProduction // Enable source map analysis in production
      })
    ].filter(Boolean),
    // Development server configuration (only applies in dev mode)
    server: {
      host: '127.0.0.1',
      port: 3000,
      strictPort: true, // Fail if port 3000 is busy, no dynamic port allocation
      // Enable CORS for root-level development and cross-origin requests
      cors: true,
      // Phase 1: Server warmup optimization for faster cold starts
      warmup: {
        clientFiles: ['./src/frontend/main.tsx', './src/frontend/App.tsx']
      },
      // Phase 1: Static proxy configuration for backend integration
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          secure: false
        }
      }
    },
    build: {
      // Environment-aware minification
      minify: isProduction ? 'terser' : false,
      terserOptions: {
        compress: {
          // Production-only optimizations
          drop_console: isProduction,
          drop_debugger: isProduction,
          pure_funcs: isProduction ? ['console.log', 'console.info', 'console.debug'] : []
        },
        mangle: {
          // Preserve function names in development for better debugging
          keep_fnames: isDevelopment
        }
      },
      
      // Source map configuration based on environment
      sourcemap: isProduction ? 'hidden' : true, // Hidden in production, full in development
      
      // Build output to root dist directory
      outDir: 'dist',
      emptyOutDir: true, // Always clean output directory
      reportCompressedSize: isProduction, // Show gzip sizes in production builds
    
      
      // Asset optimization settings
      assetsInlineLimit: 4096, // 4KB threshold for inlining small assets as base64 data URLs
      cssCodeSplit: true, // Enable CSS code splitting for better caching
      
      // Environment-aware performance settings
      chunkSizeWarningLimit: isProduction ? 500 : 1000, // Stricter limits in production
      
      // Build performance optimization
      ...(isProduction && {
        target: 'es2015', // Ensure broad browser compatibility in production
        cssTarget: 'chrome61' // CSS compatibility target
      }),
    
      
      // Phase 2: Advanced build optimizations with manual chunking
      rollupOptions: {
        output: {
          // Optimized chunking strategy for better caching
          manualChunks: {
            // Core React libraries (stable, rarely changes)
            vendor: ['react', 'react-dom'],
            // Heavy markdown processing library (45KB, separate chunk)
            markdown: ['react-markdown'],
            // PWA-related workbox libraries (separate chunk for better caching)
            pwa: ['workbox-window']
          },
          
          // Intelligent asset organization by type with content hashes
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.')
            const ext = info[info.length - 1]
            
            // Images: PNG, JPG, JPEG, SVG, GIF, WebP, etc.
            if (/png|jpe?g|svg|gif|tiff|bmp|ico|webp/i.test(ext)) {
              return `images/[name].[hash].[ext]`
            }
            
            // CSS files
            if (/css/i.test(ext)) {
              return `css/[name].[hash].[ext]`
            }
            
            // Fonts: WOFF, WOFF2, TTF, EOT, etc.
            if (/woff2?|ttf|eot|otf/i.test(ext)) {
              return `fonts/[name].[hash].[ext]`
            }
            
            // Everything else goes to general assets
            return `assets/[name].[hash].[ext]`
          },
          chunkFileNames: 'js/[name].[hash].js',
          entryFileNames: 'js/[name].[hash].js'
        }
      }
    },
    // Phase 1: Dependency optimization for faster cold starts
    optimizeDeps: {
      // Pre-bundle these dependencies for faster development startup
      include: [
        'react',
        'react-dom',
        'react-markdown',
        'workbox-window'
      ],
      // Exclude problematic dependencies if needed
      exclude: [],
      // Force re-optimization in development if needed
      force: isDevelopment && env.FORCE_OPTIMIZE === 'true'
    },
    
    // Environment variable configuration
    define: {
      // Expose build information to the application
      __BUILD_MODE__: JSON.stringify(mode),
      __BUILD_TIMESTAMP__: JSON.stringify(new Date().toISOString()),
      __IS_PRODUCTION__: JSON.stringify(isProduction),
      // Environment-specific build information
      __APP_ENV__: JSON.stringify(env.VITE_APP_ENV || mode),
      __API_URL__: JSON.stringify('http://127.0.0.1:8000'),
      __PWA_ENABLED__: JSON.stringify(env.VITE_PWA_ENABLED === 'true'),
      __DEBUG_MODE__: JSON.stringify(env.VITE_DEBUG_MODE === 'true')
    }
  }
})