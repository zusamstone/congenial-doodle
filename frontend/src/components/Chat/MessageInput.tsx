import React, { useState, useRef, useEffect, type KeyboardEvent } from 'react';
import { Send, Square, Paperclip, Mic } from 'lucide-react';
import { Button } from '@/components/ui';
import { cn } from '@/utils/helpers';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  onStopGeneration?: () => void;
  isStreaming?: boolean;
  isLoading?: boolean;
  disabled?: boolean;
  placeholder?: string;
  maxLength?: number;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  onStopGeneration,
  isStreaming = false,
  isLoading = false,
  disabled = false,
  placeholder = 'Type your message... (Shift+Enter for new line, Enter to send)',
  maxLength = 10000,
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea as content grows
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  }, [message]);

  // Focus textarea on mount
  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  const handleSubmit = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || isLoading || disabled) return;

    onSendMessage(trimmedMessage);
    setMessage('');

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleStop = () => {
    if (onStopGeneration) {
      onStopGeneration();
    }
  };

  const characterCount = message.length;
  const isNearLimit = characterCount > maxLength * 0.9;
  const isOverLimit = characterCount > maxLength;

  return (
    <div className="border-t border-gray-700 bg-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="relative flex items-end gap-2">
          {/* Optional attachment button (for future file upload) */}
          <Button
            variant="ghost"
            size="icon"
            className="mb-2 text-gray-400 hover:text-gray-300"
            disabled={disabled || isLoading || isStreaming}
            title="Attach file (coming soon)"
          >
            <Paperclip className="w-5 h-5" />
          </Button>

          {/* Text input area */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={disabled || isLoading}
              maxLength={maxLength}
              rows={1}
              className={cn(
                'w-full px-4 py-3 bg-gray-800 text-gray-100 rounded-lg',
                'border border-gray-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500',
                'resize-none overflow-y-auto',
                'placeholder:text-gray-500',
                'disabled:opacity-50 disabled:cursor-not-allowed',
                'transition-colors',
                isOverLimit && 'border-red-500 focus:border-red-500 focus:ring-red-500'
              )}
            />

            {/* Character count */}
            {(isNearLimit || isOverLimit) && (
              <div
                className={cn(
                  'absolute bottom-1 right-2 text-xs',
                  isOverLimit ? 'text-red-400' : 'text-yellow-400'
                )}
              >
                {characterCount}/{maxLength}
              </div>
            )}
          </div>

          {/* Optional voice input button (for future feature) */}
          <Button
            variant="ghost"
            size="icon"
            className="mb-2 text-gray-400 hover:text-gray-300"
            disabled={disabled || isLoading || isStreaming}
            title="Voice input (coming soon)"
          >
            <Mic className="w-5 h-5" />
          </Button>

          {/* Send/Stop button */}
          {isStreaming ? (
            <Button
              variant="secondary"
              size="icon"
              onClick={handleStop}
              className="mb-2"
              title="Stop generation"
            >
              <Square className="w-5 h-5" />
            </Button>
          ) : (
            <Button
              variant="primary"
              size="icon"
              onClick={handleSubmit}
              disabled={!message.trim() || isLoading || disabled || isOverLimit}
              className="mb-2"
              title="Send message"
            >
              <Send className="w-5 h-5" />
            </Button>
          )}
        </div>

        {/* Helper text */}
        <div className="text-xs text-gray-500 mt-2 text-center">
          Press <kbd className="px-1 py-0.5 bg-gray-800 rounded">Enter</kbd> to send,{' '}
          <kbd className="px-1 py-0.5 bg-gray-800 rounded">Shift</kbd>+
          <kbd className="px-1 py-0.5 bg-gray-800 rounded">Enter</kbd> for new line
        </div>
      </div>
    </div>
  );
};
