import React, { useState } from 'react';
import { ChevronDown, Circle, CheckCircle2, Loader2, X, Info } from 'lucide-react';
import { useModels } from '@/hooks';
import { cn } from '@/utils/helpers';
import type { Model, ModelProvider } from '@/types/models';

interface ModelSelectorProps {
  onModelChange?: (model: Model | null) => void;
  compact?: boolean;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  onModelChange,
  compact = false,
}) => {
  const { models, currentModel, isLoading, loadModel, unloadModel, setCurrentModel } = useModels();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<ModelProvider | 'all'>('all');

  // Group models by provider
  const providers: ModelProvider[] = Array.from(
    new Set(models.map((m) => m.provider))
  ) as ModelProvider[];

  // Filter models by selected provider
  const filteredModels =
    selectedProvider === 'all'
      ? models
      : models.filter((m) => m.provider === selectedProvider);

  const handleSelectModel = async (model: Model) => {
    if (!model.loaded) {
      await loadModel(model.id);
    }

    setCurrentModel(model.id);
    if (onModelChange) {
      onModelChange(model);
    }
    setIsOpen(false);
  };

  const handleUnloadModel = async (modelId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    await unloadModel(modelId);
  };

  const getProviderColor = (provider: ModelProvider): string => {
    const colors: Record<ModelProvider, string> = {
      local: 'text-green-400',
      openai: 'text-blue-400',
      anthropic: 'text-purple-400',
      google: 'text-yellow-400',
      ollama: 'text-orange-400',
      deepseek: 'text-cyan-400',
      custom: 'text-gray-400',
    };
    return colors[provider] || 'text-gray-400';
  };

  const getProviderBadge = (provider: ModelProvider): string => {
    const badges: Record<ModelProvider, string> = {
      local: 'Local',
      openai: 'OpenAI',
      anthropic: 'Anthropic',
      google: 'Google',
      ollama: 'Ollama',
      deepseek: 'DeepSeek',
      custom: 'Custom',
    };
    return badges[provider] || provider;
  };

  if (compact) {
    return (
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700 transition-colors text-sm"
        >
          {currentModel ? (
            <>
              <Circle className={cn('w-2 h-2 fill-current', getProviderColor(currentModel.provider))} />
              <span className="text-gray-200">{currentModel.name}</span>
            </>
          ) : (
            <span className="text-gray-400">Select model</span>
          )}
          <ChevronDown className="w-4 h-4 text-gray-400" />
        </button>

        {isOpen && (
          <>
            <div className="fixed inset-0 z-10" onClick={() => setIsOpen(false)} />
            <div className="absolute top-full left-0 mt-2 w-80 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-20 max-h-96 overflow-y-auto">
              <ModelList
                models={filteredModels}
                currentModel={currentModel}
                onSelectModel={handleSelectModel}
                onUnloadModel={handleUnloadModel}
                getProviderColor={getProviderColor}
              />
            </div>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
      <h3 className="text-lg font-semibold text-gray-100 mb-4">Model Selection</h3>

      {/* Provider Filter */}
      <div className="flex gap-2 mb-4 flex-wrap">
        <button
          onClick={() => setSelectedProvider('all')}
          className={cn(
            'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
            selectedProvider === 'all'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          )}
        >
          All
        </button>
        {providers.map((provider) => (
          <button
            key={provider}
            onClick={() => setSelectedProvider(provider)}
            className={cn(
              'px-3 py-1 rounded-lg text-sm font-medium transition-colors',
              selectedProvider === provider
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            )}
          >
            {getProviderBadge(provider)}
          </button>
        ))}
      </div>

      {/* Current Model Display */}
      {currentModel && (
        <div className="bg-blue-900/20 border border-blue-900/50 rounded-lg p-3 mb-4">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <CheckCircle2 className="w-4 h-4 text-green-400" />
                <span className="text-sm font-medium text-gray-100">Current Model</span>
              </div>
              <p className="text-gray-200 font-semibold">{currentModel.name}</p>
              <p className="text-xs text-gray-400 mt-1">
                {currentModel.parameters} • {currentModel.contextLength.toLocaleString()} context
                {currentModel.thinkingModel && ' • Thinking model'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Model List */}
      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
        </div>
      ) : filteredModels.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No models found</p>
          {selectedProvider !== 'all' && (
            <button
              onClick={() => setSelectedProvider('all')}
              className="text-blue-400 hover:text-blue-300 text-sm mt-2"
            >
              Show all models
            </button>
          )}
        </div>
      ) : (
        <ModelList
          models={filteredModels}
          currentModel={currentModel}
          onSelectModel={handleSelectModel}
          onUnloadModel={handleUnloadModel}
          getProviderColor={getProviderColor}
        />
      )}
    </div>
  );
};

// Model List Component
interface ModelListProps {
  models: Model[];
  currentModel: Model | null;
  onSelectModel: (model: Model) => void;
  onUnloadModel: (modelId: string, e: React.MouseEvent) => void;
  getProviderColor: (provider: ModelProvider) => string;
}

const ModelList: React.FC<ModelListProps> = ({
  models,
  currentModel,
  onSelectModel,
  onUnloadModel,
  getProviderColor,
}) => {
  return (
    <div className="space-y-2">
      {models.map((model) => (
        <div
          key={model.id}
          onClick={() => onSelectModel(model)}
          className={cn(
            'p-3 rounded-lg border cursor-pointer transition-colors',
            currentModel?.id === model.id
              ? 'bg-blue-900/20 border-blue-600'
              : 'bg-gray-700/50 border-gray-600 hover:bg-gray-700'
          )}
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                {model.loaded ? (
                  <CheckCircle2 className="w-4 h-4 text-green-400 flex-shrink-0" />
                ) : model.loading ? (
                  <Loader2 className="w-4 h-4 text-blue-400 animate-spin flex-shrink-0" />
                ) : (
                  <Circle className="w-4 h-4 text-gray-500 flex-shrink-0" />
                )}
                <span className="text-sm font-medium text-gray-100 truncate">
                  {model.name}
                </span>
                {currentModel?.id === model.id && (
                  <span className="text-xs bg-blue-600 text-white px-2 py-0.5 rounded-full flex-shrink-0">
                    Active
                  </span>
                )}
              </div>

              <div className="flex items-center gap-2 flex-wrap">
                <span className={cn('text-xs font-medium', getProviderColor(model.provider))}>
                  {model.provider.toUpperCase()}
                </span>
                {model.parameters && (
                  <span className="text-xs text-gray-400">• {model.parameters}</span>
                )}
                {model.quantization && (
                  <span className="text-xs text-gray-400">• {model.quantization}</span>
                )}
                {model.thinkingModel && (
                  <span className="text-xs bg-purple-900/50 text-purple-300 px-1.5 py-0.5 rounded">
                    Thinking
                  </span>
                )}
              </div>

              <p className="text-xs text-gray-400 mt-1">
                {model.contextLength.toLocaleString()} context • {model.maxTokens.toLocaleString()} max tokens
              </p>
            </div>

            {model.loaded && (
              <button
                onClick={(e) => onUnloadModel(model.id, e)}
                className="p-1 hover:bg-gray-600 rounded transition-colors"
                title="Unload model"
              >
                <X className="w-4 h-4 text-gray-400" />
              </button>
            )}
          </div>

          {model.metadata?.description && (
            <div className="mt-2 flex items-start gap-2 text-xs text-gray-400">
              <Info className="w-3 h-3 flex-shrink-0 mt-0.5" />
              <p className="line-clamp-2">{model.metadata.description}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
