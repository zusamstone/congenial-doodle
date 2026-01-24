# RAG Setup Guide

Complete guide to setting up and using Retrieval-Augmented Generation (RAG) in AI Studio.

## Table of Contents

- [What is RAG?](#what-is-rag)
- [Quick Start](#quick-start)
- [Document Upload Guide](#document-upload-guide)
- [Supported Formats](#supported-formats)
- [Chunking Strategies](#chunking-strategies)
- [Embedding Models](#embedding-models)
- [Retrieval Configuration](#retrieval-configuration)
- [Best Practices](#best-practices)
- [Performance Tuning](#performance-tuning)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

---

## What is RAG?

### Overview

**Retrieval-Augmented Generation (RAG)** enhances AI responses by retrieving relevant information from your documents before generating answers.

**Traditional AI**:
```
You: What did we discuss in Q4 meeting?
AI: I don't have access to that information.
```

**With RAG**:
```
You: What did we discuss in Q4 meeting?
   ↓
[AI Studio retrieves from uploaded Q4_Meeting_Notes.pdf]
   ↓
AI: According to the Q4 meeting notes, you discussed:
    - Revenue growth of 23%
    - New product launch plans
    - Hiring goals for next quarter
    [Source: Q4_Meeting_Notes.pdf, page 2]
```

### How RAG Works

**5-Step Process**:

1. **Document Upload**
   ```
   Upload document.pdf
   → Text extraction
   → Document stored
   ```

2. **Chunking**
   ```
   Full document (10,000 words)
   → Split into chunks (500 words each)
   → 20 chunks created
   ```

3. **Embedding**
   ```
   Each chunk
   → Converted to vector (numbers)
   → Captures semantic meaning
   → Stored in vector database
   ```

4. **Query (at chat time)**
   ```
   Your question
   → Converted to vector
   → Find similar chunks in database
   → Return top 5 most relevant
   ```

5. **Augmented Generation**
   ```
   Your question + Retrieved chunks
   → Sent to AI model
   → AI generates answer using both
   ```

### Benefits

✅ **Accuracy**: AI uses YOUR data, not just training knowledge

✅ **Citations**: See exactly where information came from

✅ **Current Info**: Upload latest documents, always up-to-date

✅ **Privacy**: Local processing, documents stay on your device

✅ **Flexibility**: Works with any document type

---

## Quick Start

### 5-Minute Setup

**1. Upload a Document**:
```
Sidebar → Knowledge Base → Upload Document
→ Select file or drag-and-drop
→ Wait for processing (shows progress bar)
→ ✅ Document ready!
```

**2. Enable RAG in Chat**:
```
Open chat → Settings ⚙️ → Toggle "RAG" ON
→ Select knowledge sources to use
→ Start chatting!
```

**3. Ask Questions**:
```
You: What's covered in section 3?
AI: [Retrieves from document]
    Section 3 covers implementation details...
    [Source: your_doc.pdf, p.5]
```

That's it! RAG is now active.

---

## Document Upload Guide

### Web UI Upload

**Step-by-Step**:

1. **Navigate**: Click "Knowledge Base" in sidebar

2. **Upload**: 
   - Click "Upload Document" button
   - **Or** drag-and-drop files into upload area

3. **Configure** (optional):
   - Chunk size (default: 512 tokens)
   - Chunk overlap (default: 50 tokens)
   - Embedding model (default: all-MiniLM-L6-v2)

4. **Process**: 
   - Upload starts
   - Progress bar shows status
   - Notification when complete

5. **Verify**:
   - Document appears in list
   - Shows chunk count
   - Ready for use

### Bulk Upload

**Upload Multiple Files**:
```
1. Select multiple files in file picker
   OR
2. Drag-and-drop multiple files at once

→ All files processed sequentially
→ Progress shown for each
→ All added to knowledge base
```

### URL Upload

**Upload from Web**:
```
1. Click "Upload from URL"
2. Paste URL (webpage, PDF link, etc.)
3. AI Studio fetches and processes
4. Added to knowledge base
```

**Supported URLs**:
- Direct PDF links
- Web pages (HTML)
- Google Docs (public)
- GitHub files (raw)

### API Upload

**Programmatic Upload** (Advanced):
```bash
curl -X POST http://localhost:8000/api/embeddings/upload \
  -F "file=@document.pdf" \
  -F "chunk_size=512" \
  -F "chunk_overlap=50"
```

---

## Supported Formats

### Document Types

| Format | Extension | Notes |
|--------|-----------|-------|
| **Text** | `.txt` | Plain text |
| | `.md` | Markdown |
| | `.csv` | Comma-separated values |
| **Documents** | `.pdf` | Portable Document Format |
| | `.docx` | Microsoft Word |
| | `.doc` | Word (legacy) |
| | `.rtf` | Rich Text Format |
| | `.odt` | OpenDocument Text |
| **Code** | `.py`, `.js`, `.ts` | Python, JavaScript, TypeScript |
| | `.java`, `.cpp`, `.c` | Java, C++, C |
| | `.go`, `.rs`, `.rb` | Go, Rust, Ruby |
| | `.html`, `.css`, `.xml` | Web formats |
| **Data** | `.json` | JSON data |
| | `.yaml`, `.yml` | YAML |
| | `.xml` | XML |
| | `.sql` | SQL scripts |
| **Presentations** | `.pptx` | PowerPoint |
| | `.odp` | OpenDocument Presentation |
| **Spreadsheets** | `.xlsx` | Excel |
| | `.ods` | OpenDocument Spreadsheet |
| **Web** | `.html`, `.htm` | Web pages |
| | URLs | Direct web content |

### Text Extraction

**PDF**:
- Uses PyPDF2 or pdfplumber
- Preserves page numbers
- Extracts tables (best effort)
- Handles scanned PDFs with OCR (optional)

**DOCX/DOC**:
- Uses python-docx
- Preserves formatting metadata
- Extracts comments and footnotes

**Code Files**:
- Preserves syntax
- Includes comments
- Maintains structure

**Web Pages**:
- Extracts main content
- Removes ads, navigation
- Preserves links

### Special Handling

**Scanned PDFs** (images, no text):
```
Option 1: OCR during upload (slower)
  → Converts images to text
  → May have errors
  → Enable in upload settings

Option 2: Use text-based PDFs
  → More accurate
  → Faster processing
```

**Large Files** (> 100MB):
```
→ Chunking starts during upload
→ Processed in batches
→ Takes longer but works
→ Progress indicator shown
```

**Password-Protected PDFs**:
```
→ Provide password during upload
→ Decrypted for processing
→ Re-encrypted in storage
```

---

## Chunking Strategies

### Why Chunking?

**Problem**: Documents are too large for context windows

**Solution**: Split into smaller, manageable pieces

**Example**:
```
Full Document (50 pages, 25,000 words)
  → TOO LARGE for context

Chunked (50 pieces, 500 words each)
  → Each piece fits in context
  → Retrieve only relevant pieces
```

### Chunk Size

**What It Is**: Number of tokens per chunk

**Sizes**:
- **Small (256 tokens)**: ~190 words, ~1 paragraph
- **Medium (512 tokens)**: ~380 words, ~2-3 paragraphs
- **Large (1024 tokens)**: ~770 words, ~1 page
- **Extra Large (2048 tokens)**: ~1540 words, ~2-3 pages

**Choosing Size**:

**Small Chunks (256)**:
- ✅ Precise retrieval
- ✅ More chunks = better coverage
- ❌ May lose context
- ❌ More chunks to manage
- **Best for**: Technical docs, Q&A, definitions

**Medium Chunks (512)** ⭐ **Recommended**:
- ✅ Good balance
- ✅ Enough context
- ✅ Precise retrieval
- **Best for**: Most documents

**Large Chunks (1024)**:
- ✅ More context per chunk
- ✅ Fewer chunks
- ❌ Less precise
- ❌ May include irrelevant info
- **Best for**: Narrative docs, stories

**Extra Large (2048)**:
- ✅ Maximum context
- ❌ May be too broad
- **Best for**: Long-form content, books

### Chunk Overlap

**What It Is**: How much adjacent chunks share

**Example**:
```
Chunk 1: [tokens 0-512]
Overlap: 50 tokens
Chunk 2: [tokens 462-974]  (starts 50 before 512)
Chunk 3: [tokens 924-1436]

Ensures concepts spanning chunk boundaries aren't lost
```

**Sizes**:
- **No Overlap (0)**: Clean splits, no redundancy
- **Small (25-50)**: Minimal overlap
- **Medium (50-100)**: Standard ⭐ **Recommended**
- **Large (100-200)**: Maximum context preservation

**Choosing Overlap**:

**No Overlap**:
- ✅ Fewer chunks
- ✅ Less redundancy
- ❌ May split concepts
- **Best for**: Structured docs with clear sections

**Small Overlap (50)**:
- ✅ Preserves most concepts
- ✅ Minimal redundancy
- **Best for**: Most documents ⭐

**Large Overlap (200)**:
- ✅ Maximum preservation
- ❌ Lots of redundancy
- ❌ More storage
- **Best for**: Critical docs where no info can be lost

### Splitting Strategies

**Sentence-based** ⭐ **Recommended**:
```
Split at sentence boundaries
→ Chunks end with complete sentences
→ More readable
→ Better context
```

**Paragraph-based**:
```
Split at paragraph boundaries
→ Chunks are complete paragraphs
→ Most context
→ Variable chunk sizes
```

**Fixed-size**:
```
Split at exact token count
→ Uniform chunk sizes
→ May split mid-sentence
→ Less readable
```

**Section-based** (structured docs):
```
Split at headers/sections
→ Respects document structure
→ Variable sizes
→ Best for organized content
```

### Metadata Preservation

**What's Preserved**:
```json
{
  "source": "document.pdf",
  "page": 5,
  "section": "Chapter 3: Implementation",
  "chunk_index": 12,
  "total_chunks": 45,
  "created_at": "2024-01-20T10:00:00Z"
}
```

**Usage**:
- Citations show page numbers
- Filter retrieval by section
- Track source of information

---

## Embedding Models

### What are Embeddings?

**Embeddings** convert text to numbers (vectors) that capture meaning.

**Example**:
```
"Python programming" → [0.23, -0.15, 0.87, ..., 0.44]
"Coding in Python"   → [0.21, -0.14, 0.89, ..., 0.42]
                          ↑ Very similar vectors ↑

"Cooking recipes"    → [-0.56, 0.73, -0.22, ..., 0.11]
                          ↑ Different vector ↑
```

Similar meaning = Similar vectors = Higher retrieval score

### Local Models (Recommended)

**all-MiniLM-L6-v2** ⭐ **Recommended for most users**:
```
Dimensions: 384
Speed: Very Fast (~0.1s for 1000 words)
Quality: Good
VRAM: ~120MB
Disk: ~90MB

Best for: General text, balanced performance
```

**bge-small-en-v1.5**:
```
Dimensions: 384
Speed: Fast (~0.15s for 1000 words)
Quality: Better
VRAM: ~130MB
Disk: ~130MB

Best for: Higher quality needed
```

**bge-base-en-v1.5**:
```
Dimensions: 768
Speed: Medium (~0.3s for 1000 words)
Quality: Very Good
VRAM: ~420MB
Disk: ~420MB

Best for: Quality over speed
```

**instructor-large**:
```
Dimensions: 768
Speed: Slow (~0.8s for 1000 words)
Quality: Best
VRAM: ~1.3GB
Disk: ~1.3GB

Best for: Maximum quality, technical content
```

**E5-large-v2**:
```
Dimensions: 1024
Speed: Slow (~1.0s for 1000 words)
Quality: Excellent
VRAM: ~1.3GB
Disk: ~1.3GB

Best for: State-of-the-art quality
```

### API Models

**OpenAI** (requires API key):

**text-embedding-3-small**:
```
Dimensions: 512-1536 (configurable)
Speed: Fast (API call)
Quality: Very Good
Cost: $0.02 per 1M tokens

Best for: Cost-effective, good quality
```

**text-embedding-3-large**:
```
Dimensions: 256-3072 (configurable)
Speed: Fast (API call)
Quality: Excellent
Cost: $0.13 per 1M tokens

Best for: Best quality
```

**text-embedding-ada-002** (legacy):
```
Dimensions: 1536
Speed: Fast
Quality: Good
Cost: $0.10 per 1M tokens

Best for: Backward compatibility
```

**Cohere** (requires API key):

**embed-english-v3.0**:
```
Dimensions: 1024
Speed: Fast
Quality: Excellent
Cost: $0.10 per 1M tokens

Best for: English text
```

**embed-multilingual-v3.0**:
```
Dimensions: 1024
Speed: Fast
Quality: Excellent (100+ languages)
Cost: $0.10 per 1M tokens

Best for: Multi-language documents
```

### Choosing a Model

**Decision Matrix**:

| Priority | Recommended Model |
|----------|------------------|
| Speed + Low VRAM | all-MiniLM-L6-v2 |
| Balanced | bge-small-en-v1.5 |
| Quality | instructor-large or E5-large-v2 |
| Cost-effective Cloud | OpenAI text-embedding-3-small |
| Best Cloud | OpenAI text-embedding-3-large |
| Multilingual | Cohere embed-multilingual-v3.0 |

**Hardware Considerations**:

**No GPU / Limited RAM**:
```
→ all-MiniLM-L6-v2 (runs on CPU, < 200MB)
→ Or use API models (no local resources)
```

**GPU Available**:
```
→ Any local model (much faster on GPU)
→ Larger models still practical
```

**Large Document Collections**:
```
→ Smaller dimensions (384) for storage efficiency
→ API models if budget allows
```

### Model Compatibility

**Important**: Can't mix embedding models for same knowledge base!

```
❌ Wrong:
  Upload doc1.pdf with all-MiniLM-L6-v2
  Upload doc2.pdf with instructor-large
  → Vectors incompatible, retrieval fails

✅ Correct:
  All documents with all-MiniLM-L6-v2
  OR
  Reindex entire knowledge base to switch models
```

**To Switch Models**:
```
1. Settings → RAG → Change Embedding Model
2. Click "Reindex All Documents"
3. Wait for processing (can take time for large collections)
4. New model now used for all retrieval
```

---

## Retrieval Configuration

### Retrieval Methods

**Similarity Search** ⭐ **Default**:
```
Find chunks most similar to query
→ Pure semantic similarity
→ Fast and simple
→ Works well for most cases
```

**MMR (Maximal Marginal Relevance)**:
```
Balance similarity and diversity
→ Avoids redundant results
→ Better coverage
→ Slightly slower

Useful when: Query might match many similar chunks
```

**Hybrid Search**:
```
Combine semantic (embeddings) + keyword (BM25)
→ Best of both worlds
→ More robust
→ Slower

Useful when: Exact terms matter (names, codes, IDs)
```

### Parameters

**max_chunks** (1-20):
- How many chunks to retrieve
- More = more context, but diluted relevance
- **Recommended**: 3-5 for most queries, 10 for complex

**min_relevance** (0.0-1.0):
- Minimum similarity score to include
- Higher = only very relevant chunks
- Lower = more permissive
- **Recommended**: 0.6-0.7

**Example Settings**:

**Precise Answers**:
```json
{
  "max_chunks": 3,
  "min_relevance": 0.75,
  "method": "similarity"
}
```

**Comprehensive Coverage**:
```json
{
  "max_chunks": 10,
  "min_relevance": 0.5,
  "method": "mmr"
}
```

**Technical/Exact**:
```json
{
  "max_chunks": 5,
  "min_relevance": 0.7,
  "method": "hybrid"
}
```

### Filters

**By Source**:
```
Only retrieve from specific documents
→ Useful when you know which doc to reference
```

**By Date**:
```
Only recent documents
→ Useful for time-sensitive info
```

**By Metadata**:
```
Filter by custom tags, categories, etc.
→ Organize large knowledge bases
```

### Reranking

**What It Is**: Re-score retrieved chunks with more powerful model

**Process**:
```
1. Fast retrieval gets top 20 chunks
2. Reranker (cross-encoder) scores all 20
3. Return top 5 by reranker score
```

**When to Use**:
- Maximum quality needed
- Acceptable slower performance
- Large knowledge bases

**Models**:
- ms-marco-MiniLM-L-6-v2 (fast)
- ms-marco-electra-base (better)

---

## Best Practices

### Document Preparation

**Clean Documents**:
```
✅ Remove headers/footers if repetitive
✅ Fix OCR errors in scanned PDFs
✅ Use clear section headings
❌ Don't remove important metadata
❌ Don't over-edit (keep original meaning)
```

**Structure Matters**:
```
Well-structured (better retrieval):
  # Main Topic
  ## Subtopic 1
  Content about subtopic 1...
  
  ## Subtopic 2
  Content about subtopic 2...

Unstructured (worse retrieval):
  Wall of text without sections or organization...
```

**Metadata Tagging**:
```
Add tags during upload:
  - Category (e.g., "python", "documentation")
  - Date (e.g., "2024-Q1")
  - Importance (e.g., "high-priority")
  
Helps with filtering and organization
```

### Chunking Best Practices

**Match Content Type**:

**Technical Docs**: Small chunks (256-512)
```
→ Precise retrieval of specific details
→ Code snippets fit in chunks
```

**Narratives**: Medium-Large chunks (512-1024)
```
→ Preserve story flow
→ More context per chunk
```

**Reference Material**: Medium chunks (512)
```
→ Balanced
```

**Overlap Appropriately**:
```
Structured docs (clear sections): Low overlap (25-50)
Flowing text (no clear breaks): Medium overlap (50-100)
Critical info (can't lose anything): High overlap (100-200)
```

### Query Optimization

**Specific Questions**:
```
❌ Bad: "Tell me about the project"
✅ Good: "What are the project deliverables for Q2?"

→ Specific queries retrieve better chunks
```

**Use Keywords**:
```
Include important terms from documents:
"What's the Python implementation of X?"
(vs. "How do I do X?" if doc uses "Python implementation")
```

**Rephrase if Needed**:
```
First try: "What's the budget?"
  → Poor results
  
Second try: "What are the financial allocations?"
  → Better results (matches doc terminology)
```

### Knowledge Base Organization

**Separate Knowledge Bases**:
```
Work KB: Work documents only
Personal KB: Personal reference materials
Project KB: Specific project docs

→ Prevents cross-contamination
→ More focused retrieval
```

**Version Control**:
```
Include version/date in filenames:
  Project_Plan_v2.pdf
  Q1_Report_2024.pdf
  
→ Easy to update
→ Track which version AI used
```

**Regular Maintenance**:
```
Monthly:
  - Delete outdated documents
  - Update changed documents
  - Check retrieval quality
```

---

## Performance Tuning

### Optimize Retrieval Speed

**Reduce Chunk Count**:
```
Larger chunks = Fewer total chunks = Faster search
Trade-off: Less precision
```

**Use Faster Embedding Model**:
```
all-MiniLM-L6-v2 (fastest)
  vs
instructor-large (slowest but best)

Choose based on needs
```

**Limit max_chunks**:
```
3 chunks: Very fast
10 chunks: Slower
20 chunks: Slowest

Start small, increase if needed
```

### Optimize Quality

**Better Embedding Model**:
```
Upgrade to instructor-large or E5-large-v2
→ Better semantic understanding
→ More relevant retrieval
```

**Enable Reranking**:
```
Two-stage retrieval
→ Better final results
→ Slower but worth it for quality
```

**Tune min_relevance**:
```
Too low (0.3): Retrieves junk
Too high (0.9): Misses relevant info
Sweet spot: 0.6-0.75 (test and adjust)
```

### Balance Speed & Quality

**Fast & Good** (Recommended):
```
Embedding: all-MiniLM-L6-v2
Chunk Size: 512
max_chunks: 5
min_relevance: 0.7
Method: similarity
Reranking: off
```

**Slow & Best**:
```
Embedding: instructor-large or E5-large-v2
Chunk Size: 512
max_chunks: 10
min_relevance: 0.65
Method: hybrid
Reranking: on (ms-marco-electra-base)
```

**Ultra-Fast** (when speed critical):
```
Embedding: all-MiniLM-L6-v2
Chunk Size: 1024 (fewer chunks)
max_chunks: 3
min_relevance: 0.75
Method: similarity
Reranking: off
```

---

## Advanced Features

### Custom Chunking Functions

**(Future Feature)**

```python
from ai_studio.embeddings import chunker

@chunker.register("my-custom-chunker")
def custom_chunk(text: str, size: int):
    # Your logic
    return chunks

# Use in UI: Select "Custom: my-custom-chunker"
```

### Semantic Caching

**What It Is**: Cache similar queries

```
Query 1: "What's Python?"
  → Retrieve chunks, cache

Query 2: "Tell me about Python"
  → Similar to Query 1
  → Return cached results (instant)
```

**Benefits**:
- Much faster for similar queries
- Reduces API calls (if using API embeddings)
- Improves UX

**Settings**:
```
Enable: Settings → RAG → Semantic Caching: ON
Similarity Threshold: 0.9 (how similar to use cache)
Cache Size: 100 queries
TTL: 1 hour
```

### Multi-Modal RAG

**(Future Feature)**

Support for images, audio, video:
```
Upload:
  - Images (diagrams, charts)
  - Audio (transcribed)
  - Video (transcribed + keyframes)

Retrieval:
  - Text → finds relevant media
  - Image → finds similar images
  - Cross-modal search
```

### Knowledge Graphs

**(Future Feature)**

Extract relationships from documents:
```
Documents
  → Extract entities (people, places, concepts)
  → Identify relationships
  → Build knowledge graph
  → Enhanced retrieval with graph traversal
```

---

## Troubleshooting

### Poor Retrieval Quality

**Symptoms**: AI can't find relevant info

**Solutions**:

1. **Lower min_relevance**:
   ```
   Try 0.5 instead of 0.7
   → More permissive retrieval
   ```

2. **Increase max_chunks**:
   ```
   Try 10 instead of 5
   → More coverage
   ```

3. **Check chunk size**:
   ```
   If too small, concepts split
   → Try larger chunks (768 or 1024)
   ```

4. **Rephrase query**:
   ```
   Match terminology in documents
   ```

5. **Try different method**:
   ```
   Similarity → Hybrid
   → Handles exact terms better
   ```

6. **Better embedding model**:
   ```
   all-MiniLM-L6-v2 → instructor-large
   → More nuanced understanding
   ```

### Slow Retrieval

**Symptoms**: Takes long to retrieve chunks

**Solutions**:

1. **Faster embedding model**:
   ```
   instructor-large → all-MiniLM-L6-v2
   ```

2. **Reduce max_chunks**:
   ```
   10 → 5 or 3
   ```

3. **Disable reranking**:
   ```
   If enabled, turn off
   ```

4. **Use API embeddings**:
   ```
   Local CPU slow → OpenAI API (if acceptable)
   ```

5. **Larger chunks**:
   ```
   512 → 1024 (fewer total chunks)
   ```

### Out of Memory Errors

**Symptoms**: Crashes during upload/indexing

**Solutions**:

1. **Smaller embedding model**:
   ```
   instructor-large (1.3GB) → all-MiniLM-L6-v2 (120MB)
   ```

2. **Process in batches**:
   ```
   Upload one large file at a time
   Don't upload 50 PDFs simultaneously
   ```

3. **Close other applications**:
   ```
   Free up RAM before large uploads
   ```

4. **Use API embeddings**:
   ```
   Offload to cloud if local RAM insufficient
   ```

### Citations Missing or Wrong

**Symptoms**: AI doesn't cite sources or cites wrong

**Solutions**:

1. **Enable citations**:
   ```
   Settings → RAG → Show Citations: ON
   ```

2. **Check metadata**:
   ```
   View document in KB
   → Verify metadata preserved
   ```

3. **Reindex document**:
   ```
   Delete and re-upload with metadata preservation ON
   ```

4. **Update citation format**:
   ```
   Settings → RAG → Citation Style: 
     - Inline: [Source]
     - Footnote: ^1
     - Full: (Document.pdf, p.5)
   ```

### Document Not Found

**Symptoms**: Uploaded document doesn't appear

**Solutions**:

1. **Check processing status**:
   ```
   Knowledge Base → Processing Queue
   → May still be processing
   ```

2. **Verify file format supported**:
   ```
   See Supported Formats section
   ```

3. **Check logs**:
   ```
   data/logs/ai_studio.log
   → Look for upload errors
   ```

4. **Try re-upload**:
   ```
   May have failed silently
   ```

---

**RAG transforms AI Studio from a general assistant to your personal knowledge expert. Upload your documents and start chatting with your data!**
