import { useState } from 'react';

interface ChatInput_OpenAIProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export default function ChatInput_OpenAI({ onSendMessage, isLoading }: ChatInput_OpenAIProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message..."
          className="message-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </form>
  );
}

// Simple inline styles - in production, use CSS modules or styled-components
export const inputStyles = `
  .chat-input-form {
    padding: 16px;
    background: white;
    border-top: 1px solid #e0e0e0;
  }
  
  .input-container {
    display: flex;
    gap: 8px;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .message-input {
    flex: 1;
    padding: 12px 16px;
    border: 1px solid #ddd;
    border-radius: 24px;
    outline: none;
    font-size: 14px;
  }
  
  .message-input:focus {
    border-color: #007bff;
  }
  
  .message-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .send-button {
    padding: 12px 24px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 24px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
  }
  
  .send-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .send-button:not(:disabled):hover {
    background-color: #0056b3;
  }
`;