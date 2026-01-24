import React from 'react';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useChat } from '@/hooks';
import { Loader2, AlertCircle } from 'lucide-react';

interface ChatInterfaceProps {
  chatId?: string;
  modelId?: string;
  systemPromptId?: string;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  chatId,
  modelId,
  systemPromptId,
}) => {
  const {
    currentChat,
    messages,
    isStreaming,
    isLoading,
    error,
    sendMessage,
    regenerateMessage,
    stopGeneration,
    deleteMessage,
    pinMessage,
    clearError,
  } = useChat({ chatId, modelId, systemPromptId });

  return (
    <div className="flex flex-col h-full bg-gray-900">
      {/* Chat Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700 bg-gray-800">
        <div className="flex-1">
          <h1 className="text-xl font-semibold text-gray-100">
            {currentChat?.title || 'New Chat'}
          </h1>
          {currentChat && (
            <p className="text-sm text-gray-400 mt-1">
              {currentChat.messageCount || messages.length} messages • {currentChat.tokenCount || 0} tokens
            </p>
          )}
        </div>

        {/* Chat actions can go here (e.g., settings, export, etc.) */}
      </div>

      {/* Error Banner */}
      {error && (
        <div className="flex items-center gap-3 px-6 py-3 bg-red-900/20 border-b border-red-900/50">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
          <p className="text-sm text-red-300 flex-1">{error}</p>
          <button
            onClick={clearError}
            className="text-red-400 hover:text-red-300 text-sm font-medium"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Loading State */}
      {isLoading && !currentChat && (
        <div className="flex items-center justify-center h-full">
          <div className="flex flex-col items-center gap-3 text-gray-400">
            <Loader2 className="w-8 h-8 animate-spin" />
            <p>Loading chat...</p>
          </div>
        </div>
      )}

      {/* Messages Area */}
      {!isLoading && (
        <div className="flex-1 overflow-hidden">
          <MessageList
            messages={messages}
            isStreaming={isStreaming}
            onDeleteMessage={deleteMessage}
            onPinMessage={pinMessage}
            onRegenerateMessage={regenerateMessage}
          />
        </div>
      )}

      {/* Message Input */}
      <MessageInput
        onSendMessage={sendMessage}
        onStopGeneration={stopGeneration}
        isStreaming={isStreaming}
        isLoading={isLoading}
        disabled={isLoading}
      />
    </div>
  );
};
