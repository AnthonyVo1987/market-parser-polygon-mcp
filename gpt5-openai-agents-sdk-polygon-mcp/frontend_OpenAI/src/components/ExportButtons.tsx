import { useState, useCallback, useRef, useEffect } from 'react';
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

export default function ExportButtons({ messages }: ExportButtonsProps) {
  const [buttonStates, setButtonStates] = useState<ButtonStates>({
    copyMd: 'idle',
    copyJson: 'idle',
    saveMd: 'idle',
    saveJson: 'idle',
  });

  const [errorMessages, setErrorMessages] = useState<Record<string, string>>({});
  
  // Refs to store timeout IDs for cleanup
  const timeoutRefs = useRef<Record<keyof ButtonStates, number | null>>({
    copyMd: null,
    copyJson: null,
    saveMd: null,
    saveJson: null,
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

  const handleCopyMarkdown = useCallback(async () => {
    const buttonId = 'copyMd';
    updateButtonState(buttonId, 'loading');

    try {
      validateMessages(messages);
      const markdownContent = convertToMarkdown(messages);
      await copyToClipboard(markdownContent);
      updateButtonState(buttonId, 'success');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to copy markdown';
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
      const errorMessage = error instanceof Error ? error.message : 'Failed to copy JSON';
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
      const errorMessage = error instanceof Error ? error.message : 'Failed to save markdown';
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
      const errorMessage = error instanceof Error ? error.message : 'Failed to save JSON';
      updateButtonState(buttonId, 'error', errorMessage);
    }
  }, [messages, updateButtonState]);

  const isDisabled = messages.length === 0;

  const getButtonText = (buttonId: keyof ButtonStates, defaultText: string): string => {
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
    <div className="export-buttons-container">
      <div className="export-buttons-grid">
        {/* Copy to Clipboard - Markdown */}
        <button
          onClick={handleCopyMarkdown}
          disabled={isDisabled || buttonStates.copyMd === 'loading'}
          className={getButtonClass('copyMd')}
          title={isDisabled ? 'No messages to export' : 'Copy chat as markdown to clipboard'}
          aria-label="Copy chat as markdown to clipboard"
        >
          📋 {getButtonText('copyMd', 'Copy MD')}
        </button>

        {/* Copy to Clipboard - JSON */}
        <button
          onClick={handleCopyJSON}
          disabled={isDisabled || buttonStates.copyJson === 'loading'}
          className={getButtonClass('copyJson')}
          title={isDisabled ? 'No messages to export' : 'Copy chat as JSON to clipboard'}
          aria-label="Copy chat as JSON to clipboard"
        >
          📋 {getButtonText('copyJson', 'Copy JSON')}
        </button>

        {/* Save to File - Markdown */}
        <button
          onClick={handleSaveMarkdown}
          disabled={isDisabled || buttonStates.saveMd === 'loading'}
          className={getButtonClass('saveMd')}
          title={isDisabled ? 'No messages to export' : 'Save chat as markdown file'}
          aria-label="Save chat as markdown file"
        >
          💾 {getButtonText('saveMd', 'Save MD')}
        </button>

        {/* Save to File - JSON */}
        <button
          onClick={handleSaveJSON}
          disabled={isDisabled || buttonStates.saveJson === 'loading'}
          className={getButtonClass('saveJson')}
          title={isDisabled ? 'No messages to export' : 'Save chat as JSON file'}
          aria-label="Save chat as JSON file"
        >
          💾 {getButtonText('saveJson', 'Save JSON')}
        </button>
      </div>

      {/* Error Messages Display */}
      {Object.entries(errorMessages).map(([buttonId, errorMessage]) => (
        errorMessage && buttonStates[buttonId as keyof ButtonStates] === 'error' ? (
          <div key={buttonId} className="export-error-message">
            <strong>Export Error:</strong> {errorMessage}
          </div>
        ) : null
      ))}

      {/* Empty State Message */}
      {isDisabled && (
        <div className="export-empty-state">
          Start a conversation to enable export options
        </div>
      )}
    </div>
  );
}

// Inline styles for integration with existing components
export const exportButtonStyles = `
  .export-buttons-container {
    margin: 8px 0;
    padding: 0;
  }
  
  .export-buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 8px;
    max-width: 100%;
  }
  
  @media (max-width: 640px) {
    .export-buttons-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 6px;
    }
  }
  
  .export-button {
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
  }
  
  .export-button:not(.disabled):not(.loading):hover {
    background-color: #0056b3;
    transform: translateY(-1px);
  }
  
  .export-button.disabled {
    background-color: #ccc;
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .export-button.loading {
    background-color: #6c757d;
    cursor: wait;
    position: relative;
  }
  
  .export-button.loading::after {
    content: '';
    width: 12px;
    height: 12px;
    border: 2px solid transparent;
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-left: 4px;
  }
  
  .export-button.success {
    background-color: #28a745;
    cursor: default;
  }
  
  .export-button.success:hover {
    background-color: #28a745;
    transform: none;
  }
  
  .export-button.error {
    background-color: #dc3545;
    cursor: pointer;
  }
  
  .export-button.error:hover {
    background-color: #c82333;
  }
  
  .export-error-message {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
    padding: 8px 12px;
    margin-top: 8px;
    font-size: 12px;
    text-align: left;
  }
  
  .export-empty-state {
    text-align: center;
    color: #6c757d;
    font-size: 12px;
    margin-top: 8px;
    font-style: italic;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Integration styles for chat header */
  .chat-header .export-buttons-container {
    margin: 12px 0 0 0;
  }
  
  .chat-header .export-buttons-grid {
    justify-content: center;
    max-width: 500px;
    margin: 0 auto;
  }
`;