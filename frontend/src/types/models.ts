// Model-related types
import type { SamplingSettings } from './settings';

export type ModelProvider = 'local' | 'openai' | 'anthropic' | 'google' | 'ollama' | 'deepseek' | 'custom';

export type ModelType = 'chat' | 'completion' | 'embedding';

export interface Model {
  id: string;
  name: string;
  provider: ModelProvider;
  modelId: string;
  type?: ModelType;
  path?: string; // For local models
  contextLength: number;
  maxTokens: number;
  parameters?: string; // e.g., "7B", "70B"
  architecture?: string; // e.g., "llama", "mistral"
  size?: number; // File size in bytes
  quantization?: string; // e.g., "Q4_K_M", "Q8_0"
  thinkingModel: boolean;
  supportsVision?: boolean;
  supportsFunctions?: boolean;
  supportsJsonMode?: boolean;
  loaded: boolean;
  loading?: boolean;
  metadata?: ModelMetadata;
  pricing?: ModelPricing;
  recommendedSettings?: Partial<SamplingSettings>;
  hardwareRequirements?: HardwareRequirements;
}

export interface ModelMetadata {
  description?: string;
  author?: string;
  license?: string;
  homepage?: string;
  downloads?: number;
  likes?: number;
  tags?: string[];
  createdAt?: Date;
  updatedAt?: Date;
}

export interface ModelPricing {
  input: number; // Cost per unit
  output: number; // Cost per unit
  unit: string; // e.g., "1K tokens"
  thinking?: number; // For thinking models
}

export interface HardwareRequirements {
  vram?: string;
  ram?: string;
  diskSpace?: string;
  minGpuLayers?: number;
}

export interface ModelLoadOptions {
  gpuLayers?: number;
  threads?: number;
  batchSize?: number;
  contextSize?: number;
  ropeScaling?: number;
  mlock?: boolean;
  mmap?: boolean;
}

export interface EmbeddingModel {
  id: string;
  name: string;
  provider: 'local' | 'openai' | 'cohere';
  dimensions: number;
  maxSequenceLength: number;
  size?: string;
  speed: 'slow' | 'medium' | 'fast';
  quality: 'good' | 'better' | 'excellent' | 'best';
  useCase: string;
  pricing?: {
    cost: number;
    unit: string;
  };
}

export interface LoRA {
  id: string;
  name: string;
  path: string;
  compatibleModels: string[];
  weight: number;
  enabled: boolean;
  size?: number;
  description?: string;
  author?: string;
  tags?: string[];
  metadata?: Record<string, unknown>;
  createdAt: Date;
}

export interface ModelDownload {
  id: string;
  modelId: string;
  modelName: string;
  url: string;
  status: 'queued' | 'downloading' | 'paused' | 'completed' | 'error' | 'cancelled';
  progress: number; // 0-100
  downloadedBytes: number;
  totalBytes: number;
  speed?: number; // bytes/sec
  eta?: number; // seconds remaining
  error?: string;
  createdAt: Date;
  completedAt?: Date;
}

export interface ModelCompatibility {
  compatible: boolean;
  reasons?: string[];
  warnings?: string[];
  suggestions?: string[];
}

export interface ModelBenchmark {
  modelId: string;
  tokensPerSecond?: number;
  timeToFirstToken?: number;
  vramUsage?: number;
  ramUsage?: number;
  powerUsage?: number;
  timestamp: Date;
}
