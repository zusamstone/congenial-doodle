// RAG (Retrieval Augmented Generation) types
export type DocumentFormat = 'pdf' | 'txt' | 'md' | 'docx' | 'html' | 'json' | 'csv' | 'code' | 'url';

export type ChunkingStrategy = 'sentence' | 'paragraph' | 'fixed' | 'semantic';

export type RetrievalMethod = 'similarity' | 'mmr' | 'hybrid';

export interface KnowledgeSource {
  id: string;
  name: string;
  type: DocumentFormat;
  path?: string;
  url?: string;
  chunkCount: number;
  embeddingModel: string;
  size?: number; // File size in bytes
  pageCount?: number;
  createdAt: Date;
  updatedAt?: Date;
  metadata?: SourceMetadata;
  indexed: boolean;
  indexing?: boolean;
  error?: string;
}

export interface SourceMetadata {
  author?: string;
  title?: string;
  description?: string;
  tags?: string[];
  language?: string;
  createdDate?: Date;
  modifiedDate?: Date;
  customFields?: Record<string, unknown>;
}

export interface DocumentChunk {
  id: string;
  sourceId: string;
  content: string;
  embedding?: number[];
  metadata: ChunkMetadata;
  createdAt: Date;
}

export interface ChunkMetadata {
  page?: number;
  section?: string;
  chunkIndex: number;
  startChar?: number;
  endChar?: number;
  heading?: string;
  [key: string]: unknown;
}

export interface DocumentUploadOptions {
  chunkSize: number;
  chunkOverlap: number;
  chunkingStrategy: ChunkingStrategy;
  embeddingModel: string;
  metadata?: Partial<SourceMetadata>;
  preserveFormatting?: boolean;
}

export interface DocumentUploadProgress {
  sourceId: string;
  stage: 'uploading' | 'extracting' | 'chunking' | 'embedding' | 'storing' | 'complete' | 'error';
  progress: number; // 0-100
  currentChunk?: number;
  totalChunks?: number;
  message?: string;
  error?: string;
}

export interface RAGSource {
  sourceId: string;
  sourceName: string;
  chunkId: string;
  content: string;
  relevance: number;
  metadata: ChunkMetadata;
}

export interface RAGRetrievalOptions {
  query: string;
  maxChunks: number;
  minRelevance: number;
  retrievalMethod: RetrievalMethod;
  reranking: boolean;
  filters?: RAGFilter[];
}

export interface RAGFilter {
  field: string;
  operator: 'equals' | 'contains' | 'in' | 'range';
  value: string | number | boolean | string[] | number[];
}

export interface RAGRetrievalResult {
  query: string;
  sources: RAGSource[];
  totalSources: number;
  retrievalTime: number;
  embeddingTime: number;
  rerankingTime?: number;
}

export interface EmbeddingProgress {
  sourceId: string;
  chunksProcessed: number;
  totalChunks: number;
  currentBatch: number;
  totalBatches: number;
  progress: number; // 0-100
  speed?: number; // chunks per second
  eta?: number; // seconds remaining
}

export interface VectorStoreStats {
  totalSources: number;
  totalChunks: number;
  totalVectors: number;
  storageSize: number; // bytes
  lastUpdated: Date;
}

export interface RetrievalStats {
  totalRetrievals: number;
  averageRelevance: number;
  averageRetrievalTime: number;
  popularSources: Array<{
    sourceId: string;
    sourceName: string;
    retrievalCount: number;
  }>;
}
