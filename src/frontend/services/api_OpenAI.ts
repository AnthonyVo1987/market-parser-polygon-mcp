import { getAPIBaseURL, isDevelopment } from '../config/config.loader';
import {
  AIModelId,
  MODEL_API_ENDPOINTS,
  ModelListResponse,
  ModelSelectionResponse,
} from '../types/ai_models';
import { ApiError, ChatResponse } from '../types/chat_OpenAI';
import { logger } from '../utils/logger';

// Force use of Vite proxy instead of direct localhost connection
const API_BASE_URL = `${getAPIBaseURL()}/api`;

// Initialize API service logging
logger.info('🌐 API service initialized', {
  service: 'api_OpenAI',
  baseUrl: API_BASE_URL,
  environment: isDevelopment() ? 'development' : 'production',
});

export async function sendChatMessage(
  message: string,
  model?: AIModelId
): Promise<ChatResponse> {
  const requestId =
    Date.now().toString() + Math.random().toString(36).substr(2, 9);
  const startTime = performance.now();
  const endpoint = '/chat';

  logger.apiRequest('POST', endpoint, {
    messageLength: message.length,
    messagePreview: message.slice(0, 100) + (message.length > 100 ? '...' : ''),
    requestId,
    timestamp: new Date().toISOString(),
  });

  try {
    logger.debug('🌐 Sending fetch request', {
      service: 'api_OpenAI',
      endpoint,
      method: 'POST',
      requestId,
      hasBody: true,
    });

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message, model }),
    });

    const duration = performance.now() - startTime;

    logger.debug('📡 Fetch response received', {
      service: 'api_OpenAI',
      requestId,
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: `${duration.toFixed(2)}ms`,
      headers: {
        contentType: response.headers.get('content-type'),
        contentLength: response.headers.get('content-length'),
      },
    });

    if (!response.ok) {
      let errorData: ApiError;
      try {
        errorData = (await response.json()) as ApiError;
      } catch (parseError) {
        logger.error('❌ Failed to parse error response', {
          service: 'api_OpenAI',
          requestId,
          status: response.status,
          parseError:
            parseError instanceof Error
              ? parseError.message
              : 'Unknown parse error',
        });
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      logger.apiResponse('POST', endpoint, response.status, duration, {
        error: errorData.error,
        requestId,
      });

      throw new Error(errorData.error || 'Failed to send message');
    }

    let data: ChatResponse;
    try {
      data = (await response.json()) as ChatResponse;
    } catch (parseError) {
      logger.error('❌ Failed to parse success response', {
        service: 'api_OpenAI',
        requestId,
        status: response.status,
        parseError:
          parseError instanceof Error
            ? parseError.message
            : 'Unknown parse error',
      });
      throw new Error('Failed to parse server response');
    }

    logger.apiResponse('POST', endpoint, response.status, duration, {
      responseLength: data.response.length,
      success: data.success,
      requestId,
    });

    logger.info('✅ Chat message sent successfully', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      inputLength: message.length,
      outputLength: data.response.length,
      success: data.success,
    });

    return data;
  } catch (error) {
    const duration = performance.now() - startTime;

    if (error instanceof Error) {
      logger.error('💥 API request failed with error', {
        service: 'api_OpenAI',
        requestId,
        duration: `${duration.toFixed(2)}ms`,
        errorType: error.constructor.name,
        errorMessage: error.message,
        stack:
          error.stack?.slice(0, 300) +
          (error.stack && error.stack.length > 300 ? '...' : ''),
      });

      logger.apiResponse('POST', endpoint, 0, duration, {
        error: error.message,
        errorType: error.constructor.name,
        requestId,
      });

      throw error;
    }

    logger.error('💥 API request failed with unknown error', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      error: String(error),
    });

    throw new Error('Unknown error occurred');
  }
}

// ====== AI MODEL MANAGEMENT API FUNCTIONS ======

export async function getAvailableModels(): Promise<ModelListResponse> {
  const requestId =
    Date.now().toString() + Math.random().toString(36).substr(2, 9);
  const startTime = performance.now();
  const endpoint = `${API_BASE_URL}${MODEL_API_ENDPOINTS.LIST}`;

  logger.apiRequest('GET', endpoint, {
    requestId,
    timestamp: new Date().toISOString(),
  });

  try {
    logger.debug('🌐 Sending fetch request for models', {
      service: 'api_OpenAI',
      endpoint,
      method: 'GET',
      requestId,
    });

    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const duration = performance.now() - startTime;

    logger.debug('📡 Models fetch response received', {
      service: 'api_OpenAI',
      requestId,
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: `${duration.toFixed(2)}ms`,
    });

    if (!response.ok) {
      let errorData: ApiError;
      try {
        errorData = (await response.json()) as ApiError;
      } catch (parseError) {
        logger.error('❌ Failed to parse models error response', {
          service: 'api_OpenAI',
          requestId,
          status: response.status,
          parseError:
            parseError instanceof Error
              ? parseError.message
              : 'Unknown parse error',
        });
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      logger.apiResponse('GET', endpoint, response.status, duration, {
        error: errorData.error,
        requestId,
      });

      throw new Error(errorData.error || 'Failed to fetch models');
    }

    let data: ModelListResponse;
    try {
      data = (await response.json()) as ModelListResponse;
    } catch (parseError) {
      logger.error('❌ Failed to parse models success response', {
        service: 'api_OpenAI',
        requestId,
        status: response.status,
        parseError:
          parseError instanceof Error
            ? parseError.message
            : 'Unknown parse error',
      });
      throw new Error('Failed to parse models response');
    }

    logger.apiResponse('GET', endpoint, response.status, duration, {
      modelCount: data.total_count,
      currentModel: data.current_model,
      requestId,
    });

    logger.info('✅ Models fetched successfully', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      modelCount: data.total_count,
      currentModel: data.current_model,
    });

    return data;
  } catch (error) {
    const duration = performance.now() - startTime;

    if (error instanceof Error) {
      logger.error('💥 Models API request failed with error', {
        service: 'api_OpenAI',
        requestId,
        duration: `${duration.toFixed(2)}ms`,
        errorType: error.constructor.name,
        errorMessage: error.message,
      });

      logger.apiResponse('GET', endpoint, 0, duration, {
        error: error.message,
        errorType: error.constructor.name,
        requestId,
      });

      throw error;
    }

    logger.error('💥 Models API request failed with unknown error', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      error: String(error),
    });

    throw new Error('Unknown error occurred while fetching models');
  }
}

export async function selectModel(
  modelId: AIModelId
): Promise<ModelSelectionResponse> {
  const requestId =
    Date.now().toString() + Math.random().toString(36).substr(2, 9);
  const startTime = performance.now();
  const endpoint = `${API_BASE_URL}${MODEL_API_ENDPOINTS.SELECT}`;

  logger.apiRequest('POST', endpoint, {
    modelId,
    requestId,
    timestamp: new Date().toISOString(),
  });

  try {
    logger.debug('🌐 Sending fetch request for model selection', {
      service: 'api_OpenAI',
      endpoint,
      method: 'POST',
      requestId,
      modelId,
    });

    const response = await fetch(
      `${endpoint}?model_id=${encodeURIComponent(modelId)}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    const duration = performance.now() - startTime;

    logger.debug('📡 Model selection response received', {
      service: 'api_OpenAI',
      requestId,
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: `${duration.toFixed(2)}ms`,
    });

    if (!response.ok) {
      let errorData: ApiError;
      try {
        errorData = (await response.json()) as ApiError;
      } catch (parseError) {
        logger.error('❌ Failed to parse model selection error response', {
          service: 'api_OpenAI',
          requestId,
          status: response.status,
          parseError:
            parseError instanceof Error
              ? parseError.message
              : 'Unknown parse error',
        });
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      logger.apiResponse('POST', endpoint, response.status, duration, {
        error: errorData.error,
        requestId,
      });

      throw new Error(errorData.error || 'Failed to select model');
    }

    let data: ModelSelectionResponse;
    try {
      data = (await response.json()) as ModelSelectionResponse;
    } catch (parseError) {
      logger.error('❌ Failed to parse model selection success response', {
        service: 'api_OpenAI',
        requestId,
        status: response.status,
        parseError:
          parseError instanceof Error
            ? parseError.message
            : 'Unknown parse error',
      });
      throw new Error('Failed to parse model selection response');
    }

    logger.apiResponse('POST', endpoint, response.status, duration, {
      success: data.success,
      selectedModel: data.selected_model,
      previousModel: data.previous_model,
      requestId,
    });

    logger.info('✅ Model selected successfully', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      selectedModel: data.selected_model,
      previousModel: data.previous_model,
      success: data.success,
    });

    return data;
  } catch (error) {
    const duration = performance.now() - startTime;

    if (error instanceof Error) {
      logger.error('💥 Model selection API request failed with error', {
        service: 'api_OpenAI',
        requestId,
        duration: `${duration.toFixed(2)}ms`,
        errorType: error.constructor.name,
        errorMessage: error.message,
        modelId,
      });

      logger.apiResponse('POST', endpoint, 0, duration, {
        error: error.message,
        errorType: error.constructor.name,
        requestId,
      });

      throw error;
    }

    logger.error('💥 Model selection API request failed with unknown error', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      error: String(error),
      modelId,
    });

    throw new Error('Unknown error occurred while selecting model');
  }
}
