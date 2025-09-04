import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatInterface_OpenAI from '../ChatInterface_OpenAI'

// Mock the API service
vi.mock('../../services/api_OpenAI', () => ({
  sendChatMessage: vi.fn(),
}))

import { sendChatMessage } from '../../services/api_OpenAI'

const mockSendChatMessage = vi.mocked(sendChatMessage)

describe('ChatInterface_OpenAI', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Mock successful API response by default
    mockSendChatMessage.mockResolvedValue('AI response message')
  })

  afterEach(() => {
    vi.clearAllTimers()
  })

  describe('Initial State', () => {
    it('renders with correct initial elements', () => {
      render(<ChatInterface_OpenAI />)
      
      expect(screen.getByRole('heading', { name: /openai chat interface/i })).toBeInTheDocument()
      expect(screen.getByText(/start a conversation/i)).toBeInTheDocument()
      expect(screen.getByRole('textbox')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument()
    })

    it('shows empty state message when no messages', () => {
      render(<ChatInterface_OpenAI />)
      
      expect(screen.getByText(/start a conversation by typing a message below/i)).toBeInTheDocument()
    })

    it('does not show export buttons when no messages', () => {
      render(<ChatInterface_OpenAI />)
      
      expect(screen.queryByText(/export/i)).not.toBeInTheDocument()
    })
  })

  describe('Message Sending', () => {
    it('adds user message immediately when sent', async () => {
      const user = userEvent.setup()
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Hello AI')
      await user.keyboard('{Enter}')
      
      expect(screen.getByText('Hello AI')).toBeInTheDocument()
      expect(screen.queryByText(/start a conversation/i)).not.toBeInTheDocument()
    })

    it('shows loading indicator while waiting for response', async () => {
      const user = userEvent.setup()
      // Make API call hang to test loading state
      mockSendChatMessage.mockImplementation(() => new Promise(() => {}))
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      expect(screen.getByText('Test message')).toBeInTheDocument()
      expect(screen.getByRole('generic', { name: /loading/i }) || screen.getByTestId('loading-indicator')).toBeInTheDocument()
    })

    it('adds AI response after successful API call', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('AI response message')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Hello AI')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('AI response message')).toBeInTheDocument()
      })
      
      expect(mockSendChatMessage).toHaveBeenCalledWith('Hello AI')
    })

    it('disables input while loading', async () => {
      const user = userEvent.setup()
      // Make API call hang
      mockSendChatMessage.mockImplementation(() => new Promise(() => {}))
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      expect(screen.getByRole('textbox')).toBeDisabled()
      expect(screen.getByRole('button')).toBeDisabled()
    })
  })

  describe('Error Handling', () => {
    it('displays error message when API call fails', async () => {
      const user = userEvent.setup()
      const errorMessage = 'Network error occurred'
      mockSendChatMessage.mockRejectedValue(new Error(errorMessage))
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument()
      })
      
      // Should show error banner
      expect(screen.getByText(errorMessage)).toBeInTheDocument()
    })

    it('re-enables input after error', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockRejectedValue(new Error('API Error'))
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByRole('textbox')).not.toBeDisabled()
        expect(screen.getByRole('button')).not.toBeDisabled()
      })
    })

    it('handles non-Error exceptions', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockRejectedValue('String error')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('Error: Failed to send message')).toBeInTheDocument()
      })
    })
  })

  describe('Message Management', () => {
    it('generates unique IDs for messages', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('Response')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      
      // Send first message
      await user.type(input, 'First message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('Response')).toBeInTheDocument()
      })
      
      // Send second message
      await user.type(input, 'Second message')
      await user.keyboard('{Enter}')
      
      // Both messages should be present
      expect(screen.getByText('First message')).toBeInTheDocument()
      expect(screen.getByText('Second message')).toBeInTheDocument()
      expect(screen.getAllByText('Response')).toHaveLength(2)
    })

    it('maintains message order', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('AI says hello')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'User says hello')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('AI says hello')).toBeInTheDocument()
      })
      
      const messages = screen.getAllByText(/says hello/)
      expect(messages[0]).toHaveTextContent('User says hello')
      expect(messages[1]).toHaveTextContent('AI says hello')
    })

    it('preserves timestamps on messages', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('Response')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('Response')).toBeInTheDocument()
      })
      
      // Should have timestamps (format depends on locale)
      const timestamps = screen.getAllByText(/\d{1,2}:\d{2}:\d{2}/)
      expect(timestamps.length).toBeGreaterThan(0)
    })
  })

  describe('Export Functionality', () => {
    it('shows export buttons when messages exist', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('Response')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('Response')).toBeInTheDocument()
      })
      
      // Export buttons should now be visible
      expect(screen.getByTestId('export-buttons') || screen.getByText(/export/i)).toBeInTheDocument()
    })
  })

  describe('Recent Message Buttons', () => {
    it('shows recent message buttons', () => {
      render(<ChatInterface_OpenAI />)
      
      // Recent message buttons should be present (even with empty messages)
      expect(screen.getByTestId('recent-message-buttons') || screen.getAllByRole('button')).toBeTruthy()
    })
  })

  describe('Loading States', () => {
    it('shows typing indicator with animated dots', async () => {
      const user = userEvent.setup()
      // Make API call hang to keep loading state
      mockSendChatMessage.mockImplementation(() => new Promise(() => {}))
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      // Should show loading dots
      const loadingDots = document.querySelectorAll('.typing-dots span')
      expect(loadingDots).toHaveLength(3)
    })
  })

  describe('Accessibility', () => {
    it('has proper heading structure', () => {
      render(<ChatInterface_OpenAI />)
      
      const heading = screen.getByRole('heading', { level: 1 })
      expect(heading).toHaveTextContent('OpenAI Chat Interface')
    })

    it('provides accessible error messages', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockRejectedValue(new Error('Test error'))
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        const errorAlert = screen.getByRole('alert') || screen.getByText('Test error')
        expect(errorAlert).toBeInTheDocument()
      })
    })

    it('maintains focus management during interactions', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('Response')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      
      await user.click(input)
      expect(input).toHaveFocus()
      
      await user.type(input, 'Test message')
      await user.keyboard('{Enter}')
      
      // Input should maintain focus after sending
      expect(input).toHaveFocus()
    })
  })

  describe('Component Integration', () => {
    it('integrates properly with ChatInput component', async () => {
      const user = userEvent.setup()
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      const button = screen.getByRole('button', { name: /send/i })
      
      expect(input).toBeInTheDocument()
      expect(button).toBeInTheDocument()
      
      await user.type(input, 'Integration test')
      await user.click(button)
      
      expect(screen.getByText('Integration test')).toBeInTheDocument()
    })

    it('integrates properly with ChatMessage components', async () => {
      const user = userEvent.setup()
      mockSendChatMessage.mockResolvedValue('AI response')
      
      render(<ChatInterface_OpenAI />)
      
      const input = screen.getByRole('textbox')
      await user.type(input, 'User message')
      await user.keyboard('{Enter}')
      
      await waitFor(() => {
        expect(screen.getByText('AI response')).toBeInTheDocument()
      })
      
      // Both message types should render with their respective styles
      expect(screen.getByText('User message')).toBeInTheDocument()
      expect(screen.getByText('AI response')).toBeInTheDocument()
    })
  })
})