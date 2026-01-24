# AI Studio Backend - Development Guide

## Quick Start

### 1. Setup and Run

```bash
# Install dependencies and run server
python run.py

# Or skip dependency installation
python run.py --skip-install

# Production mode (no hot reload)
python run.py --prod
```

The server will start at `http://localhost:8000`

### 2. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── run.py                     # Setup and run script
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── test_main.py              # Basic tests
│
├── api/                      # API layer
│   └── routes/              # Route modules
│       ├── chat.py          # Chat endpoints (WebSocket + REST)
│       ├── models.py        # Model management
│       ├── embeddings.py    # RAG system
│       ├── lora.py          # LoRA adapters
│       └── system_prompts.py # Prompt library
│
├── database/                # Database layer
│   ├── db.py               # Connection and session management
│   └── models.py           # SQLAlchemy ORM models
│
└── utils/                  # Utilities
    ├── config.py           # Configuration management
    ├── portable_paths.py   # Path handling for portable mode
    └── hardware_detection.py # CPU/GPU detection
```

## Development Workflow

### 1. Making Changes

The server runs with hot reload in development mode. Just edit files and save - the server will automatically restart.

### 2. Adding a New Endpoint

**Example: Adding a new chat export endpoint**

1. Open the relevant route file (e.g., `api/routes/chat.py`)

2. Define Pydantic models for validation:
   ```python
   class ExportRequest(BaseModel):
       chat_id: int
       format: str = "json"  # json, markdown, txt
   ```

3. Create the endpoint:
   ```python
   @router.post("/export")
   async def export_chat(
       request: ExportRequest,
       db: AsyncSession = Depends(get_db)
   ):
       # Implementation
       pass
   ```

4. The route is automatically available at `/api/chat/export`

### 3. Adding a New Database Model

1. Edit `database/models.py`:
   ```python
   class NewModel(Base):
       __tablename__ = "new_table"
       
       id = Column(Integer, primary_key=True)
       # ... other fields
   ```

2. The table will be created automatically on next startup

3. For production, use Alembic migrations:
   ```bash
   alembic revision --autogenerate -m "Add new table"
   alembic upgrade head
   ```

### 4. Working with Database

**Query examples:**

```python
from sqlalchemy import select
from database.models import Chat
from database.db import get_db

# In an endpoint:
async def get_chats(db: AsyncSession = Depends(get_db)):
    # Select all chats
    result = await db.execute(select(Chat))
    chats = result.scalars().all()
    
    # Select with filter
    result = await db.execute(
        select(Chat).where(Chat.archived == False)
    )
    
    # Create
    new_chat = Chat(title="New Chat")
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    
    # Update
    chat.title = "Updated"
    await db.commit()
    
    # Delete
    await db.delete(chat)
    await db.commit()
```

### 5. Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest test_main.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### 6. Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking (if mypy is installed)
mypy .
```

## Common Tasks

### Adding API Provider Integration

1. Create provider module in `models/providers/`
2. Implement provider class with standard interface
3. Register in model manager
4. Add configuration in `utils/config.py`

### Implementing Model Loading

Location: `models/manager.py` (TODO)

```python
from llama_cpp import Llama

class ModelManager:
    def __init__(self):
        self.loaded_model = None
    
    async def load_model(self, path: str, **kwargs):
        self.loaded_model = Llama(
            model_path=path,
            n_ctx=kwargs.get('context_length', 4096),
            n_gpu_layers=kwargs.get('gpu_layers', 0),
            n_threads=kwargs.get('threads', 4),
        )
    
    async def generate(self, prompt: str, **kwargs):
        return self.loaded_model.create_completion(
            prompt,
            max_tokens=kwargs.get('max_tokens', 256),
            temperature=kwargs.get('temperature', 0.7),
            stream=kwargs.get('stream', False),
        )
```

### Implementing RAG Pipeline

Location: `embeddings/` (TODO)

1. **Document Processing** (`embeddings/chunking.py`):
   - Extract text from PDFs, DOCX, etc.
   - Split into chunks with overlap
   
2. **Embedding Generation** (`embeddings/embedding.py`):
   - Load sentence-transformers model
   - Generate embeddings for chunks
   
3. **Vector Storage** (`embeddings/retrieval.py`):
   - Store in ChromaDB
   - Implement similarity search

### WebSocket Chat Implementation

Location: `api/routes/chat.py`

```python
@router.websocket("/stream")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            
            # Generate response (streaming)
            for token in model_manager.generate_stream(data['message']):
                await websocket.send_json({
                    "type": "token",
                    "token": token,
                })
            
            # Send completion
            await websocket.send_json({
                "type": "complete",
            })
            
    except WebSocketDisconnect:
        logger.info("Client disconnected")
```

## Configuration

### Environment Variables

See `.env.example` for all available options.

Key settings:
- `DEBUG`: Enable debug mode with verbose logging
- `DATA_DIR`: Base directory for all data (portable mode)
- `DEFAULT_GPU_LAYERS`: Default GPU offloading
- `*_API_KEY`: API keys for providers (encrypted in DB)

### Portable Mode

The application runs in portable mode by default:
- All data stored in `./data` relative to executable
- No system-wide installation needed
- Can run from USB drive

### Hardware Detection

The `utils/hardware_detection.py` module automatically detects:
- CPU cores and architecture
- Available GPUs (NVIDIA, AMD, Apple Silicon)
- System memory
- CUDA/Metal/Vulkan support

Use this for optimal model loading settings.

## Debugging

### Enable Debug Logging

Set in `.env`:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

### View Logs

Logs are written to `./data/logs/ai_studio.log`

```bash
tail -f data/logs/ai_studio.log
```

### Database Inspection

```bash
# Install sqlite3
sqlite3 data/database/ai_studio.db

# In sqlite3:
.tables              # List tables
.schema chats        # View schema
SELECT * FROM chats; # Query
```

### API Testing

Use the interactive docs at `/docs` or curl:

```bash
# Health check
curl http://localhost:8000/health

# Get chats
curl http://localhost:8000/api/chat/

# Create chat
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Chat"}'
```

## Production Deployment

1. **Set production environment**:
   ```bash
   DEBUG=false
   LOG_LEVEL=INFO
   ```

2. **Run with production server**:
   ```bash
   python run.py --prod
   
   # Or with uvicorn directly
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. **Use process manager** (recommended):
   ```bash
   # With systemd, supervisord, or pm2
   pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000"
   ```

## Troubleshooting

### Import Errors

Ensure you're in the backend directory and dependencies are installed:
```bash
cd backend
pip install -r requirements.txt
```

### Database Locked

SQLite doesn't handle concurrent writes well. If you get "database is locked":
- Ensure only one server instance is running
- Check no other process has the DB open
- Restart the server

### Model Loading Issues

- Verify model file exists and path is correct
- Check available system memory
- Try reducing `gpu_layers` if VRAM limited
- Check logs for specific error messages

### Port Already in Use

Change port in `.env`:
```bash
PORT=8001
```

Or in run command:
```bash
uvicorn main:app --port 8001
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [ChromaDB](https://docs.trychroma.com/)
- [Pydantic](https://docs.pydantic.dev/)
