import type { ChangeEvent, FormEvent, KeyboardEvent } from 'react';
import { FC, memo, useCallback, useEffect, useState } from 'react';
import { TickerInputProps } from '../types';
import { getTickerPlaceholder } from '../utils/placeholderText';

const SharedTickerInput: FC<TickerInputProps> = memo(
  ({ value, onChange, onSearch, disabled = false, placeholder }) => {
    // Enhanced placeholder text based on user state
    const dynamicPlaceholder =
      placeholder || getTickerPlaceholder(disabled ? 'loading' : 'idle');
    
    // Simple state management without validation
    const [ticker, setTicker] = useState(value);

    // Sync with parent component value
    useEffect(() => {
      setTicker(value);
    }, [value]);

    const handleChange = useCallback(
      (e: ChangeEvent<HTMLInputElement>) => {
        const newValue = e.target.value.toUpperCase();
        setTicker(newValue);
        onChange(newValue);
      },
      [onChange]
    );

    const handleSubmit = useCallback(
      (e: FormEvent) => {
        e.preventDefault();
        if (ticker.trim() && !disabled) {
          onSearch?.();
        }
      },
      [ticker, onSearch, disabled]
    );

    const handleKeyDown = useCallback(
      (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !disabled) {
          e.preventDefault();
          handleSubmit(e);
        }
      },
      [handleSubmit, disabled]
    );

    return (
      <div className='ticker-input-container' data-testid='ticker-input'>
        <div className='ticker-input-header'>
          <h3 className='ticker-input-title'>BUTTON PROMPT STOCK TICKER</h3>
          <div className='ticker-input-subtitle'>
            Enter stock symbol for analysis
          </div>
        </div>

        <form onSubmit={handleSubmit} className='ticker-input-form'>
          <div className='ticker-input-wrapper'>
            <input
              type='text'
              value={ticker}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              placeholder={dynamicPlaceholder}
              disabled={disabled}
              className='ticker-input-field'
              data-testid='ticker-input-field'
              aria-label='Stock ticker input - Enter stock symbol for analysis'
              aria-required='false'
              role='textbox'
              aria-autocomplete='none'
              maxLength={5}
            />
            <button
              type='submit'
              disabled={disabled || !ticker.trim()}
              className='ticker-input-search-button'
              data-testid='ticker-input-search-button'
              aria-label='Search for stock ticker'
            >
              <svg
                className='ticker-input-search-icon'
                viewBox='0 0 24 24'
                fill='none'
                xmlns='http://www.w3.org/2000/svg'
              >
                <path
                  d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'
                  stroke='currentColor'
                  strokeWidth='2'
                  strokeLinecap='round'
                  strokeLinejoin='round'
                />
              </svg>
            </button>
          </div>
        </form>
      </div>
    );
  }
);

SharedTickerInput.displayName = 'SharedTickerInput';

export default SharedTickerInput;
