import { useState, useEffect, useCallback } from 'react';
import type { Chat } from '@/types/chat';
import { api } from '@/utils/api';

interface UseChatListReturn {
  chats: Chat[];
  isLoading: boolean;
  error: string | null;
  createChat: (title?: string) => Promise<Chat | null>;
  deleteChat: (chatId: string) => Promise<void>;
  updateChat: (chatId: string, updates: Partial<Chat>) => Promise<void>;
  refreshChats: () => Promise<void>;
}

export const useChatList = (): UseChatListReturn => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadChats = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const fetchedChats = await api.get<Chat[]>('/chat');
      setChats(fetchedChats);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load chats';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadChats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const createChat = useCallback(async (title?: string): Promise<Chat | null> => {
    setError(null);

    try {
      const newChat = await api.post<Chat>('/chat', {
        title: title || 'New Chat',
      });
      setChats((prev) => [newChat, ...prev]);
      return newChat;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create chat';
      setError(errorMessage);
      return null;
    }
  }, []);

  const deleteChat = useCallback(async (chatId: string) => {
    setError(null);

    try {
      await api.delete(`/chat/${chatId}`);
      setChats((prev) => prev.filter((chat) => chat.id !== chatId));
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete chat';
      setError(errorMessage);
    }
  }, []);

  const updateChat = useCallback(async (chatId: string, updates: Partial<Chat>) => {
    setError(null);

    try {
      const updatedChat = await api.put<Chat>(`/chat/${chatId}`, updates);
      setChats((prev) =>
        prev.map((chat) => (chat.id === chatId ? updatedChat : chat))
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update chat';
      setError(errorMessage);
    }
  }, []);

  const refreshChats = useCallback(async () => {
    await loadChats();
  }, [loadChats]);

  return {
    chats,
    isLoading,
    error,
    createChat,
    deleteChat,
    updateChat,
    refreshChats,
  };
};
