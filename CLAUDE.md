# CLAUDE.md - AI Assistant Guide for AI Studio

> **Purpose**: This document provides comprehensive guidance for AI assistants (like Claude) working with the AI Studio codebase. It covers project structure, development workflows, conventions, and best practices.

**Last Updated**: 2026-01-24
**Project**: AI Studio - Local-First AI Chat Application
**Repository**: https://github.com/zusamstone/congenial-doodle

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Reference](#quick-reference)
3. [Repository Structure](#repository-structure)
4. [Technology Stack](#technology-stack)
5. [Development Workflows](#development-workflows)
6. [Code Organization & Conventions](#code-organization--conventions)
7. [Common Tasks & Patterns](#common-tasks--patterns)
8. [Testing & Validation](#testing--validation)
9. [Git Workflow](#git-workflow)
10. [Important Constraints](#important-constraints)
11. [AI Assistant Best Practices](#ai-assistant-best-practices)

---

## Project Overview

### What is AI Studio?

AI Studio is a **privacy-focused, local-first desktop AI chat application** built with:
- **Frontend**: React 19 + TypeScript + Vite + TailwindCSS
- **Desktop**: Electron 40
- **Backend**: Python 3.11+ + FastAPI + llama.cpp

### Core Features

- **Multi-Model Support**: Local models (llama.cpp/GGUF) + Cloud APIs (OpenAI, Anthropic, Google, Ollama)
- **RAG**: Document upload, embedding, and retrieval via ChromaDB
- **Context Management**: 4 strategies (smart summarization, rolling window, periodic, manual)
- **System Prompts Library**: Pre-configured personas and instructions
- **LoRA Support**: Load/manage LoRA adapters for local models
- **Thinking Models**: Special support for reasoning models (o1, o3, DeepSeek R1)
- **Resource Monitoring**: Real-time CPU/GPU/RAM/VRAM tracking
- **Portable by Default**: All data in app directory, no external dependencies

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (React/TypeScript)                            │
│  - Vite dev server: http://localhost:5173              │
│  - API proxy: /api/* → http://localhost:8000           │
└─────────────────────────────────────────────────────────┘
                         ↕ IPC
┌─────────────────────────────────────────────────────────┐
│  Electron Main Process                                  │
│  - Window management, Python process spawning          │
│  - IPC bridge between renderer and backend             │
└─────────────────────────────────────────────────────────┘
                    ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────┐
│  Backend (Python/FastAPI)                               │
│  - REST API: http://localhost:8000                     │
│  - WebSocket streaming for chat                        │
│  - llama.cpp for local inference                       │
│  - ChromaDB for embeddings, SQLite for metadata        │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Reference

### Essential Commands

```bash
# Installation
npm run install-all              # Install all dependencies (frontend, electron, backend)

# Development
npm run dev                      # Start all services (frontend + backend + electron)
npm run dev:frontend             # Frontend only (Vite on :5173)
npm run dev:backend              # Backend only (FastAPI on :8000)
npm run dev:electron             # Electron only

# Building
npm run build                    # Build frontend + electron
npm run build:frontend           # Build frontend only
npm run build:electron           # Build electron only

# Packaging
npm run package:win              # Package for Windows (portable .exe)
npm run package:mac              # Package for macOS (.app)
npm run package:linux            # Package for Linux (AppImage)
npm run package:all              # Package for all platforms

# Testing & Linting
npm run test                     # Run all tests (frontend + backend)
npm run lint                     # Lint frontend code
cd backend && pytest             # Run backend tests only
cd backend && black .            # Format Python code
cd backend && ruff check .       # Lint Python code
cd frontend && npm run lint:fix  # Auto-fix frontend linting
```

### Key Files

| File | Purpose |
|------|---------|
| `package.json` | Root workspace config, npm scripts |
| `frontend/src/App.tsx` | React root component, routing |
| `frontend/vite.config.ts` | Vite config (port 5173, API proxy) |
| `electron/main.js` | Electron main process, Python spawning |
| `electron/preload.js` | IPC bridge (context isolation) |
| `backend/main.py` | FastAPI app entry point |
| `backend/requirements.txt` | Python dependencies |
| `backend/database/models.py` | SQLAlchemy ORM models |
| `backend/api/routes/*.py` | API endpoint definitions |
| `config/default_settings.json` | Default application settings |
| `ARCHITECTURE.md` | System architecture documentation |
| `docs/DEVELOPER_GUIDE.md` | Development setup and patterns |
| `docs/CONTRIBUTING.md` | Contribution guidelines |

### Key Directories

```
congenial-doodle/
├── frontend/          # React + TypeScript UI
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── pages/        # Page components
│   │   ├── types/        # TypeScript interfaces
│   │   └── utils/        # Helper functions, API client
│   └── package.json
│
├── backend/           # Python FastAPI server
│   ├── api/routes/       # API endpoints
│   ├── database/         # SQLAlchemy models, DB setup
│   ├── models/           # Model management, inference
│   ├── embeddings/       # RAG, ChromaDB
│   ├── utils/            # Config, hardware detection
│   └── requirements.txt
│
├── electron/          # Electron desktop wrapper
│   ├── main.js           # Main process
│   ├── preload.js        # IPC bridge
│   └── package.json
│
├── config/            # Default configurations
│   ├── default_settings.json
│   ├── system_prompt_templates.json
│   ├── guidance_presets.json
│   └── model_configs.json
│
├── docs/              # Documentation
│   ├── DEVELOPER_GUIDE.md
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── USER_GUIDE.md
│
└── data/              # Runtime data (gitignored)
    ├── models/           # Downloaded GGUF models
    ├── loras/            # LoRA adapters
    ├── vector_store/     # ChromaDB embeddings
    ├── database/         # SQLite databases
    └── uploads/          # User uploaded files
```

---

## Repository Structure

### Frontend (`frontend/`)

**React 19 + TypeScript + Vite**

- **Entry Point**: `src/main.tsx` → mounts `App.tsx`
- **Routing**: React Router v7 (routes defined in `App.tsx`)
- **State Management**: React Context + Custom Hooks (no Redux)
- **Styling**: TailwindCSS 4.1 (utility-first)
- **API Communication**: `utils/api.ts` (ApiClient class)
- **Build**: Vite 7.2.4 (dev server :5173, proxy `/api/*` → `:8000`)

**Key Contexts**:
- `ChatContext`: Current chat, messages, streaming state
- `ModelsContext`: Available models, current model, loading state
- `SettingsContext`: User settings, preferences
- `RAGContext`: Knowledge base, retrieval settings

**Component Structure**:
```
components/
├── Chat/              # Chat interface components
├── Sidebar/           # Navigation components
├── Models/            # Model management UI
├── Settings/          # Settings panels
├── KnowledgeBase/     # RAG UI
├── SystemPrompts/     # Prompt library UI
└── Monitoring/        # Resource monitoring UI
```

### Backend (`backend/`)

**Python 3.11+ + FastAPI**

- **Entry Point**: `main.py` (FastAPI app with lifespan context)
- **Server**: Uvicorn ASGI (localhost:8000)
- **Database**: SQLite + SQLAlchemy 2.0 (async)
- **Inference**: llama-cpp-python (local), SDK clients (cloud APIs)
- **Embeddings**: ChromaDB + sentence-transformers
- **Logging**: Loguru (logs in `data/logs/`)

**API Routes** (`api/routes/`):
- `chat.py`: Chat/message endpoints, streaming
- `models.py`: Model management, loading/unloading
- `embeddings.py`: RAG endpoints, document upload
- `lora.py`: LoRA adapter management
- `system_prompts.py`: System prompt library

**Service Layers**:
- `models/model_manager.py`: Model lifecycle, LRU cache
- `models/inference_engine.py`: llama.cpp wrapper
- `models/api_providers.py`: OpenAI/Anthropic/Google clients
- `embeddings/vector_store.py`: ChromaDB wrapper
- `database/db.py`: Async SQLAlchemy setup

### Electron (`electron/`)

**Electron 40**

- **Main Process** (`main.js`): Window management, Python spawning, IPC handlers
- **Preload Script** (`preload.js`): Context-isolated IPC bridge
- **Security**: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`
- **Python Process**: Spawned on startup, health checks every 3s
- **IPC Channels**: 15+ handlers for settings, files, window controls, app info

**Exposed APIs** (via `contextBridge`):
```javascript
window.electronAPI = {
  settings: { get, set, getAll, reset },
  file: { select, selectFolder, saveDialog },
  system: { getDataDir, openExternal, showItemInFolder },
  window: { minimize, maximize, close },
  app: { getVersion, getPath },
  backend: { request, onReady }
}
```

### Configuration (`config/`)

**JSON Configuration Files**:
- `default_settings.json`: Default UI/sampling settings
- `system_prompt_templates.json`: Pre-built system prompts
- `guidance_presets.json`: Guidance configuration presets
- `model_configs.json`: Model metadata and recommended settings

**Settings Priority**: User settings → Default settings → Hardcoded defaults

---

## Technology Stack

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2 | UI framework |
| TypeScript | 5.9 | Type safety |
| Vite | 7.2.4 | Build tool, dev server |
| TailwindCSS | 4.1 | Styling |
| React Router | 7.13 | Client-side routing |
| Monaco Editor | 4.7 | Code display |
| React Markdown | 10.1 | Markdown rendering |
| Lucide React | 0.563 | Icon library |
| ESLint | Latest | Linting |

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Backend language |
| FastAPI | 0.109.1 | Web framework |
| Uvicorn | 0.27 | ASGI server |
| SQLAlchemy | 2.0.25 | ORM (async) |
| aiosqlite | 0.19 | Async SQLite driver |
| Pydantic | 2.5.3 | Validation |
| llama-cpp-python | 0.2.27 | Local inference |
| ChromaDB | 0.4.22 | Vector database |
| sentence-transformers | 2.3.1 | Embeddings |
| tiktoken | 0.5.2 | Token counting |
| OpenAI SDK | 1.10 | OpenAI API |
| Anthropic SDK | 0.8.1 | Claude API |
| Google GenAI | 0.3.2 | Gemini API |
| PyPDF2 | 3.0.1 | PDF extraction |
| python-docx | 1.1 | DOCX extraction |
| Loguru | 0.7.2 | Logging |
| psutil | 5.9.8 | System monitoring |

### Desktop Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Electron | 40.0 | Desktop framework |
| electron-builder | 24.9.1 | Packaging |
| electron-store | 8.1 | Persistent storage |

---

## Development Workflows

### Initial Setup

```bash
# 1. Clone repository
git clone https://github.com/zusamstone/congenial-doodle.git
cd congenial-doodle

# 2. Install all dependencies
npm run install-all

# 3. Create backend .env file (optional)
cd backend
cp .env.example .env
# Edit .env with API keys if needed

# 4. Start development servers
cd ..
npm run dev
```

### Development Mode

**All services** (recommended):
```bash
npm run dev
# Starts:
# - Frontend (Vite): http://localhost:5173
# - Backend (FastAPI): http://localhost:8000
# - Electron: Opens desktop app
```

**Individual services**:
```bash
# Terminal 1: Backend
npm run dev:backend

# Terminal 2: Frontend
npm run dev:frontend

# Terminal 3: Electron
npm run dev:electron
```

### Hot Reload Behavior

- **Frontend**: Vite HMR (instant updates on file save)
- **Backend**: Uvicorn auto-reload (restarts on Python file changes)
- **Electron**: Requires manual restart for `main.js` changes

### API Access Points

- **Frontend Dev Server**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Environment Variables

**Backend** (`.env` in `backend/`):
```bash
# Server
HOST=127.0.0.1
PORT=8000
DEBUG=true

# Paths (portable mode)
DATA_DIR=./data
MODELS_DIR=./data/models

# API Keys (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Hardware
DEFAULT_GPU_LAYERS=0        # 0 = CPU only, -1 = all layers
DEFAULT_THREADS=4

# Logging
LOG_LEVEL=INFO
LOG_FILE=./data/logs/ai_studio.log
```

---

## Code Organization & Conventions

### Naming Conventions

**Python** (PEP 8):
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

**TypeScript/React**:
- Component files: `PascalCase.tsx`
- Utility files: `camelCase.ts`
- Components: `PascalCase`
- Functions/variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Interfaces: `PascalCase` (no `I` prefix)
- Types: `PascalCase`

### File Organization

**Frontend**:
```typescript
// Import order (ESLint enforced):
// 1. External libraries
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

// 2. Internal absolute imports (@/)
import { Button } from '@/components/ui';
import { useChat } from '@/hooks';
import { Chat } from '@/types';

// 3. Relative imports
import { formatDate } from './utils';
import styles from './Component.module.css';

// Component definition
export const MyComponent: React.FC<Props> = ({ ... }) => {
  // Hook calls first
  const [state, setState] = useState();
  const navigate = useNavigate();

  // Event handlers
  const handleClick = () => { ... };

  // Render
  return <div>...</div>;
};
```

**Backend**:
```python
# Import order (isort/black enforced):
# 1. Standard library
import os
from typing import List, Optional

# 2. Third-party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# 3. Local
from database.db import get_db
from database.models import Chat, Message
from utils.config import settings

# Router/app definition
router = APIRouter()

# Route handlers
@router.get("/", response_model=List[ChatResponse])
async def get_chats(db: AsyncSession = Depends(get_db)):
    """Get all chats."""
    # Implementation
```

### TypeScript Type Definitions

**Key Types** (in `frontend/src/types/`):

```typescript
// chat.ts
interface Message {
  id: string;
  chatId: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  thinkingContent?: string;
  tokens?: number;
  thinkingTokens?: number;
  createdAt: Date;
  pinned: boolean;
  metadata?: MessageMetadata;
  status?: 'sending' | 'sent' | 'error' | 'streaming';
}

interface Chat {
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
}

// models.ts
interface Model {
  id: string;
  name: string;
  provider: 'local' | 'openai' | 'anthropic' | 'google' | 'ollama';
  modelId: string;
  contextLength: number;
  maxTokens: number;
  parameters?: string; // "7B", "70B"
  loaded: boolean;
  thinkingModel: boolean;
  supportsVision?: boolean;
  supportsFunctions?: boolean;
}

// settings.ts
interface Settings {
  userMode: 'general' | 'power' | 'developer';
  theme: 'dark' | 'light' | 'system';
  contextStrategy: 'smart_summarization' | 'rolling_window' | 'periodic_summary' | 'manual';
  sampling: SamplingSettings;
  rag: RAGSettings;
  // ... more settings
}
```

### Python Pydantic Models

**API Models** (in `backend/api/routes/*.py`):

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MessageCreate(BaseModel):
    chat_id: Optional[int] = None
    message: str
    model_id: Optional[int] = None
    system_prompt_id: Optional[int] = None
    settings: Optional[dict] = None

class MessageResponse(BaseModel):
    id: int
    chat_id: int
    role: str
    content: str
    thinking_content: Optional[str] = None
    tokens: Optional[int] = None
    created_at: datetime
    pinned: bool
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True  # For SQLAlchemy models
```

### Database Models (SQLAlchemy)

**ORM Models** (`backend/database/models.py`):

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.db import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), index=True)
    folder_id = Column(Integer, ForeignKey("folders.id"), index=True)
    pinned = Column(Boolean, default=False, index=True)
    archived = Column(Boolean, default=False)
    tags = Column(JSON)  # List[str]
    model_id = Column(Integer, ForeignKey("models.id"))

    # Relationships
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    folder = relationship("Folder", back_populates="chats")
    model = relationship("Model", back_populates="chats")
```

---

## Common Tasks & Patterns

### Adding a New API Endpoint

**1. Create Pydantic models** (`backend/api/routes/my_feature.py`):

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        from_attributes = True

@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new item."""
    # Implementation
    return new_item
```

**2. Register router** (`backend/main.py`):

```python
from api.routes import my_feature

app.include_router(
    my_feature.router,
    prefix="/api/my-feature",
    tags=["my-feature"]
)
```

**3. Add database model if needed** (`backend/database/models.py`):

```python
class MyFeature(Base):
    __tablename__ = "my_features"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

**4. Test endpoint**:

```bash
curl http://localhost:8000/api/my-feature/items
# Or visit http://localhost:8000/docs
```

### Adding a Frontend Component

**1. Create component** (`frontend/src/components/MyFeature.tsx`):

```typescript
import React, { useState } from 'react';

interface MyFeatureProps {
  title: string;
  onAction: (value: string) => void;
}

export const MyFeature: React.FC<MyFeatureProps> = ({ title, onAction }) => {
  const [value, setValue] = useState('');

  const handleSubmit = () => {
    onAction(value);
  };

  return (
    <div className="p-4 bg-gray-800 rounded-lg">
      <h2 className="text-xl font-bold mb-4">{title}</h2>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full p-2 bg-gray-700 rounded"
      />
      <button onClick={handleSubmit} className="mt-2 px-4 py-2 bg-blue-600 rounded">
        Submit
      </button>
    </div>
  );
};
```

**2. Add types** (`frontend/src/types/myFeature.ts`):

```typescript
export interface MyFeatureData {
  id: number;
  name: string;
  description?: string;
}
```

**3. Create API hook** (`frontend/src/hooks/useMyFeature.ts`):

```typescript
import { useState, useEffect } from 'react';
import { api } from '@/utils/api';
import { MyFeatureData } from '@/types/myFeature';

export const useMyFeature = () => {
  const [data, setData] = useState<MyFeatureData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.get<MyFeatureData[]>('/my-feature/items');
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { data, loading, error, refetch: fetchData };
};
```

**4. Use in page**:

```typescript
import { MyFeature } from '@/components/MyFeature';
import { useMyFeature } from '@/hooks/useMyFeature';

export const MyPage = () => {
  const { data, loading, error } = useMyFeature();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <MyFeature
      title="My Feature"
      onAction={(value) => console.log(value)}
    />
  );
};
```

### Database Operations Pattern

**Create**:
```python
async def create_chat(db: AsyncSession, title: str) -> Chat:
    chat = Chat(title=title)
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat
```

**Read**:
```python
from sqlalchemy import select

async def get_chat(db: AsyncSession, chat_id: int) -> Chat | None:
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id)
    )
    return result.scalar_one_or_none()

async def get_all_chats(db: AsyncSession) -> List[Chat]:
    result = await db.execute(
        select(Chat).order_by(Chat.updated_at.desc())
    )
    return result.scalars().all()
```

**Update**:
```python
async def update_chat(db: AsyncSession, chat_id: int, title: str) -> Chat | None:
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    if chat:
        chat.title = title
        await db.commit()
        await db.refresh(chat)
    return chat
```

**Delete**:
```python
async def delete_chat(db: AsyncSession, chat_id: int) -> bool:
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id)
    )
    chat = result.scalar_one_or_none()
    if chat:
        await db.delete(chat)
        await db.commit()
        return True
    return False
```

### Error Handling Patterns

**Backend**:
```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input"
)

# 404 Not Found
if not item:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item {item_id} not found"
    )

# 500 Internal Server Error
try:
    # Risky operation
    result = await dangerous_operation()
except Exception as e:
    logger.error(f"Error in operation: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )
```

**Frontend**:
```typescript
try {
  const data = await api.post('/endpoint', payload);
  setData(data);
} catch (error) {
  if (error instanceof Error) {
    setError(error.message);
  } else {
    setError('An unknown error occurred');
  }
  console.error('API error:', error);
}
```

### Streaming Pattern (WebSocket)

**Backend** (`backend/api/routes/chat.py`):
```python
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()

            # Stream tokens
            async for token in generate_response(data['message']):
                await websocket.send_json({
                    "type": "token",
                    "token": token,
                    "chatId": data['chatId']
                })

            # Send completion
            await websocket.send_json({
                "type": "complete",
                "chatId": data['chatId']
            })

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011)
```

**Frontend**:
```typescript
const ws = new WebSocket('ws://localhost:8000/api/chat/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({ chatId, message, model }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'token') {
    appendToken(data.token);
  } else if (data.type === 'complete') {
    finalizeMessage();
  } else if (data.type === 'error') {
    showError(data.error);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket closed');
};
```

---

## Testing & Validation

### Backend Testing (pytest)

**Test Structure**:
```
backend/
├── tests/
│   ├── conftest.py           # Fixtures
│   ├── test_api/
│   │   ├── test_chat.py
│   │   └── test_models.py
│   ├── test_services/
│   └── test_utils/
└── pytest.ini
```

**Example Test** (`backend/tests/test_api/test_chat.py`):
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_chat():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/chat/",
            json={"title": "Test Chat"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Test Chat"

@pytest.mark.asyncio
async def test_get_chats():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/chat/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
```

**Fixtures** (`backend/conftest.py`):
```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from database.models import Base

@pytest.fixture
async def test_db():
    """Create in-memory test database."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    await engine.dispose()
```

**Running Tests**:
```bash
cd backend
pytest                    # All tests
pytest -v                 # Verbose
pytest tests/test_api/    # Specific directory
pytest --cov              # With coverage
pytest -k "test_chat"     # Tests matching pattern
```

### Frontend Testing (Jest + React Testing Library)

**Example Test** (`frontend/src/components/MyComponent.test.tsx`):
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './MyComponent';

describe('MyComponent', () => {
  it('renders with title', () => {
    render(<MyComponent title="Test" onAction={() => {}} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onAction when button clicked', () => {
    const onAction = jest.fn();
    render(<MyComponent title="Test" onAction={onAction} />);

    const button = screen.getByRole('button');
    fireEvent.click(button);

    expect(onAction).toHaveBeenCalled();
  });

  it('updates value on input change', () => {
    render(<MyComponent title="Test" onAction={() => {}} />);

    const input = screen.getByRole('textbox');
    fireEvent.change(input, { target: { value: 'new value' } });

    expect(input).toHaveValue('new value');
  });
});
```

**Running Tests**:
```bash
cd frontend
npm run test              # Run tests
npm run test:watch        # Watch mode
npm run test:coverage     # With coverage
```

### Code Quality Checks

**Python** (run before committing):
```bash
cd backend
black .                   # Format code
ruff check .              # Lint
ruff check --fix .        # Auto-fix linting
mypy .                    # Type checking (if configured)
pytest                    # Run tests
```

**TypeScript** (run before committing):
```bash
cd frontend
npm run lint              # Check linting
npm run lint:fix          # Auto-fix linting
npm run type-check        # TypeScript compilation check
npm run test              # Run tests
npm run build             # Ensure builds successfully
```

### Pre-Commit Checklist

Before creating a commit, ensure:
- [ ] Code is formatted (black, prettier)
- [ ] No linting errors (ruff, eslint)
- [ ] All tests pass (pytest, jest)
- [ ] TypeScript compiles without errors
- [ ] No console errors in browser (for frontend changes)
- [ ] API endpoints work (test via /docs or curl)
- [ ] No sensitive data in code (API keys, passwords)

---

## Git Workflow

### Branching Strategy

**Branch Types**:
- `main`: Production-ready code
- `feature/*`: New features (`feature/add-dark-mode`)
- `fix/*`: Bug fixes (`fix/chat-crash`)
- `docs/*`: Documentation (`docs/update-readme`)
- `refactor/*`: Code refactoring (`refactor/cleanup-api`)
- `test/*`: Test additions (`test/add-chat-tests`)

### Commit Message Convention

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Code change (no bug fix or feature)
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance (deps, build, etc.)
- `ci`: CI/CD changes

**Scopes** (optional):
- `api`: Backend API
- `ui`: Frontend UI
- `db`: Database
- `rag`: RAG/embeddings
- `models`: Model management
- `chat`: Chat functionality

**Examples**:
```bash
feat(chat): add message pinning functionality
fix(api): resolve context limit calculation error
docs: update RAG setup guide
refactor(db): simplify query builder logic
test(chat): add unit tests for message handlers
chore(deps): update dependencies
```

### Development Workflow

**1. Sync with upstream**:
```bash
git checkout main
git pull origin main
```

**2. Create feature branch**:
```bash
git checkout -b feature/my-feature
```

**3. Make changes and commit**:
```bash
# Make changes
git add .
git commit -m "feat(scope): add feature"

# Or for multiple logical changes
git add file1.py
git commit -m "feat(api): add endpoint"
git add file2.tsx
git commit -m "feat(ui): add component"
```

**4. Push to remote**:
```bash
git push -u origin feature/my-feature
```

**5. Create Pull Request** on GitHub

**6. After PR merged, clean up**:
```bash
git checkout main
git pull origin main
git branch -d feature/my-feature
```

### Database Migrations

**Current Process** (no Alembic yet):
1. Modify model in `backend/database/models.py`
2. Delete database: `rm data/database/ai_studio.db`
3. Restart server (auto-creates new schema)

**⚠️ Note**: This is development-only. Production will use Alembic migrations.

---

## Important Constraints

### What to AVOID

**❌ Don't**:
1. **Commit secrets**: No API keys, passwords, or tokens in code
2. **Skip type hints**: Always use TypeScript types and Python type hints
3. **Use `any` in TypeScript**: Use `unknown` and type guards instead
4. **Ignore linting**: Fix linting errors before committing
5. **Break API compatibility**: Coordinate breaking changes
6. **Hardcode paths**: Use portable path helpers (`utils/portable_paths.py`)
7. **Skip error handling**: Always handle errors gracefully
8. **Use `console.log` in production**: Use proper logging
9. **Forget to test**: Write tests for new features
10. **Push directly to main**: Always use feature branches and PRs

### Security Best Practices

**Electron**:
- Keep `contextIsolation: true`
- Keep `nodeIntegration: false`
- Keep `sandbox: true`
- Only expose necessary APIs via `contextBridge`
- Validate all IPC inputs

**Backend**:
- Use Pydantic for input validation
- Never trust user input (validate, sanitize)
- Use parameterized queries (SQLAlchemy ORM)
- Encrypt API keys at rest
- Use HTTPS in production

**Frontend**:
- Sanitize user input before rendering
- Use CSP (Content Security Policy)
- No inline scripts in production
- Validate data from API

### Performance Considerations

**Frontend**:
- Use React.memo for expensive components
- Virtual scrolling for long lists (message history)
- Debounce search inputs
- Lazy load routes and heavy components
- Optimize images and assets

**Backend**:
- Use async/await consistently
- Stream large responses (WebSocket for chat)
- Lazy load models (load on first use)
- Cache embeddings and computations
- Use database indexes for queries
- LRU cache for model management

**Database**:
- Index frequently queried columns
- Use foreign keys for relationships
- Regular VACUUM operations for SQLite
- Limit query results with pagination

---

## AI Assistant Best Practices

### When Working on This Codebase

**1. Always Read Before Modifying**:
- Never propose changes to code you haven't read
- Use Read tool to examine files before editing
- Understand context and existing patterns

**2. Follow Existing Patterns**:
- Match naming conventions in the file you're editing
- Use the same import style
- Follow established component/function structures
- Maintain consistency with codebase style

**3. Type Safety First**:
- Always add TypeScript types for new code
- Always add Python type hints
- Leverage Pydantic for API validation
- Use SQLAlchemy types for database models

**4. Test Your Changes**:
- Write tests for new features
- Ensure existing tests still pass
- Test manually in development mode
- Verify API endpoints via /docs

**5. Document Your Changes**:
- Add docstrings for Python functions
- Add JSDoc comments for complex TypeScript
- Update relevant .md files if needed
- Include inline comments for complex logic

**6. Error Handling**:
- Always handle potential errors
- Use try/catch in TypeScript
- Use try/except in Python
- Return meaningful error messages
- Log errors appropriately

**7. Security Mindset**:
- Never commit secrets
- Validate all user input
- Sanitize output to prevent XSS
- Use proper authentication/authorization
- Follow principle of least privilege

**8. Commit Best Practices**:
- Write clear, descriptive commit messages
- Follow conventional commit format
- Make atomic commits (one logical change)
- Don't mix refactoring with features

### Understanding the Full Stack

**Request Flow** (Chat Example):
```
1. User types message
   └─> frontend/src/components/Chat/MessageInput.tsx

2. Component calls hook
   └─> frontend/src/hooks/useChat.ts

3. Hook calls API
   └─> frontend/src/utils/api.ts (POST /api/chat/send)

4. Vite proxy forwards to backend
   └─> http://localhost:8000/api/chat/send

5. FastAPI receives request
   └─> backend/api/routes/chat.py (route handler)

6. Route handler processes
   ├─> Context management (backend/context/)
   ├─> RAG retrieval (backend/embeddings/)
   ├─> Model inference (backend/models/)
   └─> Save to database (backend/database/)

7. Response streamed back
   └─> WebSocket → Frontend → UI update
```

### Common Debugging Approaches

**Backend Issues**:
1. Check logs: `tail -f data/logs/ai_studio.log`
2. Test endpoint: `http://localhost:8000/docs`
3. Check database: `sqlite3 data/database/ai_studio.db`
4. Add debug logging: `logger.debug("Debug info")`
5. Use Python debugger: `import pdb; pdb.set_trace()`

**Frontend Issues**:
1. Check browser console for errors
2. Check Network tab for failed API calls
3. Use React DevTools to inspect state
4. Add console.log for debugging (remove before commit)
5. Check API response in /docs

**Integration Issues**:
1. Verify backend is running (http://localhost:8000/health)
2. Verify frontend proxy config (vite.config.ts)
3. Check CORS settings (backend/main.py)
4. Verify WebSocket connection
5. Check IPC communication (Electron)

### Resources for AI Assistants

**Key Documentation Files**:
- `ARCHITECTURE.md`: System design, data flow
- `docs/DEVELOPER_GUIDE.md`: Setup, patterns, examples
- `docs/API.md`: Backend API reference
- `docs/CONTRIBUTING.md`: Contribution process
- `ROADMAP.md`: Planned features

**API Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Code Examples**:
- Check existing route handlers in `backend/api/routes/`
- Check existing components in `frontend/src/components/`
- Check existing hooks in `frontend/src/hooks/`

---

## Quick Decision Tree

### "Should I create a new component or modify existing?"

```
Is there an existing component that does something similar?
├─ Yes → Modify existing component or extract shared logic
└─ No → Create new component
    ├─ Is it reusable? → Place in components/ui/
    └─ Feature-specific? → Place in components/[Feature]/
```

### "Should I create a new API endpoint or extend existing?"

```
Does existing endpoint handle similar data?
├─ Yes → Extend existing endpoint with optional parameters
└─ No → Create new endpoint
    ├─ Related to existing route? → Add to same router
    └─ New feature area? → Create new router file
```

### "Should I create a new hook or use existing?"

```
Does existing hook provide similar functionality?
├─ Yes → Use or extend existing hook
└─ No → Create new hook
    ├─ Reusable across features? → Place in hooks/
    └─ Feature-specific? → Place in components/[Feature]/hooks/
```

---

## Conclusion

This guide provides comprehensive context for AI assistants working with the AI Studio codebase. Always prioritize:

1. **Code Quality**: Follow conventions, use types, handle errors
2. **Security**: Validate input, protect sensitive data
3. **Testing**: Write tests, verify functionality
4. **Documentation**: Update docs, add comments
5. **Consistency**: Match existing patterns
6. **Performance**: Optimize where it matters
7. **Collaboration**: Clear commits, helpful PRs

**When in doubt**:
- Check existing code for patterns
- Consult ARCHITECTURE.md or DEVELOPER_GUIDE.md
- Test changes thoroughly
- Ask in PR/issue if uncertain

Happy coding! 🚀
