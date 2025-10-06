"""Token counting utilities for the Market Parser application."""

from typing import Any, Dict, Optional


def extract_token_count_from_context_wrapper(result: Any) -> Optional[int]:
    """Extract token count from official OpenAI Agents SDK context_wrapper.

    DEPRECATED: Use extract_token_usage_from_context_wrapper() instead.
    This function is kept for backward compatibility.

    Args:
        result: The result object from Runner.run()

    Returns:
        int or None: Total token count if available, None otherwise
    """
    token_usage = extract_token_usage_from_context_wrapper(result)
    return token_usage.get("total_tokens") if token_usage else None


def extract_token_usage_from_context_wrapper(result: Any) -> Optional[Dict[str, int]]:
    """Extract detailed token usage from official OpenAI Agents SDK context_wrapper.

    Args:
        result: The result object from Runner.run()

    Returns:
        dict or None: Dictionary with 'total_tokens', 'input_tokens', and 'output_tokens'
                      if available, None otherwise
    """
    try:
        if hasattr(result, "context_wrapper") and result.context_wrapper:
            usage = result.context_wrapper.usage

            # Extract tokens using both naming conventions for compatibility
            total = getattr(usage, "total_tokens", None)
            input_tokens = getattr(usage, "input_tokens", None) or getattr(
                usage, "prompt_tokens", None
            )
            output_tokens = getattr(usage, "output_tokens", None) or getattr(
                usage, "completion_tokens", None
            )

            if total is not None:
                return {
                    "total_tokens": total,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                }
    except Exception:
        # Graceful fallback if context_wrapper is not available
        pass
    return None
