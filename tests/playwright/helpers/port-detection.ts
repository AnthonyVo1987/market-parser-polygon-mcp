/**
 * Port Detection Utilities for Playwright CLI Tests
 * 
 * Implements dynamic port discovery and server health validation
 * Supports frontend ports (3000-3003+) and backend verification (port 8000)
 * 
 * @fileoverview Port detection and server readiness validation utilities
 */

import * as net from 'net';
import { Page } from '@playwright/test';

/**
 * Server status interface
 */
export interface ServerStatus {
  port: number;
  running: boolean;
  accessible: boolean;
  responseTime?: number;
  error?: string;
  serverType?: 'frontend' | 'backend' | 'unknown';
}

/**
 * Port detection configuration
 */
export interface PortDetectionConfig {
  frontendPortRange: { start: number; end: number };
  backendPort: number;
  timeoutMs: number;
  healthCheckPath?: string;
  retryAttempts: number;
  retryDelayMs: number;
}

/**
 * Default port detection configuration
 */
export const DEFAULT_PORT_CONFIG: PortDetectionConfig = {
  frontendPortRange: { start: 3000, end: 3010 }, // Support 3000-3003+ as specified
  backendPort: 8000,
  timeoutMs: 10000,
  healthCheckPath: '/',
  retryAttempts: 3,
  retryDelayMs: 2000,
};

/**
 * Check if a specific port is in use
 * 
 * @param port - Port number to check
 * @param timeoutMs - Timeout for the check (default: 5000ms)
 * @returns Promise<boolean> - True if port is in use
 */
export async function isPortInUse(port: number, timeoutMs: number = 5000): Promise<boolean> {
  return new Promise((resolve) => {
    const server = net.createServer();
    
    const timeout = setTimeout(() => {
      server.close();
      resolve(false); // Timeout means we can't determine - assume not in use
    }, timeoutMs);
    
    server.listen(port, () => {
      clearTimeout(timeout);
      server.close(() => resolve(false)); // Port is available
    });
    
    server.on('error', () => {
      clearTimeout(timeout);
      resolve(true); // Port is in use
    });
  });
}

/**
 * Find running frontend server on dynamic ports (3000-3003+)
 * 
 * @param config - Port detection configuration
 * @returns Promise<ServerStatus | null> - Frontend server status or null if not found
 */
export async function findFrontendServer(
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<ServerStatus | null> {
  
  console.log(`[PORT-DETECTION] Scanning frontend ports ${config.frontendPortRange.start}-${config.frontendPortRange.end}`);
  
  for (let port = config.frontendPortRange.start; port <= config.frontendPortRange.end; port++) {
    try {
      const inUse = await isPortInUse(port, config.timeoutMs);
      
      if (inUse) {
        console.log(`[PORT-DETECTION] Found server on port ${port}, verifying accessibility...`);
        
        const serverStatus = await verifyServerAccessibility(port, config);
        
        if (serverStatus.accessible) {
          console.log(`[PORT-DETECTION] Frontend server confirmed on port ${port}`);
          return {
            ...serverStatus,
            serverType: 'frontend'
          };
        } else {
          console.log(`[PORT-DETECTION] Port ${port} in use but not accessible as web server`);
        }
      }
    } catch (error) {
      console.log(`[PORT-DETECTION] Error checking port ${port}:`, error);
    }
  }
  
  console.log(`[PORT-DETECTION] No accessible frontend server found in range ${config.frontendPortRange.start}-${config.frontendPortRange.end}`);
  return null;
}

/**
 * Verify backend server is running on port 8000
 * 
 * @param config - Port detection configuration
 * @returns Promise<ServerStatus> - Backend server status
 */
export async function verifyBackendServer(
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<ServerStatus> {
  
  console.log(`[PORT-DETECTION] Verifying backend server on port ${config.backendPort}`);
  
  const inUse = await isPortInUse(config.backendPort, config.timeoutMs);
  
  if (!inUse) {
    console.log(`[PORT-DETECTION] Backend port ${config.backendPort} is not in use`);
    return {
      port: config.backendPort,
      running: false,
      accessible: false,
      serverType: 'backend',
      error: 'Backend server not running'
    };
  }
  
  // Verify it's actually accessible as HTTP server
  const serverStatus = await verifyServerAccessibility(config.backendPort, config);
  
  console.log(`[PORT-DETECTION] Backend server status: running=${serverStatus.running}, accessible=${serverStatus.accessible}`);
  
  return {
    ...serverStatus,
    serverType: 'backend'
  };
}

/**
 * Verify server accessibility via HTTP request
 * 
 * @param port - Port to check
 * @param config - Port detection configuration
 * @returns Promise<ServerStatus> - Server accessibility status
 */
async function verifyServerAccessibility(
  port: number,
  config: PortDetectionConfig
): Promise<ServerStatus> {
  
  const startTime = Date.now();
  
  try {
    // Use fetch for HTTP health check
    const healthUrl = `http://localhost:${port}${config.healthCheckPath || '/'}`;
    
    console.log(`[PORT-DETECTION] Health check: ${healthUrl}`);
    
    const response = await fetch(healthUrl, {
      method: 'GET',
      signal: AbortSignal.timeout(config.timeoutMs)
    });
    
    const responseTime = Date.now() - startTime;
    
    // Accept any HTTP response (200, 404, etc.) as accessible
    const accessible = response.status >= 200 && response.status < 600;
    
    console.log(`[PORT-DETECTION] Health check response: ${response.status} (${responseTime}ms)`);
    
    return {
      port,
      running: true,
      accessible,
      responseTime
    };
    
  } catch (error) {
    const responseTime = Date.now() - startTime;
    
    console.log(`[PORT-DETECTION] Health check failed for port ${port}: ${error}`);
    
    return {
      port,
      running: true, // Port is in use, but not accessible via HTTP
      accessible: false,
      responseTime,
      error: String(error)
    };
  }
}

/**
 * Get complete system server status
 * 
 * @param config - Port detection configuration
 * @returns Promise<{frontend: ServerStatus | null, backend: ServerStatus}> - Complete server status
 */
export async function getSystemServerStatus(
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<{frontend: ServerStatus | null, backend: ServerStatus}> {
  
  console.log(`[PORT-DETECTION] Getting complete system server status...`);
  
  const [frontend, backend] = await Promise.all([
    findFrontendServer(config),
    verifyBackendServer(config)
  ]);
  
  console.log(`[PORT-DETECTION] System status - Frontend: ${frontend ? `port ${frontend.port}` : 'not found'}, Backend: ${backend.accessible ? 'accessible' : 'not accessible'}`);
  
  return { frontend, backend };
}

/**
 * Wait for server to become available with retry mechanism
 * 
 * @param port - Port to monitor
 * @param config - Port detection configuration
 * @returns Promise<ServerStatus> - Server status when available
 */
export async function waitForServerReady(
  port: number,
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<ServerStatus> {
  
  console.log(`[PORT-DETECTION] Waiting for server on port ${port} to become ready...`);
  
  for (let attempt = 1; attempt <= config.retryAttempts; attempt++) {
    console.log(`[PORT-DETECTION] Attempt ${attempt}/${config.retryAttempts} - Checking port ${port}`);
    
    try {
      const inUse = await isPortInUse(port, config.timeoutMs);
      
      if (inUse) {
        const serverStatus = await verifyServerAccessibility(port, config);
        
        if (serverStatus.accessible) {
          console.log(`[PORT-DETECTION] Server on port ${port} is ready (attempt ${attempt})`);
          return serverStatus;
        }
        
        console.log(`[PORT-DETECTION] Server on port ${port} running but not accessible yet`);
      } else {
        console.log(`[PORT-DETECTION] Port ${port} not in use yet`);
      }
      
    } catch (error) {
      console.log(`[PORT-DETECTION] Error on attempt ${attempt}:`, error);
    }
    
    if (attempt < config.retryAttempts) {
      console.log(`[PORT-DETECTION] Waiting ${config.retryDelayMs}ms before next attempt...`);
      await new Promise(resolve => setTimeout(resolve, config.retryDelayMs));
    }
  }
  
  console.log(`[PORT-DETECTION] Server on port ${port} not ready after ${config.retryAttempts} attempts`);
  
  return {
    port,
    running: false,
    accessible: false,
    error: `Server not ready after ${config.retryAttempts} attempts`
  };
}

/**
 * Auto-detect and navigate to available frontend server
 * 
 * @param page - Playwright page instance
 * @param config - Port detection configuration
 * @returns Promise<string> - URL of accessible frontend server
 */
export async function autoNavigateToFrontend(
  page: Page,
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<string> {
  
  console.log(`[PORT-DETECTION] Auto-detecting frontend server for navigation...`);
  
  // First try to find existing running server
  let frontendServer = await findFrontendServer(config);
  
  if (!frontendServer) {
    console.log(`[PORT-DETECTION] No running frontend found, waiting for server startup...`);
    
    // Wait for default port to become available
    const defaultPort = config.frontendPortRange.start;
    const serverStatus = await waitForServerReady(defaultPort, config);
    
    if (serverStatus.accessible) {
      frontendServer = serverStatus;
    } else {
      throw new Error(`Frontend server not available after waiting`);
    }
  }
  
  const frontendUrl = `http://localhost:${frontendServer.port}`;
  console.log(`[PORT-DETECTION] Navigating to frontend: ${frontendUrl}`);
  
  await page.goto(frontendUrl, { 
    waitUntil: 'networkidle',
    timeout: config.timeoutMs 
  });
  
  return frontendUrl;
}

/**
 * Validate system readiness for testing
 * 
 * @param config - Port detection configuration
 * @returns Promise<{ready: boolean, frontend?: ServerStatus, backend?: ServerStatus, errors: string[]}> - System readiness status
 */
export async function validateSystemReadiness(
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<{ready: boolean, frontend?: ServerStatus, backend?: ServerStatus, errors: string[]}> {
  
  console.log(`[PORT-DETECTION] Validating complete system readiness...`);
  
  const errors: string[] = [];
  const { frontend, backend } = await getSystemServerStatus(config);
  
  // Validate backend server
  if (!backend.accessible) {
    errors.push(`Backend server not accessible on port ${backend.port}: ${backend.error || 'Unknown error'}`);
  }
  
  // Validate frontend server
  if (!frontend) {
    errors.push(`No frontend server found in port range ${config.frontendPortRange.start}-${config.frontendPortRange.end}`);
  } else if (!frontend.accessible) {
    errors.push(`Frontend server on port ${frontend.port} not accessible: ${frontend.error || 'Unknown error'}`);
  }
  
  const ready = errors.length === 0;
  
  console.log(`[PORT-DETECTION] System readiness: ${ready ? 'READY' : 'NOT READY'}`);
  if (errors.length > 0) {
    console.log(`[PORT-DETECTION] Validation errors:`, errors);
  }
  
  return {
    ready,
    frontend: frontend || undefined,
    backend,
    errors
  };
}

/**
 * Get base URL for testing based on auto-detected frontend
 * 
 * @param config - Port detection configuration
 * @returns Promise<string> - Base URL for tests
 */
export async function getTestBaseUrl(
  config: PortDetectionConfig = DEFAULT_PORT_CONFIG
): Promise<string> {
  
  const frontendServer = await findFrontendServer(config);
  
  if (!frontendServer) {
    // Fallback to default port
    const defaultPort = config.frontendPortRange.start;
    console.log(`[PORT-DETECTION] No frontend detected, using default port ${defaultPort}`);
    return `http://localhost:${defaultPort}`;
  }
  
  const baseUrl = `http://localhost:${frontendServer.port}`;
  console.log(`[PORT-DETECTION] Test base URL: ${baseUrl}`);
  
  return baseUrl;
}