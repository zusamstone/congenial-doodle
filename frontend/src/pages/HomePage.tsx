import { useState } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { ChatInterface } from '@/components/Chat';
import { ModelSelector } from '@/components/Models';
import { Settings, Menu, X } from 'lucide-react';
import { Button } from '@/components/ui';
import { useModels } from '@/hooks';

export function HomePage() {
  const [currentChatId, setCurrentChatId] = useState<string | undefined>(undefined);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showModelSelector, setShowModelSelector] = useState(false);
  const { currentModel } = useModels();

  const handleSelectChat = (chatId: string) => {
    setCurrentChatId(chatId);
  };

  const handleNewChat = () => {
    setCurrentChatId(undefined);
  };

  return (
    <div className="h-screen flex overflow-hidden bg-gray-900 text-gray-100">
      {/* Sidebar */}
      {!sidebarCollapsed && (
        <Sidebar
          currentChatId={currentChatId}
          onSelectChat={handleSelectChat}
          onNewChat={handleNewChat}
        />
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <div className="flex items-center justify-between px-4 py-3 bg-gray-800 border-b border-gray-700">
          {/* Left side - Menu toggle and model selector */}
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              title={sidebarCollapsed ? 'Show sidebar' : 'Hide sidebar'}
            >
              {sidebarCollapsed ? <Menu className="w-5 h-5" /> : <X className="w-5 h-5" />}
            </Button>

            {/* Compact Model Selector */}
            <ModelSelector compact />
          </div>

          {/* Right side - Settings */}
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setShowModelSelector(!showModelSelector)}
              title="Model settings"
            >
              <Settings className="w-5 h-5" />
            </Button>
          </div>
        </div>

        {/* Chat Interface or Model Selector */}
        <div className="flex-1 overflow-hidden">
          {showModelSelector ? (
            <div className="h-full overflow-y-auto p-6">
              <div className="max-w-4xl mx-auto">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold">Model Selection</h2>
                  <Button
                    variant="ghost"
                    onClick={() => setShowModelSelector(false)}
                  >
                    Back to Chat
                  </Button>
                </div>
                <ModelSelector />
              </div>
            </div>
          ) : (
            <ChatInterface
              chatId={currentChatId}
              modelId={currentModel?.id}
            />
          )}
        </div>

        {/* Status Bar */}
        <div className="px-4 py-2 bg-gray-800 border-t border-gray-700 text-xs text-gray-400">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span>AI Studio v0.1.0</span>
              {currentModel && (
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                  {currentModel.name}
                </span>
              )}
            </div>
            <div>
              Ready
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
