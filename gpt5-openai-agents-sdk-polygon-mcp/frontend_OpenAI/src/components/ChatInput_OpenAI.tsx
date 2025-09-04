import { useState, useRef } from 'react';

interface ChatInput_OpenAIProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export default function ChatInput_OpenAI({
  onSendMessage,
  isLoading,
}: ChatInput_OpenAIProps) {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
      // Reset textarea height after clearing
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
    
    // Auto-resize logic
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <form onSubmit={handleSubmit} className='chat-input-form'>
      <div className='input-container'>
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder='Type your message... (Shift+Enter for new line)'
          className='message-input'
          disabled={isLoading}
          rows={4}
          style={{ minHeight: '80px', maxHeight: '200px' }}
        />
        <button
          type='submit'
          disabled={!inputValue.trim() || isLoading}
          className='send-button'
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
    border-radius: 16px;
    outline: none;
    font-size: 14px;
    resize: none;
    font-family: inherit;
    line-height: 1.4;
    min-height: 80px;
    max-height: 200px;
    overflow-y: auto;
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
