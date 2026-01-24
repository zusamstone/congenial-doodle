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

            # Extract chunk text and adjust positions to match stripped content
            raw_chunk = text[start:end]
            chunk_text = raw_chunk.strip()

            if chunk_text:
                # Calculate leading and trailing whitespace removed by strip()
                leading_ws = len(raw_chunk) - len(raw_chunk.lstrip())
                trailing_ws = len(raw_chunk) - len(raw_chunk.rstrip())
                adjusted_start = start + leading_ws
                adjusted_end = end - trailing_ws

                chunk = Chunk(
                    text=chunk_text,
                    start_char=adjusted_start,
                    end_char=adjusted_end,
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
        last_end = 0

        for sentence, start, end in sentences:
            sentence_len = len(sentence)

            # Track start of first sentence in chunk
            if not current_chunk:
                current_start = start

            # Check if adding this sentence would exceed max_size
            if current_size + sentence_len > self.max_size and current_chunk:
                # Create chunk from accumulated sentences
                chunk_text = " ".join(current_chunk).strip()
                if chunk_text:
                    chunk = Chunk(
                        text=chunk_text,
                        start_char=current_start,
                        end_char=last_end,
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
                last_end = end

            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_size += sentence_len
                last_end = end

                # Check if we've reached target size
                if current_size >= self.target_size:
                    # Create chunk
                    chunk_text = " ".join(current_chunk).strip()
                    if chunk_text:
                        chunk = Chunk(
                            text=chunk_text,
                            start_char=current_start,
                            end_char=last_end,
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

        # Add final chunk if any
        if current_chunk:
            chunk_text = " ".join(current_chunk).strip()
            if chunk_text:
                chunk = Chunk(
                    text=chunk_text,
                    start_char=current_start,
                    end_char=last_end,
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

        # Track chunk positions during recursive splitting to avoid
        # relying on text.find, which can be incorrect when the same
        # text appears multiple times.
        chunks_with_positions = self._recursive_split(text, 0, 0)

        # Convert to Chunk objects
        result_chunks = []

        for chunk_text, start, end in chunks_with_positions:
            # Align start/end with the stripped text that will be stored
            stripped_text = chunk_text.strip()
            leading_ws = len(chunk_text) - len(chunk_text.lstrip())
            trailing_ws = len(chunk_text) - len(chunk_text.rstrip())
            adjusted_start = start + leading_ws
            adjusted_end = end - trailing_ws

            chunk = Chunk(
                text=stripped_text,
                start_char=adjusted_start,
                end_char=adjusted_end,
                metadata={
                    **metadata,
                    "chunk_index": len(result_chunks),
                    "chunk_size": len(stripped_text)
                }
            )
            result_chunks.append(chunk)

        logger.debug(f"Created {len(result_chunks)} recursive chunks")
        return result_chunks

    def _recursive_split(self, text: str, separator_index: int, base_offset: int) -> List[tuple]:
        """Recursively split text at different granularities.

        Returns:
            List of (chunk_text, start_char, end_char) tuples, where
            start_char and end_char are absolute character positions in
            the original input text.
        """
        if len(text) <= self.chunk_size:
            return [(text, base_offset, base_offset + len(text))]

        if separator_index >= len(self.separators):
            # No more separators, do hard split
            return self._hard_split(text, base_offset)

        separator = self.separators[separator_index]
        splits = text.split(separator)

        chunks: List[tuple] = []
        current_chunk: List[str] = []
        current_size = 0

        # Track our position within `text` to compute absolute offsets
        local_offset = 0
        current_chunk_start_offset = base_offset

        for split in splits:
            split_len = len(split)
            sep_len = len(separator)
            split_size = split_len + sep_len

            if not current_chunk:
                # First piece of a new chunk starts here
                current_chunk_start_offset = base_offset + local_offset

            if current_size + split_size > self.chunk_size and current_chunk:
                # Join and add current chunk
                chunk_text = separator.join(current_chunk)
                chunk_start = current_chunk_start_offset
                chunk_end = chunk_start + len(chunk_text)

                if len(chunk_text) > self.chunk_size:
                    # Chunk still too large, try next separator
                    sub_chunks = self._recursive_split(
                        chunk_text, separator_index + 1, chunk_start
                    )
                    chunks.extend(sub_chunks)
                else:
                    chunks.append((chunk_text, chunk_start, chunk_end))

                # Start a new chunk with the current split
                current_chunk = [split]
                current_size = split_size
                current_chunk_start_offset = base_offset + local_offset
            else:
                current_chunk.append(split)
                current_size += split_size

            # Advance local_offset past this split and its separator
            local_offset += split_len + sep_len

        # Add final chunk
        if current_chunk:
            chunk_text = separator.join(current_chunk)
            chunk_start = current_chunk_start_offset
            chunk_end = chunk_start + len(chunk_text)
            if len(chunk_text) > self.chunk_size:
                sub_chunks = self._recursive_split(
                    chunk_text, separator_index + 1, chunk_start
                )
                chunks.extend(sub_chunks)
            else:
                chunks.append((chunk_text, chunk_start, chunk_end))

        return chunks

    def _hard_split(self, text: str, base_offset: int) -> List[tuple]:
        """Split text at exact character boundaries.

        Returns:
            List of (chunk_text, start_char, end_char) tuples.
        """
        chunks: List[tuple] = []
        step = max(1, self.chunk_size - self.overlap)
        for i in range(0, len(text), step):
            chunk_text = text[i:i + self.chunk_size]
            if chunk_text.strip():
                start = base_offset + i
                end = start + len(chunk_text)
                chunks.append((chunk_text, start, end))
        return chunks
