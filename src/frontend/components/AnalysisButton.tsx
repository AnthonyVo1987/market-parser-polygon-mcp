import { useCallback } from 'react';
import { AnalysisButtonProps } from '../types/chat_OpenAI';
import { usePromptAPI, usePromptGeneration } from '../hooks/usePromptAPI';

// Map template types to expected data-testid attributes for test compatibility
const getTestId = (templateType: string): string => {
  switch (templateType) {
    case 'snapshot':
      return 'stock-snapshot-button';
    case 'support_resistance':
      return 'support-resistance-button';
    case 'technical_analysis':
    case 'technical':
      return 'technical-analysis-button';
    default:
      return `${templateType}-button`;
  }
};

export default function AnalysisButton({
  template,
  ticker,
  onPromptGenerated,
  isLoading = false,
  disabled = false,
  className = '',
}: AnalysisButtonProps) {
  const { generatePrompt, error: apiError } = usePromptAPI();
  const { isGenerating, generationError, generateWithLoading } =
    usePromptGeneration();

  // Determine if button should show loading state
  const isButtonLoading = isLoading || isGenerating;
  const isButtonDisabled = disabled || isButtonLoading || (template.requiresTicker && ticker.length < 3);

  // Handle button click to generate and populate prompt
  const handleButtonClick = useCallback(async () => {
    if (isButtonDisabled) return;

    const tickerValue = template.requiresTicker
      ? ticker.trim() || 'AAPL'
      : undefined;

    try {
      await generateWithLoading(
        () => generatePrompt(template.id, tickerValue),
        generatedPrompt => {
          onPromptGenerated(generatedPrompt);
        }
      );
    } catch (error) {
      // Error is already handled by generateWithLoading, so we just silently catch to prevent uncaught promise rejection
    }
  }, [
    template,
    ticker,
    generatePrompt,
    onPromptGenerated,
    generateWithLoading,
    isButtonDisabled,
  ]);



  const displayError = generationError || apiError;

  return (
    <div
      className={`analysis-button-container ${className}`}
      role='group'
      aria-labelledby={`button-${template.id}-label`}
    >


      {/* Main analysis button */}
      <button
        id={`button-${template.id}-label`}
        type='button'
        onClick={handleButtonClick}
        disabled={isButtonDisabled}
        className='analysis-button'
        data-testid={getTestId(template.type)}
        aria-describedby={`button-help-${template.id} ${displayError ? `error-${template.id}` : ''}`}
        title={template.description}
      >
        <span className='button-icon' aria-hidden='true'>
          {template.icon}
        </span>
        <span className='button-text'>
          {isButtonLoading ? 'Loading...' : template.name}
        </span>
        {isButtonLoading && (
          <span className='loading-spinner' aria-hidden='true'>
            <span></span>
            <span></span>
            <span></span>
          </span>
        )}
      </button>

      {/* Button help text */}
      <div id={`button-help-${template.id}`} className='sr-only'>
        {template.description}
        {template.requiresTicker ? ` Uses ticker symbol: ${ticker}` : ''}
        {isButtonLoading
          ? ' Loading prompt...'
          : ' Click to populate chat input with analysis prompt.'}
      </div>

      {/* Error display */}
      {displayError && (
        <div
          id={`error-${template.id}`}
          className='error-message'
          role='alert'
          aria-live='polite'
        >
          {displayError}
        </div>
      )}

      {/* Follow-up questions hint */}
      {template.followUpQuestions && template.followUpQuestions.length > 0 && (
        <div className='follow-up-hint'>
          <details className='follow-up-details'>
            <summary className='follow-up-summary'>
              Suggested follow-up questions
            </summary>
            <ul className='follow-up-list'>
              {template.followUpQuestions.map((question, index) => (
                <li key={index} className='follow-up-item'>
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
    max-width: 320px; /* Slightly larger for better content fit */
    /* Performance optimizations */
    contain: layout style;
    /* Better box model control */
    box-sizing: border-box;
  }



  /* Enhanced main button styling */
  .analysis-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 18px; /* More generous padding */
    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth easing */
    min-height: 48px; /* Enhanced touch-friendly minimum */
    position: relative;
    overflow: hidden;
    /* Performance optimizations */
    will-change: transform, box-shadow;
    /* Enhanced box model */
    box-sizing: border-box;
    /* Improved text rendering */
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }

  .analysis-button:not(:disabled):hover {
    background: linear-gradient(135deg, #0056b3 0%, #004494 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
  }

  /* Enhanced focus states for better accessibility */
  .analysis-button:focus-visible {
    outline: 3px solid #007bff;
    outline-offset: 2px;
    /* Ensure focus is visible in high contrast mode */
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.3);
  }

  /* Focus-within state for container when button is focused */
  .analysis-button-container:focus-within {
    /* Subtle container highlight when button is focused */
    background: rgba(0, 123, 255, 0.02);
    border-radius: 8px;
    transition: background-color 0.2s ease;
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
    outline: 3px solid #007bff;
    outline-offset: 2px;
    /* Enhanced focus visibility */
    box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.3);
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

  /* Enhanced mobile responsiveness (320px-767px) */
  @media (max-width: 767px) {
    .analysis-button-container {
      max-width: 100%;
    }

    .analysis-button {
      padding: 16px 14px; /* More generous mobile padding */
      font-size: 15px;
      min-height: 52px; /* Larger touch targets on mobile */
      /* Enhanced mobile interactions */
      -webkit-tap-highlight-color: transparent;
      /* Better mobile typography */
      letter-spacing: 0.025em;
    }

    .button-icon {
      font-size: 20px; /* Slightly larger icons on mobile */
    }
  }

  /* Tablet optimizations (768px-1024px) */
  @media (min-width: 768px) and (max-width: 1024px) {
    .analysis-button {
      padding: 15px 17px;
      min-height: 50px;
      font-size: 14.5px;
    }
  }

  /* Desktop optimizations (1025px+) */
  @media (min-width: 1025px) {
    .analysis-button {
      /* Enhanced hover effects for desktop */
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .analysis-button:not(:disabled):hover {
      /* Refined desktop hover state */
      background: linear-gradient(135deg, #0056b3 0%, #004494 100%);
      transform: translateY(-2px); /* Slightly more pronounced lift */
      box-shadow: 0 6px 16px rgba(0, 123, 255, 0.35);
    }
  }

  /* Cross-platform input method optimizations */
  @media (hover: none) and (pointer: coarse) {
    /* Touch devices - optimize for touch interaction */
    .analysis-button {
      min-height: 56px; /* Larger touch targets */
      /* Remove hover states on touch devices */
      transition: background-color 0.1s ease;
    }

    .analysis-button:not(:disabled):hover {
      /* Disable hover transform on touch devices */
      transform: none;
      background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
    }

    /* Enhanced touch feedback */
    .analysis-button:not(:disabled):active {
      background: linear-gradient(135deg, #004494 0%, #003366 100%);
      transform: scale(0.98);
    }
  }

  @media (hover: hover) and (pointer: fine) {
    /* Mouse/trackpad devices - optimize for precision */
    .analysis-button {
      /* Refined hover states for precise input devices */
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
  }

  /* Enhanced accessibility features */
  @media (prefers-color-scheme: dark) {
    /* Dark mode preparation */
    .analysis-button {
      /* Future dark mode button styling */
      /* background: linear-gradient(135deg, #0066cc 0%, #004499 100%); */
    }
  }

  /* Print styles */
  @media print {
    .analysis-button {
      background: white !important;
      color: black !important;
      border: 2px solid #000 !important;
      box-shadow: none !important;
      transform: none !important;
    }

    .loading-spinner {
      display: none;
    }
  }

  /* Forced colors mode support (Windows High Contrast) */
  @media (forced-colors: active) {
    .analysis-button {
      border: 2px solid ButtonBorder;
      background: ButtonFace;
      color: ButtonText;
      forced-color-adjust: none;
    }

    .analysis-button:focus-visible {
      outline: 3px solid Highlight;
      outline-offset: 2px;
      box-shadow: none;
    }

    .analysis-button:not(:disabled):hover {
      background: Highlight;
      color: HighlightText;
    }
  }

  /* Enhanced high contrast mode support */
  @media (prefers-contrast: high) {
    .analysis-button {
      border: 2px solid;
      background: ButtonFace;
      color: ButtonText;
    }

    .error-message {
      border-width: 2px;
      background: Mark;
      color: MarkText;
    }

    .analysis-button:focus-visible {
      outline-width: 4px;
    }
  }

  /* Enhanced reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .analysis-button {
      transition: none;
    }

    .analysis-button:not(:disabled):hover {
      transform: none;
    }

    .analysis-button:not(:disabled):active {
      transform: none;
    }

    .loading-spinner span {
      animation: none;
    }

    .analysis-button-container:focus-within {
      transition: none;
    }
  }
`;
