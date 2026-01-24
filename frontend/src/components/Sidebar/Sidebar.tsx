import React, { useState } from 'react';
import { Plus, MessageSquare, Search, Trash2, Pin, Archive } from 'lucide-react';
import { useChatList } from '@/hooks';
import { Button } from '@/components/ui';
import { cn } from '@/utils/helpers';
import type { Chat } from '@/types/chat';

interface SidebarProps {
  currentChatId?: string;
  onSelectChat: (chatId: string) => void;
  onNewChat: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentChatId,
  onSelectChat,
  onNewChat,
}) => {
  const { chats, isLoading, createChat, deleteChat, updateChat } = useChatList();
  const [searchQuery, setSearchQuery] = useState('');
  const [showArchived, setShowArchived] = useState(false);

  const handleNewChat = async () => {
    const newChat = await createChat();
    if (newChat) {
      onNewChat();
      onSelectChat(newChat.id);
    }
  };

  const handleDeleteChat = async (chatId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this chat?')) {
      await deleteChat(chatId);
      if (currentChatId === chatId) {
        onNewChat();
      }
    }
  };

  const handlePinChat = async (chat: Chat, e: React.MouseEvent) => {
    e.stopPropagation();
    await updateChat(chat.id, { pinned: !chat.pinned });
  };

  const handleArchiveChat = async (chat: Chat, e: React.MouseEvent) => {
    e.stopPropagation();
    await updateChat(chat.id, { archived: !chat.archived });
  };

  // Filter chats
  const filteredChats = chats.filter((chat) => {
    const matchesSearch = chat.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesArchiveFilter = showArchived ? chat.archived : !chat.archived;
    return matchesSearch && matchesArchiveFilter;
  });

  // Sort chats: pinned first, then by updatedAt
  const sortedChats = [...filteredChats].sort((a, b) => {
    if (a.pinned && !b.pinned) return -1;
    if (!a.pinned && b.pinned) return 1;
    return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
  });

  return (
    <div className="flex flex-col h-full w-80 bg-gray-800 border-r border-gray-700">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-gray-700">
        <Button
          variant="primary"
          className="w-full justify-center gap-2"
          onClick={handleNewChat}
        >
          <Plus className="w-5 h-5" />
          New Chat
        </Button>

        {/* Search */}
        <div className="mt-3 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-gray-900 border border-gray-700 rounded-lg text-sm text-gray-100 placeholder:text-gray-500 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
          />
        </div>

        {/* Archive Toggle */}
        <div className="mt-3 flex items-center gap-2 text-sm">
          <button
            onClick={() => setShowArchived(!showArchived)}
            className={cn(
              'flex items-center gap-2 px-3 py-1.5 rounded-lg transition-colors',
              showArchived
                ? 'bg-blue-600 text-white'
                : 'text-gray-400 hover:bg-gray-700 hover:text-gray-300'
            )}
          >
            <Archive className="w-4 h-4" />
            Archived
          </button>
        </div>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex items-center justify-center h-32 text-gray-500">
            <p className="text-sm">Loading chats...</p>
          </div>
        ) : sortedChats.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-32 text-gray-500 px-4">
            <MessageSquare className="w-8 h-8 mb-2 opacity-50" />
            <p className="text-sm text-center">
              {searchQuery
                ? 'No chats found'
                : showArchived
                ? 'No archived chats'
                : 'No chats yet'}
            </p>
          </div>
        ) : (
          <div className="py-2">
            {sortedChats.map((chat) => (
              <ChatItem
                key={chat.id}
                chat={chat}
                isActive={chat.id === currentChatId}
                onSelect={() => onSelectChat(chat.id)}
                onDelete={(e) => handleDeleteChat(chat.id, e)}
                onPin={(e) => handlePinChat(chat, e)}
                onArchive={(e) => handleArchiveChat(chat, e)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-gray-700">
        <div className="text-xs text-gray-500 text-center">
          {chats.filter(c => !c.archived).length} active chat{chats.filter(c => !c.archived).length !== 1 ? 's' : ''}
          {chats.filter(c => c.archived).length > 0 &&
            ` • ${chats.filter(c => c.archived).length} archived`
          }
        </div>
      </div>
    </div>
  );
};

// Chat Item Component
interface ChatItemProps {
  chat: Chat;
  isActive: boolean;
  onSelect: () => void;
  onDelete: (e: React.MouseEvent) => void;
  onPin: (e: React.MouseEvent) => void;
  onArchive: (e: React.MouseEvent) => void;
}

const ChatItem: React.FC<ChatItemProps> = ({
  chat,
  isActive,
  onSelect,
  onDelete,
  onPin,
  onArchive,
}) => {
  const [showActions, setShowActions] = useState(false);

  const formatDate = (date: Date) => {
    const now = new Date();
    const chatDate = new Date(date);
    const diffInHours = (now.getTime() - chatDate.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return chatDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffInHours < 48) {
      return 'Yesterday';
    } else if (diffInHours < 168) {
      return chatDate.toLocaleDateString([], { weekday: 'short' });
    } else {
      return chatDate.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  };

  return (
    <div
      onClick={onSelect}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
      className={cn(
        'group relative px-3 py-2 mx-2 rounded-lg cursor-pointer transition-colors',
        isActive
          ? 'bg-blue-600 text-white'
          : 'text-gray-300 hover:bg-gray-700'
      )}
    >
      <div className="flex items-start gap-2">
        {/* Chat Icon */}
        <MessageSquare className="w-4 h-4 mt-1 flex-shrink-0" />

        {/* Chat Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-medium truncate">{chat.title}</h3>
            {chat.pinned && (
              <Pin className="w-3 h-3 flex-shrink-0" />
            )}
          </div>
          <p className="text-xs opacity-70 mt-0.5">
            {formatDate(chat.updatedAt)} • {chat.messageCount} msgs
          </p>
          {chat.tags && chat.tags.length > 0 && (
            <div className="flex gap-1 mt-1 flex-wrap">
              {chat.tags.slice(0, 2).map((tag) => (
                <span
                  key={tag}
                  className="text-xs px-1.5 py-0.5 bg-gray-700/50 rounded"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Actions */}
        {showActions && (
          <div className="flex items-center gap-1">
            <button
              onClick={onPin}
              className={cn(
                'p-1 rounded hover:bg-gray-600 transition-colors',
                chat.pinned && 'text-blue-400'
              )}
              title={chat.pinned ? 'Unpin' : 'Pin'}
            >
              <Pin className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onArchive}
              className="p-1 rounded hover:bg-gray-600 transition-colors"
              title={chat.archived ? 'Unarchive' : 'Archive'}
            >
              <Archive className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={onDelete}
              className="p-1 rounded hover:bg-red-600 transition-colors"
              title="Delete"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
