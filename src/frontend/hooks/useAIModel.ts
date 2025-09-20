/**
 * Custom Hook for AI Model Management
 * 
 * Provides state management and API integration for AI model selection.
 * Follows React TypeScript best practices with proper cleanup and error handling.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { getAvailableModels, selectModel } from '../services/api_OpenAI';
import { AIModel, AIModelId } from '../types/ai_models';
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
        isMountedRef.current = true;
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
            setCurrentModel(response.current_model);

            // Persist to localStorage
            localStorage.setItem('selectedAIModel', response.current_model);

            logger.info('AI models loaded successfully', {
                modelCount: response.total_count,
                currentModel: response.current_model
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
                setCurrentModel(response.selected_model);
                localStorage.setItem('selectedAIModel', response.selected_model);

                logger.info('Model selected successfully', {
                    previousModel: response.previous_model,
                    selectedModel: response.selected_model
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
        void loadModels();
    }, [loadModels]);

    return {
        models,
        currentModel,
        isLoading,
        error,
        selectModel: handleSelectModel,
        refreshModels: loadModels
    } as const;
}
