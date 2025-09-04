import {
  useState,
  useRef,
  useImperativeHandle,
  forwardRef,
  useEffect,
} from 'react';

interface ChatInput_OpenAIProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  value?: string;
  onValueChange?: (value: string) => void;
  placeholder?: string;
}

export interface ChatInputRef {
  focus: () => void;
  setValue: (value: string) => void;
  getValue: () => string;
  clear: () => void;
}

const ChatInput_OpenAI = forwardRef<ChatInputRef, ChatInput_OpenAIProps>(
  function ChatInput_OpenAI(
    {
      onSendMessage,
      isLoading,
      value: externalValue,
      onValueChange,
      placeholder = 'Type your message... (Shift+Enter for new line)',
    },
    ref
  ) {
    const [internalValue, setInternalValue] = useState('');

    // Use external value if provided, otherwise use internal state
    const inputValue =
      externalValue !== undefined ? externalValue : internalValue;

    // Update internal state when external value changes
    useEffect(() => {
      if (externalValue !== undefined) {
        setInternalValue(externalValue);
      }
    }, [externalValue]);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      if (inputValue.trim() && !isLoading) {
        onSendMessage(inputValue.trim());

        // Clear value based on control mode
        if (externalValue !== undefined && onValueChange) {
          onValueChange('');
        } else {
          setInternalValue('');
        }
        // Reset textarea height after clearing
        if (textareaRef.current) {
          textareaRef.current.style.height = 'auto';
        }
      }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = e.target.value;

      // Update appropriate state based on control mode
      if (externalValue !== undefined && onValueChange) {
        onValueChange(newValue);
      } else {
        setInternalValue(newValue);
      }

      // Auto-resize logic
      const textarea = e.target;
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        // Create a synthetic form event for handleSubmit
        const syntheticEvent = {
          preventDefault: () => {},
          target: e.target,
          currentTarget: e.target,
        } as React.FormEvent;
        handleSubmit(syntheticEvent);
      }
    };

    // Expose imperative methods to parent components
    useImperativeHandle(
      ref,
      () => ({
        focus: () => {
          if (textareaRef.current) {
            textareaRef.current.focus();
          }
        },
        setValue: (value: string) => {
          if (externalValue !== undefined && onValueChange) {
            onValueChange(value);
          } else {
            setInternalValue(value);
          }
          // Auto-resize after setting value
          if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height =
              Math.min(textareaRef.current.scrollHeight, 200) + 'px';
          }
        },
        getValue: () => inputValue,
        clear: () => {
          if (externalValue !== undefined && onValueChange) {
            onValueChange('');
          } else {
            setInternalValue('');
          }
          // Reset textarea height after clearing
          if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
          }
        },
      }),
      [inputValue, externalValue, onValueChange]
    );

    return (
      <form
        onSubmit={handleSubmit}
        className='chat-input-form'
        role='form'
        aria-label='Send message'
      >
        <div className='input-container'>
          <label htmlFor='main-input' className='sr-only'>
            Type your message here. Press Shift+Enter for new line, Enter to
            send.
          </label>
          <textarea
            id='main-input'
            ref={textareaRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className='message-input'
            disabled={isLoading}
            rows={4}
            style={{ minHeight: '80px', maxHeight: '200px' }}
            aria-describedby='input-help'
            aria-label='Message input'
            required
          />
          <div id='input-help' className='sr-only'>
            {isLoading
              ? 'Please wait while your message is being sent'
              : 'Enter your message and press Enter to send, or Shift+Enter for a new line'}
          </div>
          <button
            type='submit'
            disabled={!inputValue.trim() || isLoading}
            className='send-button'
            aria-describedby='send-help'
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
          <div id='send-help' className='sr-only'>
            {!inputValue.trim()
              ? 'Enter a message to enable sending'
              : isLoading
                ? 'Message is being sent'
                : 'Send your message'}
          </div>
        </div>
      </form>
    );
  }
);

export default ChatInput_OpenAI;

// Enhanced inline styles with accessibility improvements
export const inputStyles = `
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
    transition: border-color 0.2s ease;
  }
  
  .message-input:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }
  
  .message-input:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
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
    transition: background-color 0.2s ease, transform 0.1s ease;
    min-width: 80px;
  }
  
  .send-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  .send-button:not(:disabled):hover {
    background-color: #0056b3;
    transform: translateY(-1px);
  }
  
  .send-button:not(:disabled):active {
    transform: translateY(0);
  }
  
  .send-button:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
  }
  
  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .message-input {
      border: 2px solid;
    }
    
    .send-button {
      border: 2px solid;
    }
  }
  
  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .message-input,
    .send-button {
      transition: none;
    }
    
    .send-button:not(:disabled):hover {
      transform: none;
    }
  }
`;
