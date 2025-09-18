import { useEffect, useCallback, useState, memo, useDebugValue, useMemo, useDeferredValue, startTransition } from 'react';
import { AnalysisButtonsProps, AnalysisType } from '../types/chat_OpenAI';
import { usePromptAPI } from '../hooks/usePromptAPI';
import {
  useStateLogger,
  useInteractionLogger,
  usePerformanceLogger,
  useConditionalLogger
} from '../hooks/useDebugLog';
import { logger } from '../utils/logger';
import AnalysisButton from './AnalysisButton';
import SharedTickerInput from './SharedTickerInput';
import '../styles/AnalysisButtons.css';

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
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  process.env.NODE_ENV === 'development' && (templates.length > 0 || !!error)
  );

  // ✅ Performance tracking (kept for actual performance measurement)
  const { startTiming } = usePerformanceLogger('AnalysisButtons');

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
        error: typeof error === 'string' ? error.slice(0, 100) + (error.length > 100 ? '...' : '') : 'Unknown error',
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
      previousError: error && typeof error === 'string' ? error.slice(0, 100) + (error.length > 100 ? '...' : '') : 'Unknown error'
    });
    
    startTiming('template_retry');
    void refreshTemplates(); // Use void operator for floating promise
  }, [refreshTemplates, logInteraction, error, templates.length, startTiming]);

  // Collapsible state management with localStorage persistence
  const [isExpanded, setIsExpanded] = useState(() => {
    try {
      const saved = localStorage.getItem('quickAnalysisExpanded');
      const defaultExpanded = saved !== null ? JSON.parse(saved) as boolean : true;

      // ✅ Only log localStorage initialization when value actually changes from default
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      if (process.env.NODE_ENV === 'development' && saved !== null && defaultExpanded !== true) {
        logger.debug('📦 Initialized expand state from localStorage', {
          component: 'AnalysisButtons',
          savedValue: saved,
          defaultExpanded
        });
      }
      
      return defaultExpanded;
    } catch (error) {
      logger.warn('⚠️ Failed to parse localStorage expand state, using default', {
        component: 'AnalysisButtons',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
      return true;
    }
  });

  // ✅ Persist expand/collapse state (minimal logging)
  useEffect(() => {
    try {
      localStorage.setItem('quickAnalysisExpanded', JSON.stringify(isExpanded));
      // ✅ Only log persistence failures (errors are meaningful)
    } catch (storageError) {
      logger.warn('⚠️ Failed to persist expand state to localStorage', {
        component: 'AnalysisButtons',
        error: storageError instanceof Error ? storageError.message : 'Unknown error'
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

  // Memoize expensive template sorting operation
  const sortedTemplates = useMemo(() => {
    return [...templates].sort((a, b) => {
      const aIndex = ANALYSIS_TYPE_ORDER.indexOf(a.type);
      const bIndex = ANALYSIS_TYPE_ORDER.indexOf(b.type);

      // Put known types first in order, unknown types at the end
      if (aIndex === -1 && bIndex === -1) return 0;
      if (aIndex === -1) return 1;
      if (bIndex === -1) return -1;

      return aIndex - bIndex;
    });
  }, [templates]);
  
  // Use deferred value for ticker to improve input responsiveness
  const deferredTicker = useDeferredValue(currentTicker);
  
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
  }, [templates, sortedTemplates]);

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
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
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
            // Immediate UI update for responsiveness
            onTickerChange(newTicker);
            
            // Defer non-critical operations
            startTransition(() => {
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
            });
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
                <span className='current-ticker'> for {deferredTicker}</span>
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
            ticker={deferredTicker}
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
                error: typeof error === 'string' ? error.slice(0, 50) + (error.length > 50 ? '...' : '') : 'Unknown error',
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

