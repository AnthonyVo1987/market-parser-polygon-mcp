import { useCallback, useEffect, useState } from 'react';
import { fetchModels, selectModel } from '../services/api_OpenAI';
import { AIModel, AIModelId, ModelListResponse } from '../types/ai_models';

interface UseAIModelReturn {
    models: AIModel[];
    currentModel: AIModelId;
    isLoading: boolean;
    error: string | null;
    selectModel: (modelId: AIModelId) => Promise<void>;
    refreshModels: () => Promise<void>;
}

export function useAIModel(): UseAIModelReturn {
    const [models, setModels] = useState<AIModel[]>([]);
    const [currentModel, setCurrentModel] = useState<AIModelId>(AIModelId.GPT_5_NANO);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchModelsData = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            const response: ModelListResponse = await fetchModels();
            setModels(response.models);
            setCurrentModel(response.current_model);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to fetch models';
            setError(errorMessage);
            console.error('Error fetching models:', err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const handleSelectModel = useCallback(async (modelId: AIModelId) => {
        setIsLoading(true);
        setError(null);

        try {
            await selectModel(modelId);
            setCurrentModel(modelId);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to select model';
            setError(errorMessage);
            console.error('Error selecting model:', err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    const refreshModels = useCallback(async () => {
        await fetchModelsData();
    }, [fetchModelsData]);

    // Fetch models on mount
    useEffect(() => {
        fetchModelsData();
    }, [fetchModelsData]);

    return {
        models,
        currentModel,
        isLoading,
        error,
        selectModel: handleSelectModel,
        refreshModels,
    };
}
