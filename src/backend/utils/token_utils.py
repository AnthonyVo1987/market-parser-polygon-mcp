"""Token counting utilities for the Market Parser application."""

from typing import Any, Optional


def extract_token_count_from_context_wrapper(result: Any) -> Optional[int]:
    """Extract token count from official OpenAI Agents SDK context_wrapper.

    Args:
        result: The result object from Runner.run()

    Returns:
        int or None: Total token count if available, None otherwise
    """
    try:
        if hasattr(result, "context_wrapper") and result.context_wrapper:
            usage = result.context_wrapper.usage
            if hasattr(usage, "total_tokens"):
                return usage.total_tokens
    except Exception:
        # Graceful fallback if context_wrapper is not available
        pass
    return None
