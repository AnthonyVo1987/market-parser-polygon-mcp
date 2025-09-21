import { ChangeEvent, FC, FormEvent, KeyboardEvent, useCallback, useState } from 'react';

import { ChatInputProps } from '../types';

const ChatInput_OpenAI: FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Ask any financial question or request analysis..."
}) => {
  const [message, setMessage] = useState('');

  const handleSubmit = useCallback((e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
    }
  }, [message, onSendMessage, disabled]);

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as FormEvent);
    }
  }, [handleSubmit]);

  return (
    <div className="ai-chatbot-input-container" data-testid="ai-chatbot-input-container">
      <label htmlFor="ai-chatbot-input" className="ai-chatbot-label">
        AI CHATBOT INPUT
        <span className="required-indicator" aria-hidden="true">*</span>
      </label>
      <form onSubmit={handleSubmit} className="ai-chatbot-form">
        <textarea
          id="ai-chatbot-input"
          value={message}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={6}
          placeholder={placeholder}
          className="ai-chatbot-input"
          disabled={disabled}
          aria-label="AI Chatbot Input - Ask any financial question"
          aria-describedby="ai-input-help"
          data-testid="ai-chatbot-input"
        />
        <div id="ai-input-help" className="ai-input-help">
          Press Enter to send, Shift+Enter for new line
        </div>
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="ai-chatbot-send-button"
          data-testid="ai-chatbot-send-button"
          aria-label="Send message to AI chatbot"
        >
          Send Message
        </button>
      </form>
    </div>
  );
};

export default ChatInput_OpenAI;
