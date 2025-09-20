import { useState, useCallback, useRef, useEffect } from 'react';
import { Message } from '../types/chat_OpenAI';
import {
  convertSingleMessageToMarkdown,
  copyToClipboard,
} from '../utils/exportHelpers';

interface MessageCopyButtonProps {
  message: Message;
  className?: string;
}

type ButtonState = 'idle' | 'loading' | 'success' | 'error';

export default function MessageCopyButton({
  message,
  className = '',
}: MessageCopyButtonProps) {
  const [buttonState, setButtonState] = useState<ButtonState>('idle');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [isHovered, setIsHovered] = useState(false);
  const [showSuccessGlow, setShowSuccessGlow] = useState(false);

  // Ref to store timeout ID for cleanup
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Cleanup timeout on component unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  const updateButtonState = useCallback(
    (state: ButtonState, errorMsg?: string) => {
      // Clear any existing timeout to prevent conflicts
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }

      setButtonState(state);
      setErrorMessage(errorMsg || '');

      // Auto-reset success and error states after timeout
      if (state === 'success' || state === 'error') {
        const timeoutDuration = state === 'success' ? 2000 : 4000; // Errors show longer

        timeoutRef.current = setTimeout(() => {
          setButtonState('idle');
          setErrorMessage('');
          timeoutRef.current = null;
        }, timeoutDuration);
      }
    },
    []
  );

  const handleCopyMessage = useCallback(
    async (event: React.MouseEvent) => {
      // Prevent event from bubbling up to parent elements
      event.stopPropagation();

      updateButtonState('loading');

      try {
        const markdownContent = convertSingleMessageToMarkdown(message);
        await copyToClipboard(markdownContent);
        updateButtonState('success');
        // Trigger success glow effect
        setShowSuccessGlow(true);
        setTimeout(() => setShowSuccessGlow(false), 1000);
      } catch (error) {
        const errorMsg =
          error instanceof Error ? error.message : 'Failed to copy message';
        updateButtonState('error', errorMsg);
      }
    },
    [message, updateButtonState]
  );

  // Enhanced hover handlers for sophisticated micro-interactions
  const handleMouseEnter = useCallback(() => {
    setIsHovered(true);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setIsHovered(false);
  }, []);

  const getButtonIcon = (): string => {
    switch (buttonState) {
      case 'loading':
        return 'Copying...';
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '📋';
    }
  };

  const getButtonTitle = (): string => {
    switch (buttonState) {
      case 'loading':
        return 'Copying...';
      case 'success':
        return 'Copied to clipboard!';
      case 'error':
        return errorMessage || 'Copy failed';
      default:
        return 'Copy message to clipboard as markdown';
    }
  };

  const getButtonClass = (): string => {
    const baseClass = 'message-copy-button';
    const customClass = className ? ` ${className}` : '';
    const hoverClass = isHovered ? ' hovered' : '';
    const glowClass = showSuccessGlow ? ' success-glow' : '';

    switch (buttonState) {
      case 'loading':
        return `${baseClass} loading${customClass}${hoverClass}${glowClass}`;
      case 'success':
        return `${baseClass} success${customClass}${hoverClass}${glowClass}`;
      case 'error':
        return `${baseClass} error${customClass}${hoverClass}${glowClass}`;
      default:
        return `${baseClass}${customClass}${hoverClass}${glowClass}`;
    }
  };

  return (
    <button
      onClick={handleCopyMessage}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      disabled={buttonState === 'loading'}
      className={getButtonClass()}
      title={getButtonTitle()}
      aria-label={getButtonTitle()}
    >
      <span className={`copy-icon icon-${buttonState}`}>{getButtonIcon()}</span>
    </button>
  );
}

// Professional Fintech Glassmorphic Styles with Advanced Micro-Interactions
export const messageCopyButtonStyles = `
  /* ==========================================================================
     MESSAGE COPY BUTTON - Advanced Fintech Micro-Interactions
     ========================================================================== */
  
  .message-copy-button {
    /* Seamless Glassmorphic Integration */
    position: absolute;
    top: var(--spacing-2);
    right: var(--spacing-2);
    width: 32px;
    height: 32px;
    
    /* Professional Glass Surface */
    background: var(--glass-surface-3);
    backdrop-filter: var(--glass-blur-sm);
    border: 1px solid var(--glass-border-2);
    border-radius: 8px;
    
    /* Professional Interaction */
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--font-size-small);
    
    /* Seamless Integration - Hidden by Default */
    opacity: 0;
    transform: scale(0.9) translateZ(0); /* GPU acceleration */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 10;
    
    /* Professional Shadow */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    
    /* Performance optimization */
    will-change: transform, opacity, box-shadow;
    backface-visibility: hidden;
  }
  
  /* Enhanced Professional Hover State */
  .message-copy-button:hover,
  .message-copy-button.hovered {
    background: var(--glass-surface-4);
    border-color: var(--glass-border-3);
    transform: scale(1.05) translateY(-1px) translateZ(0);
    box-shadow: 
      0 4px 20px rgba(0, 0, 0, 0.2),
      0 2px 8px rgba(139, 92, 246, 0.15);
    backdrop-filter: var(--glass-blur-md);
  }
  
  /* Enhanced Active State */
  .message-copy-button:active {
    transform: scale(0.95) translateY(0) translateZ(0);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
  
  /* Disabled State */
  .message-copy-button:disabled {
    cursor: not-allowed;
    opacity: 0.4;
    background: var(--glass-surface-1);
    transform: scale(0.9);
  }
  
  /* Enhanced Loading State - Professional Info Color */
  .message-copy-button.loading {
    background: linear-gradient(135deg, var(--accent-info) 0%, var(--accent-info-light) 100%);
    border-color: var(--accent-info);
    color: var(--text-primary);
    cursor: wait;
    /* Animation removed for performance */
    box-shadow: 
      0 4px 16px rgba(59, 130, 246, 0.3),
      0 0 20px rgba(59, 130, 246, 0.1);
  }
  
  /* Enhanced Success State - Professional Success Treatment */
  .message-copy-button.success {
    background: linear-gradient(135deg, var(--accent-success) 0%, var(--accent-success-light) 100%);
    border-color: var(--accent-success);
    color: var(--text-primary);
    box-shadow: 
      0 4px 20px rgba(16, 185, 129, 0.4),
      0 0 24px rgba(16, 185, 129, 0.2);
    animation: success-celebrate 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .message-copy-button.success:hover,
  .message-copy-button.success.hovered {
    background: linear-gradient(135deg, var(--accent-success-light) 0%, var(--accent-success) 100%);
    transform: scale(1.08) translateY(-2px) translateZ(0);
    box-shadow: 
      0 6px 24px rgba(16, 185, 129, 0.5),
      0 0 32px rgba(16, 185, 129, 0.3);
  }
  
  /* Enhanced Error State - Professional Error Treatment */
  .message-copy-button.error {
    background: linear-gradient(135deg, var(--accent-error) 0%, var(--accent-error-light) 100%);
    border-color: var(--accent-error);
    color: var(--text-primary);
    box-shadow: 
      0 4px 16px rgba(239, 68, 68, 0.4),
      0 0 20px rgba(239, 68, 68, 0.2);
    /* Animation removed for performance */
  }
  
  .message-copy-button.error:hover,
  .message-copy-button.error.hovered {
    background: linear-gradient(135deg, var(--accent-error-hover) 0%, var(--accent-error) 100%);
    transform: scale(1.05) translateY(-1px) translateZ(0);
    box-shadow: 
      0 6px 20px rgba(239, 68, 68, 0.5),
      0 0 28px rgba(239, 68, 68, 0.3);
  }
  
  /* Enhanced Professional Icon Container */
  .copy-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    line-height: 1;
    
    /* Enhanced Icon Treatment */
    filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.2));
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform: translateZ(0);
  }
  
  /* Icon State Animations */
  .copy-icon.icon-idle {
    transform: scale(1) rotate(0deg) translateZ(0);
  }
  
  .copy-icon.icon-loading {
    transform: scale(1.1) rotate(180deg) translateZ(0);
    /* Animation removed for performance */
  }
  
  .copy-icon.icon-success {
    transform: scale(1.2) rotate(360deg) translateZ(0);
    filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.6));
    /* Animation removed for performance */
  }
  
  .copy-icon.icon-error {
    transform: scale(1.1) rotate(-10deg) translateZ(0);
    filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.6));
    animation: icon-error-wobble 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* Seamless Message Integration */
  .message-bubble {
    position: relative;
    overflow: visible;
  }
  
  /* Professional Reveal on Hover */
  .message-bubble:hover .message-copy-button {
    opacity: 1;
    transform: scale(1.0);
  }
  
  /* Focus State for Accessibility */
  .message-copy-button:focus-visible {
    opacity: 1;
    transform: scale(1.0);
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
  }
  
  .message-copy-button.success:focus-visible {
    outline-color: var(--focus-ring-success);
  }
  
  .message-copy-button.error:focus-visible {
    outline-color: var(--focus-ring-error);
  }
  
  /* Touch Device Optimization */
  @media (hover: none) {
    .message-copy-button {
      opacity: 0.6;
      transform: scale(1.0);
    }
    
    .message-bubble:hover .message-copy-button,
    .message-copy-button:focus {
      opacity: 1;
    }
  }
  
  /* Responsive Design - Mobile Enhancement */
  @media (max-width: 640px) {
    .message-copy-button {
      width: 36px;
      height: 36px;
      font-size: var(--font-size-body);
      top: var(--spacing-2);
      right: var(--spacing-2);
      
      /* Better touch targets */
      min-width: 44px;
      min-height: 44px;
    }
  }
  
  /* Tablet Optimization */
  @media (min-width: 641px) and (max-width: 1024px) {
    .message-copy-button {
      width: 34px;
      height: 34px;
    }
  }
  
  /* Desktop Enhancement */
  @media (min-width: 1025px) {
    .message-copy-button {
      width: 30px;
      height: 30px;
    }
    
    .message-copy-button:hover {
      backdrop-filter: var(--glass-blur-md);
    }
  }
  
  /* High Contrast Mode Support */
  @media (prefers-contrast: high) {
    .message-copy-button {
      border-width: 2px;
      background: var(--background-secondary);
    }
    
    .message-copy-button:hover {
      border-color: var(--accent-trust);
    }
  }
  
  /* Enhanced Reduced Motion Support */
  @media (prefers-reduced-motion: reduce) {
    .message-copy-button {
      transition: opacity 0.2s ease;
      transform: none;
      animation: none;
    }
    
    .message-copy-button:hover,
    .message-copy-button.hovered,
    .message-copy-button:active {
      transform: none;
      animation: none;
    }
    
    .message-bubble:hover .message-copy-button {
      transform: none;
    }
    
    .copy-icon,
    .copy-icon.icon-loading,
    .copy-icon.icon-success,
    .copy-icon.icon-error {
      transform: none;
      animation: none;
    }
    
    .message-copy-button.loading,
    .message-copy-button.success,
    .message-copy-button.error,
    .message-copy-button.success-glow {
      animation: none;
    }
  }
  
  /* Enhanced Performance Optimizations */
  .message-copy-button {
    will-change: opacity, transform, box-shadow;
    transform: translateZ(0); /* Force GPU acceleration */
    contain: layout style paint;
  }
  
  .copy-icon {
    will-change: transform, filter;
    contain: layout style;
  }
  
  /* High DPI display optimization */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
    .message-copy-button {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  }
  
  /* Enhanced Focus States for Accessibility */
  .message-copy-button:focus-visible {
    opacity: 1;
    transform: scale(1.0) translateZ(0);
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
    box-shadow: 
      0 0 0 4px rgba(139, 92, 246, 0.2),
      0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .message-copy-button.success:focus-visible {
    outline-color: var(--focus-ring-success);
    box-shadow: 
      0 0 0 4px rgba(16, 185, 129, 0.2),
      0 4px 20px rgba(16, 185, 129, 0.4);
  }
  
  .message-copy-button.error:focus-visible {
    outline-color: var(--focus-ring-error);
    box-shadow: 
      0 0 0 4px rgba(239, 68, 68, 0.2),
      0 4px 20px rgba(239, 68, 68, 0.4);
  }
  
  /* Success Glow Effect */
  .message-copy-button.success-glow {
    box-shadow: 
      0 0 40px rgba(16, 185, 129, 0.6),
      0 4px 20px rgba(16, 185, 129, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    /* Animation removed for performance */
  }
  
  /* All keyframe animations removed for performance */
  @keyframes loading-pulse {
    0%, 100% {
      opacity: 1;
      box-shadow: 
        0 4px 16px rgba(59, 130, 246, 0.3),
        0 0 20px rgba(59, 130, 246, 0.1);
    }
    50% {
      opacity: 0.8;
      box-shadow: 
        0 6px 20px rgba(59, 130, 246, 0.4),
        0 0 28px rgba(59, 130, 246, 0.2);
    }
  }
  
  @keyframes success-celebrate {
    0% {
      transform: scale(0.9) translateY(0) translateZ(0);
    }
    50% {
      transform: scale(1.15) translateY(-2px) translateZ(0);
      box-shadow: 
        0 8px 32px rgba(16, 185, 129, 0.5),
        0 0 40px rgba(16, 185, 129, 0.3);
    }
    100% {
      transform: scale(1.05) translateY(-1px) translateZ(0);
    }
  }
  
  @keyframes error-shake {
    0%, 100% {
      transform: scale(1.05) translateX(0) translateZ(0);
    }
    10%, 30%, 50%, 70%, 90% {
      transform: scale(1.05) translateX(-2px) translateZ(0);
    }
    20%, 40%, 60%, 80% {
      transform: scale(1.05) translateX(2px) translateZ(0);
    }
  }
  
  @keyframes success-glow-pulse {
    0% {
      box-shadow: 
        0 4px 20px rgba(16, 185, 129, 0.4),
        0 0 24px rgba(16, 185, 129, 0.2);
    }
    50% {
      box-shadow: 
        0 0 60px rgba(16, 185, 129, 0.8),
        0 8px 32px rgba(16, 185, 129, 0.6),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    100% {
      box-shadow: 
        0 4px 20px rgba(16, 185, 129, 0.4),
        0 0 24px rgba(16, 185, 129, 0.2);
    }
  }
  
  /* Icon Keyframe Animations */
  @keyframes icon-loading-spin {
    0% {
      transform: scale(1.1) rotate(180deg) translateZ(0);
    }
    100% {
      transform: scale(1.1) rotate(540deg) translateZ(0);
    }
  }
  
  @keyframes icon-success-bounce {
    0%, 20%, 53%, 80%, 100% {
      transform: scale(1.2) rotate(360deg) translate3d(0, 0, 0);
    }
    40%, 43% {
      transform: scale(1.3) rotate(360deg) translate3d(0, -3px, 0);
    }
    70% {
      transform: scale(1.25) rotate(360deg) translate3d(0, -2px, 0);
    }
    90% {
      transform: scale(1.22) rotate(360deg) translate3d(0, -1px, 0);
    }
  }
  
  @keyframes icon-error-wobble {
    0%, 100% {
      transform: scale(1.1) rotate(-10deg) translateZ(0);
    }
    25% {
      transform: scale(1.15) rotate(-15deg) translateZ(0);
    }
    75% {
      transform: scale(1.08) rotate(-5deg) translateZ(0);
    }
  }
`;
