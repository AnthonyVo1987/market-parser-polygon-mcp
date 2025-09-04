import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { sendChatMessage } from '../api_OpenAI'

// Mock fetch globally
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('api_OpenAI', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('sendChatMessage', () => {
    it('sends POST request with correct parameters', async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({
          response: 'AI response message',
          success: true,
        }),
      }
      mockFetch.mockResolvedValue(mockResponse)

      const result = await sendChatMessage('Hello AI')

      expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'Hello AI' }),
      })
      expect(result).toBe('AI response message')
    })

    it('returns response content on successful API call', async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({
          response: 'Test AI response',
          success: true,
        }),
      }
      mockFetch.mockResolvedValue(mockResponse)

      const result = await sendChatMessage('Test message')

      expect(result).toBe('Test AI response')
    })

    it('throws error when response is not ok with error message', async () => {
      const mockResponse = {
        ok: false,
        json: vi.fn().mockResolvedValue({
          error: 'Server error occurred',
        }),
      }
      mockFetch.mockResolvedValue(mockResponse)

      await expect(sendChatMessage('Test message')).rejects.toThrow('Server error occurred')
    })

    it('throws default error message when response is not ok without error', async () => {
      const mockResponse = {
        ok: false,
        json: vi.fn().mockResolvedValue({}),
      }
      mockFetch.mockResolvedValue(mockResponse)

      await expect(sendChatMessage('Test message')).rejects.toThrow('Failed to send message')
    })

    it('handles network errors', async () => {
      const networkError = new Error('Network connection failed')
      mockFetch.mockRejectedValue(networkError)

      await expect(sendChatMessage('Test message')).rejects.toThrow('Network connection failed')
    })

    it('handles non-Error exceptions', async () => {
      mockFetch.mockRejectedValue('String error')

      await expect(sendChatMessage('Test message')).rejects.toThrow('Unknown error occurred')
    })

    it('handles malformed JSON response on error', async () => {
      const mockResponse = {
        ok: false,
        json: vi.fn().mockRejectedValue(new Error('Invalid JSON')),
      }
      mockFetch.mockResolvedValue(mockResponse)

      await expect(sendChatMessage('Test message')).rejects.toThrow('Invalid JSON')
    })

    it('handles malformed JSON response on success', async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockRejectedValue(new Error('Invalid JSON')),
      }
      mockFetch.mockResolvedValue(mockResponse)

      await expect(sendChatMessage('Test message')).rejects.toThrow('Invalid JSON')
    })

    it('makes request to correct API endpoint', async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({
          response: 'Response',
          success: true,
        }),
      }
      mockFetch.mockResolvedValue(mockResponse)

      await sendChatMessage('Test')

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:8000/chat',
        expect.objectContaining({
          method: 'POST',
        })
      )
    })

    it('sends correct Content-Type header', async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({
          response: 'Response',
          success: true,
        }),
      }
      mockFetch.mockResolvedValue(mockResponse)

      await sendChatMessage('Test')

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: {
            'Content-Type': 'application/json',
          },
        })
      )
    })

    it('sends message in correct JSON format', async () => {
      const mockResponse = {
        ok: true,
        json: vi.fn().mockResolvedValue({
          response: 'Response',
          success: true,
        }),
      }
      mockFetch.mockResolvedValue(mockResponse)

      const testMessage = 'Hello, this is a test message!'
      await sendChatMessage(testMessage)

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          body: JSON.stringify({ message: testMessage }),
        })
      )
    })

    describe('Edge Cases', () => {
      it('handles empty message', async () => {
        const mockResponse = {
          ok: true,
          json: vi.fn().mockResolvedValue({
            response: 'Empty message received',
            success: true,
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        const result = await sendChatMessage('')

        expect(mockFetch).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({
            body: JSON.stringify({ message: '' }),
          })
        )
        expect(result).toBe('Empty message received')
      })

      it('handles very long messages', async () => {
        const longMessage = 'Very long message '.repeat(1000)
        const mockResponse = {
          ok: true,
          json: vi.fn().mockResolvedValue({
            response: 'Long message processed',
            success: true,
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        const result = await sendChatMessage(longMessage)

        expect(result).toBe('Long message processed')
        expect(mockFetch).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({
            body: JSON.stringify({ message: longMessage }),
          })
        )
      })

      it('handles special characters in message', async () => {
        const specialMessage = 'Hello 👋 with émojis and spëcial chars: <>&"\'`'
        const mockResponse = {
          ok: true,
          json: vi.fn().mockResolvedValue({
            response: 'Special characters handled',
            success: true,
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        const result = await sendChatMessage(specialMessage)

        expect(result).toBe('Special characters handled')
        expect(mockFetch).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({
            body: JSON.stringify({ message: specialMessage }),
          })
        )
      })
    })

    describe('Response Validation', () => {
      it('extracts response field from successful API response', async () => {
        const mockResponse = {
          ok: true,
          json: vi.fn().mockResolvedValue({
            response: 'Expected response content',
            success: true,
            metadata: { timestamp: Date.now() },
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        const result = await sendChatMessage('Test')

        expect(result).toBe('Expected response content')
      })

      it('handles response with missing success field', async () => {
        const mockResponse = {
          ok: true,
          json: vi.fn().mockResolvedValue({
            response: 'Response without success field',
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        const result = await sendChatMessage('Test')

        expect(result).toBe('Response without success field')
      })
    })

    describe('Error Response Handling', () => {
      it('prioritizes error field in error response', async () => {
        const mockResponse = {
          ok: false,
          json: vi.fn().mockResolvedValue({
            error: 'Specific API error message',
            message: 'Generic message',
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        await expect(sendChatMessage('Test')).rejects.toThrow('Specific API error message')
      })

      it('handles error response without error field', async () => {
        const mockResponse = {
          ok: false,
          json: vi.fn().mockResolvedValue({
            message: 'Some other field',
          }),
        }
        mockFetch.mockResolvedValue(mockResponse)

        await expect(sendChatMessage('Test')).rejects.toThrow('Failed to send message')
      })
    })
  })
})