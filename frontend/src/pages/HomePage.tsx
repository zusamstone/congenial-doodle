import { useTheme } from '@/hooks';
import { Button } from '@/components/ui';
import { Moon, Sun } from 'lucide-react';

export function HomePage() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="max-w-2xl w-full space-y-8 text-center">
        <h1 className="text-4xl font-bold tracking-tight">
          Welcome to AI Studio
        </h1>
        <p className="text-muted-foreground text-lg">
          Your intelligent assistant for creative work and problem-solving
        </p>
        
        <div className="flex justify-center gap-4 pt-8">
          <Button onClick={toggleTheme}>
            {theme === 'dark' ? (
              <>
                <Sun className="w-5 h-5 mr-2" />
                Light Mode
              </>
            ) : (
              <>
                <Moon className="w-5 h-5 mr-2" />
                Dark Mode
              </>
            )}
          </Button>
        </div>

        <div className="pt-12 space-y-2">
          <p className="text-sm text-muted-foreground">
            Powered by Vite + React + TypeScript
          </p>
          <div className="flex justify-center gap-4 text-xs text-muted-foreground">
            <span>✓ TailwindCSS</span>
            <span>✓ React Router</span>
            <span>✓ Monaco Editor</span>
            <span>✓ React Markdown</span>
          </div>
        </div>
      </div>
    </div>
  );
}
