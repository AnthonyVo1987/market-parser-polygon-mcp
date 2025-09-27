// Core message interface with enhanced validation
export interface Message {
  readonly id: string;
  content: string;
  sender: MessageSender;
  timestamp: Date;
  metadata?: MessageMetadata;
}

// Enhanced sender type with strict validation
export type MessageSender = 'user' | 'ai';

// Optional metadata for messages
export interface MessageMetadata {
  readonly isError?: boolean;
  readonly tokenCount?: number;
  readonly model?: string;
}

// Enhanced API response interface
export interface ChatResponse {
  response: string;
  success: boolean;
  error?: string;
  metadata?: ResponseMetadata;
}

// Response metadata for tracking and analytics
export interface ResponseMetadata {
  readonly requestId?: string;
  readonly tokenCount?: number;
  readonly model?: string;
  readonly timestamp?: string;
}

// API Error interface with enhanced error details
export interface ApiError {
  error: string;
  code?: string;
  statusCode?: number;
  details?: Record<string, unknown>;
}


// Component prop interfaces for better type safety
export interface ChatInputProps {
  onSendMessage: (message: string) => void | Promise<void>;
  isLoading: boolean;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
}

export interface ChatMessageProps {
  message: Message;
  showCopyButton?: boolean;
  className?: string;
}

export interface ChatInterfaceState {
  messages: readonly Message[];
  isLoading: boolean;
  error: string | null;
  lastMessageId?: string;
}

// Error boundary types
export interface ErrorInfo {
  componentStack: string;
}

export interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

// Utility types for better type inference
export type MessageWithoutId = Omit<Message, 'id'>;
export type MessageUpdate = Partial<Pick<Message, 'content' | 'metadata'>>;
export type SendMessageFunction = (message: string) => Promise<void>;

// Event handler types
export type MessageEventHandler = (message: Message) => void;
export type ErrorEventHandler = (error: string | Error) => void;
export type LoadingStateHandler = (isLoading: boolean) => void;

// Constants for better maintainability
export const MESSAGE_CONSTRAINTS = {
  MIN_LENGTH: 1,
  MAX_LENGTH: 10000,
  MAX_MESSAGES: 1000,
} as const;

export const API_ENDPOINTS = {
  CHAT: '/chat',
  HEALTH: '/health',
} as const;

export const ERROR_CODES = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  TIMEOUT_ERROR: 'TIMEOUT_ERROR',
} as const;

export type ErrorCode = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];

// Export utility functions for type guards
export const isValidMessageSender = (
  sender: string
): sender is MessageSender => {
  return sender === 'user' || sender === 'ai';
};

export const isApiError = (error: unknown): error is ApiError => {
  return typeof error === 'object' && error !== null && 'error' in error;
};

export const isValidMessage = (message: unknown): message is Message => {
  return (
    typeof message === 'object' &&
    message !== null &&
    'id' in message &&
    'content' in message &&
    'sender' in message &&
    'timestamp' in message &&
    typeof (message as Message).id === 'string' &&
    typeof (message as Message).content === 'string' &&
    isValidMessageSender((message as Message).sender) &&
    (message as Message).timestamp instanceof Date
  );
};
