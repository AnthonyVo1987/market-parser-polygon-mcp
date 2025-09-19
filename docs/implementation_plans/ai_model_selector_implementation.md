# AI Model Selector Implementation Plan

## Overview
This document outlines the implementation plan for adding an AI Model Selector dropdown menu in the Debug Panel, changing the default model from 'gpt-5-mini' to 'gpt-5-nano', and appending model names to all AI responses.

## Research-Based Implementation (Context7 Patterns)

### Phase 1: Backend Implementation (FastAPI/Pydantic Best Practices)

#### 1.1 Update Settings Configuration (`src/backend/main.py`)
```python
class Settings:
    """Application configuration with hard-coded server configuration."""
    
    def __init__(self):
        # ... existing code ...
        self.openai_model: str = "gpt-5-nano"  # Changed from gpt-5-mini
        self.available_models: List[str] = [
            "gpt-5-nano",
            "gpt-5-mini", 
            "gpt-4o",
            "gpt-4o-mini"
        ]
```

#### 1.2 Create API Models with Pydantic V2 (`src/backend/api_models.py`)
Following Context7 FastAPI best practices with custom base model:

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum

# Custom base model for consistent serialization (Context7 pattern)
class CustomModel(BaseModel):
    """Base model with custom configuration for all API models"""
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={"example": {}}
    )

class AIModelId(str, Enum):
    """Enum for available AI models"""
    GPT_5_NANO = "gpt-5-nano"
    GPT_5_MINI = "gpt-5-mini"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"

class AIModel(CustomModel):
    """AI Model information with validation"""
    id: AIModelId = Field(..., description="Model identifier")
    name: str = Field(..., description="Display name", min_length=1, max_length=50)
    description: Optional[str] = Field(None, description="Model description", max_length=200)
    is_default: bool = Field(False, description="Whether this is the default model")
    cost_per_1k_tokens: Optional[float] = Field(None, ge=0, description="Cost per 1000 tokens")
    max_tokens: Optional[int] = Field(None, gt=0, description="Maximum tokens supported")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is properly formatted"""
        return v.strip()

class ModelListResponse(CustomModel):
    """Response for listing available models"""
    models: List[AIModel]
    current_model: AIModelId
    total_count: int = Field(..., ge=0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ModelSelectionRequest(CustomModel):
    """Request for selecting a model with validation"""
    model_id: AIModelId = Field(..., description="Model ID to select")

class ModelSelectionResponse(CustomModel):
    """Response for model selection"""
    success: bool
    message: str = Field(..., min_length=1)
    selected_model: AIModelId
    previous_model: Optional[AIModelId] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

#### 1.3 Update process_financial_query Function
```python
from typing import Optional

async def process_financial_query(
    query: str,
    session: Session,
    server: StdioServer,
    model: Optional[AIModelId] = None
) -> str:
    """
    Process financial query with specified AI model.
    
    Args:
        query: The user's query
        session: MCP session
        server: MCP server instance
        model: Optional AI model to use (defaults to settings.openai_model)
    
    Returns:
        Formatted response with model identifier
    """
    # Use provided model or default
    active_model = model.value if model else settings.openai_model
    
    # ... existing processing logic ...
    
    # Append model name to response
    response_with_model = f"{formatted_response}\n\n[{active_model}]"
    return response_with_model
```

#### 1.4 API Endpoints with Dependency Injection Pattern
Following Context7 FastAPI dependency injection best practices:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Mapping

# Dependency for validating model selection (Context7 pattern)
async def valid_model_id(request: ModelSelectionRequest) -> AIModelId:
    """Validate that the requested model exists and is available"""
    if request.model_id.value not in settings.available_models:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid model ID: {request.model_id.value}"
        )
    return request.model_id

# Model management router
model_router = APIRouter(prefix="/api/v1/models", tags=["AI Models"])

@model_router.get(
    "",
    response_model=ModelListResponse,
    summary="List available AI models",
    description="Get list of all available AI models with current selection",
    responses={
        status.HTTP_200_OK: {
            "model": ModelListResponse,
            "description": "Successfully retrieved model list"
        }
    }
)
async def get_available_models():
    """Get list of available AI models"""
    models = [
        AIModel(
            id=AIModelId.GPT_5_NANO,
            name="GPT-5 Nano",
            description="Fast and efficient model for quick responses",
            is_default=True,
            cost_per_1k_tokens=0.15,
            max_tokens=4096
        ),
        AIModel(
            id=AIModelId.GPT_5_MINI,
            name="GPT-5 Mini",
            description="Balanced performance model",
            is_default=False,
            cost_per_1k_tokens=0.25,
            max_tokens=8192
        ),
        AIModel(
            id=AIModelId.GPT_4O,
            name="GPT-4o",
            description="Advanced model for complex tasks",
            is_default=False,
            cost_per_1k_tokens=2.50,
            max_tokens=4096
        ),
        AIModel(
            id=AIModelId.GPT_4O_MINI,
            name="GPT-4o Mini",
            description="Cost-effective advanced model",
            is_default=False,
            cost_per_1k_tokens=0.15,
            max_tokens=16384
        )
    ]
    
    return ModelListResponse(
        models=models,
        current_model=AIModelId(settings.openai_model),
        total_count=len(models)
    )

@model_router.post(
    "/select",
    response_model=ModelSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Select an AI model",
    description="Change the active AI model for subsequent requests",
    responses={
        status.HTTP_200_OK: {
            "model": ModelSelectionResponse,
            "description": "Model successfully selected"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid model ID provided"
        }
    }
)
async def select_model(
    model_id: AIModelId = Depends(valid_model_id)
):
    """Select an AI model for use"""
    previous_model = settings.openai_model
    settings.openai_model = model_id.value
    
    return ModelSelectionResponse(
        success=True,
        message=f"Successfully switched from {previous_model} to {model_id.value}",
        selected_model=model_id,
        previous_model=AIModelId(previous_model) if previous_model != model_id.value else None
    )

# Add router to app
app.include_router(model_router)
```

### Phase 2: Frontend Implementation (React TypeScript Best Practices)

#### 2.1 TypeScript Types with Strict Typing (`src/frontend/types/ai_models.ts`)
Following Context7 React TypeScript patterns:

```typescript
// Enum for model IDs matching backend
export enum AIModelId {
  GPT_5_NANO = 'gpt-5-nano',
  GPT_5_MINI = 'gpt-5-mini',
  GPT_4O = 'gpt-4o',
  GPT_4O_MINI = 'gpt-4o-mini'
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
  readonly currentModel: AIModelId;
  readonly totalCount: number;
  readonly timestamp: string;
}

export interface ModelSelectionRequest {
  readonly modelId: AIModelId;
}

export interface ModelSelectionResponse {
  readonly success: boolean;
  readonly message: string;
  readonly selectedModel: AIModelId;
  readonly previousModel?: AIModelId;
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

export function isValidModelListResponse(value: unknown): value is ModelListResponse {
  return (
    typeof value === 'object' &&
    value !== null &&
    'models' in value &&
    'currentModel' in value &&
    Array.isArray((value as ModelListResponse).models) &&
    (value as ModelListResponse).models.every(isValidAIModel)
  );
}
```

#### 2.2 Custom Hook for Model Management (`src/frontend/hooks/useAIModel.ts`)
Following Context7 React hooks patterns:

```typescript
import { useState, useEffect, useCallback, useRef } from 'react';
import { AIModel, AIModelId, ModelListResponse } from '../types/ai_models';
import { getAvailableModels, selectModel } from '../services/api_OpenAI';
import { logger } from '../utils/logger';

interface UseAIModelReturn {
  models: readonly AIModel[];
  currentModel: AIModelId | null;
  isLoading: boolean;
  error: string | null;
  selectModel: (modelId: AIModelId) => Promise<void>;
  refreshModels: () => Promise<void>;
}

export function useAIModel(): UseAIModelReturn {
  const [models, setModels] = useState<readonly AIModel[]>([]);
  const [currentModel, setCurrentModel] = useState<AIModelId | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Use ref to track if component is mounted
  const isMountedRef = useRef(true);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const loadModels = useCallback(async () => {
    if (!isMountedRef.current) return;
    
    setIsLoading(true);
    setError(null);

    try {
      const response = await getAvailableModels();
      
      if (!isMountedRef.current) return;
      
      setModels(response.models);
      setCurrentModel(response.currentModel);
      
      // Persist to localStorage
      localStorage.setItem('selectedAIModel', response.currentModel);
      
      logger.info('AI models loaded successfully', {
        modelCount: response.totalCount,
        currentModel: response.currentModel
      });
    } catch (err) {
      if (!isMountedRef.current) return;
      
      const errorMessage = err instanceof Error ? err.message : 'Failed to load models';
      setError(errorMessage);
      logger.error('Failed to load AI models', { error: errorMessage });
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  }, []);

  const handleSelectModel = useCallback(async (modelId: AIModelId) => {
    if (!isMountedRef.current || modelId === currentModel) return;
    
    setIsLoading(true);
    setError(null);

    try {
      const response = await selectModel(modelId);
      
      if (!isMountedRef.current) return;
      
      if (response.success) {
        setCurrentModel(response.selectedModel);
        localStorage.setItem('selectedAIModel', response.selectedModel);
        
        logger.info('Model selected successfully', {
          previousModel: response.previousModel,
          selectedModel: response.selectedModel
        });
      }
    } catch (err) {
      if (!isMountedRef.current) return;
      
      const errorMessage = err instanceof Error ? err.message : 'Failed to select model';
      setError(errorMessage);
      logger.error('Failed to select model', { error: errorMessage, modelId });
    } finally {
      if (isMountedRef.current) {
        setIsLoading(false);
      }
    }
  }, [currentModel]);

  // Load models on mount
  useEffect(() => {
    loadModels();
  }, [loadModels]);

  return {
    models,
    currentModel,
    isLoading,
    error,
    selectModel: handleSelectModel,
    refreshModels: loadModels
  };
}
```

#### 2.3 Updated DebugPanel Component with Context7 Patterns
```typescript
import { memo, useCallback } from 'react';
import { useComponentLogger } from '../hooks/useDebugLog';
import { logger, LogMode } from '../utils/logger';
import { AIModel, AIModelId } from '../types/ai_models';

interface DebugPanelProps {
  latestResponseTime: number | null;
  className?: string;
  onDebugAction?: (action: string, details: Record<string, unknown>) => void;
  // AI Model props
  models: readonly AIModel[];
  currentModel: AIModelId | null;
  onModelChange: (modelId: AIModelId) => void;
  isLoadingModels?: boolean;
  modelError?: string | null;
}

const DebugPanel = memo<DebugPanelProps>(({ 
  latestResponseTime, 
  className = '',
  onDebugAction,
  models,
  currentModel,
  onModelChange,
  isLoadingModels = false,
  modelError = null
}) => {
  useComponentLogger('DebugPanel', { 
    hasResponseTime: latestResponseTime !== null,
    responseTime: latestResponseTime,
    currentModel,
    modelCount: models.length
  });

  // ... existing state and handlers ...

  const handleModelChange = useCallback((event: React.ChangeEvent<HTMLSelectElement>) => {
    const modelId = event.target.value as AIModelId;
    if (Object.values(AIModelId).includes(modelId)) {
      onModelChange(modelId);
      logger.debug('Model selection changed', {
        component: 'DebugPanel',
        newModel: modelId,
        previousModel: currentModel
      });
    }
  }, [currentModel, onModelChange]);

  return (
    <div className={`debug-panel ${className}`} role="status" aria-label="Debug information">
      {/* ... existing header ... */}
      
      <div id="debug-panel-content" className={`collapsible-content ${isExpanded ? 'expanded' : 'collapsed'}`}>
        <div className="debug-content">
          {/* ... existing metrics ... */}
          
          {/* AI Model Selector - Context7 pattern */}
          <div className="debug-metric">
            <span className="debug-label">AI Model:</span>
            <div className="model-selector-container">
              <select
                className="model-selector"
                value={currentModel || ''}
                onChange={handleModelChange}
                disabled={isLoadingModels || models.length === 0}
                aria-label="Select AI model"
                aria-describedby={modelError ? "model-error" : undefined}
              >
                {models.length === 0 ? (
                  <option value="">No models available</option>
                ) : (
                  models.map(model => (
                    <option key={model.id} value={model.id}>
                      {model.name}
                      {model.isDefault && ' (default)'}
                    </option>
                  ))
                )}
              </select>
              {isLoadingModels && (
                <span className="loading-indicator" aria-label="Loading models">
                  Loading...
                </span>
              )}
              {modelError && (
                <span id="model-error" className="error-message" role="alert">
                  {modelError}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

DebugPanel.displayName = 'DebugPanel';

export default DebugPanel;
```

#### 2.4 Enhanced Styles with CSS Custom Properties
```css
/* Add to debugPanelStyles - Context7 styling patterns */
.model-selector-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  position: relative;
}

.model-selector {
  background: var(--glass-surface-1);
  backdrop-filter: var(--glass-blur-sm);
  border: 1px solid var(--glass-border-2);
  color: var(--text-primary);
  padding: var(--spacing-1) var(--spacing-2);
  padding-right: var(--spacing-6); /* Space for dropdown arrow */
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: var(--font-size-small);
  min-width: 160px;
  cursor: pointer;
  transition: all 0.2s var(--transition-timing);
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right var(--spacing-2) center;
  background-size: 16px;
}

.model-selector:hover:not(:disabled) {
  background-color: var(--glass-surface-2);
  border-color: var(--accent-info);
  box-shadow: 0 0 0 1px var(--accent-info-light);
}

.model-selector:focus {
  outline: 2px solid var(--accent-info);
  outline-offset: 2px;
}

.model-selector:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.model-selector option {
  background: var(--background-primary);
  color: var(--text-primary);
  padding: var(--spacing-1);
}

.loading-indicator {
  position: absolute;
  right: var(--spacing-8);
  font-size: var(--font-size-micro);
  color: var(--accent-info);
  animation: pulse 1.5s ease-in-out infinite;
}

.error-message {
  position: absolute;
  top: calc(100% + var(--spacing-1));
  left: 0;
  font-size: var(--font-size-micro);
  color: var(--accent-error);
  white-space: nowrap;
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .model-selector {
    min-width: 120px;
    font-size: var(--font-size-micro);
  }
  
  .model-selector-container {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-1);
  }
  
  .error-message {
    position: static;
    margin-top: var(--spacing-1);
  }
}
```

#### 2.5 API Service Functions (`src/frontend/services/api_OpenAI.ts`)
```typescript
export async function getAvailableModels(): Promise<ModelListResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/models`);
  if (!response.ok) throw new Error('Failed to fetch models');
  return response.json();
}

export async function selectModel(modelId: AIModelId): Promise<ModelSelectionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/models/select`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ modelId })
  });
  if (!response.ok) throw new Error('Failed to select model');
  return response.json();
}
```

#### 2.6 Update ChatInterface Component
```typescript
import { useAIModel } from '../hooks/useAIModel';

export default function ChatInterface() {
  const { models, currentModel, isLoading, error, selectModel } = useAIModel();
  
  // ... existing state ...

  // Pass model to API calls
  const handleSendMessage = async (message: string) => {
    try {
      const response = await sendChatMessage(message, currentModel);
      // ... handle response ...
    } catch (error) {
      // ... error handling ...
    }
  };

  return (
    <>
      {/* ... existing UI ... */}
      <DebugPanel
        latestResponseTime={latestResponseTime}
        className="main-debug-panel"
        onDebugAction={handleDebugAction}
        models={models}
        currentModel={currentModel}
        onModelChange={selectModel}
        isLoadingModels={isLoading}
        modelError={error}
      />
    </>
  );
}
```

### Phase 3: Documentation Updates

#### 3.1 Update CLAUDE.md
- Change all references from "gpt-5-mini" to "gpt-5-nano"
- Add section documenting the Model Selector feature:
  ```markdown
  ## AI Model Selector
  The Debug Panel now includes a dropdown menu for selecting AI models on-the-fly. 
  Default model is set to 'gpt-5-nano' for optimal performance.
  
  Available models:
  - GPT-5 Nano (default) - Fast and efficient
  - GPT-5 Mini - Balanced performance
  - GPT-4o - Advanced capabilities
  - GPT-4o Mini - Cost-effective option
  ```

#### 3.2 Update README.md
- Update default model references
- Add feature description in Features section
- Update architecture documentation

### Phase 4: Testing Strategy

#### 4.1 Playwright Tests
Create tests to verify:
1. Model dropdown is visible and populated
2. Model selection changes are persisted
3. API responses include model names
4. Default model is 'gpt-5-nano'

### Phase 5: Final Tasks

1. **Code Review**: Use Serena tools to verify all changes
2. **Commit Message**: Create comprehensive git commit message
3. **Update CLAUDE.md**: Add commit message to Last Completed Task Summary
4. **Git Operations**: Stage all changes, commit, and push

## Key Implementation Details

1. **State Management**: Model selection state managed at ChatInterface level and passed down to both DebugPanel and API calls
2. **Persistence**: Using localStorage to persist user's model selection across sessions
3. **Error Handling**: Proper error handling for model switching failures
4. **Loading States**: Loading indicator while switching models
5. **Response Format**: All AI responses must end with `[model-name]` format

## Context7 Research-Based Patterns Applied

### Backend (FastAPI/Pydantic)
- Custom base model for consistent serialization
- Enum types for model IDs ensuring type safety
- Field validators and constraints
- Dependency injection for validation
- Comprehensive API documentation with response schemas
- Proper error handling with HTTP status codes

### Frontend (React/TypeScript)
- Strict readonly types for immutability
- Type guards for runtime validation
- Custom hook with proper cleanup and error handling
- Memoized components for performance
- Accessibility attributes (ARIA labels, roles)
- CSS custom properties for maintainable styling
- Responsive design considerations

This implementation ensures type safety, performance, accessibility, and maintainability while following the latest best practices from the React and FastAPI ecosystems as researched through Context7.