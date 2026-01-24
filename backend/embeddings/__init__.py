"""
Embeddings and RAG (Retrieval-Augmented Generation) Module

This module handles:
- Document processing and text extraction
- Text chunking strategies
- Embedding generation with sentence-transformers
- Vector storage with ChromaDB
- Semantic search and retrieval
"""

from .vector_store import VectorStore
from .document_processor import DocumentProcessor
from .chunking import ChunkingStrategy, FixedSizeChunking, SemanticChunking, RecursiveChunking

__all__ = [
    "VectorStore",
    "DocumentProcessor",
    "ChunkingStrategy",
    "FixedSizeChunking",
    "SemanticChunking",
    "RecursiveChunking",
]
