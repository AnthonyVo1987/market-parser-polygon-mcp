"""
Enhanced Market Parser Chat UI with FSM-Driven Stock Data Display

This module extends the basic chat interface with:
- FSM-based state management for stock data requests
- Structured data display in dataframes
- Action buttons for specific stock analysis types
- Real-time state visualization and debugging
"""

import asyncio
from datetime import date
import os
import tempfile
from typing import Tuple, Optional, List, Dict, Any
import logging

import gradio as gr
import pandas as pd
from dotenv import find_dotenv, load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel

# Import our FSM components and parser
from stock_data_fsm import StateManager, AppState
from response_parser import ResponseParser, DataType

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
    # Avoid explicit shutdown to prevent task/cancel scope mismatches in GUI lifecycles.
    # MCP server processes will terminate when the app process exits.
    return


# -------- FSM-Enhanced Chat Handlers --------

async def handle_fsm_user_message(
    user_message: str,
    chat_history: List[Dict],
    pyd_message_history: List | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
    fsm_manager: StateManager,
    snapshot_df: pd.DataFrame,
    sr_df: pd.DataFrame,
    tech_df: pd.DataFrame,
    debug_state: str,
) -> Tuple:
    """
    Enhanced message handler that works with FSM state management.
    
    Routes messages through FSM when appropriate, otherwise handles as regular chat.
    """
    if pyd_message_history is None:
        pyd_message_history = []

    # Ensure MCP servers are running
    await _startup()

    # Check if this is a regular chat (FSM in IDLE state with no button context)
    if fsm_manager.get_current_state() == AppState.IDLE and not fsm_manager.context.button_type:
        # Handle as regular chat
        chat_history = chat_history + [{"role": "user", "content": user_message}]
        
        print(f"[GUI] Regular Chat - User: {user_message}")
        response = await agent.run(user_message, message_history=pyd_message_history)
        
        output_text = getattr(response, "output", "") or ""
        chat_history = chat_history + [{"role": "assistant", "content": output_text}]
        print(f"[GUI] Regular Chat - Assistant: {output_text[:200]}{'...' if len(output_text) > 200 else ''}")
        
        # Update costs and return
        cost_markdown = await _update_costs(response, tracker)
        pyd_message_history = response.all_messages()
        debug_state = _get_debug_state_info(fsm_manager)
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, debug_state
        )
    
    # FSM-controlled processing for button-triggered requests
    try:
        current_state = fsm_manager.get_current_state()
        print(f"[GUI] FSM Processing - Current State: {current_state.name}")
        
        # Process based on current FSM state
        if current_state == AppState.AI_PROCESSING:
            # Execute AI request using FSM context prompt
            response = await agent.run(fsm_manager.context.prompt, message_history=pyd_message_history)
            
            # Update FSM with AI response
            fsm_manager.transition('response_received', ai_response=response.output)
            
            # Move to parsing
            fsm_manager.transition('parse')
            
            print(f"[GUI] AI Response received: {len(response.output)} characters")
        
        if fsm_manager.get_current_state() == AppState.PARSING_RESPONSE:
            # Parse the AI response using the comprehensive ResponseParser
            button_type = fsm_manager.context.button_type
            ai_response = fsm_manager.context.ai_response
            ticker = fsm_manager.context.ticker
            
            # Initialize parser
            parser = ResponseParser(log_level=logging.INFO)
            
            try:
                # Parse based on button type using the new parser
                if button_type == 'snapshot':
                    parse_result = parser.parse_stock_snapshot(ai_response, ticker)
                    snapshot_df = parse_result.to_dataframe()
                elif button_type == 'support_resistance':
                    parse_result = parser.parse_support_resistance(ai_response, ticker)
                    sr_df = parse_result.to_dataframe()
                elif button_type == 'technical':
                    parse_result = parser.parse_technical_indicators(ai_response, ticker)
                    tech_df = parse_result.to_dataframe()
                
                # Store parse result in FSM context for debug display
                fsm_manager.context.parsed_data = {
                    'parse_result': parse_result.to_dict(),
                    'confidence': parse_result.confidence.value,
                    'warnings': parse_result.warnings
                }
                
                fsm_manager.transition('parse_success', parsed_data={'parsed': True})
            except Exception as e:
                print(f"[GUI] Parse failed: {e}")
                # Fallback to raw display - create empty dataframes
                if button_type == 'snapshot':
                    snapshot_df = pd.DataFrame({'Metric': ['Parse Failed'], 'Value': [str(e)]})
                elif button_type == 'support_resistance':
                    sr_df = pd.DataFrame({'Level': ['Parse Failed'], 'Price': [str(e)]})
                elif button_type == 'technical':
                    tech_df = pd.DataFrame({'Indicator': ['Parse Failed'], 'Value': [str(e)]})
                
                fsm_manager.transition('parse_failed')
        
        if fsm_manager.get_current_state() == AppState.UPDATING_UI:
            # Update chat history with the FSM interaction
            chat_history = chat_history + [
                {"role": "user", "content": fsm_manager.context.prompt},
                {"role": "assistant", "content": fsm_manager.context.ai_response}
            ]
            
            # Complete the FSM cycle
            fsm_manager.transition('update_complete')
            
            # Update costs if we have a response
            if 'response' in locals():
                cost_markdown = await _update_costs(response, tracker)
                pyd_message_history = response.all_messages()
        
        debug_state = _get_debug_state_info(fsm_manager)
        
    except Exception as e:
        print(f"[GUI] FSM Error: {e}")
        # Force FSM to error state and provide recovery
        fsm_manager._emergency_transition_to_error(str(e))
        debug_state = _get_debug_state_info(fsm_manager)
    
    return (
        "", chat_history, pyd_message_history, tracker, cost_markdown,
        fsm_manager, snapshot_df, sr_df, tech_df, debug_state
    )


async def handle_button_click(
    button_type: str,
    ticker: str,
    chat_history: List[Dict],
    pyd_message_history: List | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
    fsm_manager: StateManager,
    snapshot_df: pd.DataFrame,
    sr_df: pd.DataFrame,
    tech_df: pd.DataFrame,
    debug_state: str,
) -> Tuple:
    """
    Handle stock data button clicks through FSM transitions.
    """
    print(f"[GUI] Button clicked: {button_type} for {ticker}")
    
    try:
        # Start FSM workflow
        success = fsm_manager.transition('button_click', 
                                       button_type=button_type, 
                                       ticker=ticker or 'the last mentioned stock')
        
        if not success:
            print(f"[GUI] Button click transition failed")
            debug_state = _get_debug_state_info(fsm_manager)
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_df, sr_df, tech_df, debug_state
            )
        
        # Prepare prompt
        fsm_manager.transition('prepare_prompt')
        
        # Mark prompt as ready
        fsm_manager.transition('prompt_ready')
        
        print(f"[GUI] FSM ready for AI processing. Prompt: {fsm_manager.context.prompt[:100]}...")
        
        # Now process through the FSM message handler
        return await handle_fsm_user_message(
            "",  # No user message for button clicks
            chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, debug_state
        )
        
    except Exception as e:
        print(f"[GUI] Button handler error: {e}")
        fsm_manager._emergency_transition_to_error(str(e))
        debug_state = _get_debug_state_info(fsm_manager)
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, debug_state
        )


# -------- Data Parsing Functions --------
# Note: Data parsing is now handled by the comprehensive ResponseParser class
# located in response_parser.py. This provides robust parsing with multiple
# extraction strategies, data validation, and confidence scoring.


# -------- Utility Functions --------

async def _update_costs(response, tracker: TokenCostTracker) -> str:
    """Update cost tracking and return formatted markdown."""
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
        # Use the tracker to compute and accumulate totals
        tracker.record_and_print(response)
        # Compose a small summary block for the UI
        cost_markdown = (
            f"Per-message: input {request_tokens:,} tok, output {response_tokens:,} tok\n\n"
            f"Session totals: input {tracker.total_input_tokens:,} tok (${"{:.6f}".format(tracker.total_input_cost_usd)}), "
            f"output {tracker.total_output_tokens:,} tok (${"{:.6f}".format(tracker.total_output_cost_usd)}), "
            f"total ${"{:.6f}".format(tracker.total_input_cost_usd + tracker.total_output_cost_usd)}"
        )
        return cost_markdown
    except Exception:
        return ""


def _get_debug_state_info(fsm_manager: StateManager) -> str:
    """Get formatted debug information about FSM state."""
    state_info = [
        f"**Current State:** {fsm_manager.get_current_state().name}",
        f"**Button Type:** {fsm_manager.context.button_type or 'None'}",
        f"**Ticker:** {fsm_manager.context.ticker or 'None'}",
        f"**Error Attempts:** {fsm_manager.context.error_attempts}",
        f"**Total Transitions:** {len(fsm_manager.context.transition_history)}",
    ]
    
    if fsm_manager.context.error_message:
        state_info.append(f"**Error:** {fsm_manager.context.error_message}")
    
    # Add parsing information if available
    if fsm_manager.context.parsed_data and 'parse_result' in fsm_manager.context.parsed_data:
        parse_info = fsm_manager.context.parsed_data
        state_info.append(f"**Parse Confidence:** {parse_info.get('confidence', 'N/A').title()}")
        if parse_info.get('warnings'):
            state_info.append(f"**Parse Warnings:** {len(parse_info['warnings'])}")
    
    # Add recent transitions
    if fsm_manager.context.transition_history:
        recent_transitions = fsm_manager.context.transition_history[-3:]
        state_info.append("**Recent Transitions:**")
        for trans in recent_transitions:
            state_info.append(f"  • {trans.from_state} → {trans.to_state} ({trans.event})")
    
    return "\n".join(state_info)


def _build_markdown_export(chat_messages: list[dict], tracker: TokenCostTracker) -> str:
    """Build markdown export of the chat session."""
    lines: list[str] = ["# Market Parser Chat Export\n"]
    for m in chat_messages or []:
        role = m.get("role", "")
        content = m.get("content", "")
        if role == "user":
            lines.append("\n## User\n")
            lines.append(content)
        elif role == "assistant":
            lines.append("\n## Assistant\n")
            lines.append(content)
    # Append totals if available
    lines.append("\n---\n")
    lines.append("## Session Totals\n")
    lines.append(
        f"Input tokens: {tracker.total_input_tokens:,}  |  Input cost: ${tracker.total_input_cost_usd:.6f}"
    )
    lines.append(
        f"Output tokens: {tracker.total_output_tokens:,}  |  Output cost: ${tracker.total_output_cost_usd:.6f}"
    )
    lines.append(
        f"Total cost: ${(tracker.total_input_cost_usd + tracker.total_output_cost_usd):.6f}"
    )
    return "\n".join(lines) + "\n"


def export_markdown(chat_messages: list[dict], tracker: TokenCostTracker):
    """Export chat to markdown format."""
    text = _build_markdown_export(chat_messages, tracker)
    return text


# -------- Main Gradio Interface --------

def create_empty_dataframes():
    """Create empty dataframes for initialization."""
    snapshot_df = pd.DataFrame({'Metric': ['Ready for data...'], 'Value': ['Click Stock Snapshot button']})
    sr_df = pd.DataFrame({'Level': ['Ready for data...'], 'Price': ['Click Support & Resistance button']})
    tech_df = pd.DataFrame({'Indicator': ['Ready for data...'], 'Value': ['Click Technical Analysis button']})
    return snapshot_df, sr_df, tech_df


with gr.Blocks(title="Market Parser - Enhanced with FSM") as demo:
    gr.Markdown("# Market Parser – Enhanced Chatbot with Stock Data Display")
    gr.Markdown(
        "🚀 **FSM-Enhanced Interface** – This UI includes deterministic state management "
        "for structured stock data requests. Use the action buttons for specific analysis types, "
        "or chat normally for general market questions."
    )

    # -------- Main Chat Interface --------
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500, type="messages", label="Market Analysis Chat")
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask about markets, or use action buttons for structured data...",
                    container=False,
                    scale=4
                )
                send = gr.Button("Send", variant="primary", scale=1)
            
            with gr.Row():
                clear = gr.Button("Clear Chat", variant="secondary")
                ticker_input = gr.Textbox(
                    placeholder="Ticker (e.g., AAPL)", 
                    label="Stock Ticker",
                    container=False,
                    scale=1
                )
        
        with gr.Column(scale=1):
            # -------- FSM Debug Panel (Collapsible) --------
            with gr.Accordion("🔧 FSM State Debug", open=False):
                debug_display = gr.Markdown("**FSM Ready**", label="Current State Info")

    # -------- Stock Data Action Buttons --------
    gr.Markdown("### 📊 Stock Data Actions")
    gr.Markdown("Click these buttons to get structured stock data using FSM-driven analysis:")
    
    with gr.Row():
        snapshot_btn = gr.Button("📈 Stock Snapshot", variant="secondary", scale=1)
        sr_btn = gr.Button("🎯 Support & Resistance", variant="secondary", scale=1)
        tech_btn = gr.Button("🔧 Technical Analysis", variant="secondary", scale=1)

    # -------- Stock Data Display Area --------
    gr.Markdown("### 📋 Stock Data Display")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("**Stock Snapshot**")
            snapshot_df_display = gr.Dataframe(
                headers=["Metric", "Value"],
                datatype=["str", "str"],
                label="Current Stock Snapshot",
                interactive=False,
                wrap=True
            )
        
        with gr.Column():
            gr.Markdown("**Support & Resistance Levels**")
            sr_df_display = gr.Dataframe(
                headers=["Level", "Price"],
                datatype=["str", "str"],
                label="Support & Resistance Analysis",
                interactive=False,
                wrap=True
            )
        
        with gr.Column():
            gr.Markdown("**Technical Indicators**")
            tech_df_display = gr.Dataframe(
                headers=["Indicator", "Value"],
                datatype=["str", "str"],
                label="Technical Analysis",
                interactive=False,
                wrap=True
            )

    # -------- Cost Tracking & Export --------
    with gr.Accordion("💰 Cost Tracking & Export", open=False):
        costs = gr.Markdown()
        export_md = gr.Textbox(label="Markdown export", lines=8)
        export_btn = gr.Button("Export Chat to Markdown")

    # -------- State Management --------
    # Traditional state
    pyd_history_state = gr.State([])
    tracker_state = gr.State(TokenCostTracker())
    costs_state = gr.State("")
    
    # FSM state
    fsm_state = gr.State(StateManager(session_id="gradio-enhanced"))
    
    # DataFrames state
    snapshot_df_state = gr.State()
    sr_df_state = gr.State()
    tech_df_state = gr.State()
    
    # Initialize dataframes
    init_snapshot, init_sr, init_tech = create_empty_dataframes()
    snapshot_df_display.value = init_snapshot
    sr_df_display.value = init_sr
    tech_df_display.value = init_tech

    # -------- Event Handlers --------
    
    # Regular chat message handling
    msg.submit(
        handle_fsm_user_message,
        inputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs_state,
            fsm_state, snapshot_df_state, sr_df_state, tech_df_state, debug_display
        ],
        outputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs,
            fsm_state, snapshot_df_display, sr_df_display, tech_df_display, debug_display
        ]
    )
    
    send.click(
        handle_fsm_user_message,
        inputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs_state,
            fsm_state, snapshot_df_state, sr_df_state, tech_df_state, debug_display
        ],
        outputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs,
            fsm_state, snapshot_df_display, sr_df_display, tech_df_display, debug_display
        ]
    )
    
    # Stock data action buttons
    snapshot_btn.click(
        lambda ticker, *args: handle_button_click('snapshot', ticker, *args),
        inputs=[
            ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
            fsm_state, snapshot_df_state, sr_df_state, tech_df_state, debug_display
        ],
        outputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs,
            fsm_state, snapshot_df_display, sr_df_display, tech_df_display, debug_display
        ]
    )
    
    sr_btn.click(
        lambda ticker, *args: handle_button_click('support_resistance', ticker, *args),
        inputs=[
            ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
            fsm_state, snapshot_df_state, sr_df_state, tech_df_state, debug_display
        ],
        outputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs,
            fsm_state, snapshot_df_display, sr_df_display, tech_df_display, debug_display
        ]
    )
    
    tech_btn.click(
        lambda ticker, *args: handle_button_click('technical', ticker, *args),
        inputs=[
            ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
            fsm_state, snapshot_df_state, sr_df_state, tech_df_state, debug_display
        ],
        outputs=[
            msg, chatbot, pyd_history_state, tracker_state, costs,
            fsm_state, snapshot_df_display, sr_df_display, tech_df_display, debug_display
        ]
    )
    
    # Clear function
    def _clear_enhanced():
        snapshot_df, sr_df, tech_df = create_empty_dataframes()
        return (
            [],  # chat_history
            [],  # pyd_history_state
            TokenCostTracker(),  # tracker_state
            "",  # costs
            "",  # export_md
            StateManager(session_id="gradio-enhanced-new"),  # fsm_state
            snapshot_df,  # snapshot_df_display
            sr_df,  # sr_df_display
            tech_df,  # tech_df_display
            "**FSM Reset**"  # debug_display
        )
    
    clear.click(
        _clear_enhanced,
        inputs=[],
        outputs=[
            chatbot, pyd_history_state, tracker_state, costs, export_md,
            fsm_state, snapshot_df_display, sr_df_display, tech_df_display, debug_display
        ]
    )
    
    # Export functionality
    export_btn.click(export_markdown, [chatbot, tracker_state], [export_md])


if __name__ == "__main__":
    # Initialize logging for FSM
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Starting Enhanced Market Parser with FSM Integration")
    print("   - FSM-driven stock data requests")
    print("   - Structured data display in dataframes")
    print("   - Debug state visualization")
    print("   - Backward compatible with regular chat")
    
    # Launch the enhanced GUI
    demo.queue()
    demo.launch(
        server_name=os.getenv("HOST", "127.0.0.1"), 
        server_port=int(os.getenv("PORT", "7861")),  # Different port to avoid conflicts
        show_api=False
    )
