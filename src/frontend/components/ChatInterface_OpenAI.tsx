import {
  memo,
  useCallback,
  useEffect,
  useMemo,
  useReducer,
  useRef,
} from 'react';
// Removed useDebouncedCallback import - implementing direct state updates for <16ms input responsiveness

import { sendChatMessage } from '../services/api_OpenAI';
import { Message } from '../types/chat_OpenAI';
import { usePerformanceMonitoring } from '../utils/performance';

// Consolidated state interface for useReducer
interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  inputValue: string;
}

// Action types for state management
type ChatAction =
  | { type: 'SEND_MESSAGE_START'; payload: { userMessage: Message } }
  | {
      type: 'SEND_MESSAGE_SUCCESS';
      payload: { aiMessage: Message };
    }
  | {
      type: 'SEND_MESSAGE_ERROR';
      payload: {
        errorMessage: string;
        aiMessage: Message;
      };
    }
  | { type: 'UPDATE_INPUT'; payload: string }
  | { type: 'CLEAR_ERROR' }
  | { type: 'RESET_STATE' };

// Initial state
const initialChatState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  inputValue: '',
};

// Reducer function for consolidated state management
function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case 'SEND_MESSAGE_START':
      return {
        ...state,
        isLoading: true,
        error: null,
        messages: [...state.messages, action.payload.userMessage],
      };
    case 'SEND_MESSAGE_SUCCESS':
      return {
        ...state,
        isLoading: false,
        messages: [...state.messages, action.payload.aiMessage],
        inputValue: '', // Clear input after successful message send
      };
    case 'SEND_MESSAGE_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload.errorMessage,
        messages: [...state.messages, action.payload.aiMessage],
      };
    case 'UPDATE_INPUT':
      return {
        ...state,
        inputValue: action.payload,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    case 'RESET_STATE':
      return initialChatState;
    default:
      return state;
  }
}

import ChatInput_OpenAI from './ChatInput_OpenAI';
import ChatMessage_OpenAI from './ChatMessage_OpenAI';
import CollapsiblePanel from './CollapsiblePanel';

// Lazy load secondary components removed - Export and Recent Message panels removed

// Note: Styles are now included within each lazy-loaded component to prevent static imports
// that would break the lazy loading optimization

const ChatInterface_OpenAI = memo(function ChatInterface_OpenAI() {
  // Consolidated state management using useReducer for performance optimization
  const [state, dispatch] = useReducer(chatReducer, initialChatState);
  const { messages, isLoading, error, inputValue} = state;

  // Optimize useMemo - Only memoize expensive calculations
  const placeholderText = useMemo(
    () => `Ask any financial question... (Shift+Enter for new line)`,
    []
  );

  // Performance and interaction tracking

  // Phase 4: Performance Monitoring
  const { metrics: performanceMetrics } = usePerformanceMonitoring();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const statusRegionRef = useRef<HTMLDivElement>(null);
  // ChatInputRef removed - using direct props instead
  const isFirstRenderRef = useRef(true);
  const previousMessageCountRef = useRef(0);

  // Optimized auto-scroll with minimal dependencies
  useEffect(() => {
    const currentMessageCount = messages.length;

    // Only scroll if messages increased and not loading
    const shouldScroll =
      !isFirstRenderRef.current &&
      currentMessageCount > previousMessageCountRef.current &&
      !isLoading;

    if (shouldScroll && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'auto' });
    }

    // Update refs
    isFirstRenderRef.current = false;
    previousMessageCountRef.current = currentMessageCount;
  }, [messages.length, isLoading]); // Include messages.length and isLoading dependencies

  // Direct input change handler for <16ms responsiveness - no debouncing
  // Note: Input handling is now managed by ChatInput component directly

  const handleSendMessage = useCallback(
    async (messageContent: string) => {
      const messageId = Date.now().toString();
      const userMessage: Message = {
        id: messageId,
        content: messageContent,
        sender: 'user',
        timestamp: new Date(),
      };

      // Start performance timing

      // Use optimized reducer action for immediate message start state
      dispatch({
        type: 'SEND_MESSAGE_START',
        payload: { userMessage },
      });

      try {
        // Send to API and get response
        const apiResponse = await sendChatMessage(messageContent);

        // Create AI message and dispatch success action
        const aiMessage: Message = {
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          content: apiResponse.response,
          sender: 'ai',
          timestamp: new Date(),
          metadata: apiResponse.metadata
            ? {
                tokenCount: apiResponse.metadata.tokenCount,
                inputTokens: apiResponse.metadata.inputTokens,
                outputTokens: apiResponse.metadata.outputTokens,
                model: apiResponse.metadata.model,
                processingTime: apiResponse.metadata.processingTime,
                requestId: apiResponse.metadata.requestId,
                timestamp: apiResponse.metadata.timestamp,
              }
            : undefined,
        };

        dispatch({
          type: 'SEND_MESSAGE_SUCCESS',
          payload: { aiMessage },
        });

        // End performance timing
      } catch (err: unknown) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to send message';

        // Create error AI message and dispatch error action
        const aiMessage: Message = {
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          content: `Error: ${errorMessage}`,
          sender: 'ai',
          timestamp: new Date(),
          metadata: { isError: true },
        };

        dispatch({
          type: 'SEND_MESSAGE_ERROR',
          payload: { errorMessage, aiMessage },
        });

        // End performance timing even on error
      }
    },
    []
  );

  // Removed handleRecentMessageClick and handleExport callbacks as they're now handled internally
  // Removed handleDebugAction as it's now handled internally by DebugPanel

  return (
    <div
      className='chat-interface'
      role='application'
      aria-label='OpenAI Chat Interface'
    >
      {/* Skip link for keyboard navigation */}
      <a href='#main-input' className='skip-link'>
        Skip to message input
      </a>

      {/* Live regions for screen reader announcements */}
      <div
        ref={statusRegionRef}
        role='status'
        aria-live='polite'
        aria-atomic='true'
        className='sr-only'
      >
        {isLoading ? 'Sending message, please wait...' : ''}
        {error ? `Error: ${error}` : ''}
      </div>

      {/* SIMPLIFIED LAYOUT: Fixed structure to prevent UI jumping */}
      <div className='chat-layout-container'>
        {/* Header - Fixed position */}
        <header className='chat-header' role='banner'>
          <h1 id='chat-title'>OpenAI Chat Interface</h1>
          {error && (
            <div
              className='error-banner'
              role='alert'
              aria-describedby='chat-title'
            >
              {error}
            </div>
          )}
        </header>

        {/* Messages Container - Flexible height */}
        <main
          className='messages-section'
          role='log'
          aria-live='polite'
          aria-label='Chat conversation'
        >
          {messages.length === 0 ? (
            <div className='empty-state' role='status'>
              <div className='welcome-content'>
                <h2 className='welcome-title'>
                  Welcome to Financial Analysis Chat
                </h2>
                <p className='welcome-description'>
                  Get instant financial insights powered by AI. Type your own
                  questions about stocks, market data, or financial analysis.
                </p>
                <p className='getting-started'>
                  Start by typing a message directly about any financial topic.
                </p>
              </div>
            </div>
          ) : (
            <>
              {messages.map(message => (
                <ChatMessage_OpenAI key={message.id} message={message} />
              ))}
              {/* Scroll anchor */}
              <div ref={messagesEndRef} aria-hidden='true' />
            </>
          )}
        </main>

        {/* Chat Input - Fixed position at bottom */}
        <section
          className='chat-input-section'
          role='complementary'
          aria-label='Message input'
        >
          <div className='chat-input-container'>
            <ChatInput_OpenAI
              onSendMessage={handleSendMessage}
              disabled={isLoading}
              placeholder={placeholderText}
              value={inputValue}
              onChange={value =>
                dispatch({ type: 'UPDATE_INPUT', payload: value })
              }
            />
          </div>
        </section>
      </div>

      {/* Loading overlay - Fixed positioning */}
      {isLoading && (
        <div
          className='message-sent-overlay'
          role='status'
          aria-label='Message sent, waiting for AI response'
        >
          <div className='message-sent-content'>
            <div className='message-sent-icon'>
              <svg
                viewBox='0 0 24 24'
                fill='none'
                xmlns='http://www.w3.org/2000/svg'
              >
                <path
                  d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
                  stroke='currentColor'
                  strokeWidth='2'
                  strokeLinecap='round'
                  strokeLinejoin='round'
                />
              </svg>
            </div>
            <div className='message-sent-text'>
              <h3>MESSAGE SENT</h3>
              <p>PLEASE WAIT FOR AI RESPONSE</p>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Control Panels - Consolidated System Status & Performance */}
      <div className='bottom-control-panels' role='complementary'>
        {/* Consolidated System Status & Performance Panel */}
        <CollapsiblePanel
          title='System Status & Performance'
          defaultExpanded={false}
          data-testid='status-performance-panel'
        >
          <div className='status-performance-grid'>
            {/* Status Section */}
            <div className='status-section-inline'>
              <div className='status-metric'>
                <span className='status-label'>Messages:</span>
                <span
                  className='status-value'
                  aria-label={`Total messages: ${messages.length}`}
                >
                  {messages.length}
                </span>
              </div>
              <div className='status-metric'>
                <span className='status-label'>Status:</span>
                <span
                  className={`status-value ${isLoading ? 'status--loading' : 'status--ready'}`}
                  aria-label={`Current status: ${isLoading ? 'Processing request' : 'Ready for input'}`}
                >
                  {isLoading ? 'Processing...' : 'Ready'}
                </span>
              </div>
            </div>

            {/* Performance Section */}
            <div className='performance-section-inline'>
              <div className='performance-metric'>
                <span className='metric-label'>FCP:</span>
                <span
                  className={
                    performanceMetrics.fcp && performanceMetrics.fcp < 1500
                      ? 'good'
                      : 'warning'
                  }
                >
                  {performanceMetrics.fcp
                    ? `${performanceMetrics.fcp.toFixed(0)}ms`
                    : 'Calculating...'}
                </span>
              </div>
              <div className='performance-metric'>
                <span className='metric-label'>LCP:</span>
                <span
                  className={
                    performanceMetrics.lcp && performanceMetrics.lcp < 2500
                      ? 'good'
                      : 'warning'
                  }
                >
                  {performanceMetrics.lcp
                    ? `${performanceMetrics.lcp.toFixed(0)}ms`
                    : 'Calculating...'}
                </span>
              </div>
              <div className='performance-metric'>
                <span className='metric-label'>CLS:</span>
                <span
                  className={
                    performanceMetrics.cls && performanceMetrics.cls < 0.1
                      ? 'good'
                      : 'warning'
                  }
                >
                  {performanceMetrics.cls
                    ? performanceMetrics.cls.toFixed(3)
                    : 'Calculating...'}
                </span>
              </div>
            </div>
          </div>
        </CollapsiblePanel>
      </div>
    </div>
  );
});

// Enable Why Did You Render tracking for this component
ChatInterface_OpenAI.whyDidYouRender = true;
ChatInterface_OpenAI.displayName = 'ChatInterface_OpenAI';

export default ChatInterface_OpenAI;

// Enhanced responsive styles for cross-platform UI optimization with accessibility
export const interfaceStyles = `
  /* Accessibility: Skip link for keyboard navigation */
  .skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    border-radius: 4px;
    z-index: 1000;
    font-size: 14px;
  }
  
  .skip-link:focus {
    top: 6px;
  }
  
  /* Screen reader only content */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  
  /* FIXED LAYOUT: Stable structure to prevent UI jumping */
  .chat-interface {
    display: flex;
    flex-direction: column;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile */
    background: #1e293b;
    color: #ffffff;
    overflow: hidden;
    position: relative;
  }
  
  .chat-interface::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: transparent;
    pointer-events: none;
    z-index: -1;
  }
  
  /* CHAT LAYOUT CONTAINER - Fixed structure */
  .chat-layout-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    width: 100%;
    position: relative;
  }

  /* BOTTOM CONTROL PANELS - Fixed layout to prevent overlapping */
  .bottom-control-panels {
    display: flex;
    flex-direction: column;
    max-height: 50vh;
    overflow-y: auto;
    overflow-x: hidden;
    background: #1e293b;
    border-top: 1px solid #475569;
    flex-shrink: 0;
    gap: 8px;
    padding: 8px;
  }

  /* Header - Fixed position and stable */
  .chat-header {
    flex-shrink: 0;
    background: #1e293b;
    padding: 16px;
    border-bottom: 1px solid #475569;
    text-align: center;
    min-height: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    z-index: 10;
  }
  
  /* Mobile header adjustments */
  @media (max-width: 768px) {
    .chat-header {
      padding: 12px 8px;
      min-height: 50px;
    }
    
    .chat-header h1 {
      font-size: 1.25rem;
      margin: 0;
    }
  }
  
  .chat-header h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  
  .error-banner {
    background: var(--glass-surface-light);
    border: 1px solid var(--error-500);
    color: var(--error-100);
    padding: var(--space-2) var(--space-4);
    margin-top: var(--space-2);
    border-radius: var(--radius-md);
    font-size: var(--text-sm);
  }
  
  /* Messages Section - Flexible height with stable positioning */
  .messages-section {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 16px;
    width: 100%;
    margin: 0;
    scroll-behavior: auto;
    min-height: 0;
    scrollbar-width: thin;
    scrollbar-color: #64748b transparent;
    background: #1e293b;
    position: relative;
  }
  
  .messages-section:focus {
    outline: 2px solid #3b82f6;
    outline-offset: -2px;
  }
  
  /* Modern glassmorphic scrollbar styling */
  .messages-section::-webkit-scrollbar {
    width: 6px;
  }
  
  .messages-section::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .messages-section::-webkit-scrollbar-thumb {
    background: var(--glass-surface-light);
    border: 1px solid var(--glass-border-highlight);
    border-radius: var(--radius-full);
  }
  
  .messages-section::-webkit-scrollbar-thumb:hover {
    background: var(--glass-surface-medium);
    border-color: var(--primary-400);
  }
  
  /* Mobile-specific adjustments */
  @media (max-width: 768px) {
    .messages-section {
      padding: 8px;
      max-width: 100vw;
    }
    
    .messages-section::-webkit-scrollbar {
      width: 10px;
    }
    
    .welcome-content {
      padding: 0 8px;
    }
    
    .welcome-title {
      font-size: 20px;
    }
    
    .welcome-description {
      font-size: 14px;
    }
  }
  
  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--neutral-300);
    padding: var(--space-5);
  }
  
  .welcome-content {
    text-align: center;
    max-width: 600px;
    width: 100%;
  }
  
  .welcome-title {
    margin: 0 0 var(--space-3) 0;
    font-size: var(--text-2xl);
    font-weight: var(--font-semibold);
    color: var(--neutral-50);
    font-family: var(--font-inter);
  }
  
  .welcome-description {
    margin: 0 0 var(--space-6) 0;
    font-size: var(--text-base);
    line-height: var(--leading-relaxed);
    color: var(--neutral-200);
    font-family: var(--font-inter);
  }
  
  .getting-started {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--neutral-400);
    font-style: italic;
    font-family: var(--font-inter);
  }
  
  /* Loading Overlay - Fixed positioning to prevent layout shifts */
  .message-sent-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    pointer-events: all;
  }

  .message-sent-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-8);
    background: var(--glass-surface-chat);
    border: var(--glass-border-highlight);
    border-radius: var(--radius-2xl);
    box-shadow: var(--glass-shadow-2xl);
    text-align: center;
    max-width: 400px;
    width: 90%;
  }

  .message-sent-icon {
    width: 64px;
    height: 64px;
    color: var(--success-500);
  }

  .message-sent-icon svg {
    width: 100%;
    height: 100%;
  }

  .message-sent-text h3 {
    font-size: var(--text-2xl);
    font-weight: 700;
    color: var(--success-500);
    margin: 0;
    font-family: var(--font-inter);
    letter-spacing: 0.05em;
  }

  .message-sent-text p {
    font-size: var(--text-lg);
    color: var(--neutral-300);
    margin: var(--space-2) 0 0 0;
    font-family: var(--font-inter);
    font-weight: 500;
    letter-spacing: 0.02em;
  }

  /* Mobile responsive adjustments for MESSAGE SENT overlay */
  @media (max-width: 768px) {
    .message-sent-content {
      padding: var(--space-6);
      max-width: 320px;
    }

    .message-sent-icon {
      width: 48px;
      height: 48px;
    }

    .message-sent-text h3 {
      font-size: var(--text-xl);
    }

    .message-sent-text p {
      font-size: var(--text-base);
    }
  }
  
  /* Chat Input Section - Fixed position at bottom */
  .chat-input-section {
    flex-shrink: 0;
    background: #1e293b;
    border-top: 1px solid #475569;
    padding: 16px;
    min-height: 80px;
    max-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
    z-index: 10;
  }
  
  .chat-input-container {
    display: flex;
    flex-direction: column;
    max-width: 1000px;
    margin: 0 auto;
    width: 100%;
  }

  /* Mobile input adjustments */
  @media (max-width: 768px) {
    .chat-input-section {
      padding: 12px 8px;
      min-height: 70px;
    }
  }
  

  /* SECTION 6: Consolidated Status & Performance Grid */
  .status-performance-grid {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 1rem;
    width: 100%;
  }

  /* Status Section Inline */
  .status-section-inline {
    display: flex;
    gap: 2rem;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
  }

  .status-metric {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--neutral-200);
    font-size: var(--text-sm);
    font-family: var(--font-inter);
    font-weight: 500;
  }

  .status-label {
    color: var(--neutral-400);
  }

  .status-value {
    color: var(--neutral-200);
    font-weight: 600;
  }

  .status--loading {
    color: var(--warning-500);
  }

  .status--ready {
    color: var(--success-500);
  }

  /* Performance Section Inline */
  .performance-section-inline {
    display: flex;
    gap: 2rem;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
  }


  .performance-metrics-grid {
    display: flex;
    gap: 2rem;
    align-items: center;
  }

  .performance-metric {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }

  .metric-label {
    font-size: var(--text-xs);
    color: var(--neutral-400);
    font-family: var(--font-inter);
  }

  .performance-metric span:last-child {
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    font-family: var(--font-inter);
  }

  .performance-metric .good {
    color: var(--success-500);
  }

  .performance-metric .warning {
    color: var(--warning-500);
  }

  .performance-note {
    margin-top: var(--space-2);
  }

  .performance-note small {
    font-size: var(--text-xs);
    color: var(--neutral-500);
    font-family: var(--font-inter);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .bottom-control-panels {
      max-height: 40vh;
    }

    .status-performance-grid {
      gap: 1rem;
    }

    .status-section-inline,
    .performance-section-inline {
      gap: 1rem;
    }

    .performance-metrics-grid {
      gap: 1rem;
    }

    .performance-metric,
    .status-metric {
      gap: 0.25rem;
      font-size: var(--text-xs);
    }
  }

  /* Component loading states */
  .component-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-3);
    color: var(--neutral-300);
    font-size: var(--text-sm);
    font-style: italic;
    font-family: var(--font-inter);
    background: var(--glass-surface-light);
    border-radius: var(--radius-lg);
    margin: var(--space-2) 0;
    min-height: 40px;
    max-height: 60px;
    border: var(--glass-border-highlight);
    contain: layout size;
    overflow: hidden;
  }

  .component-loading::before {
    content: 'Processing...';
    margin-right: var(--space-2);
    flex-shrink: 0;
    font-size: 16px;
    color: var(--primary-400);
  }

  /* Focus visible improvements */
  .chat-interface *:focus-visible {
    outline: 2px solid #63b3ed;
    outline-offset: 2px;
    border-radius: 4px;
  }

  /* Enhanced section focus management */
  .messages-section:focus-within,
  .chat-input-section:focus-within,
  .export-buttons-section:focus-within {
    background-color: rgba(99, 179, 237, 0.1);
  }

  .chat-input-section:focus-within {
    border-color: #63b3ed;
    box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.3);
  }


  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .chat-interface {
      border: 2px solid;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
`;
