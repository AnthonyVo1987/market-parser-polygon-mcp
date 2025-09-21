import type {
  ChangeEvent,
  FormEvent,
  KeyboardEvent
} from 'react';
import {
  FC,
  memo,
  useCallback,
  useEffect
} from 'react';
import { useInputValidation } from '../hooks/useInputValidation';
import { TickerInputProps } from '../types';
import { getTickerPlaceholder } from '../utils/placeholderText';
import { ValidationRule, validateTicker } from '../utils/validation';

const SharedTickerInput: FC<TickerInputProps> = memo(({
  value,
  onChange,
  onSearch,
  disabled = false,
  placeholder
}) => {
  // Enhanced placeholder text based on user state
  const dynamicPlaceholder = placeholder || getTickerPlaceholder(disabled ? 'loading' : 'idle');
  // Enhanced validation rules for ticker input
  const validationRules: ValidationRule = {
    required: false, // Ticker is optional
    minLength: 1,
    maxLength: 5,
    custom: (val) => validateTicker(val)
  };

  // Use enhanced validation hook
  const {
    value: ticker,
    setValue: setTicker,
    isTouched,
    isValid,
    errorMessage,
    handleChange: handleValidationChange,
    handleBlur,
    handleFocus,
  } = useInputValidation({
    rules: validationRules,
    initialValue: value,
    validateOnChange: true,
    validateOnBlur: true
  });

  // Sync with parent component value
  useEffect(() => {
    setTicker(value);
  }, [value, setTicker]);

  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value.toUpperCase();
    handleValidationChange({
      ...e,
      target: { ...e.target, value: newValue }
    });
    onChange(newValue);
  }, [handleValidationChange, onChange]);

  const handleSubmit = useCallback((e: FormEvent) => {
    e.preventDefault();
    if (ticker.trim() && !disabled && isValid) {
      onSearch?.();
    }
  }, [ticker, onSearch, disabled, isValid]);

  const handleKeyDown = useCallback((e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !disabled && isValid) {
      e.preventDefault();
      handleSubmit(e);
    }
  }, [handleSubmit, disabled, isValid]);

  return (
    <div className="ticker-input-container" data-testid="ticker-input">
      <div className="ticker-input-header">
        <h3 className="ticker-input-title">BUTTON PROMPT STOCK TICKER</h3>
        <div className="ticker-input-subtitle">Enter stock symbol for analysis</div>
      </div>

      <form onSubmit={handleSubmit} className="ticker-input-form">
        <div className="ticker-input-wrapper">
          <input
            type="text"
            value={ticker}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            onBlur={handleBlur}
            onFocus={handleFocus}
            placeholder={dynamicPlaceholder}
            disabled={disabled}
            className={`ticker-input-field ${isTouched && !isValid ? 'ticker-input-field--invalid' : ''
              } ${isTouched && isValid ? 'ticker-input-field--valid' : ''
              }`}
            data-testid="ticker-input-field"
            aria-label="Stock ticker input - Enter stock symbol for analysis"
            aria-invalid={isTouched && !isValid}
            aria-describedby={isTouched && !isValid ? 'ticker-input-error' : undefined}
            aria-required="false"
            role="textbox"
            aria-autocomplete="none"
            maxLength={5}
          />
          <button
            type="submit"
            disabled={disabled || !ticker.trim() || !isValid}
            className="ticker-input-search-button"
            data-testid="ticker-input-search-button"
            aria-label="Search for stock ticker"
          >
            <svg
              className="ticker-input-search-icon"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
        {/* Enhanced validation error display */}
        {isTouched && !isValid && errorMessage && (
          <div
            id="ticker-input-error"
            className="ticker-input-error"
            data-testid="ticker-input-error"
            role="alert"
            aria-live="polite"
          >
            {errorMessage}
          </div>
        )}
      </form>
    </div>
  );
});

SharedTickerInput.displayName = 'SharedTickerInput';

export default SharedTickerInput;