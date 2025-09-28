import {
  ComponentPropsWithoutRef,
  lazy,
  memo,
  Suspense,
  useEffect,
  useMemo,
  useState,
} from 'react';

// Lazy load react-markdown for better performance
const Markdown = lazy(() => import('react-markdown'));

import { Message } from '../types/chat_OpenAI';
import { formatMessage, MessageType } from '../utils/messageFormatting';
import MessageCopyButton, {
  messageCopyButtonStyles,
} from './MessageCopyButton';

interface ChatMessage_OpenAIProps {
  message: Message;
}

// Custom components for markdown rendering - moved inside component to use useMemo
const createMarkdownComponents = () => ({
  p: ({ children, ...props }: ComponentPropsWithoutRef<'p'>) => (
    <p
      {...props}
      style={{
        marginBottom: 'var(--space-2)',
        lineHeight: 'var(--leading-relaxed)',
        fontFamily: 'var(--font-inter)',
      }}
    >
      {children}
    </p>
  ),
  h1: ({ children, ...props }: ComponentPropsWithoutRef<'h1'>) => (
    <h1
      {...props}
      style={{
        marginBottom: 'var(--space-3)',
        fontSize: 'var(--text-xl)',
        fontWeight: 'var(--font-bold)',
        color: 'var(--neutral-50)',
        fontFamily: 'var(--font-inter)',
      }}
    >
      {children}
    </h1>
  ),
  h2: ({ children, ...props }: ComponentPropsWithoutRef<'h2'>) => (
    <h2
      {...props}
      style={{
        marginBottom: 'var(--space-2)',
        fontSize: 'var(--text-lg)',
        fontWeight: 'var(--font-semibold)',
        color: 'var(--neutral-100)',
        fontFamily: 'var(--font-inter)',
      }}
    >
      {children}
    </h2>
  ),
  h3: ({ children, ...props }: ComponentPropsWithoutRef<'h3'>) => (
    <h3
      {...props}
      style={{
        marginBottom: 'var(--space-2)',
        fontSize: 'var(--text-base)',
        fontWeight: 'var(--font-medium)',
        color: 'var(--neutral-200)',
        fontFamily: 'var(--font-inter)',
      }}
    >
      {children}
    </h3>
  ),
  ul: ({ children, ...props }: ComponentPropsWithoutRef<'ul'>) => (
    <ul {...props} style={{ marginBottom: '8px', paddingLeft: '20px' }}>
      {children}
    </ul>
  ),
  ol: ({ children, ...props }: ComponentPropsWithoutRef<'ol'>) => (
    <ol {...props} style={{ marginBottom: '8px', paddingLeft: '20px' }}>
      {children}
    </ol>
  ),
  li: ({ children, ...props }: ComponentPropsWithoutRef<'li'>) => (
    <li
      {...props}
      style={{
        marginBottom: '4px',
      }}
    >
      {children}
    </li>
  ),
  strong: ({ children, ...props }: ComponentPropsWithoutRef<'strong'>) => (
    <strong
      {...props}
      style={{
        fontWeight: '600',
      }}
    >
      {children}
    </strong>
  ),
  em: ({ children, ...props }: ComponentPropsWithoutRef<'em'>) => (
    <em {...props} style={{ fontStyle: 'italic' }}>
      {children}
    </em>
  ),
  blockquote: ({
    children,
    ...props
  }: ComponentPropsWithoutRef<'blockquote'>) => (
    <blockquote
      {...props}
      style={{
        background: '#f8fafc',
        padding: '12px',
        borderRadius: '8px',
        margin: '8px 0',
        borderLeft: '4px solid #e2e8f0',
        fontStyle: 'italic',
      }}
    >
      {children}
    </blockquote>
  ),
  code: ({
    children,
    className,
    ...props
  }: ComponentPropsWithoutRef<'code'> & { className?: string }) => {
    const isInline = !className;
    return isInline ? (
      <code
        {...props}
        style={{
          backgroundColor: 'var(--glass-surface-light)',
          /* backdrop-filter removed for performance */
          border: 'var(--glass-border-highlight)',
          padding: 'var(--space-1) var(--space-2)',
          borderRadius: 'var(--radius-md)',
          fontSize: 'var(--text-sm)',
          fontFamily: 'var(--font-mono)',
          color: 'var(--primary-300)',
          wordBreak: 'break-word',
          overflowWrap: 'break-word',
        }}
      >
        {children}
      </code>
    ) : (
      <pre
        className='code-block'
        style={{
          backgroundColor: 'var(--glass-surface-dark)',
          /* backdrop-filter removed for performance */
          border: 'var(--glass-border-highlight)',
          padding: 'var(--space-3)',
          borderRadius: 'var(--radius-lg)',
          overflowX: 'auto',
          maxWidth: '100%',
          marginBottom: 'var(--space-2)',
          whiteSpace: 'pre',
          color: 'var(--neutral-100)',
          fontFamily: 'var(--font-mono)',
        }}
      >
        <code {...props}>{children}</code>
      </pre>
    );
  },
});

const ChatMessage_OpenAI = memo(
  function ChatMessage_OpenAI({ message }: ChatMessage_OpenAIProps) {
    const isUser = message.sender === 'user';
    const [isVisible, setIsVisible] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);
    const [showAbsoluteTime, setShowAbsoluteTime] = useState(false);

    // Enhanced message formatting
    const formattedMessage = useMemo(() => {
      const messageType: MessageType = message.metadata?.isError
        ? 'error'
        : message.sender === 'user'
          ? 'user'
          : 'ai';

      return formatMessage({
        type: messageType,
        content: message.content,
        timestamp: message.timestamp,
        metadata: message.metadata,
      });
    }, [message.content, message.timestamp, message.metadata, message.sender]);

    // Memoize markdown components configuration for performance
    const markdownComponents = useMemo(() => createMarkdownComponents(), []);

    // Memoize expensive message processing computations
    // const messageMetadata = useMemo(
    //   () => ({
    //     hasMetadata: !!message.metadata,
    //     isError: message.metadata?.isError,
    //     formattedTime: message.timestamp.toLocaleTimeString(),
    //   }),
    //   [message.metadata, message.timestamp]
    // );

    // Animation removed for performance - show immediately
    useEffect(() => {
      setIsVisible(true);
      setIsLoaded(true);
    }, []);

    return (
      <div
        className={`${formattedMessage.cssClass} ${
          isVisible ? 'message-visible' : 'message-hidden'
        } ${isLoaded ? 'message-loaded' : 'message-loading'}`}
        role='article'
        aria-label={formattedMessage.ariaLabel}
      >
        <div
          className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'} ${
            formattedMessage.isError ? 'message-bubble--error' : ''
          }`}
        >
          <MessageCopyButton message={message} />
          <div className='message-content'>
            {isUser ? (
              // For user messages, display as plain text
              formattedMessage.formattedContent
            ) : (
              // For AI messages, render as markdown with enhanced formatting
              <Suspense
                fallback={
                  <div className='markdown-loading'>Loading content...</div>
                }
              >
                <Markdown components={markdownComponents}>
                  {formattedMessage.formattedContent}
                </Markdown>
              </Suspense>
            )}
          </div>
          <div
            className='message-timestamp'
            onMouseEnter={() => setShowAbsoluteTime(true)}
            onMouseLeave={() => setShowAbsoluteTime(false)}
            title={formattedMessage.absoluteTime}
            aria-label={`Message timestamp: ${formattedMessage.absoluteTime}`}
          >
            {showAbsoluteTime
              ? formattedMessage.absoluteTime
              : formattedMessage.relativeTime}
          </div>

          {/* Footer Data for AI Messages */}
          {!isUser && message.metadata && (
            <div className='message-footer' data-testid='message-footer'>
              <div className='footer-metrics'>
                {message.metadata.processingTime && (
                  <span className='footer-metric'>
                    Response Time: {message.metadata.processingTime.toFixed(3)}s
                  </span>
                )}
                {message.metadata.model && (
                  <span className='footer-metric'>
                    Model: {message.metadata.model}
                  </span>
                )}
                {message.metadata.tokenCount && (
                  <span className='footer-metric'>
                    Tokens: {message.metadata.tokenCount.toLocaleString()}
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Custom comparison function for memo
    const prevMessage = prevProps.message;
    const nextMessage = nextProps.message;

    // Check if message content, timestamp, or metadata changed
    return (
      prevMessage.id === nextMessage.id &&
      prevMessage.content === nextMessage.content &&
      prevMessage.sender === nextMessage.sender &&
      prevMessage.timestamp.getTime() === nextMessage.timestamp.getTime() &&
      JSON.stringify(prevMessage.metadata) ===
        JSON.stringify(nextMessage.metadata)
    );
  }
);

ChatMessage_OpenAI.displayName = 'ChatMessage_OpenAI';

export default ChatMessage_OpenAI;

// Professional fintech glassmorphic message styling
export const messageStyles = `
  .message {
    display: flex;
    margin-bottom: var(--space-4);
    position: relative;
  }
  
  .user-message {
    justify-content: flex-end;
  }
  
  .ai-message {
    justify-content: flex-start;
  }
  
  .message-bubble {
    max-width: 85%; /* Mobile first approach */
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-2xl);
    position: relative;
    overflow-x: auto;
    overflow-y: visible;
    word-wrap: break-word;
    overflow-wrap: break-word;
    scrollbar-width: thin; /* Firefox */
    /* backdrop-filter removed for performance */
    border: var(--glass-border-highlight);
  }
  
  /* Desktop/Tablet breakpoint */
  @media (min-width: 769px) {
    .message-bubble {
      max-width: 70%;
    }
  }
  
  .user-bubble {
    /* linear-gradient removed for performance */
    background: var(--primary-600);
    color: var(--neutral-50);
    border-color: var(--primary-500);
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.2);
  }
  
  .ai-bubble {
    background: var(--glass-surface-light);
    color: var(--neutral-100);
    border-color: var(--neutral-600);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .message-content {
    margin-bottom: var(--space-1);
    line-height: var(--leading-relaxed);
    white-space: pre-wrap;
    word-break: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    font-family: var(--font-inter);
  }
  
  .message-timestamp {
    font-size: var(--text-xs);
    opacity: 0.8;
    font-family: var(--font-mono);
    color: var(--neutral-300);
  }
  
  .user-bubble .message-timestamp {
    color: var(--neutral-200);
  }
  
  /* Message Footer Styles */
  .message-footer {
    margin-top: var(--space-2);
    padding-top: var(--space-2);
    border-top: 1px solid var(--glass-border-subtle);
  }
  
  .footer-metrics {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 12px;
    color: #94a3b8;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin-top: 8px;
  }
  
  .footer-metric {
    display: block;
    padding: 4px 0;
    font-weight: 500;
    line-height: 1.4;
    color: #cbd5e1;
  }
  
  .ai-bubble .footer-metric {
    background: var(--glass-surface-medium);
    color: var(--neutral-300);
  }
  
  .user-bubble .footer-metric {
    background: rgba(255, 255, 255, 0.1);
    color: var(--neutral-200);
  }
  



  /* Enhanced key takeaways styling */
  .key-takeaways {
    background: #f8fafc !important;
    padding: 12px !important;
    border-radius: 8px !important;
    margin: 8px 0 !important;
    border-left: 4px solid #e2e8f0 !important;
  }

  /* Enhanced typography for better readability */
  .message-content h1,
  .message-content h2,
  .message-content h3 {
    margin-top: 16px;
    margin-bottom: 8px;
  }

  .message-content h1:first-child,
  .message-content h2:first-child,
  .message-content h3:first-child {
    margin-top: 0;
  }

  .message-content ul,
  .message-content ol {
    margin: 8px 0;
    padding-left: 20px;
  }

  .message-content li {
    margin-bottom: 4px;
  }

  /* Emoji and emoji support */
  .message-content {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  /* Smart scrollbar management */
  .message-bubble:not(:hover) {
    scrollbar-width: none; /* Firefox */
  }

  .message-bubble:not(:hover)::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
  }

  .message-bubble:hover,
  .message-bubble:focus-within {
    scrollbar-width: thin;
  }

  .message-bubble:hover::-webkit-scrollbar {
    display: block;
    width: 8px;
    height: 8px;
  }

  .message-bubble:hover::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
  }

  /* Code block enhanced styling */
  .code-block {
    scrollbar-width: thin; /* Firefox */
  }

  .code-block::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  .code-block::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
  }

  .code-block::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }

  /* Touch device optimization - always show scrollbars */
  @media (hover: none) {
    .message-bubble {
      scrollbar-width: thin;
    }
    
    .message-bubble::-webkit-scrollbar {
      display: block;
      width: 8px;
      height: 8px;
    }
    
    .message-bubble::-webkit-scrollbar-thumb {
      background: rgba(0, 0, 0, 0.3);
      border-radius: 4px;
    }
    
    .message-bubble::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.1);
      border-radius: 4px;
    }
  }

  /* Markdown loading state styling */
  .markdown-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    color: #666;
    font-size: 0.9em;
    font-style: italic;
    min-height: 24px;
  }

  .ai-bubble .markdown-loading {
    color: #666;
  }

  .user-bubble .markdown-loading {
    color: rgba(255, 255, 255, 0.8);
  }
  
  /* Loading state - animation removed for performance */
  .markdown-loading {
    /* Transition removed for performance */
  }
  
  .markdown-loading::after {
    content: 'Loading...';
    display: inline-block;
    margin-left: 8px;
    vertical-align: middle;
    font-size: 12px;
    /* Spinner animation replaced with static icon */
  }
  
  /* Performance optimizations - GPU hints removed for performance */
  .message-bubble {
    /* GPU acceleration removed for performance */
  }
  
  /* High DPI display optimization */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
    .message-bubble {
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
  }
  
  /* Reduced motion support - ALL ANIMATIONS ALREADY REMOVED FOR PERFORMANCE */
  @media (prefers-reduced-motion: reduce) {
    /* All animations already removed */
  }

  ${messageCopyButtonStyles}
`;
