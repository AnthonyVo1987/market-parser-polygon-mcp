import {
  FC
} from 'react';
import { DebugPanelProps } from '../types';

const DebugPanel: FC<DebugPanelProps> = ({
  lastUpdate = new Date(),
  isConnected = true
}) => {
  return (
    <div className="debug-panel-container" data-testid="debug-panel">
      <h3 className="debug-section-header">Debug Information</h3>
      <div className="debug-metrics-grid">
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
        <div className="debug-metric">
          <span className="debug-label">Session:</span>
          <span className="debug-value">Active</span>
        </div>
        <div className="debug-metric">
          <span className="debug-label">Version:</span>
          <span className="debug-value">v1.0.0</span>
        </div>
      </div>
    </div>
  );
};

export default DebugPanel;