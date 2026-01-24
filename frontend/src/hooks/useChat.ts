import { useState, useCallback, useRef, useEffect } from 'react';
import type { Chat, Message, StreamingChunk } from '@/types/chat';
import { api } from '@/utils/api';

interface UseChatOptions {
  chatId?: string;
  modelId?: string;
  systemPromptId?: string;
}

interface UseChatReturn {
  // State
  currentChat: Chat | null;
  messages: Message[];
  isStreaming: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  sendMessage: (content: string) => Promise<void>;
  regenerateMessage: (messageId: string) => Promise<void>;
  stopGeneration: () => void;
  loadChat: (chatId: string) => Promise<void>;
  createNewChat: (title?: string) => Promise<void>;
  deleteMessage: (messageId: string) => Promise<void>;
  pinMessage: (messageId: string, pinned: boolean) => Promise<void>;
  clearError: () => void;
}

export const useChat = (options: UseChatOptions = {}): UseChatReturn => {
  const [currentChat, setCurrentChat] = useState<Chat | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const streamingMessageRef = useRef<Message | null>(null);

  // Load chat messages when chatId changes
  useEffect(() => {
    if (options.chatId) {
      loadChat(options.chatId);
    }
  }, [options.chatId]);

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const loadChat = useCallback(async (chatId: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const [chat, chatMessages] = await Promise.all([
        api.get<Chat>(`/chat/${chatId}`),
        api.get<Message[]>(`/chat/${chatId}/messages`),
      ]);

      setCurrentChat(chat);
      setMessages(chatMessages);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load chat';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createNewChat = useCallback(async (title?: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const newChat = await api.post<Chat>('/chat', {
        title: title || 'New Chat',
        modelId: options.modelId,
        systemPromptId: options.systemPromptId,
      });

      setCurrentChat(newChat);
      setMessages([]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create chat';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [options.modelId, options.systemPromptId]);

  const sendMessage = useCallback(async (content: string) => {
    if (!currentChat) {
      await createNewChat();
      // Chat creation will trigger a re-render, send message after that
      return;
    }

    setError(null);
    setIsStreaming(true);

    // Create user message
    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      chatId: currentChat.id,
      role: 'user',
      content,
      createdAt: new Date(),
      pinned: false,
      status: 'sending',
    };

    setMessages((prev) => [...prev, userMessage]);

    // Initialize streaming assistant message
    const assistantMessage: Message = {
      id: `temp-streaming-${Date.now()}`,
      chatId: currentChat.id,
      role: 'assistant',
      content: '',
      createdAt: new Date(),
      pinned: false,
      status: 'streaming',
    };

    streamingMessageRef.current = assistantMessage;
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      // Connect to WebSocket for streaming
      const wsUrl = `ws://localhost:8000/api/chat/ws`;
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        ws.send(
          JSON.stringify({
            chatId: currentChat.id,
            message: content,
            modelId: options.modelId,
            systemPromptId: options.systemPromptId,
          })
        );
      };

      ws.onmessage = (event) => {
        const chunk: StreamingChunk = JSON.parse(event.data);

        if (chunk.type === 'token' && chunk.token && streamingMessageRef.current) {
          streamingMessageRef.current.content += chunk.token;
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === streamingMessageRef.current?.id
                ? { ...streamingMessageRef.current }
                : msg
            )
          );
        } else if (chunk.type === 'thinking' && chunk.token && streamingMessageRef.current) {
          if (!streamingMessageRef.current.thinkingContent) {
            streamingMessageRef.current.thinkingContent = '';
          }
          streamingMessageRef.current.thinkingContent += chunk.token;
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === streamingMessageRef.current?.id
                ? { ...streamingMessageRef.current }
                : msg
            )
          );
        } else if (chunk.type === 'complete') {
          if (streamingMessageRef.current) {
            streamingMessageRef.current.id = chunk.messageId;
            streamingMessageRef.current.status = 'sent';
            streamingMessageRef.current.tokens = chunk.tokens;
            streamingMessageRef.current.thinkingTokens = chunk.thinkingTokens;
          }
          setIsStreaming(false);
          ws.close();
        } else if (chunk.type === 'error') {
          setError(chunk.error || 'An error occurred during streaming');
          setIsStreaming(false);
          ws.close();
        }
      };

      ws.onerror = () => {
        setError('WebSocket connection error');
        setIsStreaming(false);
      };

      ws.onclose = () => {
        setIsStreaming(false);
        wsRef.current = null;
      };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      setIsStreaming(false);
    }
  }, [currentChat, options.modelId, options.systemPromptId]);

  const regenerateMessage = useCallback(async (messageId: string) => {
    if (!currentChat) return;

    setError(null);

    try {
      await api.post(`/chat/${currentChat.id}/regenerate`, { messageId });
      // Reload messages after regeneration
      await loadChat(currentChat.id);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to regenerate message';
      setError(errorMessage);
    }
  }, [currentChat, loadChat]);

  const stopGeneration = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      setIsStreaming(false);
    }
  }, []);

  const deleteMessage = useCallback(async (messageId: string) => {
    if (!currentChat) return;

    try {
      await api.delete(`/chat/${currentChat.id}/messages/${messageId}`);
      setMessages((prev) => prev.filter((msg) => msg.id !== messageId));
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete message';
      setError(errorMessage);
    }
  }, [currentChat]);

  const pinMessage = useCallback(async (messageId: string, pinned: boolean) => {
    if (!currentChat) return;

    try {
      await api.put(`/chat/${currentChat.id}/messages/${messageId}/pin`, { pinned });
      setMessages((prev) =>
        prev.map((msg) => (msg.id === messageId ? { ...msg, pinned } : msg))
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to pin message';
      setError(errorMessage);
    }
  }, [currentChat]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    currentChat,
    messages,
    isStreaming,
    isLoading,
    error,
    sendMessage,
    regenerateMessage,
    stopGeneration,
    loadChat,
    createNewChat,
    deleteMessage,
    pinMessage,
    clearError,
  };
};
