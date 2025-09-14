import { ChatResponse, ApiError } from '../types/chat_OpenAI';
import { logger } from '../utils/logger';

const API_BASE_URL = (import.meta.env.VITE_API_URL as string) || '/api';

// Initialize API service logging
logger.info('🌐 API service initialized', {
  service: 'api_OpenAI',
  baseUrl: API_BASE_URL,
  environment: import.meta.env.MODE
});

export async function sendChatMessage(message: string): Promise<string> {
  const requestId = Date.now().toString() + Math.random().toString(36).substr(2, 9);
  const startTime = performance.now();
  const endpoint = `${API_BASE_URL}/chat`;
  
  logger.apiRequest('POST', endpoint, {
    messageLength: message.length,
    messagePreview: message.slice(0, 100) + (message.length > 100 ? '...' : ''),
    requestId,
    timestamp: new Date().toISOString()
  });
  
  try {
    logger.debug('🌐 Sending fetch request', {
      service: 'api_OpenAI',
      endpoint,
      method: 'POST',
      requestId,
      hasBody: true
    });
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
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
        contentLength: response.headers.get('content-length')
      }
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
          parseError: parseError instanceof Error ? parseError.message : 'Unknown parse error'
        });
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      logger.apiResponse('POST', endpoint, response.status, duration, {
        error: errorData.error,
        requestId
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
        parseError: parseError instanceof Error ? parseError.message : 'Unknown parse error'
      });
      throw new Error('Failed to parse server response');
    }
    
    logger.apiResponse('POST', endpoint, response.status, duration, {
      responseLength: data.response.length,
      success: data.success,
      requestId
    });
    
    logger.info('✅ Chat message sent successfully', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      inputLength: message.length,
      outputLength: data.response.length,
      success: data.success
    });
    
    return data.response;
    
  } catch (error) {
    const duration = performance.now() - startTime;
    
    if (error instanceof Error) {
      logger.error('💥 API request failed with error', {
        service: 'api_OpenAI',
        requestId,
        duration: `${duration.toFixed(2)}ms`,
        errorType: error.constructor.name,
        errorMessage: error.message,
        stack: error.stack?.slice(0, 300) + (error.stack && error.stack.length > 300 ? '...' : '')
      });
      
      logger.apiResponse('POST', endpoint, 0, duration, {
        error: error.message,
        errorType: error.constructor.name,
        requestId
      });
      
      throw error;
    }
    
    logger.error('💥 API request failed with unknown error', {
      service: 'api_OpenAI',
      requestId,
      duration: `${duration.toFixed(2)}ms`,
      error: String(error)
    });
    
    throw new Error('Unknown error occurred');
  }
}
