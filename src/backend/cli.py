"""CLI functionality for the Market Parser application."""

import time
from datetime import datetime

from agents import Runner, SQLiteSession

from .config import settings
from .services import create_agent
from .utils import print_error, print_response
from .utils.token_utils import extract_token_usage_from_context_wrapper


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


def _format_performance_footer(processing_time: float, token_usage: dict, model_name: str) -> str:
    """Format performance metrics footer as plain text.

    This function generates the canonical footer format used by ALL interfaces.
    No Rich markup - plain text only for maximum compatibility.

    Args:
        processing_time: Query processing time in seconds
        token_usage: Dict with token counts from extract_token_usage_from_context_wrapper()
        model_name: Model name (e.g., "gpt-5-nano")

    Returns:
        str: Formatted footer text

    Example Output:
        Performance Metrics:
           Response Time: 5.135s
           Tokens Used: 21,701 (Input: 21,402, Output: 299)
           Model: gpt-5-nano
    """
    footer = "Performance Metrics:\n"
    footer += f"   Response Time: {processing_time:.3f}s\n"

    # Add token information if available
    if token_usage:
        token_count = token_usage.get("total_tokens")
        input_tokens = token_usage.get("input_tokens")
        output_tokens = token_usage.get("output_tokens")
        cached_input = token_usage.get("cached_input_tokens", 0)
        cached_output = token_usage.get("cached_output_tokens", 0)

        if token_count:
            footer += f"   Tokens Used: {token_count:,}"

            if input_tokens and output_tokens:
                footer += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"

                # Show cache hit information if tokens were cached
                if cached_input > 0 or cached_output > 0:
                    cache_parts = []
                    if cached_input > 0:
                        cache_parts.append(f"Cached Input: {cached_input:,}")
                    if cached_output > 0:
                        cache_parts.append(f"Cached Output: {cached_output:,}")
                    footer += f" | {', '.join(cache_parts)}"

            footer += "\n"

    # Add model information
    footer += f"   Model: {model_name}\n"

    return footer


async def process_query_with_footer(agent, session, user_input):
    """Process query and return complete response with performance metrics footer.

    This is the SINGLE SOURCE OF TRUTH for performance metrics footer generation.
    All interfaces (CLI, Gradio) call this function.

    Following the architecture principle "CLI = core, GUI = wrapper":
    - CLI owns core business logic (this function)
    - GUIs import and call this function (no duplication)

    Args:
        agent: The persistent agent instance
        session: The SQLite session for conversation memory
        user_input: The user's query string

    Returns:
        str: Complete response text with performance metrics footer appended

    Architecture Pattern:
        User Input → Interface → process_query_with_footer() → process_query() → Agent

    Example Return Value:
        "[Agent Response Text]

        Performance Metrics:
           Response Time: 5.135s
           Tokens Used: 21,701 (Input: 21,402, Output: 299)
           Model: gpt-5-nano
        "
    """
    # Measure processing time
    start_time = time.perf_counter()

    # Call core query processor (existing shared function)
    result = await process_query(agent, session, user_input)

    # Calculate processing time
    processing_time = time.perf_counter() - start_time

    # Extract response text from agent
    response_text = str(result.final_output)

    # Extract token usage using shared utility
    token_usage = extract_token_usage_from_context_wrapper(result)

    # Get model name from settings
    model_name = settings.available_models[0]

    # Format footer using shared utility (single source of truth)
    footer = _format_performance_footer(processing_time, token_usage, model_name)

    # Return complete response with footer appended
    return response_text + "\n\n" + footer


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

            # Process the user input with persistent agent (returns complete response with footer)
            complete_response = await _process_user_input(cli_session, analysis_agent, user_input)

            # Display the complete response (footer already included)
            print_response(complete_response)

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
    """Process user input using CLI core function with footer.

    Calls process_query_with_footer() which returns complete response
    with performance metrics footer already included.

    Args:
        cli_session: The SQLite session for conversation memory
        analysis_agent: The persistent agent instance (reused for all messages)
        user_input: The user's query string

    Returns:
        str: Complete response text with performance metrics footer
    """
    try:
        # Call CLI core function - returns complete response with footer
        complete_response = await process_query_with_footer(
            analysis_agent,
            cli_session,
            user_input
        )

        return complete_response

    except Exception as e:
        print_error(e, "AI Model Error")
        return f"Error: Unable to process request. {str(e)}"

if __name__ == "__main__":
    import asyncio
    asyncio.run(cli_async())
