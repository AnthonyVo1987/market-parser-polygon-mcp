/**
 * AI Model Selection Types
 *
 * TypeScript interfaces and enums for AI model management in the frontend.
 * These types correspond to the backend API models for model selection.
 */

// Enum for model IDs matching backend
export enum AIModelId {
  GPT_5_NANO = 'gpt-5-nano',
  GPT_5_MINI = 'gpt-5-mini',
}

// Strict interface definitions
export interface AIModel {
  readonly id: AIModelId;
  readonly name: string;
  readonly description?: string;
  readonly isDefault: boolean;
  readonly costPer1kTokens?: number;
  readonly maxTokens?: number;
}

export interface ModelListResponse {
  readonly models: readonly AIModel[];
  readonly current_model: AIModelId;
  readonly total_count: number;
  readonly timestamp: string;
}

export interface ModelSelectionRequest {
  readonly modelId: AIModelId;
}

export interface ModelSelectionResponse {
  readonly success: boolean;
  readonly message: string;
  readonly selected_model: AIModelId;
  readonly previous_model?: AIModelId;
  readonly timestamp: string;
}

// Type guards for runtime validation
export function isValidAIModel(value: unknown): value is AIModel {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    'isDefault' in value &&
    Object.values(AIModelId).includes((value as AIModel).id)
  );
}

export function isValidModelListResponse(
  value: unknown
): value is ModelListResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'models' in value &&
    'currentModel' in value &&
    Array.isArray((value as unknown as ModelListResponse).models) &&
    (value as unknown as ModelListResponse).models.every(isValidAIModel)
  );
}

// API endpoint constants
export const MODEL_API_ENDPOINTS = {
  LIST: '/v1/models',
  SELECT: '/v1/models/select',
} as const;
