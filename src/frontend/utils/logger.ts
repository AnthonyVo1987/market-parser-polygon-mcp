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

export interface ConsoleLogEntry {
  timestamp: Date;
  level: 'log' | 'debug' | 'info' | 'warn' | 'error';
  message: string;
  args: string[];
  source: string;
}

export interface FileLogServiceConfig {
  bufferSize: number;
  flushIntervalMs: number;
  apiEndpoint: string;
  enabled: boolean;
}

// FileLogService class for managing console log file operations
class FileLogService {
  private config: FileLogServiceConfig;
  private buffer: ConsoleLogEntry[] = [];
  private flushTimer: number | null = null;
  private isFlushingActive: boolean = false;
  private totalEntries: number = 0;
  private bufferWrapped: boolean = false;
  private wrapCount: number = 0;

  constructor(config: FileLogServiceConfig) {
    this.config = config;
    this.startPeriodicFlush();
  }

  /**
   * Add a log entry to the circular buffer
   */
  addEntry(entry: ConsoleLogEntry): void {
    if (!this.config.enabled) return;

    try {
      // Add to circular buffer
      if (this.buffer.length >= this.config.bufferSize) {
        // Buffer is full, start overwriting oldest entries
        const index = this.totalEntries % this.config.bufferSize;
        this.buffer[index] = entry;

        if (!this.bufferWrapped) {
          this.bufferWrapped = true;
          this.wrapCount = 1;
        } else {
          this.wrapCount++;
        }
      } else {
        this.buffer.push(entry);
      }

      this.totalEntries++;
    } catch (error) {
      console.error('Failed to add entry to log buffer:', error);
    }
  }

  /**
   * Flush buffer to file via API
   */
  async flush(): Promise<void> {
    if (!this.config.enabled || this.isFlushingActive || this.buffer.length === 0) {
      return;
    }

    this.isFlushingActive = true;

    try {
      // Create a copy of buffer for flushing
      const entriesToFlush = [...this.buffer];

      // Add wrap indicator if buffer has wrapped
      if (this.bufferWrapped) {
        const wrapIndicator: ConsoleLogEntry = {
          timestamp: new Date(),
          level: 'info',
          message: `🔄 Buffer wrapped ${this.wrapCount} time(s). Total entries processed: ${this.totalEntries}`,
          args: [`wrapCount:${this.wrapCount}`, `totalEntries:${this.totalEntries}`],
          source: 'fileLogService'
        };
        entriesToFlush.unshift(wrapIndicator);
      }

      const response = await fetch(this.config.apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          entries: entriesToFlush.map(entry => ({
            timestamp: entry.timestamp.toISOString(),
            level: entry.level,
            message: entry.message,
            args: entry.args,
            source: entry.source
          }))
        })
      });

      if (response.ok) {
        // Clear buffer after successful flush
        this.buffer = [];
        this.bufferWrapped = false;
        this.wrapCount = 0;
      } else {
        console.error('Failed to flush log buffer:', response.statusText);
      }
    } catch (error) {
      console.error('Error flushing log buffer:', error);
    } finally {
      this.isFlushingActive = false;
    }
  }

  /**
   * Start periodic flushing
   */
  private startPeriodicFlush(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
    }

    this.flushTimer = window.setInterval(() => {
      this.flush();
    }, this.config.flushIntervalMs);
  }

  /**
   * Stop periodic flushing
   */
  stopPeriodicFlush(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
  }

  /**
   * Check if file logging is enabled
   */
  isEnabled(): boolean {
    return this.config.enabled;
  }

  /**
   * Get buffer status
   */
  getBufferStatus(): {
    size: number;
    capacity: number;
    totalEntries: number;
    wrapped: boolean;
    wrapCount: number;
  } {
    return {
      size: this.buffer.length,
      capacity: this.config.bufferSize,
      totalEntries: this.totalEntries,
      wrapped: this.bufferWrapped,
      wrapCount: this.wrapCount
    };
  }

  /**
   * Cleanup resources
   */
  destroy(): void {
    this.stopPeriodicFlush();
    // Final flush before destroy
    this.flush();
  }
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
  private fileLogService: FileLogService | null = null;
  private originalConsole: {
    log: typeof console.log;
    debug: typeof console.debug;
    info: typeof console.info;
    warn: typeof console.warn;
    error: typeof console.error;
  } | null = null;

  constructor() {
    this.isDevelopment = import.meta.env.DEV || import.meta.env.MODE === 'development';

    // Initialize log mode from localStorage, default to NONE
    const storedLogMode = localStorage.getItem('console_log_mode') as LogMode;
    this.logMode = ['DEBUG', 'PRODUCTION', 'NONE'].includes(storedLogMode) ? storedLogMode : 'NONE';

    this.isDebugMode = this.isDevelopment && (
      localStorage.getItem('debug_mode') === 'true' ||
      (window as Record<string, unknown>).__DEBUG_MODE__ === true ||
      this.logMode === 'DEBUG'
    );
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
    (window as Record<string, unknown>).__setLogMode = (mode: LogMode) => this.setLogMode(mode);
    (window as Record<string, unknown>).__getLogMode = () => this.getLogMode();

    // Initialize file logging service
    this.initializeFileLogging();

    if (this.isDevelopment) {
      this.info('🚀 Frontend logger initialized', {
        environment: import.meta.env.MODE,
        debugMode: this.isDebugMode,
        logMode: this.logMode,
        fileLogging: this.fileLogService?.isEnabled() || false,
        timestamp: new Date().toISOString()
      });
    }
  }

  /**
   * Initialize file logging service and console interception
   */
  private initializeFileLogging(): void {
    // Skip initialization entirely in NONE mode
    if (this.logMode === 'NONE') {
      if (this.isDevelopment) {
        console.info('📴 File logging disabled - NONE mode active');
      }
      return;
    }

    try {
      // Create file log service with configuration
      const config: FileLogServiceConfig = {
        bufferSize: 1000,
        flushIntervalMs: 10000, // 10 seconds
        apiEndpoint: '/api/v1/logs/console/write',
        enabled: this.isDevelopment
      };

      this.fileLogService = new FileLogService(config);

      // Clear log file on app startup
      this.clearLogFile();

      // Intercept console methods
      this.interceptConsole();

      if (this.isDevelopment) {
        this.debug('📝 File logging service initialized', {
          bufferSize: config.bufferSize,
          flushInterval: `${config.flushIntervalMs}ms`,
          enabled: config.enabled
        });
      }
    } catch (error) {
      this.error('Failed to initialize file logging service', { error });
    }
  }

  /**
   * Intercept console methods to capture logs
   */
  private interceptConsole(): void {
    // Skip console interception in NONE mode
    if (this.logMode === 'NONE' || !this.fileLogService || this.originalConsole) return;

    // Store original console methods
    this.originalConsole = {
      log: console.log.bind(console),
      debug: console.debug.bind(console),
      info: console.info.bind(console),
      warn: console.warn.bind(console),
      error: console.error.bind(console)
    };

    // Intercept console.log
    console.log = (...args: unknown[]) => {
      this.originalConsole!.log(...args);
      this.captureConsoleLog('log', args);
    };

    // Intercept console.debug
    console.debug = (...args: unknown[]) => {
      this.originalConsole!.debug(...args);
      this.captureConsoleLog('debug', args);
    };

    // Intercept console.info
    console.info = (...args: unknown[]) => {
      this.originalConsole!.info(...args);
      this.captureConsoleLog('info', args);
    };

    // Intercept console.warn
    console.warn = (...args: unknown[]) => {
      this.originalConsole!.warn(...args);
      this.captureConsoleLog('warn', args);
    };

    // Intercept console.error
    console.error = (...args: unknown[]) => {
      this.originalConsole!.error(...args);
      this.captureConsoleLog('error', args);
    };
  }

  /**
   * Capture console log for file writing
   */
  private captureConsoleLog(level: ConsoleLogEntry['level'], args: unknown[]): void {
    if (!this.fileLogService) return;

    try {
      const message = args.length > 0 ? String(args[0]) : '';
      const additionalArgs = args.slice(1).map(arg => {
        try {
          return typeof arg === 'object' ? JSON.stringify(arg) : String(arg);
        } catch {
          return String(arg);
        }
      });

      const entry: ConsoleLogEntry = {
        timestamp: new Date(),
        level,
        message,
        args: additionalArgs,
        source: 'frontend'
      };

      this.fileLogService.addEntry(entry);
    } catch (error) {
      // Use original console to avoid infinite recursion
      this.originalConsole?.error('Failed to capture console log:', error);
    }
  }

  /**
   * Clear the log file on startup
   */
  private async clearLogFile(): Promise<void> {
    try {
      const response = await fetch('/api/v1/logs/console', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        this.debug('🗑️ Console log file cleared on startup');
      }
    } catch (error) {
      this.warn('Failed to clear log file on startup', { error });
    }
  }

  /**
   * Set the current log mode (NONE, DEBUG or PRODUCTION)
   */
  setLogMode(mode: LogMode): void {
    if (!['DEBUG', 'PRODUCTION', 'NONE'].includes(mode)) {
      this.warn('Invalid log mode provided', { attemptedMode: mode, validModes: ['DEBUG', 'PRODUCTION', 'NONE'] });
      return;
    }

    const previousMode = this.logMode;
    this.logMode = mode;

    // Update isDebugMode based on new mode
    this.isDebugMode = this.isDevelopment && (
      localStorage.getItem('debug_mode') === 'true' ||
      (window as Record<string, unknown>).__DEBUG_MODE__ === true ||
      this.logMode === 'DEBUG'
    );

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
          this.error('Error notifying log mode change listener', { error, mode });
        }
      }
    });

    // Only log mode change if not transitioning to NONE mode
    if (mode !== 'NONE') {
      this.info(`🔄 Console log mode changed: ${previousMode} → ${mode}`, {
        previousMode,
        newMode: mode,
        isDebugMode: this.isDebugMode
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
    try {
      // Destroy file log service
      if (this.fileLogService) {
        this.fileLogService.destroy();
        this.fileLogService = null;
      }

      // Restore original console methods
      if (this.originalConsole) {
        console.log = this.originalConsole.log;
        console.debug = this.originalConsole.debug;
        console.info = this.originalConsole.info;
        console.warn = this.originalConsole.warn;
        console.error = this.originalConsole.error;
        this.originalConsole = null;
      }

      if (this.isDevelopment) {
        console.info('🧹 File logging services cleaned up - NONE mode active');
      }
    } catch (error) {
      console.error('Failed to cleanup file logging services:', error);
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
  apiRequest(method: string, url: string, data?: unknown): void {
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
  apiResponse(method: string, url: string, status: number, duration: number, data?: unknown): void {
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
  stateChange(componentName: string, stateName: string, oldValue: unknown, newValue: unknown): void {
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
    return now.toTimeString().slice(0, 8) + '.' + now.getMilliseconds().toString().padStart(3, '0');
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
  },
  mode: {
    set: logger.setLogMode.bind(logger),
    get: logger.getLogMode.bind(logger),
    onChange: logger.onLogModeChange.bind(logger)
  }
};

// Add debugging helpers to window in development
if (import.meta.env.DEV) {
  (window as Record<string, unknown>).__logger = logger;
  (window as Record<string, unknown>).__loggers = loggers;
}