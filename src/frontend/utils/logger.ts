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

import { isDebugMode, isDevelopment } from '../config/config.loader';

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';
export type LogMode = 'DEBUG' | 'PRODUCTION' | 'NONE';

export interface LogContext {
  [key: string]: unknown;
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
  private logMode: LogMode;
  private performanceMetrics: Map<string, PerformanceMetric>;
  private logBuffer: Array<{
    timestamp: string;
    level: LogLevel;
    message: string;
    context?: LogContext;
  }>;
  private maxBufferSize: number = 100;
  private logModeChangeListeners: Array<(mode: LogMode) => void> = [];

  // File logging properties

  constructor() {
    this.isDevelopment = isDevelopment();

    // Initialize log mode from localStorage, default to NONE
    const storedLogMode = localStorage.getItem('console_log_mode') as LogMode;
    this.logMode = ['DEBUG', 'PRODUCTION', 'NONE'].includes(storedLogMode)
      ? storedLogMode
      : 'NONE';

    this.isDebugMode =
      this.isDevelopment &&
      (localStorage.getItem('debug_mode') === 'true' ||
        (window as Record<string, unknown>).__DEBUG_MODE__ === true ||
        this.logMode === 'DEBUG');
    this.performanceMetrics = new Map();
    this.logBuffer = [];

    // Enable global debug mode control
    (window as Record<string, unknown>).__enableDebugMode = () => {
      localStorage.setItem('debug_mode', 'true');
      this.isDebugMode = true;
      this.info('🔧 Debug mode enabled - verbose logging active');
    };

    (window as Record<string, unknown>).__disableDebugMode = () => {
      localStorage.setItem('debug_mode', 'false');
      this.isDebugMode = false;
      this.info('🔇 Debug mode disabled - minimal logging active');
    };

    (window as Record<string, unknown>).__exportLogs = () => this.exportLogs();

    // Add global log mode control methods
    (window as Record<string, unknown>).__setLogMode = (mode: LogMode) =>
      this.setLogMode(mode);
    (window as Record<string, unknown>).__getLogMode = () => this.getLogMode();

    // Initialize file logging service
    this.initializeFileLogging();

    if (this.isDevelopment) {
      this.info('🚀 Frontend logger initialized', {
        environment: isDevelopment() ? 'development' : 'production',
        debugMode: this.isDebugMode,
        logMode: this.logMode,
        timestamp: new Date().toISOString(),
      });
    }
  }

  /**
   * Initialize file logging service and console interception
   */
  private initializeFileLogging(): void {
    // File logging has been removed - this method is now a no-op
    // LOG_MODE=NONE provides native console performance
    if (this.isDevelopment) {
      // eslint-disable-next-line no-console
      console.info(
        '📴 File logging disabled - native console performance active'
      );
    }
  }

  /**
   * Intercept console methods to capture logs
   */

  /**
   * Capture console log for file writing
   */

  /**
   * Clear the log file on startup
   */

  /**
   * Set the current log mode (NONE, DEBUG or PRODUCTION)
   */
  setLogMode(mode: LogMode): void {
    if (!['DEBUG', 'PRODUCTION', 'NONE'].includes(mode)) {
      this.warn('Invalid log mode provided', {
        attemptedMode: mode,
        validModes: ['DEBUG', 'PRODUCTION', 'NONE'],
      });
      return;
    }

    const previousMode = this.logMode;
    this.logMode = mode;

    // Update isDebugMode based on new mode
    this.isDebugMode =
      this.isDevelopment &&
      (localStorage.getItem('debug_mode') === 'true' ||
        (window as Record<string, unknown>).__DEBUG_MODE__ === true ||
        this.logMode === 'DEBUG');

    // Persist to localStorage
    localStorage.setItem('console_log_mode', mode);

    // Handle mode transition logic
    this.handleModeTransition(previousMode, mode);

    // Notify listeners of mode change
    this.logModeChangeListeners.forEach(listener => {
      try {
        listener(mode);
      } catch (error) {
        // Only log error if not transitioning to NONE mode
        if (mode !== 'NONE') {
          this.error('Error notifying log mode change listener', {
            error,
            mode,
          });
        }
      }
    });

    // Only log mode change if not transitioning to NONE mode
    if (mode !== 'NONE') {
      this.info(`🔄 Console log mode changed: ${previousMode} → ${mode}`, {
        previousMode,
        newMode: mode,
        isDebugMode: this.isDebugMode,
      });
    }
  }

  /**
   * Get the current log mode
   */
  getLogMode(): LogMode {
    return this.logMode;
  }

  /**
   * Handle mode transition logic for proper initialization/cleanup
   */
  private handleModeTransition(previousMode: LogMode, newMode: LogMode): void {
    // Transitioning FROM NONE mode - need to initialize services
    if (previousMode === 'NONE' && newMode !== 'NONE') {
      this.initializeFileLogging();
    }

    // Transitioning TO NONE mode - need to cleanup services
    if (previousMode !== 'NONE' && newMode === 'NONE') {
      this.cleanupFileLogging();
    }
  }

  /**
   * Cleanup file logging services
   */
  private cleanupFileLogging(): void {
    // File logging has been removed - this method is now a no-op
    // No cleanup needed as console methods are no longer intercepted
    if (this.isDevelopment) {
      // eslint-disable-next-line no-console
      console.info(
        '🧹 File logging cleanup complete - native console performance maintained'
      );
    }
  }

  /**
   * Add a listener for log mode changes
   */
  onLogModeChange(listener: (mode: LogMode) => void): () => void {
    this.logModeChangeListeners.push(listener);

    // Return unsubscribe function
    return () => {
      const index = this.logModeChangeListeners.indexOf(listener);
      if (index > -1) {
        this.logModeChangeListeners.splice(index, 1);
      }
    };
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
    // eslint-disable-next-line no-console
    console[method](`📁 ${timestamp} ${groupName}`);
  }

  /**
   * End the current console group
   */
  groupEnd(): void {
    if (!this.shouldLog('info')) return;
    // eslint-disable-next-line no-console
    console.groupEnd();
  }

  /**
   * Start performance timing for an operation
   */
  startTiming(name: string): void {
    if (!this.isDebugMode) return;

    const metric: PerformanceMetric = {
      name,
      startTime: performance.now(),
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
      endTime: metric.endTime,
    });

    this.performanceMetrics.delete(name);
    return metric.duration;
  }

  /**
   * Log API call with request details
   */
  apiRequest(method: string, url: string, data?: unknown): void {
    this.group(`🌐 API Request: ${method.toUpperCase()} ${url}`, true);
    this.info('Request started', {
      method: method.toUpperCase(),
      url,
      timestamp: new Date().toISOString(),
      hasData: !!data,
    });
    if (data && this.isDebugMode) {
      this.debug('Request data', { data });
    }
    this.groupEnd();
  }

  /**
   * Log API response with status and timing
   */
  apiResponse(
    method: string,
    url: string,
    status: number,
    duration: number,
    data?: unknown
  ): void {
    const emoji = status < 300 ? '✅' : status < 400 ? '⚠️' : '❌';
    const level = status < 300 ? 'info' : status < 400 ? 'warn' : 'error';

    this.group(`${emoji} API Response: ${method.toUpperCase()} ${url}`, true);
    this[level]('Response received', {
      method: method.toUpperCase(),
      url,
      status,
      duration: `${duration.toFixed(2)}ms`,
      timestamp: new Date().toISOString(),
    });
    if (data && this.isDebugMode) {
      this.debug('Response data', { data });
    }
    this.groupEnd();
  }

  /**
   * Log React component lifecycle events
   */
  componentLifecycle(
    componentName: string,
    event: 'mount' | 'unmount' | 'update',
    details?: LogContext
  ): void {
    const emoji = event === 'mount' ? '🎭' : event === 'unmount' ? '💀' : '🔄';
    this.debug(`${emoji} Component ${event}: ${componentName}`, {
      component: componentName,
      event,
      timestamp: new Date().toISOString(),
      ...details,
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
      ...details,
    });
  }

  /**
   * Log state changes (use carefully to avoid render loops)
   */
  stateChange(
    componentName: string,
    stateName: string,
    oldValue: unknown,
    newValue: unknown
  ): void {
    this.debug(`🔄 State change in ${componentName}`, {
      component: componentName,
      state: stateName,
      oldValue,
      newValue,
      changed: !this.deepEqual(oldValue, newValue),
      timestamp: new Date().toISOString(),
    });
  }

  /**
   * Export logs as downloadable file
   */
  exportLogs(): void {
    const logs = {
      exported_at: new Date().toISOString(),
      environment: isDevelopment() ? 'development' : 'production',
      debug_mode: this.isDebugMode,
      buffer: this.logBuffer,
      performance_metrics: Array.from(this.performanceMetrics.entries()),
    };

    const blob = new Blob([JSON.stringify(logs, null, 2)], {
      type: 'application/json',
    });
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
  private log(
    level: LogLevel,
    message: string,
    context?: LogContext,
    emoji?: string,
    style?: string
  ): void {
    if (!this.shouldLog(level)) return;

    const timestamp = this.getTimestamp();
    const prefix = emoji ? `${emoji} ${timestamp}` : timestamp;
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context,
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

    // eslint-disable-next-line no-console
    console[level](...args);
  }

  /**
   * Check if we should log at this level
   */
  private shouldLog(level: LogLevel): boolean {
    // In NONE mode, disable all logging
    if (this.logMode === 'NONE') return false;

    // Always log errors
    if (level === 'error') return true;

    // Always log warnings
    if (level === 'warn') return true;

    // In PRODUCTION mode, only log warnings and errors
    if (this.logMode === 'PRODUCTION') {
      return level === 'warn' || level === 'error';
    }

    // In DEBUG mode, respect the development environment settings
    if (!this.isDevelopment && level !== 'warn') return false;
    if (level === 'debug' && !this.isDebugMode) return false;

    return true;
  }

  /**
   * Get formatted timestamp
   */
  private getTimestamp(): string {
    const now = new Date();
    return (
      now.toTimeString().slice(0, 8) +
      '.' +
      now.getMilliseconds().toString().padStart(3, '0')
    );
  }

  /**
   * Deep equality check for state change detection
   */
  private deepEqual(a: unknown, b: unknown): boolean {
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
    response: logger.apiResponse.bind(logger),
  },
  component: {
    lifecycle: logger.componentLifecycle.bind(logger),
    stateChange: logger.stateChange.bind(logger),
  },
  user: {
    interaction: logger.userInteraction.bind(logger),
  },
  performance: {
    start: logger.startTiming.bind(logger),
    end: logger.endTiming.bind(logger),
  },
  mode: {
    set: logger.setLogMode.bind(logger),
    get: logger.getLogMode.bind(logger),
    onChange: logger.onLogModeChange.bind(logger),
  },
};

// Add debugging helpers to window in development
if (isDebugMode()) {
  (window as Record<string, unknown>).__logger = logger;
  (window as Record<string, unknown>).__loggers = loggers;
}
