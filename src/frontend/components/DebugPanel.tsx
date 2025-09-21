import React, { FC } from 'react';

interface DebugPanelProps {
  responseTime?: number;
  messageCount?: number;
  lastUpdate?: Date;
  isConnected?: boolean;
}

const DebugPanel: FC<DebugPanelProps> = ({
  responseTime = 0,
  messageCount = 0,
  lastUpdate = new Date(),
  isConnected = true
}) => {
  return (
    <div className="debug-panel-container" data-testid="debug-panel">
      <h3 className="debug-section-header">Debug Information</h3>
      <div className="debug-metrics-grid">
        <div className="debug-metric">
          <span className="debug-label">Response Time:</span>
          <span className="debug-value">{responseTime.toFixed(2)}s</span>
        </div>
        <div className="debug-metric">
          <span className="debug-label">Messages:</span>
          <span className="debug-value">{messageCount}</span>
        </div>
        <div className="debug-metric">
          <span className="debug-label">Last Update:</span>
          <span className="debug-value">{lastUpdate.toLocaleTimeString()}</span>
        </div>
        <div className="debug-metric">
          <span className="debug-label">Status:</span>
          <span className={`debug-value ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default DebugPanel;
