import { FC, memo } from 'react';
import { AIModel, AIModelId } from '../types/ai_models';

interface AIModelSelectorProps {
    models: AIModel[];
    currentModel: AIModelId;
    onModelChange: (modelId: AIModelId) => void;
    loading?: boolean;
    error?: string | null;
    disabled?: boolean;
}

const AIModelSelector: FC<AIModelSelectorProps> = memo(({
    models,
    currentModel,
    onModelChange,
    loading = false,
    error = null,
    disabled = false,
}) => {
    const handleModelChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedModelId = e.target.value as AIModelId;
        onModelChange(selectedModelId);
    };

    return (
        <div className="ai-model-selector-container" data-testid="ai-model-selector">
            <label htmlFor="model-selector" className="model-selector-label">
                Model:
            </label>
            <select
                id="model-selector"
                value={currentModel}
                onChange={handleModelChange}
                disabled={disabled || loading}
                className={`model-selector ${error ? 'error' : ''} ${loading ? 'loading' : ''}`}
                aria-label="Select AI Model"
                aria-describedby={error ? 'model-selector-error' : undefined}
            >
                {models.map((model) => (
                    <option key={model.id} value={model.id}>
                        {model.name}
                    </option>
                ))}
            </select>
            {error && (
                <div id="model-selector-error" className="model-selector-error" role="alert">
                    {error}
                </div>
            )}
            {loading && (
                <div className="model-selector-loading" aria-live="polite">
                    Loading models...
                </div>
            )}
        </div>
    );
});

AIModelSelector.displayName = 'AIModelSelector';

export default AIModelSelector;

// Styles for the AI Model Selector
export const modelSelectorStyles = `
  .ai-model-selector-container {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 120px;
  }

  .model-selector-label {
    font-size: 12px;
    color: var(--neutral-300);
    font-weight: 500;
    font-family: var(--font-inter);
  }

  .model-selector {
    padding: 8px 12px;
    border: 1px solid var(--glass-border-highlight);
    border-radius: var(--radius-md);
    background: var(--glass-surface-light);
    color: var(--neutral-100);
    font-size: 14px;
    font-family: var(--font-inter);
    cursor: pointer;
    transition: all 0.2s ease;
    min-height: 36px;
  }

  .model-selector:hover:not(:disabled) {
    border-color: var(--primary-400);
    background: var(--glass-surface-medium);
  }

  .model-selector:focus {
    outline: none;
    border-color: var(--primary-500);
    box-shadow: 0 0 0 2px rgba(99, 179, 237, 0.2);
  }

  .model-selector:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background: var(--glass-surface-dark);
  }

  .model-selector.loading {
    opacity: 0.7;
    cursor: wait;
  }

  .model-selector.error {
    border-color: var(--error-500);
    background: rgba(239, 68, 68, 0.1);
  }

  .model-selector-error {
    font-size: 11px;
    color: var(--error-400);
    font-family: var(--font-inter);
    margin-top: 2px;
  }

  .model-selector-loading {
    font-size: 11px;
    color: var(--neutral-400);
    font-family: var(--font-inter);
    margin-top: 2px;
    font-style: italic;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .ai-model-selector-container {
      min-width: 100px;
    }

    .model-selector {
      padding: 6px 8px;
      font-size: 13px;
      min-height: 32px;
    }

    .model-selector-label {
      font-size: 11px;
    }
  }
`;
