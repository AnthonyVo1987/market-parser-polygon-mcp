import { useState, useRef, useEffect } from 'react';

import { sendChatMessage } from '../services/api_OpenAI';
import { Message } from '../types/chat_OpenAI';

import ChatInput_OpenAI from './ChatInput_OpenAI';
import ChatMessage_OpenAI from './ChatMessage_OpenAI';
import ExportButtons, { exportButtonStyles } from './ExportButtons';
import RecentMessageButtons, { recentMessageButtonsStyles } from './RecentMessageButtons';

export default function ChatInterface_OpenAI() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const statusRegionRef = useRef<HTMLDivElement>(null);

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
    <div className='chat-interface' role='application' aria-label='OpenAI Chat Interface'>
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
        {messages.length > 0 && <ExportButtons messages={messages} />}
        <RecentMessageButtons messages={messages} />
        {error && (
          <div className='error-banner' role='alert' aria-describedby='chat-title'>
            {error}
          </div>
        )}
      </header>

      <main className='messages-container' role='log' aria-live='polite' aria-label='Chat conversation'>
        {messages.length === 0 ? (
          <div className='empty-state' role='status'>
            <p>Start a conversation by typing a message below.</p>
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
          <div className='loading-indicator' role='status' aria-label='AI is typing'>
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
        <ChatInput_OpenAI
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
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
  }
  
  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #666;
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
  
  ${exportButtonStyles}
  ${recentMessageButtonsStyles}
`;
