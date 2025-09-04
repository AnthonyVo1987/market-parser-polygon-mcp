import { useState, useCallback } from 'react';
import { AnalysisButtonProps } from '../types/chat_OpenAI';
import { usePromptAPI, usePromptGeneration } from '../hooks/usePromptAPI';

export default function AnalysisButton({
  template,
  onPromptGenerated,
  isLoading = false,
  disabled = false,
  className = '',
}: AnalysisButtonProps) {
  const { generatePrompt, error: apiError } = usePromptAPI();
  const { isGenerating, generationError, generateWithLoading } = usePromptGeneration();
  const [currentTicker, setCurrentTicker] = useState<string>('');

  // Determine if button should show loading state
  const isButtonLoading = isLoading || isGenerating;
  const isButtonDisabled = disabled || isButtonLoading;

  // Handle button click to generate and populate prompt
  const handleButtonClick = useCallback(async () => {
    if (isButtonDisabled) return;

    const ticker = template.requiresTicker ? currentTicker.trim() || 'AAPL' : undefined;

    try {
      await generateWithLoading(
        () => generatePrompt(template.id, ticker),
        (generatedPrompt) => {
          onPromptGenerated(generatedPrompt);
        }
      );
    } catch (error) {
      // Error is already handled by generateWithLoading, so we just silently catch to prevent uncaught promise rejection
    }
  }, [template, currentTicker, generatePrompt, onPromptGenerated, generateWithLoading, isButtonDisabled]);

  // Handle ticker input change
  const handleTickerChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    setCurrentTicker(value);
  }, []);

  // Handle ticker input key press (Enter to trigger button)
  const handleTickerKeyPress = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isButtonDisabled) {
      void handleButtonClick(); // Use void operator for floating promise
    }
  }, [handleButtonClick, isButtonDisabled]);

  const displayError = generationError || apiError;

  return (
    <div className={`analysis-button-container ${className}`} role="group" aria-labelledby={`button-${template.id}-label`}>
      {/* Ticker input for templates that require it */}
      {template.requiresTicker && (
        <div className="ticker-input-container">
          <label htmlFor={`ticker-${template.id}`} className="ticker-label">
            Stock Symbol:
          </label>
          <input
            id={`ticker-${template.id}`}
            type="text"
            value={currentTicker}
            onChange={handleTickerChange}
            onKeyPress={handleTickerKeyPress}
            placeholder="AAPL"
            maxLength={10}
            className="ticker-input"
            disabled={isButtonDisabled}
            aria-describedby={`ticker-help-${template.id}`}
          />
          <div id={`ticker-help-${template.id}`} className="sr-only">
            Enter a stock symbol (letters and numbers only). Press Enter to generate analysis.
          </div>
        </div>
      )}

      {/* Main analysis button */}
      <button
        id={`button-${template.id}-label`}
        type="button"
        onClick={handleButtonClick}
        disabled={isButtonDisabled}
        className="analysis-button"
        aria-describedby={`button-help-${template.id} ${displayError ? `error-${template.id}` : ''}`}
        title={template.description}
      >
        <span className="button-icon" aria-hidden="true">
          {template.icon}
        </span>
        <span className="button-text">
          {isButtonLoading ? 'Loading...' : template.name}
        </span>
        {isButtonLoading && (
          <span className="loading-spinner" aria-hidden="true">
            <span></span>
            <span></span>
            <span></span>
          </span>
        )}
      </button>

      {/* Button help text */}
      <div id={`button-help-${template.id}`} className="sr-only">
        {template.description}
        {template.requiresTicker ? ' Enter a ticker symbol first.' : ''}
        {isButtonLoading ? ' Loading prompt...' : ' Click to populate chat input with analysis prompt.'}
      </div>

      {/* Error display */}
      {displayError && (
        <div
          id={`error-${template.id}`}
          className="error-message"
          role="alert"
          aria-live="polite"
        >
          {displayError}
        </div>
      )}

      {/* Follow-up questions hint */}
      {template.followUpQuestions && template.followUpQuestions.length > 0 && (
        <div className="follow-up-hint">
          <details className="follow-up-details">
            <summary className="follow-up-summary">Suggested follow-up questions</summary>
            <ul className="follow-up-list">
              {template.followUpQuestions.map((question, index) => (
                <li key={index} className="follow-up-item">
                  {question}
                </li>
              ))}
            </ul>
          </details>
        </div>
      )}
    </div>
  );
}

// Enhanced inline styles following existing patterns
export const analysisButtonStyles = `
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

  .analysis-button-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
    width: 100%;
    max-width: 280px;
  }

  /* Ticker input styling */
  .ticker-input-container {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .ticker-label {
    font-size: 12px;
    font-weight: 500;
    color: #666;
    margin-bottom: 2px;
  }

  .ticker-input {
    padding: 6px 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    text-align: center;
    text-transform: uppercase;
    background: white;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .ticker-input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }

  .ticker-input:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
  }

  .ticker-input:disabled {
    background-color: #f5f5f5;
    color: #999;
    cursor: not-allowed;
  }

  /* Main button styling */
  .analysis-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 44px; /* Touch-friendly minimum */
    position: relative;
    overflow: hidden;
  }

  .analysis-button:not(:disabled):hover {
    background: linear-gradient(135deg, #0056b3 0%, #004494 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
  }

  .analysis-button:not(:disabled):active {
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(0, 123, 255, 0.3);
  }

  .analysis-button:disabled {
    background: linear-gradient(135deg, #ccc 0%, #999 100%);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .analysis-button:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
  }

  /* Button content styling */
  .button-icon {
    font-size: 18px;
    flex-shrink: 0;
  }

  .button-text {
    flex: 1;
    text-align: center;
  }

  /* Loading spinner styling */
  .loading-spinner {
    display: flex;
    gap: 3px;
    margin-left: 8px;
  }

  .loading-spinner span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.8);
    animation: loading-pulse 1.4s infinite ease-in-out;
  }

  .loading-spinner span:nth-child(1) {
    animation-delay: -0.32s;
  }

  .loading-spinner span:nth-child(2) {
    animation-delay: -0.16s;
  }

  @keyframes loading-pulse {
    0%, 80%, 100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }

  /* Error message styling */
  .error-message {
    background-color: #fee;
    color: #c33;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    border: 1px solid #fcc;
  }

  /* Follow-up questions styling */
  .follow-up-hint {
    margin-top: 4px;
  }

  .follow-up-details {
    font-size: 12px;
    color: #666;
  }

  .follow-up-summary {
    cursor: pointer;
    padding: 4px 0;
    font-weight: 500;
    border-bottom: 1px dotted #ccc;
    margin-bottom: 6px;
  }

  .follow-up-summary:hover {
    color: #007bff;
  }

  .follow-up-list {
    list-style: none;
    padding: 0;
    margin: 0;
    gap: 4px;
    display: flex;
    flex-direction: column;
  }

  .follow-up-item {
    padding: 4px 8px;
    background: #f8f9fa;
    border-radius: 6px;
    font-size: 11px;
    line-height: 1.3;
  }

  /* Mobile responsiveness */
  @media (max-width: 767px) {
    .analysis-button-container {
      max-width: 100%;
    }

    .analysis-button {
      padding: 14px 12px;
      font-size: 15px;
      min-height: 48px; /* Larger touch targets on mobile */
    }

    .ticker-input {
      padding: 10px 12px;
      font-size: 16px; /* Prevents iOS zoom */
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .analysis-button {
      border: 2px solid;
    }

    .ticker-input {
      border: 2px solid;
    }

    .error-message {
      border-width: 2px;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .analysis-button,
    .ticker-input {
      transition: none;
    }

    .analysis-button:not(:disabled):hover {
      transform: none;
    }

    .loading-spinner span {
      animation: none;
    }
  }
`;