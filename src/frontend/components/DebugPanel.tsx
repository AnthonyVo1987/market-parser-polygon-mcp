import { memo, useCallback, useEffect, useState } from 'react';
import { useComponentLogger } from '../hooks/useDebugLog';
import { AIModel, AIModelId } from '../types/ai_models';
import { logger, LogMode } from '../utils/logger';

/**
 * Props interface for the DebugPanel component
 */
interface DebugPanelProps {
  /** The most recent AI response time in seconds, or null if no responses yet */
  latestResponseTime: number | null;
  /** Additional CSS classes to apply to the component */
  className?: string;
  /** Optional callback for debug actions */
  onDebugAction?: (action: string, details: Record<string, unknown>) => void;
  // AI Model props
  models: readonly AIModel[];
  currentModel: AIModelId | null;
  onModelChange: (modelId: AIModelId) => void;
  isLoadingModels?: boolean;
  modelError?: string | null;
}

/**
 * DebugPanel component - displays developer information including the latest AI response time
 * 
 * This component is designed for debugging and monitoring during development.
 * It shows the processing time of the most recent AI response in a developer-friendly format.
 * 
 * @param props - The component props
 * @returns JSX element displaying debug information
 */
const DebugPanel = memo<DebugPanelProps>(({
  latestResponseTime,
  className = '',
  onDebugAction: _onDebugAction,
  models,
  currentModel,
  onModelChange,
  isLoadingModels = false,
  modelError = null
}) => {
  // Initialize logging
  useComponentLogger('DebugPanel', {
    hasResponseTime: latestResponseTime !== null,
    responseTime: latestResponseTime,
    currentModel,
    modelCount: models.length
  });
  // const _logInteraction = useInteractionLogger('DebugPanel');

  // Console log mode state management
  const [logMode, setLogMode] = useState<LogMode>(() => logger.getLogMode());

  // Collapsible state management with localStorage persistence
  const [isExpanded, setIsExpanded] = useState(() => {
    try {
      const saved = localStorage.getItem('debugPanelExpanded');
      const defaultExpanded = saved !== null ? JSON.parse(saved) as boolean : true;

      logger.debug('🔧 DebugPanel initialized', {
        component: 'DebugPanel',
        expanded: defaultExpanded,
        hasResponseTime: latestResponseTime !== null,
        responseTime: latestResponseTime,
        logMode: logMode
      });

      return defaultExpanded;
    } catch (error) {
      logger.warn('⚠️ Failed to parse DebugPanel localStorage state', {
        component: 'DebugPanel',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
      return true;
    }
  });

  // Persist expand/collapse state
  useEffect(() => {
    localStorage.setItem('debugPanelExpanded', JSON.stringify(isExpanded));
  }, [isExpanded]);

  // Listen for log mode changes from logger
  useEffect(() => {
    const unsubscribe = logger.onLogModeChange((newMode: LogMode) => {
      setLogMode(newMode);
    });

    return unsubscribe;
  }, []);

  // Toggle expand/collapse with keyboard support
  const toggleExpanded = useCallback((event?: React.KeyboardEvent | React.MouseEvent) => {
    if (event && 'key' in event) {
      // Handle keyboard events
      if (event.key !== 'Enter' && event.key !== ' ') {
        return;
      }
      event.preventDefault();
    }
    setIsExpanded(prev => !prev);
  }, []);

  // Toggle log mode cycling through NONE → DEBUG → PRODUCTION → NONE
  const toggleLogMode = useCallback((event?: React.KeyboardEvent | React.MouseEvent) => {
    if (event && 'key' in event) {
      // Handle keyboard events
      if (event.key !== 'Enter' && event.key !== ' ') {
        return;
      }
      event.preventDefault();
    }

    // Cycle through modes: NONE → DEBUG → PRODUCTION → NONE
    let newMode: LogMode;
    switch (logMode) {
      case 'NONE':
        newMode = 'DEBUG';
        break;
      case 'DEBUG':
        newMode = 'PRODUCTION';
        break;
      case 'PRODUCTION':
        newMode = 'NONE';
        break;
      default:
        newMode = 'NONE'; // fallback
        break;
    }

    logger.setLogMode(newMode);

    // Only log if not switching to NONE mode
    if (newMode !== 'NONE') {
      logger.info(`🔄 Console log mode toggled via UI`, {
        component: 'DebugPanel',
        previousMode: logMode,
        newMode: newMode,
        timestamp: new Date().toISOString()
      });
    }
  }, [logMode]);

  // Handle model selection change
  const handleModelChange = useCallback((event: React.ChangeEvent<HTMLSelectElement>) => {
    const modelId = event.target.value as AIModelId;
    if (Object.values(AIModelId).includes(modelId)) {
      onModelChange(modelId);
      logger.debug('Model selection changed', {
        component: 'DebugPanel',
        newModel: modelId,
        previousModel: currentModel
      });
    }
  }, [currentModel, onModelChange]);

  return (
    <div
      className={`debug-panel ${className}`}
      role="status"
      aria-label="Debug information"
    >
      <div
        className="debug-header clickable-header"
        onClick={toggleExpanded}
        onKeyDown={toggleExpanded}
        role="button"
        aria-expanded={isExpanded}
        aria-controls="debug-panel-content"
        tabIndex={0}
        aria-label={`${isExpanded ? 'Collapse' : 'Expand'} Debug Info section`}
      >
        <div className="header-content">
          <div className="header-left">
            <h3 className="debug-title">Debug Info</h3>
          </div>
          <div className={`chevron-icon ${isExpanded ? 'expanded' : 'collapsed'}`} aria-hidden="true">
            ▶
          </div>
        </div>
      </div>

      <div
        id="debug-panel-content"
        className={`collapsible-content ${isExpanded ? 'expanded' : 'collapsed'}`}
        aria-hidden={!isExpanded}
      >
        <div className="debug-content">
          <div className="debug-metric">
            <span className="debug-label">Latest Response Time:</span>
            <span className="debug-value" aria-live="polite">
              {latestResponseTime !== null
                ? `${latestResponseTime.toFixed(1)}s`
                : 'No responses yet'
              }
            </span>
          </div>

          <div className="debug-metric">
            <span className="debug-label">Console Log Mode:</span>
            <div className="log-mode-toggle-container">
              <button
                className={`log-mode-toggle ${logMode.toLowerCase()}-mode`}
                onClick={toggleLogMode}
                onKeyDown={toggleLogMode}
                aria-label={`Switch from ${logMode} to ${logMode === 'NONE' ? 'DEBUG' :
                  logMode === 'DEBUG' ? 'PRODUCTION' : 'NONE'
                  } mode`}
                aria-pressed={logMode !== 'NONE'}
                role="switch"
              >
                <span className="toggle-slider" aria-hidden="true">
                  <span className="toggle-indicator"></span>
                </span>
                <span className="toggle-labels">
                  <span className={`toggle-label none-label-text ${logMode === 'NONE' ? 'active' : ''}`}>
                    NONE
                  </span>
                  <span className={`toggle-label debug-label-text ${logMode === 'DEBUG' ? 'active' : ''}`}>
                    DEBUG
                  </span>
                  <span className={`toggle-label production-label-text ${logMode === 'PRODUCTION' ? 'active' : ''}`}>
                    PRODUCTION
                  </span>
                </span>
              </button>
              <span className="current-mode-indicator" aria-live="polite">
                {logMode} Mode
              </span>
            </div>
          </div>

          {/* AI Model Selector */}
          <div className="debug-metric">
            <span className="debug-label">AI Model:</span>
            <div className="model-selector-container">
              <select
                className="model-selector"
                value={currentModel || ''}
                onChange={handleModelChange}
                disabled={isLoadingModels || models.length === 0}
                aria-label="Select AI model"
                aria-describedby={modelError ? "model-error" : undefined}
              >
                {models.length === 0 ? (
                  <option value="">No models available</option>
                ) : (
                  models.map(model => (
                    <option key={model.id} value={model.id}>
                      {model.name}
                      {model.isDefault && ' (default)'}
                    </option>
                  ))
                )}
              </select>
              {isLoadingModels && (
                <span className="loading-indicator" aria-label="Loading models">
                  Loading...
                </span>
              )}
              {modelError && (
                <span id="model-error" className="error-message" role="alert">
                  {modelError}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

DebugPanel.displayName = 'DebugPanel';

export default DebugPanel;

/**
 * Professional Fintech Glassmorphic Styles for Developer Debug Panel
 * Enhanced monospace typography with professional fintech polish
 */
export const debugPanelStyles = `
  /* ==========================================================================
     DEBUG PANEL - Developer-Focused Component with Professional Fintech Design
     ========================================================================== */
  
  .debug-panel {
    /* Professional Glassmorphic Foundation */
    background: var(--glass-surface-2);
    backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--glass-border-1);
    box-shadow: var(--glass-shadow-sm);
    
    /* Developer Panel Design */
    border-radius: 12px;
    padding: var(--spacing-3) var(--spacing-4);
    margin: 0;
    width: 100%;
    max-width: 1000px;
    
    /* Professional Developer Typography */
    font-family: var(--font-mono);
    font-size: var(--font-size-small);
    color: var(--text-secondary);
    
    /* Modern Enhancement */
    position: relative;
    overflow: hidden;
  }
  
  /* Debug Panel Accent Border */
  .debug-panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-info) 0%, var(--accent-info-light) 100%);
    opacity: 0.6;
  }
  
  .debug-header {
    margin-bottom: var(--spacing-2);
    border-bottom: 1px solid var(--glass-border-2);
    padding-bottom: var(--spacing-2);
    position: relative;
  }

  .debug-header.clickable-header {
    cursor: pointer;
    border-radius: 8px;
    padding: var(--spacing-2) var(--spacing-3) var(--spacing-2) var(--spacing-3);
    margin: 0 0 var(--spacing-2) 0;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
  }

  .debug-header.clickable-header:hover {
    background: var(--glass-surface-1);
    border-color: var(--accent-info);
  }

  .debug-header.clickable-header:focus-visible {
    outline: 2px solid var(--accent-info);
    outline-offset: 2px;
    background: var(--glass-surface-1);
  }

  .debug-header .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
  }

  .debug-header .header-left {
    flex: 1;
    text-align: left;
  }
  
  .debug-title {
    margin: 0;
    font-size: var(--font-size-micro);
    font-weight: var(--font-weight-semibold);
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: var(--letter-spacing-wider);
    font-family: var(--font-mono);

    /* Developer Badge Styling */
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-1);
  }

  .clickable-header .debug-title {
    margin: 0;
    text-align: left;
  }
  
  .debug-title::before {
    content: 'Debug';
    font-size: var(--font-size-small);
  }

  /* Chevron icon styling for debug panel */
  .debug-header .chevron-icon {
    font-size: 14px;
    color: var(--text-secondary);
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    flex-shrink: 0;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    margin-left: var(--spacing-2);
  }

  .debug-header .chevron-icon.expanded {
    transform: rotate(90deg);
    color: var(--accent-info);
  }

  .debug-header.clickable-header:hover .chevron-icon {
    color: var(--accent-info);
    background: rgba(59, 130, 246, 0.1);
  }

  /* Collapsible content container for debug panel */
  .debug-panel .collapsible-content {
    overflow: hidden;
  }

  .debug-panel .collapsible-content.expanded {
    max-height: 500px; /* Sufficient for debug content */
    opacity: 1;
  }

  .debug-panel .collapsible-content.collapsed {
    max-height: 0;
    opacity: 0;
  }
  
  .debug-content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-2);
  }
  
  .debug-metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-1) 0;
    border-radius: 6px;
  }
  
  .debug-metric:hover {
    background: var(--glass-surface-1);
    padding-left: var(--spacing-2);
    padding-right: var(--spacing-2);
  }
  
  .debug-label {
    color: var(--neutral-color);
    font-weight: var(--font-weight-medium);
    font-size: var(--font-size-small);
    font-family: var(--font-mono);
    letter-spacing: var(--letter-spacing-normal);
  }
  
  .debug-value {
    /* Professional Value Badge */
    color: var(--accent-info-light);
    font-weight: var(--font-weight-bold);
    background: linear-gradient(135deg, var(--accent-info) 0%, var(--accent-info-light) 100%);
    color: var(--text-primary);
    
    padding: var(--spacing-1) var(--spacing-2);
    border-radius: 6px;
    font-size: var(--font-size-small);
    border: 1px solid var(--accent-info);
    
    min-width: 90px;
    text-align: center;
    font-family: var(--font-mono);
    letter-spacing: var(--letter-spacing-tight);
    
    /* Professional Enhancement */
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    position: relative;
    overflow: hidden;
  }
  
  /* Value Badge Animation - REMOVED FOR PERFORMANCE */
  .debug-value::before {
    display: none;
  }
  
  /* State-specific styling */
  .debug-value:empty::after {
    content: '---';
    color: var(--neutral-color);
    font-style: italic;
    font-weight: var(--font-weight-normal);
  }
  
  /* ==========================================================================
     CONSOLE LOG MODE TOGGLE - Professional Glassmorphic Toggle Switch
     ========================================================================== */

  .log-mode-toggle-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-1);
    align-items: flex-end;
  }

  .log-mode-toggle {
    position: relative;
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
    background: var(--glass-surface-1);
    backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--glass-border-2);
    border-radius: 20px;
    padding: var(--spacing-1) var(--spacing-2);
    cursor: pointer;
    font-family: var(--font-mono);
    font-size: var(--font-size-micro);
    min-width: 180px;
    height: 32px;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
  }

  .log-mode-toggle:hover {
    background: var(--glass-surface-2);
    border-color: var(--accent-info);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
  }

  .log-mode-toggle:focus-visible {
    outline: 2px solid var(--accent-info);
    outline-offset: 2px;
  }

  .toggle-slider {
    position: relative;
    width: 48px;
    height: 18px;
    background: var(--neutral-600);
    border-radius: 9px;
    flex-shrink: 0;
  }

  .toggle-indicator {
    position: absolute;
    top: 2px;
    left: 2px;
    width: 14px;
    height: 14px;
    background: var(--text-primary);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .toggle-labels {
    display: flex;
    gap: var(--spacing-1);
    font-weight: var(--font-weight-medium);
    letter-spacing: var(--letter-spacing-wider);
    flex-wrap: wrap;
  }

  .toggle-label {
    color: var(--text-secondary);
    font-size: var(--font-size-micro);
  }

  .toggle-label.active {
    color: var(--text-primary);
    font-weight: var(--font-weight-bold);
  }

  .current-mode-indicator {
    font-size: var(--font-size-micro);
    color: var(--accent-info-light);
    font-weight: var(--font-weight-medium);
    font-family: var(--font-mono);
    letter-spacing: var(--letter-spacing-tight);
  }

  /* ==========================================================================
     AI MODEL SELECTOR - Professional Glassmorphic Dropdown
     ========================================================================== */

  .model-selector-container {
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
    position: relative;
  }

  .model-selector {
    background: var(--glass-surface-1);
    backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--glass-border-2);
    color: var(--text-primary);
    padding: var(--spacing-1) var(--spacing-2);
    padding-right: var(--spacing-6); /* Space for dropdown arrow */
    border-radius: 6px;
    font-family: var(--font-mono);
    font-size: var(--font-size-small);
    min-width: 160px;
    cursor: pointer;
    transition: all 0.2s var(--transition-timing);
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right var(--spacing-2) center;
    background-size: 16px;
  }

  .model-selector:hover:not(:disabled) {
    background-color: var(--glass-surface-2);
    border-color: var(--accent-info);
    box-shadow: 0 0 0 1px var(--accent-info-light);
  }

  .model-selector:focus {
    outline: 2px solid var(--accent-info);
    outline-offset: 2px;
  }

  .model-selector:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .model-selector option {
    background: var(--background-primary);
    color: var(--text-primary);
    padding: var(--spacing-1);
  }

  .loading-indicator {
    position: absolute;
    right: var(--spacing-8);
    font-size: var(--font-size-micro);
    color: var(--accent-info);
    animation: pulse 1.5s ease-in-out infinite;
  }

  .error-message {
    position: absolute;
    top: calc(100% + var(--spacing-1));
    left: 0;
    font-size: var(--font-size-micro);
    color: var(--accent-error);
    white-space: nowrap;
  }

  @keyframes pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
  }

  /* NONE Mode Styling - Neutral gray theme */
  .log-mode-toggle.none-mode .toggle-slider {
    background: linear-gradient(135deg, var(--neutral-700) 0%, var(--neutral-600) 100%);
  }

  .log-mode-toggle.none-mode .toggle-indicator {
    transform: translateX(0);
    background: var(--neutral-400);
  }

  .log-mode-toggle.none-mode .none-label-text {
    color: var(--neutral-400);
    font-weight: var(--font-weight-bold);
  }

  /* DEBUG Mode Styling */
  .log-mode-toggle.debug-mode .toggle-slider {
    background: linear-gradient(135deg, var(--accent-info) 0%, var(--accent-info-light) 100%);
  }

  .log-mode-toggle.debug-mode .toggle-indicator {
    transform: translateX(16px);
    background: var(--background-primary);
  }

  .log-mode-toggle.debug-mode .debug-label-text {
    color: var(--accent-info-light);
    font-weight: var(--font-weight-bold);
  }

  /* PRODUCTION Mode Styling */
  .log-mode-toggle.production-mode .toggle-slider {
    background: linear-gradient(135deg, var(--neutral-500) 0%, var(--neutral-400) 100%);
  }

  .log-mode-toggle.production-mode .toggle-indicator {
    transform: translateX(32px);
    background: var(--background-primary);
  }

  .log-mode-toggle.production-mode .production-label-text {
    color: var(--neutral-300);
    font-weight: var(--font-weight-bold);
  }

  /* Responsive Design - Mobile Optimization */
  @media (max-width: 640px) {
    .log-mode-toggle-container {
      align-items: stretch;
    }

    .log-mode-toggle {
      min-width: 140px;
      height: 28px;
      font-size: 10px;
    }

    .toggle-slider {
      width: 36px;
      height: 14px;
    }

    .toggle-indicator {
      width: 10px;
      height: 10px;
    }

    .log-mode-toggle.debug-mode .toggle-indicator {
      transform: translateX(12px);
    }

    .log-mode-toggle.production-mode .toggle-indicator {
      transform: translateX(24px);
    }
    .debug-panel {
      padding: var(--spacing-2) var(--spacing-3);
      font-size: var(--font-size-micro);
      border-radius: 10px;
    }
    
    .debug-header.clickable-header {
      padding: var(--spacing-2);
      border-radius: 6px;
    }

    .debug-header .header-content {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-1);
    }

    .debug-header .header-left {
      order: 1;
      width: 100%;
    }

    .debug-header .chevron-icon {
      order: 2;
      align-self: flex-end;
      margin: 0;
      font-size: 12px;
      width: 18px;
      height: 18px;
    }
    
    .debug-title {
      font-size: var(--font-size-small);
    }

    .clickable-header .debug-title {
      margin-bottom: var(--spacing-1);
    }
    
    .debug-metric {
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-1);
      padding: var(--spacing-2) 0;
    }
    
    .debug-label {
      font-size: var(--font-size-micro);
    }
    
    .debug-value {
      font-size: var(--font-size-micro);
      padding: var(--spacing-1);
      min-width: 80px;
      align-self: flex-end;
    }

    .model-selector {
      min-width: 120px;
      font-size: var(--font-size-micro);
    }
    
    .model-selector-container {
      flex-direction: column;
      align-items: stretch;
      gap: var(--spacing-1);
    }
    
    .error-message {
      position: static;
      margin-top: var(--spacing-1);
    }
  }
  
  /* Tablet Optimization */
  @media (min-width: 641px) and (max-width: 1024px) {
    .debug-panel {
      padding: var(--spacing-3);
      font-size: var(--font-size-small);
    }
  }
  
  /* Desktop Enhancement */
  @media (min-width: 1025px) {
    .debug-panel {
      padding: var(--spacing-4) var(--spacing-6);
      font-size: var(--font-size-body);
    }
    
    .debug-title {
      font-size: var(--font-size-h6);
    }
    
    .debug-value {
      font-size: var(--font-size-body);
      padding: var(--spacing-2) var(--spacing-3);
      min-width: 100px;
    }
    
    .debug-panel:hover {
      backdrop-filter: var(--glass-blur-md);
    }
  }
  
  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .debug-panel {
      border: 2px solid var(--text-primary);
      background: var(--background-primary);
    }
    
    .debug-value {
      border: 2px solid var(--accent-info);
      background: var(--accent-info);
      color: var(--background-primary);
    }
  }
  
  /* Focus Management - Professional Developer Tools */
  .debug-panel:focus-within {
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
    border-color: var(--accent-info);
  }
  
  /* Reduced Motion Support - ALL ANIMATIONS REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }
  
  /* Performance Optimizations - GPU HINTS REMOVED FOR PERFORMANCE */
  .debug-panel {
    /* GPU acceleration hints removed */
  }
  
  /* High DPI Display Support */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
    .debug-panel {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  }
  
  /* Professional Loading State - SPINNER ANIMATION REMOVED FOR PERFORMANCE */
  .debug-panel[data-loading="true"] {
    opacity: 0.7;
    pointer-events: none;
  }
  
  .debug-panel[data-loading="true"]::after {
    content: 'Processing...';
    position: absolute;
    top: 50%;
    right: var(--spacing-3);
    transform: translateY(-50%);
    font-size: 16px;
    color: var(--accent-info);
  }
`;