import { useEffect, useCallback, useState, memo, useDebugValue } from 'react';
import { AnalysisButtonsProps, AnalysisType } from '../types/chat_OpenAI';
import { usePromptAPI } from '../hooks/usePromptAPI';
import {
  useStateLogger,
  useInteractionLogger,
  usePerformanceLogger,
  useConditionalLogger
} from '../hooks/useDebugLog';
import { logger } from '../utils/logger';
import AnalysisButton, { analysisButtonStyles } from './AnalysisButton';
import SharedTickerInput, { sharedTickerInputStyles } from './SharedTickerInput';

// Define the expected order of analysis types for consistent display
const ANALYSIS_TYPE_ORDER: AnalysisType[] = [
  'snapshot',
  'support_resistance',
  'technical_analysis',
];

export default memo(function AnalysisButtons({
  onPromptGenerated,
  currentTicker,
  onTickerChange,
  className = '',
}: AnalysisButtonsProps) {
  const { templates, loading, error, refreshTemplates } = usePromptAPI();

  // ✅ React DevTools debugging (preferred for component inspection)
  useDebugValue(
    `Templates: ${templates.length}, Loading: ${loading}, Ticker: ${currentTicker}`,
    (value) => `AnalysisButtons - ${value}`
  );

  // ✅ Consolidated state logging (React best practice: single focused logger)
  useStateLogger('AnalysisButtons', 'state', {
    templatesCount: templates.length,
    loading,
    hasError: !!error,
    ticker: currentTicker
  },
  // ✅ Only log on meaningful changes (avoids Strict Mode double-logging)
  process.env.NODE_ENV === 'development' && (templates.length > 0 || !!error)
  );

  // ✅ Performance tracking (kept for actual performance measurement)
  const { startTiming, endTiming: _endTiming } = usePerformanceLogger('AnalysisButtons');

  // ✅ User interaction logging (kept for user actions)
  const logInteraction = useInteractionLogger('AnalysisButtons');

  // ✅ Simplified error logging (only when errors actually occur)
  useConditionalLogger('AnalysisButtons', !!error, 'Error state detected', {
    errorMessage: error,
    templatesCount: templates.length
  }, 'warn');
  
  // Conditional logging for successful template loads
  useConditionalLogger('AnalysisButtons', templates.length > 0 && !loading, 'Templates loaded successfully', {
    templateCount: templates.length,
    currentTicker
  }, 'info');

  // Auto-retry template loading on error after a delay
  useEffect(() => {
    if (error && !loading) {
      logger.warn('⚠️ Templates failed to load, scheduling auto-retry', {
        component: 'AnalysisButtons',
        error: error.slice(0, 100) + (error.length > 100 ? '...' : ''),
        retryDelaySeconds: 3
      });
      
      const retryTimeout = setTimeout(() => {
        logger.info('🔄 Auto-retrying template load after error');
        void refreshTemplates(); // Use void operator for floating promise
      }, 3000); // Retry after 3 seconds

      return () => {
        clearTimeout(retryTimeout);
        logger.debug('🧹 Cleared auto-retry timeout');
      };
    }
  }, [error, loading, refreshTemplates]);

  // Handle prompt generation from individual buttons
  const handlePromptGenerated = useCallback(
    (prompt: string) => {
      logInteraction('prompt_generated', 'analysis_button', {
        promptLength: prompt.length,
        promptPreview: prompt.slice(0, 80) + (prompt.length > 80 ? '...' : ''),
        currentTicker
      });
      
      logger.info('🎯 Analysis prompt generated', {
        component: 'AnalysisButtons',
        promptLength: prompt.length,
        ticker: currentTicker,
        timestamp: new Date().toISOString()
      });
      
      onPromptGenerated(prompt);
    },
    [onPromptGenerated, currentTicker, logInteraction]
  );

  // Handle retry button click
  const handleRetry = useCallback(() => {
    logInteraction('retry_templates', 'retry_button', {
      previousError: error,
      templatesCount: templates.length
    });
    
    logger.info('🔄 Manual retry triggered', {
      component: 'AnalysisButtons',
      reason: 'user_retry',
      previousError: error?.slice(0, 100) + (error && error.length > 100 ? '...' : '')
    });
    
    startTiming('template_retry');
    void refreshTemplates(); // Use void operator for floating promise
  }, [refreshTemplates, logInteraction, error, templates.length, startTiming]);

  // Collapsible state management with localStorage persistence
  const [isExpanded, setIsExpanded] = useState(() => {
    const saved = localStorage.getItem('quickAnalysisExpanded');
    const defaultExpanded = saved !== null ? JSON.parse(saved) : true;

    // ✅ Only log localStorage initialization when value actually changes from default
    if (process.env.NODE_ENV === 'development' && saved !== null && defaultExpanded !== true) {
      logger.debug('📦 Initialized expand state from localStorage', {
        component: 'AnalysisButtons',
        savedValue: saved,
        defaultExpanded
      });
    }
    
    return defaultExpanded;
  });

  // ✅ Persist expand/collapse state (minimal logging)
  useEffect(() => {
    try {
      localStorage.setItem('quickAnalysisExpanded', JSON.stringify(isExpanded));
      // ✅ Only log persistence failures (errors are meaningful)
    } catch (error) {
      logger.warn('⚠️ Failed to persist expand state to localStorage', {
        component: 'AnalysisButtons',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }, [isExpanded]);

  // Toggle expand/collapse with keyboard support
  const toggleExpanded = useCallback((event?: React.KeyboardEvent | React.MouseEvent) => {
    if (event && 'key' in event) {
      // Handle keyboard events
      if (event.key !== 'Enter' && event.key !== ' ') {
        return;
      }
      event.preventDefault();
      
      logInteraction('toggle_expanded', 'keyboard', {
        key: event.key,
        currentState: isExpanded,
        newState: !isExpanded
      });
    } else if (event) {
      logInteraction('toggle_expanded', 'mouse_click', {
        currentState: isExpanded,
        newState: !isExpanded
      });
    }
    
    logger.info(`🔄 Toggling analysis section: ${isExpanded ? 'collapsing' : 'expanding'}`, {
      component: 'AnalysisButtons',
      previousState: isExpanded,
      newState: !isExpanded,
      inputMethod: event && 'key' in event ? 'keyboard' : 'mouse'
    });
    
    setIsExpanded(prev => !prev);
  }, [isExpanded, logInteraction]);

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
  
  // Log template sorting results when templates change
  useEffect(() => {
    if (templates.length > 0) {
      const templateTypes = sortedTemplates.map(t => t.type);
      const unknownTypes = templates.filter(t => !ANALYSIS_TYPE_ORDER.includes(t.type));
      
      logger.debug('📊 Templates sorted for display', {
        component: 'AnalysisButtons',
        totalTemplates: templates.length,
        sortedOrder: templateTypes,
        unknownTypes: unknownTypes.map(t => t.type),
        predefinedOrder: ANALYSIS_TYPE_ORDER
      });
    }
  }, [templates.length, sortedTemplates]);

  // Loading state
  if (loading && templates.length === 0) {
    logger.debug('⏳ Rendering loading state', {
      component: 'AnalysisButtons',
      loading,
      templatesCount: templates.length
    });
    
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
    logger.warn('❌ Rendering error state', {
      component: 'AnalysisButtons',
      error: error.slice(0, 150) + (error.length > 150 ? '...' : ''),
      loading,
      templatesCount: templates.length
    });
    
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
    // ✅ Only log empty state when it's meaningful (not during initial load or Strict Mode cycles)
    if (process.env.NODE_ENV === 'development' && !loading && !!error) {
      logger.info('📭 Rendering empty state due to error', {
        component: 'AnalysisButtons',
        loading,
        error,
        templatesCount: templates.length
      });
    }
    
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
      {/* Integrated Ticker Input */}
      <div className='ticker-input-wrapper'>
        <SharedTickerInput
          value={currentTicker}
          onChange={(newTicker) => {
            logInteraction('ticker_change', 'ticker_input', {
              oldTicker: currentTicker,
              newTicker,
              source: 'shared_ticker_input'
            });
            
            logger.info('🏷️ Ticker changed via input', {
              component: 'AnalysisButtons',
              oldTicker: currentTicker,
              newTicker,
              timestamp: new Date().toISOString()
            });
            
            onTickerChange(newTicker);
          }}
          label='Stock Symbol'
          placeholder='NVDA'
          className='integrated-ticker-input'
          aria-describedby='ticker-help'
        />
        <div id='ticker-help' className='sr-only'>
          Enter a stock ticker symbol to use with analysis tools
        </div>
      </div>

      <div 
        className='buttons-header clickable-header'
        onClick={toggleExpanded}
        onKeyDown={toggleExpanded}
        role='button'
        aria-expanded={isExpanded}
        aria-controls='analysis-buttons-content'
        tabIndex={0}
        aria-label={`${isExpanded ? 'Collapse' : 'Expand'} Quick Analysis section`}
      >
        <div className='header-content'>
          <div className='header-left'>
            <h3 className='buttons-title'>Quick Analysis</h3>
            <p className='buttons-subtitle'>
              Click to populate your message with financial analysis prompts
              {currentTicker && (
                <span className='current-ticker'> for {currentTicker}</span>
              )}
            </p>
          </div>
          <div className={`chevron-icon ${isExpanded ? 'expanded' : 'collapsed'}`} aria-hidden='true'>
            ▶
          </div>
        </div>
      </div>

      <div 
        id='analysis-buttons-content'
        className={`collapsible-content ${isExpanded ? 'expanded' : 'collapsed'}`}
        aria-hidden={!isExpanded}
      >
        <div className='buttons-grid'>
        {sortedTemplates.map(template => (
          <AnalysisButton
            key={template.id}
            template={template}
            ticker={currentTicker}
            onPromptGenerated={handlePromptGenerated}
            isLoading={loading}
            className='grid-button'
          />
        ))}
        </div>
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
          <button 
            onClick={() => {
              logInteraction('retry_refresh_error', 'retry_button_small', {
                error: error.slice(0, 50) + (error.length > 50 ? '...' : ''),
                templatesCount: templates.length
              });
              handleRetry();
            }} 
            className='retry-button-small'
          >
            Retry
          </button>
        </div>
      )}
    </div>
  );
});

// Enhanced inline styles following existing component patterns
export const analysisButtonsStyles = `
  /* Import button styles */
  ${analysisButtonStyles}
  
  /* Import SharedTickerInput styles */
  ${sharedTickerInputStyles}

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

  /* Integrated ticker input wrapper styling */
  .analysis-buttons-container .ticker-input-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
    padding: 16px;
    background: rgba(26, 32, 44, 0.3);
    border-radius: 16px;
    border: 1px solid rgba(124, 58, 237, 0.1);
    box-shadow: 
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }

  .analysis-buttons-container .integrated-ticker-input {
    max-width: 200px;
    margin: 0;
  }

  /* Enhanced main container with sophisticated fintech card styling */
  .analysis-buttons-container {
    /* Modern glassmorphic background */
    background: rgba(26, 32, 44, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
    width: 100%;
    max-width: 100%;
    position: relative;
    /* Enhanced depth with sophisticated shadows */
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.2),
      0 2px 8px rgba(124, 58, 237, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    /* Modern container query support */
    container-type: inline-size;
    container-name: analysis-buttons;
    /* Performance optimizations */
    contain: layout style;
    box-sizing: border-box;
    /* Sophisticated transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    /* Enhanced visual hierarchy */
    overflow: hidden;
  }

  /* Sophisticated container hover state */
  .analysis-buttons-container:hover {
    background: rgba(26, 32, 44, 0.85);
    border-color: rgba(124, 58, 237, 0.3);
    transform: translateY(-2px);
    box-shadow: 
      0 12px 48px rgba(0, 0, 0, 0.25),
      0 4px 16px rgba(124, 58, 237, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.15);
  }

  /* Enhanced focus-within state */
  .analysis-buttons-container:focus-within {
    border-color: var(--accent-trust);
    box-shadow: 
      0 0 0 1px var(--accent-trust),
      0 12px 48px rgba(0, 0, 0, 0.25),
      0 4px 16px rgba(124, 58, 237, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.15);
  }

  /* Enhanced header section with fintech styling - now clickable */
  .buttons-header {
    margin-bottom: 20px;
    text-align: center;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(124, 58, 237, 0.15);
  }

  .buttons-header.clickable-header {
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 12px;
    padding: 12px 16px 16px 16px;
    margin: 0 0 20px 0;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
  }

  .buttons-header.clickable-header:hover {
    background: rgba(124, 58, 237, 0.05);
    border-color: rgba(124, 58, 237, 0.25);
  }

  .buttons-header.clickable-header:focus-visible {
    outline: 2px solid var(--accent-trust);
    outline-offset: 2px;
    background: rgba(124, 58, 237, 0.08);
  }

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  .header-left {
    flex: 1;
    text-align: left;
  }

  .buttons-title {
    margin: 0 0 8px 0;
    font-family: var(--font-display);
    font-size: var(--font-size-micro);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    letter-spacing: var(--letter-spacing-wide);
    /* Subtle gradient text effect */
    background: var(--gradient-trust);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .clickable-header .buttons-title {
    margin: 0 0 4px 0;
    text-align: left;
  }

  .buttons-subtitle {
    margin: 0;
    font-size: var(--font-size-small);
    font-family: var(--font-body);
    color: var(--text-secondary);
    line-height: var(--line-height-normal);
    letter-spacing: var(--letter-spacing-normal);
  }

  .clickable-header .buttons-subtitle {
    text-align: left;
  }

  .current-ticker {
    font-weight: var(--font-weight-semibold);
    color: var(--accent-trust);
    font-family: var(--font-mono);
    letter-spacing: var(--letter-spacing-wider);
    text-transform: uppercase;
  }

  /* Chevron icon styling */
  .chevron-icon {
    font-size: 16px;
    color: var(--text-secondary);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), color 0.2s ease;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    margin-left: 12px;
  }

  .chevron-icon.expanded {
    transform: rotate(90deg);
    color: var(--accent-trust);
  }

  .clickable-header:hover .chevron-icon {
    color: var(--accent-trust);
    background: rgba(124, 58, 237, 0.1);
  }

  /* Collapsible content container */
  .collapsible-content {
    overflow: hidden;
    transition: max-height 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s ease;
  }

  .collapsible-content.expanded {
    max-height: 1000px; /* Large enough for all content */
    opacity: 1;
  }

  .collapsible-content.collapsed {
    max-height: 0;
    opacity: 0;
  }

  /* Modern responsive button grid layout */
  .buttons-grid {
    display: grid;
    /* Use explicit responsive columns for better control */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    align-items: stretch; /* Ensure consistent button heights */
    justify-items: center;
    /* Performance optimizations */
    contain: layout style;
    /* Ensure grid stability */
    min-height: 60px; /* Prevent layout shift during loading */
  }

  .grid-button {
    width: 100%;
    max-width: none;
    /* Ensure consistent button sizing within grid */
    min-height: 60px;
    /* Performance optimization for button animations */
    will-change: transform;
    /* Better box model control */
    box-sizing: border-box;
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

  /* Enhanced mobile responsive design with fintech styling (320px-767px) */
  @media (max-width: 767px) {
    .analysis-buttons-container {
      margin: 12px 0;
      padding: 16px;
      border-radius: 16px;
      /* Enhanced mobile glassmorphic effect */
      background: rgba(26, 32, 44, 0.8);
      /* Optimize for mobile interactions */
      -webkit-tap-highlight-color: transparent;
      /* Simplified mobile shadows */
      box-shadow: 
        0 6px 24px rgba(0, 0, 0, 0.15),
        0 2px 8px rgba(124, 58, 237, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    .analysis-buttons-container:hover {
      transform: none;
      background: rgba(26, 32, 44, 0.85);
    }

    .buttons-header {
      margin-bottom: 16px;
      padding-bottom: 12px;
    }

    .buttons-header.clickable-header {
      padding: 10px 12px 12px 12px;
      border-radius: 10px;
    }

    .header-content {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }

    .header-left {
      order: 1;
      width: 100%;
    }

    .chevron-icon {
      order: 2;
      align-self: flex-end;
      margin: 0;
    }

    .buttons-title {
      font-size: calc(var(--font-size-h6) * 0.95);
    }

    .clickable-header .buttons-title {
      margin-bottom: 4px;
    }

    .buttons-subtitle {
      font-size: var(--font-size-micro);
      line-height: var(--line-height-relaxed);
    }

    .current-ticker {
      font-size: var(--font-size-small);
    }

    .chevron-icon {
      font-size: 14px;
      width: 20px;
      height: 20px;
    }
  }

    .buttons-grid {
      /* Single column for mobile with optimized spacing */
      grid-template-columns: 1fr;
      gap: 14px; /* Slightly larger gap for touch */
      justify-items: stretch; /* Full-width buttons on mobile */
      /* Minimum touch target compliance */
      min-height: 64px; /* Accommodate larger mobile buttons */
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

  /* Enhanced tablet responsive design (768px-1024px) */
  @media (min-width: 768px) and (max-width: 1024px) {
    .buttons-grid {
      /* Two columns for optimal tablet layout */
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      justify-items: stretch;
      /* Ensure consistent spacing */
      grid-auto-rows: minmax(60px, auto);
    }

    .analysis-buttons-container {
      padding: 18px; /* Balanced tablet padding */
    }
  }

  /* Enhanced desktop optimizations (1025px+) */
  @media (min-width: 1025px) {
    .buttons-grid {
      /* Three columns for desktop with refined spacing */
      grid-template-columns: repeat(3, 1fr);
      gap: 18px; /* More generous desktop spacing */
      justify-items: stretch;
      /* Consistent button heights */
      grid-auto-rows: minmax(60px, auto);
    }

    .analysis-buttons-container {
      padding: 24px; /* Generous desktop padding */
    }

    /* Desktop hover optimizations */
    .buttons-grid:hover {
      /* Subtle grid interaction feedback */
      will-change: transform;
    }
  }

  /* Large desktop optimizations (1440px+) */
  @media (min-width: 1440px) {
    .buttons-grid {
      /* Maintain 3 columns but with better spacing */
      max-width: 1200px; /* Prevent buttons from becoming too wide */
      margin: 0 auto; /* Center the grid */
      gap: 20px;
    }

    .analysis-buttons-container {
      padding: 28px;
    }
  }

  /* Ultra-wide display support (1920px+) */
  @media (min-width: 1920px) {
    .buttons-grid {
      /* Consider 4 columns for ultra-wide displays */
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      max-width: 1400px;
      gap: 24px;
    }
  }

  /* Modern container queries for component-based responsive design */
  /* These provide more precise control than viewport-based media queries */
  @container analysis-buttons (max-width: 400px) {
    .buttons-grid {
      grid-template-columns: 1fr;
      gap: 12px;
    }

    .buttons-header {
      margin-bottom: 10px;
    }

    .buttons-title {
      font-size: 14px;
    }
  }

  @container analysis-buttons (min-width: 401px) and (max-width: 600px) {
    .buttons-grid {
      grid-template-columns: 1fr;
      gap: 14px;
    }
  }

  @container analysis-buttons (min-width: 601px) and (max-width: 900px) {
    .buttons-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }
  }

  @container analysis-buttons (min-width: 901px) {
    .buttons-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }
  }

  /* Cross-platform input method optimizations */
  @media (hover: none) and (pointer: coarse) {
    /* Touch devices - enhance touch targets */
    .buttons-grid {
      gap: 16px; /* Larger gaps for touch */
    }

    .grid-button {
      min-height: 64px; /* Larger touch targets */
    }
  }

  @media (hover: hover) and (pointer: fine) {
    /* Mouse/trackpad devices - optimize for precision */
    .buttons-grid {
      gap: 14px; /* Tighter spacing for precision input */
    }
  }

  /* Enhanced accessibility and performance features */
  @media (prefers-color-scheme: dark) {
    .analysis-buttons-container {
      /* Dark mode preparation - can be activated when dark mode is implemented */
      /* background: #1a1a1a; */
      /* border-color: #404040; */
      /* color: #ffffff; */
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

  /* Enhanced reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .loading-spinner-large span,
    .refresh-spinner span {
      animation: none;
    }

    .retry-button,
    .refresh-button {
      transition: none;
    }

    /* Remove all transforms and transitions for reduced motion */
    .analysis-buttons-container {
      transition: none;
    }

    .buttons-grid:hover {
      will-change: auto;
    }

    .grid-button {
      will-change: auto;
    }
  }

  /* Print styles for better document printing */
  @media print {
    .analysis-buttons-container {
      background: white !important;
      border: 1px solid #000;
      box-shadow: none;
    }

    .loading-spinner-large,
    .refresh-spinner,
    .refresh-overlay {
      display: none;
    }
  }

  /* Forced colors mode support (Windows High Contrast) */
  @media (forced-colors: active) {
    .analysis-buttons-container {
      border: 2px solid ButtonBorder;
      background: ButtonFace;
    }

    .retry-button,
    .refresh-button {
      border: 2px solid ButtonBorder;
      background: ButtonFace;
      color: ButtonText;
    }
  }
`;
