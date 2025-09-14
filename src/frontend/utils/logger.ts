/**
 * Frontend logging utility for Market Parser React application.
 * 
 * Provides environment-aware logging with console organization, performance tracking,
 * and safe React integration patterns to prevent render loops.
 * 
 * Usage:
 *   import { logger } from '@/utils/logger';
 *   
 *   logger.info('Component mounted', { component: 'ChatInterface' });
 *   logger.debug('API call started', { endpoint: '/chat', method: 'POST' });
 *   logger.group('User Interaction');
 *   logger.info('Button clicked', { button: 'send' });
 *   logger.groupEnd();
 */

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface LogContext {
  [key: string]: any;
}

export interface PerformanceMetric {
  name: string;
  startTime: number;
  endTime?: number;
  duration?: number;
}

class FrontendLogger {
  private isDevelopment: boolean;
  private isDebugMode: boolean;
  private performanceMetrics: Map<string, PerformanceMetric>;
  private logBuffer: any[];
  private maxBufferSize: number = 100;

  constructor() {
    this.isDevelopment = import.meta.env.DEV || import.meta.env.MODE === 'development';
    this.isDebugMode = this.isDevelopment && (
      localStorage.getItem('debug_mode') === 'true' || 
      (window as any).__DEBUG_MODE__ === true
    );
    this.performanceMetrics = new Map();
    this.logBuffer = [];
    
    // Enable global debug mode control
    (window as any).__enableDebugMode = () => {
      localStorage.setItem('debug_mode', 'true');
      this.isDebugMode = true;
      this.info('🔧 Debug mode enabled - verbose logging active');
    };
    
    (window as any).__disableDebugMode = () => {
      localStorage.setItem('debug_mode', 'false');
      this.isDebugMode = false;
      this.info('🔇 Debug mode disabled - minimal logging active');
    };
    
    (window as any).__exportLogs = () => this.exportLogs();
    
    if (this.isDevelopment) {
      this.info('🚀 Frontend logger initialized', {
        environment: import.meta.env.MODE,
        debugMode: this.isDebugMode,
        timestamp: new Date().toISOString()
      });
    }
  }

  /**
   * Log debug messages (only in debug mode)
   */
  debug(message: string, context?: LogContext): void {
    if (!this.isDebugMode) return;
    
    this.log('debug', message, context, '🔍', 'color: #6B7280');
  }

  /**
   * Log info messages
   */
  info(message: string, context?: LogContext): void {
    if (!this.isDevelopment && !this.isDebugMode) return;
    
    this.log('info', message, context, 'ℹ️', 'color: #3B82F6');
  }

  /**
   * Log warning messages
   */
  warn(message: string, context?: LogContext): void {
    this.log('warn', message, context, '⚠️', 'color: #F59E0B');
  }

  /**
   * Log error messages (always logged)
   */
  error(message: string, context?: LogContext): void {
    this.log('error', message, context, '❌', 'color: #EF4444');
  }

  /**
   * Start a console group for organizing related logs
   */
  group(groupName: string, collapsed: boolean = false): void {
    if (!this.shouldLog('info')) return;
    
    const timestamp = this.getTimestamp();
    const method = collapsed ? 'groupCollapsed' : 'group';
    console[method](`📁 ${timestamp} ${groupName}`);
  }

  /**
   * End the current console group
   */
  groupEnd(): void {
    if (!this.shouldLog('info')) return;
    console.groupEnd();
  }

  /**
   * Start performance timing for an operation
   */
  startTiming(name: string): void {
    if (!this.isDebugMode) return;
    
    const metric: PerformanceMetric = {
      name,
      startTime: performance.now()
    };
    
    this.performanceMetrics.set(name, metric);
    this.debug(`⏱️ Started timing: ${name}`);
  }

  /**
   * End performance timing and log the duration
   */
  endTiming(name: string): number | null {
    if (!this.isDebugMode) return null;
    
    const metric = this.performanceMetrics.get(name);
    if (!metric) {
      this.warn(`⏱️ No timing started for: ${name}`);
      return null;
    }
    
    metric.endTime = performance.now();
    metric.duration = metric.endTime - metric.startTime;
    
    this.info(`⏱️ Timing complete: ${name}`, {
      duration: `${metric.duration.toFixed(2)}ms`,
      startTime: metric.startTime,
      endTime: metric.endTime
    });
    
    this.performanceMetrics.delete(name);
    return metric.duration;
  }

  /**
   * Log API call with request details
   */
  apiRequest(method: string, url: string, data?: any): void {
    this.group(`🌐 API Request: ${method.toUpperCase()} ${url}`, true);
    this.info('Request started', {
      method: method.toUpperCase(),
      url,
      timestamp: new Date().toISOString(),
      hasData: !!data
    });
    if (data && this.isDebugMode) {
      this.debug('Request data', { data });
    }
    this.groupEnd();
  }

  /**
   * Log API response with status and timing
   */
  apiResponse(method: string, url: string, status: number, duration: number, data?: any): void {
    const emoji = status < 300 ? '✅' : status < 400 ? '⚠️' : '❌';
    const level = status < 300 ? 'info' : status < 400 ? 'warn' : 'error';
    
    this.group(`${emoji} API Response: ${method.toUpperCase()} ${url}`, true);
    this[level]('Response received', {
      method: method.toUpperCase(),
      url,
      status,
      duration: `${duration.toFixed(2)}ms`,
      timestamp: new Date().toISOString()
    });
    if (data && this.isDebugMode) {
      this.debug('Response data', { data });
    }
    this.groupEnd();
  }

  /**
   * Log React component lifecycle events
   */
  componentLifecycle(componentName: string, event: 'mount' | 'unmount' | 'update', details?: LogContext): void {
    const emoji = event === 'mount' ? '🎭' : event === 'unmount' ? '💀' : '🔄';
    this.debug(`${emoji} Component ${event}: ${componentName}`, {
      component: componentName,
      event,
      timestamp: new Date().toISOString(),
      ...details
    });
  }

  /**
   * Log user interactions
   */
  userInteraction(action: string, element: string, details?: LogContext): void {
    this.info(`👤 User ${action}: ${element}`, {
      action,
      element,
      timestamp: new Date().toISOString(),
      ...details
    });
  }

  /**
   * Log state changes (use carefully to avoid render loops)
   */
  stateChange(componentName: string, stateName: string, oldValue: any, newValue: any): void {
    this.debug(`🔄 State change in ${componentName}`, {
      component: componentName,
      state: stateName,
      oldValue,
      newValue,
      changed: !this.deepEqual(oldValue, newValue),
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Export logs as downloadable file
   */
  exportLogs(): void {
    const logs = {
      exported_at: new Date().toISOString(),
      environment: import.meta.env.MODE,
      debug_mode: this.isDebugMode,
      buffer: this.logBuffer,
      performance_metrics: Array.from(this.performanceMetrics.entries())
    };
    
    const blob = new Blob([JSON.stringify(logs, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `frontend-logs-${new Date().toISOString().slice(0, 19)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    this.info('📁 Logs exported to file');
  }

  /**
   * Core logging method
   */
  private log(level: LogLevel, message: string, context?: LogContext, emoji?: string, style?: string): void {
    if (!this.shouldLog(level)) return;
    
    const timestamp = this.getTimestamp();
    const prefix = emoji ? `${emoji} ${timestamp}` : timestamp;
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context
    };
    
    // Add to buffer for export
    this.logBuffer.push(logEntry);
    if (this.logBuffer.length > this.maxBufferSize) {
      this.logBuffer.shift();
    }
    
    // Console output
    const args = [`${prefix} ${message}`];
    if (style) {
      args[0] = `%c${args[0]}`;
      args.splice(1, 0, style);
    }
    if (context) {
      args.push(context);
    }
    
    console[level](...args);
  }

  /**
   * Check if we should log at this level
   */
  private shouldLog(level: LogLevel): boolean {
    if (level === 'error') return true; // Always log errors
    if (!this.isDevelopment && level !== 'warn') return false; // Production: only warnings and errors
    if (level === 'debug' && !this.isDebugMode) return false; // Debug only in debug mode
    return true;
  }

  /**
   * Get formatted timestamp
   */
  private getTimestamp(): string {
    const now = new Date();
    return now.toTimeString().slice(0, 8) + '.' + now.getMilliseconds().toString().padStart(3, '0');
  }

  /**
   * Deep equality check for state change detection
   */
  private deepEqual(a: any, b: any): boolean {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (typeof a !== typeof b) return false;
    if (typeof a !== 'object') return false;
    
    const keysA = Object.keys(a);
    const keysB = Object.keys(b);
    if (keysA.length !== keysB.length) return false;
    
    for (const key of keysA) {
      if (!keysB.includes(key)) return false;
      if (!this.deepEqual(a[key], b[key])) return false;
    }
    
    return true;
  }
}

// Export singleton logger instance
export const logger = new FrontendLogger();

// Export utilities for React components
export const loggers = {
  api: {
    request: logger.apiRequest.bind(logger),
    response: logger.apiResponse.bind(logger)
  },
  component: {
    lifecycle: logger.componentLifecycle.bind(logger),
    stateChange: logger.stateChange.bind(logger)
  },
  user: {
    interaction: logger.userInteraction.bind(logger)
  },
  performance: {
    start: logger.startTiming.bind(logger),
    end: logger.endTiming.bind(logger)
  }
};

// Add debugging helpers to window in development
if (import.meta.env.DEV) {
  (window as any).__logger = logger;
  (window as any).__loggers = loggers;
}