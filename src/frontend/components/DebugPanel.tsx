// React import not needed with modern JSX transform

/**
 * Props interface for the DebugPanel component
 */
interface DebugPanelProps {
  /** The most recent AI response time in seconds, or null if no responses yet */
  latestResponseTime: number | null;
  /** Additional CSS classes to apply to the component */
  className?: string;
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
export default function DebugPanel({ 
  latestResponseTime, 
  className = '' 
}: DebugPanelProps) {
  return (
    <div 
      className={`debug-panel ${className}`}
      role="status"
      aria-label="Debug information"
    >
      <div className="debug-header">
        <h3 className="debug-title">Debug Info</h3>
      </div>
      
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
      </div>
    </div>
  );
}

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
  
  .debug-title {
    margin: 0;
    font-size: var(--font-size-body);
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
  
  .debug-title::before {
    content: '⚙️';
    font-size: var(--font-size-small);
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
    transition: background 0.2s ease;
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
  
  /* Value Badge Animation */
  .debug-value::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s ease;
  }
  
  .debug-value:hover::before {
    left: 100%;
  }
  
  /* State-specific styling */
  .debug-value:empty::after {
    content: '---';
    color: var(--neutral-color);
    font-style: italic;
    font-weight: var(--font-weight-normal);
  }
  
  /* Responsive Design - Mobile Optimization */
  @media (max-width: 640px) {
    .debug-panel {
      padding: var(--spacing-2) var(--spacing-3);
      font-size: var(--font-size-micro);
      border-radius: 10px;
    }
    
    .debug-title {
      font-size: var(--font-size-small);
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
  
  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .debug-value {
      transition: none;
    }
    
    .debug-value::before {
      display: none;
    }
    
    .debug-metric {
      transition: none;
    }
  }
  
  /* Performance Optimizations */
  .debug-panel {
    will-change: backdrop-filter;
    transform: translateZ(0); /* Force GPU acceleration */
  }
  
  /* High DPI Display Support */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
    .debug-panel {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  }
  
  /* Professional Loading State */
  .debug-panel[data-loading="true"] {
    opacity: 0.7;
    pointer-events: none;
  }
  
  .debug-panel[data-loading="true"]::after {
    content: '';
    position: absolute;
    top: 50%;
    right: var(--spacing-3);
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid var(--accent-info);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    transform: translateY(-50%);
  }
  
  @keyframes spin {
    0% { transform: translateY(-50%) rotate(0deg); }
    100% { transform: translateY(-50%) rotate(360deg); }
  }
`;