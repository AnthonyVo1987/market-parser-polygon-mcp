"""Response formatting utilities for the Market Parser application."""

from rich.console import Console
from rich.markdown import Markdown

console = Console()


def print_response(response_text: str):
    """Display complete agent response with built-in performance metrics footer.

    The response text already includes the performance metrics footer
    from process_query_with_footer(). No metadata extraction needed.

    Args:
        response_text: Complete response string with footer already included
    """
    console.print("\n[bold green]✅ Query processed successfully![/bold green]")
    console.print("[bold]Agent Response:[/bold]\n")

    # Display complete response (includes footer at end)
    # Use Markdown for structured content, Rich handles plain text footer naturally
    has_markdown = any(tag in response_text for tag in ["#", "*", "`", "-", ">"])

    if has_markdown:
        console.print(Markdown(response_text))
    else:
        console.print(response_text)

    # Separator
    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")


def print_error(error, error_type="Error"):
    """Display errors in a consistent, readable format for the CLI."""
    console.print(f"\n[bold red]!!! {error_type} !!![/bold red]")
    console.print(str(error).strip())
    console.print("------------------\n")
