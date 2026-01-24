# AI Studio - Features Documentation

This document provides a comprehensive overview of all features in AI Studio.

## Table of Contents

- [Chat Interface](#chat-interface)
- [System Prompts Library](#system-prompts-library)
- [User Experience Modes](#user-experience-modes)
- [Context Management](#context-management)
- [Thinking Models Support](#thinking-models-support)
- [Embeddings & RAG](#embeddings--rag)
- [LoRA Support](#lora-support)
- [Guidance System](#guidance-system)
- [Model Management](#model-management)
- [Resource Monitoring](#resource-monitoring)
- [Chat Management](#chat-management)
- [Portable Mode](#portable-mode)

## Chat Interface

### Overview
A beautiful, dark-themed chat interface inspired by LM Studio with a focus on usability and productivity.

### Features

#### Sidebar Navigation
- **Chat Sessions**: View and switch between multiple chat sessions
- **System Prompts**: Quick access to prompt library
- **Settings**: Model selection and configuration
- **Knowledge Base**: RAG document management

#### Message Display
- **Markdown Rendering**: Full markdown support with syntax highlighting
- **Code Blocks**: Syntax highlighting for 100+ languages
- **LaTeX Math**: Render mathematical equations (inline and block)
- **Tables**: Properly formatted tables
- **Images**: Display image attachments

#### Message Actions
- **Copy**: Copy message content to clipboard
- **Edit**: Edit and resend messages
- **Regenerate**: Regenerate AI responses
- **Delete**: Remove messages from conversation
- **Pin**: Pin important messages (never summarized)

#### Input Features
- **Rich Text Input**: Multi-line text area with auto-resize
- **File Attachments**: Upload documents, images, code files
- **Keyboard Shortcuts**:
  - `Ctrl+Enter`: Send message
  - `Ctrl+N`: New chat
  - `Ctrl+K`: Focus search
  - `Ctrl+/`: Toggle sidebar
  - `Ctrl+,`: Open settings

#### Streaming
- **Real-time Streaming**: See AI responses as they're generated
- **Stop Generation**: Interrupt long generations
- **Partial Regeneration**: Edit and regenerate from any point

## System Prompts Library

### Overview
Organized collection of pre-configured personas and instructions for different use cases.

### Prompt Structure
Each system prompt includes:
- **Name**: Short, descriptive name
- **Icon**: Emoji or icon identifier
- **Description**: What the prompt is good for
- **Full Prompt**: The actual system instruction
- **Tags**: Categorization (e.g., "code", "creative", "professional")
- **Usage Stats**: How many times used
- **Default Settings**: Preferred model, temperature, etc.

### Built-in Templates

#### Professional Assistant
- Formal, helpful tone
- Structured responses
- Business communication focus
- Default: GPT-4, temp=0.7

#### Code Assistant
- Technical, precise language
- Code examples with explanations
- Best practices emphasis
- Default: GPT-4, temp=0.3, guidance enabled

#### Creative Writer
- Imaginative, engaging style
- Story development support
- Character and plot assistance
- Default: Claude, temp=0.9

#### Tutor/Explainer
- Educational, patient tone
- Break down complex topics
- Use analogies and examples
- Default: GPT-3.5, temp=0.6

#### Research Assistant
- Analytical, thorough approach
- Cite sources when possible
- Structured findings
- Default: Claude, temp=0.4, RAG enabled

#### General Assistant
- Balanced, friendly tone
- Versatile across tasks
- Default settings

### Features

#### Quick Start
- Start new chats from any prompt with one click
- Prompt previews on hover

#### Search & Filter
- Search by name, description, or tags
- Filter by category
- Sort by usage, name, or date created

#### Import/Export
- Export prompts as JSON
- Import custom prompts
- Share prompts with others

#### Customization
- Create new prompts
- Edit existing prompts
- Clone and modify built-ins
- Delete custom prompts

## User Experience Modes

### Overview
Three experience levels that progressively reveal advanced features based on user expertise.

### General User Mode (Default)

**Philosophy**: Simple, approachable, smart defaults

**Available Controls**:
- Temperature slider (0.0 - 2.0)
- Max response length
- Model selector
- Context strategy selector

**Hidden Features**:
- Advanced sampling parameters
- Debug tools
- Raw API access
- Model loading parameters

**Best For**: Most users, everyday use

### Power User Mode

**Philosophy**: More control without overwhelming complexity

**Additional Controls**:
- Top-p (nucleus sampling)
- Top-k
- Repeat penalty
- Frequency penalty
- Presence penalty
- Context length slider
- Stop sequences
- Random seed (for reproducibility)

**Additional Features**:
- Performance metrics display
- Token usage breakdown
- Model info panel

**Best For**: Users comfortable with AI parameters

### Developer Mode

**Philosophy**: Full control and transparency

**All Controls**:
- All sampling parameters:
  - Mirostat (v1 and v2)
  - TFS (tail free sampling)
  - Min-p
  - Typical-p
  - Repeat penalty range
  - Penalty alpha
- Model loading:
  - GPU layer count
  - Thread count
  - Batch size
  - Context size override
  - RoPE scaling
- Prompt template editor
- System message override

**Additional Features**:
- Token stream viewer (see each token as generated)
- Raw API request/response inspector
- Performance profiler
- Log viewer
- Memory usage details
- Context window visualizer

**Best For**: Developers, researchers, advanced users

### Mode Switching
- Switch modes anytime in settings
- Settings persist per mode
- Visual indicator of current mode

## Context Management

### Overview
Four strategies for handling limited context windows, each with different trade-offs.

### Strategy 1: Smart Summarization

**How It Works**:
1. Monitor token usage in real-time
2. When approaching threshold (default 75%), trigger summarization
3. Use AI to create concise summary of older messages
4. Replace old messages with summary
5. Keep system prompt + summary + recent messages

**Configuration**:
- Threshold percentage (50% - 95%)
- Summary style (concise, detailed, bullet points)
- Minimum messages before summarization
- Summary model (can be different from chat model)

**Features**:
- Visual context usage bar (green → yellow → red)
- Editable summaries (review before applying)
- Summary history (view past summaries)
- Pinned messages never summarized

**Best For**: Long conversations where history matters

**Trade-offs**:
- ✅ Retains conversation essence
- ✅ Adaptive to conversation flow
- ❌ Summarization takes time
- ❌ Some nuance may be lost

### Strategy 2: Rolling Window

**How It Works**:
1. Keep only last N message pairs
2. Drop older messages automatically
3. No summarization overhead

**Configuration**:
- Window size (5 - 50 message pairs)
- Include/exclude system prompt in count

**Features**:
- Instant, no processing
- Predictable memory usage
- Visual "sliding window" indicator

**Best For**: Quick interactions, stateless conversations

**Trade-offs**:
- ✅ Fast, no overhead
- ✅ Simple and predictable
- ❌ "Forgets" older context completely
- ❌ Not suitable for long conversations

### Strategy 3: Periodic Summary

**How It Works**:
1. Summarize every N messages automatically
2. Keep summaries stacked
3. Optional: merge summaries when many accumulate

**Configuration**:
- Summary interval (10 - 100 messages)
- Maximum summaries before merging
- Auto-merge vs. hierarchical summaries

**Features**:
- Predictable structure
- Multiple summary levels
- Timeline view of summaries

**Best For**: Structured conversations, interviews, meetings

**Trade-offs**:
- ✅ Organized, predictable
- ✅ Can handle very long conversations
- ❌ May summarize too early/late
- ❌ Overhead at regular intervals

### Strategy 4: Manual Only

**How It Works**:
1. No automatic management
2. User controls everything
3. Warnings when approaching limit

**Features**:
- Manual summarization button
- Manual message deletion
- Context usage warnings (75%, 90%, 95%)
- Error handling at 100%

**Best For**: Users who want full control

**Trade-offs**:
- ✅ Complete user control
- ✅ No surprises
- ❌ Requires active management
- ❌ Can hit context limit

### Universal Features

**Message Pinning**:
- Pin critical messages
- Pinned messages never removed/summarized
- Visual pin indicator
- Count toward context but protected

**Context Visualization**:
- Real-time token count
- Breakdown by component:
  - System prompt: X tokens
  - Pinned messages: X tokens
  - Summaries: X tokens
  - Recent messages: X tokens
  - Total: X / Y tokens (Z%)
- Color-coded usage bar

**Token Counting**:
- Uses tiktoken for accuracy
- Per-message token counts
- Real-time updates as you type

**Summary Management**:
- View all summaries
- Edit summaries
- Regenerate summaries
- Export summaries

## Thinking Models Support

### Overview
Special handling for models that separate reasoning/thinking from final responses (o1, o3, DeepSeek R1, Gemini 2.0 Flash Thinking, etc.).

### Detection
- Automatic detection for known models
- Custom delimiter configuration for local models
- Manual enable/disable toggle

### Display

**Thinking Section**:
- Collapsible panel above response
- Different visual style (italic, muted color)
- Separate token count
- Optional: show/hide by default

**Response Section**:
- Normal display
- Standard formatting

### Token Handling
- Thinking tokens excluded from context limit
- Separate tracking:
  - Thinking: X tokens
  - Response: Y tokens
  - Total: Z tokens
- Cost calculation (thinking may be priced differently)

### Streaming
- Stream thinking and response separately
- Real-time collapsible update
- Visual indicator of which section is streaming

### Configuration

**Per Model**:
- Enable/disable thinking support
- Custom delimiters (for local models)
- Default collapsed/expanded state

**Global Settings**:
- Show thinking by default
- Include in exports
- Separate token limits for thinking

### Export Options
- Include thinking: Full export
- Exclude thinking: Response only
- Thinking only: For analysis

## Embeddings & RAG

### Overview
Retrieval Augmented Generation allows you to chat with your documents by embedding them into a vector database and retrieving relevant chunks during conversation.

### Knowledge Base Management

#### Document Upload
**Supported Formats**:
- Text: .txt, .md, .csv
- Documents: .pdf, .docx, .rtf
- Code: .py, .js, .ts, .java, .cpp, etc.
- Data: .json, .xml, .yaml
- Web: HTML pages (via URL)

**Upload Process**:
1. Select files or paste URLs
2. Automatic format detection
3. Text extraction and cleaning
4. Chunking with configurable size/overlap
5. Embedding generation
6. Storage in ChromaDB

#### Document Management
- List all uploaded documents
- View document metadata (chunks, size, date)
- Preview documents
- Delete documents
- Re-index with different settings

#### Chunking Configuration
- Chunk size (256 - 2048 tokens)
- Chunk overlap (0 - 512 tokens)
- Separator strategy (sentence, paragraph, fixed)
- Metadata preservation (page numbers, sections)

### Embedding Options

#### Local Models (Recommended)
**all-MiniLM-L6-v2**:
- Fast, 384 dimensions
- Good for general text
- Low memory usage

**bge-small-en-v1.5**:
- Better quality, 384 dimensions
- Slower than MiniLM
- Medium memory usage

**instructor-large**:
- Best quality, 768 dimensions
- Slower
- Higher memory usage

#### API Embeddings
**OpenAI**:
- text-embedding-3-small
- text-embedding-3-large
- text-embedding-ada-002

**Cohere**:
- embed-english-v3.0
- embed-multilingual-v3.0

### RAG in Chat

#### Automatic Retrieval
- Analyzes user query
- Retrieves relevant chunks
- Injects into system message or context
- AI uses retrieved info in response

#### Configuration
- **Enable/Disable**: Toggle RAG per chat
- **Max Chunks**: 1-10 (default 5)
- **Min Relevance**: 0.0-1.0 (default 0.7)
- **Retrieval Method**: similarity, MMR, hybrid
- **Reranking**: Optional cross-encoder reranking

#### Source Citations
- Inline citations in responses [1], [2]
- Source list at end of message
- Click to view full source
- Highlight relevant excerpt

#### Relevance Scoring
- Show relevance scores (developer mode)
- Adjust threshold based on results
- Visualize retrieval quality

### Chat History Indexing
- Optionally index all past conversations
- Retrieve from your own chat history
- Cross-chat knowledge retrieval

## LoRA Support

### Overview
Load and manage LoRA (Low-Rank Adaptation) adapters for fine-tuning local models on specific tasks or styles.

### LoRA Management

#### Loading LoRAs
- Load multiple LoRAs simultaneously
- Adjustable weight per LoRA (0.0 - 2.0)
- Real-time enable/disable
- Hot-swapping (no model reload needed*)

*Depends on backend support

#### Compatibility
- Automatic compatibility detection
- Base model matching
- VRAM requirement calculation
- Warning if incompatible

#### Organization
- Name, description, tags
- Compatible models list
- File size and location
- Usage statistics

### LoRA Browser

#### HuggingFace Integration
- Search HuggingFace for LoRAs
- Filter by:
  - Base model
  - Task (text generation, chat, coding, etc.)
  - Downloads/likes
  - Language
- View model cards
- Direct download

#### CivitAI Integration
- Browse CivitAI LoRAs (primarily for future image gen)
- Filter and search
- Download and install

#### Popular LoRAs
- Curated list of useful LoRAs:
  - Code improvement
  - Creative writing
  - Instruction following
  - Specific domain knowledge

### LoRA Manager

**Features**:
- List all installed LoRAs
- Enable/disable
- Adjust weights
- Delete
- Update (check for newer versions)
- Import/export configurations

**VRAM Tracking**:
- Show VRAM impact per LoRA
- Total VRAM usage
- Warnings when approaching limit

**Presets**:
- Save LoRA combinations as presets
- Quick-load presets
- Share presets

## Guidance System

### Overview
Three methods to guide model outputs toward desired outcomes and away from undesired content.

### Method 1: System Prompt Integration

**How It Works**:
- Append guidance to system prompt
- Works with all models (local and API)
- Most compatible method

**Configuration**:
- Positive guidance (encourage)
- Negative guidance (discourage)
- Category-based organization

**Example**:
```
Positive: Technical accuracy, code examples, citations
Negative: Speculation without evidence, verbose introductions
```

**Best For**: Universal compatibility

### Method 2: CFG (Classifier-Free Guidance)

**How It Works**:
1. Run inference twice:
   - With positive guidance
   - With negative guidance (or neutral)
2. Steer output based on difference
3. Strength parameter controls effect

**Configuration**:
- Positive prompt
- Negative prompt
- Guidance strength (1.0 - 10.0)

**Requirements**:
- Model must support CFG
- Increases inference time (2x)
- Higher VRAM usage

**Best For**: Advanced local models, strong steering needed

### Method 3: Logit Bias

**How It Works**:
- Bias token probabilities directly
- Encourage/discourage specific tokens
- API-level support (OpenAI, Anthropic)

**Configuration**:
- Token list with bias values (-100 to 100)
- Presets for common use cases

**Best For**: API models, fine-grained control

### Category Organization

**Style**:
- Formal/informal
- Concise/detailed
- Technical/accessible

**Content**:
- Include: examples, citations, code
- Exclude: opinions, assumptions, disclaimers

**Format**:
- Markdown, lists, tables
- Code blocks, JSON, YAML

**Length**:
- Brief, moderate, comprehensive

### Presets

**Code Assistant**:
- Positive: code examples, best practices, explanations
- Negative: vague suggestions, incomplete code

**Creative Writer**:
- Positive: vivid descriptions, dialogue, sensory details
- Negative: clichés, passive voice, repetition

**Data Analyst**:
- Positive: data, statistics, visualizations, insights
- Negative: opinions without data, speculation

**Academic Writing**:
- Positive: citations, formal tone, structured arguments
- Negative: casual language, unsupported claims

**Business Communication**:
- Positive: clear action items, professional tone, conciseness
- Negative: jargon, ambiguity, excessive length

**Technical Documentation**:
- Positive: step-by-step, examples, diagrams, accuracy
- Negative: assumptions, missing prerequisites, verbosity

### Integration with System Prompts
- System prompts can include default guidance
- Override per chat
- Combine guidance sources

### Analytics (Developer Mode)
- Track guidance effectiveness
- A/B comparison (with/without guidance)
- Adjust based on results

## Model Management

### Model Browser

#### HuggingFace Integration
**Features**:
- Search 100,000+ models
- Filter by:
  - Architecture (Llama, Mistral, Qwen, etc.)
  - Size (parameters)
  - Quantization (Q4, Q5, Q6, Q8, F16)
  - Task (chat, completion, code, etc.)
  - Language
  - Downloads/likes
- View model cards
- Check compatibility

**Model Information**:
- Parameters (size)
- Context length
- License
- Training data info
- Benchmark scores
- Download count

**Quantization Guide**:
- Q4: Smallest, fastest, lower quality
- Q5: Balanced
- Q6: Higher quality
- Q8: Near-original quality
- F16: Full precision (large)

#### Download Queue
- Queue multiple downloads
- Pause/resume downloads
- Cancel downloads
- Progress tracking
- Estimated time remaining
- Disk space warnings

#### Compatibility Checks
- VRAM requirements
- Disk space requirements
- GPU architecture compatibility
- Context length support

### Local Model Support

#### llama.cpp Integration
- Efficient CPU and GPU inference
- GGUF format support
- Metal, CUDA, ROCm, Vulkan support
- Configurable parameters:
  - GPU layers (0 = CPU only)
  - Thread count
  - Batch size
  - Context size

#### Model Loading
- Lazy loading (load on demand)
- Unload unused models
- Keep multiple models in memory (if VRAM allows)

#### Model Info Display
- Model name and version
- File size
- Parameters
- Context length
- Quantization level
- Loaded GPU layers
- Current VRAM usage

### API Provider Support

#### OpenAI
**Models**:
- GPT-4 Turbo
- GPT-4
- GPT-3.5 Turbo
- o1-preview, o1-mini (thinking models)

**Features**:
- Function calling
- JSON mode
- Vision (GPT-4V)

#### Anthropic
**Models**:
- Claude 3 Opus
- Claude 3 Sonnet
- Claude 3 Haiku

**Features**:
- Long context (200k tokens)
- Vision
- Artifacts

#### Google
**Models**:
- Gemini 1.5 Pro
- Gemini 1.5 Flash
- Gemini 2.0 Flash Thinking

**Features**:
- Multimodal
- Long context (1M+ tokens)

#### Ollama
- Local server integration
- Pull models from Ollama library
- Supports all Ollama features

#### Custom Endpoints
- OpenAI-compatible API support
- Configure base URL
- Custom headers
- Local servers (LM Studio, vLLM, etc.)

### API Key Management
- Encrypted storage
- Per-provider keys
- Test connection
- Usage tracking:
  - Total tokens used
  - Estimated cost
  - Request count
- Set spending limits

### Model Switching
- Switch models mid-conversation
- Model comparison mode (side-by-side)
- Auto-select best model for task

## Resource Monitoring

### Overview
Real-time monitoring of system resources to ensure smooth operation and prevent crashes.

### Metrics Tracked

#### CPU
- Overall usage (%)
- Per-core usage
- Process usage
- Temperature (if available)

#### GPU
- Model name and capabilities
- Usage (%)
- Memory usage / total
- Temperature
- Compute capability

#### RAM
- Used / Total
- Process usage
- Available
- Swap usage

#### VRAM
- Used / Total
- Per-model allocation
- LoRA overhead
- Available for new models

### Hardware Detection

**GPU Capabilities**:
- Vendor (NVIDIA, AMD, Intel, Apple)
- Architecture
- CUDA/ROCm/Metal support
- Compute capability
- Maximum memory

**CPU Information**:
- Model name
- Core count (physical/logical)
- Instruction sets (AVX, AVX2, AVX512)
- Architecture (x86, ARM)

### Compatibility Checks

**Before Model Download**:
- Verify sufficient disk space
- Check VRAM requirements
- Warn if slow on current hardware

**Before Model Load**:
- Verify VRAM available
- Check GPU compatibility
- Suggest GPU layer count

**Ongoing**:
- Warn if VRAM approaching limit
- Suggest closing other applications
- Recommend lighter quantization

### Performance Metrics

**Inference Speed**:
- Tokens per second
- Time to first token
- Total generation time

**Latency**:
- API response times
- Local inference latency
- Embedding generation time

**Resource Efficiency**:
- Tokens per watt (if supported)
- Memory efficiency
- Throughput vs. quality

### Guardrails

**Prevent Issues**:
- Block model loads that exceed VRAM
- Warn before opening many large models
- Suggest model unloading
- Auto-unload on OOM errors

## Chat Management

### Organization

#### Folders
- Create nested folders
- Drag-and-drop chats
- Folder icons and colors
- Collapse/expand folders

#### Tags
- Add multiple tags per chat
- Tag-based filtering
- Popular tags suggestions
- Tag colors

#### Pinning
- Pin important chats to top
- Separate pinned section
- Unpin anytime

#### Archiving
- Archive old chats
- Hidden from main list
- View archived section
- Unarchive anytime

### Search

#### Keyword Search
- Search titles
- Search message content
- Filter by date range
- Filter by model used
- Filter by tags/folders

#### Semantic Search
- Natural language queries
- "Find chats about Python"
- Powered by embeddings
- Cross-chat retrieval

### Bulk Operations
- Select multiple chats
- Bulk delete
- Bulk tag
- Bulk move to folder
- Bulk archive
- Bulk export

### Export Options

**Formats**:
- **Markdown**: Human-readable, portable
- **JSON**: Machine-readable, full metadata
- **PDF**: Print-friendly, formatted
- **HTML**: Web-viewable, styled

**Options**:
- Include system prompt
- Include metadata (model, settings)
- Include thinking sections
- Include timestamps
- Include source citations

**Export Targets**:
- Single chat
- Multiple chats (zip)
- Entire folder
- Search results

## Portable Mode

### Overview
AI Studio is portable by default - all data is stored within the application directory, making it easy to move between computers or run multiple instances.

### Data Structure

```
AppDirectory/
├── AI-Studio.exe (or .app or .AppImage)
├── data/
│   ├── models/           # Downloaded models
│   ├── loras/            # LoRA adapters
│   ├── vector_store/     # ChromaDB embeddings
│   ├── database/         # SQLite chat history
│   ├── uploads/          # User uploaded files
│   └── chats/            # Exported chats
├── config/
│   └── settings.json     # User settings
└── logs/
    └── app.log           # Application logs
```

### Features

#### No System Installation
- No registry entries (Windows)
- No system-wide files
- No admin/sudo required
- Uninstall = delete folder

#### Move Between Computers
1. Copy entire app folder
2. Run on new computer
3. All settings, chats, models preserved

#### Multiple Instances
- Run different versions simultaneously
- Separate data per instance
- Useful for testing, different use cases

#### Sync Options
- Manual sync via cloud storage (Dropbox, etc.)
- Sync only `data/` and `config/` folders
- Models can be symbolic links

### Cross-Platform

**Windows**:
- Portable .exe
- No installer needed
- Run from USB drive

**macOS**:
- .app bundle
- Drag to Applications or anywhere
- Data in app bundle or user-selected location

**Linux**:
- AppImage
- No dependencies
- Run anywhere

### Build Configuration

**electron-builder**:
- Portable builds by default
- Include runtime (Node, Python)
- Bundle dependencies
- Compression options

### First-Run Setup
- Welcome screen
- Choose data directory (optional)
- Keep default: ./data
- Custom location: user-selected path
- Preference saved in config

---

This comprehensive feature set makes AI Studio a powerful, flexible, and user-friendly local-first AI chat application suitable for a wide range of users from general consumers to advanced developers.
