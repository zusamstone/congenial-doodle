// Settings and configuration types
export type UserMode = 'general' | 'power' | 'developer';

export type Theme = 'dark' | 'light' | 'system';

export type ContextStrategy = 'smart_summarization' | 'rolling_window' | 'periodic_summary' | 'manual';

export interface Settings {
  userMode: UserMode;
  theme: Theme;
  contextStrategy: ContextStrategy;
  contextThreshold: number;
  defaultModel?: string;
  sampling: SamplingSettings;
  advanced?: AdvancedSamplingSettings;
  modelLoading?: ModelLoadingSettings;
  rag: RAGSettings;
  guidance: GuidanceSettings;
  thinkingModels: ThinkingModelsSettings;
  chat: ChatSettings;
  ui: UISettings;
  privacy: PrivacySettings;
  performance: PerformanceSettings;
  export: ExportSettings;
  updates: UpdateSettings;
  storage: StorageSettings;
  keyboardShortcuts: KeyboardShortcutsSettings;
  experimental?: ExperimentalSettings;
}

export interface SamplingSettings {
  temperature: number;
  maxTokens: number;
  topP: number;
  topK: number;
  repeatPenalty: number;
  frequencyPenalty?: number;
  presencePenalty?: number;
  seed?: number | null;
  stopSequences?: string[];
}

export interface AdvancedSamplingSettings {
  mirostat: number;
  mirostatTau: number;
  mirostatEta: number;
  tfs: number;
  minP: number;
  typicalP: number;
  repeatPenaltyRange: number;
  penaltyAlpha: number;
}

export interface ModelLoadingSettings {
  gpuLayers: number;
  threads?: number | null;
  batchSize: number;
  contextSize?: number | null;
  ropeScaling?: number | null;
}

export interface RAGSettings {
  enabled: boolean;
  maxChunks: number;
  minRelevance: number;
  embeddingModel: string;
  retrievalMethod: 'similarity' | 'mmr' | 'hybrid';
  reranking: boolean;
  chunkSize: number;
  chunkOverlap: number;
  indexChatHistory: boolean;
}

export interface GuidanceSettings {
  enabled: boolean;
  method: 'system_prompt' | 'cfg' | 'logit_bias';
  strength: number;
  positive: string[];
  negative: string[];
}

export interface ThinkingModelsSettings {
  enabled: boolean;
  autoDetect: boolean;
  defaultCollapsed: boolean;
  excludeFromContext: boolean;
  customDelimiters: {
    start: string;
    end: string;
  };
}

export interface ChatSettings {
  streamingEnabled: boolean;
  autoSave: boolean;
  autoTitle: boolean;
  maxHistoryLength: number;
  defaultSystemPrompt?: string | null;
}

export interface UISettings {
  sidebarCollapsed: boolean;
  messageTimestamps: boolean;
  showTokenCounts: boolean;
  showResourceMonitor: boolean;
  codeHighlighting: boolean;
  syntaxTheme: string;
  fontSize: 'small' | 'medium' | 'large';
  messageSpacing: 'compact' | 'comfortable' | 'spacious';
}

export interface PrivacySettings {
  telemetryEnabled: boolean;
  crashReporting: boolean;
  localOnly: boolean;
}

export interface PerformanceSettings {
  lazyLoadModels: boolean;
  autoUnloadUnused: boolean;
  maxLoadedModels: number;
  batchEmbeddings: boolean;
}

export interface ExportSettings {
  includeSystemPrompt: boolean;
  includeMetadata: boolean;
  includeThinking: boolean;
  includeTimestamps: boolean;
  defaultFormat: 'markdown' | 'json' | 'pdf' | 'html';
}

export interface UpdateSettings {
  checkForUpdates: boolean;
  autoDownload: boolean;
  notifyOnly: boolean;
}

export interface StorageSettings {
  dataDirectory: string;
  maxDiskUsage?: number | null;
  autoCleanup: boolean;
  retentionDays?: number | null;
}

export interface KeyboardShortcutsSettings {
  enabled: boolean;
  customShortcuts: Record<string, string>;
}

export interface ExperimentalSettings {
  multimodalSupport: boolean;
  voiceInput: boolean;
  conversationBranching: boolean;
}

export interface SystemPrompt {
  id: string;
  name: string;
  icon: string;
  description: string;
  prompt: string;
  tags: string[];
  usageCount: number;
  defaultSettings?: Partial<Settings>;
  createdAt: Date;
  updatedAt: Date;
}

export interface GuidancePreset {
  id: string;
  name: string;
  description: string;
  method: GuidanceSettings['method'];
  strength: number;
  categories: {
    style: {
      positive: string[];
      negative: string[];
    };
    content: {
      positive: string[];
      negative: string[];
    };
    format: {
      positive: string[];
      negative: string[];
    };
    length: {
      positive: string[];
      negative: string[];
    };
  };
}

export interface APIKey {
  id: string;
  provider: string;
  name: string;
  key: string; // Encrypted
  createdAt: Date;
  lastUsed?: Date;
  usageStats?: {
    requests: number;
    tokens: number;
    cost: number;
  };
}
