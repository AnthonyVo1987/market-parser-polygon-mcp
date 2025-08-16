import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from rich.console import Console
from rich.markdown import Markdown
from pydantic_ai import Agent, RunContext
from pydantic_ai.mcp import MCPServerStdio

# Load env from nearest .env up the directory tree (project root or example dir)
_ENV_PATH = find_dotenv()
load_dotenv(_ENV_PATH)
if _ENV_PATH:
    print(f"Loaded .env from: {_ENV_PATH}")

# ------------- MCP Server Factory -------------
def create_polygon_mcp_server():
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    if not polygon_api_key:
      raise Exception("POLYGON_API_KEY is not set in the environment or .env file.")
    env = os.environ.copy()
    env["POLYGON_API_KEY"] = polygon_api_key
    return MCPServerStdio(
        command="uvx",
        args=[
            "--from",
            "git+https://github.com/polygon-io/mcp_polygon@v0.4.0",
            "mcp_polygon"
        ],
        env=env
    )

# ------------- CLI Logic -------------
console = Console()

class TokenCostTracker:
    """Tracks per-message and cumulative token usage and costs."""

    def __init__(self) -> None:
        # Prices can be set via usd per 1M tokens OR per token
        self.input_price_per_million: float
        self.output_price_per_million: float
        self.input_price_per_token: float
        self.output_price_per_token: float

        (
            self.input_price_per_million,
            self.input_price_per_token,
        ) = self._read_price_config(
            [
                "OPENAI_GPT5_NANO_INPUT_PRICE_PER_1M",
                "OPENAI_INPUT_PRICE_PER_1M",
            ],
            [
                "OPENAI_GPT5_NANO_INPUT_PRICE_PER_TOKEN",
                "OPENAI_INPUT_PRICE_PER_TOKEN",
            ],
        )
        (
            self.output_price_per_million,
            self.output_price_per_token,
        ) = self._read_price_config(
            [
                "OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_1M",
                "OPENAI_OUTPUT_PRICE_PER_1M",
            ],
            [
                "OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_TOKEN",
                "OPENAI_OUTPUT_PRICE_PER_TOKEN",
            ],
        )

        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_input_cost_usd: float = 0.0
        self.total_output_cost_usd: float = 0.0

        self._printed_pricing_hint: bool = False

    @staticmethod
    def _safe_float(value: str | None) -> float:
        try:
            return float(value) if value else 0.0
        except Exception:
            return 0.0

    def _read_price_config(
        self, per_million_envs: list[str], per_token_envs: list[str]
    ) -> tuple[float, float]:
        per_million = 0.0
        per_token = 0.0
        for key in per_million_envs:
            per_million = self._safe_float(os.getenv(key))
            if per_million:
                break
        for key in per_token_envs:
            per_token = self._safe_float(os.getenv(key))
            if per_token:
                break
        return per_million, per_token

    def _calc_cost(self, tokens: int, price_per_million: float, price_per_token: float) -> float:
        if price_per_token:
            return tokens * price_per_token
        return (tokens / 1_000_000.0) * price_per_million

    def record_and_print(self, response) -> None:
        """Record usage/cost for this response and print per-message and session totals."""
        # Try to get usage from the response
        usage = None
        try:
            # pydantic-ai AgentRunResult typically exposes usage() method
            if hasattr(response, "usage"):
                usage = response.usage()
        except Exception:
            usage = None

        # Fallback attempt: some responses might have .data or similar
        if usage is None:
            # If usage is unavailable, skip printing detailed token info
            console.print("[yellow]Token usage not available from provider response.[/yellow]")
            return

        # Extract tokens
        request_tokens = getattr(usage, "request_tokens", None)
        response_tokens = getattr(usage, "response_tokens", None)
        if request_tokens is None and hasattr(usage, "input_tokens"):
            request_tokens = getattr(usage, "input_tokens")
        if response_tokens is None and hasattr(usage, "output_tokens"):
            response_tokens = getattr(usage, "output_tokens")

        if request_tokens is None:
            request_tokens = 0
        if response_tokens is None:
            response_tokens = 0

        # Calculate costs for this message
        input_cost = self._calc_cost(
            request_tokens, self.input_price_per_million, self.input_price_per_token
        )
        output_cost = self._calc_cost(
            response_tokens, self.output_price_per_million, self.output_price_per_token
        )

        # Update totals
        self.total_input_tokens += int(request_tokens)
        self.total_output_tokens += int(response_tokens)
        self.total_input_cost_usd += input_cost
        self.total_output_cost_usd += output_cost

        # Pricing hint if prices are unset
        if not self._printed_pricing_hint and (
            (self.input_price_per_million == 0.0 and self.input_price_per_token == 0.0)
            or (self.output_price_per_million == 0.0 and self.output_price_per_token == 0.0)
        ):
            console.print(
                "[yellow]Tip: set pricing in .env for accurate cost estimates. Supported envs:"
            )
            console.print(
                "[yellow]  - OPENAI_GPT5_NANO_INPUT_PRICE_PER_1M or OPENAI_INPUT_PRICE_PER_1M[/yellow]"
            )
            console.print(
                "[yellow]  - OPENAI_GPT5_NANO_OUTPUT_PRICE_PER_1M or OPENAI_OUTPUT_PRICE_PER_1M[/yellow]"
            )
            console.print(
                "[yellow]  - Alternatively per-token: OPENAI_GPT5_NANO_INPUT_PRICE_PER_TOKEN / OPENAI_INPUT_PRICE_PER_TOKEN and matching OUTPUT vars[/yellow]"
            )
            self._printed_pricing_hint = True

        # Print per-message summary
        console.print("[bold]Per Message Usage & Cost:[/bold]")
        console.print(
            f"  - Input tokens: {request_tokens:,} | Input cost: ${input_cost:.6f}"
        )
        console.print(
            f"  - Output tokens: {response_tokens:,} | Output cost: ${output_cost:.6f}"
        )
        console.print(
            f"  - Message total cost: ${(input_cost + output_cost):.6f}"
        )

        # Print session cumulative summary
        console.print("[bold]Session Total (Cumulative):[/bold]")
        console.print(
            f"  - Total input tokens: {self.total_input_tokens:,} | Total input cost: ${self.total_input_cost_usd:.6f}"
        )
        console.print(
            f"  - Total output tokens: {self.total_output_tokens:,} | Total output cost: ${self.total_output_cost_usd:.6f}"
        )
        console.print(
            f"  - Session total cost: ${(self.total_input_cost_usd + self.total_output_cost_usd):.6f}\n"
        )

def print_agent_response(response):
    console.print("\n[bold green]✔ Query processed successfully![/bold green]")
    console.print("[bold]Agent Response:[/bold]")
    output = getattr(response, "output", None)
    if output is not None:
        # Try to render as Markdown if it looks like Markdown
        if any(tag in output for tag in ["#", "*", "`", "-", ">"]):
            console.print(Markdown(output))
        else:
            console.print(output.strip())
    elif isinstance(response, str):
        console.print(response.strip())
    else:
        console.print(str(response))
    console.print("---------------------\n")

def print_agent_error(error):
    console.print("\n[bold red]!!! Error !!![/bold red]")
    if isinstance(error, Exception):
        console.print(str(error).strip())
    elif isinstance(error, dict):
        import json
        console.print(json.dumps(error, indent=2))
    else:
        console.print(str(error).strip())
    console.print("------------------\n")

def print_tools_used(response):
    tools = set()
    for msg in response.all_messages():
        if hasattr(msg, "parts"):
            for part in msg.parts:
                if hasattr(part, "tool_name"):
                    tools.add(part.tool_name)
    if tools:
        print("Tools used in this run:", ", ".join(tools))
    else:
        print("No tools used in this run.")

async def cli_async():
    print("Welcome to the Market Parser CLI. Type 'exit' to quit.")
    try:
        server = create_polygon_mcp_server()
        from pydantic_ai.models.openai import OpenAIResponsesModel

        # Configure OpenAI Responses API model with gpt-5-nano
        # Uses OPENAI_API_KEY from environment automatically
        model = OpenAIResponsesModel('gpt-5-nano')

        agent = Agent(
            model=model,
            mcp_servers=[server],
            system_prompt=(
                "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
                "Use the latest data available. Always double check your math. "
                "For any questions about the current date, use the 'get_today_date' tool. "
                "For long or complex queries, break the query into logical subtasks and process each subtask in order."
            )
        )

        # Add a custom tool to provide today's date
        from datetime import date
        @agent.tool
        def get_today_date(ctx: RunContext) -> str:
            """Returns today's date in YYYY-MM-DD format."""
            return str(date.today())


        token_tracker = TokenCostTracker()

        async with agent.run_mcp_servers():
            message_history = []
            while True:
                try:
                    user_input = input('> ').strip()
                    if user_input.lower() == 'exit':
                        print("Goodbye!")
                        break
                    try:
                        # Run the agent with the current message history
                        response = await agent.run(
                            user_input,
                            message_history=message_history
                        )
                        print("\r", end="")
                        print_agent_response(response)
                        print_tools_used(response)
                        # Token & cost usage
                        token_tracker.record_and_print(response)
                        # Use the agent's own message objects for the next run
                        message_history = response.all_messages()
                    except Exception as agent_err:
                        print("\r", end="")
                        print_agent_error(agent_err)
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    break
                except Exception as e:
                    print_agent_error(e)
    except Exception as setup_err:
        print(f"Failed to start CLI agent or MCP server: {setup_err}")

def main():
    asyncio.run(cli_async())

if __name__ == "__main__":
    main() 