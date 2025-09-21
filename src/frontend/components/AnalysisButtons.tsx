import {
  FC,
  useCallback
} from 'react';
import { AnalysisButtonsProps } from '../types';
import { useButtonState } from '../utils/buttonStates';
import LoadingSpinner from './LoadingSpinner';

const AnalysisButtons: FC<AnalysisButtonsProps> = ({
  onSnapshot,
  onSupportResistance,
  onTechnicalAnalysis,
  disabled = false
}) => {
  // Button state management for each analysis button
  const snapshotButton = useButtonState({
    idleText: '📊 Stock Snapshot',
    loadingText: 'Analyzing...',
    successText: '✓ Complete',
    errorText: '✗ Error',
    disabledText: 'Stock Snapshot',
    onStateChange: (state) => console.log('Snapshot button state:', state)
  });

  const supportResistanceButton = useButtonState({
    idleText: '📈 Support/Resistance',
    loadingText: 'Analyzing...',
    successText: '✓ Complete',
    errorText: '✗ Error',
    disabledText: 'Support/Resistance',
    onStateChange: (state) => console.log('Support/Resistance button state:', state)
  });

  const technicalAnalysisButton = useButtonState({
    idleText: '🔍 Technical Analysis',
    loadingText: 'Analyzing...',
    successText: '✓ Complete',
    errorText: '✗ Error',
    disabledText: 'Technical Analysis',
    onStateChange: (state) => console.log('Technical Analysis button state:', state)
  });

  // Enhanced click handlers with state management
  const handleSnapshotClick = useCallback(async () => {
    if (snapshotButton.isLoading || disabled) return;

    try {
      snapshotButton.startLoading();
      await onSnapshot();
      snapshotButton.setSuccess();
    } catch (error) {
      snapshotButton.setError();
    }
  }, [snapshotButton, onSnapshot, disabled]);

  const handleSupportResistanceClick = useCallback(async () => {
    if (supportResistanceButton.isLoading || disabled) return;

    try {
      supportResistanceButton.startLoading();
      await onSupportResistance();
      supportResistanceButton.setSuccess();
    } catch (error) {
      supportResistanceButton.setError();
    }
  }, [supportResistanceButton, onSupportResistance, disabled]);

  const handleTechnicalAnalysisClick = useCallback(async () => {
    if (technicalAnalysisButton.isLoading || disabled) return;

    try {
      technicalAnalysisButton.startLoading();
      await onTechnicalAnalysis();
      technicalAnalysisButton.setSuccess();
    } catch (error) {
      technicalAnalysisButton.setError();
    }
  }, [technicalAnalysisButton, onTechnicalAnalysis, disabled]);

  return (
    <div className="analysis-buttons-container" data-testid="analysis-buttons">
      <h3 className="analysis-section-header">QUICK ANALYSIS</h3>
      <div className="analysis-buttons-grid">
        <button
          className={`analysis-button snapshot-button ${snapshotButton.state === 'loading' ? 'analysis-button--loading' : ''
            } ${snapshotButton.state === 'success' ? 'analysis-button--success' : ''
            } ${snapshotButton.state === 'error' ? 'analysis-button--error' : ''
            }`}
          onClick={handleSnapshotClick}
          disabled={disabled || snapshotButton.isDisabled}
          data-testid="analysis-button-snapshot"
          aria-label={snapshotButton.ariaLabel}
          aria-disabled={disabled || snapshotButton.isDisabled}
        >
          {snapshotButton.isLoading && <LoadingSpinner size="sm" className="mr-2" />}
          {snapshotButton.displayText}
        </button>
        <button
          className={`analysis-button support-resistance-button ${supportResistanceButton.state === 'loading' ? 'analysis-button--loading' : ''
            } ${supportResistanceButton.state === 'success' ? 'analysis-button--success' : ''
            } ${supportResistanceButton.state === 'error' ? 'analysis-button--error' : ''
            }`}
          onClick={handleSupportResistanceClick}
          disabled={disabled || supportResistanceButton.isDisabled}
          data-testid="analysis-button-support-resistance"
          aria-label={supportResistanceButton.ariaLabel}
          aria-disabled={disabled || supportResistanceButton.isDisabled}
        >
          {supportResistanceButton.isLoading && <LoadingSpinner size="sm" className="mr-2" />}
          {supportResistanceButton.displayText}
        </button>
        <button
          className={`analysis-button technical-analysis-button ${technicalAnalysisButton.state === 'loading' ? 'analysis-button--loading' : ''
            } ${technicalAnalysisButton.state === 'success' ? 'analysis-button--success' : ''
            } ${technicalAnalysisButton.state === 'error' ? 'analysis-button--error' : ''
            }`}
          onClick={handleTechnicalAnalysisClick}
          disabled={disabled || technicalAnalysisButton.isDisabled}
          data-testid="analysis-button-technical"
          aria-label={technicalAnalysisButton.ariaLabel}
          aria-disabled={disabled || technicalAnalysisButton.isDisabled}
        >
          {technicalAnalysisButton.isLoading && <LoadingSpinner size="sm" className="mr-2" />}
          {technicalAnalysisButton.displayText}
        </button>
      </div>
    </div>
  );
};

export default AnalysisButtons;