import type { ChangeEvent, FormEvent, KeyboardEvent } from 'react';
import { FC, memo, useCallback, useEffect, useState } from 'react';
import { useInputValidation } from '../hooks/useInputValidation';
import { ChatInputProps } from '../types';
import { getChatPlaceholder } from '../utils/placeholderText';
import { ValidationRule } from '../utils/validation';

const ChatInput_OpenAI: FC<ChatInputProps> = memo(
  ({ onSendMessage, disabled = false, placeholder, value = '', onChange }) => {
    const [isComposing, setIsComposing] = useState(false);

    // Enhanced placeholder text based on user state
    const dynamicPlaceholder =
      placeholder || getChatPlaceholder(disabled ? 'loading' : 'idle');

    // Enhanced validation rules for chat input
    const validationRules: ValidationRule = {
      required: true,
      minLength: 1,
      maxLength: 2000,
      pattern: /^[\s\S]*$/, // Allow any characters including newlines
    };

    // Use enhanced validation hook
    const {
      value: message,
      setValue: setMessage,
      isTouched,
      isValid,
      errorMessage,
      handleChange: handleValidationChange,
      handleBlur,
      handleFocus,
    } = useInputValidation({
      rules: validationRules,
      initialValue: value,
      validateOnChange: true,
      validateOnBlur: true,
    });

    // Sync with parent component value
    useEffect(() => {
      setMessage(value);
    }, [value, setMessage]);

    const handleSubmit = useCallback(
      (e: FormEvent) => {
        e.preventDefault();
        if (message.trim() && !disabled && !isComposing && isValid) {
          onSendMessage(message.trim());
          // Note: Parent component handles clearing the input via onChange
        }
      },
      [message, onSendMessage, disabled, isComposing, isValid]
    );

    const handleKeyDown = useCallback(
      (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey && !isComposing && isValid) {
          e.preventDefault();
          handleSubmit(e);
        }
      },
      [handleSubmit, isComposing, isValid]
    );

    const handleCompositionStart = useCallback(() => {
      setIsComposing(true);
    }, []);

    const handleCompositionEnd = useCallback(() => {
      setIsComposing(false);
    }, []);

    const handleChange = useCallback(
      (e: ChangeEvent<HTMLTextAreaElement>) => {
        handleValidationChange(e);
        if (onChange) {
          onChange(e.target.value);
        }
      },
      [handleValidationChange, onChange]
    );

    return (
      <div className='chat-input-container' data-testid='chat-input'>
        <div className='chat-input-header'>
          <h3 className='chat-input-title'>AI CHATBOT INPUT</h3>
          <div className='chat-input-subtitle'>
            Type your financial questions here
          </div>
        </div>

        <form onSubmit={handleSubmit} className='chat-input-form'>
          <div className='chat-input-wrapper'>
            <textarea
              value={message}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              onCompositionStart={handleCompositionStart}
              onCompositionEnd={handleCompositionEnd}
              onBlur={handleBlur}
              onFocus={handleFocus}
              placeholder={dynamicPlaceholder}
              disabled={disabled}
              className={`chat-input-textarea ${
                isTouched && !isValid ? 'chat-input-textarea--invalid' : ''
              } ${isTouched && isValid ? 'chat-input-textarea--valid' : ''}`}
              rows={6}
              data-testid='chat-input-textarea'
              aria-label='AI Chatbot Input - Type your financial questions here'
              aria-invalid={isTouched && !isValid}
              aria-describedby={
                isTouched && !isValid
                  ? 'chat-input-error'
                  : 'chat-input-character-count'
              }
              aria-required='true'
              role='textbox'
              aria-multiline='true'
              maxLength={2000}
            />
            <button
              type='submit'
              disabled={disabled || !message.trim() || isComposing || !isValid}
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

          {/* Enhanced validation error display */}
          {isTouched && !isValid && errorMessage && (
            <div
              id='chat-input-error'
              className='chat-input-error'
              data-testid='chat-input-error'
              role='alert'
              aria-live='polite'
            >
              {errorMessage}
            </div>
          )}

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
