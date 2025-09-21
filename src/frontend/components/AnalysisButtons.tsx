import { FC } from 'react';

interface AnalysisButtonsProps {
  onSnapshot: () => void;
  onSupportResistance: () => void;
  onTechnicalAnalysis: () => void;
  disabled?: boolean;
}

const AnalysisButtons: FC<AnalysisButtonsProps> = ({
  onSnapshot,
  onSupportResistance,
  onTechnicalAnalysis,
  disabled = false
}) => {
  return (
    <div className="analysis-buttons-container" data-testid="analysis-buttons">
      <h3 className="analysis-section-header">Quick Analysis</h3>
      <div className="analysis-buttons-grid">
        <button
          className="analysis-button snapshot-button"
          onClick={onSnapshot}
          disabled={disabled}
          data-testid="analysis-button-snapshot"
          aria-label="Take stock snapshot analysis"
        >
          📊 Stock Snapshot
        </button>
        <button
          className="analysis-button support-resistance-button"
          onClick={onSupportResistance}
          disabled={disabled}
          data-testid="analysis-button-support-resistance"
          aria-label="Analyze support and resistance levels"
        >
          📈 Support/Resistance
        </button>
        <button
          className="analysis-button technical-analysis-button"
          onClick={onTechnicalAnalysis}
          disabled={disabled}
          data-testid="analysis-button-technical"
          aria-label="Perform technical analysis"
        >
          🔍 Technical Analysis
        </button>
      </div>
    </div>
  );
};

export default AnalysisButtons;
