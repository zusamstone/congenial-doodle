import { useState, useEffect, useCallback } from 'react';
import type { Model, ModelLoadOptions } from '@/types/models';
import { api } from '@/utils/api';

interface UseModelsReturn {
  models: Model[];
  currentModel: Model | null;
  isLoading: boolean;
  error: string | null;
  loadModel: (modelId: string, options?: ModelLoadOptions) => Promise<void>;
  unloadModel: (modelId: string) => Promise<void>;
  setCurrentModel: (modelId: string) => void;
  refreshModels: () => Promise<void>;
}

export const useModels = (): UseModelsReturn => {
  const [models, setModels] = useState<Model[]>([]);
  const [currentModel, setCurrentModelState] = useState<Model | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchModels = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const fetchedModels = await api.get<Model[]>('/models');
      setModels(fetchedModels);

      // Set current model to first loaded model if none is selected
      setCurrentModelState((prevCurrentModel) => {
        if (!prevCurrentModel && fetchedModels.length > 0) {
          const loadedModel = fetchedModels.find((m) => m.loaded);
          return loadedModel || null;
        }
        return prevCurrentModel;
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load models';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchModels();
  }, []);

  const loadModel = useCallback(async (modelId: string, options?: ModelLoadOptions) => {
    setError(null);

    try {
      // Update model status to loading
      setModels((prev) =>
        prev.map((m) => (m.id === modelId ? { ...m, loading: true } : m))
      );

      await api.post(`/models/${modelId}/load`, options || {});

      // Refresh models to get updated status
      await fetchModels();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load model';
      setError(errorMessage);

      // Reset loading status on error
      setModels((prev) =>
        prev.map((m) => (m.id === modelId ? { ...m, loading: false } : m))
      );
    }
  }, [fetchModels]);

  const unloadModel = useCallback(async (modelId: string) => {
    setError(null);

    try {
      await api.post(`/models/${modelId}/unload`);

      // Update model status and clear current model if it was unloaded
      setModels((prev) => {
        const updated = prev.map((m) => (m.id === modelId ? { ...m, loaded: false } : m));
        
        // If current model was unloaded, find another loaded model
        if (currentModel?.id === modelId) {
          const otherLoadedModel = updated.find((m) => m.loaded && m.id !== modelId);
          setCurrentModelState(otherLoadedModel || null);
        }
        
        return updated;
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to unload model';
      setError(errorMessage);
    }
  }, [currentModel]);

  const setCurrentModel = useCallback((modelId: string) => {
    const model = models.find((m) => m.id === modelId);
    if (model) {
      setCurrentModelState(model);
    }
  }, [models]);

  const refreshModels = useCallback(async () => {
    await fetchModels();
  }, [fetchModels]);

  return {
    models,
    currentModel,
    isLoading,
    error,
    loadModel,
    unloadModel,
    setCurrentModel,
    refreshModels,
  };
};
