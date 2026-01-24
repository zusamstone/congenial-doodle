# AI Studio Backend

FastAPI backend for AI Studio - Local AI Chat Application

## Overview

This is the Python backend that powers AI Studio. It provides:

- **Chat API**: WebSocket-based streaming chat with AI models
- **Model Management**: Load, unload, and manage local and API models
- **RAG System**: Document embeddings and retrieval-augmented generation
- **LoRA Support**: Dynamic LoRA adapter loading for local models
- **System Prompts**: Reusable prompt library
- **Database**: SQLite with SQLAlchemy async ORM

## Installation

1. **Install Python 3.11+**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the server**:
   ```bash
   python main.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

## Architecture

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
│
├── api/                    # API routes
│   └── routes/
│       ├── chat.py         # Chat endpoints
│       ├── models.py       # Model management
│       ├── embeddings.py   # RAG endpoints
│       ├── lora.py         # LoRA management
│       └── system_prompts.py
│
├── database/              # Database layer
│   ├── db.py             # Database connection
│   └── models.py         # SQLAlchemy models
│
├── models/               # Model management (TODO)
│   ├── manager.py        # Model loading/unloading
│   ├── inference.py      # Inference logic
│   └── providers/        # API providers
│
├── embeddings/           # RAG system (TODO)
│   ├── chunking.py       # Document chunking
│   ├── embedding.py      # Embedding generation
│   └── retrieval.py      # Vector search
│
└── utils/                # Utilities
    ├── config.py         # Configuration
    ├── portable_paths.py # Path management
    └── hardware_detection.py
```

## API Documentation

Once running, visit:
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc
- **OpenAPI spec**: http://localhost:8000/openapi.json

## Key Endpoints

### Chat
- `WS /api/chat/stream` - WebSocket streaming chat
- `GET /api/chat/{chat_id}/messages` - Get chat messages
- `POST /api/chat/` - Create new chat
- `DELETE /api/chat/{chat_id}` - Delete chat

### Models
- `GET /api/models` - List all models
- `POST /api/models/load` - Load a model
- `POST /api/models/unload` - Unload a model
- `POST /api/models/download` - Download model from HuggingFace

### Embeddings (RAG)
- `POST /api/embeddings/upload` - Upload document
- `GET /api/embeddings/sources` - List knowledge sources
- `POST /api/embeddings/retrieve` - Retrieve relevant chunks

### System Prompts
- `GET /api/system-prompts` - List all prompts
- `POST /api/system-prompts` - Create new prompt
- `PUT /api/system-prompts/{id}` - Update prompt

## Configuration

Environment variables (set in `.env` or system environment):

```bash
# Server
HOST=127.0.0.1
PORT=8000
DEBUG=false

# Paths (portable mode)
DATA_DIR=./data
MODELS_DIR=./data/models
VECTOR_STORE_DIR=./data/vector_store

# Models
DEFAULT_MODEL=
DEFAULT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Hardware
DEFAULT_GPU_LAYERS=0
DEFAULT_THREADS=4

# API Keys (optional)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
```

## Database

SQLite database with async support (aiosqlite).

**Tables**:
- `chats` - Chat sessions
- `messages` - Chat messages
- `system_prompts` - Prompt library
- `models` - Model registry
- `loras` - LoRA adapters
- `knowledge_sources` - RAG documents
- `folders` - Chat organization
- `settings` - App settings
- `summaries` - Context summaries

The database is automatically created on first run at `./data/database/ai_studio.db`.

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
ruff check .
```

### Adding a New Route
1. Create route file in `api/routes/`
2. Define Pydantic models for request/response
3. Implement endpoints with proper async/await
4. Add to `main.py` with `app.include_router()`

## TODO

The following features have skeleton implementations and need to be completed:

- [ ] Model loading with llama-cpp-python
- [ ] Streaming inference with WebSocket
- [ ] Document processing and chunking
- [ ] ChromaDB integration for RAG
- [ ] API provider integrations (OpenAI, Anthropic, Google)
- [ ] LoRA adapter support
- [ ] Model downloading from HuggingFace
- [ ] Hardware optimization (GPU layers, CUDA, Metal)
- [ ] API key encryption
- [ ] Context management and summarization
- [ ] Token counting and limits
- [ ] Rate limiting
- [ ] Caching

## License

See LICENSE file in root directory.
