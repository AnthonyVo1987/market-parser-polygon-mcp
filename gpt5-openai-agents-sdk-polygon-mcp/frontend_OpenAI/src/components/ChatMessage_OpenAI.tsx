import { ComponentPropsWithoutRef } from 'react';
import Markdown from 'react-markdown';

import { Message } from '../types/chat_OpenAI';
import MessageCopyButton, { messageCopyButtonStyles } from './MessageCopyButton';

interface ChatMessage_OpenAIProps {
  message: Message;
}



// Custom components for markdown rendering
const markdownComponents = {
  p: ({ children, ...props }: ComponentPropsWithoutRef<'p'>) => (
    <p
      {...props}
      style={{
        marginBottom: '8px',
        lineHeight: '1.6',
      }}
    >
      {children}
    </p>
  ),
  h1: ({ children, ...props }: ComponentPropsWithoutRef<'h1'>) => (
    <h1
      {...props}
      style={{
        marginBottom: '12px',
        fontSize: '1.5em',
        fontWeight: '600',
        color: '#1a202c',
      }}
    >
      {children}
    </h1>
  ),
  h2: ({ children, ...props }: ComponentPropsWithoutRef<'h2'>) => (
    <h2
      {...props}
      style={{
        marginBottom: '10px',
        fontSize: '1.3em',
        fontWeight: '600',
        color: '#2d3748',
      }}
    >
      {children}
    </h2>
  ),
  h3: ({ children, ...props }: ComponentPropsWithoutRef<'h3'>) => (
    <h3
      {...props}
      style={{
        marginBottom: '8px',
        fontSize: '1.2em',
        fontWeight: '600',
        color: '#4a5568',
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
          backgroundColor: '#f7fafc',
          padding: '2px 4px',
          borderRadius: '3px',
          fontSize: '0.9em',
          fontFamily: 'monospace',
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
          backgroundColor: '#f7fafc',
          padding: '12px',
          borderRadius: '8px',
          overflowX: 'auto',
          maxWidth: '100%',
          marginBottom: '8px',
          whiteSpace: 'pre',
        }}
      >
        <code {...props}>{children}</code>
      </pre>
    );
  },
};

export default function ChatMessage_OpenAI({
  message,
}: ChatMessage_OpenAIProps) {
  const isUser = message.sender === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className={`message-bubble ${isUser ? 'user-bubble' : 'ai-bubble'}`}>
        <MessageCopyButton message={message} />
        <div className='message-content'>
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
        <div className='message-timestamp'>
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

// Enhanced inline styles for message components
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
    max-width: 85%; /* Mobile first approach */
    padding: 12px 16px;
    border-radius: 16px;
    position: relative;
    overflow-x: auto;
    overflow-y: visible;
    word-wrap: break-word;
    overflow-wrap: break-word;
    scrollbar-width: thin; /* Firefox */
  }
  
  /* Desktop/Tablet breakpoint */
  @media (min-width: 768px) {
    .message-bubble {
      max-width: 70%;
    }
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
    word-break: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
  }
  
  .message-timestamp {
    font-size: 0.75rem;
    opacity: 0.7;
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

  ${messageCopyButtonStyles}
`;
