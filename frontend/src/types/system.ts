// System monitoring and resource types
export interface SystemResources {
  cpu: CPUInfo;
  gpu?: GPUInfo;
  memory: MemoryInfo;
  vram?: VRAMInfo;
  disk: DiskInfo;
  timestamp: Date;
}

export interface CPUInfo {
  model: string;
  cores: number;
  threads: number;
  usage: number; // 0-100
  perCoreUsage?: number[];
  temperature?: number;
  frequency?: number; // MHz
  architecture: string;
  features: string[]; // AVX, AVX2, AVX512, etc.
}

export interface GPUInfo {
  vendor: 'nvidia' | 'amd' | 'intel' | 'apple' | 'other';
  model: string;
  usage: number; // 0-100
  memory: number; // Total VRAM in bytes
  memoryUsed: number; // Used VRAM in bytes
  temperature?: number;
  powerUsage?: number; // Watts
  computeCapability?: string;
  driverVersion?: string;
  cudaVersion?: string;
  supports: {
    cuda?: boolean;
    rocm?: boolean;
    metal?: boolean;
    vulkan?: boolean;
  };
}

export interface MemoryInfo {
  total: number; // bytes
  used: number; // bytes
  available: number; // bytes
  percentage: number; // 0-100
  swapTotal?: number;
  swapUsed?: number;
}

export interface VRAMInfo {
  total: number; // bytes
  used: number; // bytes
  available: number; // bytes
  percentage: number; // 0-100
  allocations?: VRAMAllocation[];
}

export interface VRAMAllocation {
  id: string;
  name: string; // Model name or process
  size: number; // bytes
  type: 'model' | 'lora' | 'embeddings' | 'cache' | 'other';
}

export interface DiskInfo {
  total: number; // bytes
  used: number; // bytes
  available: number; // bytes
  percentage: number; // 0-100
  dataDirectory: {
    size: number;
    modelCount: number;
    loraCount: number;
    sourceCount: number;
  };
}

export interface PerformanceMetrics {
  modelId?: string;
  tokensPerSecond?: number;
  timeToFirstToken?: number; // ms
  totalGenerationTime?: number; // ms
  promptTokens?: number;
  completionTokens?: number;
  totalTokens?: number;
  vramUsage?: number; // bytes
  ramUsage?: number; // bytes
  cpuUsage?: number; // percentage
  gpuUsage?: number; // percentage
  timestamp: Date;
}

export interface HardwareCapabilities {
  cpu: {
    model: string;
    cores: number;
    threads: number;
    features: string[];
  };
  gpu?: {
    vendor: string;
    model: string;
    vram: number;
    computeCapability?: string;
    supports: string[];
  };
  ram: number;
  recommendedModels: string[];
  warnings: string[];
}

export interface ResourceWarning {
  id: string;
  type: 'vram' | 'ram' | 'disk' | 'cpu' | 'gpu' | 'temperature';
  severity: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  suggestion?: string;
  timestamp: Date;
  dismissed?: boolean;
}

export interface TokenUsage {
  chatId: string;
  messageId?: string;
  promptTokens: number;
  completionTokens: number;
  thinkingTokens?: number;
  totalTokens: number;
  cost?: number;
  model: string;
  timestamp: Date;
}

export interface ContextUsage {
  chatId: string;
  systemPromptTokens: number;
  pinnedMessagesTokens: number;
  summariesTokens: number;
  recentMessagesTokens: number;
  ragContextTokens: number;
  totalTokens: number;
  maxTokens: number;
  percentage: number; // 0-100
  breakdown: ContextBreakdown[];
}

export interface ContextBreakdown {
  component: 'system' | 'pinned' | 'summary' | 'messages' | 'rag';
  tokens: number;
  percentage: number;
  details?: string;
}

// Notification types
export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  action?: NotificationAction;
  dismissible: boolean;
  autoClose?: number; // ms
  createdAt: Date;
}

export interface NotificationAction {
  label: string;
  onClick: () => void;
}

// Search types
export interface SearchQuery {
  query: string;
  type: 'keyword' | 'semantic' | 'hybrid';
  filters?: SearchFilters;
  limit?: number;
  offset?: number;
}

export interface SearchFilters {
  chatIds?: string[];
  dateRange?: {
    start: Date;
    end: Date;
  };
  models?: string[];
  tags?: string[];
  folders?: string[];
  pinned?: boolean;
  archived?: boolean;
}

export interface SearchResult {
  type: 'chat' | 'message' | 'source';
  id: string;
  chatId?: string;
  title: string;
  content: string;
  relevance: number;
  highlights?: string[];
  metadata?: Record<string, any>;
}

export interface SearchResults {
  query: string;
  results: SearchResult[];
  total: number;
  searchTime: number;
  type: 'keyword' | 'semantic' | 'hybrid';
}

// Error types
export interface AppError {
  id: string;
  code: string;
  message: string;
  details?: string;
  stack?: string;
  timestamp: Date;
  context?: Record<string, any>;
  recoverable: boolean;
  suggestion?: string;
}

export type ErrorCode =
  | 'MODEL_LOAD_FAILED'
  | 'MODEL_INFERENCE_FAILED'
  | 'NETWORK_ERROR'
  | 'API_ERROR'
  | 'VRAM_INSUFFICIENT'
  | 'DISK_FULL'
  | 'DATABASE_ERROR'
  | 'EMBEDDING_FAILED'
  | 'INVALID_INPUT'
  | 'UNAUTHORIZED'
  | 'RATE_LIMITED'
  | 'UNKNOWN_ERROR';

// Update types
export interface UpdateInfo {
  version: string;
  releaseDate: Date;
  releaseNotes: string;
  downloadUrl: string;
  mandatory: boolean;
  size: number;
}

export interface UpdateProgress {
  status: 'checking' | 'available' | 'downloading' | 'ready' | 'error';
  progress?: number; // 0-100
  downloaded?: number;
  total?: number;
  error?: string;
}
