"""Response formatting utilities for the Market Parser application."""

from rich.console import Console

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

    # Display complete response as plain text (preserves Markdown pipes and table structure)
    # Output: Pure Markdown with pipes (|) and dividers (---) for tables
    # This allows Gradio to render properly AND CLI displays readable text
    console.print(response_text)

    # Separator
    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")


def print_error(error, error_type="Error"):
    """Display errors in a consistent, readable format for the CLI."""
    console.print(f"\n[bold red]!!! {error_type} !!![/bold red]")
    console.print(str(error).strip())
    console.print("------------------\n")
