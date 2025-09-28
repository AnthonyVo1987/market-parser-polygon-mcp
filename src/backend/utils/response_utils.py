"""Response formatting utilities for the Market Parser application."""

from rich.console import Console
from rich.markdown import Markdown

console = Console()


def print_response(result):
    """Simplified response renderer with emoji support and performance metrics."""
    console.print("\n[bold green]✅ Query processed successfully![/bold green]")
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
        # Use direct printing with Rich markup for better emoji support
        console.print(final_text)

    # Display performance metrics if available
    if hasattr(result, "metadata") and result.metadata:
        console.print("\n[bold cyan]📊 Performance Metrics:[/bold cyan]")

        # Display processing time if available
        if hasattr(result.metadata, "processing_time") and result.metadata.processing_time:
            console.print(f"   ⏱️  Response Time: {result.metadata.processing_time:.3f}s")

        # Extract token information
        token_count = None
        input_tokens = None
        output_tokens = None

        if hasattr(result.metadata, "get"):
            token_count = result.metadata.get("tokenCount")
            input_tokens = result.metadata.get("inputTokens")
            output_tokens = result.metadata.get("outputTokens")
        elif hasattr(result.metadata, "usage"):
            usage = result.metadata.usage
            if hasattr(usage, "total_tokens"):
                token_count = usage.total_tokens
            if hasattr(usage, "prompt_tokens"):
                input_tokens = usage.prompt_tokens
            if hasattr(usage, "completion_tokens"):
                output_tokens = usage.completion_tokens
        elif hasattr(result.metadata, "token_count"):
            token_count = result.metadata.token_count

        # Display token information
        if token_count:
            token_display = f"   🔢  Tokens Used: {token_count:,}"
            if input_tokens and output_tokens:
                token_display += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"
            console.print(token_display)

        # Display model information
        if hasattr(result.metadata, "model"):
            console.print(f"   🤖  Model: {result.metadata.model}")
        elif hasattr(result, "model"):
            console.print(f"   🤖  Model: {result.model}")

    # Enhanced separator with emoji
    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")


def print_error(error, error_type="Error"):
    """Display errors in a consistent, readable format for the CLI."""
    console.print(f"\n[bold red]!!! {error_type} !!![/bold red]")
    console.print(str(error).strip())
    console.print("------------------\n")