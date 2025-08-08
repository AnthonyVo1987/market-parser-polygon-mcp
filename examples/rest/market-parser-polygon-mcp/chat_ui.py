import asyncio
from datetime import date
import os

import gradio as gr
from dotenv import find_dotenv, load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel

# Reuse server factory and token tracking from CLI
from market_parser_demo import create_polygon_mcp_server, TokenCostTracker


# Load .env from nearest path so GUI behaves the same as CLI
_ENV_PATH = find_dotenv()
load_dotenv(_ENV_PATH)


# -------- Agent & MCP server setup --------
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5-nano")

server = create_polygon_mcp_server()
model = OpenAIResponsesModel(MODEL_NAME)
agent = Agent(
    model=model,
    mcp_servers=[server],
    system_prompt=(
        "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
        "Use the latest data available. Always double check your math. "
        "For any questions about the current date, use the 'get_today_date' tool. "
        "For long or complex queries, break the query into logical subtasks and process each subtask in order."
    ),
)


@agent.tool
def get_today_date(ctx: RunContext) -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return str(date.today())


# Keep MCP servers running while the app is live
_mcp_ctx = None


async def _startup():
    global _mcp_ctx
    if _mcp_ctx is None:
        _mcp_ctx = agent.run_mcp_servers()
        await _mcp_ctx.__aenter__()


async def _shutdown():
    global _mcp_ctx
    if _mcp_ctx is not None:
        await _mcp_ctx.__aexit__(None, None, None)
        _mcp_ctx = None


# -------- Chat handlers --------
async def handle_user_message(
    user_message: str,
    chat_history: list[tuple[str, str]],
    pyd_message_history: list | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
):
    if pyd_message_history is None:
        pyd_message_history = []

    # Run the agent with persisted message history
    response = await agent.run(user_message, message_history=pyd_message_history)

    # Append assistant output to chat
    output_text = getattr(response, "output", "") or ""
    chat_history = chat_history + [(user_message, output_text)]

    # Update token & cost usage and format a compact summary for the UI
    try:
        usage = response.usage()
        request_tokens = (
            getattr(usage, "request_tokens", None)
            or getattr(usage, "input_tokens", 0)
            or 0
        )
        response_tokens = (
            getattr(usage, "response_tokens", None)
            or getattr(usage, "output_tokens", 0)
            or 0
        )
        # Use the tracker to compute and accumulate totals (it will also print to console)
        tracker.record_and_print(response)
        # Compose a small summary block for the UI
        cost_markdown = (
            f"Per-message: input {request_tokens:,} tok, output {response_tokens:,} tok\n\n"
            f"Session totals: input {tracker.total_input_tokens:,} tok (${"{:.6f}".format(tracker.total_input_cost_usd)}), "
            f"output {tracker.total_output_tokens:,} tok (${"{:.6f}".format(tracker.total_output_cost_usd)}), "
            f"total ${"{:.6f}".format(tracker.total_input_cost_usd + tracker.total_output_cost_usd)}"
        )
    except Exception:
        # Fallback if usage not available
        cost_markdown = ""

    # Persist message history for next turn
    pyd_message_history = response.all_messages()
    return "", chat_history, pyd_message_history, tracker, cost_markdown


with gr.Blocks() as demo:
    gr.Markdown("# Market Parser – Chatbot GUI")
    gr.Markdown(
        "This UI uses the same agent as the CLI and the Polygon MCP server. Set pricing env vars for cost estimates."
    )

    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(placeholder="Ask about markets, e.g. 'NVDA snapshot'…")
    send = gr.Button("Send")
    clear = gr.Button("Clear")

    costs = gr.Markdown()

    # State: Pydantic-AI message history and TokenCostTracker
    pyd_history_state = gr.State([])
    tracker_state = gr.State(TokenCostTracker())
    costs_state = gr.State("")

    # Wire events
    msg.submit(
        handle_user_message,
        [msg, chatbot, pyd_history_state, tracker_state, costs_state],
        [msg, chatbot, pyd_history_state, tracker_state, costs],
    )
    send.click(
        handle_user_message,
        [msg, chatbot, pyd_history_state, tracker_state, costs_state],
        [msg, chatbot, pyd_history_state, tracker_state, costs],
    )

    def _clear(chat_history: list[tuple[str, str]]):
        return [], [], TokenCostTracker(), ""

    clear.click(_clear, [chatbot], [chatbot, pyd_history_state, tracker_state, costs])

    demo.load(lambda: asyncio.run(_startup()))
    demo.unload(lambda: asyncio.run(_shutdown()))


if __name__ == "__main__":
    # Launch the GUI. Users can override host/port via env if desired.
    demo.queue()
    demo.launch(server_name=os.getenv("HOST", "127.0.0.1"), server_port=int(os.getenv("PORT", "7860")))


