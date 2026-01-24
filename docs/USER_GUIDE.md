# AI Studio User Guide

Welcome to AI Studio! This comprehensive guide will help you get started and make the most of your AI chat experience.

## Table of Contents

- [Getting Started](#getting-started)
- [Chat Interface](#chat-interface)
- [System Prompts](#system-prompts)
- [Model Selection](#model-selection)
- [Settings & Configuration](#settings--configuration)
- [RAG (Knowledge Base)](#rag-knowledge-base)
- [Context Management](#context-management)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Tips & Tricks](#tips--tricks)
- [FAQ](#faq)

---

## Getting Started

### First Launch

When you first launch AI Studio:

1. **Welcome Screen** - Choose your experience level:
   - **General User** - Simple interface with essential controls
   - **Power User** - More parameters and controls
   - **Developer** - Full access to all features

2. **Initial Setup**:
   - Choose data directory location (default is portable mode)
   - Optionally configure API keys for cloud models
   - Select your default model

3. **Start Chatting** - Create your first chat session!

### Quick Start

1. Click **New Chat** or press `Ctrl+N`
2. Type your message in the input box
3. Press `Ctrl+Enter` or click Send
4. Watch the AI respond in real-time

That's it! You're ready to chat with AI.

---

## Chat Interface

### Main Layout

```
┌─────────────┬────────────────────────────────────┐
│             │                                    │
│  Sidebar    │         Chat Messages              │
│             │                                    │
│  - Chats    │  User: Hello!                      │
│  - Prompts  │  AI: Hi! How can I help?          │
│  - Settings │                                    │
│  - RAG      │                                    │
│             │                                    │
│             ├────────────────────────────────────┤
│             │                                    │
│             │   Message Input Box                │
│             │   [Type here...]        [Send]     │
└─────────────┴────────────────────────────────────┘
```

### Sidebar Navigation

**Chat Sessions**:
- View all your chats
- Create new chat with `+` button
- Search chats with `Ctrl+K`
- Organize with folders and tags
- Pin important chats to top

**System Prompts**:
- Browse prompt library
- Create custom prompts
- Quick-start chats from prompts

**Settings**:
- Model selection
- Parameter adjustments
- Experience mode switching
- API key configuration

**Knowledge Base**:
- Upload documents
- Manage RAG sources
- Enable/disable RAG per chat

### Message Display

**Markdown Support**:
- **Bold**, *italic*, ~~strikethrough~~
- Headers, lists, blockquotes
- Code blocks with syntax highlighting
- Tables
- Links and images
- LaTeX math equations

**Code Blocks**:
```python
# Syntax highlighting for 100+ languages
def hello_world():
    print("Hello, AI Studio!")
```

**Thinking Models**:
For models like o1 or DeepSeek R1, see the AI's reasoning process:
```
💭 Thinking (collapsed by default)
   The user wants to know...
   I should explain...

📝 Response
   Here's my answer based on...
```

### Message Actions

Hover over any message to see action buttons:

- **Copy** 📋 - Copy message to clipboard
- **Edit** ✏️ - Edit and resend (user messages)
- **Regenerate** 🔄 - Generate a new response
- **Delete** 🗑️ - Remove message
- **Pin** 📌 - Pin important messages (never summarized)

### Input Features

**Text Input**:
- Multi-line text area (auto-resizing)
- Markdown preview (optional)
- Character/token counter
- Draft saving (auto-saves as you type)

**File Attachments**:
- Drag and drop files
- Click 📎 to browse files
- Support for images, documents, code files
- Preview before sending

**Keyboard Shortcuts**:
- `Ctrl+Enter` - Send message
- `Ctrl+N` - New chat
- `Ctrl+K` - Search chats
- `Ctrl+/` - Toggle sidebar
- `Ctrl+,` - Open settings
- `Ctrl+B` - Toggle bold in input
- `Ctrl+I` - Toggle italic in input
- `Esc` - Cancel current generation

### Streaming Responses

Watch AI responses appear in real-time:
- Green cursor indicates active streaming
- Token counter updates live
- Click **Stop** to interrupt generation
- Partial responses are saved

---

## System Prompts

System prompts define the AI's personality and behavior.

### Using System Prompts

**Quick Start from Prompt**:
1. Click **System Prompts** in sidebar
2. Browse or search for a prompt
3. Click **Start Chat** on any prompt
4. New chat opens with prompt applied

**Apply to Existing Chat**:
1. Open chat settings (⚙️ icon)
2. Select **System Prompt**
3. Choose from dropdown
4. Click **Apply**

### Built-in Prompts

**💼 Professional Assistant**:
- Formal, business-oriented tone
- Structured, clear responses
- Great for: Work emails, reports, professional communication

**💻 Code Assistant**:
- Technical, precise language
- Code examples with explanations
- Great for: Programming help, debugging, learning to code

**✍️ Creative Writer**:
- Imaginative, engaging style
- Storytelling and creative content
- Great for: Stories, creative writing, brainstorming

**🎓 Tutor/Explainer**:
- Educational, patient approach
- Break down complex topics
- Great for: Learning new subjects, homework help

**🔬 Research Assistant**:
- Analytical, thorough
- Evidence-based responses
- Great for: Research, analysis, fact-finding

**💬 General Assistant** (Default):
- Balanced, friendly tone
- Versatile for any task
- Great for: Everyday conversations

### Creating Custom Prompts

1. Click **System Prompts** → **Create New**
2. Fill in the form:
   - **Name**: Short, descriptive name
   - **Description**: What it's good for
   - **Prompt**: The actual system instruction
   - **Icon**: Choose an emoji
   - **Tags**: For organization (e.g., "code", "creative")
   - **Default Settings**: Preferred temperature, model, etc.
3. Click **Save**

**Example Custom Prompt**:
```
Name: Python Expert
Description: Python programming specialist
Prompt: You are a Python expert with 10+ years of experience...
Icon: 🐍
Tags: code, python, technical
Default Settings:
  - Temperature: 0.3
  - Model: GPT-4
```

### Managing Prompts

**Edit**: Click ✏️ to modify any custom prompt

**Delete**: Click 🗑️ to remove (built-ins can't be deleted)

**Export/Import**: Share prompts as JSON files
- Export: Select prompts → **Export**
- Import: **Import** → Choose JSON file

**Usage Stats**: See how often you've used each prompt

---

## Model Selection

### Local Models

Run AI models directly on your computer.

**Advantages**:
- ✅ Complete privacy - no data leaves your device
- ✅ No API costs
- ✅ Works offline
- ✅ Full control

**Requirements**:
- Models stored locally (~4-20 GB per model)
- RAM/VRAM for inference
- CPU or GPU (GPU recommended)

**Popular Local Models**:
- **Llama 2** - Meta's open model, good all-around
- **Mistral** - Fast, efficient, high quality
- **Qwen** - Excellent for coding
- **DeepSeek** - Great reasoning capabilities

**Quantization Levels**:
- **Q4** - Smallest (4-5 GB), fastest, lower quality
- **Q5** - Balanced (5-6 GB), good quality/speed
- **Q6** - Higher quality (7-8 GB), slower
- **Q8** - Near-original quality (10-15 GB)
- **F16** - Full precision (15-30 GB), slowest

### Cloud API Models

Use models via cloud APIs (requires internet and API key).

**OpenAI**:
- GPT-4 Turbo - Most capable, best for complex tasks
- GPT-4 - Highly capable, reliable
- GPT-3.5 Turbo - Fast, affordable
- o1-preview - Advanced reasoning model

**Anthropic**:
- Claude 3 Opus - Most capable, 200k context
- Claude 3 Sonnet - Balanced performance
- Claude 3 Haiku - Fast, affordable

**Google**:
- Gemini 1.5 Pro - Very long context (1M+ tokens)
- Gemini 1.5 Flash - Fast, efficient
- Gemini 2.0 Flash Thinking - Reasoning model

**Cost Considerations**:
- Tokens are charged per message
- Longer conversations cost more
- Check pricing at provider websites
- AI Studio shows estimated costs

### Switching Models

**Mid-Conversation**:
1. Click model name in chat header
2. Select new model
3. Continue conversation with new model

**Comparison Mode**:
1. Click **Compare** button
2. Select 2+ models
3. Send message to all simultaneously
4. See side-by-side responses

### Downloading Models

**From UI** (Coming soon):
1. Settings → Models → Browse
2. Search HuggingFace
3. Filter by size, quantization
4. Click **Download**
5. Track progress in downloads panel

**Manual Installation**:
1. Download GGUF file from HuggingFace
2. Place in `data/models/` directory
3. Settings → Models → Register Model
4. Fill in details, click **Add**

---

## Settings & Configuration

### General Settings

**Appearance**:
- Theme: Dark (default), Light, Auto
- Font size: Small, Medium, Large
- Message density: Compact, Comfortable, Spacious
- Code theme: 20+ syntax highlighting themes

**Behavior**:
- Auto-save drafts: On/Off
- Send on Enter: Ctrl+Enter, Enter, or Shift+Enter
- Show thinking by default: Yes/No
- Streaming speed: Instant, Fast, Smooth, Slow

**Privacy**:
- Telemetry: Off (always)
- Clear history on exit: Yes/No
- Export location

### Model Settings

**Temperature** (0.0 - 2.0):
- 0.0 - Deterministic, focused
- 0.7 - Balanced (default)
- 1.5+ - Creative, varied

Higher = more creative but less predictable

**Max Response Length**:
- Tokens to generate (e.g., 500, 1000, 2000)
- Longer = more complete responses
- Costs more for API models

**Context Strategy**:
- Smart Summarization (recommended)
- Rolling Window
- Periodic Summary
- Manual Only

See [Context Management](#context-management) for details.

### Power User Settings

Enable in Settings → Experience Mode → Power User

**Additional Parameters**:
- **Top-p** (0.0-1.0): Nucleus sampling threshold
- **Top-k** (1-100): Limit to top K tokens
- **Frequency Penalty** (-2.0 to 2.0): Reduce repetition
- **Presence Penalty** (-2.0 to 2.0): Encourage new topics
- **Repeat Penalty** (1.0-2.0): Penalize repeated tokens
- **Random Seed**: For reproducible responses

### Developer Settings

Enable in Settings → Experience Mode → Developer

**All Power User settings plus**:
- Mirostat v1/v2
- Tail-free sampling (TFS)
- Min-p, Typical-p
- Custom prompt templates
- Token stream viewer
- API request/response inspector
- Performance profiler
- Context window visualizer

### API Keys

Configure API keys for cloud models:

1. Settings → API Keys
2. Select provider (OpenAI, Anthropic, Google)
3. Paste API key
4. Click **Test Connection**
5. Save

**Where to get API keys**:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://makersuite.google.com/app/apikey

**Security**:
- Keys are encrypted and stored locally
- Never shared or transmitted except to provider
- Set spending limits to avoid overages

---

## RAG (Knowledge Base)

Retrieval-Augmented Generation lets you chat with your documents.

### Uploading Documents

1. Click **Knowledge Base** in sidebar
2. Click **Upload Document**
3. Select files or drag-and-drop
4. Wait for processing (shows progress)
5. Document is ready for retrieval!

**Supported Formats**:
- Text: `.txt`, `.md`, `.csv`
- Documents: `.pdf`, `.docx`, `.rtf`
- Code: `.py`, `.js`, `.ts`, `.java`, `.cpp`, etc.
- Data: `.json`, `.xml`, `.yaml`
- Web: Paste URLs to fetch web pages

**Processing Steps**:
1. Text extraction
2. Chunking (split into pieces)
3. Embedding (convert to vectors)
4. Storage in vector database

### Using RAG in Chat

**Enable for Chat**:
1. Open chat
2. Click **RAG** toggle in settings
3. Select knowledge sources to use
4. Start asking questions!

**How It Works**:
1. You ask a question
2. AI Studio finds relevant chunks from your documents
3. Chunks are added to context
4. AI answers based on your documents

**Example**:
```
You: What's in the Q4 financial report?

[AI retrieves relevant sections from uploaded report]

AI: According to the Q4 financial report, revenue 
increased by 23% to $45.2M... [Citation: Q4_Report.pdf, p.3]
```

### RAG Settings

**Max Chunks** (1-10):
- How many document pieces to retrieve
- More = more context, but slower
- Recommended: 5

**Min Relevance** (0.0-1.0):
- Minimum similarity score to include
- Higher = only very relevant chunks
- Recommended: 0.7

**Retrieval Method**:
- **Similarity** - Most similar chunks
- **MMR** - Max marginal relevance (diverse results)
- **Hybrid** - Combine both approaches

**Source Citations**:
- Show inline: Yes/No
- Link to source: Yes/No
- Highlight excerpts: Yes/No

### Managing Documents

**View Documents**:
- Knowledge Base → All Sources
- See name, type, chunks, date uploaded

**Delete Documents**:
- Select document
- Click Delete (🗑️)
- Confirm deletion

**Reindex Document**:
- Select document
- Click Reindex
- Choose new chunk size/overlap
- Wait for processing

**Chunk Settings**:
- **Chunk Size** (256-2048 tokens): Size of each piece
- **Overlap** (0-512 tokens): Overlap between chunks
- **Strategy**: Sentence, paragraph, or fixed-size

---

## Context Management

AI models have limited context windows. AI Studio helps manage this automatically.

### Context Indicator

Watch the context bar in the chat header:
- 🟢 Green (0-50%): Plenty of space
- 🟡 Yellow (50-75%): Getting full
- 🟠 Orange (75-90%): Nearly full
- 🔴 Red (90-100%): Almost at limit

### Strategy: Smart Summarization (Recommended)

**How it works**:
- Monitors context usage in real-time
- When reaching threshold (default 75%), triggers summarization
- AI creates concise summary of older messages
- Keeps: System prompt + summary + recent messages + pinned

**When to use**: Long conversations where history matters

**Settings**:
- Threshold: 50-95% (when to summarize)
- Style: Concise, detailed, or bullet points
- Min messages: Don't summarize until X messages

**Tips**:
- Pin important messages to prevent summarization
- Review summaries before applying (editable)
- View summary history anytime

### Strategy: Rolling Window

**How it works**:
- Keeps only last N message pairs
- Drops older messages automatically
- No summarization overhead

**When to use**: Quick interactions, stateless queries

**Settings**:
- Window size: 5-50 message pairs

**Trade-off**: Fast and simple, but forgets older context

### Strategy: Periodic Summary

**How it works**:
- Summarizes every N messages automatically
- Stacks multiple summaries
- Optional: merge summaries when many accumulate

**When to use**: Structured conversations, meetings, interviews

**Settings**:
- Interval: 10-100 messages
- Max summaries before merging
- Merge strategy: Auto-merge or hierarchical

### Strategy: Manual Only

**How it works**:
- No automatic management
- You control everything
- Warnings when approaching limit

**When to use**: When you want complete control

**Actions**:
- Manual summarize button
- Delete individual messages
- Context usage warnings (75%, 90%, 95%)

### Pinning Messages

Pin important messages to protect them:
1. Hover over message
2. Click 📌 pin icon
3. Message shows pin indicator
4. Never removed or summarized

**Use for**:
- Important instructions
- Key information
- Reference data

---

## Advanced Features

### LoRA Adapters

Fine-tune local models for specific tasks.

**What are LoRAs?**
- Low-Rank Adaptation files
- Modify model behavior without retraining
- Small files (10-100 MB vs. multi-GB models)

**Using LoRAs**:
1. Settings → LoRA
2. Add LoRA file
3. Set weight (0.0-2.0)
4. Enable/disable
5. Compatible models will use it

**Popular LoRAs**:
- Code improvement
- Creative writing
- Instruction following
- Domain-specific knowledge

### Guidance System

Steer AI outputs toward desired outcomes.

**Method 1: System Prompt** (All models)
- Add positive/negative guidance to system prompt
- Example: "Be concise" or "Avoid speculation"

**Method 2: CFG** (Local models)
- Classifier-Free Guidance
- Run inference twice and steer
- Stronger effect but slower

**Method 3: Logit Bias** (API models)
- Directly bias token probabilities
- Fine-grained control

**Presets**:
- Code Assistant: Encourage examples, discourage vague code
- Creative Writer: Vivid descriptions, avoid clichés
- Data Analyst: Promote data/stats, reduce opinions

### Multi-Model Comparison

Compare responses from different models:

1. Click **Compare** in chat
2. Select 2-4 models
3. Type your message
4. See responses side-by-side
5. Rate responses or choose favorite

Great for:
- Finding best model for your task
- Quality comparison
- A/B testing prompts

### Export & Backup

**Export Single Chat**:
1. Open chat
2. Click menu (⋮)
3. **Export** → Choose format
4. Save file

**Export All Chats**:
1. Settings → Data
2. **Export All Chats**
3. Choose format and location
4. Creates zip file

**Formats**:
- **Markdown** - Human-readable, portable
- **JSON** - Machine-readable, full metadata
- **PDF** - Print-friendly, formatted
- **HTML** - Web-viewable, styled

**Backup**:
- All data in `data/` folder
- Copy folder to back up everything
- Restore by copying back

---

## Troubleshooting

### Model Won't Load

**Symptoms**: Error when trying to load local model

**Solutions**:
1. Check file exists in `data/models/`
2. Verify VRAM/RAM available (Settings → Resources)
3. Reduce GPU layers if insufficient VRAM
4. Try smaller quantization (Q4 instead of Q6)
5. Check logs: `data/logs/ai_studio.log`

### Slow Response Time

**Symptoms**: Model takes long to respond

**Solutions**:
1. Check if using CPU instead of GPU
2. Increase GPU layers (Settings → Model → GPU Layers)
3. Use smaller model or lighter quantization
4. Close other applications using GPU
5. Check system resources (Settings → Resources)

### Context Limit Error

**Symptoms**: "Context limit exceeded" error

**Solutions**:
1. Enable context management (Smart Summarization)
2. Delete old messages
3. Summarize conversation manually
4. Use model with larger context window
5. Reduce max response length

### RAG Not Finding Relevant Info

**Symptoms**: AI can't find information from uploaded documents

**Solutions**:
1. Check document uploaded successfully
2. Increase max chunks (try 10)
3. Lower min relevance threshold (try 0.5)
4. Reindex with smaller chunk size
5. Verify document contains the information
6. Try different embedding model

### WebSocket Disconnects

**Symptoms**: "Connection lost" during streaming

**Solutions**:
1. Check internet connection (for API models)
2. Verify backend is running
3. Check firewall settings
4. Restart application
5. Check logs for errors

### High API Costs

**Symptoms**: Unexpected API charges

**Solutions**:
1. Set spending limits (Settings → API Keys)
2. Use context management to reduce tokens
3. Reduce max response length
4. Switch to cheaper model (GPT-3.5 vs GPT-4)
5. Use local models for routine tasks
6. Monitor usage (Settings → API Keys → Usage)

---

## Tips & Tricks

### Efficiency Tips

**1. Use Keyboard Shortcuts**
- Learn shortcuts for faster navigation
- Customize in Settings → Keyboard

**2. Template Messages**
- Save common prompts as system prompts
- Quick-start from templates

**3. Organize Chats**
- Use folders for projects
- Tag chats for easy filtering
- Pin important chats to top

**4. Context Management**
- Pin critical messages
- Summarize periodically
- Delete unnecessary messages

### Quality Tips

**1. Better Prompts**
- Be specific and clear
- Provide context and examples
- Use system prompts for consistent behavior

**2. Right Model for Task**
- Simple tasks: GPT-3.5, smaller local models
- Complex reasoning: GPT-4, Claude Opus
- Code: Qwen, GPT-4
- Creative: Claude, higher temperature

**3. Adjust Temperature**
- Factual info: 0.3-0.5
- General chat: 0.7
- Creative writing: 1.0-1.5

**4. Use RAG for Facts**
- Upload reference documents
- Enable RAG for accuracy
- Verify sources in responses

### Privacy Tips

**1. Use Local Models**
- Complete privacy
- No data leaves your device

**2. Disable Cloud Features**
- Don't configure API keys if not needed
- Local-only mode in settings

**3. Regular Backups**
- Export important chats
- Backup `data/` folder

**4. Clear Sensitive Chats**
- Delete after use
- Or use separate portable instance

---

## FAQ

**Q: Is my data private?**
A: Yes! AI Studio is local-first. With local models, nothing leaves your device. With API models, data goes only to the chosen provider (OpenAI, etc.).

**Q: Do I need a GPU?**
A: No, but it helps. CPU-only works but is slower. GPU makes local models much faster.

**Q: How much does it cost?**
A: AI Studio is free. Cloud API usage costs vary by provider (pay-per-token). Local models have no usage cost.

**Q: Can I use it offline?**
A: Yes with local models! API models require internet.

**Q: What's the best model for coding?**
A: GPT-4, Claude Opus, or Qwen (local) are excellent for coding.

**Q: How do I update?**
A: Download new version and replace executable. Data folder is preserved.

**Q: Can I run multiple instances?**
A: Yes! Copy the entire app folder to create separate instances with independent data.

**Q: Where is my data stored?**
A: In the `data/` folder next to the application (portable mode) or a custom location you choose.

**Q: How do I delete all my data?**
A: Settings → Data → Clear All Data, or manually delete the `data/` folder.

**Q: Does it support other languages?**
A: Models support many languages. UI is currently English only.

**Q: Can I customize the UI?**
A: Yes! Themes, fonts, layouts are customizable in Settings.

**Q: What's the difference between system prompts and messages?**
A: System prompts set the AI's behavior/personality. Messages are the conversation content.

**Q: How do thinking models work?**
A: They show their reasoning process before the final answer. You can hide/show the thinking section.

**Q: Can I import ChatGPT history?**
A: Not yet, but it's planned! You can manually copy conversations.

**Q: Is there a mobile version?**
A: Not currently. AI Studio is desktop-only (Windows, macOS, Linux).

---

**Need more help?** 

- Check GitHub Issues: https://github.com/zusamstone/congenial-doodle/issues
- Read Developer Guide: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- View API docs: [API.md](API.md)

**Happy chatting! 🚀**
