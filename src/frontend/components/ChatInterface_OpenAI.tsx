import { useState, useRef, useEffect, Suspense, lazy } from 'react';

import { sendChatMessage } from '../services/api_OpenAI';
import { Message, MessageMetadata } from '../types/chat_OpenAI';
import { 
  useComponentLogger, 
  useStateLogger, 
  useInteractionLogger, 
  usePerformanceLogger,
  useRenderLogger 
} from '../hooks/useDebugLog';
import { logger } from '../utils/logger';

import ChatInput_OpenAI, { ChatInputRef } from './ChatInput_OpenAI';
import ChatMessage_OpenAI from './ChatMessage_OpenAI';
import DebugPanel from './DebugPanel';

// Lazy load secondary components for better performance
const ExportButtons = lazy(() =>
  import('./ExportButtons').then(module => ({ default: module.default }))
);
const RecentMessageButtons = lazy(() =>
  import('./RecentMessageButtons').then(module => ({ default: module.default }))
);
const AnalysisButtons = lazy(() =>
  import('./AnalysisButtons').then(module => ({ default: module.default }))
);

// Note: Styles are now included within each lazy-loaded component to prevent static imports
// that would break the lazy loading optimization

export default function ChatInterface_OpenAI() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState<string>('');
  const [sharedTicker, setSharedTicker] = useState<string>('NVDA');
  const [latestResponseTime, setLatestResponseTime] = useState<number | null>(null);

  // Initialize logging hooks
  useComponentLogger('ChatInterface_OpenAI', {
    initialMessageCount: messages.length,
    initialTicker: sharedTicker
  });
  
  // Safe state logging that prevents render loops
  useStateLogger('ChatInterface_OpenAI', 'messages', messages.length);
  useStateLogger('ChatInterface_OpenAI', 'isLoading', isLoading);
  useStateLogger('ChatInterface_OpenAI', 'error', error);
  useStateLogger('ChatInterface_OpenAI', 'sharedTicker', sharedTicker);
  
  // Performance tracking
  const { startTiming, endTiming } = usePerformanceLogger('ChatInterface_OpenAI');
  
  // User interaction logging
  const logInteraction = useInteractionLogger('ChatInterface_OpenAI');
  
  // Render cycle monitoring (helps detect infinite loops)
  useRenderLogger('ChatInterface_OpenAI', 15); // Warn if more than 15 renders in 5 seconds

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const statusRegionRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<ChatInputRef>(null);
  const isFirstRenderRef = useRef(true);
  const previousMessageCountRef = useRef(0);

  // Auto-scroll to bottom when new messages are added
  // FIXED: Only scroll when messages actually increase, not during loading states
  useEffect(() => {
    const currentMessageCount = messages.length;
    const shouldScroll = !isFirstRenderRef.current &&
                        currentMessageCount > previousMessageCountRef.current &&
                        !isLoading;

    logger.debug('🔄 Auto-scroll effect triggered', {
      component: 'ChatInterface_OpenAI',
      messagesCount: currentMessageCount,
      previousCount: previousMessageCountRef.current,
      isFirstRender: isFirstRenderRef.current,
      isLoading,
      shouldScroll,
      hasMessagesEndRef: !!messagesEndRef.current
    });

    if (shouldScroll && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
      logger.debug('📜 Scrolled to bottom of messages');
    }

    // Update refs
    isFirstRenderRef.current = false;
    previousMessageCountRef.current = currentMessageCount;
  }, [messages, isLoading]);

  const addMessage = (content: string, sender: 'user' | 'ai', metadata?: MessageMetadata) => {
    const messageId = Date.now().toString() + Math.random().toString(36).substr(2, 9);
    const newMessage: Message = {
      id: messageId,
      content,
      sender,
      timestamp: new Date(),
      metadata,
    };
    
    logger.info(`💬 Adding ${sender} message`, {
      component: 'ChatInterface_OpenAI',
      messageId,
      sender,
      contentLength: content.length,
      hasMetadata: !!metadata,
      messageCount: messages.length + 1
    });
    
    setMessages(prev => [...prev, newMessage]);
  };

  // Handle prompt population from analysis buttons
  const handlePromptGenerated = (prompt: string) => {
    logInteraction('prompt_generated', 'analysis_button', {
      promptLength: prompt.length,
      promptPreview: prompt.slice(0, 50) + (prompt.length > 50 ? '...' : '')
    });
    
    setInputValue(prompt);
    
    // Focus the input after populating
    if (chatInputRef.current) {
      chatInputRef.current.focus();
      logger.debug('🎯 Focused chat input after prompt generation');
    } else {
      logger.warn('⚠️ Could not focus chat input - ref not available');
    }
  };



  const handleSendMessage = async (messageContent: string) => {
    const messageId = Date.now().toString();
    
    logInteraction('send_message', 'chat_input', {
      messageLength: messageContent.length,
      messagePreview: messageContent.slice(0, 100) + (messageContent.length > 100 ? '...' : ''),
      messageId
    });
    
    // Start performance timing
    startTiming('message_processing');
    
    // Add user message immediately
    addMessage(messageContent, 'user');
    setIsLoading(true);
    setError(null);

    // Start timing for response tracking
    const startTime = Date.now();

    try {
      logger.group('🌐 API Request Processing');
      logger.info('Sending message to API', {
        messageId,
        contentLength: messageContent.length,
        timestamp: new Date().toISOString()
      });
      
      // Send to API and get response
      const aiResponse = await sendChatMessage(messageContent);
      const processingTime = (Date.now() - startTime) / 1000;
      
      logger.info('✅ API response received', {
        messageId,
        processingTime: `${processingTime.toFixed(2)}s`,
        responseLength: aiResponse.length
      });
      logger.groupEnd();
      
      setLatestResponseTime(processingTime);
      addMessage(aiResponse, 'ai', { processingTime });
      
      // End performance timing
      endTiming('message_processing');
      
    } catch (err) {
      const processingTime = (Date.now() - startTime) / 1000;
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      
      logger.group('❌ API Request Failed');
      logger.error('API request failed', {
        messageId,
        processingTime: `${processingTime.toFixed(2)}s`,
        errorType: err instanceof Error ? err.constructor.name : 'Unknown',
        errorMessage: errorMessage.slice(0, 200) + (errorMessage.length > 200 ? '...' : '')
      });
      logger.groupEnd();
      
      setError(errorMessage);
      setLatestResponseTime(processingTime);
      addMessage(`Error: ${errorMessage}`, 'ai', { processingTime, isError: true });
      
      // End performance timing even on error
      endTiming('message_processing');
      
    } finally {
      setIsLoading(false);
      
      logger.debug('🔄 Message processing completed', {
        messageId,
        finalState: {
          messageCount: messages.length + 2, // +1 for user, +1 for AI
          isLoading: false,
          hasError: !!error
        }
      });
    }
  };

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
                Get instant financial insights powered by AI. Use the ticker input and quick
                analysis tools below or type your own questions.
              </p>
              <p className='getting-started'>
                Start by entering a ticker symbol and using the analysis buttons, or type a message directly.
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
        {isLoading && (
          <div
            className='loading-indicator'
            role='status'
            aria-label='AI is typing'
          >
            <div className='typing-dots' aria-hidden='true'>
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className='sr-only'>AI is responding to your message</span>
          </div>
        )}
      </main>

      {/* SECTION 3: Chat Input */}
      <section className='chat-input-section' role='complementary' aria-label='Message input'>
        <div className='chat-input-container'>
          <ChatInput_OpenAI
            ref={chatInputRef}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            value={inputValue}
            onValueChange={setInputValue}
            placeholder={`Ask about ${sharedTicker} or any financial question... (Shift+Enter for new line)`}
          />
        </div>
      </section>

      {/* SECTION 4: Analysis Buttons (now includes integrated ticker input) */}
      <section className='analysis-buttons-section' role='complementary' aria-label='Quick analysis tools'>
        <Suspense
          fallback={
            <div className='component-loading analysis-loading'>
              Loading analysis tools...
            </div>
          }
        >
          <AnalysisButtons
            onPromptGenerated={handlePromptGenerated}
            currentTicker={sharedTicker}
            onTickerChange={(newTicker) => {
              logInteraction('ticker_change', 'analysis_buttons', {
                oldTicker: sharedTicker,
                newTicker,
                source: 'analysis_buttons'
              });
              setSharedTicker(newTicker);
            }}
            className='fixed-analysis-buttons'
          />
        </Suspense>
      </section>

      {/* SECTION 5: Export/Recent Buttons */}
      <section className='export-buttons-section' role='complementary' aria-label='Export and recent message functions'>
        {messages.length > 0 && (
          <div className='export-recent-container'>
            <Suspense
              fallback={
                <div className='component-loading'>Loading recent messages...</div>
              }
            >
              <RecentMessageButtons 
                messages={messages}
                onRecentMessageClick={(messageContent) => {
                  logInteraction('recent_message_click', 'recent_button', {
                    messageLength: messageContent.length,
                    messageCount: messages.length
                  });
                }}
              />
            </Suspense>
            <Suspense
              fallback={
                <div className='component-loading'>Loading export options...</div>
              }
            >
              <ExportButtons 
                messages={messages}
                onExport={(format, messageCount) => {
                  logInteraction('export_messages', 'export_button', {
                    format,
                    messageCount,
                    totalMessages: messages.length
                  });
                }}
              />
            </Suspense>
          </div>
        )}
      </section>

      {/* SECTION 6: Debug Panel */}
      <section className='debug-section' role='complementary' aria-label='Debug information'>
        <DebugPanel 
          latestResponseTime={latestResponseTime}
          className='main-debug-panel'
          onDebugAction={(action, details) => {
            logInteraction('debug_action', 'debug_panel', {
              action,
              ...details
            });
          }}
        />
      </section>
    </div>
  );
}

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
  
  /* SIX-SECTION LAYOUT: Professional Fintech Glassmorphic Implementation with Layout Stability */
  .chat-interface {
    display: grid;
    /* Stable grid rows using minmax() to prevent layout shifts during loading states */
    grid-template-rows: 
      minmax(70px, auto)    /* Header: stable minimum height */
      1fr                   /* Messages: flexible space for scrolling */
      minmax(90px, 150px)   /* Chat Input: stable height range */
      minmax(180px, 280px)  /* Analysis Buttons with Ticker: increased height range */
      minmax(70px, 120px)   /* Export Buttons: stable height range */
      minmax(80px, 120px);  /* Debug: stable height range */
    grid-template-areas: 
      "header"
      "messages"
      "chat-input"
      "buttons"
      "export-buttons"
      "debug";
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
  
  /* Mobile viewport optimizations with stable grid layout */
  @media (max-width: 767px) {
    .chat-interface {
      height: 100vh;
      height: 100svh; /* Small viewport height for mobile browsers */
      /* Mobile-optimized stable grid rows */
      grid-template-rows: 
        minmax(50px, auto)    /* Header: smaller mobile minimum */
        1fr                   /* Messages: flexible space */
        minmax(70px, 120px)   /* Chat Input: mobile-optimized range */
        minmax(150px, 240px)  /* Analysis Buttons with Ticker: mobile-optimized range */
        minmax(60px, 100px)   /* Export Buttons: mobile-optimized range */
        minmax(50px, 80px);   /* Debug: mobile-optimized range */
    }
  }
  
  /* SECTION 1: Header - Professional Fintech Glassmorphic Header with Blue Chat Theme */
  .chat-header {
    grid-area: header;
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
    transition: box-shadow var(--timing-base) var(--ease-out);
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
    grid-area: messages;
    overflow-y: auto;
    overflow-x: hidden; /* Prevent horizontal page scroll */
    padding: var(--space-4);
    width: 100%;
    max-width: 100%; /* Remove 800px limit for better mobile */
    margin: 0 auto;
    /* Enhanced focus management */
    scroll-behavior: smooth;
    min-height: 0; /* Allow shrinking in grid layout */
    /* Custom scrollbar for glassmorphic look */
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-400) transparent;
    /* Blue Chat Theme Enhancement - Tasks 4 & 6 */
    background: var(--glass-surface-chat);
    border-left: var(--border-chat);
    border-right: var(--border-chat);
    box-shadow: var(--border-glow-chat);
    transition: box-shadow var(--timing-base) var(--ease-out);
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
  
  .loading-indicator {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin: var(--space-4) 0;
    gap: var(--space-2);
  }
  
  .typing-dots {
    display: flex;
    align-items: center;
    gap: var(--space-1);
    padding: var(--space-3) var(--space-4);
    background: var(--glass-surface-light);
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
    border: var(--glass-border-highlight);
    border-radius: var(--radius-2xl);
  }
  
  .typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--primary-400);
    animation: typing 1.4s infinite ease-in-out;
  }
  
  .typing-dots span:nth-child(1) {
    animation-delay: -0.32s;
  }
  
  .typing-dots span:nth-child(2) {
    animation-delay: -0.16s;
  }
  
  @keyframes typing {
    0%, 80%, 100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }
  
  /* SECTION 3: Chat Input - Professional glassmorphic input section with Blue Chat Theme */
  .chat-input-section {
    grid-area: chat-input;
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
    transition: box-shadow var(--timing-base) var(--ease-out);
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
  
  /* SECTION 4: Analysis Buttons with Integrated Ticker - Professional glassmorphic analysis tools with Purple Analysis Theme */
  .analysis-buttons-section {
    grid-area: buttons;
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
    transition: box-shadow var(--timing-base) var(--ease-out);
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
    grid-area: export-buttons;
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
    transition: box-shadow var(--timing-base) var(--ease-out);
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
    grid-area: debug;
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
    transition: box-shadow var(--timing-base) var(--ease-out);
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
  
  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .messages-section {
      scroll-behavior: auto;
    }
    
    .typing-dots span {
      animation: none;
    }
    
    .chat-interface {
      transition: none;
    }
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
    transition: background-color 0.2s ease;
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
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid var(--neutral-600);
    border-top: 2px solid var(--primary-400);
    border-radius: 50%;
    animation: component-loading-spin 1s linear infinite;
    margin-right: var(--space-2);
    flex-shrink: 0;
  }

  @keyframes component-loading-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
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
  
  /* Reduced motion support - DARK MODE */
  @media (prefers-reduced-motion: reduce) {
    .component-loading::before {
      animation: none;
      border: 2px solid #63b3ed; /* Light blue for dark mode */
    }
    
    .chat-input-section,
    .ticker-input-section,
    .analysis-buttons-section,
    .export-buttons-section,
    .debug-section {
      transition: none;
    }
  }
  
  /* Note: Component-specific styles are now included within each lazy-loaded component */
  /* Import SharedTickerInput styles for seamless integration */
  @import url('./SharedTickerInput.css');
`;
