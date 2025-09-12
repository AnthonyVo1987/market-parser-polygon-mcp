import { useEffect, useCallback } from 'react';
import { AnalysisButtonsProps, AnalysisType } from '../types/chat_OpenAI';
import { usePromptAPI } from '../hooks/usePromptAPI';
import AnalysisButton, { analysisButtonStyles } from './AnalysisButton';

// Define the expected order of analysis types for consistent display
const ANALYSIS_TYPE_ORDER: AnalysisType[] = [
  'snapshot',
  'support_resistance',
  'technical_analysis',
];

export default function AnalysisButtons({
  onPromptGenerated,
  currentTicker,
  className = '',
}: AnalysisButtonsProps) {
  const { templates, loading, error, refreshTemplates } = usePromptAPI();

  // Auto-retry template loading on error after a delay
  useEffect(() => {
    if (error && !loading) {
      const retryTimeout = setTimeout(() => {
        void refreshTemplates(); // Use void operator for floating promise
      }, 3000); // Retry after 3 seconds

      return () => clearTimeout(retryTimeout);
    }
  }, [error, loading, refreshTemplates]);

  // Handle prompt generation from individual buttons
  const handlePromptGenerated = useCallback(
    (prompt: string) => {
      onPromptGenerated(prompt);
    },
    [onPromptGenerated]
  );

  // Handle retry button click
  const handleRetry = useCallback(() => {
    void refreshTemplates(); // Use void operator for floating promise
  }, [refreshTemplates]);

  // Sort templates by the predefined order for consistent UI
  const sortedTemplates = [...templates].sort((a, b) => {
    const aIndex = ANALYSIS_TYPE_ORDER.indexOf(a.type);
    const bIndex = ANALYSIS_TYPE_ORDER.indexOf(b.type);

    // Put known types first in order, unknown types at the end
    if (aIndex === -1 && bIndex === -1) return 0;
    if (aIndex === -1) return 1;
    if (bIndex === -1) return -1;

    return aIndex - bIndex;
  });

  // Loading state
  if (loading && templates.length === 0) {
    return (
      <div
        className={`analysis-buttons-container loading ${className}`}
        role='status'
        aria-label='Loading analysis buttons'
      >
        <div className='loading-content'>
          <div className='loading-spinner-large' aria-hidden='true'>
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p className='loading-text'>Loading analysis tools...</p>
        </div>
      </div>
    );
  }

  // Error state with retry option
  if (error && templates.length === 0) {
    return (
      <div
        className={`analysis-buttons-container error ${className}`}
        role='alert'
      >
        <div className='error-content'>
          <div className='error-icon' aria-hidden='true'>
            ⚠️
          </div>
          <p className='error-text'>Failed to load analysis tools</p>
          <p className='error-detail'>{error}</p>
          <button
            onClick={handleRetry}
            className='retry-button'
            disabled={loading}
            aria-describedby='retry-help'
          >
            {loading ? 'Retrying...' : 'Retry'}
          </button>
          <div id='retry-help' className='sr-only'>
            Click to retry loading the analysis tools
          </div>
        </div>
      </div>
    );
  }

  // No templates available
  if (templates.length === 0) {
    return (
      <div
        className={`analysis-buttons-container empty ${className}`}
        role='status'
      >
        <div className='empty-content'>
          <div className='empty-icon' aria-hidden='true'>
            📊
          </div>
          <p className='empty-text'>No analysis tools available</p>
          <button
            onClick={handleRetry}
            className='refresh-button'
            disabled={loading}
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`analysis-buttons-container loaded ${className}`}
      role='group'
      aria-label='Financial analysis tools'
    >
      <div className='buttons-header'>
        <h3 className='buttons-title'>Quick Analysis</h3>
        <p className='buttons-subtitle'>
          Click to populate your message with financial analysis prompts
          {currentTicker && (
            <span className='current-ticker'> for {currentTicker}</span>
          )}
        </p>
      </div>

      <div className='buttons-grid'>
        {sortedTemplates.map(template => (
          <AnalysisButton
            key={template.id}
            template={template}
            onPromptGenerated={handlePromptGenerated}
            isLoading={loading}
            className='grid-button'
          />
        ))}
      </div>

      {/* Loading overlay for refresh operations */}
      {loading && templates.length > 0 && (
        <div className='refresh-overlay' aria-hidden='true'>
          <div className='refresh-spinner'>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      {/* Non-blocking error notification for refresh failures */}
      {error && templates.length > 0 && (
        <div className='refresh-error' role='alert' aria-live='polite'>
          <span className='error-icon-small'>⚠️</span>
          <span className='error-text-small'>Failed to refresh: {error}</span>
          <button onClick={handleRetry} className='retry-button-small'>
            Retry
          </button>
        </div>
      )}
    </div>
  );
}

// Enhanced inline styles following existing component patterns
export const analysisButtonsStyles = `
  /* Import button styles */
  ${analysisButtonStyles}

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

  /* Main container */
  .analysis-buttons-container {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 16px;
    margin: 16px 0;
    width: 100%;
    max-width: 100%;
    position: relative;
  }

  /* Header section */
  .buttons-header {
    margin-bottom: 16px;
    text-align: center;
  }

  .buttons-title {
    margin: 0 0 4px 0;
    font-size: 16px;
    font-weight: 600;
    color: #333;
  }

  .buttons-subtitle {
    margin: 0;
    font-size: 13px;
    color: #666;
    line-height: 1.4;
  }

  .current-ticker {
    font-weight: 500;
    color: #007bff;
  }

  /* Button grid layout */
  .buttons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    align-items: start;
  }

  .grid-button {
    width: 100%;
    max-width: none;
  }

  /* Loading state */
  .analysis-buttons-container.loading {
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .loading-content {
    text-align: center;
    color: #666;
  }

  .loading-spinner-large {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin-bottom: 12px;
  }

  .loading-spinner-large span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #007bff;
    animation: loading-bounce 1.4s infinite ease-in-out;
  }

  .loading-spinner-large span:nth-child(1) {
    animation-delay: -0.32s;
  }

  .loading-spinner-large span:nth-child(2) {
    animation-delay: -0.16s;
  }

  @keyframes loading-bounce {
    0%, 80%, 100% {
      transform: scale(0);
      opacity: 0.5;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }

  .loading-text {
    margin: 0;
    font-size: 14px;
    font-weight: 500;
  }

  /* Error state */
  .analysis-buttons-container.error {
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fef2f2;
    border-color: #fecaca;
  }

  .error-content {
    text-align: center;
    max-width: 300px;
  }

  .error-icon {
    font-size: 32px;
    margin-bottom: 8px;
  }

  .error-text {
    margin: 0 0 4px 0;
    font-size: 16px;
    font-weight: 600;
    color: #dc2626;
  }

  .error-detail {
    margin: 0 0 16px 0;
    font-size: 13px;
    color: #991b1b;
    line-height: 1.4;
  }

  .retry-button {
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .retry-button:hover:not(:disabled) {
    background: #b91c1c;
  }

  .retry-button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
  }

  .retry-button:focus-visible {
    outline: 2px solid #dc2626;
    outline-offset: 2px;
  }

  /* Empty state */
  .analysis-buttons-container.empty {
    min-height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f9fafb;
  }

  .empty-content {
    text-align: center;
  }

  .empty-icon {
    font-size: 32px;
    margin-bottom: 8px;
    opacity: 0.6;
  }

  .empty-text {
    margin: 0 0 16px 0;
    font-size: 16px;
    color: #6b7280;
  }

  .refresh-button {
    background: #6b7280;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }

  .refresh-button:hover:not(:disabled) {
    background: #4b5563;
  }

  .refresh-button:focus-visible {
    outline: 2px solid #6b7280;
    outline-offset: 2px;
  }

  /* Refresh overlay */
  .refresh-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    z-index: 1;
  }

  .refresh-spinner {
    display: flex;
    gap: 4px;
  }

  .refresh-spinner span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #007bff;
    animation: loading-bounce 1.4s infinite ease-in-out;
  }

  .refresh-spinner span:nth-child(1) {
    animation-delay: -0.32s;
  }

  .refresh-spinner span:nth-child(2) {
    animation-delay: -0.16s;
  }

  /* Refresh error notification */
  .refresh-error {
    position: absolute;
    bottom: -40px;
    left: 50%;
    transform: translateX(-50%);
    background: #fee2e2;
    color: #991b1b;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    border: 1px solid #fecaca;
    display: flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 2;
  }

  .error-icon-small {
    font-size: 14px;
    flex-shrink: 0;
  }

  .error-text-small {
    flex: 1;
    min-width: 0;
  }

  .retry-button-small {
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 11px;
    cursor: pointer;
    flex-shrink: 0;
  }

  .retry-button-small:hover {
    background: #b91c1c;
  }

  /* Mobile responsive design */
  @media (max-width: 767px) {
    .analysis-buttons-container {
      margin: 8px 0;
      padding: 12px;
    }

    .buttons-header {
      margin-bottom: 12px;
    }

    .buttons-title {
      font-size: 15px;
    }

    .buttons-subtitle {
      font-size: 12px;
    }

    .buttons-grid {
      grid-template-columns: 1fr;
      gap: 12px;
    }

    .refresh-error {
      position: relative;
      bottom: auto;
      left: auto;
      transform: none;
      margin-top: 12px;
      font-size: 11px;
    }
  }

  /* Tablet responsive design */
  @media (min-width: 768px) and (max-width: 1024px) {
    .buttons-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  /* Desktop optimizations */
  @media (min-width: 1025px) {
    .buttons-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .analysis-buttons-container {
      padding: 20px;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .analysis-buttons-container {
      border-width: 2px;
    }

    .retry-button,
    .refresh-button,
    .retry-button-small {
      border: 2px solid;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .loading-spinner-large span,
    .refresh-spinner span {
      animation: none;
    }

    .retry-button,
    .refresh-button {
      transition: none;
    }
  }
`;
