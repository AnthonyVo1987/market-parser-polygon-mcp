"""Response formatting utilities for the Market Parser application."""

from rich.console import Console
from rich.markdown import Markdown

console = Console()


def print_response(result):
    """Simplified response renderer for CLI output with performance metrics."""
    console.print("\n[bold green]Query processed successfully![/bold green]")
    console.print("[bold]Agent Response:[/bold]\n")

    # Extract content
    final_output = getattr(result, "final_output", result)
    final_text = str(final_output)

    # Check if content has markdown-like formatting
    has_markdown = any(tag in final_text for tag in ["#", "*", "`", "-", ">"])

    if has_markdown:
        # Use Markdown rendering for structured content
        console.print(Markdown(final_text))
    else:
        # Use direct printing with Rich markup
        console.print(final_text)

    # Display performance metrics if available
    if hasattr(result, "metadata") and result.metadata:
        console.print("\n[bold cyan]Performance Metrics:[/bold cyan]")

        # Display processing time if available
        if hasattr(result.metadata, "processing_time") and result.metadata.processing_time:
            console.print(f"   Response Time: {result.metadata.processing_time:.3f}s")

        # Extract token information using official OpenAI Agents SDK
        from .token_utils import extract_token_usage_from_context_wrapper

        token_usage = extract_token_usage_from_context_wrapper(result)

        if token_usage:
            token_count = token_usage.get("total_tokens")
            input_tokens = token_usage.get("input_tokens")
            output_tokens = token_usage.get("output_tokens")
            cached_input = token_usage.get("cached_input_tokens", 0)
            cached_output = token_usage.get("cached_output_tokens", 0)

            # Display token information with caching metrics
            if token_count:
                token_display = f"   Tokens Used: {token_count:,}"

                if input_tokens and output_tokens:
                    token_display += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"

                    # Show cache hit information if any tokens were cached
                    if cached_input > 0 or cached_output > 0:
                        cache_parts = []
                        if cached_input > 0:
                            cache_parts.append(f"Cached Input: {cached_input:,}")
                        if cached_output > 0:
                            cache_parts.append(f"Cached Output: {cached_output:,}")
                        token_display += f" | {', '.join(cache_parts)}"

                console.print(token_display)

        # Display model information
        if hasattr(result.metadata, "model"):
            console.print(f"   Model: {result.metadata.model}")
        elif hasattr(result, "model"):
            console.print(f"   Model: {result.model}")

    # Separator
    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")


def print_error(error, error_type="Error"):
    """Display errors in a consistent, readable format for the CLI."""
    console.print(f"\n[bold red]!!! {error_type} !!![/bold red]")
    console.print(str(error).strip())
    console.print("------------------\n")
