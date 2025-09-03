import { Message } from '../types/chat_OpenAI';

interface ChatMessage_OpenAIProps {
  message: Message;
}

export default function ChatMessage_OpenAI({ message }: ChatMessage_OpenAIProps) {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`}>
        <div className="message-content">
          {message.content}
        </div>
        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

// Simple inline styles - in production, use CSS modules or styled-components
export const messageStyles = `
  .message {
    display: flex;
    margin-bottom: 16px;
  }
  
  .user-message {
    justify-content: flex-end;
  }
  
  .ai-message {
    justify-content: flex-start;
  }
  
  .message-bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 16px;
    position: relative;
  }
  
  .user-bubble {
    background-color: #007bff;
    color: white;
  }
  
  .ai-bubble {
    background-color: #f1f1f1;
    color: #333;
  }
  
  .message-content {
    margin-bottom: 4px;
  }
  
  .message-timestamp {
    font-size: 0.75rem;
    opacity: 0.7;
  }
`;