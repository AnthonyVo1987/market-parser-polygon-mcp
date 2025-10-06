import { ApiError, ChatResponse } from '../types/chat_OpenAI';

export async function sendChatMessage(
  message: string
): Promise<ChatResponse> {
  const endpoint = '/api/v1/chat/';

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      let errorData: ApiError;
      try {
        errorData = (await response.json()) as ApiError;
      } catch (parseError) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      throw new Error(errorData.error || 'Failed to send message');
    }

    let data: ChatResponse;
    try {
      data = (await response.json()) as ChatResponse;
    } catch (parseError) {
      throw new Error('Failed to parse server response');
    }

    // Add metadata to response
    const responseWithMetadata: ChatResponse = {
      ...data,
      metadata: {
        ...data.metadata,
        requestId:
          Date.now().toString() + Math.random().toString(36).substr(2, 9),
        timestamp: new Date().toISOString(),
      },
    };

    return responseWithMetadata;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }

    throw new Error('Unknown error occurred');
  }
}
