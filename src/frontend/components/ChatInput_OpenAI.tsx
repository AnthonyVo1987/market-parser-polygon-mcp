import type { ChangeEvent, FormEvent, KeyboardEvent } from 'react';
import { FC, memo, useCallback, useEffect, useState } from 'react';
import { ChatInputProps } from '../types';
import { getChatPlaceholder } from '../utils/placeholderText';
import AIModelSelector, { modelSelectorStyles } from './AIModelSelector';

const ChatInput_OpenAI: FC<ChatInputProps> = memo(
  ({
    onSendMessage,
    disabled = false,
    placeholder,
    value = '',
    onChange,
    selectedModel,
    onModelChange,
    models = [],
    modelLoading = false,
    modelError = null
  }) => {
    const [isComposing, setIsComposing] = useState(false);

    // Enhanced placeholder text based on user state
    const dynamicPlaceholder =
      placeholder || getChatPlaceholder(disabled ? 'loading' : 'idle');

    // Simple state management without validation
    const [message, setMessage] = useState(value);

    // Sync with parent component value
    useEffect(() => {
      setMessage(value);
    }, [value]);

    const handleSubmit = useCallback(
      (e: FormEvent) => {
        e.preventDefault();
        if (message.trim() && !disabled && !isComposing) {
          onSendMessage(message.trim(), selectedModel);
          // Note: Parent component handles clearing the input via onChange
        }
      },
      [message, onSendMessage, disabled, isComposing, selectedModel]
    );

    const handleKeyDown = useCallback(
      (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey && !isComposing) {
          e.preventDefault();
          handleSubmit(e);
        }
      },
      [handleSubmit, isComposing]
    );

    const handleCompositionStart = useCallback(() => {
      setIsComposing(true);
    }, []);

    const handleCompositionEnd = useCallback(() => {
      setIsComposing(false);
    }, []);

    const handleChange = useCallback(
      (e: ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(e.target.value);
        if (onChange) {
          onChange(e.target.value);
        }
      },
      [onChange]
    );

    return (
      <div className='chat-input-container' data-testid='chat-input'>
        <form onSubmit={handleSubmit} className='chat-input-form'>
          <div className='chat-input-wrapper'>
            <textarea
              value={message}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              onCompositionStart={handleCompositionStart}
              onCompositionEnd={handleCompositionEnd}
              placeholder={dynamicPlaceholder}
              disabled={disabled}
              className='chat-input-textarea'
              rows={3}
              data-testid='chat-input-textarea'
              aria-label='AI Chatbot Input - Type your financial questions here'
              aria-describedby='chat-input-character-count'
              aria-required='true'
              role='textbox'
              aria-multiline='true'
              maxLength={2000}
            />
            <div className='chat-input-controls'>
              {models.length > 0 && onModelChange && (
                <AIModelSelector
                  models={models}
                  currentModel={selectedModel || 'gpt-5-nano'}
                  onModelChange={onModelChange}
                  loading={modelLoading}
                  error={modelError}
                  disabled={disabled}
                />
              )}
              <button
                type='submit'
                disabled={disabled || !message.trim() || isComposing}
                className='chat-input-send-button'
                data-testid='chat-input-send-button'
                aria-label='Send message to AI chatbot'
              >
                <svg
                  className='chat-input-send-icon'
                  viewBox='0 0 24 24'
                  fill='none'
                  xmlns='http://www.w3.org/2000/svg'
                >
                  <path
                    d='M2.01 21L23 12 2.01 3 2 10l15 2-15 2z'
                    fill='currentColor'
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Character count display */}
          <div
            id='chat-input-character-count'
            className='chat-input-character-count'
            data-testid='chat-input-character-count'
            aria-live='polite'
            aria-label={`Character count: ${message.length} of 2000 characters`}
          >
            {message.length}/2000 characters
          </div>
        </form>
      </div>
    );
  }
);

ChatInput_OpenAI.displayName = 'ChatInput_OpenAI';

export default ChatInput_OpenAI;

// Enhanced styles for chat input with AI model selector
export const chatInputStyles = `
  .chat-input-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
    max-width: 1000px;
    margin: 0 auto;
  }

  .chat-input-form {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }

  .chat-input-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
  }

  .chat-input-textarea {
    width: 100%;
    min-height: 80px;
    padding: 12px 16px;
    border: 1px solid var(--glass-border-highlight);
    border-radius: var(--radius-lg);
    background: var(--glass-surface-light);
    color: var(--neutral-100);
    font-size: 14px;
    font-family: var(--font-inter);
    resize: vertical;
    transition: all 0.2s ease;
  }

  .chat-input-textarea:focus {
    outline: none;
    border-color: var(--primary-500);
    box-shadow: 0 0 0 2px rgba(99, 179, 237, 0.2);
  }

  .chat-input-textarea:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: var(--glass-surface-dark);
  }

  .chat-input-controls {
    display: flex;
    align-items: center;
    gap: 12px;
    justify-content: space-between;
    width: 100%;
  }

  .chat-input-send-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border: none;
    border-radius: var(--radius-lg);
    background: var(--primary-600);
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .chat-input-send-button:hover:not(:disabled) {
    background: var(--primary-700);
    transform: translateY(-1px);
  }

  .chat-input-send-button:active:not(:disabled) {
    transform: translateY(0);
  }

  .chat-input-send-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: var(--neutral-600);
  }

  .chat-input-send-icon {
    width: 20px;
    height: 20px;
  }

  .chat-input-character-count {
    font-size: 12px;
    color: var(--neutral-400);
    text-align: right;
    font-family: var(--font-inter);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .chat-input-controls {
      gap: 8px;
    }

    .chat-input-send-button {
      width: 44px;
      height: 44px;
    }

    .chat-input-send-icon {
      width: 18px;
      height: 18px;
    }

    .chat-input-textarea {
      min-height: 70px;
      padding: 10px 12px;
      font-size: 13px;
    }
  }

  /* Include model selector styles */
  ${modelSelectorStyles}
`;
