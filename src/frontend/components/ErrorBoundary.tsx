/* eslint-disable react-refresh/only-export-components */
import React from 'react';
import { ErrorBoundaryState, ErrorInfo } from '../types/chat_OpenAI';
import { ErrorBoundaryProps, ErrorFallbackProps } from '../types/error';

// Default error fallback component
const DefaultErrorFallback: React.FC<ErrorFallbackProps> = ({
  error,
  errorInfo,
  resetError,
}) => {
  return (
    <div role='alert' className='error-boundary-fallback'>
      <h2>Something went wrong</h2>
      <details style={{ whiteSpace: 'pre-wrap' }}>
        <summary>Error Details</summary>
        <div className='error-details'>
          <p>
            <strong>Error:</strong> {error.message}
          </p>
          {errorInfo && (
            <p>
              <strong>Component Stack:</strong> {errorInfo.componentStack}
            </p>
          )}
        </div>
      </details>
      {resetError && (
        <button
          onClick={resetError}
          className='error-reset-button'
          aria-label='Try again'
        >
          Try again
        </button>
      )}
    </div>
  );
};

// Enhanced Error Boundary Component
export default class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    const enhancedErrorInfo: ErrorInfo = {
      componentStack: errorInfo.componentStack || '',
    };

    this.setState({
      error,
      errorInfo: enhancedErrorInfo,
    });

    // Call optional error handler
    if (this.props.onError) {
      this.props.onError(error, enhancedErrorInfo);
    }

    // Log error for debugging - ESLint disabled for error boundary logging
    // eslint-disable-next-line no-console
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  resetError = () => {
    this.setState({
      hasError: false,
      error: undefined,
      errorInfo: undefined,
    });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;

      return (
        <FallbackComponent
          error={this.state.error}
          errorInfo={this.state.errorInfo ?? undefined}
          resetError={this.resetError}
        />
      );
    }

    return this.props.children;
  }
}

// Professional Fintech Error Boundary Styles - Trustworthy Error Presentation
export const errorBoundaryStyles = `
  /* ==========================================================================
     ERROR BOUNDARY - Professional Fintech Error Handling with Trustworthy Design
     ========================================================================== */
  
  .error-boundary-fallback {
    /* Professional Glassmorphic Error Container */
    background: var(--glass-surface-3);
    /* backdrop-filter removed for performance */
    border: 2px solid var(--accent-error);
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
    
    /* Professional Spacing */
    padding: var(--spacing-6);
    margin: var(--spacing-4);
    max-width: 600px;
    
    /* Professional Typography */
    color: var(--text-primary);
    font-family: var(--font-body);
    line-height: var(--line-height-relaxed);
    
    /* Modern Enhancement */
    position: relative;
    overflow: hidden;
  }
  
  /* Error Accent Border */
  .error-boundary-fallback::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    /* Complex gradient simplified for performance */
    background: var(--accent-error);
    opacity: 0.8;
  }
  
  /* Professional Error Title */
  .error-boundary-fallback h2 {
    color: var(--accent-error-light);
    margin-top: 0;
    margin-bottom: var(--spacing-4);
    font-size: var(--font-size-h4);
    font-weight: var(--font-weight-semibold);
    font-family: var(--font-display);
    
    /* Error Icon Integration */
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
  }
  
  .error-boundary-fallback h2::before {
    content: '⚠️';
    font-size: var(--font-size-h3);
    /* filter: grayscale(0.2); removed for performance */
  }
  
  /* Professional Error Details Container */
  .error-boundary-fallback details {
    margin-bottom: var(--spacing-4);
    padding: var(--spacing-3);
    
    /* Glass Effect for Details */
    background: var(--glass-surface-2);
    /* backdrop-filter removed for performance */
    border: 1px solid var(--glass-border-2);
    border-radius: 12px;
    
    /* Professional Enhancement */
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }
  
  /* Interactive Summary */
  .error-boundary-fallback summary {
    cursor: pointer;
    font-weight: var(--font-weight-semibold);
    color: var(--text-secondary);
    margin-bottom: var(--spacing-2);
    
    font-size: var(--font-size-body);
    padding: var(--spacing-1);
    border-radius: 4px;
    transition: opacity 0.2s ease;
    
    /* Professional Enhancement */
    display: flex;
    align-items: center;
    gap: var(--spacing-1);
  }
  
  .error-boundary-fallback summary::before {
    content: '▶';
    /* transition: transform 0.1s ease; removed for performance */
    font-size: var(--font-size-small);
  }
  
  .error-boundary-fallback details[open] summary::before {
    transform: rotate(90deg);
  }
  
  .error-boundary-fallback summary:hover {
    color: var(--accent-error-light);
    background: var(--glass-surface-1);
    transform: translateX(var(--spacing-1));
  }
  
  /* Professional Error Details */
  .error-details {
    margin-top: var(--spacing-2);
    font-family: var(--font-mono);
    font-size: var(--font-size-small);
    line-height: var(--line-height-normal);
    
    /* Code Block Styling */
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    padding: var(--spacing-3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    
    /* Modern Scrollbar */
    overflow-x: auto;
  }
  
  .error-details p {
    margin: var(--spacing-2) 0;
    word-break: break-word;
  }
  
  .error-details strong {
    color: var(--accent-error);
    font-weight: var(--font-weight-bold);
  }
  
  /* Professional Reset Button */
  .error-reset-button {
    /* Fintech Button Design */
    /* Complex gradient simplified for performance */
    background: var(--accent-error);
    color: var(--text-primary);
    border: 1px solid var(--accent-error);
    
    padding: var(--spacing-3) var(--spacing-5);
    border-radius: 12px;
    cursor: pointer;
    
    /* Professional Typography */
    font-family: var(--font-body);
    font-size: var(--font-size-body);
    font-weight: var(--font-weight-medium);
    letter-spacing: var(--letter-spacing-wide);
    
    /* Professional Transitions */
    transition: opacity 0.2s ease;
    position: relative;
    overflow: hidden;
    
    /* Enhancement */
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
    
    /* Button Icon */
    display: flex;
    align-items: center;
    gap: var(--spacing-2);
  }
  
  .error-reset-button::before {
    content: '🔄';
    font-size: var(--font-size-small);
  }
  
  .error-reset-button:hover {
    /* Complex gradient simplified for performance */
    background: var(--accent-error-hover);
    transform: translateY(-2px);
    box-shadow: 0 3px 12px rgba(239, 68, 68, 0.3);
  }
  
  .error-reset-button:active {
    transform: translateY(0);
  }
  
  .error-reset-button:focus-visible {
    outline: 2px solid var(--focus-ring-error);
    outline-offset: 2px;
  }
  
  /* Responsive Design - Mobile Optimization */
  @media (max-width: 768px) {
    .error-boundary-fallback {
      padding: var(--spacing-4);
      margin: var(--spacing-2);
      border-radius: 12px;
    }
    
    .error-boundary-fallback h2 {
      font-size: var(--font-size-h5);
      margin-bottom: var(--spacing-3);
    }
    
    .error-boundary-fallback details {
      padding: var(--spacing-2);
    }
    
    .error-details {
      font-size: var(--font-size-micro);
      padding: var(--spacing-2);
    }
    
    .error-reset-button {
      padding: var(--spacing-3);
      font-size: var(--font-size-small);
      width: 100%;
      justify-content: center;
    }
  }
  
  /* Tablet Optimization */
  @media (min-width: 769px) and (max-width: 1024px) {
    .error-boundary-fallback {
      padding: var(--spacing-5);
    }
  }
  
  /* Desktop Enhancement */
  @media (min-width: 1025px) {
    .error-boundary-fallback {
      padding: var(--spacing-8);
      margin: var(--spacing-6);
    }
    
    .error-boundary-fallback:hover {
      /* backdrop-filter removed for performance */
    }
  }
  
  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .error-boundary-fallback {
      border: 3px solid var(--accent-error);
      background: var(--background-primary);
    }
    
    .error-reset-button {
      border: 2px solid var(--accent-error);
      background: var(--accent-error);
    }
    
    .error-details {
      border: 2px solid rgba(255, 255, 255, 0.3);
    }
  }
  
  /* Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .error-reset-button {
      transition: none;
      transform: none;
    }
    
    .error-reset-button:hover {
      transform: none;
    }
    
    .error-boundary-fallback summary {
      transition: none;
    }
    
    .error-boundary-fallback summary::before {
      transition: none;
    }
  }
  
  /* Performance Optimizations */
  .error-boundary-fallback {
    /* will-change: backdrop-filter; removed for performance */
    transform: translateZ(0); /* Force GPU acceleration */
  }
  
  /* Professional Loading Animation for Retry */
  .error-reset-button[data-loading="true"] {
    pointer-events: none;
    opacity: 0.7;
  }
  
  .error-reset-button[data-loading="true"]::after {
    content: 'Loading...';
    position: absolute;
    top: 50%;
    right: var(--spacing-3);
    font-size: 14px;
    color: var(--text-primary);
    transform: translateY(-50%);
  }
  
  /* @keyframes spin removed for performance */
`;
