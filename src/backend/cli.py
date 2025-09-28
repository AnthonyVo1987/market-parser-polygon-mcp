"""CLI functionality for the Market Parser application."""

import time
from datetime import datetime

from agents import Runner, SQLiteSession

from .api_models import ResponseMetadata
from .config import settings
from .services import create_agent, create_polygon_mcp_server
from .utils import print_error, print_response


async def cli_async():
    """Run the interactive CLI loop."""
    print("Welcome to the GPT-5 powered Market Analysis Agent. Type 'exit' to quit.")

    try:
        # Initialize persistent CLI session for conversation memory
        cli_session = SQLiteSession(settings.cli_session_name)
        print(f"📊 CLI session '{settings.cli_session_name}' initialized for conversation memory")

        server = create_polygon_mcp_server()

        # Initialize CLI MCP server
        async with server:
            await _run_cli_loop(server, cli_session)

    except Exception as e:
        print_error(e, "Startup Error")
    finally:
        # Clean up CLI session and agent cache on exit
        try:
            if "cli_session" in locals():
                # Session cleanup is handled automatically by SQLiteSession
                print("📊 CLI session cleaned up")

        except Exception as cleanup_error:
            print(f"Warning: Cleanup failed: {cleanup_error}")


async def _run_cli_loop(server, cli_session):
    """Run the main CLI input loop."""
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            if not user_input or len(user_input.strip()) < 2:
                print("Please enter a valid query (at least 2 characters).")
                continue

            # Process the user input
            result = await _process_user_input(server, cli_session, user_input)

            # Display the response with full result object for metadata
            print_response(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            # Handle end of input stream (e.g., when piping input)
            print("\nInput stream ended. Goodbye!")
            break
        except Exception as e:
            print_error(e, "Unexpected Error")


async def _process_user_input(server, cli_session, user_input):
    """Process a single user input and return the result."""
    try:
        # Start timing for performance metrics
        start_time = time.perf_counter()

        # Get or create agent using factory function
        analysis_agent = create_agent(server)

        # Run the financial analysis agent with the user message
        result = await Runner.run(analysis_agent, user_input, session=cli_session)

        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Extract token information from OpenAI response metadata
        token_count = _extract_token_count(result)

        # Create metadata object for CLI response
        cli_metadata = ResponseMetadata(
            model=settings.available_models[0],
            timestamp=datetime.now().isoformat(),
            processing_time=processing_time,
            request_id=None,  # CLI doesn't use request IDs
            token_count=token_count,
        )

        # Attach metadata to result object
        result.metadata = cli_metadata

        # Extract the response (stored in result object for print_response)
        _ = str(result.final_output)

        return result

    except Exception as e:
        print_error(e, "AI Model Error")

        # Create a mock result object for error cases
        class MockResult:
            def __init__(self, error_msg):
                self.final_output = error_msg
                self.metadata = None

        return MockResult(f"Error: Unable to process request. {str(e)}")


def _extract_token_count(result):
    """Extract token count from result metadata."""
    if hasattr(result, "metadata") and result.metadata:
        # Try to extract token information from OpenAI response metadata
        if hasattr(result.metadata, "get"):
            return result.metadata.get("tokenCount")
        if hasattr(result.metadata, "usage"):
            # Handle OpenAI usage object format
            usage = result.metadata.usage
            if hasattr(usage, "total_tokens"):
                return usage.total_tokens
    return None
