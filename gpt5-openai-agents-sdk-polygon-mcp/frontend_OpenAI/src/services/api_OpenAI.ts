import { ChatResponse, ApiError } from '../types/chat_OpenAI';

const API_BASE_URL = 'http://localhost:8001';

export async function sendChatMessage(message: string): Promise<string> {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const errorData = (await response.json()) as ApiError;
      throw new Error(errorData.error || 'Failed to send message');
    }

    const data = (await response.json()) as ChatResponse;
    return data.response;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred');
  }
}
