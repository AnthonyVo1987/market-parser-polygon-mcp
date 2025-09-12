// Error boundary and error handling types

import { ErrorInfo } from './chat_OpenAI';

// Enhanced error boundary component props
export interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<ErrorFallbackProps>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

// Error fallback component props
export interface ErrorFallbackProps {
  error: Error;
  errorInfo?: ErrorInfo;
  resetError?: () => void;
}

// Application error types
export type AppErrorType =
  | 'network'
  | 'validation'
  | 'server'
  | 'timeout'
  | 'unknown';

export interface AppError extends Error {
  type: AppErrorType;
  code?: string;
  statusCode?: number;
  timestamp: Date;
  context?: Record<string, unknown>;
  cause?: Error;
}

// Error factory functions
export const createAppError = (
  message: string,
  type: AppErrorType,
  options?: {
    code?: string;
    statusCode?: number;
    context?: Record<string, unknown>;
    cause?: Error;
  }
): AppError => {
  const error = new Error(message) as AppError;
  error.type = type;
  error.code = options?.code;
  error.statusCode = options?.statusCode;
  error.timestamp = new Date();
  error.context = options?.context;

  if (options?.cause) {
    error.cause = options.cause;
  }

  return error;
};

// Type guards for error handling
export const isAppError = (error: unknown): error is AppError => {
  return error instanceof Error && 'type' in error;
};

export const isNetworkError = (error: unknown): boolean => {
  return isAppError(error) && error.type === 'network';
};

export const isValidationError = (error: unknown): boolean => {
  return isAppError(error) && error.type === 'validation';
};

// Error severity levels
export type ErrorSeverity = 'low' | 'medium' | 'high' | 'critical';

export interface ErrorReport {
  error: AppError;
  severity: ErrorSeverity;
  userAgent: string;
  url: string;
  timestamp: Date;
  userId?: string;
  sessionId?: string;
}
