"""
Token Counter Module

Provides token counting for various models using tiktoken.
"""

import logging
from typing import Dict, List

try:
    import tiktoken
except ImportError:
    tiktoken = None
    logging.warning("tiktoken not installed. Token counting will use approximation.")


logger = logging.getLogger(__name__)


class TokenCounter:
    """
    Token counter for text using tiktoken.

    Falls back to word-based approximation if tiktoken not available.

    Example:
        ```python
        counter = TokenCounter(model="gpt-3.5-turbo")
        tokens = counter.count("Hello, world!")
        ```
    """

    # Model to encoding mapping
    MODEL_ENCODINGS = {
        # OpenAI
        "gpt-4": "cl100k_base",
        "gpt-4-turbo": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "text-davinci-003": "p50k_base",
        "text-davinci-002": "p50k_base",
        "code-davinci-002": "p50k_base",
        # Claude (approximation, use cl100k_base)
        "claude-3": "cl100k_base",
        "claude-2": "cl100k_base",
        # Llama (approximation)
        "llama": "cl100k_base",
        "llama-2": "cl100k_base",
        # Default
        "default": "cl100k_base",
    }

    def __init__(self, model: str = "default"):
        """
        Initialize token counter.

        Args:
            model: Model name or identifier
        """
        self.model = model
        self.encoding = None

        if tiktoken is not None:
            try:
                # Get encoding for model
                encoding_name = self._get_encoding_name(model)
                self.encoding = tiktoken.get_encoding(encoding_name)
                logger.info(f"TokenCounter initialized with encoding: {encoding_name}")
            except Exception as e:
                logger.warning(f"Failed to load tiktoken encoding: {e}. Using approximation.")
                self.encoding = None
        else:
            logger.warning("tiktoken not available. Using word-based approximation.")

    def _get_encoding_name(self, model: str) -> str:
        """Get encoding name for a model."""
        # Try exact match
        if model in self.MODEL_ENCODINGS:
            return self.MODEL_ENCODINGS[model]

        # Try partial match
        for model_key, encoding in self.MODEL_ENCODINGS.items():
            if model_key in model.lower():
                return encoding

        # Default
        return self.MODEL_ENCODINGS["default"]

    def count(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        if not text:
            return 0

        if self.encoding is not None:
            # Use tiktoken
            try:
                return len(self.encoding.encode(text))
            except Exception as e:
                logger.warning(f"Error counting tokens: {e}. Falling back to approximation.")

        # Fallback: word-based approximation
        # Rough estimate: 1 token ≈ 0.75 words (or 1.33 tokens per word)
        word_count = len(text.split())
        return int(word_count * 1.33)

    def count_messages(self, messages: List[Dict[str, str]]) -> int:
        """
        Count tokens in a list of messages.

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            Total token count including message formatting
        """
        if not messages:
            return 0

        total_tokens = 0

        for message in messages:
            # Count role (typically 4 tokens for formatting)
            total_tokens += 4

            # Count content
            content = message.get("content", "")
            total_tokens += self.count(content)

            # Count name if present
            if "name" in message:
                total_tokens += self.count(message["name"])
                total_tokens += 1  # Extra token for name

        # Every message has 3 tokens of overhead
        total_tokens += 3

        return total_tokens

    def truncate_to_limit(
        self,
        text: str,
        max_tokens: int,
        suffix: str = "..."
    ) -> str:
        """
        Truncate text to fit within token limit.

        Args:
            text: Text to truncate
            max_tokens: Maximum number of tokens
            suffix: Suffix to add if truncated

        Returns:
            Truncated text
        """
        if not text:
            return text

        current_tokens = self.count(text)

        if current_tokens <= max_tokens:
            return text

        # Binary search for truncation point
        if self.encoding is not None:
            # Use tiktoken for precise truncation
            tokens = self.encoding.encode(text)
            truncated_tokens = tokens[:max_tokens - self.count(suffix)]
            truncated_text = self.encoding.decode(truncated_tokens)
        else:
            # Approximation: truncate by characters
            # Rough estimate: 4 characters per token
            max_chars = int(max_tokens * 4 * 0.75)  # Be conservative
            truncated_text = text[:max_chars]

        return truncated_text + suffix

    def get_remaining_tokens(
        self,
        used_tokens: int,
        context_length: int
    ) -> int:
        """
        Calculate remaining tokens in context window.

        Args:
            used_tokens: Number of tokens already used
            context_length: Maximum context length

        Returns:
            Number of tokens remaining
        """
        return max(0, context_length - used_tokens)

    def estimate_tokens(self, char_count: int) -> int:
        """
        Estimate token count from character count.

        Args:
            char_count: Number of characters

        Returns:
            Estimated token count
        """
        # Rough estimate: 4 characters per token
        return int(char_count / 4)

    def estimate_chars(self, token_count: int) -> int:
        """
        Estimate character count from token count.

        Args:
            token_count: Number of tokens

        Returns:
            Estimated character count
        """
        # Rough estimate: 4 characters per token
        return token_count * 4

    def __repr__(self) -> str:
        """String representation."""
        encoding = self.encoding.name if self.encoding else "approximation"
        return f"TokenCounter(model={self.model}, encoding={encoding})"


# Convenience function
def count_tokens(text: str, model: str = "default") -> int:
    """
    Quick token counting without creating a counter instance.

    Args:
        text: Text to count
        model: Model name

    Returns:
        Token count
    """
    counter = TokenCounter(model=model)
    return counter.count(text)
