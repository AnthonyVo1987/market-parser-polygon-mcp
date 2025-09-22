import react from '@vitejs/plugin-react'
import browserslist from 'browserslist'
import { browserslistToTargets } from 'lightningcss'
import { visualizer } from 'rollup-plugin-visualizer'
import { defineConfig, loadEnv } from 'vite'
import { VitePWA } from 'vite-plugin-pwa'
import { config } from './src/frontend/config/config.loader'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load environment variables from root directory
  const env = loadEnv(mode, process.cwd(), '')

  // Environment detection
  const isProduction = mode === 'production'
  const isDevelopment = mode === 'development'
  const isBuild = command === 'build'

  // Lightning CSS browser targets
  const targets = browserslistToTargets(browserslist('>= 0.25%', 'not dead'))

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
              urlPattern: new RegExp(`^http://127\.0\.0\.1:8000\/chat$`),
              handler: 'NetworkOnly'
            },
            {
              urlPattern: new RegExp(`^http://127\.0\.0\.1:8000\/api\/v1\/prompts\/generate$`),
              handler: 'NetworkOnly'
            },
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
          enabled: config.frontend.features.pwa && isDevelopment,
          type: 'module'
        }
      }),
      // Bundle analysis - environment-aware configuration
      (env.ANALYZE || config.frontend.development.bundleAnalyzer) && visualizer({
        filename: 'dist/bundle-analysis.html',
        open: !isBuild, // Only auto-open in development
        gzipSize: true,
        brotliSize: true,
        template: 'treemap', // treemap, sunburst, network
        projectRoot: '.',
        title: `Bundle Analysis - ${mode.toUpperCase()}`,
        sourcemap: isProduction // Enable source map analysis in production
      })
    ].filter(Boolean),
    // Development server configuration (only applies in dev mode)
    server: {
      host: config.frontend.server.host,
      port: config.frontend.server.port,
      strictPort: true, // Fail if port is busy, no dynamic port allocation
      // Enable CORS for root-level development and cross-origin requests
      cors: true,
      // Phase 1: Server warmup optimization for faster cold starts
      warmup: {
        clientFiles: ['./src/frontend/main.tsx', './src/frontend/App.tsx']
      },
      // Phase 1: Static proxy configuration for backend integration
      proxy: {
        '/api': {
          target: `http://${config.backend.server.host}:${config.backend.server.port}`,
          changeOrigin: true,
          secure: false
        },
        '/chat': {
          target: `http://${config.backend.server.host}:${config.backend.server.port}`,
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
      sourcemap: isProduction ? 'hidden' : config.frontend.development.sourceMap, // Use config for source maps

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
    // CSS optimization with Lightning CSS
    css: {
      transformer: 'lightningcss',
      lightningcss: {
        targets,
        minify: isProduction,
        sourceMap: isProduction
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
      __APP_ENV__: JSON.stringify(config.frontend.features.appEnv),
      __API_URL__: JSON.stringify(`http://${config.backend.server.host}:${config.backend.server.port}`),
      __PWA_ENABLED__: JSON.stringify(config.frontend.features.pwa),
      __DEBUG_MODE__: JSON.stringify(config.frontend.features.debugMode)
    }
  }
})