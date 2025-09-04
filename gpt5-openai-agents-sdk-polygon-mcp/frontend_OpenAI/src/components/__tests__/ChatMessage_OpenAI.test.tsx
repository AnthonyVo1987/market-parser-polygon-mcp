import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatMessage_OpenAI from '../ChatMessage_OpenAI'
import { Message } from '../../types/chat_OpenAI'

const createMockMessage = (overrides: Partial<Message> = {}): Message => ({
  id: 'test-id',
  content: 'Test message content',
  sender: 'user',
  timestamp: new Date('2024-01-01T12:00:00Z'),
  ...overrides,
})

// Mock the copy functionality
Object.assign(navigator, {
  clipboard: {
    writeText: vi.fn(),
  },
})

describe('ChatMessage_OpenAI', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Rendering', () => {
    it('renders user message correctly', () => {
      const message = createMockMessage({ sender: 'user', content: 'Hello from user' })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByText('Hello from user')).toBeInTheDocument()
      expect(screen.getByText('12:00:00 PM')).toBeInTheDocument()
    })

    it('renders AI message correctly', () => {
      const message = createMockMessage({ sender: 'ai', content: 'Hello from AI' })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByText('Hello from AI')).toBeInTheDocument()
      expect(screen.getByText('12:00:00 PM')).toBeInTheDocument()
    })

    it('applies correct CSS classes for user messages', () => {
      const message = createMockMessage({ sender: 'user' })
      const { container } = render(<ChatMessage_OpenAI message={message} />)
      
      expect(container.querySelector('.user-message')).toBeInTheDocument()
      expect(container.querySelector('.user-bubble')).toBeInTheDocument()
    })

    it('applies correct CSS classes for AI messages', () => {
      const message = createMockMessage({ sender: 'ai' })
      const { container } = render(<ChatMessage_OpenAI message={message} />)
      
      expect(container.querySelector('.ai-message')).toBeInTheDocument()
      expect(container.querySelector('.ai-bubble')).toBeInTheDocument()
    })
  })

  describe('Message Content Rendering', () => {
    it('renders user messages as plain text', () => {
      const message = createMockMessage({ 
        sender: 'user', 
        content: '**Bold text** and *italic text*' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      // Should render as plain text, not as markdown
      expect(screen.getByText('**Bold text** and *italic text*')).toBeInTheDocument()
    })

    it('renders AI messages as markdown', () => {
      const message = createMockMessage({ 
        sender: 'ai', 
        content: '**Bold text** and *italic text*' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      // Should render as markdown
      expect(screen.getByText('Bold text')).toBeInTheDocument()
      expect(screen.getByText('italic text')).toBeInTheDocument()
    })

    it('handles markdown headings in AI messages', () => {
      const message = createMockMessage({ 
        sender: 'ai', 
        content: '# Heading 1\n## Heading 2\n### Heading 3' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Heading 1')
      expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Heading 2')
      expect(screen.getByRole('heading', { level: 3 })).toHaveTextContent('Heading 3')
    })

    it('handles markdown lists in AI messages', () => {
      const message = createMockMessage({ 
        sender: 'ai', 
        content: '- Item 1\n- Item 2\n- Item 3' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByRole('list')).toBeInTheDocument()
      expect(screen.getAllByRole('listitem')).toHaveLength(3)
    })

    it('handles code blocks in AI messages', () => {
      const message = createMockMessage({ 
        sender: 'ai', 
        content: '```javascript\nconst test = "hello";\n```' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByText('const test = "hello";')).toBeInTheDocument()
    })

    it('handles inline code in AI messages', () => {
      const message = createMockMessage({ 
        sender: 'ai', 
        content: 'Use the `console.log()` function for debugging.' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByText('console.log()')).toBeInTheDocument()
    })
  })

  describe('Copy Functionality', () => {
    it('shows copy button for messages', () => {
      const message = createMockMessage()
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByRole('button', { name: /copy/i })).toBeInTheDocument()
    })

    it('copies message content when copy button is clicked', async () => {
      const user = userEvent.setup()
      const message = createMockMessage({ content: 'Message to copy' })
      render(<ChatMessage_OpenAI message={message} />)
      
      const copyButton = screen.getByRole('button', { name: /copy/i })
      await user.click(copyButton)
      
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('Message to copy')
    })
  })

  describe('Timestamp Formatting', () => {
    it('formats timestamp correctly', () => {
      const message = createMockMessage({ 
        timestamp: new Date('2024-01-01T14:30:45Z') 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      // Should show formatted time
      expect(screen.getByText(/2:30:45 PM/)).toBeInTheDocument()
    })

    it('updates timestamp display for different times', () => {
      const message = createMockMessage({ 
        timestamp: new Date('2024-01-01T09:15:30Z') 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByText(/9:15:30 AM/)).toBeInTheDocument()
    })
  })

  describe('Accessibility', () => {
    it('has proper message structure for screen readers', () => {
      const message = createMockMessage({ 
        sender: 'ai', 
        content: 'Accessible message content' 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      // Message content should be accessible
      expect(screen.getByText('Accessible message content')).toBeInTheDocument()
      
      // Timestamp should be accessible
      expect(screen.getByText('12:00:00 PM')).toBeInTheDocument()
    })

    it('provides accessible copy button', () => {
      const message = createMockMessage()
      render(<ChatMessage_OpenAI message={message} />)
      
      const copyButton = screen.getByRole('button', { name: /copy/i })
      expect(copyButton).toBeInTheDocument()
      expect(copyButton).toHaveAttribute('type', 'button')
    })
  })

  describe('Long Content Handling', () => {
    it('handles very long messages without breaking layout', () => {
      const longContent = 'Very long message content '.repeat(100)
      const message = createMockMessage({ content: longContent })
      const { container } = render(<ChatMessage_OpenAI message={message} />)
      
      const messageElement = container.querySelector('.message-content')
      expect(messageElement).toHaveStyle({ wordBreak: 'break-word' })
      expect(screen.getByText(longContent)).toBeInTheDocument()
    })

    it('handles code blocks with horizontal scrolling', () => {
      const longCode = 'const veryLongVariableName = "this is a very long line of code that should trigger horizontal scrolling";'.repeat(3)
      const message = createMockMessage({ 
        sender: 'ai',
        content: `\`\`\`javascript\n${longCode}\n\`\`\`` 
      })
      render(<ChatMessage_OpenAI message={message} />)
      
      expect(screen.getByText(longCode)).toBeInTheDocument()
    })
  })

  describe('Message Bubble Layout', () => {
    it('positions user messages to the right', () => {
      const message = createMockMessage({ sender: 'user' })
      const { container } = render(<ChatMessage_OpenAI message={message} />)
      
      const messageContainer = container.querySelector('.message')
      expect(messageContainer).toHaveClass('user-message')
    })

    it('positions AI messages to the left', () => {
      const message = createMockMessage({ sender: 'ai' })
      const { container } = render(<ChatMessage_OpenAI message={message} />)
      
      const messageContainer = container.querySelector('.message')
      expect(messageContainer).toHaveClass('ai-message')
    })

    it('applies correct bubble styling', () => {
      const message = createMockMessage()
      const { container } = render(<ChatMessage_OpenAI message={message} />)
      
      const bubble = container.querySelector('.message-bubble')
      expect(bubble).toBeInTheDocument()
      expect(bubble).toHaveClass('user-bubble')
    })
  })
})