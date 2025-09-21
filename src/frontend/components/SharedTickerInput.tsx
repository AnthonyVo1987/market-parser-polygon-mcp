import React, { 
  useState, 
  useCallback, 
  useEffect, 
  useMemo, 
  useId,
  FC,
  ComponentType,
  ReactNode,
  JSX
} from 'react';
import type { 
  FormEvent, 
  KeyboardEvent, 
  ChangeEvent 
} from 'react';
import { TickerInputProps } from '../types';

const SharedTickerInput: FC<TickerInputProps> = ({
  value,
  onChange,
  onSearch,
  disabled = false,
  placeholder = "Enter stock ticker (e.g., AAPL)"
}) => {
  const [ticker, setTicker] = useState(value);
  const [isValid, setIsValid] = useState(true);

  useEffect(() => {
    setTicker(value);
  }, [value]);

  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value.toUpperCase();
    setTicker(newValue);
    onChange(newValue);
    
    // Basic validation for stock ticker format
    const tickerRegex = /^[A-Z]{1,5}$/;
    setIsValid(tickerRegex.test(newValue) || newValue === '');
  }, [onChange]);

  const handleSubmit = useCallback((e: FormEvent) => {
    e.preventDefault();
    if (ticker.trim() && !disabled && isValid) {
      onSearch(ticker.trim());
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
            placeholder={placeholder}
            disabled={disabled}
            className={`ticker-input-field ${!isValid ? 'invalid' : ''}`}
            data-testid="ticker-input-field"
            aria-label="Stock ticker input - Enter stock symbol for analysis"
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
        {!isValid && ticker && (
          <div className="ticker-input-error" data-testid="ticker-input-error">
            Please enter a valid stock ticker (1-5 letters)
          </div>
        )}
      </form>
    </div>
  );
};

export default SharedTickerInput;