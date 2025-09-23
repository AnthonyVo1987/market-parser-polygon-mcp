import { memo, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Message } from '../types/chat_OpenAI';
import {
  convertSingleMessageToMarkdown,
  copyToClipboard,
  getMostRecentMessage,
} from '../utils/exportHelpers';

interface RecentMessageButtonsProps {
  messages: Message[];
}

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

interface ButtonStates {
  lastAI: ButtonState;
  lastUser: ButtonState;
}

const RecentMessageButtons = memo(
  function RecentMessageButtons({ messages }: RecentMessageButtonsProps) {
    const [buttonStates, setButtonStates] = useState<ButtonStates>({
      lastAI: 'idle',
      lastUser: 'idle',
    });

    const [errorMessages, setErrorMessages] = useState<Record<string, string>>(
      {}
    );

    // Refs to store timeout IDs for cleanup
    const timeoutRefs = useRef<
      Record<keyof ButtonStates, ReturnType<typeof setTimeout> | null>
    >({
      lastAI: null,
      lastUser: null,
    });

    // Cleanup timeouts on component unmount
    useEffect(() => {
      return () => {
        // Clear all active timeouts to prevent memory leaks
        // Copy ref value inside effect cleanup to avoid stale reference
        // eslint-disable-next-line react-hooks/exhaustive-deps
        const currentTimeouts = timeoutRefs.current;
        Object.values(currentTimeouts).forEach(timeoutId => {
          if (timeoutId) {
            clearTimeout(timeoutId);
          }
        });
      };
    }, []);

    const updateButtonState = useCallback(
      (
        buttonId: keyof ButtonStates,
        state: ButtonState,
        errorMessage?: string
      ) => {
        // Clear any existing timeout for this button to prevent conflicts
        if (timeoutRefs.current[buttonId]) {
          clearTimeout(timeoutRefs.current[buttonId]);
          timeoutRefs.current[buttonId] = null;
        }

        setButtonStates(prev => ({ ...prev, [buttonId]: state }));

        if (errorMessage) {
          setErrorMessages(prev => ({ ...prev, [buttonId]: errorMessage }));
        } else {
          setErrorMessages(prev => ({ ...prev, [buttonId]: '' }));
        }

        // Auto-reset success and error states after timeout
        if (state === 'success' || state === 'error') {
          const timeoutDuration = state === 'success' ? 2000 : 4000; // Errors show longer

          timeoutRefs.current[buttonId] = setTimeout(() => {
            setButtonStates(prev => ({ ...prev, [buttonId]: 'idle' }));
            setErrorMessages(prev => ({ ...prev, [buttonId]: '' }));
            timeoutRefs.current[buttonId] = null;
          }, timeoutDuration);
        }
      },
      []
    );

    const handleCopyLastAI = useCallback(async () => {
      const buttonId = 'lastAI';
      updateButtonState(buttonId, 'loading');

      try {
        const lastAIMessage = getMostRecentMessage(messages, 'ai');
        if (!lastAIMessage) {
          throw new Error('No AI messages found');
        }

        const markdownContent = convertSingleMessageToMarkdown(lastAIMessage);
        await copyToClipboard(markdownContent);
        updateButtonState(buttonId, 'success');
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : 'Failed to copy AI response';
        updateButtonState(buttonId, 'error', errorMessage);
      }
    }, [messages, updateButtonState]);

    const handleCopyLastUser = useCallback(async () => {
      const buttonId = 'lastUser';
      updateButtonState(buttonId, 'loading');

      try {
        const lastUserMessage = getMostRecentMessage(messages, 'user');
        if (!lastUserMessage) {
          throw new Error('No user messages found');
        }

        const markdownContent = convertSingleMessageToMarkdown(lastUserMessage);
        await copyToClipboard(markdownContent);
        updateButtonState(buttonId, 'success');
      } catch (error) {
        const errorMessage =
          error instanceof Error
            ? error.message
            : 'Failed to copy user request';
        updateButtonState(buttonId, 'error', errorMessage);
      }
    }, [messages, updateButtonState]);

    // Memoize expensive message computations
    const messageAnalysis = useMemo(() => {
      const messageCount = messages.length;
      const isEmpty = messageCount === 0;
      const hasAIMessages = messages.some(m => m.sender === 'ai');
      const hasUserMessages = messages.some(m => m.sender === 'user');

      return {
        messageCount,
        isEmpty,
        hasAIMessages,
        hasUserMessages,
      };
    }, [messages]);

    const { isEmpty, hasAIMessages, hasUserMessages } = messageAnalysis;

    const getButtonText = (
      buttonId: keyof ButtonStates,
      defaultText: string
    ): string => {
      const state = buttonStates[buttonId];
      switch (state) {
        case 'loading':
          return 'Copying...';
        case 'success':
          return 'Copied!';
        case 'error':
          return 'Error';
        default:
          return defaultText;
      }
    };

    const getButtonClass = (
      buttonId: keyof ButtonStates,
      isDisabled: boolean
    ): string => {
      const state = buttonStates[buttonId];
      const baseClass = 'recent-message-button';

      if (isDisabled) return `${baseClass} disabled`;

      switch (state) {
        case 'loading':
          return `${baseClass} loading`;
        case 'success':
          return `${baseClass} success`;
        case 'error':
          return `${baseClass} error`;
        default:
          return baseClass;
      }
    };

    // Don't render if no messages at all
    if (isEmpty) {
      return null;
    }

    return (
      <div className='recent-message-buttons-container'>
        <div className='recent-message-buttons'>
          {/* Copy Last AI Response Button */}
          <button
            onClick={handleCopyLastAI}
            disabled={!hasAIMessages || buttonStates.lastAI === 'loading'}
            className={getButtonClass('lastAI', !hasAIMessages)}
            title={
              !hasAIMessages
                ? 'No AI responses to copy'
                : 'Copy most recent AI response to clipboard as markdown'
            }
            aria-label='Copy most recent AI response to clipboard as markdown'
          >
            🤖 {getButtonText('lastAI', 'Copy Last AI Response')}
          </button>

          {/* Copy Last User Request Button */}
          <button
            onClick={handleCopyLastUser}
            disabled={!hasUserMessages || buttonStates.lastUser === 'loading'}
            className={getButtonClass('lastUser', !hasUserMessages)}
            title={
              !hasUserMessages
                ? 'No user requests to copy'
                : 'Copy most recent user request to clipboard as markdown'
            }
            aria-label='Copy most recent user request to clipboard as markdown'
          >
            👤 {getButtonText('lastUser', 'Copy Last User Request')}
          </button>
        </div>

        {/* Error Messages Display */}
        {Object.entries(errorMessages).map(([buttonId, errorMessage]) =>
          errorMessage &&
          buttonStates[buttonId as keyof ButtonStates] === 'error' ? (
            <div key={buttonId} className='recent-message-error-message'>
              <strong>Copy Error:</strong> {errorMessage}
            </div>
          ) : null
        )}
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Custom comparison function - only re-render if message count or message content changes
    const prevMessages = prevProps.messages;
    const nextMessages = nextProps.messages;

    // Quick length check first
    if (prevMessages.length !== nextMessages.length) {
      return false;
    }

    // If same length, check if the most recent messages of each type changed
    // This is more efficient than deep comparison for this use case
    const prevLastAI = prevMessages.filter(m => m.sender === 'ai').pop();
    const nextLastAI = nextMessages.filter(m => m.sender === 'ai').pop();
    const prevLastUser = prevMessages.filter(m => m.sender === 'user').pop();
    const nextLastUser = nextMessages.filter(m => m.sender === 'user').pop();

    return (
      prevLastAI?.id === nextLastAI?.id && prevLastUser?.id === nextLastUser?.id
    );
  }
);

RecentMessageButtons.displayName = 'RecentMessageButtons';

export default RecentMessageButtons;

// Professional Fintech Glassmorphic Styles for Recent Message Access
export const recentMessageButtonsStyles = `
  /* ==========================================================================
     RECENT MESSAGE BUTTONS - Subtle Utility Component with Professional Fintech Design
     ========================================================================== */
  
  .recent-message-buttons-container {
    margin: var(--spacing-2) 0;
    padding: 0;
    width: 100%;
  }
  
  .recent-message-buttons {
    display: flex;
    gap: var(--spacing-2);
    justify-content: center;
    flex-wrap: wrap;
    max-width: 100%;
  }
  
  /* Professional Recent Message Button Base Styling */
  .recent-message-button {
    /* Subtle Glassmorphic Foundation */
    background: var(--glass-surface-1);
    /* backdrop-filter removed for performance */
    border: 1px solid var(--glass-border-1);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
    
    /* Professional Button Design */
    padding: var(--spacing-2) var(--spacing-3);
    border-radius: 8px;
    cursor: pointer;
    
    /* Typography - Subtle Utility Styling */
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-normal);
    color: var(--neutral-color);
    letter-spacing: var(--letter-spacing-normal);
    
    /* Layout */
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-1);
    min-height: 38px;
    text-align: center;
    min-width: 160px;
    
    /* Transitions removed for performance */
    position: relative;
    overflow: hidden;
  }
  
  /* Hover Effect - Enhanced but Subtle Glass Surface */
  .recent-message-button:not(.disabled):not(.loading):hover {
    background: var(--glass-surface-2);
    border-color: var(--glass-border-2);
    color: var(--text-secondary);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    /* Transform removed for performance */
  }
  
  /* Active State */
  .recent-message-button:not(.disabled):not(.loading):active {
    background: var(--glass-surface-3);
    /* Transform removed for performance */
  }
  
  /* Disabled State - Very Subtle */
  .recent-message-button.disabled {
    background: rgba(255, 255, 255, 0.02);
    border-color: rgba(255, 255, 255, 0.03);
    color: rgba(160, 174, 192, 0.5);
    cursor: not-allowed;
    opacity: 0.4;
  }
  
  /* Loading State - Professional with Info Color */
  .recent-message-button.loading {
    background: var(--glass-surface-2);
    border-color: var(--accent-info);
    color: var(--accent-info-light);
    cursor: wait;
  }
  
  .recent-message-button.loading::after {
    content: 'Loading...';
    font-size: 12px;
    color: var(--accent-info);
    margin-left: var(--spacing-1);
    /* Spinner animation replaced with static icon */
  }
  
  /* Success State - Subtle Success Gradient */
  .recent-message-button.success {
    /* Complex gradient simplified for performance */
    background: var(--accent-success);
    border-color: var(--accent-success);
    color: var(--text-primary);
    cursor: default;
    box-shadow: 0 3px 10px rgba(16, 185, 129, 0.25);
  }
  
  .recent-message-button.success:hover {
    /* Complex gradient simplified for performance */
    background: var(--accent-success);
  }
  
  /* Error State - Subtle Error Treatment */
  .recent-message-button.error {
    /* Complex gradient simplified for performance */
    background: var(--accent-error);
    border-color: var(--accent-error);
    color: var(--text-primary);
    cursor: pointer;
    box-shadow: 0 3px 10px rgba(239, 68, 68, 0.25);
  }
  
  .recent-message-button.error:hover {
    /* Complex gradient simplified for performance */
    background: var(--accent-error-hover);
    /* Transform removed for performance */
  }
  
  /* Professional Error Message Display */
  .recent-message-error-message {
    background: var(--glass-surface-2);
    /* backdrop-filter removed for performance */
    border: 1px solid var(--accent-error);
    border-radius: 8px;
    padding: var(--spacing-2) var(--spacing-3);
    margin-top: var(--spacing-2);
    
    color: var(--accent-error-light);
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-medium);
    text-align: left;
    
    max-width: 450px;
    margin-left: auto;
    margin-right: auto;
    
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
  }
  
  .recent-message-error-message strong {
    color: var(--accent-error);
    font-weight: var(--font-weight-semibold);
  }
  
  /* Responsive Design - Mobile Optimization */
  @media (max-width: 768px) {
    .recent-message-buttons {
      gap: var(--spacing-1);
      flex-direction: column;
      align-items: center;
    }
    
    .recent-message-button {
      padding: var(--spacing-2);
      min-height: 44px; /* Touch target optimization */
      font-size: var(--font-size-micro);
      min-width: 200px;
    }
    
    .recent-message-error-message {
      padding: var(--spacing-2);
      font-size: var(--font-size-micro);
      max-width: 100%;
    }
  }
  
  /* Tablet Optimization */
  @media (min-width: 769px) and (max-width: 1024px) {
    .recent-message-buttons {
      gap: var(--spacing-2);
    }
    
    .recent-message-button {
      min-width: 180px;
    }
  }
  
  /* Desktop Enhancement - More Subtle */
  @media (min-width: 1025px) {
    .recent-message-button {
      padding: var(--spacing-2) var(--spacing-4);
      min-height: 36px;
      min-width: 170px;
    }
    
    .recent-message-button:hover {
      /* backdrop-filter removed for performance */
    }
  }
  
  /* Integration Styles for Chat Interface */
  .chat-header .recent-message-buttons-container {
    margin: var(--spacing-2) 0 0 0;
  }
  
  .chat-header .recent-message-buttons {
    justify-content: center;
    max-width: 550px;
    margin: 0 auto;
  }
  
  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .recent-message-button {
      border-width: 2px;
      background: var(--background-secondary);
    }
    
    .recent-message-button:hover {
      border-color: var(--accent-info);
    }
  }
  
  /* Reduced Motion Support - ALL ANIMATIONS ALREADY REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
  
  /* Performance Optimizations - GPU hints removed for performance */
  .recent-message-button {
    /* GPU acceleration hints removed */
  }
  
  /* Animations removed for performance */
  /* @keyframes spin removed */
  
  /* Focus Management - Accessibility */
  .recent-message-button:focus-visible {
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
  }
  
  .recent-message-button.error:focus-visible {
    outline-color: var(--focus-ring-error);
  }
  
  .recent-message-button.success:focus-visible {
    outline-color: var(--focus-ring-success);
  }
`;
