import React, { memo, useCallback, useState } from 'react';
import { AnalysisButtonProps } from '../types/chat_OpenAI';

// Map template types to expected data-testid attributes for test compatibility
const getTestId = (templateType: string): string => {
  switch (templateType) {
    case 'snapshot':
      return 'analysis-button-snapshot';
    case 'support_resistance':
      return 'analysis-button-support-resistance';
    case 'technical_analysis':
    case 'technical':
      return 'analysis-button-technical';
    default:
      return `analysis-button-${templateType}`;
  }
};

const AnalysisButton = memo(function AnalysisButton({
  template,
  ticker,
  onPromptGenerated,
  isLoading = false,
  disabled = false,
  className = '',
}: AnalysisButtonProps) {
  const [showSuccess, setShowSuccess] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  // Determine if button should show loading state
  const isButtonLoading = isLoading;
  const isButtonDisabled =
    disabled ||
    isButtonLoading ||
    (template.requiresTicker && ticker.length < 3);

  // Handle button click to generate and populate prompt
  const handleButtonClick = useCallback(() => {
    if (isButtonDisabled) return;

    // Clear any existing states
    setHasError(false);
    setShowSuccess(false);

    const tickerValue = template.requiresTicker
      ? ticker.trim() || 'AAPL'
      : undefined;

    try {
      // Generate prompt from static template
      const generatedPrompt = template.template.replace('{ticker}', tickerValue || 'the selected stock');

      // Call the onPromptGenerated callback
      onPromptGenerated(generatedPrompt);

      // Show success feedback
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 1000);
    } catch (error) {
      // Show error feedback
      setHasError(true);
      setTimeout(() => setHasError(false), 1000);
    }
  }, [
    template,
    ticker,
    onPromptGenerated,
    isButtonDisabled,
  ]);

  // Mouse event handlers for enhanced hover state
  const handleMouseEnter = useCallback(() => {
    setIsHovered(true);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setIsHovered(false);
  }, []);

  // No error handling needed for static templates
  const displayError = null;

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
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        disabled={isButtonDisabled}
        className={`analysis-button ${showSuccess ? 'button-success' : ''} ${hasError ? 'button-error' : ''
          } ${isHovered ? 'button-hovered' : ''}`}
        data-testid={getTestId(template.type)}
        aria-describedby={`button-help-${template.id} ${displayError ? `error-${template.id}` : ''}`}
        title={template.description}
      >
        <span className='button-icon' aria-hidden='true'>
          {template.icon}
        </span>
        <span className='button-text'>
          {isButtonLoading
            ? 'Loading...'
            : showSuccess
              ? 'Generated!'
              : template.name}
        </span>
        {isButtonLoading && (
          <span className='loading-spinner' aria-hidden='true'>
            Loading...
          </span>
        )}
        {showSuccess && !isButtonLoading && (
          <span className='success-indicator' aria-hidden='true'>
            ✓
          </span>
        )}
        {hasError && !isButtonLoading && (
          <span className='error-indicator' aria-hidden='true'>
            ⚠
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
    </div>
  );
});

AnalysisButton.displayName = 'AnalysisButton';

export default AnalysisButton;

// Enhanced fintech-grade inline styles with sophisticated design system integration
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

  /* Enhanced container with glassmorphic card styling */
  .analysis-button-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 16px;
    width: 100%;
    max-width: 340px;
    /* Modern glassmorphic card background */
    background: rgba(45, 55, 72, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(124, 58, 237, 0.15);
    border-radius: 16px;
    padding: 4px;
    /* Enhanced shadows for depth */
    box-shadow: 
      0 4px 20px rgba(0, 0, 0, 0.15),
      0 1px 4px rgba(124, 58, 237, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.05);
    /* Performance optimizations */
    contain: layout style;
    box-sizing: border-box;
    /* Smooth transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .analysis-button-container:hover {
    background: rgba(45, 55, 72, 0.75);
    border-color: rgba(124, 58, 237, 0.25);
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.2),
      0 2px 8px rgba(124, 58, 237, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
  }



  /* Enhanced main button with trust gradient and neumorphic styling */
  .analysis-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 16px 20px;
    /* Trust gradient from design system */
    background: var(--gradient-trust);
    color: var(--text-primary);
    border: 1px solid var(--accent-trust);
    border-radius: 12px;
    /* Enhanced typography */
    font-family: var(--font-body);
    font-size: var(--font-size-body);
    font-weight: var(--font-weight-semibold);
    letter-spacing: var(--letter-spacing-wide);
    cursor: pointer;
    /* Sophisticated transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 56px;
    position: relative;
    overflow: hidden;
    /* Enhanced shadows with trust color */
    box-shadow: 
      0 4px 14px rgba(124, 58, 237, 0.25),
      0 2px 6px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    /* Performance optimizations */
    will-change: transform, box-shadow, background;
    box-sizing: border-box;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    /* Subtle text shadow for depth */
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  /* Sophisticated hover state with enhanced trust colors */
  .analysis-button:not(:disabled):hover {
    background: linear-gradient(135deg, var(--accent-trust-hover) 0%, var(--accent-info) 100%);
    border-color: var(--accent-trust-hover);
    transform: translateY(-2px) scale(1.02);
    box-shadow: 
      0 8px 25px rgba(124, 58, 237, 0.35),
      0 4px 12px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    /* Enhanced glow effect */
    filter: brightness(1.05);
  }

  /* Enhanced focus states using design system */
  .analysis-button:focus-visible {
    outline: 3px solid var(--focus-ring);
    outline-offset: 3px;
    box-shadow: 
      0 0 0 4px rgba(124, 58, 237, 0.2),
      0 8px 25px rgba(124, 58, 237, 0.35),
      0 4px 12px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  /* Enhanced focus-within state for container */
  .analysis-button-container:focus-within {
    background: rgba(45, 55, 72, 0.8);
    border-color: var(--accent-trust);
    box-shadow: 
      0 0 0 1px var(--accent-trust),
      0 8px 32px rgba(0, 0, 0, 0.2),
      0 2px 8px rgba(124, 58, 237, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
  }

  /* Active state with subtle press effect */
  .analysis-button:not(:disabled):active {
    transform: translateY(-1px) scale(0.98);
    box-shadow: 
      0 4px 14px rgba(124, 58, 237, 0.25),
      0 2px 6px rgba(0, 0, 0, 0.1),
      inset 0 2px 4px rgba(0, 0, 0, 0.1);
    filter: brightness(0.95);
  }

  /* Enhanced disabled state */
  .analysis-button:disabled {
    background: var(--accent-trust-disabled);
    border-color: var(--accent-trust-disabled);
    color: rgba(247, 250, 252, 0.6);
    cursor: not-allowed;
    transform: none;
    filter: none;
    box-shadow: 
      0 2px 8px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.05);
    text-shadow: none;
  }

  /* Enhanced button content styling with better typography */
  .button-icon {
    font-size: 20px;
    flex-shrink: 0;
    /* Enhanced icon contrast */
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .analysis-button:hover .button-icon,
  .analysis-button.button-hovered .button-icon {
    transform: scale(1.1) rotate(2deg);
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  }
  
  /* Success state icon animation */
  .analysis-button.button-success .button-icon {
    transform: scale(1.2) rotate(10deg);
    filter: drop-shadow(0 0 8px rgba(34, 197, 94, 0.5));
  }
  
  /* Error state icon animation */
  .analysis-button.button-error .button-icon {
    transform: scale(1.1) rotate(-5deg);
    filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.5));
    /* Animation removed for performance */
  }
  
  /* @keyframes icon-error-shake removed for performance */

  .button-text {
    flex: 1;
    text-align: center;
    font-weight: var(--font-weight-semibold);
    letter-spacing: var(--letter-spacing-wide);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
  }
  
  /* Success text animation */
  .analysis-button.button-success .button-text {
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 0 8px rgba(34, 197, 94, 0.3);
  }
  
  /* Error text animation */
  .analysis-button.button-error .button-text {
    color: rgba(255, 255, 255, 0.95);
    text-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
  }

  /* Static loading indicator */
  .loading-spinner {
    display: inline-block;
    margin-left: 10px;
    font-size: 16px;
    color: rgba(255, 255, 255, 0.9);
  }

  /* Loading spinner animation delays removed for performance */

  /* @keyframes sophisticated-loading removed for performance */
  
  /* Success indicator styling */
  .success-indicator {
    font-size: 18px;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.95);
    /* Animation removed for performance */
    filter: drop-shadow(0 0 6px rgba(34, 197, 94, 0.6));
    margin-left: 8px;
  }
  
  /* @keyframes success-appear removed for performance */
  
  /* Error indicator styling */
  .error-indicator {
    font-size: 18px;
    font-weight: bold;
    color: rgba(255, 255, 255, 0.95);
    /* Animation removed for performance */
    filter: drop-shadow(0 0 6px rgba(239, 68, 68, 0.6));
    margin-left: 8px;
  }
  
  /* @keyframes error-appear removed for performance */

  /* Enhanced error message with design system colors */
  .error-message {
    background: var(--gradient-error-subtle);
    color: var(--accent-error);
    padding: 12px 16px;
    border-radius: 10px;
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-medium);
    border: 1px solid var(--accent-error);
    box-shadow: 
      0 2px 8px rgba(239, 68, 68, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    margin-top: 8px;
  }



  /* Financial semantic button variants */
  .analysis-button.bullish {
    background: var(--gradient-success);
    border-color: var(--accent-success);
    box-shadow: 
      0 4px 14px rgba(16, 185, 129, 0.25),
      0 2px 6px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .analysis-button.bullish:not(:disabled):hover {
    background: linear-gradient(135deg, var(--accent-success-hover) 0%, var(--financial-bullish-3) 100%);
    box-shadow: 
      0 8px 25px rgba(16, 185, 129, 0.35),
      0 4px 12px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .analysis-button.bearish {
    background: var(--gradient-error);
    border-color: var(--accent-error);
    box-shadow: 
      0 4px 14px rgba(239, 68, 68, 0.25),
      0 2px 6px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .analysis-button.bearish:not(:disabled):hover {
    background: linear-gradient(135deg, var(--accent-error-hover) 0%, var(--financial-bearish-3) 100%);
    box-shadow: 
      0 8px 25px rgba(239, 68, 68, 0.35),
      0 4px 12px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .analysis-button.neutral {
    background: var(--gradient-surface-2);
    border-color: var(--neutral-color);
    color: var(--text-secondary);
    box-shadow: 
      0 4px 14px rgba(160, 174, 192, 0.15),
      0 2px 6px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .analysis-button.neutral:not(:disabled):hover {
    background: var(--gradient-surface-3);
    color: var(--text-primary);
    transform: translateY(-2px);
  }

  /* Enhanced mobile responsiveness with fintech styling (320px-767px) */
  @media (max-width: 767px) {
    .analysis-button-container {
      max-width: 100%;
      margin-bottom: 12px;
      padding: 3px;
      border-radius: 14px;
    }

    .analysis-button {
      padding: 18px 16px;
      font-size: var(--font-size-body);
      min-height: 60px;
      gap: 8px;
      /* Enhanced mobile interactions */
      -webkit-tap-highlight-color: transparent;
      /* Mobile-optimized shadows */
      box-shadow: 
        0 3px 12px rgba(124, 58, 237, 0.2),
        0 1px 4px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .analysis-button:not(:disabled):hover {
      /* Simplified hover for mobile */
      transform: translateY(-1px);
      box-shadow: 
        0 4px 16px rgba(124, 58, 237, 0.25),
        0 2px 6px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }

    .button-icon {
      font-size: 22px;
    }

    .follow-up-hint {
      padding: 10px;
      border-radius: 10px;
    }
  }

  /* Enhanced tablet optimizations (768px-1024px) */
  @media (min-width: 768px) and (max-width: 1024px) {
    .analysis-button-container {
      max-width: 360px;
    }

    .analysis-button {
      padding: 16px 18px;
      min-height: 54px;
      font-size: var(--font-size-body);
    }

    .button-icon {
      font-size: 20px;
    }
  }

  /* Enhanced desktop optimizations with sophisticated effects (1025px+) */
  @media (min-width: 1025px) {
    .analysis-button-container {
      max-width: 380px;
    }

    .analysis-button {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .analysis-button:not(:disabled):hover,
    .analysis-button.button-hovered:not(:disabled) {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 
        0 12px 40px rgba(124, 58, 237, 0.4),
        0 6px 16px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.25);
      filter: brightness(1.1) saturate(1.1);
    }

    .analysis-button-container:hover {
      transform: translateY(-2px);
      box-shadow: 
        0 12px 48px rgba(0, 0, 0, 0.25),
        0 4px 12px rgba(124, 58, 237, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }

    /* Enhanced desktop icon animations */
    .analysis-button:hover .button-icon,
    .analysis-button.button-hovered .button-icon {
      transform: scale(1.15) rotate(5deg);
    }
    
    /* Desktop success state enhancement */
    .analysis-button.button-success:not(:disabled) {
      transform: translateY(-4px) scale(1.03);
      box-shadow: 
        0 16px 48px rgba(34, 197, 94, 0.4),
        0 8px 20px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
      filter: brightness(1.15) saturate(1.2);
    }
    
    /* Desktop error state enhancement */
    .analysis-button.button-error:not(:disabled) {
      transform: translateY(-2px) scale(1.01);
      box-shadow: 
        0 12px 32px rgba(239, 68, 68, 0.4),
        0 6px 16px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.25);
      filter: brightness(1.05) saturate(1.1);
    }
  }

  /* Enhanced cross-platform optimizations with fintech styling */
  @media (hover: none) and (pointer: coarse) {
    /* Touch devices - enhanced touch interaction with trust colors */
    .analysis-button {
      min-height: 64px;
      /* Simplified transitions for touch */
      transition: background-color 0.2s ease, transform 0.1s ease;
    }

    .analysis-button:not(:disabled):hover {
      /* Maintain original styling on touch hover */
      transform: none;
      background: var(--gradient-trust);
      box-shadow: 
        0 4px 14px rgba(124, 58, 237, 0.25),
        0 2px 6px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    /* Enhanced touch feedback with trust gradient */
    .analysis-button:not(:disabled):active {
      background: linear-gradient(135deg, var(--accent-trust-active) 0%, var(--accent-info-active) 100%);
      transform: scale(0.96);
      box-shadow: 
        0 2px 8px rgba(124, 58, 237, 0.3),
        inset 0 2px 4px rgba(0, 0, 0, 0.15);
    }

    .analysis-button-container:hover {
      transform: none;
    }
  }

  @media (hover: hover) and (pointer: fine) {
    /* Precision input devices - sophisticated hover states */
    .analysis-button {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .analysis-button-container {
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Enhanced precision hover effects */
    .analysis-button:not(:disabled):hover {
      background: linear-gradient(135deg, var(--accent-trust-hover) 0%, var(--accent-info-hover) 100%);
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
    
    .button-icon {
      transition: none;
      animation: none;
    }
    
    .analysis-button.button-success .button-icon,
    .analysis-button.button-error .button-icon {
      transform: none;
      animation: none;
    }
    
    .success-indicator,
    .error-indicator {
      animation: none;
    }
    
    .button-text {
      transition: none;
    }
  }
`;
