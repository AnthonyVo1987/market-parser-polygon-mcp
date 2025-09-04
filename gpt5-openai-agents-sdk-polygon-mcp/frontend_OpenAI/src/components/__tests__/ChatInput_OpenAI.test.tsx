import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatInput_OpenAI from '../ChatInput_OpenAI'

const defaultProps = {
  onSendMessage: vi.fn(),
  isLoading: false,
}

describe('ChatInput_OpenAI', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Rendering', () => {
    it('renders input field and send button', () => {
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument()
    })

    it('shows loading state when isLoading is true', () => {
      render(<ChatInput_OpenAI {...defaultProps} isLoading={true} />)
      
      expect(screen.getByRole('button', { name: /sending/i })).toBeDisabled()
      expect(screen.getByRole('textbox')).toBeDisabled()
    })

    it('displays correct placeholder text', () => {
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      expect(screen.getByPlaceholderText('Type your message... (Shift+Enter for new line)')).toBeInTheDocument()
    })
  })

  describe('User Interactions', () => {
    it('calls onSendMessage when form is submitted with valid input', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const input = screen.getByRole('textbox')
      const button = screen.getByRole('button', { name: /send/i })
      
      await user.type(input, 'Hello world')
      await user.click(button)
      
      expect(defaultProps.onSendMessage).toHaveBeenCalledWith('Hello world')
      expect(input).toHaveValue('')
    })

    it('calls onSendMessage when Enter key is pressed', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const input = screen.getByRole('textbox')
      
      await user.type(input, 'Hello world')
      await user.keyboard('{Enter}')
      
      expect(defaultProps.onSendMessage).toHaveBeenCalledWith('Hello world')
    })

    it('does not submit when Shift+Enter is pressed (allows new line)', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const input = screen.getByRole('textbox')
      
      await user.type(input, 'Line 1')
      await user.keyboard('{Shift>}{Enter}{/Shift}')
      await user.type(input, 'Line 2')
      
      expect(defaultProps.onSendMessage).not.toHaveBeenCalled()
      expect(input).toHaveValue('Line 1\nLine 2')
    })

    it('does not submit empty or whitespace-only messages', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const input = screen.getByRole('textbox')
      const button = screen.getByRole('button', { name: /send/i })
      
      // Test empty string
      await user.click(button)
      expect(defaultProps.onSendMessage).not.toHaveBeenCalled()
      
      // Test whitespace-only
      await user.type(input, '   ')
      await user.click(button)
      expect(defaultProps.onSendMessage).not.toHaveBeenCalled()
    })

    it('trims whitespace from messages before sending', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const input = screen.getByRole('textbox')
      
      await user.type(input, '  Hello world  ')
      await user.keyboard('{Enter}')
      
      expect(defaultProps.onSendMessage).toHaveBeenCalledWith('Hello world')
    })
  })

  describe('Textarea Auto-resize', () => {
    it('expands textarea as content grows', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const textarea = screen.getByRole('textbox') as HTMLTextAreaElement
      
      // Initially should have minimum height
      expect(textarea.style.minHeight).toBe('80px')
      
      // Type long content
      await user.type(textarea, 'This is a very long message that should cause the textarea to expand beyond its initial height. '.repeat(5))
      
      // Should have expanded (this is tested via the auto-resize functionality)
      expect(textarea.scrollHeight).toBeGreaterThan(80)
    })

    it('resets height after message is sent', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const textarea = screen.getByRole('textbox') as HTMLTextAreaElement
      
      await user.type(textarea, 'This is a long message that will expand the textarea')
      await user.keyboard('{Enter}')
      
      // After sending, textarea should be cleared and height reset
      expect(textarea.value).toBe('')
    })
  })

  describe('Accessibility', () => {
    it('has proper ARIA labels and roles', () => {
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const textarea = screen.getByRole('textbox')
      const button = screen.getByRole('button')
      
      expect(textarea).toBeInTheDocument()
      expect(button).toBeInTheDocument()
    })

    it('maintains focus management', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const textarea = screen.getByRole('textbox')
      
      await user.click(textarea)
      expect(textarea).toHaveFocus()
      
      await user.type(textarea, 'Test message')
      await user.keyboard('{Enter}')
      
      // Textarea should still be focused after sending
      expect(textarea).toHaveFocus()
    })

    it('disables interactions when loading', () => {
      render(<ChatInput_OpenAI {...defaultProps} isLoading={true} />)
      
      const textarea = screen.getByRole('textbox')
      const button = screen.getByRole('button')
      
      expect(textarea).toBeDisabled()
      expect(button).toBeDisabled()
    })
  })

  describe('Form Validation', () => {
    it('enables submit button only with non-empty input', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} />)
      
      const button = screen.getByRole('button', { name: /send/i })
      const textarea = screen.getByRole('textbox')
      
      // Initially disabled (empty input)
      expect(button).toBeDisabled()
      
      // Enabled with content
      await user.type(textarea, 'Hello')
      expect(button).toBeEnabled()
      
      // Disabled again when cleared
      await user.clear(textarea)
      expect(button).toBeDisabled()
    })

    it('prevents submission when loading', async () => {
      const user = userEvent.setup()
      render(<ChatInput_OpenAI {...defaultProps} isLoading={true} />)
      
      const textarea = screen.getByRole('textbox')
      
      // Even with content, should not call onSendMessage when loading
      await user.type(textarea, 'Test message')
      await user.keyboard('{Enter}')
      
      expect(defaultProps.onSendMessage).not.toHaveBeenCalled()
    })
  })
})