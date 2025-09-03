import { Message } from '../types/chat_OpenAI';
import Markdown from 'react-markdown';
import { ComponentPropsWithoutRef } from 'react';

interface ChatMessage_OpenAIProps {
  message: Message;
}

// Sentiment analysis keywords - aligned with backend CLI keywords for consistency
const BULLISH_KEYWORDS = [
  'bullish', 'buy', 'growth', 'profit', 'gain', 'up', 'positive', 'strong', 'upward', 'rise', 'increase',
  'rising', 'bullish signals', 'outperform', 'buy signal', 'momentum', 'rally',
  '📈', 'BULLISH', 'BUY', 'GROWTH', 'PROFIT', 'GAIN', 'POSITIVE', 'UP', 'STRONG', 'RISING', 'RALLY'
];

const BEARISH_KEYWORDS = [
  'bearish', 'sell', 'decline', 'loss', 'down', 'negative', 'weak', 'downward', 'fall', 'decrease',
  'falling', 'bearish signals', 'underperform', 'sell signal', 'correction', 'crash',
  '📉', 'BEARISH', 'SELL', 'DECLINE', 'LOSS', 'NEGATIVE', 'DOWN', 'WEAK', 'FALLING', 'CRASH'
];

// Function to detect sentiment in text
const detectSentiment = (text: string): 'bullish' | 'bearish' | 'neutral' => {
  const textLower = text.toLowerCase();
  const hasBullish = BULLISH_KEYWORDS.some(keyword => textLower.includes(keyword.toLowerCase()));
  const hasBearish = BEARISH_KEYWORDS.some(keyword => textLower.includes(keyword.toLowerCase()));
  
  if (hasBullish && !hasBearish) return 'bullish';
  if (hasBearish && !hasBullish) return 'bearish';
  return 'neutral';
};

// Custom components for markdown rendering with sentiment analysis
const markdownComponents = {
  p: ({ children, ...props }: ComponentPropsWithoutRef<'p'>) => {
    // Apply sentiment styling to paragraph content
    const textContent = typeof children === 'string' ? children : String(children);
    const sentiment = detectSentiment(textContent);
    
    return (
      <p {...props} style={{ 
        marginBottom: '8px', 
        lineHeight: '1.6',
        color: sentiment === 'bullish' ? '#10b981' : sentiment === 'bearish' ? '#ef4444' : 'inherit'
      }}>
        {children}
      </p>
    );
  },
  h1: ({ children, ...props }: ComponentPropsWithoutRef<'h1'>) => (
    <h1 {...props} style={{ marginBottom: '12px', fontSize: '1.5em', fontWeight: '600', color: '#1a202c' }}>
      {children}
    </h1>
  ),
  h2: ({ children, ...props }: ComponentPropsWithoutRef<'h2'>) => (
    <h2 {...props} style={{ marginBottom: '10px', fontSize: '1.3em', fontWeight: '600', color: '#2d3748' }}>
      {children}
    </h2>
  ),
  h3: ({ children, ...props }: ComponentPropsWithoutRef<'h3'>) => (
    <h3 {...props} style={{ marginBottom: '8px', fontSize: '1.2em', fontWeight: '600', color: '#4a5568' }}>
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
  li: ({ children, ...props }: ComponentPropsWithoutRef<'li'>) => {
    // Apply sentiment styling to list items
    const textContent = typeof children === 'string' ? children : String(children);
    const sentiment = detectSentiment(textContent);
    
    return (
      <li {...props} style={{ 
        marginBottom: '4px',
        color: sentiment === 'bullish' ? '#10b981' : sentiment === 'bearish' ? '#ef4444' : 'inherit',
        fontWeight: sentiment !== 'neutral' ? '500' : 'normal'
      }}>
        {children}
      </li>
    );
  },
  strong: ({ children, ...props }: ComponentPropsWithoutRef<'strong'>) => {
    // Apply sentiment styling to bold text
    const textContent = typeof children === 'string' ? children : String(children);
    const sentiment = detectSentiment(textContent);
    
    return (
      <strong {...props} style={{ 
        fontWeight: '600',
        color: sentiment === 'bullish' ? '#10b981' : sentiment === 'bearish' ? '#ef4444' : 'inherit'
      }}>
        {children}
      </strong>
    );
  },
  em: ({ children, ...props }: ComponentPropsWithoutRef<'em'>) => (
    <em {...props} style={{ fontStyle: 'italic' }}>
      {children}
    </em>
  ),
  blockquote: ({ children, ...props }: ComponentPropsWithoutRef<'blockquote'>) => (
    <blockquote {...props} style={{
      background: '#f8fafc',
      padding: '12px',
      borderRadius: '8px',
      margin: '8px 0',
      borderLeft: '4px solid #e2e8f0',
      fontStyle: 'italic'
    }}>
      {children}
    </blockquote>
  ),
  code: ({ children, className, ...props }: ComponentPropsWithoutRef<'code'> & { className?: string }) => {
    const isInline = !className;
    return isInline ? (
      <code {...props} style={{ 
        backgroundColor: '#f7fafc', 
        padding: '2px 4px', 
        borderRadius: '3px', 
        fontSize: '0.9em',
        fontFamily: 'monospace'
      }}>
        {children}
      </code>
    ) : (
      <pre style={{
        backgroundColor: '#f7fafc',
        padding: '12px',
        borderRadius: '8px',
        overflow: 'auto',
        marginBottom: '8px'
      }}>
        <code {...props}>{children}</code>
      </pre>
    );
  }
};

export default function ChatMessage_OpenAI({ message }: ChatMessage_OpenAIProps) {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`}>
        <div className="message-content">
          {isUser ? (
            // For user messages, display as plain text
            message.content
          ) : (
            // For AI messages, render as markdown with enhanced formatting
            <Markdown components={markdownComponents}>
              {message.content}
            </Markdown>
          )}
        </div>
        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

// Enhanced inline styles with sentiment color classes
export const messageStyles = `
  .message {
    display: flex;
    margin-bottom: 16px;
  }
  
  .user-message {
    justify-content: flex-end;
  }
  
  .ai-message {
    justify-content: flex-start;
  }
  
  .message-bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 16px;
    position: relative;
  }
  
  .user-bubble {
    background-color: #007bff;
    color: white;
  }
  
  .ai-bubble {
    background-color: #f1f1f1;
    color: #333;
  }
  
  .message-content {
    margin-bottom: 4px;
    line-height: 1.6;
    white-space: pre-wrap;
  }
  
  .message-timestamp {
    font-size: 0.75rem;
    opacity: 0.7;
  }

  /* Sentiment-based color classes */
  .bullish-text {
    color: #10b981 !important;
    font-weight: 500;
  }
  
  .bearish-text {
    color: #ef4444 !important;
    font-weight: 500;
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
`;