"""
Vector Store Interface for ChromaDB

Handles embedding storage, indexing, and retrieval using ChromaDB.
"""

import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    chromadb = None
    logging.warning("ChromaDB not installed. RAG functionality will not be available.")

from utils.config import settings as app_settings
from utils.portable_paths import get_vector_store_dir


logger = logging.getLogger(__name__)


class VectorStore:
    """
    Vector database interface using ChromaDB.

    Features:
    - Document embedding storage
    - Semantic similarity search
    - Metadata filtering
    - Persistent storage

    Example:
        ```python
        store = VectorStore(collection_name="knowledge_base")

        # Add documents
        store.add_documents(
            texts=["Document 1", "Document 2"],
            metadatas=[{"source": "file1.pdf"}, {"source": "file2.pdf"}],
            ids=["doc1", "doc2"]
        )

        # Search
        results = store.search("query text", n_results=5)
        ```
    """

    def __init__(
        self,
        collection_name: str = "default",
        embedding_model: Optional[str] = None
    ):
        """
        Initialize vector store.

        Args:
            collection_name: Name of the ChromaDB collection
            embedding_model: Embedding model to use (default from settings)
        """
        if chromadb is None:
            raise ImportError(
                "ChromaDB is required for RAG. "
                "Install it with: pip install chromadb"
            )

        self.collection_name = collection_name
        self.embedding_model = embedding_model or app_settings.DEFAULT_EMBEDDING_MODEL

        # Initialize ChromaDB client
        persist_directory = str(get_vector_store_dir())

        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"embedding_model": self.embedding_model}
        )

        logger.info(f"Initialized VectorStore: {collection_name}")
        logger.info(f"Documents in collection: {self.collection.count()}")

    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """
        Add documents to the vector store.

        Args:
            texts: List of text documents
            metadatas: Optional metadata for each document
            ids: Optional IDs for each document (auto-generated if not provided)
        """
        if not texts:
            logger.warning("No texts provided to add_documents")
            return

        # Generate IDs if not provided
        if ids is None:
            start_id = self.collection.count()
            ids = [f"doc_{start_id + i}" for i in range(len(texts))]

        # Generate metadatas if not provided
        if metadatas is None:
            metadatas = [{}] * len(texts)

        # Add to collection
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Added {len(texts)} documents to {self.collection_name}")

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
        where_document: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for similar documents.

        Args:
            query: Query text
            n_results: Number of results to return
            where: Metadata filter
            where_document: Document content filter

        Returns:
            Dict with ids, documents, metadatas, and distances
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            where_document=where_document
        )

        logger.debug(f"Search query: '{query[:50]}...' returned {len(results['ids'][0])} results")

        return {
            "ids": results["ids"][0],
            "documents": results["documents"][0],
            "metadatas": results["metadatas"][0],
            "distances": results["distances"][0]
        }

    def delete_documents(self, ids: List[str]) -> None:
        """
        Delete documents by IDs.

        Args:
            ids: List of document IDs to delete
        """
        self.collection.delete(ids=ids)
        logger.info(f"Deleted {len(ids)} documents from {self.collection_name}")

    def delete_by_metadata(self, where: Dict[str, Any]) -> None:
        """
        Delete documents matching metadata filter.

        Args:
            where: Metadata filter
        """
        self.collection.delete(where=where)
        logger.info(f"Deleted documents matching filter from {self.collection_name}")

    def update_documents(
        self,
        ids: List[str],
        texts: Optional[List[str]] = None,
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Update existing documents.

        Args:
            ids: Document IDs to update
            texts: New text content (optional)
            metadatas: New metadata (optional)
        """
        self.collection.update(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        logger.info(f"Updated {len(ids)} documents in {self.collection_name}")

    def get_count(self) -> int:
        """Get total number of documents in collection."""
        return self.collection.count()

    def reset(self) -> None:
        """Delete all documents from collection."""
        # Delete and recreate collection
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"embedding_model": self.embedding_model}
        )
        logger.info(f"Reset collection: {self.collection_name}")

    def peek(self, limit: int = 10) -> Dict[str, Any]:
        """
        Peek at first N documents in collection.

        Args:
            limit: Number of documents to return

        Returns:
            Dict with ids, documents, and metadatas
        """
        return self.collection.peek(limit=limit)

    def __repr__(self) -> str:
        """String representation."""
        return f"VectorStore(collection={self.collection_name}, count={self.get_count()})"
