import {
  useState,
  useEffect,
  useRef,
  useCallback,
  forwardRef,
  useImperativeHandle,
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

const SharedTickerInput = forwardRef<
  SharedTickerInputRef,
  SharedTickerInputProps
>(function SharedTickerInput(
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
  const inputValue =
    externalValue !== undefined ? externalValue : internalValue;

  // Update internal state when external value changes
  useEffect(() => {
    if (externalValue !== undefined) {
      setInternalValue(externalValue);
    }
  }, [externalValue]);

  // Validation function
  const validateTicker = useCallback(
    (ticker: string): string => {
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
    },
    [required]
  );

  // Handle input changes with formatting and validation
  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const rawValue = e.target.value;

      // Format input: uppercase and alphanumeric only
      const formattedValue = rawValue.toUpperCase().replace(/[^A-Z0-9]/g, '');

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
    },
    [externalValue, onChange, validateTicker, isTouched]
  );

  // Handle blur event for validation
  const handleBlur = useCallback(() => {
    setIsTouched(true);
    const error = validateTicker(inputValue);
    setValidationError(error);
  }, [inputValue, validateTicker]);

  // Handle key press events
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !disabled && onEnter) {
        e.preventDefault();
        const error = validateTicker(inputValue);
        if (!error) {
          onEnter();
        }
      }
    },
    [inputValue, validateTicker, disabled, onEnter]
  );

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

  const describedBy = [helpId, hasError ? errorId : null, ariaDescribedBy]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={`shared-ticker-input-container ${className}`}>
      <label htmlFor={inputId} className='ticker-label'>
        {label}
        {required && (
          <span className='required-indicator' aria-hidden='true'>
            *
          </span>
        )}
      </label>

      <div className='ticker-input-wrapper'>
        <input
          id={inputId}
          ref={inputRef}
          type='text'
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
          autoComplete='off'
          autoCorrect='off'
          autoCapitalize='characters'
        />

        {/* Validation status icon */}
        <div className='validation-icon' aria-hidden='true'>
          {isValid && !hasError && (
            <span className='validation-success'>✓</span>
          )}
          {hasError && <span className='validation-error'>!</span>}
        </div>
      </div>

      {/* Help text */}
      <div id={helpId} className='sr-only'>
        Enter a stock symbol (3-10 characters, letters and numbers only).
        {onEnter && ' Press Enter to proceed.'}
        {required && ' This field is required.'}
      </div>

      {/* Error message */}
      {hasError && (
        <div
          id={errorId}
          className='error-message'
          role='alert'
          aria-live='polite'
        >
          {displayError}
        </div>
      )}

      {/* Success feedback for screen readers */}
      {isValid && !hasError && isTouched && (
        <div className='sr-only' aria-live='polite'>
          Valid stock symbol entered
        </div>
      )}
    </div>
  );
});

export default SharedTickerInput;

// Enhanced fintech glassmorphic inline styles using comprehensive design system
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

  /* Enhanced container with sophisticated glassmorphic card styling */
  .shared-ticker-input-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-2);
    width: 100%;
    max-width: 240px;
    /* Professional glassmorphic card background */
    background: var(--glass-surface-2);
    backdrop-filter: var(--glass-blur-sm);
    -webkit-backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--glass-border-1);
    border-radius: var(--radius-card);
    padding: var(--spacing-4);
    /* Enhanced shadows for depth */
    box-shadow: var(--glass-shadow-sm);
    /* Performance optimizations */
    contain: layout style;
    box-sizing: border-box;
    /* Sophisticated transitions */
    transition: all var(--timing-base) var(--ease-out);
    /* Enhanced visual hierarchy */
    position: relative;
  }

  /* Sophisticated container hover and focus states */
  .shared-ticker-input-container:hover {
    background: var(--glass-surface-3);
    border-color: var(--glass-border-2);
    transform: translateY(-1px);
    box-shadow: var(--glass-shadow-md);
  }

  .shared-ticker-input-container:focus-within {
    background: var(--glass-surface-4);
    border-color: var(--accent-trust);
    box-shadow:
      0 0 0 1px var(--accent-trust),
      var(--glass-shadow-lg),
      var(--shadow-glow-trust);
    transform: translateY(-2px);
  }

  /* Enhanced label with fintech typography and trust color accent */
  .ticker-label {
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-normal);
    letter-spacing: var(--letter-spacing-wide);
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: var(--spacing-1);
    margin-bottom: var(--spacing-1);
    text-transform: uppercase;
    /* Smooth color transitions */
    transition: color var(--timing-base) var(--ease-out);
  }

  .shared-ticker-input-container:focus-within .ticker-label {
    color: var(--accent-trust);
    transform: translateY(-1px);
  }

  .required-indicator {
    color: var(--accent-error);
    font-weight: var(--font-weight-bold);
    font-size: var(--font-size-body);
  }

  /* Enhanced input wrapper with professional positioning */
  .ticker-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    /* Glassmorphic wrapper effect */
    background: var(--glass-surface-1);
    border-radius: var(--radius-input);
    border: 1px solid var(--glass-border-1);
    overflow: hidden;
    /* Professional depth */
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 1px 0 rgba(255, 255, 255, 0.05);
    transition: all var(--timing-base) var(--ease-out);
  }

  .ticker-input-wrapper:hover {
    background: var(--glass-surface-2);
    border-color: var(--glass-border-2);
  }

  .ticker-input-wrapper:focus-within {
    background: var(--glass-surface-3);
    border-color: var(--accent-trust);
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 1px 0 rgba(255, 255, 255, 0.1),
      0 0 0 1px var(--accent-trust);
  }

  /* Professional fintech input field styling */
  .ticker-input {
    width: 100%;
    padding: var(--spacing-3) var(--spacing-10) var(--spacing-3) var(--spacing-3);
    border: none;
    background: transparent;
    font-family: var(--font-mono);
    font-size: var(--font-size-ticker);
    font-weight: var(--font-weight-semibold);
    line-height: var(--line-height-normal);
    letter-spacing: var(--letter-spacing-wider);
    text-align: center;
    text-transform: uppercase;
    color: var(--text-primary);
    /* Advanced text rendering */
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    /* Performance optimizations */
    box-sizing: border-box;
    /* Enhanced transitions */
    transition: all var(--timing-base) var(--ease-out);
    /* Financial data formatting */
    font-variant-numeric: tabular-nums;
    /* Remove default styling */
    outline: none;
    resize: none;
    /* Mobile optimizations */
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
  }

  .ticker-input::placeholder {
    color: var(--neutral-color);
    font-weight: var(--font-weight-medium);
    opacity: 0.7;
    transition: opacity var(--timing-fast) var(--ease-out);
  }

  .ticker-input:focus::placeholder {
    opacity: 0.4;
    transform: translateY(-1px);
  }

  /* Enhanced focus states using fintech design system */
  .ticker-input:focus-visible {
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
    border-radius: var(--radius-md);
  }

  /* Professional validation states with semantic colors */
  .ticker-input.valid {
    color: var(--accent-success);
    text-shadow: 0 0 8px rgba(16, 185, 129, 0.3);
  }

  .ticker-input-wrapper:has(.ticker-input.valid) {
    border-color: var(--accent-success);
    background: rgba(16, 185, 129, 0.05);
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 1px 0 rgba(255, 255, 255, 0.1),
      0 0 8px rgba(16, 185, 129, 0.2);
  }

  .ticker-input.error {
    color: var(--accent-error);
    /* Animation removed for performance */
  }

  .ticker-input-wrapper:has(.ticker-input.error) {
    border-color: var(--accent-error);
    background: rgba(239, 68, 68, 0.05);
    box-shadow:
      inset 0 1px 2px rgba(0, 0, 0, 0.1),
      0 1px 0 rgba(255, 255, 255, 0.1),
      0 0 8px rgba(239, 68, 68, 0.2);
  }

  /* Enhanced disabled state */
  .ticker-input:disabled {
    color: rgba(247, 250, 252, 0.4);
    cursor: not-allowed;
    text-shadow: none;
  }

  .ticker-input-wrapper:has(.ticker-input:disabled) {
    background: var(--glass-surface-1);
    border-color: rgba(255, 255, 255, 0.05);
    opacity: 0.6;
    cursor: not-allowed;
  }

  /* Professional validation icon positioning and styling */
  .validation-icon {
    position: absolute;
    right: var(--spacing-3);
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    pointer-events: none;
    z-index: 2;
    /* Enhanced icon transitions */
    transition: all var(--timing-base) var(--ease-out);
  }

  .validation-success {
    color: var(--accent-success);
    font-weight: var(--font-weight-bold);
    font-size: var(--font-size-body);
    text-shadow: 0 0 4px rgba(16, 185, 129, 0.4);
    /* Animation removed for performance */
  }

  .validation-error {
    color: var(--accent-error);
    font-weight: var(--font-weight-bold);
    font-size: var(--font-size-small);
    background: var(--gradient-error-subtle);
    border: 1px solid var(--accent-error);
    border-radius: var(--radius-full);
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Animation removed for performance */
    /* Enhanced error styling */
    box-shadow:
      0 2px 4px rgba(239, 68, 68, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  /* Professional error message with glassmorphic styling */
  .error-message {
    background: var(--gradient-error-subtle);
    color: var(--accent-error);
    padding: var(--spacing-2) var(--spacing-3);
    border-radius: var(--radius-lg);
    font-family: var(--font-body);
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-normal);
    letter-spacing: var(--letter-spacing-wide);
    border: 1px solid var(--accent-error);
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
    /* Enhanced error styling */
    box-shadow:
      0 2px 8px rgba(239, 68, 68, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    /* Backdrop blur for glassmorphism */
    backdrop-filter: var(--glass-blur-xs);
    -webkit-backdrop-filter: var(--glass-blur-xs);
    /* Animation removed for performance */
    margin-top: var(--spacing-2);
  }

  .error-message::before {
    content: '⚠';
    font-size: var(--font-size-body);
    flex-shrink: 0;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  }

  /* Enhanced mobile responsiveness with fintech styling (320px-767px) */
  @media (max-width: 767px) {
    .shared-ticker-input-container {
      max-width: 100%;
      padding: var(--spacing-3);
      /* Mobile glassmorphic optimization */
      backdrop-filter: var(--glass-blur-md);
      -webkit-backdrop-filter: var(--glass-blur-md);
    }

    .ticker-input {
      padding: var(--spacing-4) var(--spacing-12) var(--spacing-4) var(--spacing-4);
      font-size: var(--font-size-body); /* Prevents iOS zoom while maintaining readability */
      min-height: 44px; /* Touch-friendly minimum */
      letter-spacing: var(--letter-spacing-wide);
      /* Enhanced mobile interactions */
      -webkit-tap-highlight-color: transparent;
    }

    .ticker-label {
      font-size: var(--font-size-body);
      font-weight: var(--font-weight-medium);
    }

    .error-message {
      padding: var(--spacing-3) var(--spacing-4);
      font-size: var(--font-size-small);
    }

    .validation-icon {
      right: var(--spacing-4);
      width: 24px;
      height: 24px;
    }
  }

  /* Enhanced tablet optimizations (768px-1024px) */
  @media (min-width: 768px) and (max-width: 1024px) {
    .ticker-input {
      padding: calc(var(--spacing-3) + 1px) var(--spacing-11) calc(var(--spacing-3) + 1px) calc(var(--spacing-3) + 1px);
      font-size: calc(var(--font-size-ticker) * 0.95);
    }

    .shared-ticker-input-container {
      max-width: 220px;
    }
  }

  /* Enhanced desktop optimizations with sophisticated effects (1025px+) */
  @media (min-width: 1025px) {
    .shared-ticker-input-container {
      max-width: 260px;
      transition: all var(--timing-base) var(--ease-out);
    }

    .shared-ticker-input-container:hover {
      transform: translateY(-2px);
      box-shadow: var(--glass-shadow-lg), var(--shadow-glow-trust);
    }

    .shared-ticker-input-container:focus-within {
      transform: translateY(-3px);
      box-shadow:
        0 0 0 1px var(--accent-trust),
        var(--glass-shadow-lg),
        var(--shadow-glow-trust),
        0 12px 32px rgba(0, 0, 0, 0.15);
    }
  }

  /* Enhanced cross-platform optimizations with fintech styling */
  @media (hover: none) and (pointer: coarse) {
    /* Touch devices - enhanced touch interaction */
    .ticker-input {
      min-height: 48px; /* Larger touch target */
      /* Simplified transitions for touch */
      transition: color var(--timing-fast) var(--ease-out);
    }

    .shared-ticker-input-container:hover {
      /* Maintain original styling on touch hover */
      transform: none;
    }

    /* Enhanced touch feedback */
    .shared-ticker-input-container:focus-within {
      background: var(--glass-surface-4);
      transform: none;
    }
  }

  @media (hover: hover) and (pointer: fine) {
    /* Precision input devices - sophisticated hover states */
    .ticker-input-wrapper:hover {
      background: var(--glass-surface-3);
    }

    .ticker-input:not(:disabled):hover {
      color: var(--accent-trust);
      text-shadow: 0 0 8px rgba(99, 102, 241, 0.3);
    }

    .ticker-input.valid:not(:disabled):hover {
      color: var(--accent-success-hover);
    }

    .ticker-input.error:not(:disabled):hover {
      color: var(--accent-error-hover);
    }
  }

  /* Enhanced accessibility features */
  @media (prefers-contrast: high) {
    .shared-ticker-input-container {
      border-width: 2px;
      background: rgba(26, 32, 44, 0.9);
    }

    .ticker-input-wrapper {
      border-width: 2px;
    }

    .ticker-input.valid {
      text-shadow: none;
      color: var(--accent-success-hover);
    }

    .ticker-input.error {
      color: var(--accent-error-hover);
    }

    .error-message {
      border-width: 2px;
      background: rgba(239, 68, 68, 0.2);
    }
  }

  /* Enhanced reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .shared-ticker-input-container,
    .ticker-input-wrapper,
    .ticker-input,
    .ticker-label,
    .validation-icon {
      transition: none;
      animation: none;
    }

    .shared-ticker-input-container:hover,
    .shared-ticker-input-container:focus-within {
      transform: none;
    }

    .validation-success {
      animation: none;
    }

    .validation-error {
      animation: none;
    }

    .error-message {
      animation: none;
    }
  }

  /* Print styles for export functionality */
  @media print {
    .shared-ticker-input-container {
      background: white !important;
      border: 2px solid #000;
      box-shadow: none;
      backdrop-filter: none;
    }

    .ticker-input-wrapper {
      background: white !important;
      border: 1px solid #000;
    }

    .ticker-input {
      color: #000 !important;
      text-shadow: none;
    }

    .ticker-label {
      color: #000 !important;
    }

    .error-message {
      background: #fff !important;
      color: #000 !important;
      border: 1px solid #000;
    }

    .validation-success,
    .validation-error {
      color: #000 !important;
      background: #fff !important;
      text-shadow: none;
      box-shadow: none;
    }
  }

  /* Forced colors mode support (Windows High Contrast) */
  @media (forced-colors: active) {
    .shared-ticker-input-container {
      border: 2px solid ButtonBorder;
      background: ButtonFace;
    }

    .ticker-input-wrapper {
      border: 2px solid ButtonBorder;
      background: Field;
    }

    .ticker-input {
      color: FieldText;
      background: Field;
    }

    .ticker-label {
      color: ButtonText;
    }

    .ticker-input:focus-visible {
      outline: 3px solid Highlight;
      outline-offset: 2px;
    }

    .error-message {
      border: 2px solid ButtonBorder;
      background: Mark;
      color: MarkText;
    }
  }

  /* Legacy browser support */
  @supports not (backdrop-filter: blur(8px)) {
    .shared-ticker-input-container {
      background: rgba(45, 55, 72, 0.95);
    }

    .ticker-input-wrapper {
      background: rgba(26, 32, 44, 0.8);
    }
  }

  /* Animation keyframes removed for performance */
`;
