import { useState, useRef, useEffect, Suspense, lazy } from 'react';

import { sendChatMessage } from '../services/api_OpenAI';
import { Message } from '../types/chat_OpenAI';

import ChatInput_OpenAI, { ChatInputRef } from './ChatInput_OpenAI';
import ChatMessage_OpenAI from './ChatMessage_OpenAI';

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
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const statusRegionRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<ChatInputRef>(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const addMessage = (content: string, sender: 'user' | 'ai') => {
    const newMessage: Message = {
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      content,
      sender,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  // Handle prompt population from analysis buttons
  const handlePromptGenerated = (prompt: string) => {
    setInputValue(prompt);
    // Focus the input after populating
    if (chatInputRef.current) {
      chatInputRef.current.focus();
    }
  };

  const handleSendMessage = async (messageContent: string) => {
    // Add user message immediately
    addMessage(messageContent, 'user');
    setIsLoading(true);
    setError(null);

    try {
      // Send to API and get response
      const aiResponse = await sendChatMessage(messageContent);
      addMessage(aiResponse, 'ai');
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      addMessage(`Error: ${errorMessage}`, 'ai');
    } finally {
      setIsLoading(false);
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

      <header className='chat-header' role='banner'>
        <h1 id='chat-title'>OpenAI Chat Interface</h1>
        {messages.length > 0 && (
          <Suspense
            fallback={
              <div className='component-loading'>Loading export options...</div>
            }
          >
            <ExportButtons messages={messages} />
          </Suspense>
        )}
        <Suspense
          fallback={
            <div className='component-loading'>Loading recent messages...</div>
          }
        >
          <RecentMessageButtons messages={messages} />
        </Suspense>
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

      <main
        className='messages-container'
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
                Get instant financial insights powered by AI. Use the quick
                analysis tools below or type your own questions.
              </p>
              {/* Analysis buttons for empty state */}
              <Suspense
                fallback={
                  <div className='component-loading'>
                    Loading analysis tools...
                  </div>
                }
              >
                <AnalysisButtons
                  onPromptGenerated={handlePromptGenerated}
                  className='welcome-buttons'
                />
              </Suspense>
              <p className='getting-started'>
                Or start typing a message in the input field below.
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

      <div role='complementary' className='chat-input-section'>
        {/* Analysis buttons for active conversation */}
        {messages.length > 0 && (
          <Suspense
            fallback={
              <div className='component-loading'>Loading analysis tools...</div>
            }
          >
            <AnalysisButtons
              onPromptGenerated={handlePromptGenerated}
              className='conversation-buttons'
            />
          </Suspense>
        )}

        <ChatInput_OpenAI
          ref={chatInputRef}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          value={inputValue}
          onValueChange={setInputValue}
          placeholder={
            messages.length === 0
              ? 'Ask about stocks, earnings, or market trends... (Shift+Enter for new line)'
              : 'Type your message... (Shift+Enter for new line)'
          }
        />
      </div>
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
  
  .chat-interface {
    display: flex;
    flex-direction: column;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile */
    background-color: #f5f5f5;
    overflow: hidden; /* Prevent page-level scrolling */
  }
  
  /* Mobile viewport optimizations */
  @media (max-width: 767px) {
    .chat-interface {
      height: 100vh;
      height: 100svh; /* Small viewport height for mobile browsers */
    }
  }
  
  .chat-header {
    position: relative;
  }
  
  .chat-header {
    background: white;
    padding: 16px;
    border-bottom: 1px solid #e0e0e0;
    text-align: center;
    flex-shrink: 0; /* Prevent header compression */
  }
  
  /* Mobile header adjustments */
  @media (max-width: 767px) {
    .chat-header {
      padding: 12px 8px;
    }
    
    .chat-header h1 {
      font-size: 1.25rem;
      margin: 0 0 8px 0;
    }
  }
  
  .chat-header h1 {
    margin: 0 0 8px 0;
    font-size: 1.5rem;
    color: #333;
  }
  
  .error-banner {
    background-color: #fee;
    color: #c33;
    padding: 8px 16px;
    margin-top: 8px;
    border-radius: 4px;
    font-size: 0.875rem;
  }
  
  .messages-container {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden; /* Prevent horizontal page scroll */
    padding: 16px;
    width: 100%;
    max-width: 100%; /* Remove 800px limit for better mobile */
    margin: 0 auto;
    /* Enhanced focus management */
    scroll-behavior: smooth;
  }
  
  .messages-container:focus {
    outline: 2px solid #007bff;
    outline-offset: -2px;
  }
  
  /* Mobile-specific adjustments */
  @media (max-width: 767px) {
    .messages-container {
      padding: 8px;
      max-width: 100vw;
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
    .messages-container {
      max-width: 900px;
      padding: 20px;
    }
  }
  
  /* Desktop optimizations */
  @media (min-width: 1025px) {
    .messages-container {
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
    color: #666;
    padding: 20px;
  }
  
  .welcome-content {
    text-align: center;
    max-width: 600px;
    width: 100%;
  }
  
  .welcome-title {
    margin: 0 0 12px 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
  
  .welcome-description {
    margin: 0 0 24px 0;
    font-size: 16px;
    line-height: 1.5;
    color: #666;
  }
  
  .welcome-buttons {
    margin: 0 0 24px 0;
  }
  
  .getting-started {
    margin: 0;
    font-size: 14px;
    color: #888;
    font-style: italic;
  }
  
  .loading-indicator {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    margin: 16px 0;
    gap: 8px;
  }
  
  .typing-dots {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 12px 16px;
    background-color: #f1f1f1;
    border-radius: 16px;
  }
  
  .typing-dots span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #999;
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
  
  /* Chat input section styling */
  .chat-input-section {
    flex-shrink: 0;
  }
  
  .conversation-buttons {
    border-bottom: 1px solid #e0e0e0;
    border-radius: 0;
    margin: 0;
  }
  
  /* Enhanced compatibility with multi-line input */
  .chat-input-form {
    padding: 16px;
    background: white;
    border-top: 1px solid #e0e0e0;
    flex-shrink: 0; /* Prevent input compression */
  }
  
  /* Mobile input adjustments */
  @media (max-width: 767px) {
    .chat-input-form {
      padding: 12px 8px;
    }
    
    .input-container {
      max-width: 100%;
      gap: 6px;
    }
  }
  
  /* Tablet and desktop input optimizations */
  @media (min-width: 768px) {
    .chat-input-form {
      padding: 20px;
    }
    
    .input-container {
      max-width: 1000px;
    }
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
  
  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .messages-container {
      scroll-behavior: auto;
    }
    
    .typing-dots span {
      animation: none;
    }
  }
  
  /* Focus visible improvements */
  .chat-interface *:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
  }

  /* Component loading states */
  .component-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    color: #666;
    font-size: 13px;
    font-style: italic;
    background: #f8f9fa;
    border-radius: 8px;
    margin: 8px 0;
    min-height: 40px;
    border: 1px solid #e9ecef;
  }

  .component-loading::before {
    content: '';
    width: 16px;
    height: 16px;
    border: 2px solid #e9ecef;
    border-top: 2px solid #007bff;
    border-radius: 50%;
    animation: component-loading-spin 1s linear infinite;
    margin-right: 8px;
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

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .component-loading::before {
      animation: none;
      border: 2px solid #007bff;
    }
  }
  
  /* Note: Component-specific styles are now included within each lazy-loaded component */
`;
