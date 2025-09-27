import {
  Suspense,
  lazy,
  memo,
  startTransition,
  useCallback,
  useEffect,
  useMemo,
  useReducer,
  useRef
} from 'react';
// Removed useDebouncedCallback import - implementing direct state updates for <16ms input responsiveness

import {
  useInteractionLogger,
  usePerformanceLogger,
} from '../hooks/useDebugLog';
import { sendChatMessage } from '../services/api_OpenAI';
import { AIModelId } from '../types/ai_models';
import { Message } from '../types/chat_OpenAI';
import { logger } from '../utils/logger';
import { usePerformanceMonitoring } from '../utils/performance';

// Consolidated state interface for useReducer
interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  inputValue: string;
  isMobileSidebarOpen: boolean;
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
  | { type: 'TOGGLE_MOBILE_SIDEBAR' }
  | { type: 'CLOSE_MOBILE_SIDEBAR' }
  | { type: 'RESET_STATE' };

// Initial state
const initialChatState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  inputValue: '',
  isMobileSidebarOpen: false,
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
    case 'CLEAR_INPUT':
      return {
        ...state,
        inputValue: '',
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    case 'TOGGLE_MOBILE_SIDEBAR':
      return {
        ...state,
        isMobileSidebarOpen: !state.isMobileSidebarOpen,
      };
    case 'CLOSE_MOBILE_SIDEBAR':
      return {
        ...state,
        isMobileSidebarOpen: false,
      };
    case 'RESET_STATE':
      return initialChatState;
    default:
      return state;
  }
}

import ChatInput_OpenAI from './ChatInput_OpenAI';
import ChatMessage_OpenAI from './ChatMessage_OpenAI';
import DebugPanel from './DebugPanel';

// Lazy load secondary components for better performance
const ExportButtons = lazy(() =>
  import('./ExportButtons').then(module => ({ default: module.default }))
);
const RecentMessageButtons = lazy(() =>
  import('./RecentMessageButtons').then(module => ({ default: module.default }))
);

// Note: Styles are now included within each lazy-loaded component to prevent static imports
// that would break the lazy loading optimization

const ChatInterface_OpenAI = memo(function ChatInterface_OpenAI() {
  // Consolidated state management using useReducer for performance optimization
  const [state, dispatch] = useReducer(chatReducer, initialChatState);
  const {
    messages,
    isLoading,
    error,
    inputValue,
    isMobileSidebarOpen,
  } = state;

  // AI Model management - temporarily disabled to fix React Hook order error
  // const {
  //   models,
  //   currentModel,
  //   isLoading: isLoadingModels,
  //   error: modelError,
  //   selectModel,
  // } = useAIModel();
  const currentModel: AIModelId = 'gpt-5-nano' as AIModelId;


  // Optimize useMemo - Only memoize expensive calculations
  const hasMessages = messages.length > 0;
  const placeholderText = useMemo(
    () =>
      `Ask any financial question... (Shift+Enter for new line)`,
    []
  );

  // Performance and interaction tracking

  // Performance tracking - always available for optimization
  const { startTiming, endTiming } = usePerformanceLogger(
    'ChatInterface_OpenAI'
  );

  // User interaction logging - always available for UX insights
  const logInteraction = useInteractionLogger('ChatInterface_OpenAI');

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
      startTiming('message_processing');

      // Use optimized reducer action for immediate message start state
      dispatch({
        type: 'SEND_MESSAGE_START',
        payload: { userMessage },
      });

      // Use startTransition for non-critical logging
      startTransition(() => {
        logInteraction('send_message', 'chat_input', {
          messageLength: messageContent.length,
          messagePreview:
            messageContent.slice(0, 100) +
            (messageContent.length > 100 ? '...' : ''),
          messageId,
        });
      });

      try {
        logger.group('🌐 API Request Processing');
        logger.info('Sending message to API', {
          messageId,
          contentLength: messageContent.length,
          timestamp: new Date().toISOString(),
        });

        // Send to API and get response
        const apiResponse = await sendChatMessage(
          messageContent,
          currentModel || undefined
        );

        logger.info('✅ API response received', {
          messageId,
          responseLength: apiResponse.response.length,
        });
        logger.groupEnd();

        // Create AI message and dispatch success action
        const aiMessage: Message = {
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          content: apiResponse.response,
          sender: 'ai',
          timestamp: new Date(),
        };

        dispatch({
          type: 'SEND_MESSAGE_SUCCESS',
          payload: { aiMessage },
        });

        // End performance timing
        endTiming('message_processing');
      } catch (err: unknown) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to send message';

        logger.group('❌ API Request Failed');
        logger.error('API request failed', {
          messageId,
          errorType: err instanceof Error ? err.constructor.name : 'Unknown',
          errorMessage:
            errorMessage.slice(0, 200) +
            (errorMessage.length > 200 ? '...' : ''),
        });
        logger.groupEnd();

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
        endTiming('message_processing');
      }
    },
    [startTiming, endTiming, logInteraction, currentModel]
  ); // Include currentModel dependency



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

      {/* MAIN CONTENT PANEL: Header, Messages, Chat Input - NOW FULL WIDTH */}
      <div className='main-content-panel'>
        {/* SECTION 1: Header - Clean title only */}
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

        {/* SECTION 2: Messages Container */}
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
          {/* MESSAGE SENT OVERLAY - Phase 3 Implementation */}
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
        </main>

        {/* SECTION 3: Chat Input */}
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

      {/* BOTTOM CONTROL PANELS: All former sidebar components moved here */}
      <div className='bottom-control-panels' role='complementary'>

        {/* SECTION 6: Export/Recent Buttons */}
        <section
          className='export-buttons-section'
          role='complementary'
          aria-label='Export and recent message functions'
        >
          <div className='export-recent-container'>
            {hasMessages && (
              <Suspense
                fallback={
                  <div className='component-loading'>
                    Loading recent messages...
                  </div>
                }
              >
                <RecentMessageButtons messages={messages} />
              </Suspense>
            )}
            <Suspense
              fallback={
                <div className='component-loading'>
                  Loading export options...
                </div>
              }
            >
              <ExportButtons messages={messages} />
            </Suspense>
          </div>
        </section>

        {/* SECTION 7: Debug Panel */}
        <section
          className='debug-section'
          role='complementary'
          aria-label='Debug information'
        >
          <DebugPanel
            messageCount={messages.length}
            lastUpdate={new Date()}
            isConnected={true}
          />
        </section>

        {/* SECTION 8: Message Count and Status */}
        <section className='status-section' role='status' aria-live='polite'>
          <div className='message-count-display'>
            <span className='message-count-label'>Messages:</span>
            <span
              className='message-count-value'
              aria-label={`Total messages: ${messages.length}`}
            >
              {messages.length}
            </span>
          </div>
          <div className='status-info'>
            <span className='status-label'>Status:</span>
            <span
              className={`status-value ${isLoading ? 'status--loading' : 'status--ready'}`}
              aria-label={`Current status: ${isLoading ? 'Processing request' : 'Ready for input'}`}
            >
              {isLoading ? 'Processing...' : 'Ready'}
            </span>
          </div>
        </section>

        {/* SECTION 9: Performance Monitoring Display */}
        <section
          className='performance-section'
          data-testid='performance-indicator'
        >
          <div className='performance-header'>
            <h4>Performance Metrics</h4>
          </div>
          <div className='performance-metrics-grid'>
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
          <div className='performance-note'>
            <small>Metrics update after user interaction</small>
          </div>
        </section>
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
  
  /* FULL-WIDTH LAYOUT: Professional Fintech Glassmorphic Implementation with Layout Stability */
  .chat-interface {
    display: flex;
    flex-direction: column;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile */
    background: var(--glass-surface-medium);
    color: var(--neutral-100);
    overflow: hidden; /* Prevent page-level scrolling */
    position: relative;
  }
  
  .chat-interface::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--neutral-900);
    opacity: 0.05;
    pointer-events: none;
    z-index: -1;
  }
  
  /* MAIN CONTENT PANEL - Now takes full width */
  .main-content-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
    width: 100%;
  }

  /* BOTTOM CONTROL PANELS - All former sidebar components */
  .bottom-control-panels {
    display: flex;
    flex-direction: column;
    max-height: 50vh; /* Limit height to allow scrolling */
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--glass-surface-medium);
    border-top: 1px solid var(--glass-border-highlight);
  }

  /* SECTION 1: Header - Professional Fintech Glassmorphic Header with Blue Chat Theme */
  .chat-header {
    flex-shrink: 0;
    position: relative;
    background: var(--glass-surface-chat);
    padding: var(--space-4);
    border: var(--border-chat);
    border-bottom: var(--border-chat);
    box-shadow: var(--border-glow-chat);
    text-align: center;
    min-height: 70px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .chat-header:hover {
    box-shadow: var(--border-glow-chat-hover);
  }
  
  /* Mobile header adjustments */
  @media (max-width: 768px) {
    .chat-header {
      padding: 12px 8px;
      min-height: 50px;
    }
    
    .chat-header h1 {
      font-size: 1.25rem;
      margin: 0 0 8px 0;
    }
  }
  
  .chat-header h1 {
    margin: 0 0 var(--space-2) 0;
    font-size: var(--text-xl);
    font-weight: var(--font-semibold);
    color: var(--neutral-50);
    font-family: var(--font-inter);
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
  
  /* SECTION 2: Messages - Flexible height with glassmorphic scrolling and Blue Chat Theme */
  .messages-section {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: var(--space-4);
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    scroll-behavior: auto;
    min-height: 0;
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-400) transparent;
    background: var(--glass-surface-chat);
    border-left: var(--border-chat);
    border-right: var(--border-chat);
    box-shadow: var(--border-glow-chat);
  }
  
  .messages-section:hover {
    box-shadow: var(--border-glow-chat-hover);
  }
  
  .messages-section:focus {
    outline: 2px solid #007bff;
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
  
  /* MESSAGE SENT Overlay - Prominent loading state */
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
  
  /* SECTION 3: Chat Input - Professional glassmorphic input section with Blue Chat Theme */
  .chat-input-section {
    flex-shrink: 0;
    background: var(--glass-surface-chat);
    border: var(--border-chat);
    border-top: var(--border-chat);
    border-bottom: var(--border-chat);
    box-shadow: var(--border-glow-chat);
    padding: var(--space-4);
    min-height: 90px;
    max-height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .chat-input-section:hover {
    box-shadow: var(--border-glow-chat-hover);
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
  
  
  /* SECTION 6: Export/Recent Buttons - Professional glassmorphic utilities with Green Export Theme */
  .export-buttons-section {
    flex-shrink: 0;
    background: var(--glass-surface-export);
    border: var(--border-export);
    border-top: var(--border-export);
    border-bottom: var(--border-export);
    box-shadow: var(--border-glow-export);
    padding: var(--space-3) var(--space-4);
    min-height: 70px; 
    max-height: 120px; 
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto;
    overflow-x: hidden;
    contain: layout style;
  }
  
  .export-buttons-section:hover {
    box-shadow: var(--border-glow-export-hover);
  }
  
  .export-recent-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    max-width: 1000px;
    align-items: center;
  }
  
  /* SECTION 7: Debug Panel - Professional glassmorphic developer information with Orange/Amber Debug Theme */
  .debug-section {
    flex-shrink: 0;
    background: var(--glass-surface-debug);
    border: var(--border-debug);
    border-top: var(--border-debug);
    box-shadow: var(--border-glow-debug);
    padding: var(--space-3) var(--space-4);
    min-height: 80px; 
    max-height: 120px; 
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto;
    overflow-x: hidden;
    contain: layout style;
  }
  
  .debug-section:hover {
    box-shadow: var(--border-glow-debug-hover);
  }

  /* SECTION 8: Status Section - Message Count and Status */
  .status-section {
    flex-shrink: 0;
    background: var(--glass-surface-debug);
    border: var(--border-debug);
    border-top: var(--border-debug);
    box-shadow: var(--border-glow-debug);
    padding: var(--space-3) var(--space-4);
    min-height: 60px;
    max-height: 80px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    overflow-x: auto;
    overflow-y: hidden;
    contain: layout style;
  }

  .status-section:hover {
    box-shadow: var(--border-glow-debug-hover);
  }

  .message-count-display {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--neutral-200);
    font-size: var(--text-sm);
    font-family: var(--font-inter);
    font-weight: 500;
  }

  .status-info {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--neutral-300);
    font-size: var(--text-xs);
    font-family: var(--font-inter);
  }

  /* SECTION 9: Performance Section */
  .performance-section {
    flex-shrink: 0;
    background: var(--glass-surface-debug);
    border: var(--border-debug);
    border-top: var(--border-debug);
    box-shadow: var(--border-glow-debug);
    padding: var(--space-3) var(--space-4);
    min-height: 80px;
    max-height: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-y: auto;
    overflow-x: hidden;
    contain: layout style;
  }

  .performance-section:hover {
    box-shadow: var(--border-glow-debug-hover);
  }

  .performance-header h4 {
    margin: 0 0 var(--space-2) 0;
    font-size: var(--text-sm);
    font-weight: var(--font-semibold);
    color: var(--neutral-200);
    font-family: var(--font-inter);
  }

  .performance-metrics-grid {
    display: flex;
    gap: var(--space-4);
    align-items: center;
  }

  .performance-metric {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-1);
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

    .export-buttons-section,
    .debug-section,
    .status-section,
    .performance-section {
      padding: 8px 12px;
      min-height: 60px;
    }


    .performance-metrics-grid {
      gap: var(--space-2);
    }

    .performance-metric {
      gap: 2px;
    }

    .message-count-display,
    .status-info {
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