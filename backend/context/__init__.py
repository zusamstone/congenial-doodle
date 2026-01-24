"""
Context Management Module

Handles context window management for AI models:
- Smart summarization strategy
- Rolling window strategy
- Periodic summarization
- Manual context management
- Token counting and limits
"""

# TODO: Implement manager and strategies modules
# from .manager import ContextManager
# from .strategies import (
#     ContextStrategy,
#     SmartSummarizationStrategy,
#     RollingWindowStrategy,
#     PeriodicSummaryStrategy,
#     ManualStrategy
# )
from .token_counter import TokenCounter

__all__ = [
    # "ContextManager",
    # "ContextStrategy",
    # "SmartSummarizationStrategy",
    # "RollingWindowStrategy",
    # "PeriodicSummaryStrategy",
    # "ManualStrategy",
    "TokenCounter",
]
