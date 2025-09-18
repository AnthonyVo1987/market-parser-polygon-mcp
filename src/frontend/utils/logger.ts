/**
 * Minimal Frontend Logger - Performance Optimized
 * Simplified logging with LOG_MODE=NONE support only, no console interception
 */

// Types
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';
export type LogMode = 'DEBUG' | 'PRODUCTION' | 'NONE';

export interface LogContext {
  [key: string]: unknown;
}

/**
 * Minimal logger that respects LOG_MODE without performance overhead
 */
class Logger {
  private logMode: LogMode;
  private isDevelopment: boolean;

  constructor() {
    this.isDevelopment = import.meta.env.DEV || import.meta.env.MODE === 'development';

    // Initialize log mode from environment, default to NONE
    const storedLogMode = localStorage.getItem('console_log_mode') as LogMode;
    this.logMode = ['DEBUG', 'PRODUCTION', 'NONE'].includes(storedLogMode) ? storedLogMode : 'NONE';
  }

  /**
   * Log debug messages (only in debug mode)
   */
  debug(message: string, context?: LogContext): void {
    // No-op for performance optimization
  }

  /**
   * Log info messages
   */
  info(message: string, context?: LogContext): void {
    // No-op for performance optimization
  }

  /**
   * Log warning messages
   */
  warn(message: string, context?: LogContext): void {
    // No-op for performance optimization
  }

  /**
   * Log error messages (always logged unless NONE mode)
   */
  error(message: string, context?: LogContext): void {
    // No-op for performance optimization
  }

  /**
   * Set the current log mode
   */
  setLogMode(mode: LogMode): void {
    if (!['DEBUG', 'PRODUCTION', 'NONE'].includes(mode)) {
      return;
    }

    this.logMode = mode;
    localStorage.setItem('console_log_mode', mode);
  }

  /**
   * Get the current log mode
   */
  getLogMode(): LogMode {
    return this.logMode;
  }

  /**
   * Start a console group (no-op for minimal logger)
   */
  group(groupName: string, _collapsed: boolean = false): void {
    // No-op for performance optimization
  }

  /**
   * End the current console group (no-op for minimal logger)
   */
  groupEnd(): void {
    // No-op for performance optimization
  }

  /**
   * Log component lifecycle events (no-op for minimal logger)
   */
  componentLifecycle(componentName: string, event: 'mount' | 'unmount' | 'update', details?: LogContext): void {
    if (this.shouldLog('debug')) {
      this.debug(`Component ${event}: ${componentName}`, details);
    }
  }

  /**
   * Log state changes (no-op for minimal logger)
   */
  stateChange(componentName: string, stateName: string, oldValue: unknown, newValue: unknown): void {
    if (this.shouldLog('debug')) {
      this.debug(`State change in ${componentName}`, { state: stateName, oldValue, newValue });
    }
  }

  /**
   * Log user interactions (no-op for minimal logger)
   */
  userInteraction(action: string, element: string, details?: LogContext): void {
    if (this.shouldLog('info')) {
      this.info(`User ${action}: ${element}`, details);
    }
  }

  /**
   * Start performance timing (no-op for minimal logger)
   */
  startTiming(_name: string): void {
    // No-op for performance
  }

  /**
   * End performance timing (no-op for minimal logger)
   */
  endTiming(_name: string): number | null {
    // No-op for performance
    return null;
  }

  /**
   * Log API request (no-op for minimal logger)
   */
  apiRequest(method: string, url: string, data?: unknown): void {
    if (this.shouldLog('debug')) {
      this.debug(`API Request: ${method.toUpperCase()} ${url}`, { hasData: !!data });
    }
  }

  /**
   * Log API response (no-op for minimal logger)
   */
  apiResponse(method: string, url: string, status: number, duration: number, _data?: unknown): void {
    const level = status < 300 ? 'info' : status < 400 ? 'warn' : 'error';
    if (this.shouldLog(level)) {
      this[level](`API Response: ${method.toUpperCase()} ${url} - ${status}`, { duration: `${duration}ms` });
    }
  }

  /**
   * Add a listener for log mode changes (no-op for minimal logger)
   */
  onLogModeChange(_listener: (mode: LogMode) => void): () => void {
    // No-op for minimal logger - return empty unsubscribe function
    return () => {};
  }

  /**
   * Check if we should log at this level
   */
  private shouldLog(level: LogLevel): boolean {
    // In NONE mode, disable all logging
    if (this.logMode === 'NONE') return false;

    // Always log errors and warnings
    if (level === 'error' || level === 'warn') return true;

    // In PRODUCTION mode, only log warnings and errors
    if (this.logMode === 'PRODUCTION') {
      return false;
    }

    // In DEBUG mode, log everything in development
    if (this.logMode === 'DEBUG') {
      return this.isDevelopment;
    }

    return false;
  }
}

// Create and export singleton logger instance
export const logger = new Logger();

// Export multiple instances for different contexts (all use same minimal logger)
export const loggers = {
  frontend: logger,
  component: logger,
  api: logger,
  performance: logger,
  user: logger
};