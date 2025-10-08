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
        dict or None: Dictionary with 'total_tokens', 'input_tokens', 'output_tokens',
                      'cached_input_tokens', and 'cached_output_tokens' if available,
                      None otherwise
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

            # Extract cached tokens from OpenAI Prompt Caching API
            # Responses API uses input_tokens_details.cached_tokens
            # Chat Completions API uses prompt_tokens_details.cached_tokens
            cached_input_tokens = None
            cached_output_tokens = None

            # Try Responses API format (OpenAI Agents SDK v0.2.9)
            if hasattr(usage, "input_tokens_details") and usage.input_tokens_details:
                cached_input_tokens = getattr(
                    usage.input_tokens_details, "cached_tokens", 0
                )

            # Fallback to Chat Completions API format
            if cached_input_tokens is None and hasattr(usage, "prompt_tokens_details"):
                if usage.prompt_tokens_details:
                    cached_input_tokens = getattr(
                        usage.prompt_tokens_details, "cached_tokens", 0
                    )

            # Output cached tokens (if available in future API versions)
            if hasattr(usage, "output_tokens_details") and usage.output_tokens_details:
                cached_output_tokens = getattr(
                    usage.output_tokens_details, "cached_tokens", 0
                )

            if total is not None:
                return {
                    "total_tokens": total,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cached_input_tokens": cached_input_tokens or 0,
                    "cached_output_tokens": cached_output_tokens or 0,
                }
    except Exception:
        # Graceful fallback if context_wrapper is not available
        pass
    return None
