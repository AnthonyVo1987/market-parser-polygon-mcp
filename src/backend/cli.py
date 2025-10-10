"""CLI functionality for the Market Parser application."""

import time
from datetime import datetime

from agents import Runner, SQLiteSession

from .api_models import ResponseMetadata
from .config import settings
from .services import create_agent
from .utils import print_error, print_response
from .utils.token_utils import extract_token_count_from_context_wrapper


def initialize_persistent_agent():
    """Initialize persistent agent for the session.

    This is the SINGLE SOURCE OF TRUTH for agent initialization.
    Both CLI and GUI modes use this function to create their agent instance.

    Following the architecture principle from commit b866f0a:
    - CLI owns core business logic (this function)
    - GUI imports and calls this function (no duplication)

    Returns:
        Agent: The initialized financial analysis agent
    """
    return create_agent()


async def process_query(agent, session, user_input):
    """Process a user query using the persistent agent.

    This is the CORE BUSINESS LOGIC for query processing.
    Both CLI and GUI modes call this function (no duplication).

    Following the architecture principle from commit b866f0a:
    - CLI owns core business logic (this function)
    - GUI imports and calls this function (no duplication)

    Args:
        agent: The persistent agent instance
        session: The SQLite session for conversation memory
        user_input: The user's query string

    Returns:
        RunResult: The result from Runner.run() containing the agent's response
    """
    result = await Runner.run(agent, user_input, session=session)
    return result


async def cli_async():
    """Run the interactive CLI loop."""
    print("Welcome to the GPT-5 powered Market Analysis Agent. Type 'exit' to quit.")

    try:
        # Initialize persistent CLI session for conversation memory
        cli_session = SQLiteSession(settings.cli_session_name)
        print(f"📊 CLI session '{settings.cli_session_name}' initialized for conversation memory")

        # Create persistent agent ONCE for the entire session (following b866f0a pattern)
        analysis_agent = initialize_persistent_agent()
        print("🤖 Persistent agent initialized - agent will be reused for all messages")

        await _run_cli_loop(cli_session, analysis_agent)

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


async def _run_cli_loop(cli_session, analysis_agent):
    """Run the main CLI input loop.
    
    Args:
        cli_session: The SQLite session for conversation memory
        analysis_agent: The persistent agent instance (reused for all messages)
    """
    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            if not user_input or len(user_input.strip()) < 2:
                print("Please enter a valid query (at least 2 characters).")
                continue

            # Process the user input with persistent agent
            result = await _process_user_input(cli_session, analysis_agent, user_input)

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


async def _process_user_input(cli_session, analysis_agent, user_input):
    """Process a single user input and return the result.
    
    Args:
        cli_session: The SQLite session for conversation memory
        analysis_agent: The persistent agent instance (reused for all messages)
        user_input: The user's query string
    
    Returns:
        RunResult: The result with CLI-specific metadata attached
    """
    try:
        # Start timing for performance metrics
        start_time = time.perf_counter()

        # Call shared processing function (core business logic - no duplication)
        result = await process_query(analysis_agent, cli_session, user_input)

        # Calculate processing time
        processing_time = time.perf_counter() - start_time

        # Extract token data using official OpenAI Agents SDK
        token_count = extract_token_count_from_context_wrapper(result)

        # Create metadata object for CLI response (CLI-specific wrapper)
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
