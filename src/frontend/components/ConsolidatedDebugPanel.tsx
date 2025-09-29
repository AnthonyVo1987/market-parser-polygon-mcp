import { FC } from 'react';

interface ConsolidatedDebugPanelProps {
  messageCount: number;
  isLoading: boolean;
  lastUpdate: Date;
  isConnected: boolean;
  performanceMetrics?: {
    fcp?: number;
    lcp?: number;
    cls?: number;
  };
}

const ConsolidatedDebugPanel: FC<ConsolidatedDebugPanelProps> = ({
  messageCount,
  isLoading,
  lastUpdate,
  isConnected,
  performanceMetrics = {},
}) => {
  return (
    <div className="consolidated-debug-panel" data-testid="consolidated-debug-panel">
      <h3 className="debug-section-header">System Information</h3>
      
      {/* Debug Information Section */}
      <div className="debug-section">
        <h4 className="debug-subsection-title">Debug Information</h4>
        <div className="debug-metrics-grid">
          <div className="debug-metric">
            <span className="debug-label">Last Update:</span>
            <span className="debug-value">{lastUpdate.toLocaleTimeString()}</span>
          </div>
          <div className="debug-metric">
            <span className="debug-label">Status:</span>
            <span
              className={`debug-value ${isConnected ? 'connected' : 'disconnected'}`}
            >
              {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
            </span>
          </div>
          <div className="debug-metric">
            <span className="debug-label">Version:</span>
            <span className="debug-value">v1.0.0</span>
          </div>
        </div>
      </div>

      {/* Status Information Section */}
      <div className="status-section">
        <h4 className="debug-subsection-title">Status Information</h4>
        <div className="status-metrics-grid">
          <div className="status-metric">
            <span className="status-label">Messages:</span>
            <span
              className="status-value"
              aria-label={`Total messages: ${messageCount}`}
            >
              {messageCount}
            </span>
          </div>
          <div className="status-metric">
            <span className="status-label">Processing:</span>
            <span
              className={`status-value ${isLoading ? 'status--loading' : 'status--ready'}`}
              aria-label={`Current status: ${isLoading ? 'Processing request' : 'Ready for input'}`}
            >
              {isLoading ? 'Processing...' : 'Ready'}
            </span>
          </div>
        </div>
      </div>

      {/* Performance Metrics Section */}
      {performanceMetrics && (
        <div className="performance-section">
          <h4 className="debug-subsection-title">Performance Metrics</h4>
          <div className="performance-metrics-grid">
            <div className="performance-metric">
              <span className="metric-label">FCP:</span>
              <span
                className={
                  performanceMetrics.fcp && performanceMetrics.fcp < 1500
                    ? 'good'
                    : 'warning'
                }
              >
                {performanceMetrics.fcp
                  ? `${performanceMetrics.fcp.toFixed(0)}ms`
                  : 'Calculating...'}
              </span>
            </div>
            <div className="performance-metric">
              <span className="metric-label">LCP:</span>
              <span
                className={
                  performanceMetrics.lcp && performanceMetrics.lcp < 2500
                    ? 'good'
                    : 'warning'
                }
              >
                {performanceMetrics.lcp
                  ? `${performanceMetrics.lcp.toFixed(0)}ms`
                  : 'Calculating...'}
              </span>
            </div>
            <div className="performance-metric">
              <span className="metric-label">CLS:</span>
              <span
                className={
                  performanceMetrics.cls && performanceMetrics.cls < 0.1
                    ? 'good'
                    : 'warning'
                }
              >
                {performanceMetrics.cls
                  ? performanceMetrics.cls.toFixed(3)
                  : 'Calculating...'}
              </span>
            </div>
          </div>
          <div className="performance-note">
            <small>Metrics update after user interaction</small>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConsolidatedDebugPanel;

// Styles for the consolidated debug panel
export const consolidatedDebugPanelStyles = `
  .consolidated-debug-panel {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px;
    background: var(--glass-surface-debug);
    border: var(--border-debug);
    border-radius: var(--radius-lg);
    box-shadow: var(--border-glow-debug);
  }

  .debug-section-header {
    margin: 0 0 8px 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--neutral-100);
    font-family: var(--font-inter);
    text-align: center;
  }

  .debug-subsection-title {
    margin: 0 0 8px 0;
    font-size: 14px;
    font-weight: 500;
    color: var(--neutral-200);
    font-family: var(--font-inter);
    border-bottom: 1px solid var(--glass-border-highlight);
    padding-bottom: 4px;
  }

  .debug-section,
  .status-section,
  .performance-section {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .debug-metrics-grid,
  .status-metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 8px;
  }

  .performance-metrics-grid {
    display: flex;
    gap: 16px;
    align-items: center;
    flex-wrap: wrap;
  }

  .debug-metric,
  .status-metric,
  .performance-metric {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 8px;
    background: var(--glass-surface-light);
    border-radius: var(--radius-md);
    border: 1px solid var(--glass-border-highlight);
  }

  .debug-label,
  .status-label,
  .metric-label {
    font-size: 11px;
    color: var(--neutral-400);
    font-family: var(--font-inter);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .debug-value,
  .status-value {
    font-size: 13px;
    color: var(--neutral-200);
    font-family: var(--font-inter);
    font-weight: 500;
  }

  .debug-value.connected {
    color: var(--success-500);
  }

  .debug-value.disconnected {
    color: var(--error-500);
  }

  .status-value.status--loading {
    color: var(--warning-500);
  }

  .status-value.status--ready {
    color: var(--success-500);
  }

  .performance-metric .good {
    color: var(--success-500);
  }

  .performance-metric .warning {
    color: var(--warning-500);
  }

  .performance-note {
    margin-top: 8px;
    text-align: center;
  }

  .performance-note small {
    font-size: 10px;
    color: var(--neutral-500);
    font-family: var(--font-inter);
    font-style: italic;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .consolidated-debug-panel {
      padding: 12px;
      gap: 12px;
    }

    .debug-metrics-grid,
    .status-metrics-grid {
      grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
      gap: 6px;
    }

    .performance-metrics-grid {
      gap: 8px;
    }

    .debug-metric,
    .status-metric,
    .performance-metric {
      padding: 6px;
    }

    .debug-label,
    .status-label,
    .metric-label {
      font-size: 10px;
    }

    .debug-value,
    .status-value {
      font-size: 12px;
    }
  }
`;
