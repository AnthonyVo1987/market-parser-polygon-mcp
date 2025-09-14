import { 
  useState, 
  useEffect, 
  useRef,
  useCallback,
  forwardRef,
  useImperativeHandle 
} from 'react';

interface SharedTickerInputProps {
  value?: string;
  onChange: (ticker: string) => void;
  className?: string;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
  label?: string;
  'aria-describedby'?: string;
  onEnter?: () => void;
  autoFocus?: boolean;
  required?: boolean;
}

export interface SharedTickerInputRef {
  focus: () => void;
  setValue: (value: string) => void;
  getValue: () => string;
  clear: () => void;
  validate: () => boolean;
}

const SharedTickerInput = forwardRef<SharedTickerInputRef, SharedTickerInputProps>(
  function SharedTickerInput(
    {
      value: externalValue,
      onChange,
      className = '',
      placeholder = 'NVDA',
      disabled = false,
      error: externalError,
      label = 'Stock Symbol',
      'aria-describedby': ariaDescribedBy,
      onEnter,
      autoFocus = false,
      required = false,
    },
    ref
  ) {
    // Internal state for uncontrolled mode and validation
    const [internalValue, setInternalValue] = useState(externalValue ?? 'NVDA');
    const [validationError, setValidationError] = useState<string>('');
    const [isTouched, setIsTouched] = useState(false);
    
    const inputRef = useRef<HTMLInputElement>(null);

    // Use external value if provided, otherwise use internal state
    const inputValue = externalValue !== undefined ? externalValue : internalValue;

    // Update internal state when external value changes
    useEffect(() => {
      if (externalValue !== undefined) {
        setInternalValue(externalValue);
      }
    }, [externalValue]);

    // Validation function
    const validateTicker = useCallback((ticker: string): string => {
      const cleanTicker = ticker.trim();
      
      if (!cleanTicker) {
        return required ? 'Stock symbol is required' : '';
      }
      
      if (cleanTicker.length < 3) {
        return 'Stock symbol must be at least 3 characters';
      }
      
      if (cleanTicker.length > 10) {
        return 'Stock symbol must be 10 characters or less';
      }
      
      // Check for valid characters (alphanumeric only)
      if (!/^[A-Z0-9]+$/.test(cleanTicker)) {
        return 'Stock symbol must contain only letters and numbers';
      }
      
      return '';
    }, [required]);

    // Handle input changes with formatting and validation
    const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
      const rawValue = e.target.value;
      
      // Format input: uppercase and alphanumeric only
      const formattedValue = rawValue
        .toUpperCase()
        .replace(/[^A-Z0-9]/g, '');

      // Update appropriate state based on control mode
      if (externalValue !== undefined) {
        onChange(formattedValue);
      } else {
        setInternalValue(formattedValue);
        onChange(formattedValue);
      }

      // Validate and set error state if input has been touched
      if (isTouched) {
        const error = validateTicker(formattedValue);
        setValidationError(error);
      }
    }, [externalValue, onChange, validateTicker, isTouched]);

    // Handle blur event for validation
    const handleBlur = useCallback(() => {
      setIsTouched(true);
      const error = validateTicker(inputValue);
      setValidationError(error);
    }, [inputValue, validateTicker]);

    // Handle key press events
    const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !disabled && onEnter) {
        e.preventDefault();
        const error = validateTicker(inputValue);
        if (!error) {
          onEnter();
        }
      }
    }, [inputValue, validateTicker, disabled, onEnter]);

    // Determine current error to display
    const displayError = externalError || validationError;
    const hasError = Boolean(displayError);
    const isValid = !hasError && inputValue.length >= 3;

    // Auto-focus effect
    useEffect(() => {
      if (autoFocus && inputRef.current) {
        inputRef.current.focus();
      }
    }, [autoFocus]);

    // Expose imperative methods to parent components
    useImperativeHandle(
      ref,
      () => ({
        focus: () => {
          inputRef.current?.focus();
        },
        setValue: (value: string) => {
          const formattedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '');
          if (externalValue !== undefined) {
            onChange(formattedValue);
          } else {
            setInternalValue(formattedValue);
            onChange(formattedValue);
          }
          setValidationError('');
        },
        getValue: () => inputValue,
        clear: () => {
          const defaultValue = 'NVDA';
          if (externalValue !== undefined) {
            onChange(defaultValue);
          } else {
            setInternalValue(defaultValue);
            onChange(defaultValue);
          }
          setValidationError('');
          setIsTouched(false);
        },
        validate: () => {
          const error = validateTicker(inputValue);
          setValidationError(error);
          setIsTouched(true);
          return !error;
        },
      }),
      [inputValue, externalValue, onChange, validateTicker]
    );

    const inputId = `ticker-input-${Math.random().toString(36).substr(2, 9)}`;
    const errorId = `${inputId}-error`;
    const helpId = `${inputId}-help`;

    const describedBy = [
      helpId,
      hasError ? errorId : null,
      ariaDescribedBy,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <div className={`shared-ticker-input-container ${className}`}>
        <label htmlFor={inputId} className="ticker-label">
          {label}
          {required && (
            <span className="required-indicator" aria-hidden="true">
              *
            </span>
          )}
        </label>
        
        <div className="ticker-input-wrapper">
          <input
            id={inputId}
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            maxLength={10}
            className={`ticker-input ${hasError ? 'error' : ''} ${isValid ? 'valid' : ''}`}
            disabled={disabled}
            aria-describedby={describedBy}
            aria-invalid={hasError}
            aria-required={required}
            spellCheck={false}
            autoComplete="off"
            autoCorrect="off"
            autoCapitalize="characters"
          />
          
          {/* Validation status icon */}
          <div className="validation-icon" aria-hidden="true">
            {isValid && !hasError && (
              <span className="validation-success">✓</span>
            )}
            {hasError && (
              <span className="validation-error">!</span>
            )}
          </div>
        </div>

        {/* Help text */}
        <div id={helpId} className="sr-only">
          Enter a stock symbol (3-10 characters, letters and numbers only).
          {onEnter && ' Press Enter to proceed.'}
          {required && ' This field is required.'}
        </div>

        {/* Error message */}
        {hasError && (
          <div
            id={errorId}
            className="error-message"
            role="alert"
            aria-live="polite"
          >
            {displayError}
          </div>
        )}

        {/* Success feedback for screen readers */}
        {isValid && !hasError && isTouched && (
          <div className="sr-only" aria-live="polite">
            Valid stock symbol entered
          </div>
        )}
      </div>
    );
  }
);

export default SharedTickerInput;

// Enhanced inline styles following project patterns
export const sharedTickerInputStyles = `
  /* Screen reader only content */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  .shared-ticker-input-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 100%;
    max-width: 200px;
  }

  /* Label styling */
  .ticker-label {
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-bottom: 2px;
  }

  .required-indicator {
    color: #dc2626;
    font-weight: bold;
  }

  /* Input wrapper for positioning validation icons */
  .ticker-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }

  /* Main input styling */
  .ticker-input {
    width: 100%;
    padding: 10px 40px 10px 12px;
    border: 1.5px solid #d1d5db;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
    text-transform: uppercase;
    background: white;
    color: #111827;
    transition: all 0.2s ease;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
    letter-spacing: 0.5px;
  }

  .ticker-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    background: #fefefe;
  }

  .ticker-input:focus-visible {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
  }

  /* Input validation states */
  .ticker-input.valid {
    border-color: #10b981;
    background: #f0fdf4;
  }

  .ticker-input.valid:focus {
    border-color: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
  }

  .ticker-input.error {
    border-color: #ef4444;
    background: #fef2f2;
  }

  .ticker-input.error:focus {
    border-color: #ef4444;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
  }

  .ticker-input:disabled {
    background-color: #f9fafb;
    border-color: #e5e7eb;
    color: #9ca3af;
    cursor: not-allowed;
  }

  /* Validation icon styling */
  .validation-icon {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    pointer-events: none;
  }

  .validation-success {
    color: #10b981;
    font-weight: bold;
    font-size: 14px;
  }

  .validation-error {
    color: #ef4444;
    font-weight: bold;
    font-size: 14px;
    background: #fee2e2;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
  }

  /* Error message styling */
  .error-message {
    background-color: #fef2f2;
    color: #dc2626;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    border: 1px solid #fecaca;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .error-message::before {
    content: '⚠';
    font-size: 14px;
    flex-shrink: 0;
  }

  /* Mobile responsiveness */
  @media (max-width: 767px) {
    .shared-ticker-input-container {
      max-width: 100%;
    }

    .ticker-input {
      padding: 12px 40px 12px 14px;
      font-size: 16px; /* Prevents iOS zoom */
      min-height: 44px; /* Touch-friendly minimum */
    }

    .ticker-label {
      font-size: 14px;
    }

    .error-message {
      padding: 8px 12px;
      font-size: 13px;
    }
  }

  /* Tablet optimizations */
  @media (min-width: 768px) and (max-width: 1023px) {
    .ticker-input {
      padding: 11px 40px 11px 13px;
      font-size: 15px;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .ticker-input {
      border-width: 2px;
    }

    .ticker-input.valid {
      border-width: 2px;
    }

    .ticker-input.error {
      border-width: 2px;
    }

    .error-message {
      border-width: 2px;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .ticker-input {
      transition: none;
    }
  }

  /* Dark mode support preparation */
  @media (prefers-color-scheme: dark) {
    .ticker-input {
      background: #1f2937;
      border-color: #4b5563;
      color: #f9fafb;
    }

    .ticker-input:focus {
      background: #111827;
    }

    .ticker-label {
      color: #e5e7eb;
    }

    .ticker-input.valid {
      background: #064e3b;
    }

    .ticker-input.error {
      background: #7f1d1d;
    }

    .error-message {
      background-color: #7f1d1d;
      color: #fca5a5;
      border-color: #dc2626;
    }
  }

  /* Focus-within enhancement for the container */
  .shared-ticker-input-container:focus-within .ticker-label {
    color: #3b82f6;
    transition: color 0.2s ease;
  }

  /* Hover effects for non-touch devices */
  @media (hover: hover) and (pointer: fine) {
    .ticker-input:not(:disabled):not(:focus):hover {
      border-color: #9ca3af;
      background: #fdfdfd;
    }

    .ticker-input.valid:not(:focus):hover {
      border-color: #059669;
    }

    .ticker-input.error:not(:focus):hover {
      border-color: #dc2626;
    }
  }
`;