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
 * CSS styles for the DebugPanel component
 * Follows the established design system and responsive patterns from ChatInterface_OpenAI
 */
export const debugPanelStyles = `
  /* DEBUG PANEL: Developer-focused section - DARK MODE DEFAULT */
  .debug-panel {
    background: #2d3748; /* Dark background */
    border: 1px solid #4a5568; /* Dark border */
    border-radius: 8px;
    padding: 12px 16px;
    margin: 0;
    font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
    font-size: 13px;
    width: 100%;
    max-width: 1000px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3); /* Darker shadow for dark mode */
    color: #e2e8f0; /* Light text */
  }
  
  .debug-header {
    margin-bottom: 8px;
    border-bottom: 1px solid #4a5568; /* Dark border */
    padding-bottom: 4px;
  }
  
  .debug-title {
    margin: 0;
    font-size: 14px;
    font-weight: 600;
    color: #f7fafc; /* Light title */
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-family: inherit;
  }
  
  .debug-content {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  
  .debug-metric {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
  }
  
  .debug-label {
    color: #a0aec0; /* Light label color */
    font-weight: 500;
    font-size: 12px;
  }
  
  .debug-value {
    color: #63b3ed; /* Light blue value */
    font-weight: 700;
    background: #1a365d; /* Dark blue background */
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 13px;
    border: 1px solid #2c5282; /* Dark blue border */
    min-width: 80px;
    text-align: center;
  }
  
  /* State-specific styling */
  .debug-value:empty::after {
    content: '---';
    color: #718096; /* Lighter gray for dark mode */
    font-style: italic;
  }
  
  /* Mobile adjustments */
  @media (max-width: 767px) {
    .debug-panel {
      padding: 10px 12px;
      font-size: 12px;
      border-radius: 6px;
    }
    
    .debug-title {
      font-size: 13px;
    }
    
    .debug-metric {
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
      padding: 6px 0;
    }
    
    .debug-label {
      font-size: 11px;
    }
    
    .debug-value {
      font-size: 12px;
      padding: 3px 6px;
      min-width: 70px;
      align-self: flex-end;
    }
  }
  
  /* Tablet adjustments */
  @media (min-width: 768px) and (max-width: 1024px) {
    .debug-panel {
      padding: 14px 18px;
      font-size: 13px;
    }
  }
  
  /* Desktop optimizations */
  @media (min-width: 1025px) {
    .debug-panel {
      padding: 16px 20px;
      font-size: 14px;
    }
    
    .debug-title {
      font-size: 15px;
    }
    
    .debug-value {
      font-size: 14px;
      padding: 5px 10px;
      min-width: 90px;
    }
  }
  
  /* High contrast mode support - DARK MODE */
  @media (prefers-contrast: high) {
    .debug-panel {
      border: 2px solid #f7fafc; /* Light border for dark high contrast */
      background: #1a202c; /* Darker background for high contrast */
    }
    
    .debug-value {
      border: 2px solid #63b3ed; /* Light blue border for high contrast */
      background: #1a365d; /* Dark blue background */
      color: #90cdf4; /* Lighter blue for high contrast */
    }
  }
  
  /* Dark mode is now the default theme - no media queries needed */
  
  /* Focus management - DARK MODE */
  .debug-panel:focus-within {
    outline: 2px solid #63b3ed; /* Light blue focus outline for dark mode */
    outline-offset: 2px;
  }
  
  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .debug-value {
      transition: none;
    }
  }
  
  /* Performance optimizations for high DPI displays */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
    .debug-panel {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  }
`;