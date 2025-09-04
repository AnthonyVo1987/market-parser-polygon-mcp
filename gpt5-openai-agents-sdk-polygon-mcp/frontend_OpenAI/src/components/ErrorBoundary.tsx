import React from 'react';
import { ErrorBoundaryProps, ErrorFallbackProps } from '../types/error';
import { ErrorBoundaryState, ErrorInfo } from '../types/chat_OpenAI';

// Default error fallback component
const DefaultErrorFallback: React.FC<ErrorFallbackProps> = ({ 
  error, 
  errorInfo, 
  resetError 
}) => {
  return (
    <div role="alert" className="error-boundary-fallback">
      <h2>Something went wrong</h2>
      <details style={{ whiteSpace: 'pre-wrap' }}>
        <summary>Error Details</summary>
        <div className="error-details">
          <p><strong>Error:</strong> {error.message}</p>
          {errorInfo && (
            <p><strong>Component Stack:</strong> {errorInfo.componentStack}</p>
          )}
        </div>
      </details>
      {resetError && (
        <button 
          onClick={resetError}
          className="error-reset-button"
          aria-label="Try again"
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

    // Log error for debugging
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

// Error boundary styles
export const errorBoundaryStyles = `
  .error-boundary-fallback {
    padding: 20px;
    margin: 20px;
    border: 2px solid #ff6b6b;
    border-radius: 8px;
    background-color: #fff5f5;
    color: #721c24;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  .error-boundary-fallback h2 {
    color: #c53030;
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 1.25rem;
  }

  .error-boundary-fallback details {
    margin-bottom: 16px;
    padding: 12px;
    background-color: #fed7d7;
    border-radius: 4px;
    border: 1px solid #fc8181;
  }

  .error-boundary-fallback summary {
    cursor: pointer;
    font-weight: 600;
    color: #742a2a;
    margin-bottom: 8px;
  }

  .error-boundary-fallback summary:hover {
    color: #c53030;
  }

  .error-details {
    margin-top: 8px;
    font-family: 'Courier New', monospace;
    font-size: 0.875rem;
    line-height: 1.4;
  }

  .error-details p {
    margin: 8px 0;
  }

  .error-details strong {
    color: #c53030;
  }

  .error-reset-button {
    background-color: #c53030;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    transition: background-color 0.2s ease;
  }

  .error-reset-button:hover {
    background-color: #9b2c2c;
  }

  .error-reset-button:focus {
    outline: 2px solid #c53030;
    outline-offset: 2px;
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .error-boundary-fallback {
      border: 3px solid;
      background-color: white;
    }
    
    .error-reset-button {
      border: 2px solid;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .error-reset-button {
      transition: none;
    }
  }
`;