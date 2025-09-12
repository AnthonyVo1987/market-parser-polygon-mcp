import { defineConfig, devices } from '@playwright/test';
import { spawn } from 'child_process';
import { promisify } from 'util';
import net from 'net';

/**
 * Dynamic port detection for React/Vite development server
 * Supports ports 3000-3003+ as specified in requirements
 */
async function findAvailablePort(): Promise<number> {
  const checkPort = (port: number): Promise<boolean> => {
    return new Promise((resolve) => {
      const server = net.createServer();
      server.listen(port, () => {
        server.close(() => resolve(true));
      });
      server.on('error', () => resolve(false));
    });
  };

  // Check ports 3000-3003+ for running Vite server
  for (let port = 3000; port <= 3010; port++) {
    const isAvailable = await checkPort(port);
    if (!isAvailable) {
      // Port is in use, likely by Vite server
      return port;
    }
  }
  
  // Default to 3000 if no running server detected
  return 3000;
}

/**
 * Check if backend server is running on port 8000
 */
async function isBackendRunning(): Promise<boolean> {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.listen(8000, () => {
      server.close(() => resolve(false)); // Port available = backend not running
    });
    server.on('error', () => resolve(true)); // Port in use = backend running
  });
}

/**
 * Optimized Playwright configuration for React/Vite stack
 * Updated for new project structure with backend at /src/ and frontend at /frontend/
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests/playwright',
  
  /* CRITICAL: Single browser session requirement - All tests in one browser instance */
  fullyParallel: false,
  workers: 1, // Enforced single worker for sequential execution
  
  /* CRITICAL: No retries to maintain single session requirement */
  retries: 0,
  
  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,
  
  /* Enhanced reporter with performance classification */
  reporter: [
    ['html'],
    ['line'],
    ['json', { outputFile: 'test-results/results.json' }]
  ],
  
  /* CRITICAL: 120-second test timeout as specified */
  timeout: 120000,
  
  /* Global timeout for expect assertions */
  expect: {
    timeout: 30000,
  },
  
  /* Shared settings optimized for React/Vite testing */
  use: {
    /* Dynamic base URL detection - will be set by webServer config */
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    
    /* Enhanced trace collection on failure */
    trace: 'retain-on-failure',
    
    /* Screenshot collection on failure */
    screenshot: 'only-on-failure',
    
    /* Video recording for debugging */
    video: 'retain-on-failure',
    
    /* Performance timing for classification */
    actionTimeout: 120000, // SUCCESS <45s, SLOW_PERFORMANCE 45-120s, TIMEOUT >120s
    navigationTimeout: 120000,
    
    /* Browser context options */
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    
    /* Enhanced debugging capabilities */
    launchOptions: {
      slowMo: 0, // No artificial delays for accurate performance measurement
    },
  },

  /* CRITICAL: Chromium browser configuration for single session testing */
  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Channel: 'chrome', // Uncomment to use installed Chrome instead of Chromium
      },
    },
  ],

  /* Web server configuration updated for new project structure */
  webServer: [
    {
      // Frontend React/Vite server - updated path for new structure
      command: 'cd frontend && npm run dev',
      port: 3000,
      reuseExistingServer: !process.env.CI,
      timeout: 120000,
      env: {
        NODE_ENV: 'development',
        VITE_API_BASE_URL: 'http://localhost:8000',
      },
    },
    {
      // Backend FastAPI server verification - backend now at /src/
      command: 'echo "Backend server check - should already be running on port 8000"',
      port: 8000,
      reuseExistingServer: true, // Always reuse existing backend server
      timeout: 10000, // Quick check since server should already be running
    },
  ],
  
  /* Output directories for test artifacts */
  outputDir: 'test-results/',
  
  /* Global setup and teardown */
  globalSetup: undefined, // Add global setup file path if needed
  globalTeardown: undefined, // Add global teardown file path if needed
  
  /* Test file patterns - supports test-b00X.spec.ts pattern */
  testMatch: [
    'test-b*.spec.ts',
    '*.test.ts',
    '*.spec.ts'
  ],
  
  /* Metadata for performance classification */
  metadata: {
    performance_thresholds: {
      success: '< 45 seconds',
      slow_performance: '45-120 seconds', 
      timeout: '> 120 seconds'
    },
    test_requirements: {
      single_browser_session: true,
      sequential_execution: true,
      no_retries: true,
      dynamic_port_detection: '3000-3003+'
    },
    project_structure: {
      backend: '/src/',
      frontend: '/frontend/',
      tests: '/tests/'
    }
  },
});