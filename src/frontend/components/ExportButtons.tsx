import { useState, useCallback, useRef, useEffect, memo, useMemo } from 'react';
import { Message } from '../types/chat_OpenAI';
import {
  convertToMarkdown,
  convertToJSON,
  copyToClipboard,
  downloadFile,
  generateSafeFilename,
  validateMessages,
} from '../utils/exportHelpers';

interface ExportButtonsProps {
  messages: Message[];
}

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

interface ButtonStates {
  copyMd: ButtonState;
  copyJson: ButtonState;
  saveMd: ButtonState;
  saveJson: ButtonState;
}

const ExportButtons = memo(function ExportButtons({ messages }: ExportButtonsProps) {
  const [buttonStates, setButtonStates] = useState<ButtonStates>({
    copyMd: 'idle',
    copyJson: 'idle',
    saveMd: 'idle',
    saveJson: 'idle',
  });

  const [errorMessages, setErrorMessages] = useState<Record<string, string>>(
    {}
  );

  // Refs to store timeout IDs for cleanup
  const timeoutRefs = useRef<
    Record<keyof ButtonStates, ReturnType<typeof setTimeout> | null>
  >({
    copyMd: null,
    copyJson: null,
    saveMd: null,
    saveJson: null,
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
      const timeoutId = timeoutRefs.current[buttonId];
      if (timeoutId !== null) {
        clearTimeout(timeoutId);
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

  const handleCopyMarkdown = useCallback(async () => {
    const buttonId = 'copyMd';
    updateButtonState(buttonId, 'loading');

    try {
      validateMessages(messages);
      const markdownContent = convertToMarkdown(messages);
      await copyToClipboard(markdownContent);
      updateButtonState(buttonId, 'success');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to copy markdown';
      updateButtonState(buttonId, 'error', errorMessage);
    }
  }, [messages, updateButtonState]);

  const handleCopyJSON = useCallback(async () => {
    const buttonId = 'copyJson';
    updateButtonState(buttonId, 'loading');

    try {
      validateMessages(messages);
      const jsonContent = convertToJSON(messages);
      await copyToClipboard(jsonContent);
      updateButtonState(buttonId, 'success');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to copy JSON';
      updateButtonState(buttonId, 'error', errorMessage);
    }
  }, [messages, updateButtonState]);

  const handleSaveMarkdown = useCallback(() => {
    const buttonId = 'saveMd';
    updateButtonState(buttonId, 'loading');

    try {
      validateMessages(messages);
      const markdownContent = convertToMarkdown(messages);
      const filename = generateSafeFilename('chat_export', '.md');
      downloadFile(markdownContent, filename, 'text/markdown');
      updateButtonState(buttonId, 'success');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to save markdown';
      updateButtonState(buttonId, 'error', errorMessage);
    }
  }, [messages, updateButtonState]);

  const handleSaveJSON = useCallback(() => {
    const buttonId = 'saveJson';
    updateButtonState(buttonId, 'loading');

    try {
      validateMessages(messages);
      const jsonContent = convertToJSON(messages);
      const filename = generateSafeFilename('chat_export', '.json');
      downloadFile(jsonContent, filename, 'application/json');
      updateButtonState(buttonId, 'success');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to save JSON';
      updateButtonState(buttonId, 'error', errorMessage);
    }
  }, [messages, updateButtonState]);

  // Memoize computed values for performance
  const computedValues = useMemo(() => {
    const messageCount = messages.length;
    const isDisabled = messageCount === 0;
    const hasMessages = messageCount > 0;
    
    return {
      messageCount,
      isDisabled,
      hasMessages
    };
  }, [messages.length]);
  
  const { isDisabled } = computedValues;

  const getButtonText = (
    buttonId: keyof ButtonStates,
    defaultText: string
  ): string => {
    const state = buttonStates[buttonId];
    switch (state) {
      case 'loading':
        return 'Loading...';
      case 'success':
        return 'Success!';
      case 'error':
        return 'Error';
      default:
        return defaultText;
    }
  };

  const getButtonClass = (buttonId: keyof ButtonStates): string => {
    const state = buttonStates[buttonId];
    const baseClass = 'export-button';

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

  return (
    <div className='export-buttons-container'>
      <div className='export-buttons-grid'>
        {/* Copy to Clipboard - Markdown */}
        <button
          onClick={handleCopyMarkdown}
          disabled={isDisabled || buttonStates.copyMd === 'loading'}
          className={getButtonClass('copyMd')}
          title={
            isDisabled
              ? 'No messages to export'
              : 'Copy chat as markdown to clipboard'
          }
          aria-label='Copy chat as markdown to clipboard'
        >
          📋 {getButtonText('copyMd', 'Copy MD')}
        </button>

        {/* Copy to Clipboard - JSON */}
        <button
          onClick={handleCopyJSON}
          disabled={isDisabled || buttonStates.copyJson === 'loading'}
          className={getButtonClass('copyJson')}
          title={
            isDisabled
              ? 'No messages to export'
              : 'Copy chat as JSON to clipboard'
          }
          aria-label='Copy chat as JSON to clipboard'
        >
          📋 {getButtonText('copyJson', 'Copy JSON')}
        </button>

        {/* Save to File - Markdown */}
        <button
          onClick={handleSaveMarkdown}
          disabled={isDisabled || buttonStates.saveMd === 'loading'}
          className={getButtonClass('saveMd')}
          title={
            isDisabled ? 'No messages to export' : 'Save chat as markdown file'
          }
          aria-label='Save chat as markdown file'
        >
          💾 {getButtonText('saveMd', 'Save MD')}
        </button>

        {/* Save to File - JSON */}
        <button
          onClick={handleSaveJSON}
          disabled={isDisabled || buttonStates.saveJson === 'loading'}
          className={getButtonClass('saveJson')}
          title={
            isDisabled ? 'No messages to export' : 'Save chat as JSON file'
          }
          aria-label='Save chat as JSON file'
        >
          💾 {getButtonText('saveJson', 'Save JSON')}
        </button>
      </div>

      {/* Error Messages Display */}
      {Object.entries(errorMessages).map(([buttonId, errorMessage]) =>
        errorMessage &&
        buttonStates[buttonId as keyof ButtonStates] === 'error' ? (
          <div key={buttonId} className='export-error-message'>
            <strong>Export Error:</strong> {errorMessage}
          </div>
        ) : null
      )}

      {/* Empty State Message */}
      {isDisabled && (
        <div className='export-empty-state'>
          Start a conversation to enable export options
        </div>
      )}
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison function - only re-render if message count changes
  return prevProps.messages.length === nextProps.messages.length;
});

ExportButtons.displayName = 'ExportButtons';

export default ExportButtons;

// Professional Fintech Glassmorphic Styles for Export Functionality
export const exportButtonStyles = `
  /* ==========================================================================
     EXPORT BUTTONS - Professional Fintech Utility Component with Glassmorphic Design
     ========================================================================== */
  
  .export-buttons-container {
    margin: var(--spacing-2) 0;
    padding: 0;
    width: 100%;
  }
  
  .export-buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: var(--spacing-2);
    max-width: 100%;
    padding: 0;
  }
  
  /* Professional Export Button Base Styling */
  .export-button {
    /* Glassmorphic Foundation */
    background: var(--glass-surface-2);
    backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--glass-border-1);
    box-shadow: var(--glass-shadow-sm);
    
    /* Professional Button Design */
    padding: var(--spacing-2) var(--spacing-3);
    border-radius: 12px;
    cursor: pointer;
    
    /* Typography */
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-medium);
    color: var(--text-secondary);
    letter-spacing: var(--letter-spacing-wide);
    
    /* Layout */
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-1);
    min-height: 40px;
    text-align: center;
    
    /* Transitions removed for performance */
    position: relative;
    overflow: hidden;
  }
  
  /* Hover Effect - Enhanced Glass Surface */
  .export-button:not(.disabled):not(.loading):hover {
    background: var(--glass-surface-3);
    border-color: var(--glass-border-2);
    color: var(--text-primary);
    box-shadow: var(--glass-shadow-md);
    /* Transform removed for performance */
  }
  
  /* Active State */
  .export-button:not(.disabled):not(.loading):active {
    background: var(--glass-surface-4);
    /* Transform removed for performance */
  }
  
  /* Disabled State - Subtle Glass Treatment */
  .export-button.disabled {
    background: var(--glass-surface-1);
    border-color: rgba(255, 255, 255, 0.05);
    color: var(--neutral-color);
    cursor: not-allowed;
    opacity: 0.5;
  }
  
  /* Loading State - Professional Animation */
  .export-button.loading {
    background: var(--glass-surface-3);
    border-color: var(--accent-info);
    color: var(--accent-info-light);
    cursor: wait;
  }
  
  .export-button.loading::after {
    content: 'Loading...';
    font-size: 14px;
    color: var(--accent-info);
    margin-left: var(--spacing-1);
    /* Spinner animation replaced with static icon */
  }
  
  /* Success State - Fintech Green */
  .export-button.success {
    background: linear-gradient(135deg, var(--accent-success) 0%, var(--accent-success-light) 100%);
    border-color: var(--accent-success);
    color: var(--text-primary);
    cursor: default;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
  }
  
  .export-button.success:hover {
    background: linear-gradient(135deg, var(--accent-success) 0%, var(--accent-success-light) 100%);
  }
  
  /* Error State - Fintech Red */
  .export-button.error {
    background: linear-gradient(135deg, var(--accent-error) 0%, var(--accent-error-light) 100%);
    border-color: var(--accent-error);
    color: var(--text-primary);
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  }
  
  .export-button.error:hover {
    background: linear-gradient(135deg, var(--accent-error-hover) 0%, var(--accent-error) 100%);
    /* Transform removed for performance */
  }
  
  /* Professional Error Message Display */
  .export-error-message {
    background: var(--glass-surface-2);
    backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--accent-error);
    border-radius: 8px;
    padding: var(--spacing-2) var(--spacing-3);
    margin-top: var(--spacing-2);
    
    color: var(--accent-error-light);
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-medium);
    text-align: left;
    
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
  }
  
  .export-error-message strong {
    color: var(--accent-error);
    font-weight: var(--font-weight-semibold);
  }
  
  /* Empty State - Professional Messaging */
  .export-empty-state {
    text-align: center;
    color: var(--neutral-color);
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-style: italic;
    margin-top: var(--spacing-2);
    padding: var(--spacing-4);
    
    background: var(--glass-surface-1);
    backdrop-filter: var(--glass-blur-xs);
    border: 1px solid var(--glass-border-1);
    border-radius: 8px;
    
    opacity: 0.8;
  }
  
  /* Responsive Design - Mobile Optimization */
  @media (max-width: 640px) {
    .export-buttons-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: var(--spacing-1);
    }
    
    .export-button {
      padding: var(--spacing-2);
      min-height: 44px; /* Touch target optimization */
      font-size: var(--font-size-micro);
    }
    
    .export-error-message {
      padding: var(--spacing-2);
      font-size: var(--font-size-micro);
    }
  }
  
  /* Tablet Optimization */
  @media (min-width: 641px) and (max-width: 1024px) {
    .export-buttons-grid {
      grid-template-columns: repeat(4, 1fr);
      gap: var(--spacing-2);
    }
  }
  
  /* Desktop Enhancement */
  @media (min-width: 1025px) {
    .export-button {
      padding: var(--spacing-3) var(--spacing-4);
      min-height: 42px;
    }
    
    .export-button:hover {
      backdrop-filter: var(--glass-blur-md);
    }
  }
  
  /* Integration Styles for Chat Interface */
  .chat-header .export-buttons-container {
    margin: var(--spacing-3) 0 0 0;
  }
  
  .chat-header .export-buttons-grid {
    justify-content: center;
    max-width: 600px;
    margin: 0 auto;
  }
  
  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .export-button {
      border-width: 2px;
      background: var(--background-secondary);
    }
    
    .export-button:hover {
      border-color: var(--accent-trust);
    }
  }
  
  /* Reduced Motion Support - ALL ANIMATIONS ALREADY REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
  
  /* Performance Optimizations - GPU hints removed for performance */
  .export-button {
    /* GPU acceleration hints removed */
  }
  
  /* Animations removed for performance */
  /* @keyframes spin removed */
  
  /* Focus Management - Accessibility */
  .export-button:focus-visible {
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
  }
  
  .export-button.error:focus-visible {
    outline-color: var(--focus-ring-error);
  }
  
  .export-button.success:focus-visible {
    outline-color: var(--focus-ring-success);
  }
`;
