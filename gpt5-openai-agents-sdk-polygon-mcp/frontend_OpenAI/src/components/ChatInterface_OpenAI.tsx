import { useState } from 'react';

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
    <div className='chat-interface'>
      <div className='chat-header'>
        <h1>OpenAI Chat Interface</h1>
        {messages.length > 0 && <ExportButtons messages={messages} />}
        <RecentMessageButtons messages={messages} />
        {error && <div className='error-banner'>{error}</div>}
      </div>

      <div className='messages-container'>
        {messages.length === 0 ? (
          <div className='empty-state'>
            <p>Start a conversation by typing a message below.</p>
          </div>
        ) : (
          messages.map(message => (
            <ChatMessage_OpenAI key={message.id} message={message} />
          ))
        )}
        {isLoading && (
          <div className='loading-indicator'>
            <div className='typing-dots'>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>

      <ChatInput_OpenAI
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}

// Enhanced responsive styles for cross-platform UI optimization
export const interfaceStyles = `
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
    margin: 16px 0;
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
  
  ${exportButtonStyles}
  ${recentMessageButtonsStyles}
`;
