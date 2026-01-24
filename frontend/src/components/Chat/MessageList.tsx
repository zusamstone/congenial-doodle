import React, { useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSanitize from 'rehype-sanitize';
import { Pin, Copy, Trash2, RotateCcw, ChevronDown, ChevronUp, Check } from 'lucide-react';
import type { Message } from '@/types/chat';
import { Button } from '@/components/ui';
import { cn } from '@/utils/helpers';

interface MessageListProps {
  messages: Message[];
  isStreaming: boolean;
  onDeleteMessage?: (messageId: string) => void;
  onPinMessage?: (messageId: string, pinned: boolean) => void;
  onRegenerateMessage?: (messageId: string) => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isStreaming,
  onDeleteMessage,
  onPinMessage,
  onRegenerateMessage,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const prevMessageCountRef = useRef<number>(0);
  const [expandedThinking, setExpandedThinking] = React.useState<Set<string>>(new Set());
  const [copiedId, setCopiedId] = React.useState<string | null>(null);

  // Auto-scroll to bottom when new messages arrive or while streaming
  useEffect(() => {
    const prevCount = prevMessageCountRef.current;
    const currentCount = messages.length;
    const hasNewMessage = currentCount > prevCount;

    if (!hasNewMessage && !isStreaming) {
      prevMessageCountRef.current = currentCount;
      return;
    }

    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    prevMessageCountRef.current = currentCount;
  }, [messages, isStreaming]);

  const copyToClipboard = (content: string, messageId: string) => {
    navigator.clipboard
      .writeText(content)
      .then(() => {
        setCopiedId(messageId);
        setTimeout(() => setCopiedId(null), 2000);
      })
      .catch((error) => {
        console.error('Failed to copy to clipboard:', error);
      });
  };

  const toggleThinking = (messageId: string) => {
    setExpandedThinking((prev) => {
      const next = new Set(prev);
      if (next.has(messageId)) {
        next.delete(messageId);
      } else {
        next.add(messageId);
      }
      return next;
    });
  };

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <div className="text-center">
          <p className="text-lg font-medium">No messages yet</p>
          <p className="text-sm mt-2">Start a conversation by typing a message below</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-y-auto px-4 py-6 space-y-6">
      {messages.map((message) => (
        <div
          key={message.id}
          className={cn(
            'flex flex-col gap-2 max-w-4xl',
            message.role === 'user' ? 'ml-auto items-end' : 'mr-auto items-start'
          )}
        >
          {/* Message Header */}
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <span className="font-medium">
              {message.role === 'user' ? 'You' : 'Assistant'}
            </span>
            {message.tokens && (
              <span className="text-xs">
                ({message.tokens} tokens
                {message.thinkingTokens && ` + ${message.thinkingTokens} thinking`})
              </span>
            )}
            {message.pinned && (
              <Pin className="w-3 h-3 text-blue-400" />
            )}
          </div>

          {/* Thinking Content (for thinking models) */}
          {message.thinkingContent && (
            <div className="w-full bg-gray-800/50 rounded-lg p-3 border border-gray-700">
              <button
                onClick={() => toggleThinking(message.id)}
                className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300 mb-2"
              >
                {expandedThinking.has(message.id) ? (
                  <ChevronUp className="w-4 h-4" />
                ) : (
                  <ChevronDown className="w-4 h-4" />
                )}
                <span className="font-medium">Thinking Process</span>
              </button>
              {expandedThinking.has(message.id) && (
                <div className="text-sm text-gray-300 whitespace-pre-wrap font-mono">
                  {message.thinkingContent}
                </div>
              )}
            </div>
          )}

          {/* Main Message Content */}
          <div
            className={cn(
              'rounded-lg px-4 py-3 max-w-full',
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-100 border border-gray-700'
            )}
          >
            {message.role === 'assistant' ? (
              <div className="prose prose-invert max-w-none">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeSanitize]}
                  components={{
                    code({ className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '');
                      const inline = !match;
                      const codeContent = String(children);
                      const codeId = `code-${message.id}-${codeContent.substring(0, 10)}`;
                      return inline ? (
                        <code className="bg-gray-900 px-1 py-0.5 rounded text-sm" {...props}>
                          {children}
                        </code>
                      ) : (
                        <div className="relative group">
                          <button
                            onClick={() => copyToClipboard(codeContent, codeId)}
                            className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity bg-gray-700 hover:bg-gray-600 p-1.5 rounded"
                            title={copiedId === codeId ? 'Copied!' : 'Copy code'}
                          >
                            {copiedId === codeId ? (
                              <Check className="w-4 h-4 text-green-400" />
                            ) : (
                              <Copy className="w-4 h-4" />
                            )}
                          </button>
                          <code className={className} {...props}>
                            {children}
                          </code>
                        </div>
                      );
                    },
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
            ) : (
              <p className="whitespace-pre-wrap">{message.content}</p>
            )}

            {/* Streaming indicator */}
            {message.status === 'streaming' && (
              <div className="flex items-center gap-2 mt-2 text-gray-400">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            )}

            {/* Error indicator */}
            {message.status === 'error' && (
              <div className="mt-2 text-red-400 text-sm">
                Error: {message.metadata?.error || 'Failed to send message'}
              </div>
            )}
          </div>

          {/* Message Actions */}
          {message.status !== 'streaming' && message.status !== 'sending' && (
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(message.content, message.id)}
                className={cn(
                  'text-gray-400 hover:text-gray-300',
                  copiedId === message.id && 'text-green-400'
                )}
                title={copiedId === message.id ? 'Copied!' : 'Copy message'}
              >
                {copiedId === message.id ? (
                  <Check className="w-4 h-4" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </Button>
              {onPinMessage && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onPinMessage(message.id, !message.pinned)}
                  className={cn(
                    'text-gray-400 hover:text-gray-300',
                    message.pinned && 'text-blue-400'
                  )}
                >
                  <Pin className="w-4 h-4" />
                </Button>
              )}
              {message.role === 'assistant' && onRegenerateMessage && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onRegenerateMessage(message.id)}
                  className="text-gray-400 hover:text-gray-300"
                >
                  <RotateCcw className="w-4 h-4" />
                </Button>
              )}
              {onDeleteMessage && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onDeleteMessage(message.id)}
                  className="text-gray-400 hover:text-red-400"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              )}
            </div>
          )}

          {/* RAG Sources */}
          {message.metadata?.ragSources && message.metadata.ragSources.length > 0 && (
            <div className="text-xs text-gray-400 mt-1">
              <span className="font-medium">Sources:</span>{' '}
              {message.metadata.ragSources.map((source, idx) => (
                <span key={idx}>
                  {source.sourceName}
                  {idx < (message.metadata?.ragSources?.length ?? 0) - 1 && ', '}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}

      {/* Scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  );
};
