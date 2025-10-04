import { useCallback, useEffect, useRef, useState } from 'react';
import { Message } from '../types/chat_OpenAI';

// Inline clipboard utility (extracted from removed exportHelpers)
const copyToClipboard = async (text: string): Promise<void> => {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    textArea.style.opacity = '0';
    textArea.setAttribute('readonly', '');
    textArea.setAttribute('aria-hidden', 'true');

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    const successful = document.execCommand('copy');
    textArea.remove();

    if (!successful) {
      throw new Error('Copy command was unsuccessful');
    }
  } catch (error) {
    throw new Error(
      `Failed to copy to clipboard: ${error instanceof Error ? error.message : 'Unknown error'}`
    );
  }
};

// Inline message formatting (extracted from removed exportHelpers)
const convertSingleMessageToMarkdown = (message: Message): string => {
  const sender = message.sender === 'user' ? '👤 User' : '🤖 AI Assistant';
  const timestamp = message.timestamp.toLocaleString();
  const content = message.content.trim();

  return `## ${sender} - ${timestamp}\n\n${content}`;
};

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
    /* backdrop-filter removed for performance */
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
    /* transform: scale(0.9); removed for performance */
    transition: opacity 0.2s ease;
    z-index: 10;
    
    /* Professional Shadow */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    
    /* Performance optimization */
    /* will-change: transform, opacity, box-shadow; removed for performance */
    backface-visibility: hidden;
  }
  
  /* Enhanced Professional Hover State */
  .message-copy-button:hover,
  .message-copy-button.hovered {
    background: var(--glass-surface-4);
    border-color: var(--glass-border-3);
    /* transform: scale(1.05) translateY(-1px); removed for performance */
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    /* backdrop-filter removed for performance */
  }
  
  /* Enhanced Active State */
  .message-copy-button:active {
    /* transform: scale(0.95); removed for performance */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
  
  /* Disabled State */
  .message-copy-button:disabled {
    cursor: not-allowed;
    opacity: 0.4;
    background: var(--glass-surface-1);
    /* transform: scale(0.9); removed for performance */
  }
  
  /* Enhanced Loading State - Professional Info Color */
  .message-copy-button.loading {
    /* Complex gradient simplified for performance */
    background: var(--accent-info);
    border-color: var(--accent-info);
    color: var(--text-primary);
    cursor: wait;
    /* Animation removed for performance */
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
  }
  
  /* Enhanced Success State - Professional Success Treatment */
  .message-copy-button.success {
    /* Complex gradient simplified for performance */
    background: var(--accent-success);
    border-color: var(--accent-success);
    color: var(--text-primary);
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    /* animation: success-celebrate 0.6s cubic-bezier(0.4, 0, 0.2, 1); removed for performance */
  }
  
  .message-copy-button.success:hover,
  .message-copy-button.success.hovered {
    /* Complex gradient simplified for performance */
    background: var(--accent-success-light);
    /* transform: scale(1.08) translateY(-2px); removed for performance */
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  }
  
  /* Enhanced Error State - Professional Error Treatment */
  .message-copy-button.error {
    /* Complex gradient simplified for performance */
    background: var(--accent-error);
    border-color: var(--accent-error);
    color: var(--text-primary);
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    /* Animation removed for performance */
  }
  
  .message-copy-button.error:hover,
  .message-copy-button.error.hovered {
    /* Complex gradient simplified for performance */
    background: var(--accent-error-hover);
    /* transform: scale(1.05) translateY(-1px); removed for performance */
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
  }
  
  /* Enhanced Professional Icon Container */
  .copy-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    line-height: 1;
    
    /* Enhanced Icon Treatment - simplified for performance */
    /* filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.2)); removed for performance */
    transition: opacity 0.2s ease;
    /* transform: translateZ(0); removed for performance */
  }
  
  /* Icon State Animations */
  .copy-icon.icon-idle {
    /* transform: scale(1); removed for performance */
  }
  
  .copy-icon.icon-loading {
    /* transform: scale(1.1); removed for performance */
    /* Animation removed for performance */
  }
  
  .copy-icon.icon-success {
    /* transform: scale(1.2); removed for performance */
    /* filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.6)); removed for performance */
    /* Animation removed for performance */
  }
  
  .copy-icon.icon-error {
    /* transform: scale(1.1); removed for performance */
    /* filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.6)); removed for performance */
    /* animation: icon-error-wobble 0.6s cubic-bezier(0.4, 0, 0.2, 1); removed for performance */
  }
  
  /* Seamless Message Integration */
  .message-bubble {
    position: relative;
    overflow: visible;
  }
  
  /* Professional Reveal on Hover */
  .message-bubble:hover .message-copy-button {
    opacity: 1;
    /* transform: scale(1.0); removed for performance */
  }
  
  /* Focus State for Accessibility */
  .message-copy-button:focus-visible {
    opacity: 1;
    /* transform: scale(1.0); removed for performance */
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
      /* transform: scale(1.0); removed for performance */
    }
    
    .message-bubble:hover .message-copy-button,
    .message-copy-button:focus {
      opacity: 1;
    }
  }
  
  /* Responsive Design - Mobile Enhancement */
  @media (max-width: 768px) {
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
  @media (min-width: 769px) and (max-width: 1024px) {
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
      /* backdrop-filter removed for performance */
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
      /* transform: none; removed for performance */
      animation: none;
    }
    
    .message-copy-button:hover,
    .message-copy-button.hovered,
    .message-copy-button:active {
      /* transform: none; removed for performance */
      animation: none;
    }
    
    .message-bubble:hover .message-copy-button {
      /* transform: none; removed for performance */
    }
    
    .copy-icon,
    .copy-icon.icon-loading,
    .copy-icon.icon-success,
    .copy-icon.icon-error {
      /* transform: none; removed for performance */
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
    /* will-change: opacity, transform, box-shadow; removed for performance */
    /* transform: translateZ(0); removed for performance */
    contain: layout style paint;
  }
  
  .copy-icon {
    /* will-change: transform, filter; removed for performance */
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
    outline: 2px solid var(--focus-ring);
    outline-offset: 2px;
  }
  
  .message-copy-button.success:focus-visible {
    outline-color: var(--accent-success);
  }
  
  .message-copy-button.error:focus-visible {
    outline-color: var(--accent-error);
  }
  
  /* Success Glow Effect */
  .message-copy-button.success-glow {
    /* Complex box-shadow simplified for performance */
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    /* Animation removed for performance */
  }
  
  /* All keyframe animations removed for performance */
`;
