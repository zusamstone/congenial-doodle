# AI Studio - Architecture Documentation

This document describes the technical architecture, design decisions, and system interactions of AI Studio.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Component Details](#component-details)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [IPC Communication](#ipc-communication)
- [Security](#security)
- [Performance Considerations](#performance-considerations)
- [Portable Structure](#portable-structure)

## System Overview

AI Studio is a multi-layered desktop application built on three main components:

1. **Frontend (React + TypeScript)**: User interface and client-side logic
2. **Electron**: Desktop application wrapper and IPC bridge
3. **Backend (Python + FastAPI)**: AI inference, database, and business logic

### Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Desktop Framework | Electron | Cross-platform, mature ecosystem, web tech |
| Frontend Framework | React 18 | Modern, component-based, large ecosystem |
| Type System | TypeScript | Type safety, better DX, fewer bugs |
| Styling | TailwindCSS | Utility-first, fast development, consistent |
| Build Tool | Vite | Fast HMR, modern, optimized builds |
| Backend Language | Python 3.11+ | AI/ML ecosystem, type hints, async support |
| Web Framework | FastAPI | Fast, modern, auto-docs, type validation |
| Local Inference | llama.cpp | Efficient, hardware-optimized, broad support |
| Vector DB | ChromaDB | Embedded, simple API, portable |
| Relational DB | SQLite | Embedded, portable, reliable |
| ORM | SQLAlchemy | Mature, flexible, async support |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    React Frontend                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │  │
│  │  │  Chat    │  │ Sidebar  │  │ Settings │  │  Models  │ │  │
│  │  │Interface │  │          │  │          │  │          │ │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │           State Management (Hooks + Context)         │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↕ IPC                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Electron Main Process                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │  │
│  │  │   Window   │  │    IPC     │  │  Python Process   │ │  │
│  │  │ Management │  │  Bridge    │  │    Manager         │ │  │
│  │  └────────────┘  └────────────┘  └────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────────┐
│                     Python Backend (FastAPI)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      API Routes                           │  │
│  │  /chat  /models  /embeddings  /lora  /system-prompts    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↕                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │    Model     │  │  Embedding   │  │     Context          │ │
│  │   Manager    │  │   Manager    │  │    Manager           │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│                              ↕                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │   llama.cpp  │  │   ChromaDB   │  │      SQLite          │ │
│  │  (Inference) │  │  (Vectors)   │  │   (Metadata)         │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      Portable Data Directory                    │
│  ./data/models/  ./data/vector_store/  ./data/database/        │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React + TypeScript)

#### Directory Structure
```
frontend/
├── src/
│   ├── App.tsx                 # Root component
│   ├── main.tsx                # Entry point
│   ├── components/             # UI components
│   │   ├── Chat/               # Chat interface
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── ThinkingDisplay.tsx
│   │   ├── Sidebar/            # Navigation
│   │   ├── Models/             # Model management
│   │   ├── Settings/           # Settings panels
│   │   ├── KnowledgeBase/      # RAG UI
│   │   ├── SystemPrompts/      # Prompt library
│   │   └── Monitoring/         # Resource display
│   ├── hooks/                  # Custom hooks
│   │   ├── useChat.ts          # Chat logic
│   │   ├── useModels.ts        # Model management
│   │   ├── useContextManagement.ts
│   │   ├── useRAG.ts           # RAG logic
│   │   ├── useSystemPrompts.ts
│   │   └── useSettings.ts
│   ├── utils/                  # Utilities
│   │   ├── tokenCounter.ts     # Token counting
│   │   ├── markdown.ts         # Markdown rendering
│   │   ├── storage.ts          # Local storage
│   │   └── api.ts              # API client
│   ├── types/                  # TypeScript types
│   └── styles/                 # Global styles
└── package.json
```

#### State Management

**Approach**: React Context + Custom Hooks (no Redux)

**Key Contexts**:
- `ChatContext`: Current chat, messages, streaming state
- `ModelsContext`: Available models, current model, loading state
- `SettingsContext`: User settings, preferences
- `RAGContext`: Knowledge base, retrieval settings

**Why No Redux**:
- React hooks are sufficient for this application
- Simpler mental model
- Less boilerplate
- Better TypeScript integration

#### Component Architecture

**Smart Components** (connected to state):
- `ChatInterface`: Main chat orchestrator
- `ModelSelector`: Model management
- `SettingsPanel`: Settings management

**Presentational Components** (pure, reusable):
- `MessageList`: Display messages
- `MessageInput`: Input field
- `Button`, `Modal`, `Dropdown`, etc.

### Electron Layer

#### Main Process (`main.js`)

**Responsibilities**:
- Create application window
- Manage window lifecycle
- Start Python backend
- Handle IPC from renderer
- Manage updates
- Configure portable paths

**Key APIs Used**:
- `BrowserWindow`: Window management
- `ipcMain`: IPC communication
- `app`: Application lifecycle
- `dialog`: File dialogs
- `shell`: Open external links

#### Preload Script (`preload.js`)

**Purpose**: Secure IPC bridge between renderer and main

**Exposed APIs** (via `contextBridge`):
```typescript
window.electronAPI = {
  // Chat
  sendMessage: (message: string) => Promise<void>,
  streamResponse: (callback: Function) => void,
  stopGeneration: () => void,
  
  // Files
  selectFile: () => Promise<string>,
  readFile: (path: string) => Promise<string>,
  
  // Models
  downloadModel: (url: string) => Promise<void>,
  loadModel: (path: string) => Promise<void>,
  
  // Settings
  getSetting: (key: string) => Promise<any>,
  setSetting: (key: string, value: any) => Promise<void>,
}
```

**Security**:
- `contextIsolation: true`: Renderer has no Node access
- `nodeIntegration: false`: No Node in renderer
- `sandbox: true`: Additional isolation
- Only expose necessary APIs

#### Python Process Management

**Starting Python Backend**:
```javascript
const { spawn } = require('child_process');
const pythonProcess = spawn('python', ['backend/main.py'], {
  cwd: app.getAppPath(),
  env: { ...process.env, PORTABLE_MODE: 'true' }
});
```

**Health Checks**:
- Ping backend on startup
- Retry on failure
- Display error if backend fails to start

**Shutdown**:
- Graceful shutdown signal to Python
- Wait for cleanup
- Force kill if timeout

### Backend (Python + FastAPI)

#### Directory Structure
```
backend/
├── main.py                     # FastAPI app entry
├── requirements.txt            # Dependencies
├── api/
│   ├── routes/
│   │   ├── chat.py             # Chat endpoints
│   │   ├── models.py           # Model management
│   │   ├── embeddings.py       # RAG endpoints
│   │   ├── lora.py             # LoRA management
│   │   └── system_prompts.py   # Prompt library
│   └── middleware/             # Custom middleware
├── models/
│   ├── model_manager.py        # Model loading/unloading
│   ├── inference_engine.py     # llama.cpp wrapper
│   ├── lora_manager.py         # LoRA handling
│   └── api_providers.py        # OpenAI, Anthropic, etc.
├── embeddings/
│   ├── embedding_manager.py    # Embedding generation
│   ├── vector_store.py         # ChromaDB wrapper
│   ├── document_processor.py   # Text extraction
│   └── retriever.py            # RAG retrieval
├── context/
│   ├── context_manager.py      # Context strategies
│   ├── summarizer.py           # Summarization
│   ├── rolling_window.py       # Rolling window
│   └── periodic_summary.py     # Periodic summary
├── guidance/
│   ├── guidance_manager.py     # Guidance orchestrator
│   ├── system_prompt_integration.py
│   ├── cfg_handler.py          # CFG implementation
│   └── logit_bias.py           # Logit bias
├── monitoring/
│   ├── resource_monitor.py     # CPU/GPU/RAM tracking
│   └── token_counter.py        # Token counting
├── database/
│   ├── db.py                   # Database setup
│   ├── models.py               # SQLAlchemy models
│   └── migrations/             # Schema migrations
└── utils/
    ├── config.py               # Configuration
    ├── hardware_detection.py   # GPU/CPU detection
    └── portable_paths.py       # Path management
```

#### FastAPI Application

**Main App** (`main.py`):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, models, embeddings, lora, system_prompts

app = FastAPI(title="AI Studio Backend", version="1.0.0")

# CORS for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(embeddings.router, prefix="/api/embeddings", tags=["embeddings"])
app.include_router(lora.router, prefix="/api/lora", tags=["lora"])
app.include_router(system_prompts.router, prefix="/api/system-prompts", tags=["system-prompts"])

@app.on_event("startup")
async def startup():
    # Initialize database
    # Load configuration
    # Start resource monitoring
    pass

@app.on_event("shutdown")
async def shutdown():
    # Cleanup resources
    # Unload models
    pass
```

#### Model Management

**Model Manager** (`models/model_manager.py`):
- Track loaded models
- Lazy loading (load on first use)
- Automatic unloading (LRU when memory tight)
- VRAM tracking

**Inference Engine** (`models/inference_engine.py`):
- Wrapper around llama-cpp-python
- Streaming support
- Parameter validation
- Error handling

**API Providers** (`models/api_providers.py`):
- Unified interface for OpenAI, Anthropic, Google
- API key management
- Token counting
- Error handling and retries

#### Embeddings & RAG

**Document Processing Flow**:
1. **Upload**: Receive file from frontend
2. **Extract**: Use appropriate extractor (PyPDF2, python-docx, etc.)
3. **Chunk**: Split text into overlapping chunks
4. **Embed**: Generate embeddings with chosen model
5. **Store**: Save to ChromaDB with metadata
6. **Index**: Make searchable

**Retrieval Flow**:
1. **Query**: Receive user query
2. **Embed Query**: Generate query embedding
3. **Search**: ChromaDB similarity search
4. **Rerank** (optional): Cross-encoder reranking
5. **Return**: Top K chunks with metadata

**ChromaDB Configuration**:
```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./data/vector_store",
    anonymized_telemetry=False
))

collection = client.get_or_create_collection(
    name="knowledge_base",
    metadata={"hnsw:space": "cosine"}
)
```

#### Context Management

**Strategy Pattern**:
```python
class ContextStrategy(ABC):
    @abstractmethod
    async def manage_context(
        self, 
        messages: List[Message], 
        max_tokens: int
    ) -> List[Message]:
        pass

class SmartSummarizationStrategy(ContextStrategy):
    async def manage_context(self, messages, max_tokens):
        # Implementation
        pass

class RollingWindowStrategy(ContextStrategy):
    async def manage_context(self, messages, max_tokens):
        # Implementation
        pass
```

**Context Manager**:
- Select strategy based on settings
- Monitor token usage
- Trigger management when needed
- Handle pinned messages

## Data Flow

### Chat Message Flow

```
User Types Message
       ↓
[Frontend] MessageInput component
       ↓
[Frontend] useChat hook
       ↓
[Frontend] API call via api.ts
       ↓
[IPC] Electron IPC bridge (optional)
       ↓
[HTTP] POST /api/chat/send
       ↓
[Backend] chat.py route handler
       ↓
[Backend] Context Manager (check tokens, summarize if needed)
       ↓
[Backend] RAG Retriever (if enabled, fetch relevant chunks)
       ↓
[Backend] Guidance Manager (apply positive/negative guidance)
       ↓
[Backend] Model Manager (select appropriate model)
       ↓
[Backend] Inference Engine OR API Provider
       ↓
[WebSocket] Stream tokens back to frontend
       ↓
[Frontend] Update UI in real-time
       ↓
[Backend] Save message to database
       ↓
[Frontend] Display complete message
```

### Model Loading Flow

```
User Selects Model
       ↓
[Frontend] ModelSelector component
       ↓
[Backend] GET /api/models/{id}
       ↓
[Backend] Model Manager checks if loaded
       ↓
If not loaded:
  ├─→ Check VRAM availability
  ├─→ Check disk space
  ├─→ Load model with llama.cpp
  └─→ Update loaded models registry
       ↓
[Backend] Return model info + status
       ↓
[Frontend] Update UI
```

### RAG Upload Flow

```
User Uploads Document
       ↓
[Frontend] DocumentUpload component
       ↓
[Backend] POST /api/embeddings/upload (multipart)
       ↓
[Backend] Document Processor
  ├─→ Detect format
  ├─→ Extract text
  └─→ Clean and normalize
       ↓
[Backend] Chunking
  ├─→ Split by strategy (sentence, paragraph, etc.)
  ├─→ Apply overlap
  └─→ Preserve metadata (page, section)
       ↓
[Backend] Embedding Manager
  ├─→ Generate embeddings (batch)
  └─→ Track progress
       ↓
[Backend] Vector Store
  ├─→ Save to ChromaDB
  └─→ Update metadata in SQLite
       ↓
[WebSocket] Progress updates to frontend
       ↓
[Frontend] Display progress bar
       ↓
[Backend] Return success
       ↓
[Frontend] Update knowledge base list
```

## Database Schema

### SQLite Schema

```sql
-- Chat sessions
CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    folder_id INTEGER,
    pinned BOOLEAN DEFAULT FALSE,
    archived BOOLEAN DEFAULT FALSE,
    tags TEXT,  -- JSON array
    model_id INTEGER,
    FOREIGN KEY (folder_id) REFERENCES folders(id),
    FOREIGN KEY (model_id) REFERENCES models(id)
);

-- Messages within chats
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    role TEXT NOT NULL,  -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    thinking_content TEXT,  -- For thinking models
    tokens INTEGER,
    thinking_tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pinned BOOLEAN DEFAULT FALSE,
    metadata TEXT,  -- JSON: model used, settings, etc.
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);

-- System prompts
CREATE TABLE system_prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    prompt TEXT NOT NULL,
    tags TEXT,  -- JSON array
    icon TEXT,
    usage_count INTEGER DEFAULT 0,
    default_settings TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Models registry
CREATE TABLE models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT,  -- For local models
    type TEXT NOT NULL,  -- 'local', 'openai', 'anthropic', etc.
    size INTEGER,  -- File size in bytes
    context_length INTEGER,
    parameters TEXT,  -- e.g., "7B", "13B"
    metadata TEXT,  -- JSON: quantization, architecture, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LoRA adapters
CREATE TABLE loras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    compatible_models TEXT,  -- JSON array of model IDs
    weight REAL DEFAULT 1.0,
    enabled BOOLEAN DEFAULT TRUE,
    metadata TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge sources
CREATE TABLE knowledge_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'pdf', 'txt', 'url', etc.
    path TEXT,
    chunk_count INTEGER DEFAULT 0,
    embedding_model TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON: page count, file size, etc.
);

-- Folders for organization
CREATE TABLE folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_id INTEGER,
    icon TEXT,
    color TEXT,
    FOREIGN KEY (parent_id) REFERENCES folders(id)
);

-- Settings
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,  -- JSON
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Summaries (for context management)
CREATE TABLE summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    summary TEXT NOT NULL,
    message_range TEXT,  -- JSON: {start: msg_id, end: msg_id}
    tokens INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);
```

### ChromaDB Collections

**knowledge_base** collection:
- Documents from uploads
- Metadata: source_id, page, chunk_index, file_type

**chat_history** collection (optional):
- Embedded chat messages
- Metadata: chat_id, message_id, timestamp, role

### Indexes

```sql
CREATE INDEX idx_messages_chat_id ON messages(chat_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_chats_updated_at ON chats(updated_at);
CREATE INDEX idx_chats_folder_id ON chats(folder_id);
CREATE INDEX idx_chats_pinned ON chats(pinned);
```

## IPC Communication

### Electron IPC Channels

#### Renderer → Main

**Chat**:
- `chat:send-message` - Send user message
- `chat:stop-generation` - Stop streaming
- `chat:regenerate` - Regenerate last response
- `chat:edit-message` - Edit and resend

**Files**:
- `file:select` - Open file dialog
- `file:upload` - Upload file for RAG
- `file:export-chat` - Export chat to file

**Models**:
- `model:load` - Load a model
- `model:unload` - Unload a model
- `model:download` - Download from HuggingFace

**Settings**:
- `settings:get` - Get setting value
- `settings:set` - Set setting value
- `settings:reset` - Reset to defaults

#### Main → Renderer

**Chat**:
- `chat:message-chunk` - Streaming token
- `chat:message-complete` - Generation complete
- `chat:error` - Error during generation

**Files**:
- `file:upload-progress` - Upload progress
- `file:embedding-progress` - Embedding progress

**Models**:
- `model:load-progress` - Model loading progress
- `model:download-progress` - Download progress

**System**:
- `system:resource-update` - CPU/GPU/RAM update
- `system:notification` - Toast notification

### REST API Endpoints

#### Chat Routes

```
POST   /api/chat/send
  Body: { message, chatId?, model?, settings? }
  Returns: { messageId, chatId }
  
GET    /api/chat/{chatId}/messages
  Returns: { messages: [...] }
  
DELETE /api/chat/{chatId}
  
PATCH  /api/chat/{chatId}/message/{messageId}
  Body: { content }
  
POST   /api/chat/{chatId}/regenerate
  Body: { messageId }
```

#### Model Routes

```
GET    /api/models
  Returns: { models: [...] }
  
GET    /api/models/{modelId}
  Returns: { model: {...} }
  
POST   /api/models/load
  Body: { modelId, gpuLayers?, threads? }
  
POST   /api/models/unload
  Body: { modelId }
  
POST   /api/models/download
  Body: { url, quantization? }
  Returns: { downloadId }
  
GET    /api/models/download/{downloadId}/progress
  Returns: { progress, speed, eta }
```

#### Embeddings Routes

```
POST   /api/embeddings/upload
  Body: multipart/form-data (files)
  Returns: { sourceId, status }
  
GET    /api/embeddings/sources
  Returns: { sources: [...] }
  
DELETE /api/embeddings/sources/{sourceId}
  
POST   /api/embeddings/retrieve
  Body: { query, maxChunks, minRelevance }
  Returns: { chunks: [...] }
```

#### System Prompts Routes

```
GET    /api/system-prompts
  Returns: { prompts: [...] }
  
POST   /api/system-prompts
  Body: { name, description, prompt, tags, icon, defaultSettings }
  
PUT    /api/system-prompts/{promptId}
  
DELETE /api/system-prompts/{promptId}
```

### WebSocket Connections

**Chat Streaming**:
```
ws://localhost:8000/api/chat/stream

Client sends:
{
  "action": "send",
  "chatId": 123,
  "message": "Hello",
  "model": "gpt-4",
  "settings": {...}
}

Server sends:
{
  "type": "token",
  "token": "Hello",
  "chatId": 123,
  "messageId": 456
}

{
  "type": "thinking",
  "token": "Let me think...",
  "chatId": 123,
  "messageId": 456
}

{
  "type": "complete",
  "chatId": 123,
  "messageId": 456,
  "tokens": 50
}

{
  "type": "error",
  "error": "Model not loaded"
}
```

## Security

### Electron Security

**Renderer Process**:
- `contextIsolation: true` - No access to Node APIs
- `nodeIntegration: false` - Explicitly disable Node
- `sandbox: true` - Additional sandboxing
- `webSecurity: true` - Enforce same-origin policy

**Preload Script**:
- Only expose necessary APIs via `contextBridge`
- Validate all inputs from renderer
- No direct file system access from renderer

**CSP (Content Security Policy)**:
```javascript
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self'; " +
        "script-src 'self' 'unsafe-inline'; " +
        "style-src 'self' 'unsafe-inline'; " +
        "img-src 'self' data: https:; " +
        "connect-src 'self' ws://localhost:8000 http://localhost:8000"
      ]
    }
  });
});
```

### API Security

**API Keys**:
- Stored encrypted in SQLite
- Never sent to frontend in plain text
- Decrypted only in backend memory
- Environment variables as fallback

**CORS**:
- Restrict to localhost origins only
- No wildcard origins in production

**Rate Limiting**:
- Limit API requests per minute
- Prevent abuse of expensive operations

**Input Validation**:
- Pydantic models for all inputs
- Sanitize file uploads
- Validate file types and sizes
- SQL injection prevention (ORM)

### Data Privacy

**No Telemetry**:
- No analytics by default
- Optional opt-in crash reporting
- No data sent to external servers

**Local Processing**:
- All inference happens locally or via user's API keys
- No proxy servers
- Direct API connections

**Encryption**:
- API keys encrypted at rest
- Optional chat history encryption (future)

## Performance Considerations

### Frontend Optimizations

**React Performance**:
- Memo for expensive components
- Virtual scrolling for message lists
- Debounce search inputs
- Lazy load components
- Code splitting by route

**Asset Optimization**:
- Vite tree shaking
- Minification in production
- Image optimization
- Font subsetting

### Backend Optimizations

**Model Loading**:
- Lazy loading (on first use)
- Keep hot models in memory
- LRU cache for model unloading
- Quantized models for speed

**Inference**:
- Batch processing where possible
- GPU acceleration (CUDA, Metal, ROCm)
- Optimal thread count based on CPU
- KV cache for speed

**Embeddings**:
- Batch embedding generation
- Cache embeddings
- Use smaller models when sufficient

**Database**:
- Prepared statements
- Connection pooling
- Indexes on common queries
- Regular VACUUM operations

### Memory Management

**Model Memory**:
- Track VRAM usage per model
- Warn before loading large models
- Auto-unload unused models
- Suggest lighter quantizations

**Frontend Memory**:
- Limit message history in memory (virtualize)
- Clean up old WebSocket connections
- Garbage collection for old state

**Backend Memory**:
- Streaming for large responses
- Chunked file uploads
- Generator patterns for large data

## Portable Structure

### Directory Layout

```
AI-Studio/                      # App root
├── AI-Studio.exe               # Main executable (Windows)
├── resources/                  # Electron resources
│   └── app.asar                # Bundled frontend/Electron code
├── python/                     # Bundled Python runtime
│   ├── python.exe
│   ├── Lib/
│   └── Scripts/
├── data/                       # User data (portable)
│   ├── models/
│   │   ├── llama-2-7b-q4.gguf
│   │   └── mistral-7b-q5.gguf
│   ├── loras/
│   │   └── coding-lora.bin
│   ├── vector_store/
│   │   └── chromadb/
│   ├── database/
│   │   └── ai_studio.db
│   ├── uploads/
│   └── chats/
├── config/
│   ├── default_settings.json
│   ├── user_settings.json      # User overrides
│   └── models_registry.json
└── logs/
    └── ai_studio.log
```

### Path Resolution

**Portable Paths** (`backend/utils/portable_paths.py`):
```python
import os
from pathlib import Path

def get_app_root():
    """Get application root directory."""
    if os.getenv('PORTABLE_MODE'):
        # Running in portable mode
        return Path(__file__).parent.parent.parent
    else:
        # Development mode
        return Path(__file__).parent.parent

def get_data_dir():
    """Get data directory path."""
    return get_app_root() / 'data'

def get_models_dir():
    """Get models directory path."""
    return get_data_dir() / 'models'

# ... similar for other directories
```

### Configuration Management

**Settings Priority**:
1. User settings (`config/user_settings.json`)
2. Default settings (`config/default_settings.json`)
3. Hardcoded defaults

**Settings Loading**:
```python
import json
from pathlib import Path

def load_settings():
    default_path = get_config_dir() / 'default_settings.json'
    user_path = get_config_dir() / 'user_settings.json'
    
    # Load defaults
    with open(default_path) as f:
        settings = json.load(f)
    
    # Override with user settings
    if user_path.exists():
        with open(user_path) as f:
            user_settings = json.load(f)
        settings.update(user_settings)
    
    return settings
```

### Cross-Platform Considerations

**Windows**:
- Executable: AI-Studio.exe
- Bundle Python with PyInstaller or similar
- Registry: None (portable)
- Data location: ./data/

**macOS**:
- Bundle: AI-Studio.app
- Python: Included in app bundle
- Data location: AI-Studio.app/Contents/data/ or user-selected
- Code signing required for distribution

**Linux**:
- AppImage: AI-Studio.AppImage
- Python: Included in AppImage
- Data location: ./data/ next to AppImage
- No installation required

---

This architecture provides a solid foundation for a powerful, portable, local-first AI chat application with room for future expansion and optimization.
