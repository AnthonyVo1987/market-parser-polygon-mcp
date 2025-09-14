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
  readonly processingTime?: number;
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
  readonly processingTime?: number;
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

// Prompt template types for financial analysis buttons
export interface PromptTemplate {
  readonly id: string;
  readonly type: AnalysisType;
  readonly name: string;
  readonly description: string;
  readonly template: string;
  readonly icon: string;
  readonly requiresTicker: boolean;
  readonly followUpQuestions?: readonly string[];
}

export type AnalysisType =
  | 'snapshot'
  | 'support_resistance'
  | 'technical_analysis'
  | 'technical';

export interface PromptTemplateResponse {
  templates: readonly PromptTemplate[];
  success: boolean;
  error?: string;
}

export interface GeneratePromptRequest {
  templateId: string;
  ticker?: string;
  additionalContext?: Record<string, unknown>;
}

export interface GeneratePromptResponse {
  prompt: string;
  templateId: string;
  success: boolean;
  error?: string;
}

// Analysis button component props
export interface AnalysisButtonProps {
  template: PromptTemplate;
  onPromptGenerated: (prompt: string) => void;
  isLoading?: boolean;
  disabled?: boolean;
  className?: string;
}

export interface AnalysisButtonsProps {
  onPromptGenerated: (prompt: string) => void;
  currentTicker?: string;
  className?: string;
}

// Hook return types
export interface UsePromptAPIResult {
  templates: readonly PromptTemplate[];
  loading: boolean;
  error: string | null;
  generatePrompt: (templateId: string, ticker?: string) => Promise<string>;
  refreshTemplates: () => Promise<void>;
}

// API endpoints for prompt functionality
export const PROMPT_API_ENDPOINTS = {
  TEMPLATES: '/templates',
  GENERATE: '/api/v1/prompts/generate',
  ANALYSIS_CHAT: '/api/v1/analysis/chat',
} as const;

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

export const isValidAnalysisType = (type: string): type is AnalysisType => {
  return [
    'snapshot',
    'support_resistance',
    'technical_analysis',
    'technical',
  ].includes(type);
};

export const isValidPromptTemplate = (
  template: unknown
): template is PromptTemplate => {
  return (
    typeof template === 'object' &&
    template !== null &&
    'id' in template &&
    'type' in template &&
    'name' in template &&
    'template' in template &&
    'icon' in template &&
    'requiresTicker' in template &&
    typeof (template as PromptTemplate).id === 'string' &&
    typeof (template as PromptTemplate).name === 'string' &&
    typeof (template as PromptTemplate).template === 'string' &&
    typeof (template as PromptTemplate).icon === 'string' &&
    typeof (template as PromptTemplate).requiresTicker === 'boolean' &&
    isValidAnalysisType((template as PromptTemplate).type)
  );
};
