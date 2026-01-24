# AI Studio Developer Guide

Comprehensive guide for developers who want to contribute to or build upon AI Studio.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Running in Development Mode](#running-in-development-mode)
- [Code Organization](#code-organization)
- [Adding New Features](#adding-new-features)
- [Testing Guidelines](#testing-guidelines)
- [Code Style](#code-style)
- [Database Management](#database-management)
- [API Development](#api-development)
- [Frontend Development](#frontend-development)
- [Build & Packaging](#build--packaging)
- [Pull Request Process](#pull-request-process)
- [Debugging](#debugging)

---

## Development Environment Setup

### Prerequisites

**Required**:
- Node.js 18+ and npm 9+
- Python 3.11+
- Git

**Recommended**:
- VS Code (or your preferred IDE)
- GPU with CUDA/ROCm support (for local model development)
- At least 16GB RAM (32GB recommended)

### Initial Setup

1. **Clone the repository**:
```bash
git clone https://github.com/zusamstone/congenial-doodle.git
cd congenial-doodle
```

2. **Install dependencies**:
```bash
npm run install-all
```

This installs:
- Root workspace dependencies
- Frontend dependencies (React, Vite, TypeScript)
- Backend dependencies (FastAPI, llama-cpp-python, etc.)
- Electron dependencies

3. **Create environment file**:
```bash
cd backend
cp .env.example .env
```

Edit `.env` with your settings:
```bash
# Server
HOST=127.0.0.1
PORT=8000
DEBUG=true

# Paths
DATA_DIR=./data
MODELS_DIR=./data/models

# API Keys (optional for development)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

4. **Initialize database**:
```bash
cd backend
python run.py
```

First run will create SQLite database and initialize tables.

### IDE Setup

**VS Code Extensions** (Recommended):
- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- TypeScript Vue Plugin (Volar)
- SQLite Viewer

**VS Code Settings** (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

---

## Project Structure

```
congenial-doodle/
├── electron/                    # Electron main process
│   ├── main.js                 # Electron entry point
│   ├── preload.js              # Preload scripts
│   └── build/                  # Build configurations
│
├── frontend/                    # React TypeScript UI
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom hooks
│   │   ├── utils/              # Utility functions
│   │   ├── types/              # TypeScript types
│   │   └── styles/             # CSS/Tailwind styles
│   ├── public/                 # Static assets
│   ├── index.html              # HTML template
│   ├── package.json            # Frontend dependencies
│   └── vite.config.ts          # Vite configuration
│
├── backend/                     # Python FastAPI server
│   ├── api/                    # API routes
│   │   ├── routes/             # Route handlers
│   │   │   ├── chat.py
│   │   │   ├── models.py
│   │   │   ├── embeddings.py
│   │   │   ├── lora.py
│   │   │   └── system_prompts.py
│   │   └── middleware/         # API middleware
│   │
│   ├── database/               # Database layer
│   │   ├── db.py              # Connection management
│   │   ├── models.py          # SQLAlchemy models
│   │   └── migrations/        # DB migrations
│   │
│   ├── models/                 # Model management
│   │   ├── local.py           # llama.cpp integration
│   │   ├── openai.py          # OpenAI API
│   │   ├── anthropic.py       # Anthropic API
│   │   └── google.py          # Google API
│   │
│   ├── embeddings/             # RAG & embeddings
│   │   ├── chunker.py         # Text chunking
│   │   ├── embedder.py        # Embedding generation
│   │   └── retriever.py       # Vector search
│   │
│   ├── context/                # Context management
│   │   ├── strategies.py      # Context strategies
│   │   └── summarizer.py      # Summarization
│   │
│   ├── guidance/               # Output guidance
│   │   ├── cfg.py             # Classifier-Free Guidance
│   │   └── logit_bias.py      # Logit biasing
│   │
│   ├── monitoring/             # Resource monitoring
│   │   └── hardware.py        # CPU/GPU/RAM monitoring
│   │
│   ├── utils/                  # Utilities
│   │   ├── config.py          # Configuration
│   │   ├── paths.py           # Path management
│   │   └── logger.py          # Logging setup
│   │
│   ├── main.py                 # FastAPI app
│   ├── run.py                  # Development server
│   └── requirements.txt        # Python dependencies
│
├── config/                      # Default configurations
│   ├── system_prompts.json     # Built-in prompts
│   └── settings.json           # Default settings
│
├── data/                        # Runtime data (gitignored)
│   ├── models/                 # Downloaded models
│   ├── loras/                  # LoRA adapters
│   ├── vector_store/           # ChromaDB data
│   ├── database/               # SQLite databases
│   ├── uploads/                # User uploads
│   ├── chats/                  # Exported chats
│   └── logs/                   # Application logs
│
├── docs/                        # Documentation
│   ├── API.md
│   ├── USER_GUIDE.md
│   ├── DEVELOPER_GUIDE.md      # This file
│   ├── CONTEXT_MANAGEMENT.md
│   ├── RAG_SETUP.md
│   └── CONTRIBUTING.md
│
├── package.json                 # Root workspace config
├── README.md
├── FEATURES.md
├── ARCHITECTURE.md
├── ROADMAP.md
└── LICENSE
```

---

## Running in Development Mode

### Start All Services

**Option 1: Single command** (recommended):
```bash
npm run dev
```

This starts:
- Backend (FastAPI) on http://localhost:8000
- Frontend (Vite) on http://localhost:5173
- Electron desktop app

**Option 2: Individual services**:

Terminal 1 - Backend:
```bash
cd backend
python run.py
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Terminal 3 - Electron:
```bash
npm run electron:dev
```

### Access Points

- **Frontend Dev Server**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Hot Reload

**Backend**:
- Edit Python files → auto-reloads
- See changes immediately

**Frontend**:
- Edit React/TypeScript files → Vite HMR
- Changes reflect instantly in browser

**Electron**:
- Edit electron/main.js → restart electron
- Frontend changes work with HMR

---

## Code Organization

### Backend Architecture

**Layered Architecture**:
```
Routes (API) → Services → Database
              ↓
           External APIs (OpenAI, etc.)
```

**Route Handlers** (`api/routes/`):
- Handle HTTP requests
- Validate input (Pydantic)
- Call services
- Return responses

**Services** (various modules):
- Business logic
- Model management
- Embedding generation
- Context strategies

**Database** (`database/`):
- SQLAlchemy models
- Database operations
- Migrations

### Frontend Architecture

**Component Structure**:
```
Pages → Containers → Components → Atoms
```

**Pages** (`pages/`):
- Top-level routes
- Page layouts

**Containers** (in `components/`):
- Feature containers
- State management
- Business logic

**Components** (`components/`):
- Reusable UI components
- Presentational only

**Hooks** (`hooks/`):
- Custom React hooks
- Shared logic
- API calls

**Types** (`types/`):
- TypeScript interfaces
- Type definitions

### Naming Conventions

**Python**:
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

**TypeScript/React**:
- Files: `PascalCase.tsx` for components, `camelCase.ts` for utils
- Components: `PascalCase`
- Functions/variables: `camelCase`
- Constants: `UPPER_SNAKE_CASE`
- Interfaces: `PascalCase` (prefix with `I` optional)

---

## Adding New Features

### Backend Feature

**Example: Add new API endpoint**

1. **Create route handler** (`backend/api/routes/my_feature.py`):
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db

router = APIRouter()

@router.get("/my-feature")
async def get_my_feature(db: AsyncSession = Depends(get_db)):
    """Get my feature data"""
    # Implementation
    return {"status": "success"}
```

2. **Register route** (`backend/main.py`):
```python
from api.routes import my_feature

app.include_router(
    my_feature.router,
    prefix="/api/my-feature",
    tags=["my-feature"]
)
```

3. **Add database model** if needed (`backend/database/models.py`):
```python
class MyFeature(Base):
    __tablename__ = "my_features"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(JSON)
```

4. **Create migration**:
```bash
# Manually create migration or use Alembic
# For now, drop data/ and restart for dev
```

5. **Test endpoint**:
```bash
curl http://localhost:8000/api/my-feature
```

### Frontend Feature

**Example: Add new component**

1. **Create component** (`frontend/src/components/MyFeature.tsx`):
```typescript
import React from 'react';

interface MyFeatureProps {
  title: string;
  onAction: () => void;
}

export const MyFeature: React.FC<MyFeatureProps> = ({ title, onAction }) => {
  return (
    <div className="my-feature">
      <h2>{title}</h2>
      <button onClick={onAction}>Do Action</button>
    </div>
  );
};
```

2. **Add types** (`frontend/src/types/myFeature.ts`):
```typescript
export interface MyFeatureData {
  id: number;
  name: string;
  data: unknown;
}
```

3. **Create API hook** (`frontend/src/hooks/useMyFeature.ts`):
```typescript
import { useState, useEffect } from 'react';
import { MyFeatureData } from '../types/myFeature';

export const useMyFeature = () => {
  const [data, setData] = useState<MyFeatureData | null>(null);
  const [loading, setLoading] = useState(false);
  
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/my-feature');
      const result = await response.json();
      setData(result);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchData();
  }, []);
  
  return { data, loading, refetch: fetchData };
};
```

4. **Use in page**:
```typescript
import { MyFeature } from '../components/MyFeature';
import { useMyFeature } from '../hooks/useMyFeature';

export const MyPage = () => {
  const { data, loading } = useMyFeature();
  
  if (loading) return <div>Loading...</div>;
  
  return <MyFeature title={data?.name} onAction={() => {}} />;
};
```

---

## Testing Guidelines

### Backend Testing

**Test Structure**:
```
backend/
├── tests/
│   ├── test_api/
│   │   ├── test_chat.py
│   │   ├── test_models.py
│   │   └── test_embeddings.py
│   ├── test_services/
│   └── test_utils/
└── conftest.py  # Pytest fixtures
```

**Run tests**:
```bash
cd backend
pytest                    # All tests
pytest tests/test_api/    # Specific directory
pytest -v                 # Verbose
pytest --cov              # With coverage
```

**Example test** (`backend/tests/test_api/test_chat.py`):
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
async def test_list_chats():
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
    """Create test database"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        yield session
    
    await engine.dispose()
```

### Frontend Testing

**Test Structure**:
```
frontend/
├── src/
│   ├── components/
│   │   ├── MyComponent.tsx
│   │   └── MyComponent.test.tsx
└── tests/
```

**Run tests**:
```bash
cd frontend
npm run test          # Run tests
npm run test:watch    # Watch mode
npm run test:coverage # With coverage
```

**Example test** (`frontend/src/components/MyComponent.test.tsx`):
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './MyComponent';

describe('MyComponent', () => {
  it('renders with title', () => {
    render(<MyComponent title="Test" />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });
  
  it('calls onAction when button clicked', () => {
    const onAction = jest.fn();
    render(<MyComponent title="Test" onAction={onAction} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(onAction).toHaveBeenCalled();
  });
});
```

### Integration Testing

Test full workflows:
```python
@pytest.mark.asyncio
async def test_chat_workflow():
    """Test creating chat and sending message"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create chat
        response = await client.post("/api/chat/", json={"title": "Test"})
        chat_id = response.json()["id"]
        
        # Get messages (should be empty)
        response = await client.get(f"/api/chat/{chat_id}/messages")
        assert len(response.json()) == 0
        
        # TODO: Send message via WebSocket
        # TODO: Verify message saved
```

---

## Code Style

### Python

**Follow PEP 8** with these tools:

**Black** (code formatter):
```bash
black backend/
```

**Ruff** (linter):
```bash
ruff check backend/
ruff check --fix backend/  # Auto-fix
```

**Type hints**:
```python
from typing import List, Optional

def process_messages(
    messages: List[dict],
    max_length: Optional[int] = None
) -> str:
    """Process messages and return summary"""
    # Implementation
    return summary
```

**Docstrings** (Google style):
```python
def calculate_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Calculate token count for text.
    
    Args:
        text: Input text to count
        model: Model name for tokenizer
    
    Returns:
        Number of tokens
    
    Raises:
        ValueError: If model not supported
    """
    pass
```

### TypeScript/React

**ESLint & Prettier**:
```bash
cd frontend
npm run lint           # Check
npm run lint:fix       # Fix
npm run format         # Format with Prettier
```

**TypeScript best practices**:
```typescript
// Use interfaces for props
interface ComponentProps {
  title: string;
  count?: number;  // Optional
  onClick: () => void;
}

// Use type for unions/aliases
type Status = 'idle' | 'loading' | 'success' | 'error';

// Avoid 'any'
const data: unknown = fetchData();
if (isMyData(data)) {
  // Now TypeScript knows the type
  console.log(data.field);
}
```

**React patterns**:
```typescript
// Functional components with FC
export const MyComponent: React.FC<Props> = ({ title }) => {
  return <div>{title}</div>;
};

// Custom hooks start with 'use'
export const useCustomHook = () => {
  // Hook logic
};

// Event handlers named 'handle...'
const handleClick = () => {
  // Handle click
};
```

---

## Database Management

### SQLAlchemy Models

Define models in `backend/database/models.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from database.db import Base

class MyModel(Base):
    __tablename__ = "my_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    data = Column(JSON)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Database Operations

**Create**:
```python
async def create_item(db: AsyncSession, name: str):
    item = MyModel(name=name)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
```

**Read**:
```python
from sqlalchemy import select

async def get_items(db: AsyncSession):
    result = await db.execute(select(MyModel))
    return result.scalars().all()

async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(MyModel).where(MyModel.id == item_id)
    )
    return result.scalar_one_or_none()
```

**Update**:
```python
async def update_item(db: AsyncSession, item_id: int, name: str):
    result = await db.execute(
        select(MyModel).where(MyModel.id == item_id)
    )
    item = result.scalar_one_or_none()
    if item:
        item.name = name
        await db.commit()
        await db.refresh(item)
    return item
```

**Delete**:
```python
async def delete_item(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(MyModel).where(MyModel.id == item_id)
    )
    item = result.scalar_one_or_none()
    if item:
        await db.delete(item)
        await db.commit()
```

### Migrations

For schema changes, currently need to:

1. Modify model in `models.py`
2. Delete test database: `rm data/database/ai_studio.db`
3. Restart server to recreate

**TODO**: Implement Alembic migrations

---

## API Development

### Creating Endpoints

**RESTful conventions**:
- `GET /api/resource` - List all
- `GET /api/resource/{id}` - Get one
- `POST /api/resource` - Create
- `PUT /api/resource/{id}` - Update (full)
- `PATCH /api/resource/{id}` - Update (partial)
- `DELETE /api/resource/{id}` - Delete

**Example**:
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

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
    """Create a new item"""
    new_item = MyModel(**item.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get item by ID"""
    result = await db.execute(
        select(MyModel).where(MyModel.id == item_id)
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item
```

### Error Handling

```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input"
)

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# 500 Internal Server Error
try:
    # Risky operation
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal error"
    )
```

### WebSocket Development

```python
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive
            data = await websocket.receive_json()
            
            # Process
            result = await process_message(data)
            
            # Send response
            await websocket.send_json(result)
            
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011)
```

---

## Frontend Development

### Component Development

**Atomic design pattern**:

**Atoms** (smallest):
```typescript
export const Button: React.FC<ButtonProps> = ({ children, onClick }) => (
  <button className="btn" onClick={onClick}>
    {children}
  </button>
);
```

**Molecules** (combine atoms):
```typescript
export const SearchBox: React.FC = () => (
  <div className="search-box">
    <Input placeholder="Search..." />
    <Button>Search</Button>
  </div>
);
```

**Organisms** (complex features):
```typescript
export const ChatMessage: React.FC<MessageProps> = ({ message }) => (
  <div className="chat-message">
    <Avatar user={message.user} />
    <MessageContent content={message.content} />
    <MessageActions onCopy={} onEdit={} />
  </div>
);
```

### State Management

**Local state** (useState):
```typescript
const [count, setCount] = useState(0);
```

**Context** (for shared state):
```typescript
// Create context
export const ThemeContext = createContext<Theme>('dark');

// Provider
export const ThemeProvider: React.FC = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('dark');
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Consumer
const { theme } = useContext(ThemeContext);
```

**Consider**: Zustand or Redux for complex state

### API Integration

```typescript
// API client
const API_BASE = 'http://localhost:8000/api';

export const api = {
  async getChats(): Promise<Chat[]> {
    const response = await fetch(`${API_BASE}/chat`);
    if (!response.ok) throw new Error('Failed to fetch chats');
    return response.json();
  },
  
  async createChat(title: string): Promise<Chat> {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    });
    if (!response.ok) throw new Error('Failed to create chat');
    return response.json();
  },
};

// Hook
export const useChats = () => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [loading, setLoading] = useState(false);
  
  const fetchChats = async () => {
    setLoading(true);
    try {
      const data = await api.getChats();
      setChats(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchChats();
  }, []);
  
  return { chats, loading, refetch: fetchChats };
};
```

---

## Build & Packaging

### Development Build

```bash
npm run build
```

Builds:
- Frontend (Vite) → `frontend/dist`
- Backend bundled with PyInstaller
- Electron packaged

### Production Packaging

**Windows**:
```bash
npm run package:win
```
Creates portable `.exe` in `dist/`

**macOS**:
```bash
npm run package:mac
```
Creates `.app` bundle in `dist/`

**Linux**:
```bash
npm run package:linux
```
Creates AppImage in `dist/`

**All platforms**:
```bash
npm run package:all
```

### electron-builder Configuration

`package.json`:
```json
{
  "build": {
    "appId": "com.aistudio.app",
    "productName": "AI Studio",
    "files": [
      "electron/**/*",
      "frontend/dist/**/*",
      "backend/dist/**/*"
    ],
    "directories": {
      "output": "dist"
    },
    "win": {
      "target": "portable"
    },
    "mac": {
      "target": "dmg"
    },
    "linux": {
      "target": "AppImage"
    }
  }
}
```

---

## Pull Request Process

### Before Submitting

1. **Create feature branch**:
```bash
git checkout -b feature/my-feature
```

2. **Make changes**:
- Write code
- Add tests
- Update documentation

3. **Run checks**:
```bash
# Backend
cd backend
black .
ruff check .
pytest

# Frontend
cd frontend
npm run lint:fix
npm run test
npm run build
```

4. **Commit**:
```bash
git add .
git commit -m "feat: Add my feature"
```

**Commit message format**:
- `feat: ` - New feature
- `fix: ` - Bug fix
- `docs: ` - Documentation
- `style: ` - Formatting
- `refactor: ` - Code refactoring
- `test: ` - Tests
- `chore: ` - Maintenance

5. **Push**:
```bash
git push origin feature/my-feature
```

### Creating PR

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
```

5. Submit PR

### Code Review

- Address reviewer comments
- Make requested changes
- Push updates to same branch
- PR automatically updates

### Merging

Once approved:
- Squash and merge (preferred)
- Delete branch after merge

---

## Debugging

### Backend Debugging

**Logs**:
```bash
tail -f data/logs/ai_studio.log
```

**Print debugging**:
```python
from loguru import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning")
logger.error("Error occurred")
```

**VS Code debugger**:

`.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "DEBUG": "true"
      }
    }
  ]
}
```

**Breakpoints**:
```python
# Set breakpoint in VS Code
# Or use:
import pdb; pdb.set_trace()
```

### Frontend Debugging

**Browser DevTools**:
- Console for logs
- Network tab for API calls
- React DevTools extension

**Console logging**:
```typescript
console.log('Data:', data);
console.error('Error:', error);
console.table(arrayOfObjects);
```

**VS Code debugger**:

`.vscode/launch.json`:
```json
{
  "name": "Chrome Debug",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/frontend"
}
```

### Database Debugging

**View database**:
```bash
sqlite3 data/database/ai_studio.db

# Inside sqlite3:
.tables                    # List tables
.schema chats             # View schema
SELECT * FROM chats;      # Query data
```

**Or use SQLite Viewer extension in VS Code**

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Electron Documentation**: https://www.electronjs.org/docs
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **llama.cpp**: https://github.com/ggerganov/llama.cpp

---

**Questions?** Open an issue or discussion on GitHub!

**Happy coding! 🚀**
