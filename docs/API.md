# AI Studio API Reference

Complete REST and WebSocket API documentation for AI Studio backend.

## Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Error Responses](#error-responses)
- [Chat API](#chat-api)
- [Models API](#models-api)
- [Embeddings API (RAG)](#embeddings-api-rag)
- [LoRA API](#lora-api)
- [System Prompts API](#system-prompts-api)
- [WebSocket API](#websocket-api)
- [Health & Status](#health--status)

---

## Base URL

```
http://localhost:8000
```

All API endpoints are prefixed with `/api`.

---

## Authentication

Currently, AI Studio does not require authentication as it's a local-first application. Future versions may include optional API key protection.

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid request body |
| 500 | Internal Server Error |
| 501 | Not Implemented - Feature coming soon |

### Validation Error Response

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Chat API

Manage chat sessions and messages.

### Create Chat

Create a new chat session.

**Endpoint:** `POST /api/chat/`

**Request Body:**

```json
{
  "title": "My New Chat",
  "model_id": 1,
  "folder_id": null
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | Chat title (default: "New Chat") |
| model_id | integer | No | ID of model to use |
| folder_id | integer | No | ID of folder to organize chat in |

**Response:** `201 Created`

```json
{
  "id": 1,
  "title": "My New Chat",
  "created_at": "2024-01-20T10:30:00Z",
  "updated_at": "2024-01-20T10:30:00Z",
  "folder_id": null,
  "pinned": false,
  "archived": false,
  "tags": null,
  "model_id": 1,
  "message_count": 0
}
```

---

### List Chats

Get all chat sessions.

**Endpoint:** `GET /api/chat/`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| folder_id | integer | null | Filter by folder |
| archived | boolean | false | Show archived chats |
| limit | integer | 50 | Max results to return |
| offset | integer | 0 | Pagination offset |

**Example Request:**

```bash
GET /api/chat/?folder_id=1&limit=20&offset=0
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "My Chat",
    "created_at": "2024-01-20T10:30:00Z",
    "updated_at": "2024-01-20T10:35:00Z",
    "folder_id": 1,
    "pinned": false,
    "archived": false,
    "tags": ["python", "coding"],
    "model_id": 1,
    "message_count": 5
  }
]
```

---

### Get Chat Messages

Retrieve all messages from a chat.

**Endpoint:** `GET /api/chat/{chat_id}/messages`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| chat_id | integer | Chat ID |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 100 | Max messages to return |
| offset | integer | 0 | Pagination offset |

**Example Request:**

```bash
GET /api/chat/1/messages?limit=50
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "chat_id": 1,
    "role": "user",
    "content": "Hello, can you help me with Python?",
    "thinking_content": null,
    "tokens": 8,
    "thinking_tokens": null,
    "created_at": "2024-01-20T10:31:00Z",
    "pinned": false,
    "metadata": null
  },
  {
    "id": 2,
    "chat_id": 1,
    "role": "assistant",
    "content": "Of course! I'd be happy to help with Python.",
    "thinking_content": "The user wants Python help. I should be friendly and ask what specifically they need.",
    "tokens": 12,
    "thinking_tokens": 15,
    "created_at": "2024-01-20T10:31:05Z",
    "pinned": false,
    "metadata": {
      "model": "gpt-4",
      "temperature": 0.7
    }
  }
]
```

---

### Edit Message

Edit an existing message (typically user messages).

**Endpoint:** `PATCH /api/chat/{chat_id}/message/{message_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| chat_id | integer | Chat ID |
| message_id | integer | Message ID |

**Request Body:**

```json
{
  "content": "Updated message content"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "chat_id": 1,
  "role": "user",
  "content": "Updated message content",
  "thinking_content": null,
  "tokens": 4,
  "thinking_tokens": null,
  "created_at": "2024-01-20T10:31:00Z",
  "pinned": false,
  "metadata": null
}
```

---

### Delete Chat

Delete a chat and all its messages.

**Endpoint:** `DELETE /api/chat/{chat_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| chat_id | integer | Chat ID |

**Response:** `200 OK`

```json
{
  "status": "deleted",
  "chat_id": 1
}
```

**Error Response:** `404 Not Found`

```json
{
  "detail": "Chat not found"
}
```

---

## Models API

Manage AI models (local and API-based).

### List Models

Get all registered models.

**Endpoint:** `GET /api/models/`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by type: "local", "openai", "anthropic", "google" |

**Example Request:**

```bash
GET /api/models/?type=local
```

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Llama-2-7B-Chat-GGUF",
    "path": "/data/models/llama-2-7b-chat.Q4_K_M.gguf",
    "type": "local",
    "size": 4368080896,
    "context_length": 4096,
    "parameters": "7B",
    "metadata": {
      "quantization": "Q4_K_M",
      "architecture": "llama"
    },
    "created_at": "2024-01-20T09:00:00Z",
    "is_loaded": false
  },
  {
    "id": 2,
    "name": "GPT-4",
    "path": null,
    "type": "openai",
    "size": null,
    "context_length": 8192,
    "parameters": null,
    "metadata": {
      "supports_vision": true,
      "supports_functions": true
    },
    "created_at": "2024-01-20T09:00:00Z",
    "is_loaded": true
  }
]
```

---

### Get Model

Get details of a specific model.

**Endpoint:** `GET /api/models/{model_id}`

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Llama-2-7B-Chat-GGUF",
  "path": "/data/models/llama-2-7b-chat.Q4_K_M.gguf",
  "type": "local",
  "size": 4368080896,
  "context_length": 4096,
  "parameters": "7B",
  "metadata": {
    "quantization": "Q4_K_M",
    "architecture": "llama"
  },
  "created_at": "2024-01-20T09:00:00Z",
  "is_loaded": false
}
```

---

### Register Model

Add a new model to the registry.

**Endpoint:** `POST /api/models/`

**Request Body:**

```json
{
  "name": "Mistral-7B-Instruct",
  "path": "/data/models/mistral-7b-instruct.Q5_K_M.gguf",
  "type": "local",
  "context_length": 8192,
  "parameters": "7B",
  "metadata": {
    "quantization": "Q5_K_M",
    "architecture": "mistral"
  }
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Model display name |
| path | string | No | File path (required for local models) |
| type | string | Yes | Model type: "local", "openai", "anthropic", "google" |
| context_length | integer | No | Context window size |
| parameters | string | No | Model size (e.g., "7B", "13B") |
| metadata | object | No | Additional model information |

**Response:** `201 Created`

```json
{
  "id": 3,
  "name": "Mistral-7B-Instruct",
  "path": "/data/models/mistral-7b-instruct.Q5_K_M.gguf",
  "type": "local",
  "size": null,
  "context_length": 8192,
  "parameters": "7B",
  "metadata": {
    "quantization": "Q5_K_M",
    "architecture": "mistral"
  },
  "created_at": "2024-01-20T11:00:00Z",
  "is_loaded": false
}
```

---

### Delete Model

Remove a model from the registry (does not delete the file).

**Endpoint:** `DELETE /api/models/{model_id}`

**Response:** `200 OK`

```json
{
  "status": "deleted",
  "model_id": 3
}
```

---

### Load Model

Load a local model into memory for inference.

**Endpoint:** `POST /api/models/load`

**Request Body:**

```json
{
  "model_id": 1,
  "gpu_layers": 32,
  "threads": 8,
  "context_length": 4096
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| model_id | integer | Yes | Model ID to load |
| gpu_layers | integer | No | Number of layers to offload to GPU (0 = CPU only) |
| threads | integer | No | CPU threads to use |
| context_length | integer | No | Override context length |

**Response:** `200 OK` *(Not yet implemented - 501 error)*

---

### Unload Model

Unload a model from memory.

**Endpoint:** `POST /api/models/unload`

**Request Body:**

```json
{
  "model_id": 1
}
```

**Response:** `200 OK` *(Not yet implemented - 501 error)*

---

### Download Model

Download a model from HuggingFace or other source.

**Endpoint:** `POST /api/models/download`

**Request Body:**

```json
{
  "url": "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF",
  "quantization": "Q4_K_M"
}
```

**Response:** `200 OK` *(Not yet implemented - 501 error)*

Returns a download ID for tracking progress.

---

### Get Download Progress

Track download progress for a model.

**Endpoint:** `GET /api/models/download/{download_id}/progress`

**Response:** `200 OK` *(Not yet implemented - 501 error)*

```json
{
  "download_id": "abc123",
  "status": "downloading",
  "progress": 0.45,
  "downloaded_bytes": 1966080000,
  "total_bytes": 4368080896,
  "speed_mbps": 25.6,
  "eta_seconds": 95
}
```

---

## Embeddings API (RAG)

Upload documents and retrieve relevant chunks for Retrieval-Augmented Generation.

### Upload Document

Upload a document for embedding and retrieval.

**Endpoint:** `POST /api/embeddings/upload`

**Request:** Multipart form data

```bash
curl -X POST http://localhost:8000/api/embeddings/upload \
  -F "file=@document.pdf"
```

**Supported Formats:**
- Text: `.txt`, `.md`, `.csv`
- Documents: `.pdf`, `.docx`, `.rtf`
- Code: `.py`, `.js`, `.ts`, `.java`, `.cpp`, etc.
- Data: `.json`, `.xml`, `.yaml`

**Response:** `201 Created` *(Not yet implemented - 501 error)*

```json
{
  "id": 1,
  "name": "document.pdf",
  "type": "pdf",
  "path": "/data/uploads/document.pdf",
  "chunk_count": 42,
  "embedding_model": "all-MiniLM-L6-v2",
  "created_at": "2024-01-20T11:00:00Z",
  "metadata": {
    "pages": 10,
    "file_size": 1024000
  }
}
```

---

### List Knowledge Sources

Get all uploaded documents.

**Endpoint:** `GET /api/embeddings/sources`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| type | string | Filter by document type |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Python Documentation",
    "type": "pdf",
    "path": "/data/uploads/python-docs.pdf",
    "chunk_count": 42,
    "embedding_model": "all-MiniLM-L6-v2",
    "created_at": "2024-01-20T11:00:00Z",
    "metadata": {
      "pages": 10
    }
  }
]
```

---

### Get Knowledge Source

Get details of a specific document.

**Endpoint:** `GET /api/embeddings/sources/{source_id}`

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Python Documentation",
  "type": "pdf",
  "path": "/data/uploads/python-docs.pdf",
  "chunk_count": 42,
  "embedding_model": "all-MiniLM-L6-v2",
  "created_at": "2024-01-20T11:00:00Z",
  "metadata": {
    "pages": 10,
    "file_size": 1024000
  }
}
```

---

### Delete Knowledge Source

Delete a document and its embeddings.

**Endpoint:** `DELETE /api/embeddings/sources/{source_id}`

**Response:** `200 OK`

```json
{
  "status": "deleted",
  "source_id": 1
}
```

---

### Retrieve Chunks

Retrieve relevant document chunks for a query.

**Endpoint:** `POST /api/embeddings/retrieve`

**Request Body:**

```json
{
  "query": "How do I use list comprehensions in Python?",
  "max_chunks": 5,
  "min_relevance": 0.7
}
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| query | string | Yes | - | Search query |
| max_chunks | integer | No | 5 | Maximum chunks to return (1-20) |
| min_relevance | float | No | 0.5 | Minimum relevance score (0.0-1.0) |

**Response:** `200 OK` *(Not yet implemented - 501 error)*

```json
[
  {
    "content": "List comprehensions provide a concise way to create lists...",
    "source_id": 1,
    "source_name": "Python Documentation",
    "metadata": {
      "page": 5,
      "section": "Data Structures"
    },
    "relevance_score": 0.92
  },
  {
    "content": "The syntax for list comprehensions is [expression for item in iterable]...",
    "source_id": 1,
    "source_name": "Python Documentation",
    "metadata": {
      "page": 5,
      "section": "Data Structures"
    },
    "relevance_score": 0.87
  }
]
```

---

### Reindex Document

Re-embed and reindex a document with new settings.

**Endpoint:** `POST /api/embeddings/reindex/{source_id}`

**Response:** `200 OK` *(Not yet implemented - 501 error)*

---

## LoRA API

Manage LoRA (Low-Rank Adaptation) adapters for local models.

### List LoRAs

Get all registered LoRA adapters.

**Endpoint:** `GET /api/lora/`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| model_id | integer | Filter by compatible model |
| enabled_only | boolean | Only show enabled LoRAs |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Python Coding LoRA",
    "path": "/data/loras/python-coding.bin",
    "compatible_models": [1, 3],
    "weight": 1.0,
    "enabled": true,
    "metadata": {
      "base_model": "Llama-2-7B",
      "training_data": "Python code"
    },
    "created_at": "2024-01-20T10:00:00Z"
  }
]
```

---

### Get LoRA

Get details of a specific LoRA adapter.

**Endpoint:** `GET /api/lora/{lora_id}`

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Python Coding LoRA",
  "path": "/data/loras/python-coding.bin",
  "compatible_models": [1, 3],
  "weight": 1.0,
  "enabled": true,
  "metadata": {
    "base_model": "Llama-2-7B",
    "training_data": "Python code"
  },
  "created_at": "2024-01-20T10:00:00Z"
}
```

---

### Register LoRA

Add a new LoRA adapter.

**Endpoint:** `POST /api/lora/`

**Request Body:**

```json
{
  "name": "Creative Writing LoRA",
  "path": "/data/loras/creative-writing.bin",
  "compatible_models": [1],
  "weight": 1.0,
  "metadata": {
    "base_model": "Llama-2-7B",
    "description": "Improves creative writing"
  }
}
```

**Response:** `201 Created`

```json
{
  "id": 2,
  "name": "Creative Writing LoRA",
  "path": "/data/loras/creative-writing.bin",
  "compatible_models": [1],
  "weight": 1.0,
  "enabled": false,
  "metadata": {
    "base_model": "Llama-2-7B",
    "description": "Improves creative writing"
  },
  "created_at": "2024-01-20T11:30:00Z"
}
```

---

### Update LoRA

Update LoRA weight or enabled status.

**Endpoint:** `PATCH /api/lora/{lora_id}`

**Request Body:**

```json
{
  "weight": 1.5,
  "enabled": true
}
```

**Response:** `200 OK`

```json
{
  "id": 2,
  "name": "Creative Writing LoRA",
  "path": "/data/loras/creative-writing.bin",
  "compatible_models": [1],
  "weight": 1.5,
  "enabled": true,
  "metadata": {
    "base_model": "Llama-2-7B",
    "description": "Improves creative writing"
  },
  "created_at": "2024-01-20T11:30:00Z"
}
```

---

### Delete LoRA

Remove a LoRA from the registry (does not delete the file).

**Endpoint:** `DELETE /api/lora/{lora_id}`

**Response:** `200 OK`

```json
{
  "status": "deleted",
  "lora_id": 2
}
```

---

### Apply LoRA

Apply a LoRA to a loaded model.

**Endpoint:** `POST /api/lora/{lora_id}/apply`

**Request Body:**

```json
{
  "model_id": 1
}
```

**Response:** `200 OK` *(Not yet implemented - 501 error)*

---

### Remove LoRA

Remove a LoRA from a loaded model.

**Endpoint:** `POST /api/lora/{lora_id}/remove`

**Request Body:**

```json
{
  "model_id": 1
}
```

**Response:** `200 OK` *(Not yet implemented - 501 error)*

---

## System Prompts API

Manage the system prompt library.

### List System Prompts

Get all system prompts.

**Endpoint:** `GET /api/system-prompts/`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| tag | string | Filter by tag |
| search | string | Search in name/description |
| limit | integer | Max results (default: 50) |
| offset | integer | Pagination offset |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Code Assistant",
    "description": "Expert programmer providing clean, well-documented code",
    "prompt": "You are an expert programmer...",
    "tags": ["code", "technical"],
    "icon": "💻",
    "usage_count": 42,
    "default_settings": {
      "temperature": 0.3,
      "model_type": "gpt-4"
    },
    "created_at": "2024-01-20T09:00:00Z",
    "updated_at": "2024-01-20T09:00:00Z"
  }
]
```

---

### Get System Prompt

Get a specific system prompt.

**Endpoint:** `GET /api/system-prompts/{prompt_id}`

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Code Assistant",
  "description": "Expert programmer providing clean, well-documented code",
  "prompt": "You are an expert programmer with deep knowledge of software engineering best practices...",
  "tags": ["code", "technical"],
  "icon": "💻",
  "usage_count": 42,
  "default_settings": {
    "temperature": 0.3,
    "model_type": "gpt-4"
  },
  "created_at": "2024-01-20T09:00:00Z",
  "updated_at": "2024-01-20T09:00:00Z"
}
```

---

### Create System Prompt

Create a new system prompt.

**Endpoint:** `POST /api/system-prompts/`

**Request Body:**

```json
{
  "name": "Research Assistant",
  "description": "Analytical researcher with focus on evidence",
  "prompt": "You are a meticulous research assistant...",
  "tags": ["research", "academic"],
  "icon": "🔬",
  "default_settings": {
    "temperature": 0.4,
    "rag_enabled": true
  }
}
```

**Response:** `201 Created`

```json
{
  "id": 5,
  "name": "Research Assistant",
  "description": "Analytical researcher with focus on evidence",
  "prompt": "You are a meticulous research assistant...",
  "tags": ["research", "academic"],
  "icon": "🔬",
  "usage_count": 0,
  "default_settings": {
    "temperature": 0.4,
    "rag_enabled": true
  },
  "created_at": "2024-01-20T12:00:00Z",
  "updated_at": "2024-01-20T12:00:00Z"
}
```

---

### Update System Prompt

Update an existing system prompt.

**Endpoint:** `PUT /api/system-prompts/{prompt_id}`

**Request Body:** (all fields optional)

```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "prompt": "Updated prompt text...",
  "tags": ["new", "tags"],
  "icon": "🆕",
  "default_settings": {
    "temperature": 0.5
  }
}
```

**Response:** `200 OK`

---

### Delete System Prompt

Delete a system prompt.

**Endpoint:** `DELETE /api/system-prompts/{prompt_id}`

**Response:** `200 OK`

```json
{
  "status": "deleted",
  "prompt_id": 5
}
```

---

### Increment Usage Count

Increment the usage counter for a prompt (called when used in chat).

**Endpoint:** `POST /api/system-prompts/{prompt_id}/use`

**Response:** `200 OK`

```json
{
  "status": "incremented",
  "usage_count": 43
}
```

---

## WebSocket API

Real-time streaming chat interface.

### WebSocket Chat Stream

**Endpoint:** `WS /api/chat/stream`

**Protocol:** WebSocket

**Connection:**

```javascript
const ws = new WebSocket('ws://localhost:8000/api/chat/stream');
```

### Client → Server Messages

**Send Message:**

```json
{
  "type": "message",
  "chat_id": 1,
  "content": "Hello, how are you?",
  "model_id": 2,
  "system_prompt_id": 1,
  "settings": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 0.9
  },
  "rag_enabled": false
}
```

**Stop Generation:**

```json
{
  "type": "stop"
}
```

### Server → Client Messages

**Token Stream:**

```json
{
  "type": "token",
  "content": "Hello",
  "is_thinking": false
}
```

**Thinking Token:**

```json
{
  "type": "token",
  "content": "Let me consider...",
  "is_thinking": true
}
```

**Metadata:**

```json
{
  "type": "metadata",
  "tokens": 156,
  "thinking_tokens": 42,
  "model": "gpt-4",
  "finish_reason": "stop"
}
```

**Complete:**

```json
{
  "type": "complete",
  "message_id": 42,
  "chat_id": 1
}
```

**Error:**

```json
{
  "type": "error",
  "error": "Model not loaded",
  "code": "MODEL_NOT_LOADED"
}
```

**Status Update:**

```json
{
  "type": "status",
  "status": "generating",
  "progress": 0.35
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `MODEL_NOT_LOADED` | Selected model is not loaded |
| `CONTEXT_LIMIT_EXCEEDED` | Message exceeds context limit |
| `INVALID_REQUEST` | Malformed request data |
| `GENERATION_FAILED` | Model failed to generate response |
| `RATE_LIMIT` | Too many requests |

---

## Health & Status

### Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:** `200 OK`

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-01-20T12:00:00Z"
}
```

---

### API Documentation

**Interactive API Docs:** http://localhost:8000/docs

**ReDoc Documentation:** http://localhost:8000/redoc

---

## Rate Limiting

Currently, no rate limiting is implemented as AI Studio is a local application. Future versions may include configurable rate limits for API endpoints.

---

## Versioning

The API follows semantic versioning. Breaking changes will be introduced in new major versions with appropriate migration guides.

Current version: **v1** (implicit in endpoints)

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/zusamstone/congenial-doodle/issues
- Documentation: https://github.com/zusamstone/congenial-doodle/docs

---

**Last Updated:** January 2024
