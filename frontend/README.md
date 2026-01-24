# AI Studio Frontend

Modern React frontend for AI Studio built with Vite, TypeScript, and TailwindCSS.

## Tech Stack

- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS with dark mode support
- **Routing:** React Router DOM
- **UI Components:** Custom components with Lucide React icons
- **Code Editor:** Monaco Editor
- **Markdown:** React Markdown

## Project Structure

```
src/
├── components/      # React components
│   ├── ui/         # Reusable UI components
│   ├── chat/       # Chat-related components
│   ├── settings/   # Settings components
│   └── models/     # Model selection components
├── hooks/          # Custom React hooks
├── pages/          # Page components
├── styles/         # Global styles
├── types/          # TypeScript type definitions
└── utils/          # Utility functions
    ├── api.ts      # API client
    └── helpers.ts  # Helper functions
```

## Development

```bash
# Install dependencies
npm install

# Start dev server (runs on port 5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check
```

## Features

- ✅ TypeScript with strict type checking
- ✅ TailwindCSS with custom dark theme
- ✅ React Router for navigation
- ✅ API proxy to backend (/api -> http://localhost:3000)
- ✅ Path aliases (@/ -> ./src/)
- ✅ Custom scrollbar styles
- ✅ Theme persistence in localStorage

## Configuration

### Vite Config
- Dev server runs on port 5173
- API requests to `/api/*` are proxied to `http://localhost:3000`
- Path aliases configured for clean imports

### TailwindCSS
- Dark mode support using class strategy
- Custom color scheme with CSS variables
- Responsive design utilities
- Custom scrollbar styles

### TypeScript
- Strict mode enabled
- Path aliases configured
- Unused variables/parameters detection

