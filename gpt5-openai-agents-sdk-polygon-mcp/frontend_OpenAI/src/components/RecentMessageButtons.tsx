import { useState, useCallback, useRef, useEffect } from 'react';
import { Message } from '../types/chat_OpenAI';
import {
  getMostRecentMessage,
  convertSingleMessageToMarkdown,
  copyToClipboard,
} from '../utils/exportHelpers';

interface RecentMessageButtonsProps {
  messages: Message[];
}

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

interface ButtonStates {
  lastAI: ButtonState;
  lastUser: ButtonState;
}

export default function RecentMessageButtons({ messages }: RecentMessageButtonsProps) {
  const [buttonStates, setButtonStates] = useState<ButtonStates>({
    lastAI: 'idle',
    lastUser: 'idle',
  });

  const [errorMessages, setErrorMessages] = useState<Record<string, string>>({});
  
  // Refs to store timeout IDs for cleanup
  const timeoutRefs = useRef<Record<keyof ButtonStates, number | null>>({
    lastAI: null,
    lastUser: null,
  });

  // Cleanup timeouts on component unmount
  useEffect(() => {
    return () => {
      // Clear all active timeouts to prevent memory leaks
      Object.values(timeoutRefs.current).forEach(timeoutId => {
        if (timeoutId) {
          clearTimeout(timeoutId);
        }
      });
    };
  }, []);

  const updateButtonState = useCallback(
    (buttonId: keyof ButtonStates, state: ButtonState, errorMessage?: string) => {
      // Clear any existing timeout for this button to prevent conflicts
      if (timeoutRefs.current[buttonId]) {
        clearTimeout(timeoutRefs.current[buttonId]!);
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
      const errorMessage = error instanceof Error ? error.message : 'Failed to copy AI response';
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
      const errorMessage = error instanceof Error ? error.message : 'Failed to copy user request';
      updateButtonState(buttonId, 'error', errorMessage);
    }
  }, [messages, updateButtonState]);

  // Check if we have messages of each type
  const hasAIMessages = messages.some(m => m.sender === 'ai');
  const hasUserMessages = messages.some(m => m.sender === 'user');
  const isEmpty = messages.length === 0;

  const getButtonText = (buttonId: keyof ButtonStates, defaultText: string): string => {
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

  const getButtonClass = (buttonId: keyof ButtonStates, isDisabled: boolean): string => {
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
    <div className="recent-message-buttons-container">
      <div className="recent-message-buttons">
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
          aria-label="Copy most recent AI response to clipboard as markdown"
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
          aria-label="Copy most recent user request to clipboard as markdown"
        >
          👤 {getButtonText('lastUser', 'Copy Last User Request')}
        </button>
      </div>

      {/* Error Messages Display */}
      {Object.entries(errorMessages).map(([buttonId, errorMessage]) => (
        errorMessage && buttonStates[buttonId as keyof ButtonStates] === 'error' ? (
          <div key={buttonId} className="recent-message-error-message">
            <strong>Copy Error:</strong> {errorMessage}
          </div>
        ) : null
      ))}
    </div>
  );
}

// Inline styles for RecentMessageButtons component
export const recentMessageButtonsStyles = `
  .recent-message-buttons-container {
    margin: 8px 0;
    padding: 0;
  }
  
  .recent-message-buttons {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    max-width: 100%;
  }
  
  @media (max-width: 640px) {
    .recent-message-buttons {
      gap: 6px;
    }
  }
  
  .recent-message-button {
    padding: 8px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 16px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    min-height: 36px;
    text-align: center;
    min-width: 140px;
  }
  
  .recent-message-button:not(.disabled):not(.loading):hover {
    background-color: #0056b3;
    transform: translateY(-1px);
  }
  
  .recent-message-button:not(.disabled):not(.loading):active {
    transform: translateY(0);
  }
  
  .recent-message-button.disabled {
    background-color: #ccc;
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .recent-message-button.loading {
    background-color: #6c757d;
    cursor: wait;
    position: relative;
  }
  
  .recent-message-button.loading::after {
    content: '';
    width: 12px;
    height: 12px;
    border: 2px solid transparent;
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 4px;
  }
  
  .recent-message-button.success {
    background-color: #28a745;
    cursor: default;
  }
  
  .recent-message-button.success:hover {
    background-color: #28a745;
    transform: none;
  }
  
  .recent-message-button.error {
    background-color: #dc3545;
    cursor: pointer;
  }
  
  .recent-message-button.error:hover {
    background-color: #c82333;
  }
  
  .recent-message-error-message {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    padding: 8px 12px;
    margin-top: 8px;
    font-size: 12px;
    text-align: left;
    max-width: 400px;
    margin-left: auto;
    margin-right: auto;
  }
  
  /* Integration styles for chat header */
  .chat-header .recent-message-buttons-container {
    margin: 8px 0 0 0;
  }
  
  .chat-header .recent-message-buttons {
    justify-content: center;
    max-width: 500px;
    margin: 0 auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;