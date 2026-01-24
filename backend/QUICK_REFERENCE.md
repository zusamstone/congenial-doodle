# AI Studio Backend - Quick Reference

## 🚀 Start Server

```bash
python run.py                    # Dev mode (hot reload)
python run.py --prod            # Production mode
python run.py --skip-install    # Skip dependency install
```

## 📚 API Endpoints

### Chat
```
POST   /api/chat/                           Create chat
GET    /api/chat/                           List chats
GET    /api/chat/{id}/messages              Get messages
DELETE /api/chat/{id}                       Delete chat
PATCH  /api/chat/{id}/message/{mid}         Edit message
WS     /api/chat/stream                     WebSocket chat
```

### Models
```
GET    /api/models                          List models
POST   /api/models                          Register model
GET    /api/models/{id}                     Get model
DELETE /api/models/{id}                     Delete model
POST   /api/models/load                     Load model
POST   /api/models/unload                   Unload model
POST   /api/models/download                 Download model
GET    /api/models/download/{id}/progress   Download progress
```

### Embeddings (RAG)
```
POST   /api/embeddings/upload               Upload document
GET    /api/embeddings/sources              List sources
GET    /api/embeddings/sources/{id}         Get source
DELETE /api/embeddings/sources/{id}         Delete source
POST   /api/embeddings/retrieve             Retrieve chunks
POST   /api/embeddings/reindex/{id}         Reindex source
```

### LoRA
```
GET    /api/lora                            List LoRAs
POST   /api/lora                            Register LoRA
GET    /api/lora/{id}                       Get LoRA
PATCH  /api/lora/{id}                       Update LoRA
DELETE /api/lora/{id}                       Delete LoRA
POST   /api/lora/{id}/apply                 Apply to model
POST   /api/lora/{id}/remove                Remove from model
```

### System Prompts
```
GET    /api/system-prompts                  List prompts
POST   /api/system-prompts                  Create prompt
GET    /api/system-prompts/{id}             Get prompt
PUT    /api/system-prompts/{id}             Update prompt
DELETE /api/system-prompts/{id}             Delete prompt
POST   /api/system-prompts/{id}/use         Increment usage
```

## 📦 Database Models

- `Chat` - Chat sessions
- `Message` - Messages with thinking support
- `SystemPrompt` - Prompt library
- `Model` - Model registry
- `LoRA` - LoRA adapters
- `KnowledgeSource` - RAG documents
- `Folder` - Chat folders
- `Setting` - App settings
- `Summary` - Context summaries

## 🔧 Configuration (.env)

```bash
# Server
HOST=127.0.0.1
PORT=8000
DEBUG=false

# Paths
DATA_DIR=./data
MODELS_DIR=./data/models

# Models
DEFAULT_MODEL=
DEFAULT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Hardware
DEFAULT_GPU_LAYERS=0
DEFAULT_THREADS=4

# API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
```

## 🧪 Testing

```bash
pytest                          # Run all tests
pytest test_main.py            # Run specific test
pytest --cov                   # With coverage
```

## 🛠️ Development

```bash
black .                        # Format code
ruff check .                   # Lint code
mypy .                         # Type check
```

## 📂 Directory Structure

```
backend/
├── main.py              # FastAPI app
├── run.py               # Setup script
├── requirements.txt     # Dependencies
│
├── api/routes/          # API endpoints
├── database/            # DB models & connection
└── utils/               # Config, paths, hardware
```

## 🔗 URLs

- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc  
- **Health**: http://localhost:8000/health

## 💡 Quick Tips

1. **Hot Reload**: Edit files and save - server auto-restarts
2. **Logs**: See `data/logs/ai_studio.log`
3. **Database**: Located at `data/database/ai_studio.db`
4. **Test API**: Use `/docs` interactive interface

## 🐛 Troubleshooting

```bash
# Check if server is running
curl http://localhost:8000/health

# View logs
tail -f data/logs/ai_studio.log

# Database inspection
sqlite3 data/database/ai_studio.db ".tables"

# Clean restart
rm -rf data/ && python run.py
```

## 📝 Next Implementation Tasks

1. ☐ Model loading (llama-cpp-python)
2. ☐ WebSocket streaming
3. ☐ RAG pipeline (chunking, embedding, retrieval)
4. ☐ API providers (OpenAI, Anthropic, Google)
5. ☐ LoRA support
6. ☐ Model downloads
7. ☐ Context management
8. ☐ API key encryption

---
For detailed documentation, see README.md and DEVELOPMENT.md
