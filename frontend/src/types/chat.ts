// Chat-related types
import type { RAGSource } from './rag';

export type MessageRole = 'user' | 'assistant' | 'system';

export type MessageStatus = 'sending' | 'sent' | 'error' | 'streaming';

export interface Message {
  id: string;
  chatId: string;
  role: MessageRole;
  content: string;
  thinkingContent?: string; // For thinking models
  tokens?: number;
  thinkingTokens?: number;
  createdAt: Date;
  updatedAt?: Date;
  pinned: boolean;
  metadata?: MessageMetadata;
  status?: MessageStatus;
}

export interface MessageMetadata {
  modelUsed?: string;
  temperature?: number;
  maxTokens?: number;
  stopReason?: string;
  ragSources?: RAGSource[];
  guidanceApplied?: boolean;
  error?: string;
}

export interface Chat {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
  folderId?: string;
  pinned: boolean;
  archived: boolean;
  tags: string[];
  modelId?: string;
  systemPromptId?: string;
  messageCount: number;
  tokenCount: number;
}

export interface ChatFolder {
  id: string;
  name: string;
  parentId?: string;
  icon?: string;
  color?: string;
  createdAt: Date;
}

export interface ChatSummary {
  id: string;
  chatId: string;
  summary: string;
  messageRange: {
    start: string;
    end: string;
  };
  tokens: number;
  createdAt: Date;
}

export interface StreamingChunk {
  type: 'token' | 'thinking' | 'complete' | 'error';
  token?: string;
  chatId: string;
  messageId: string;
  tokens?: number;
  thinkingTokens?: number;
  error?: string;
}

export interface ChatExportOptions {
  format: 'markdown' | 'json' | 'pdf' | 'html';
  includeSystemPrompt: boolean;
  includeMetadata: boolean;
  includeThinking: boolean;
  includeTimestamps: boolean;
  includeSources: boolean;
}
