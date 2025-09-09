import { useState, useEffect, useCallback, useRef } from 'react';
import {
  PromptTemplate,
  PromptTemplateResponse,
  GeneratePromptRequest,
  GeneratePromptResponse,
  UsePromptAPIResult,
  PROMPT_API_ENDPOINTS,
  isValidPromptTemplate,
} from '../types/chat_OpenAI';

const API_BASE_URL = 'http://localhost:8001';

// Cache for template data to avoid unnecessary API calls
const templateCache = {
  data: null as readonly PromptTemplate[] | null,
  timestamp: 0,
  ttl: 5 * 60 * 1000, // 5 minutes cache TTL
};

/**
 * Custom hook for managing prompt template API integration
 * Follows the patterns learned from Rooks library for API management
 */
export function usePromptAPI(): UsePromptAPIResult {
  const [templates, setTemplates] = useState<readonly PromptTemplate[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Cleanup function for component unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  /**
   * Fetches prompt templates from the API with caching
   */
  const fetchTemplates = useCallback(
    async (forceRefresh = false): Promise<void> => {
      // Check cache first (unless force refresh)
      const now = Date.now();
      if (
        !forceRefresh &&
        templateCache.data &&
        now - templateCache.timestamp < templateCache.ttl
      ) {
        setTemplates(templateCache.data);
        return;
      }

      // Cancel previous request if still in progress
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      setLoading(true);
      setError(null);

      try {
        abortControllerRef.current = new AbortController();

        const response = await fetch(
          `${API_BASE_URL}${PROMPT_API_ENDPOINTS.TEMPLATES}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
            signal: abortControllerRef.current.signal,
          }
        );

        if (!response.ok) {
          throw new Error(
            `Failed to fetch templates: ${response.status} ${response.statusText}`
          );
        }

        const data = (await response.json()) as PromptTemplateResponse;

        if (!data.success) {
          throw new Error(data.error || 'Failed to fetch templates');
        }

        // Validate template data
        const validTemplates = data.templates.filter(
          (template): template is PromptTemplate => {
            if (!isValidPromptTemplate(template)) {
              // Invalid template filtered out silently
              return false;
            }
            return true;
          }
        );

        // Update cache
        templateCache.data = validTemplates;
        templateCache.timestamp = now;

        setTemplates(validTemplates);
      } catch (err) {
        // Handle aborted requests gracefully
        if (err instanceof Error && err.name === 'AbortError') {
          return;
        }

        const errorMessage =
          err instanceof Error
            ? err.message
            : 'Unknown error fetching templates';
        setError(errorMessage);
        // Error logged via setError state for user feedback
      } finally {
        setLoading(false);
        abortControllerRef.current = null;
      }
    },
    []
  );

  /**
   * Generates a prompt from a template with dynamic ticker substitution
   */
  const generatePrompt = useCallback(
    async (templateId: string, ticker?: string): Promise<string> => {
      try {
        const requestData: GeneratePromptRequest = {
          templateId,
          ...(ticker && { ticker }),
        };

        const response = await fetch(
          `${API_BASE_URL}${PROMPT_API_ENDPOINTS.GENERATE}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
          }
        );

        if (!response.ok) {
          throw new Error(
            `Failed to generate prompt: ${response.status} ${response.statusText}`
          );
        }

        const data = (await response.json()) as GeneratePromptResponse;

        if (!data.success) {
          throw new Error(data.error || 'Failed to generate prompt');
        }

        return data.prompt;
      } catch (err) {
        const errorMessage =
          err instanceof Error
            ? err.message
            : 'Unknown error generating prompt';
        setError(errorMessage);
        // Error logged via setError state for user feedback
        throw new Error(errorMessage);
      }
    },
    []
  );

  /**
   * Force refresh templates from API
   */
  const refreshTemplates = useCallback(async (): Promise<void> => {
    await fetchTemplates(true);
  }, [fetchTemplates]);

  // Load templates on mount
  useEffect(() => {
    void fetchTemplates(); // Use void operator to explicitly indicate we're not awaiting this promise
  }, [fetchTemplates]);

  return {
    templates,
    loading,
    error,
    generatePrompt,
    refreshTemplates,
  };
}

/**
 * Utility hook for managing prompt generation loading state
 * Useful for individual button components
 */
export function usePromptGeneration() {
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [generationError, setGenerationError] = useState<string | null>(null);

  const generateWithLoading = useCallback(
    async (
      generateFn: () => Promise<string>,
      onSuccess: (prompt: string) => void
    ) => {
      setIsGenerating(true);
      setGenerationError(null);

      try {
        const prompt = await generateFn();
        onSuccess(prompt);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'Failed to generate prompt';
        setGenerationError(errorMessage);
        // Error logged via setGenerationError state for user feedback
      } finally {
        setIsGenerating(false);
      }
    },
    []
  );

  return {
    isGenerating,
    generationError,
    generateWithLoading,
  };
}
