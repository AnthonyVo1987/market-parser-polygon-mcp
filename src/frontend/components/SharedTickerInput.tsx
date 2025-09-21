import { ChangeEvent, FC, KeyboardEvent, useCallback, useId, useState } from 'react';

import { TickerInputProps } from '../types';

const SharedTickerInput: FC<TickerInputProps> = ({
  value,
  onChange,
  onAnalyze,
  disabled = false,
  required = true
}) => {
  const inputId = useId();
  const [isValid, setIsValid] = useState(true);

  const handleInputChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value.toUpperCase();
    onChange(newValue);

    // Basic ticker validation (1-5 characters, letters only)
    const tickerRegex = /^[A-Z]{1,5}$/;
    setIsValid(tickerRegex.test(newValue) || newValue === '');
  }, [onChange]);

  const handleKeyDown = useCallback((e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !disabled && value.trim()) {
      e.preventDefault();
      onAnalyze();
    }
  }, [onAnalyze, disabled, value]);

  return (
    <div className="shared-ticker-input-container" data-testid="ticker-input-container">
      <label htmlFor={inputId} className="ticker-label button-prompt-label">
        BUTTON PROMPT STOCK TICKER
        {required && <span className="required-indicator" aria-hidden="true">*</span>}
      </label>
      <div className="ticker-input-group">
        <input
          id={inputId}
          type="text"
          value={value}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Enter stock ticker (e.g., AAPL, MSFT)"
          className={`ticker-input ${!isValid ? 'invalid' : ''}`}
          disabled={disabled}
          maxLength={5}
          aria-label="Stock ticker for button prompt analysis"
          aria-describedby="ticker-help"
          data-testid="stock-ticker-input"
        />
        <button
          onClick={onAnalyze}
          disabled={disabled || !value.trim() || !isValid}
          className="ticker-analyze-button"
          data-testid="ticker-analyze-button"
          aria-label="Analyze stock ticker"
        >
          Analyze
        </button>
      </div>
      <div id="ticker-help" className="ticker-help">
        Enter a valid stock ticker symbol (1-5 letters) for button prompt analysis
      </div>
      {!isValid && value && (
        <div className="ticker-error" role="alert">
          Invalid ticker format. Use 1-5 letters only.
        </div>
      )}
    </div>
  );
};

export default SharedTickerInput;
