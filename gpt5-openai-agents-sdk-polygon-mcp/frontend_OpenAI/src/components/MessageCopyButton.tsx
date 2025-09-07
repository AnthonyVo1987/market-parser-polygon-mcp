import { useState, useCallback, useRef, useEffect } from 'react';
import { Message } from '../types/chat_OpenAI';
import {
  convertSingleMessageToMarkdown,
  copyToClipboard,
} from '../utils/exportHelpers';

interface MessageCopyButtonProps {
  message: Message;
  className?: string;
}

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

export default function MessageCopyButton({
  message,
  className = '',
}: MessageCopyButtonProps) {
  const [buttonState, setButtonState] = useState<ButtonState>('idle');
  const [errorMessage, setErrorMessage] = useState<string>('');

  // Ref to store timeout ID for cleanup
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Cleanup timeout on component unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const updateButtonState = useCallback(
    (state: ButtonState, errorMsg?: string) => {
      // Clear any existing timeout to prevent conflicts
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }

      setButtonState(state);
      setErrorMessage(errorMsg || '');

      // Auto-reset success and error states after timeout
      if (state === 'success' || state === 'error') {
        const timeoutDuration = state === 'success' ? 2000 : 4000; // Errors show longer

        timeoutRef.current = setTimeout(() => {
          setButtonState('idle');
          setErrorMessage('');
          timeoutRef.current = null;
        }, timeoutDuration);
      }
    },
    []
  );

  const handleCopyMessage = useCallback(
    async (event: React.MouseEvent) => {
      // Prevent event from bubbling up to parent elements
      event.stopPropagation();

      updateButtonState('loading');

      try {
        const markdownContent = convertSingleMessageToMarkdown(message);
        await copyToClipboard(markdownContent);
        updateButtonState('success');
      } catch (error) {
        const errorMsg =
          error instanceof Error ? error.message : 'Failed to copy message';
        updateButtonState('error', errorMsg);
      }
    },
    [message, updateButtonState]
  );

  const getButtonIcon = (): string => {
    switch (buttonState) {
      case 'loading':
        return '⏳';
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '📋';
    }
  };

  const getButtonTitle = (): string => {
    switch (buttonState) {
      case 'loading':
        return 'Copying...';
      case 'success':
        return 'Copied to clipboard!';
      case 'error':
        return errorMessage || 'Copy failed';
      default:
        return 'Copy message to clipboard as markdown';
    }
  };

  const getButtonClass = (): string => {
    const baseClass = 'message-copy-button';
    const customClass = className ? ` ${className}` : '';

    switch (buttonState) {
      case 'loading':
        return `${baseClass} loading${customClass}`;
      case 'success':
        return `${baseClass} success${customClass}`;
      case 'error':
        return `${baseClass} error${customClass}`;
      default:
        return `${baseClass}${customClass}`;
    }
  };

  return (
    <button
      onClick={handleCopyMessage}
      disabled={buttonState === 'loading'}
      className={getButtonClass()}
      title={getButtonTitle()}
      aria-label={getButtonTitle()}
    >
      <span className='copy-icon'>{getButtonIcon()}</span>
    </button>
  );
}

// Inline styles for the MessageCopyButton component
export const messageCopyButtonStyles = `
  .message-copy-button {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 28px;
    height: 28px;
    background-color: rgba(255, 255, 255, 0.9);
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    opacity: 0;
    transition: all 0.2s ease;
    z-index: 10;
    backdrop-filter: blur(4px);
  }

  .message-copy-button:hover {
    background-color: rgba(255, 255, 255, 1);
    border-color: #cbd5e0;
    transform: scale(1.05);
  }

  .message-copy-button:active {
    transform: scale(0.95);
  }

  .message-copy-button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  .message-copy-button.loading {
    background-color: rgba(108, 117, 125, 0.9);
    border-color: #6c757d;
    cursor: wait;
  }

  .message-copy-button.success {
    background-color: rgba(40, 167, 69, 0.9);
    border-color: #28a745;
    color: white;
  }

  .message-copy-button.success:hover {
    background-color: rgba(40, 167, 69, 1);
    transform: none;
  }

  .message-copy-button.error {
    background-color: rgba(220, 53, 69, 0.9);
    border-color: #dc3545;
    color: white;
  }

  .message-copy-button.error:hover {
    background-color: rgba(220, 53, 69, 1);
  }

  .copy-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    line-height: 1;
  }

  /* Show button on message hover */
  .message-bubble {
    position: relative;
  }

  .message-bubble:hover .message-copy-button {
    opacity: 1;
  }

  /* Ensure button is always visible on touch devices */
  @media (hover: none) {
    .message-copy-button {
      opacity: 0.7;
    }
    
    .message-bubble:hover .message-copy-button,
    .message-copy-button:focus {
      opacity: 1;
    }
  }

  /* Responsive adjustments for smaller screens */
  @media (max-width: 640px) {
    .message-copy-button {
      width: 32px;
      height: 32px;
      font-size: 14px;
      top: 6px;
      right: 6px;
    }
  }
`;
