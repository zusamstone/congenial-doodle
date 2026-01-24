# AI Studio

<div align="center">
  <h3>A Powerful, Local-First AI Chat Application</h3>
  <p>Privacy-focused desktop application with support for local models and cloud APIs</p>
</div>

## 🚀 Features

- **🎨 Beautiful Chat Interface**: LM Studio-style dark theme with sidebar navigation
- **🤖 Multi-Model Support**: Local models (llama.cpp) and cloud APIs (OpenAI, Anthropic, Google, Ollama)
- **📚 System Prompts Library**: Pre-configured personas and instructions for different use cases
- **🧠 Smart Context Management**: 4 strategies including summarization, rolling window, and periodic summaries
- **📖 RAG (Retrieval Augmented Generation)**: Upload documents and chat with your knowledge base
- **🎯 LoRA Support**: Load and manage multiple LoRAs for fine-tuned local models
- **🎛️ Advanced Guidance**: System prompt integration, CFG, and logit bias
- **👥 User Experience Modes**: General, Power User, and Developer modes with appropriate controls
- **🤔 Thinking Models**: Special support for reasoning models (o1, o3, DeepSeek R1)
- **📊 Resource Monitoring**: Real-time CPU/GPU/RAM/VRAM tracking
- **💾 Portable by Default**: All data in app directory, easy to move between computers
- **🔒 Privacy First**: No telemetry, offline-capable, local processing

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Building from Source](#building-from-source)
- [Technology Stack](#technology-stack)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Quick Start

### Prerequisites

- **Node.js** 18+ and npm 9+
- **Python** 3.11+
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zusamstone/congenial-doodle.git
   cd congenial-doodle
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Run the application**
   ```bash
   npm run dev
   ```

   This will start:
   - Frontend (React + Vite) on `http://localhost:5173`
   - Backend (FastAPI) on `http://localhost:8000`
   - Electron desktop application

## 🔧 Building from Source

### Development Build

```bash
# Install dependencies
npm run install-all

# Run in development mode
npm run dev
```

### Production Build

```bash
# Build frontend and backend
npm run build

# Package for your platform
npm run package:win    # Windows portable
npm run package:mac    # macOS .app
npm run package:linux  # Linux AppImage
npm run package:all    # All platforms
```

### Platform-Specific Notes

**Windows**:
- Portable .exe file, no installation required
- All data stored in app directory

**macOS**:
- .app bundle, drag to Applications
- Sign and notarize for distribution (see docs)

**Linux**:
- AppImage for maximum compatibility
- Or build .deb/.rpm packages

## 🛠️ Technology Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling
- **React Markdown** - Message rendering
- **Monaco Editor** - Code display

### Desktop
- **Electron** - Cross-platform desktop framework
- **electron-builder** - Packaging and distribution

### Backend
- **Python 3.11+** - Backend language
- **FastAPI** - REST API framework
- **llama-cpp-python** - Local model inference
- **ChromaDB** - Vector database for embeddings
- **SQLite** - Metadata and chat history
- **SQLAlchemy** - Database ORM

### AI/ML
- **llama.cpp** - Efficient local inference
- **sentence-transformers** - Embeddings
- **tiktoken** - Token counting
- **OpenAI SDK** - Cloud API integration
- **Anthropic SDK** - Claude API integration

## 📚 Documentation

- **[FEATURES.md](docs/FEATURES.md)** - Complete feature documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design
- **[ROADMAP.md](docs/ROADMAP.md)** - Development roadmap and phases
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - End-user guide
- **[DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** - Development setup and contributing
- **[API.md](docs/API.md)** - Backend API documentation
- **[CONTEXT_MANAGEMENT.md](docs/CONTEXT_MANAGEMENT.md)** - Context strategies deep dive
- **[RAG_SETUP.md](docs/RAG_SETUP.md)** - Setting up knowledge bases
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - How to contribute

## 📁 Project Structure

```
congenial-doodle/
├── electron/          # Electron main process and build config
├── frontend/          # React + TypeScript UI
├── backend/           # Python FastAPI server
├── config/            # Default configurations
├── docs/              # Documentation
├── data/              # Runtime data (gitignored)
│   ├── models/        # Downloaded models
│   ├── loras/         # LoRA adapters
│   ├── vector_store/  # ChromaDB data
│   ├── database/      # SQLite databases
│   ├── uploads/       # User uploaded files
│   └── chats/         # Exported chats
└── package.json       # Root workspace config
```

## 🎨 Screenshots

*Coming soon - screenshots will be added as features are implemented*

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `npm run test`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **llama.cpp** - For efficient local inference
- **LM Studio** - UI inspiration
- **FastAPI** - Excellent Python web framework
- **Electron** - Cross-platform desktop capabilities
- All the open-source AI/ML libraries that make this possible

## 🔗 Links

- [GitHub Repository](https://github.com/zusamstone/congenial-doodle)
- [Issue Tracker](https://github.com/zusamstone/congenial-doodle/issues)
- [Discussions](https://github.com/zusamstone/congenial-doodle/discussions)

## ⭐ Support

If you find this project useful, please consider giving it a star on GitHub!