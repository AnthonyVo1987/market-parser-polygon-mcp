import {
  forwardRef,
  memo,
  startTransition,
  useCallback,
  useEffect,
  useImperativeHandle,
  useRef,
  useState,
} from 'react';
import { useComponentLogger } from '../hooks/useDebugLog';
import { logger } from '../utils/logger';

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

const ChatInput_OpenAI = memo(forwardRef<ChatInputRef, ChatInput_OpenAIProps>(
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
    const [isFocused, setIsFocused] = useState(false);
    const [hasError, setHasError] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);

    // Initialize logging
    useComponentLogger('ChatInput_OpenAI', { placeholder });
    // const _logInteraction = useInteractionLogger('ChatInput_OpenAI');

    // Use external value if provided, otherwise use internal state
    const inputValue =
      externalValue !== undefined ? externalValue : internalValue;

    // Update internal state when external value changes
    useEffect(() => {
      if (externalValue !== undefined) {
        logger.debug('📝 External value updated', {
          component: 'ChatInput_OpenAI',
          newValueLength: externalValue.length,
          hasContent: externalValue.length > 0
        });
        setInternalValue(externalValue);
      }
    }, [externalValue]);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = useCallback((e: React.FormEvent) => {
      e.preventDefault();

      // Clear any existing error state
      setHasError(false);

      if (inputValue.trim() && !isLoading) {
        // Show success feedback
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 500);

        onSendMessage(inputValue.trim());

        // Immediate clear for instant UI feedback
        if (externalValue !== undefined && onValueChange) {
          onValueChange('');
        } else {
          setInternalValue('');
        }

        // Use startTransition for non-critical height reset
        startTransition(() => {
          if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
          }
        });
      } else if (!inputValue.trim()) {
        // Show error feedback for empty submission
        setHasError(true);
        setTimeout(() => setHasError(false), 600);
      }
    }, [inputValue, isLoading, onSendMessage, externalValue, onValueChange]);

    const handleInputChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = e.target.value;

      // Immediate state updates for instant UI responsiveness
      setHasError(prev => prev ? false : prev);

      // Update appropriate state immediately - no debouncing for <16ms responsiveness
      if (externalValue !== undefined && onValueChange) {
        onValueChange(newValue);
      } else {
        setInternalValue(newValue);
      }

      // Use startTransition for non-critical auto-resize calculations
      const textarea = e.target;
      startTransition(() => {
        // Auto-resize logic deferred to not block input responsiveness
        const previousHeight = textarea.style.height;
        textarea.style.height = 'auto';
        const newHeight = Math.min(textarea.scrollHeight, 200) + 'px';

        if (previousHeight !== newHeight) {
          textarea.style.height = newHeight;
        }
      });
    }, [externalValue, onValueChange]);

    const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        // Create a synthetic form event for handleSubmit
        const syntheticEvent = {
          preventDefault: () => { },
          target: e.target,
          currentTarget: e.target,
        } as React.FormEvent;
        handleSubmit(syntheticEvent);
      }
    }, [handleSubmit]);

    // Enhanced focus handlers for smooth transitions
    const handleFocus = useCallback(() => {
      setIsFocused(true);
    }, []);

    const handleBlur = useCallback(() => {
      setIsFocused(false);
    }, []);

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
          // Immediate state update for instant responsiveness
          if (externalValue !== undefined && onValueChange) {
            onValueChange(value);
          } else {
            setInternalValue(value);
          }

          // Use startTransition for non-critical auto-resize
          startTransition(() => {
            if (textareaRef.current) {
              textareaRef.current.style.height = 'auto';
              textareaRef.current.style.height =
                Math.min(textareaRef.current.scrollHeight, 200) + 'px';
            }
          });
        },
        getValue: () => inputValue,
        clear: () => {
          // Immediate state clear for instant responsiveness
          if (externalValue !== undefined && onValueChange) {
            onValueChange('');
          } else {
            setInternalValue('');
          }

          // Use startTransition for non-critical height reset
          startTransition(() => {
            if (textareaRef.current) {
              textareaRef.current.style.height = 'auto';
            }
          });
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
            onFocus={handleFocus}
            onBlur={handleBlur}
            placeholder={placeholder}
            className={`message-input ${isFocused ? 'input-focused' : ''
              } ${hasError ? 'input-error' : ''
              } ${showSuccess ? 'input-success' : ''
              }`}
            disabled={isLoading}
            rows={4}
            style={{ minHeight: '80px', maxHeight: '200px' }}
            aria-describedby='input-help'
            aria-label='Message input'
            aria-invalid={hasError}
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
            className={`send-button ${showSuccess ? 'button-success' : ''
              } ${hasError ? 'button-error' : ''
              }`}
            aria-describedby='send-help'
          >
            {isLoading ? (
              <>
                <span className='loading-spinner' aria-hidden='true'></span>
                Sending...
              </>
            ) : showSuccess ? (
              <>
                <span className='success-icon' aria-hidden='true'>✓</span>
                Sent
              </>
            ) : (
              'Send'
            )}
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
));

export default ChatInput_OpenAI;

// Professional fintech glassmorphic input styling with micro-interactions
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
    padding: var(--space-4);
    background: transparent;
    border: none;
  }
  
  .input-container {
    display: flex;
    gap: var(--space-2);
    max-width: 1000px;
    margin: 0 auto;
  }
  
  /* Enhanced message input with sophisticated micro-interactions */
  .message-input {
    flex: 1;
    padding: var(--space-3) var(--space-4);
    background: var(--glass-surface-light);
    backdrop-filter: var(--backdrop-blur-md);
    -webkit-backdrop-filter: var(--backdrop-blur-md);
    border: var(--glass-border-highlight);
    border-radius: var(--radius-2xl);
    outline: none;
    font-size: var(--text-sm);
    font-family: var(--font-inter);
    color: var(--neutral-100);
    resize: none;
    line-height: var(--leading-relaxed);
    min-height: 80px;
    max-height: 200px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-400) transparent;
    /* GPU hints removed for performance */
    position: relative;
  }
  
  /* Professional focus state with trust-building glow */
  .message-input.input-focused,
  .message-input:focus {
    border-color: var(--primary-500);
    background: var(--glass-surface-medium);
    box-shadow: 
      0 0 0 3px rgba(139, 92, 246, 0.15),
      0 4px 20px rgba(139, 92, 246, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    /* Transform removed for performance */
  }
  
  /* Error state - animation removed for performance */
  .message-input.input-error {
    border-color: var(--error-500);
    background: var(--glass-surface-light);
    box-shadow: 
      0 0 0 3px rgba(239, 68, 68, 0.15),
      0 4px 20px rgba(239, 68, 68, 0.2);
    /* Shake animation removed for performance */
  }
  
  /* Success state - animation removed for performance */
  .message-input.input-success {
    border-color: var(--success-500);
    background: var(--glass-surface-medium);
    box-shadow: 
      0 0 0 3px rgba(34, 197, 94, 0.15),
      0 4px 20px rgba(34, 197, 94, 0.2);
    /* Pulse animation removed for performance */
  }
  
  /* Animations removed for performance */
  /* @keyframes input-shake and input-success-pulse removed */
  
  /* Enhanced placeholder - transitions removed for performance */
  .message-input::placeholder {
    color: var(--neutral-400);
    font-family: var(--font-inter);
  }
  
  .message-input.input-focused::placeholder {
    color: var(--neutral-500);
    opacity: 0.8;
  }
  
  /* Focus-visible for keyboard navigation */

  
  .message-input:focus-visible {
    outline: 2px solid var(--primary-400);
    outline-offset: 2px;
  }
  
  .message-input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  /* Enhanced send button with professional micro-interactions */
  .send-button {
    padding: var(--space-3) var(--space-6);
    background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    color: var(--neutral-50);
    border: 1px solid var(--primary-500);
    border-radius: var(--radius-full);
    cursor: pointer;
    font-size: var(--text-sm);
    font-weight: var(--font-medium);
    font-family: var(--font-inter);
    min-width: 100px;
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    /* GPU hints removed for performance */
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-1);
  }
  
  .send-button:disabled {
    background: var(--glass-surface-light);
    color: var(--neutral-400);
    border-color: var(--neutral-600);
    cursor: not-allowed;
    box-shadow: none;
  }
  
  /* Professional hover state - transforms removed for performance */
  .send-button:not(:disabled):hover {
    background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%);
    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
    border-color: var(--primary-400);
  }
  
  /* Active state - transforms removed for performance */
  .send-button:not(:disabled):active {
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
  }
  
  /* Enhanced focus state */
  .send-button:focus-visible {
    outline: 2px solid var(--primary-300);
    outline-offset: 2px;
    box-shadow: 
      0 0 0 4px rgba(139, 92, 246, 0.2),
      0 6px 20px rgba(139, 92, 246, 0.4);
  }
  
  /* Success button state - animation removed for performance */
  .send-button.button-success {
    background: linear-gradient(135deg, var(--success-600) 0%, var(--success-700) 100%);
    border-color: var(--success-500);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
  }
  
  /* Error button state - animation removed for performance */
  .send-button.button-error {
    background: linear-gradient(135deg, var(--error-600) 0%, var(--error-700) 100%);
    border-color: var(--error-500);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  }
  
  /* Button animations removed for performance */
  /* @keyframes button-success-pulse and button-error-shake removed */
  
  /* Loading spinner - animation removed for performance */
  .loading-spinner {
    width: 16px;
    height: 16px;
    margin-right: var(--space-1);
    /* Replaced spinner with static icon */
  }
  
  .loading-spinner::before {
    content: 'Loading...';
    font-size: 16px;
    color: currentColor;
  }
  
  /* Success icon - animation removed for performance */
  .success-icon {
    font-size: var(--text-base);
    font-weight: bold;
    color: currentColor;
  }
  
  /* Enhanced glassmorphic scrollbar styling for input */
  .message-input::-webkit-scrollbar {
    width: 6px;
  }
  
  .message-input::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .message-input::-webkit-scrollbar-thumb {
    background: var(--glass-surface-medium);
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
    border: 1px solid var(--glass-border-highlight);
    border-radius: var(--radius-full);
    /* Transition removed for performance */
  }
  
  .message-input::-webkit-scrollbar-thumb:hover {
    background: var(--primary-400);
    border-color: var(--primary-300);
  }
  
  /* Enhanced scrollbar for focused state */
  .message-input.input-focused::-webkit-scrollbar-thumb {
    background: rgba(139, 92, 246, 0.6);
    border-color: var(--primary-400);
  }
  
  /* Mobile responsive adjustments */
  @media (max-width: 767px) {
    .input-container {
      gap: var(--space-2);
    }
    
    .message-input {
      font-size: var(--text-base);
      min-height: 60px;
    }
    
    .send-button {
      padding: var(--space-3) var(--space-4);
      min-width: 80px;
      font-size: var(--text-xs);
    }
  }
  
  /* Enhanced high contrast mode support */
  @media (prefers-contrast: high) {
    .message-input {
      border: 2px solid var(--primary-400);
    }
    
    .message-input.input-focused {
      border: 3px solid var(--primary-300);
      box-shadow: none;
    }
    
    .message-input.input-error {
      border: 3px solid var(--error-500);
      box-shadow: none;
    }
    
    .message-input.input-success {
      border: 3px solid var(--success-500);
      box-shadow: none;
    }
    
    .send-button {
      border: 2px solid var(--primary-400);
      box-shadow: none;
    }
  }
  
  /* Reduced motion support - ALL ANIMATIONS ALREADY REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
`;
