import {
  Suspense,
  lazy,
  memo,
  startTransition,
  useCallback,
  useDeferredValue,
  useEffect,
  useMemo,
  useReducer,
  useRef,
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
  sharedTicker: string;
  latestResponseTime: number | null;
  isMobileSidebarOpen: boolean;
}

// Action types for state management
type ChatAction =
  | { type: 'SEND_MESSAGE_START'; payload: { userMessage: Message } }
  | {
    type: 'SEND_MESSAGE_SUCCESS';
    payload: { aiMessage: Message; responseTime: number };
  }
  | {
    type: 'SEND_MESSAGE_ERROR';
    payload: {
      errorMessage: string;
      aiMessage: Message;
      responseTime: number;
    };
  }
  | { type: 'UPDATE_INPUT'; payload: string }
  | { type: 'UPDATE_TICKER'; payload: string }
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
  sharedTicker: 'NVDA',
  latestResponseTime: null,
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
        latestResponseTime: action.payload.responseTime,
      };
    case 'SEND_MESSAGE_ERROR':
      return {
        ...state,
        isLoading: false,
        error: action.payload.errorMessage,
        messages: [...state.messages, action.payload.aiMessage],
        latestResponseTime: action.payload.responseTime,
      };
    case 'UPDATE_INPUT':
      return {
        ...state,
        inputValue: action.payload,
      };
    case 'UPDATE_TICKER':
      return {
        ...state,
        sharedTicker: action.payload,
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
import SharedTickerInput from './SharedTickerInput';

// Lazy load secondary components for better performance
const ExportButtons = lazy(() =>
  import('./ExportButtons').then(module => ({ default: module.default }))
);
const RecentMessageButtons = lazy(() =>
  import('./RecentMessageButtons').then(module => ({ default: module.default }))
);
const AnalysisButton = lazy(() =>
  import('./AnalysisButton').then(module => ({ default: module.default }))
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
    sharedTicker,
    latestResponseTime,
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

  // Use deferred values for non-urgent UI updates to improve responsiveness
  const deferredSharedTicker = useDeferredValue(sharedTicker);

  // Optimize useMemo - Only memoize expensive calculations
  const hasMessages = messages.length > 0;
  const lastMessage = messages[messages.length - 1];
  const placeholderText = useMemo(() =>
    `Ask about ${sharedTicker} or any financial question... (Shift+Enter for new line)`,
    [sharedTicker]
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

  // Prompt template API for analysis buttons - temporarily disabled to fix React Hook order error
  // const { templates } = usePromptAPI();
  const templates = [
    { id: 'snapshot', type: 'snapshot' as const, name: 'Stock Snapshot', description: 'Snapshot analysis template', template: 'Provide snapshot analysis for {ticker}', icon: '📊', requiresTicker: true, followUpQuestions: ['Would you like more details on this analysis?', 'Should we analyze another stock?'] as readonly string[] },
    { id: 'support_resistance', type: 'support_resistance' as const, name: 'Support/Resistance', description: 'Support Resistance analysis template', template: 'Provide support resistance analysis for {ticker}', icon: '📈', requiresTicker: true, followUpQuestions: ['Would you like more details on this analysis?', 'Should we analyze another stock?'] as readonly string[] },
    { id: 'technical', type: 'technical' as const, name: 'Technical Analysis', description: 'Technical analysis template', template: 'Provide technical analysis for {ticker}', icon: '🔍', requiresTicker: true, followUpQuestions: ['Would you like more details on this analysis?', 'Should we analyze another stock?'] as readonly string[] }
  ];

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

  // Handle prompt population from analysis buttons with immediate updates
  const handlePromptGenerated = useCallback(
    (prompt: string) => {
      // Immediate state update for instant UI feedback using reducer dispatch
      dispatch({ type: 'UPDATE_INPUT', payload: prompt });

      // Focus the input immediately for best UX
      // Note: Focus handling moved to ChatInput component

      // Use startTransition for non-critical logging and analytics
      startTransition(() => {
        logInteraction('prompt_generated', 'analysis_button', {
          promptLength: prompt.length,
          promptPreview:
            prompt.slice(0, 50) + (prompt.length > 50 ? '...' : ''),
        });

        logger.debug('🎯 Prompt generated and input updated', {
          promptLength: prompt.length,
        });
      });
    },
    [logInteraction]
  );

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
        const apiResponse = await sendChatMessage(messageContent, currentModel || undefined);

        // Extract response time from backend metadata
        const responseTime = apiResponse.metadata?.response_time
          ? parseFloat(apiResponse.metadata.response_time.replace('s', ''))
          : 0;

        logger.info('✅ API response received', {
          messageId,
          processingTime: `${responseTime}s`,
          responseLength: apiResponse.response.length,
        });
        logger.groupEnd();

        // Create AI message and dispatch success action
        const aiMessage: Message = {
          id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
          content: apiResponse.response,
          sender: 'ai',
          timestamp: new Date(),
          metadata: { processingTime: responseTime },
        };

        dispatch({
          type: 'SEND_MESSAGE_SUCCESS',
          payload: { aiMessage, responseTime },
        });

        // End performance timing
        endTiming('message_processing');
      } catch (err: unknown) {
        // For errors, we don't have backend response time, so use 0 as fallback
        const responseTime = 0;
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to send message';

        logger.group('❌ API Request Failed');
        logger.error('API request failed', {
          messageId,
          processingTime: `${responseTime}s`,
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
          metadata: { processingTime: responseTime, isError: true },
        };

        dispatch({
          type: 'SEND_MESSAGE_ERROR',
          payload: { errorMessage, aiMessage, responseTime },
        });

        // End performance timing even on error
        endTiming('message_processing');
      }
    },
    [startTiming, endTiming, logInteraction, currentModel]
  ); // Include currentModel dependency

  const handleTickerChange = useCallback(
    (newTicker: string) => {
      // Immediate ticker update using reducer dispatch
      dispatch({ type: 'UPDATE_TICKER', payload: newTicker });

      // Use startTransition for non-critical logging
      startTransition(() => {
        logInteraction('ticker_change', 'analysis_buttons', {
          oldTicker: sharedTicker,
          newTicker,
          source: 'analysis_buttons',
        });
      });
    },
    [logInteraction, sharedTicker]
  );

  // Phase 4: Mobile Sidebar Toggle Handlers
  const handleToggleMobileSidebar = useCallback(() => {
    dispatch({ type: 'TOGGLE_MOBILE_SIDEBAR' });

    startTransition(() => {
      logInteraction('mobile_sidebar_toggle', 'mobile_ui', {
        isOpen: !isMobileSidebarOpen,
      });
    });
  }, [logInteraction, isMobileSidebarOpen]);

  const handleCloseMobileSidebar = useCallback(() => {
    dispatch({ type: 'CLOSE_MOBILE_SIDEBAR' });

    startTransition(() => {
      logInteraction('mobile_sidebar_close', 'mobile_ui', {
        isOpen: false,
      });
    });
  }, [logInteraction]);

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

      {/* MAIN CONTENT PANEL: Header, Messages, Chat Input */}
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
                  Get instant financial insights powered by AI. Use the ticker
                  input and quick analysis tools below or type your own questions.
                </p>
                <p className='getting-started'>
                  Start by entering a ticker symbol and using the analysis
                  buttons, or type a message directly.
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
              onChange={(value) => dispatch({ type: 'UPDATE_INPUT', payload: value })}
            />
          </div>
        </section>
      </div>

      {/* Phase 4: Mobile Sidebar Toggle Button */}
      <button
        className="mobile-sidebar-toggle"
        onClick={handleToggleMobileSidebar}
        aria-label="Toggle sidebar"
        aria-expanded={isMobileSidebarOpen}
        data-testid="mobile-sidebar-toggle"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M3 12h18M3 6h18M3 18h18"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {/* Phase 4: Mobile Sidebar Overlay */}
      {isMobileSidebarOpen && (
        <div
          className="mobile-sidebar-overlay"
          onClick={handleCloseMobileSidebar}
          aria-hidden="true"
        />
      )}

      {/* RIGHT SIDEBAR PANEL: Ticker Input, Analysis Buttons, Export Buttons, Debug */}
      <div className={`right-sidebar-panel ${isMobileSidebarOpen ? 'open' : ''}`}>
        {/* Phase 4: Mobile Sidebar Close Button */}
        <button
          className="mobile-sidebar-close"
          onClick={handleCloseMobileSidebar}
          aria-label="Close sidebar"
          data-testid="mobile-sidebar-close"
        >
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M18 6L6 18M6 6l12 12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>

        {/* SECTION 4: Ticker Input */}
        <section
          className='ticker-input-section'
          role='complementary'
          aria-label='Stock ticker input'
        >
          <Suspense
            fallback={
              <div className='component-loading'>
                Loading ticker input...
              </div>
            }
          >
            <SharedTickerInput
              value={deferredSharedTicker}
              onChange={handleTickerChange}
              onAnalyze={() => handlePromptGenerated(`analyze ${deferredSharedTicker}`)}
              disabled={isLoading}
            />
          </Suspense>
        </section>

        {/* SECTION 5: Analysis Buttons */}
        <section
          className='analysis-buttons-section'
          role='complementary'
          aria-label='Quick analysis tools'
        >
          <Suspense
            fallback={
              <div className='component-loading analysis-loading'>
                Loading analysis tools...
              </div>
            }
          >
            <div className="analysis-buttons-container" data-testid="analysis-buttons">
              <h3 className="analysis-section-header">QUICK ANALYSIS</h3>
              <div className="analysis-buttons-grid">
                {templates.map((template) => (
                  <Suspense key={template.id} fallback={<div>Loading...</div>}>
                    <AnalysisButton
                      template={template}
                      ticker={deferredSharedTicker}
                      onPromptGenerated={handlePromptGenerated}
                      isLoading={isLoading}
                      disabled={isLoading}
                    />
                  </Suspense>
                ))}
              </div>
            </div>
          </Suspense>
        </section>

        {/* SECTION 6: Export/Recent Buttons */}
        <section
          className='export-buttons-section'
          role='complementary'
          aria-label='Export and recent message functions'
        >
          {hasMessages && (
            <div className='export-recent-container'>
              <Suspense
                fallback={
                  <div className='component-loading'>
                    Loading recent messages...
                  </div>
                }
              >
                <RecentMessageButtons messages={messages} />
              </Suspense>
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
          )}
        </section>

        {/* SECTION 7: Debug Panel */}
        <section
          className='debug-section'
          role='complementary'
          aria-label='Debug information'
        >
          <DebugPanel
            responseTime={latestResponseTime || 0}
            messageCount={messages.length}
            lastUpdate={new Date()}
            isConnected={true}
          />
        </section>
      </div>

      {/* BOTTOM CONTROL PANEL: Response Time and Message Count */}
      <div className='bottom-control-panel' role="status" aria-live="polite">
        <div className='response-time-display'>
          <span className='response-time-label'>Response Time:</span>
          <span
            className={`response-time-value ${latestResponseTime
              ? latestResponseTime < 5
                ? 'response-time--fast'
                : latestResponseTime < 15
                  ? 'response-time--medium'
                  : 'response-time--slow'
              : ''
              }`}
            aria-label={`Response time: ${latestResponseTime ? `${latestResponseTime.toFixed(2)} seconds` : 'Not available'}`}
          >
            {latestResponseTime ? `${latestResponseTime.toFixed(2)}s` : 'N/A'}
          </span>
        </div>
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
      </div>

      {/* Phase 4: Performance Monitoring Display - Enhanced */}
      <div className="performance-indicator" data-testid="performance-indicator">
        <div className="performance-header">
          <h4>Performance Metrics</h4>
        </div>
        <div className="performance-metrics-grid">
          <div className="performance-metric">
            <span className="metric-label">FCP:</span>
            <span className={performanceMetrics.fcp && performanceMetrics.fcp < 1500 ? 'good' : 'warning'}>
              {performanceMetrics.fcp ? `${performanceMetrics.fcp.toFixed(0)}ms` : 'Calculating...'}
            </span>
          </div>
          <div className="performance-metric">
            <span className="metric-label">LCP:</span>
            <span className={performanceMetrics.lcp && performanceMetrics.lcp < 2500 ? 'good' : 'warning'}>
              {performanceMetrics.lcp ? `${performanceMetrics.lcp.toFixed(0)}ms` : 'Calculating...'}
            </span>
          </div>
          <div className="performance-metric">
            <span className="metric-label">CLS:</span>
            <span className={performanceMetrics.cls && performanceMetrics.cls < 0.1 ? 'good' : 'warning'}>
              {performanceMetrics.cls ? performanceMetrics.cls.toFixed(3) : 'Calculating...'}
            </span>
          </div>
        </div>
        <div className="performance-note">
          <small>Metrics update after user interaction</small>
        </div>
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
  
  /* TWO-PANEL LAYOUT: Professional Fintech Glassmorphic Implementation with Layout Stability */
  .chat-interface {
    display: grid;
    /* Two-panel layout with bottom control panel */
    grid-template-columns: 1fr 350px; /* Main content + 350px sidebar */
    grid-template-rows: 1fr auto; /* Main content + bottom control panel */
    grid-template-areas: 
      "main-content sidebar"
      "bottom-control bottom-control";
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile */
    background: var(--glass-surface-medium);
    backdrop-filter: var(--backdrop-blur-lg);
    -webkit-backdrop-filter: var(--backdrop-blur-lg);
    color: var(--neutral-100);
    overflow: hidden; /* Prevent page-level scrolling */
    gap: 0; /* No gaps between sections for seamless design */
    position: relative;
  }
  
  .chat-interface::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      135deg,
      var(--primary-900) 0%,
      var(--primary-800) 50%,
      var(--neutral-900) 100%
    );
    opacity: 0.05;
    pointer-events: none;
    z-index: -1;
  }
  
  /* Tablet layout adjustments */
  @media (min-width: 768px) and (max-width: 1024px) {
    .chat-interface {
      grid-template-columns: 1fr 300px; /* Main content + 300px sidebar */
    }
  }

  /* Mobile viewport optimizations with stable grid layout */
  @media (max-width: 767px) {
    .chat-interface {
      height: 100vh;
      height: 100svh; /* Small viewport height for mobile browsers */
      /* Mobile-optimized two-panel layout */
      grid-template-areas: 
        "main-content"
        "sidebar"
        "bottom-control";
      grid-template-columns: 1fr; /* Single column on mobile */
      grid-template-rows: 1fr auto auto; /* Main content + sidebar + bottom control */
    }
  }
  
  /* MAIN CONTENT PANEL - Contains header, messages, and chat input */
  .main-content-panel {
    grid-area: main-content;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  /* RIGHT SIDEBAR PANEL - Contains ticker input, analysis buttons, export buttons, debug */
  .right-sidebar-panel {
    grid-area: sidebar;
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    gap: 0;
  }

  /* SECTION 1: Header - Professional Fintech Glassmorphic Header with Blue Chat Theme */
  .chat-header {
    flex-shrink: 0;
    position: relative;
    background: var(--glass-surface-chat);
    backdrop-filter: var(--glass-blur-md);
    -webkit-backdrop-filter: var(--glass-blur-md);
    padding: var(--space-4);
    border: var(--border-chat);
    border-bottom: var(--border-chat);
    box-shadow: var(--border-glow-chat);
    text-align: center;
    min-height: 70px; /* Prevent layout shifts */
    display: flex;
    flex-direction: column;
    justify-content: center;
    /* Transition removed for performance */
  }
  
  .chat-header:hover {
    box-shadow: var(--border-glow-chat-hover);
  }
  
  /* Mobile header adjustments */
  @media (max-width: 767px) {
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
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
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
    overflow-x: hidden; /* Prevent horizontal page scroll */
    padding: var(--space-4);
    width: 100%;
    max-width: 100%; /* Remove 800px limit for better mobile */
    margin: 0 auto;
    /* Enhanced focus management - SMOOTH SCROLLING REMOVED FOR PERFORMANCE */
    scroll-behavior: auto;
    min-height: 0; /* Allow shrinking in flex layout */
    /* Custom scrollbar for glassmorphic look */
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-400) transparent;
    /* Blue Chat Theme Enhancement - Tasks 4 & 6 */
    background: var(--glass-surface-chat);
    border-left: var(--border-chat);
    border-right: var(--border-chat);
    box-shadow: var(--border-glow-chat);
    /* Transition removed for performance */
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
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
    border: 1px solid var(--glass-border-highlight);
    border-radius: var(--radius-full);
  }
  
  .messages-section::-webkit-scrollbar-thumb:hover {
    background: var(--glass-surface-medium);
    border-color: var(--primary-400);
  }
  
  /* Mobile-specific adjustments */
  @media (max-width: 767px) {
    .messages-section {
      padding: 8px;
      max-width: 100vw;
    }
    
    .messages-section::-webkit-scrollbar {
      width: 10px; /* Thicker scrollbars on mobile */
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
  
  /* Tablet adjustments */
  @media (min-width: 768px) and (max-width: 1024px) {
    .messages-section {
      max-width: 900px;
      padding: 20px;
    }
  }
  
  /* Desktop optimizations */
  @media (min-width: 1025px) {
    .messages-section {
      max-width: 1000px;
      padding: 24px;
    }
    
    .welcome-title {
      font-size: 28px;
    }
    
    .welcome-description {
      font-size: 18px;
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
  
  .welcome-buttons {
    margin: 0 0 24px 0;
  }
  
  .getting-started {
    margin: 0;
    font-size: var(--text-sm);
    color: var(--neutral-400);
    font-style: italic;
    font-family: var(--font-inter);
  }
  
  /* ==========================================================================
     PHASE 3: LOADING STATE ENHANCEMENT - MESSAGE SENT OVERLAY
     ========================================================================== */

  /* MESSAGE SENT Overlay - Prominent loading state */
  .message-sent-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    animation: fadeIn 0.3s ease-out;
  }

  .message-sent-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-8);
    background: var(--glass-surface-chat);
    backdrop-filter: var(--glass-blur-lg);
    -webkit-backdrop-filter: var(--glass-blur-lg);
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
    animation: pulse 2s infinite;
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

  /* Animations for MESSAGE SENT overlay */
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.05);
      opacity: 0.8;
    }
  }

  /* Mobile responsive adjustments for MESSAGE SENT overlay */
  @media (max-width: 767px) {
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
    backdrop-filter: var(--glass-blur-md);
    -webkit-backdrop-filter: var(--glass-blur-md);
    border: var(--border-chat);
    border-top: var(--border-chat);
    border-bottom: var(--border-chat);
    box-shadow: var(--border-glow-chat);
    padding: var(--space-4);
    min-height: 90px; /* Fixed minimum height prevents jumping */
    max-height: 150px; /* Prevent excessive expansion */
    display: flex;
    flex-direction: column;
    justify-content: center;
    /* Transition removed for performance */
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
  @media (max-width: 767px) {
    .chat-input-section {
      padding: 12px 8px;
      min-height: 70px;
    }
    

  }
  
  /* Tablet and desktop input optimizations */
  @media (min-width: 768px) {
    .chat-input-section {
      padding: 20px;
      min-height: 80px;
    }
  }
  
  /* SECTION 4: Ticker Input - Professional glassmorphic ticker input with Purple Analysis Theme */
  .ticker-input-section {
    flex-shrink: 0;
    background: var(--glass-surface-analysis);
    backdrop-filter: var(--glass-blur-lg);
    -webkit-backdrop-filter: var(--glass-blur-lg);
    border: var(--border-analysis);
    border-top: var(--border-analysis);
    border-bottom: var(--border-analysis);
    box-shadow: var(--border-glow-analysis);
    padding: var(--space-2) var(--space-4);
    min-height: 80px;
    max-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    contain: layout style;
  }

  .ticker-input-section:hover {
    box-shadow: var(--border-glow-analysis-hover);
  }

  /* SECTION 5: Analysis Buttons - Professional glassmorphic analysis tools with Purple Analysis Theme */
  .analysis-buttons-section {
    flex-shrink: 0;
    background: var(--glass-surface-analysis);
    backdrop-filter: var(--glass-blur-lg);
    -webkit-backdrop-filter: var(--glass-blur-lg);
    border: var(--border-analysis);
    border-top: var(--border-analysis);
    border-bottom: var(--border-analysis);
    box-shadow: var(--border-glow-analysis);
    padding: var(--space-2) var(--space-4);
    /* Increased height to accommodate integrated ticker input - no scrolling */
    min-height: 180px; 
    max-height: 280px; 
    overflow-y: visible; /* Show all content without scrolling */
    overflow-x: hidden; /* Prevent horizontal overflow */
    display: flex;
    align-items: flex-start;
    justify-content: center;
    /* Contain layout changes during loading states */
    contain: layout style;
    /* Transition removed for performance */
  }
  
  .analysis-buttons-section:hover {
    box-shadow: var(--border-glow-analysis-hover);
  }
  

  
  .fixed-analysis-buttons {
    margin: 0;
    border: none;
    background: transparent;
    width: 100%;
    max-width: 1000px;
    padding: 0;
  }
  
  .analysis-loading {
    min-height: 80px;
    background: #2d3748; /* Dark loading background */
    border-radius: 8px;
    margin: 8px 0;
    color: #cbd5e0; /* Light loading text */
  }
  
  /* Mobile analysis buttons adjustments */
  @media (max-width: 767px) {
    .analysis-buttons-section {
      padding: 6px 8px;
      min-height: 150px;
      max-height: 240px;
    }
  }
  
  /* Tablet and desktop analysis buttons optimizations */
  @media (min-width: 768px) {
    .analysis-buttons-section {
      padding: 12px 20px;
      min-height: 160px;
      max-height: 260px;
    }
  }
  
  /* SECTION 6: Export/Recent Buttons - Professional glassmorphic utilities with Green Export Theme */
  .export-buttons-section {
    flex-shrink: 0;
    background: var(--glass-surface-export);
    backdrop-filter: var(--glass-blur-md);
    -webkit-backdrop-filter: var(--glass-blur-md);
    border: var(--border-export);
    border-top: var(--border-export);
    border-bottom: var(--border-export);
    box-shadow: var(--border-glow-export);
    padding: var(--space-3) var(--space-4);
    /* Grid minmax() now controls height - these ensure consistent behavior */
    min-height: 70px; 
    max-height: 120px; 
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto; /* Enable scrolling if content exceeds bounds */
    overflow-x: hidden; /* Prevent horizontal overflow */
    /* Contain layout changes during loading states */
    contain: layout style;
    /* Transition removed for performance */
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
  
  /* Mobile export-recent container adjustments */
  @media (max-width: 767px) {
    .export-recent-container {
      gap: 6px;
    }
  }
  
  /* SECTION 7: Debug Panel - Professional glassmorphic developer information with Orange/Amber Debug Theme */
  .debug-section {
    flex-shrink: 0;
    background: var(--glass-surface-debug);
    backdrop-filter: var(--glass-blur-lg);
    -webkit-backdrop-filter: var(--glass-blur-lg);
    border: var(--border-debug);
    border-top: var(--border-debug);
    box-shadow: var(--border-glow-debug);
    padding: var(--space-3) var(--space-4);
    /* Grid minmax() now controls height - these ensure consistent behavior */
    min-height: 80px; 
    max-height: 120px; 
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-y: auto; /* Enable scrolling if content exceeds bounds */
    overflow-x: hidden; /* Prevent horizontal overflow */
    /* Contain layout changes during loading states */
    contain: layout style;
    /* Transition removed for performance */
  }
  
  .debug-section:hover {
    box-shadow: var(--border-glow-debug-hover);
  }
  
  .main-debug-panel {
    margin: 0;
    border: none;
    background: transparent;
    width: 100%;
    max-width: 1000px;
    padding: 0;
    box-shadow: none;
  }

  /* BOTTOM CONTROL PANEL - Response Time and Message Count Display */
  .bottom-control-panel {
    grid-area: bottom-control;
    background: var(--glass-surface-debug);
    backdrop-filter: var(--glass-blur-lg);
    -webkit-backdrop-filter: var(--glass-blur-lg);
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

  .bottom-control-panel:hover {
    box-shadow: var(--border-glow-debug-hover);
  }

  .response-time-display {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--neutral-200);
    font-size: var(--text-sm);
    font-family: var(--font-inter);
    font-weight: 500;
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

  /* Mobile bottom control panel adjustments */
  @media (max-width: 767px) {
    .bottom-control-panel {
      padding: 8px 12px;
      min-height: 50px;
      max-height: 70px;
      flex-direction: column;
      gap: 4px;
    }

    .response-time-display,
    .message-count-display,
    .status-info {
      font-size: var(--text-xs);
    }
  }
  
  /* Mobile export and debug section adjustments */
  @media (max-width: 767px) {
    .export-buttons-section {
      padding: 8px 12px;
      min-height: 60px;
      max-height: 100px; /* Increased for both button sets */
    }
    
    .debug-section {
      padding: 8px 12px;
      min-height: 50px;
      max-height: 80px;
    }
  }
  
  /* Tablet and desktop export and debug section optimizations */
  @media (min-width: 768px) {
    .export-buttons-section {
      padding: 16px 20px;
      min-height: 70px;
      max-height: 110px; /* Increased for both button sets */
    }
    
    .debug-section {
      padding: 16px 20px;
      min-height: 70px;
      max-height: 100px;
    }
  }
  
  /* Export and debug section focus management - DARK MODE */
  .export-buttons-section:focus-within {
    border-color: #63b3ed; /* Light blue border for dark mode */
    box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.3);
  }
  
  .debug-section:focus-within {
    border-color: #63b3ed; /* Light blue border for dark mode */
    box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.3);
  }
  
  /* Export buttons responsive layout */
  @media (max-width: 640px) {
    .export-buttons-grid,
    .recent-message-buttons {
      gap: 6px;
    }
  }
  
  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .chat-interface {
      border: 2px solid;
    }
    
    .message-bubble {
      border: 1px solid;
    }
  }
  
  /* Modern Grid Layout Stability Enhancements */
  .chat-interface {
    container-type: inline-size; /* Enable container queries */
  }
  
  /* Container query for ultra-responsive design */
  @container (max-width: 500px) {
    .inputs-container {
      gap: 8px;
    }
    
    .user-inputs-section {
      min-height: 90px;
    }
    
    .analysis-buttons-section {
      min-height: 130px;
    }
  }
  
  /* Reduced motion support - ALL ANIMATIONS ALREADY REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
  
  /* Focus visible improvements with modern focus rings - DARK MODE */
  .chat-interface *:focus-visible {
    outline: 2px solid #63b3ed; /* Light blue focus ring for dark mode */
    outline-offset: 2px;
    border-radius: 4px;
  }
  
  /* Enhanced section focus management - DARK MODE */
  .messages-section:focus-within,
  .chat-input-section:focus-within,
  .ticker-input-section:focus-within,
  .analysis-buttons-section:focus-within,
  .export-buttons-section:focus-within {
    background-color: rgba(99, 179, 237, 0.1); /* Light blue overlay for dark mode */
    /* Transition removed for performance */
  }
  
  /* Modern focus indicators for sections - DARK MODE */
  .chat-input-section:focus-within {
    border-color: #63b3ed; /* Light blue border for dark mode */
    box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.3);
  }
  
  .ticker-input-section:focus-within {
    border-color: #63b3ed; /* Light blue border for dark mode */
    box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.3);
  }
  
  .analysis-buttons-section:focus-within {
    border-color: #63b3ed; /* Light blue border for dark mode */
    box-shadow: inset 0 0 0 1px rgba(99, 179, 237, 0.3);
  }

  /* Component loading states - Professional glassmorphic loading with layout containment */
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
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
    border-radius: var(--radius-lg);
    margin: var(--space-2) 0;
    min-height: 40px;
    max-height: 60px; /* Prevent loading states from growing too large */
    border: var(--glass-border-highlight);
    /* Ensure loading states don't affect parent section dimensions */
    contain: layout size;
    overflow: hidden;
  }

  .component-loading::before {
    content: 'Processing...';
    margin-right: var(--space-2);
    flex-shrink: 0;
    font-size: 16px;
    color: var(--primary-400);
    /* Spinner animation removed for performance */
  }

  /* Loading state variations for different locations */
  .chat-header .component-loading {
    margin: 4px 0;
    min-height: 32px;
    font-size: 12px;
  }

  .welcome-buttons .component-loading {
    margin: 16px 0;
    min-height: 60px;
    font-size: 14px;
  }

  .conversation-buttons .component-loading {
    margin: 0;
    border-radius: 0;
    border-top: 1px solid #e0e0e0;
    border-bottom: 1px solid #e0e0e0;
  }

  /* High DPI and Retina Display Support */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
    .chat-interface {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    
    .messages-section::-webkit-scrollbar-thumb,
    .analysis-buttons-section::-webkit-scrollbar-thumb {
      border-radius: 4px;
    }
  }
  
  /* Dark mode is now the default theme - no media queries needed */
  
  /* Reduced motion support - ALL ANIMATIONS ALREADY REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
  
  /* ==========================================================================
     PHASE 2: INPUT DIFFERENTIATION & LABELING - Enhanced Input Components
     ========================================================================== */

  /* Chat Input Container - AI CHATBOT INPUT */
  .chat-input-container {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    padding: var(--space-4);
    background: var(--glass-surface-chat);
    backdrop-filter: var(--glass-blur-md);
    -webkit-backdrop-filter: var(--glass-blur-md);
    border: var(--glass-border-highlight);
    border-radius: var(--radius-xl);
    box-shadow: var(--glass-shadow-lg);
  }

  .chat-input-header {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
  }

  .chat-input-title {
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--primary-500);
    margin: 0;
    font-family: var(--font-inter);
  }

  .chat-input-subtitle {
    font-size: var(--text-sm);
    color: var(--neutral-400);
    margin: 0;
    font-family: var(--font-inter);
  }

  .chat-input-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .chat-input-wrapper {
    display: flex;
    gap: var(--space-3);
    align-items: flex-end;
  }

  .chat-input-textarea {
    flex: 1;
    min-height: 120px; /* 6 rows * 20px per row */
    padding: var(--space-3);
    background: var(--glass-surface-input);
    backdrop-filter: var(--glass-blur-sm);
    -webkit-backdrop-filter: var(--glass-blur-sm);
    border: var(--glass-border-subtle);
    border-radius: var(--radius-lg);
    color: var(--neutral-100);
    font-size: var(--text-base);
    font-family: var(--font-inter);
    resize: vertical;
    outline: none;
    transition: all 0.2s ease;
  }

  .chat-input-textarea:focus {
    border-color: var(--primary-500);
    box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.1);
  }

  .chat-input-textarea::placeholder {
    color: var(--neutral-400);
  }

  .chat-input-send-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: var(--primary-500);
    border: none;
    border-radius: var(--radius-lg);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .chat-input-send-button:hover:not(:disabled) {
    background: var(--primary-600);
    transform: translateY(-1px);
    box-shadow: var(--glass-shadow-lg);
  }

  .chat-input-send-button:disabled {
    background: var(--neutral-600);
    cursor: not-allowed;
    opacity: 0.5;
  }

  .chat-input-send-icon {
    width: 20px;
    height: 20px;
  }

  /* Ticker Input Container - BUTTON PROMPT STOCK TICKER */
  .ticker-input-container {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    padding: var(--space-4);
    background: var(--glass-surface-ticker);
    backdrop-filter: var(--glass-blur-md);
    -webkit-backdrop-filter: var(--glass-blur-md);
    border: var(--glass-border-highlight);
    border-radius: var(--radius-xl);
    box-shadow: var(--glass-shadow-lg);
  }

  .ticker-input-header {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
  }

  .ticker-input-title {
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--accent-500);
    margin: 0;
    font-family: var(--font-inter);
  }

  .ticker-input-subtitle {
    font-size: var(--text-sm);
    color: var(--neutral-400);
    margin: 0;
    font-family: var(--font-inter);
  }

  .ticker-input-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  .ticker-input-wrapper {
    display: flex;
    gap: var(--space-3);
    align-items: center;
  }

  .ticker-input-field {
    flex: 1;
    height: 48px;
    padding: var(--space-3);
    background: var(--glass-surface-input);
    backdrop-filter: var(--glass-blur-sm);
    -webkit-backdrop-filter: var(--glass-blur-sm);
    border: var(--glass-border-subtle);
    border-radius: var(--radius-lg);
    color: var(--neutral-100);
    font-size: var(--text-base);
    font-family: var(--font-inter);
    text-transform: uppercase;
    outline: none;
    transition: all 0.2s ease;
  }

  .ticker-input-field:focus {
    border-color: var(--accent-500);
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
  }

  .ticker-input-field::placeholder {
    color: var(--neutral-400);
    text-transform: none;
  }

  .ticker-input-field.invalid {
    border-color: var(--error-500);
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
  }

  .ticker-input-search-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: var(--accent-500);
    border: none;
    border-radius: var(--radius-lg);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .ticker-input-search-button:hover:not(:disabled) {
    background: var(--accent-600);
    transform: translateY(-1px);
    box-shadow: var(--glass-shadow-lg);
  }

  .ticker-input-search-button:disabled {
    background: var(--neutral-600);
    cursor: not-allowed;
    opacity: 0.5;
  }

  .ticker-input-search-icon {
    width: 20px;
    height: 20px;
  }

  .ticker-input-error {
    font-size: var(--text-sm);
    color: var(--error-500);
    margin-top: var(--space-1);
    font-family: var(--font-inter);
  }

  /* Mobile responsive adjustments for input components */
  @media (max-width: 767px) {
    .chat-input-container,
    .ticker-input-container {
      padding: var(--space-3);
    }

    .chat-input-title,
    .ticker-input-title {
      font-size: var(--text-base);
    }

    .chat-input-textarea {
      min-height: 100px; /* Reduced for mobile */
    }

    .chat-input-wrapper,
    .ticker-input-wrapper {
      gap: var(--space-2);
    }

    .chat-input-send-button,
    .ticker-input-search-button {
      width: 44px;
      height: 44px;
    }
  }

  /* Note: Component-specific styles are now included within each lazy-loaded component */
  /* Import SharedTickerInput styles for seamless integration */
  @import url('./SharedTickerInput.css');
`;
