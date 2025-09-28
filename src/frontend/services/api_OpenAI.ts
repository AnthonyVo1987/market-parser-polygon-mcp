import { getAPIBaseURL } from '../config/config.loader';
import {
  AIModelId,
  MODEL_API_ENDPOINTS,
  ModelListResponse,
  ModelSelectionResponse,
} from '../types/ai_models';
import { ApiError, ChatResponse } from '../types/chat_OpenAI';

// Force use of Vite proxy instead of direct localhost connection
const API_BASE_URL = `${getAPIBaseURL()}/api`;

export async function sendChatMessage(
  message: string,
  model?: AIModelId
): Promise<ChatResponse> {
  const endpoint = '/api/v1/chat/';

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, model }),
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

export async function fetchModels(): Promise<ModelListResponse> {
  const endpoint = `${API_BASE_URL}${MODEL_API_ENDPOINTS.LIST}`;

  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      let errorData: ApiError;
      try {
        errorData = (await response.json()) as ApiError;
      } catch (parseError) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      throw new Error(errorData.error || 'Failed to fetch models');
    }

    let data: ModelListResponse;
    try {
      data = (await response.json()) as ModelListResponse;
    } catch (parseError) {
      throw new Error('Failed to parse models response');
    }

    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }

    throw new Error('Unknown error occurred');
  }
}

export async function selectModel(
  modelId: AIModelId
): Promise<ModelSelectionResponse> {
  const endpoint = `${API_BASE_URL}${MODEL_API_ENDPOINTS.SELECT}`;

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ model_id: modelId }),
    });

    if (!response.ok) {
      let errorData: ApiError;
      try {
        errorData = (await response.json()) as ApiError;
      } catch (parseError) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      throw new Error(errorData.error || 'Failed to select model');
    }

    let data: ModelSelectionResponse;
    try {
      data = (await response.json()) as ModelSelectionResponse;
    } catch (parseError) {
      throw new Error('Failed to parse model selection response');
    }

    return data;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }

    throw new Error('Unknown error occurred');
  }
}
