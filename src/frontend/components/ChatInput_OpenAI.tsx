import {
  useState,
  useRef,
  useImperativeHandle,
  forwardRef,
  useEffect,
  useCallback,
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
    const [isFocused, setIsFocused] = useState(false);
    const [hasError, setHasError] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);

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

    const handleSubmit = useCallback((e: React.FormEvent) => {
      e.preventDefault();
      
      // Clear any existing error state
      setHasError(false);
      
      if (inputValue.trim() && !isLoading) {
        // Show success feedback
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 500);
        
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
      } else if (!inputValue.trim()) {
        // Show error feedback for empty submission
        setHasError(true);
        setTimeout(() => setHasError(false), 600);
      }
    }, [inputValue, isLoading, onSendMessage, externalValue, onValueChange]);

    const handleInputChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = e.target.value;
      
      // Clear error state when user starts typing
      if (hasError) {
        setHasError(false);
      }

      // Update appropriate state based on control mode
      if (externalValue !== undefined && onValueChange) {
        onValueChange(newValue);
      } else {
        setInternalValue(newValue);
      }

      // Auto-resize logic with smooth transition
      const textarea = e.target;
      const previousHeight = textarea.style.height;
      textarea.style.height = 'auto';
      const newHeight = Math.min(textarea.scrollHeight, 200) + 'px';
      
      if (previousHeight !== newHeight) {
        textarea.style.height = newHeight;
      }
    }, [hasError, externalValue, onValueChange]);

    const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
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
            onFocus={handleFocus}
            onBlur={handleBlur}
            placeholder={placeholder}
            className={`message-input ${
              isFocused ? 'input-focused' : ''
            } ${
              hasError ? 'input-error' : ''
            } ${
              showSuccess ? 'input-success' : ''
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
            className={`send-button ${
              showSuccess ? 'button-success' : ''
            } ${
              hasError ? 'button-error' : ''
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
);

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
    /* Professional fintech transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    scrollbar-width: thin;
    scrollbar-color: var(--neutral-400) transparent;
    /* Performance optimization */
    will-change: border-color, box-shadow, background-color;
    transform: translateZ(0); /* GPU acceleration */
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
    transform: translateY(-1px);
  }
  
  /* Error state with professional shake animation */
  .message-input.input-error {
    border-color: var(--error-500);
    background: var(--glass-surface-light);
    box-shadow: 
      0 0 0 3px rgba(239, 68, 68, 0.15),
      0 4px 20px rgba(239, 68, 68, 0.2);
    animation: input-shake 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* Success state with subtle celebration */
  .message-input.input-success {
    border-color: var(--success-500);
    background: var(--glass-surface-medium);
    box-shadow: 
      0 0 0 3px rgba(34, 197, 94, 0.15),
      0 4px 20px rgba(34, 197, 94, 0.2);
    animation: input-success-pulse 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* Professional shake animation for errors */
  @keyframes input-shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
    20%, 40%, 60%, 80% { transform: translateX(4px); }
  }
  
  /* Success pulse animation */
  @keyframes input-success-pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
  }
  
  /* Enhanced placeholder with smooth transitions */
  .message-input::placeholder {
    color: var(--neutral-400);
    font-family: var(--font-inter);
    transition: color 0.3s ease, opacity 0.3s ease;
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
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-width: 100px;
    backdrop-filter: var(--backdrop-blur-sm);
    -webkit-backdrop-filter: var(--backdrop-blur-sm);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    /* Performance optimization */
    will-change: transform, box-shadow, background;
    transform: translateZ(0);
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
  
  /* Professional hover state with trust enhancement */
  .send-button:not(:disabled):hover {
    background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%);
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
    border-color: var(--primary-400);
  }
  
  /* Active state with satisfying feedback */
  .send-button:not(:disabled):active {
    transform: translateY(-1px) scale(0.98);
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
  
  /* Success button state */
  .send-button.button-success {
    background: linear-gradient(135deg, var(--success-600) 0%, var(--success-700) 100%);
    border-color: var(--success-500);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
    animation: button-success-pulse 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* Error button state */
  .send-button.button-error {
    background: linear-gradient(135deg, var(--error-600) 0%, var(--error-700) 100%);
    border-color: var(--error-500);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    animation: button-error-shake 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* Button success pulse animation */
  @keyframes button-success-pulse {
    0% { transform: scale(1); }
    50% { 
      transform: scale(1.05);
      box-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
    }
    100% { transform: scale(1); }
  }
  
  /* Button error shake animation */
  @keyframes button-error-shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
    20%, 40%, 60%, 80% { transform: translateX(2px); }
  }
  
  /* Loading spinner for button */
  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: button-loading-spin 1s linear infinite;
    margin-right: var(--space-1);
  }
  
  @keyframes button-loading-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Success icon with smooth appearance */
  .success-icon {
    font-size: var(--text-base);
    font-weight: bold;
    color: currentColor;
    animation: success-icon-appear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  @keyframes success-icon-appear {
    0% { 
      transform: scale(0) rotate(-90deg);
      opacity: 0;
    }
    100% { 
      transform: scale(1) rotate(0deg);
      opacity: 1;
    }
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
    transition: all 0.3s ease;
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
      border: 2px solid var(--primary-300);
      box-shadow: none;
    }
    
    .message-input.input-error {
      border: 2px solid var(--error-500);
      box-shadow: none;
    }
    
    .message-input.input-success {
      border: 2px solid var(--success-500);
      box-shadow: none;
    }
    
    .send-button {
      border: 2px solid var(--primary-400);
      box-shadow: none;
    }
  }
  
  /* Enhanced reduced motion support for accessibility */
  @media (prefers-reduced-motion: reduce) {
    .message-input,
    .send-button {
      transition: none;
      animation: none;
    }
    
    .send-button:not(:disabled):hover {
      transform: none;
    }
    
    .message-input.input-focused {
      transform: none;
      animation: none;
    }
    
    .message-input.input-error {
      animation: none;
    }
    
    .message-input.input-success {
      animation: none;
    }
    
    .send-button.button-success,
    .send-button.button-error {
      animation: none;
    }
    
    .loading-spinner {
      animation: none;
      border: 2px solid currentColor;
    }
    
    .success-icon {
      animation: none;
    }
  }
`;
