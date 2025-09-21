import React, { 
  useState, 
  useCallback, 
  useEffect, 
  useMemo, 
  useId,
  FC,
  ComponentType,
  ReactNode,
  JSX
} from 'react';
import type { 
  FormEvent, 
  KeyboardEvent, 
  ChangeEvent 
} from 'react';
import { ChatInputProps } from '../types';

const ChatInput_OpenAI: FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Type your message here..."
}) => {
  const [message, setMessage] = useState('');
  const [isComposing, setIsComposing] = useState(false);

  const handleSubmit = useCallback((e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled && !isComposing) {
      onSendMessage(message.trim());
      setMessage('');
    }
  }, [message, onSendMessage, disabled, isComposing]);

  const handleKeyDown = useCallback((e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey && !isComposing) {
      e.preventDefault();
      handleSubmit(e);
    }
  }, [handleSubmit, isComposing]);

  const handleCompositionStart = useCallback(() => {
    setIsComposing(true);
  }, []);

  const handleCompositionEnd = useCallback(() => {
    setIsComposing(false);
  }, []);

  const handleChange = useCallback((e: ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
  }, []);

  return (
    <div className="chat-input-container" data-testid="chat-input">
      <div className="chat-input-header">
        <h3 className="chat-input-title">AI CHATBOT INPUT</h3>
        <div className="chat-input-subtitle">Type your financial questions here</div>
      </div>
      
      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="chat-input-wrapper">
          <textarea
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onCompositionStart={handleCompositionStart}
            onCompositionEnd={handleCompositionEnd}
            placeholder={placeholder}
            disabled={disabled}
            className="chat-input-textarea"
            rows={6}
            data-testid="chat-input-textarea"
            aria-label="AI Chatbot Input - Type your financial questions here"
          />
          <button
            type="submit"
            disabled={disabled || !message.trim() || isComposing}
            className="chat-input-send-button"
            data-testid="chat-input-send-button"
            aria-label="Send message to AI chatbot"
          >
            <svg
              className="chat-input-send-icon"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInput_OpenAI;