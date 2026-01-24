"""
Text Chunking Strategies for RAG

Provides different strategies for splitting documents into chunks
for embedding and retrieval.
"""

import logging
from typing import List, Protocol
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Represents a text chunk."""
    text: str
    start_char: int
    end_char: int
    metadata: dict


class ChunkingStrategy(Protocol):
    """Protocol for chunking strategies."""

    def chunk(self, text: str, metadata: dict = None) -> List[Chunk]:
        """
        Split text into chunks.

        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to chunks

        Returns:
            List of Chunk objects
        """
        ...


class FixedSizeChunking:
    """
    Fixed-size chunking with overlap.

    Splits text into chunks of a fixed size with optional overlap
    to preserve context at chunk boundaries.

    Example:
        ```python
        chunker = FixedSizeChunking(chunk_size=512, overlap=50)
        chunks = chunker.chunk("Long document text...")
        ```
    """

    def __init__(
        self,
        chunk_size: int = 512,
        overlap: int = 50,
        separator: str = "\n\n"
    ):
        """
        Initialize fixed-size chunking.

        Args:
            chunk_size: Target size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            separator: Preferred separator for splitting (paragraphs by default)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator

        if overlap >= chunk_size:
            raise ValueError("Overlap must be less than chunk_size")

        logger.info(f"FixedSizeChunking: size={chunk_size}, overlap={overlap}")

    def chunk(self, text: str, metadata: dict = None) -> List[Chunk]:
        """Split text into fixed-size chunks."""
        if metadata is None:
            metadata = {}

        chunks = []
        current_pos = 0

        while current_pos < len(text):
            # Calculate chunk boundaries
            start = current_pos
            end = min(current_pos + self.chunk_size, len(text))

            # Try to split at separator if not at end of text
            if end < len(text):
                # Look for separator near the end
                search_start = max(start, end - 100)
                last_sep = text.rfind(self.separator, search_start, end)

                if last_sep != -1 and last_sep > start:
                    # Found separator, split there
                    end = last_sep + len(self.separator)

            # Extract chunk text
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk = Chunk(
                    text=chunk_text,
                    start_char=start,
                    end_char=end,
                    metadata={
                        **metadata,
                        "chunk_index": len(chunks),
                        "chunk_size": len(chunk_text)
                    }
                )
                chunks.append(chunk)

            # Move to next chunk with overlap
            current_pos = end - self.overlap if end < len(text) else end

            # Safety check to prevent infinite loop
            if current_pos <= start:
                current_pos = start + 1

        logger.debug(f"Created {len(chunks)} fixed-size chunks")
        return chunks


class SemanticChunking:
    """
    Semantic chunking based on sentence boundaries.

    Splits text into chunks at sentence boundaries, trying to keep
    chunks close to target size while preserving semantic units.

    Example:
        ```python
        chunker = SemanticChunking(target_size=512)
        chunks = chunker.chunk("Text with sentences...")
        ```
    """

    def __init__(
        self,
        target_size: int = 512,
        max_size: int = 768,
        sentence_endings: str = ".!?"
    ):
        """
        Initialize semantic chunking.

        Args:
            target_size: Target chunk size in characters
            max_size: Maximum chunk size (hard limit)
            sentence_endings: Characters that end sentences
        """
        self.target_size = target_size
        self.max_size = max_size
        self.sentence_endings = sentence_endings

        logger.info(f"SemanticChunking: target={target_size}, max={max_size}")

    def chunk(self, text: str, metadata: dict = None) -> List[Chunk]:
        """Split text into semantic chunks."""
        if metadata is None:
            metadata = {}

        # Split into sentences
        sentences = self._split_sentences(text)

        chunks = []
        current_chunk = []
        current_size = 0
        current_start = 0

        for sentence, start, end in sentences:
            sentence_len = len(sentence)

            # Check if adding this sentence would exceed max_size
            if current_size + sentence_len > self.max_size and current_chunk:
                # Create chunk from accumulated sentences
                chunk_text = " ".join(current_chunk).strip()
                if chunk_text:
                    chunk = Chunk(
                        text=chunk_text,
                        start_char=current_start,
                        end_char=start,
                        metadata={
                            **metadata,
                            "chunk_index": len(chunks),
                            "chunk_size": len(chunk_text),
                            "sentence_count": len(current_chunk)
                        }
                    )
                    chunks.append(chunk)

                # Start new chunk
                current_chunk = [sentence]
                current_size = sentence_len
                current_start = start

            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_size += sentence_len

                # Check if we've reached target size
                if current_size >= self.target_size:
                    # Create chunk
                    chunk_text = " ".join(current_chunk).strip()
                    if chunk_text:
                        chunk = Chunk(
                            text=chunk_text,
                            start_char=current_start,
                            end_char=end,
                            metadata={
                                **metadata,
                                "chunk_index": len(chunks),
                                "chunk_size": len(chunk_text),
                                "sentence_count": len(current_chunk)
                            }
                        )
                        chunks.append(chunk)

                    # Start new chunk
                    current_chunk = []
                    current_size = 0
                    current_start = end

        # Add final chunk if any
        if current_chunk:
            chunk_text = " ".join(current_chunk).strip()
            if chunk_text:
                chunk = Chunk(
                    text=chunk_text,
                    start_char=current_start,
                    end_char=len(text),
                    metadata={
                        **metadata,
                        "chunk_index": len(chunks),
                        "chunk_size": len(chunk_text),
                        "sentence_count": len(current_chunk)
                    }
                )
                chunks.append(chunk)

        logger.debug(f"Created {len(chunks)} semantic chunks")
        return chunks

    def _split_sentences(self, text: str) -> List[tuple[str, int, int]]:
        """
        Split text into sentences with positions.

        Returns:
            List of (sentence, start_pos, end_pos) tuples
        """
        sentences = []
        current_sentence = []
        current_start = 0
        i = 0

        while i < len(text):
            char = text[i]
            current_sentence.append(char)

            # Check if this is a sentence ending
            if char in self.sentence_endings:
                # Look ahead for spaces or end of text
                if i + 1 >= len(text) or text[i + 1].isspace():
                    # Complete sentence
                    sentence = "".join(current_sentence).strip()
                    if sentence:
                        sentences.append((sentence, current_start, i + 1))

                    current_sentence = []
                    current_start = i + 1

            i += 1

        # Add final sentence if any
        if current_sentence:
            sentence = "".join(current_sentence).strip()
            if sentence:
                sentences.append((sentence, current_start, len(text)))

        return sentences


class RecursiveChunking:
    """
    Recursive chunking that tries multiple separators.

    Attempts to split text at increasingly fine-grained separators
    (paragraphs → sentences → words) to achieve target chunk size.
    """

    def __init__(
        self,
        chunk_size: int = 512,
        overlap: int = 50,
        separators: List[str] = None
    ):
        """
        Initialize recursive chunking.

        Args:
            chunk_size: Target chunk size
            overlap: Overlap between chunks
            separators: List of separators to try (in order)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

        if separators is None:
            # Default separators: paragraphs, sentences, clauses, words
            self.separators = ["\n\n", "\n", ". ", ", ", " "]
        else:
            self.separators = separators

        logger.info(f"RecursiveChunking: size={chunk_size}, separators={len(self.separators)}")

    def chunk(self, text: str, metadata: dict = None) -> List[Chunk]:
        """Split text using recursive strategy."""
        if metadata is None:
            metadata = {}

        chunks = self._recursive_split(text, 0)

        # Convert to Chunk objects
        result_chunks = []
        current_pos = 0

        for chunk_text in chunks:
            start = text.find(chunk_text, current_pos)
            if start == -1:
                start = current_pos

            end = start + len(chunk_text)

            chunk = Chunk(
                text=chunk_text.strip(),
                start_char=start,
                end_char=end,
                metadata={
                    **metadata,
                    "chunk_index": len(result_chunks),
                    "chunk_size": len(chunk_text)
                }
            )
            result_chunks.append(chunk)
            current_pos = end

        logger.debug(f"Created {len(result_chunks)} recursive chunks")
        return result_chunks

    def _recursive_split(self, text: str, separator_index: int) -> List[str]:
        """Recursively split text at different granularities."""
        if len(text) <= self.chunk_size:
            return [text]

        if separator_index >= len(self.separators):
            # No more separators, do hard split
            return self._hard_split(text)

        separator = self.separators[separator_index]
        splits = text.split(separator)

        chunks = []
        current_chunk = []
        current_size = 0

        for split in splits:
            split_size = len(split) + len(separator)

            if current_size + split_size > self.chunk_size and current_chunk:
                # Join and add current chunk
                chunk = separator.join(current_chunk)
                if len(chunk) > self.chunk_size:
                    # Chunk still too large, try next separator
                    sub_chunks = self._recursive_split(chunk, separator_index + 1)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append(chunk)

                current_chunk = [split]
                current_size = split_size
            else:
                current_chunk.append(split)
                current_size += split_size

        # Add final chunk
        if current_chunk:
            chunk = separator.join(current_chunk)
            if len(chunk) > self.chunk_size:
                sub_chunks = self._recursive_split(chunk, separator_index + 1)
                chunks.extend(sub_chunks)
            else:
                chunks.append(chunk)

        return chunks

    def _hard_split(self, text: str) -> List[str]:
        """Split text at exact character boundaries."""
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks
