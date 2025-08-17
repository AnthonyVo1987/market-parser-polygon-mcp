"""
Enhanced Stock Market Analysis Chat UI - Phase 5 Implementation
Final integrated version with comprehensive FSM, enhanced parsing, 
prompt templates, loading states, error handling, and user feedback.
"""

import os
import asyncio
import logging
from typing import List, Dict, Tuple, Any, Optional
import time
import traceback

import gradio as gr
import pandas as pd
from dotenv import find_dotenv, load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel

# Import our comprehensive systems
from stock_data_fsm import StateManager, AppState
from response_parser import ResponseParser, DataType
from prompt_templates import PromptTemplateManager, PromptType

# Reuse server factory and token tracking from CLI
from market_parser_demo import create_polygon_mcp_server, TokenCostTracker

# Load environment variables
load_dotenv(find_dotenv())

# -------- Global state for MCP server management --------
_mcp_ctx = None


# -------- Agent & MCP server setup --------
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

server = create_polygon_mcp_server()
model = OpenAIResponsesModel(MODEL_NAME)

# Initialize enhanced systems
prompt_manager = PromptTemplateManager()
response_parser = ResponseParser(log_level=logging.INFO)

# Enhanced system prompt for structured output
base_system_prompt = (
    "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
    "Use the latest data available. Always double check your math. "
    "For any questions about the current date, use the 'get_today_date' tool. "
    "For long or complex queries, break the query into logical subtasks and process each subtask in order."
)

enhanced_system_prompt = prompt_manager.get_enhanced_system_prompt(base_system_prompt)

agent = Agent(
    model=model,
    mcp_servers=[server],
    system_prompt=enhanced_system_prompt,
)


@agent.tool
def get_today_date(ctx: RunContext) -> str:
    """Returns today's date in YYYY-MM-DD format."""
    import datetime
    return datetime.date.today().strftime("%Y-%m-%d")


# -------- Enhanced Loading and Status Management --------

class ProcessingStatus:
    """Manages processing status and loading states"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.is_processing = False
        self.status_message = ""
        self.progress = 0
        self.start_time = None
        self.current_step = ""
        self.total_steps = 0
    
    def start_processing(self, message: str, total_steps: int = 5):
        self.is_processing = True
        self.status_message = message
        self.progress = 0
        self.start_time = time.time()
        self.current_step = "Initializing..."
        self.total_steps = total_steps
    
    def update_step(self, step: str, progress: int):
        self.current_step = step
        self.progress = min(progress, self.total_steps)
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.status_message = f"🔄 {step} ({self.progress}/{self.total_steps}) - {elapsed:.1f}s"
    
    def complete(self, message: str = "✅ Complete"):
        self.is_processing = False
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.status_message = f"{message} - {elapsed:.1f}s"
        self.progress = self.total_steps
        self.current_step = "Finished"
    
    def error(self, message: str):
        self.is_processing = False
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.status_message = f"❌ {message} - {elapsed:.1f}s"
        self.current_step = "Error"


# Global processing status
processing_status = ProcessingStatus()


# -------- MCP Server Management --------

async def _startup():
    """Initialize MCP servers"""
    global _mcp_ctx
    if _mcp_ctx is None:
        # Gradio runs in event loop; use asyncio context manager
        from contextlib import AsyncExitStack
        _mcp_ctx = AsyncExitStack()


async def _shutdown():
    """Clean shutdown of MCP servers"""
    global _mcp_ctx
    # Avoid explicit shutdown to prevent task/cancel scope mismatches in GUI lifecycles.
    # MCP server processes will terminate when the app process exits.
    return


# -------- Enhanced Chat Handlers with Loading States --------

async def handle_user_message(
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
    Enhanced message handler with loading states and improved error handling.
    """
    if pyd_message_history is None:
        pyd_message_history = []

    # Update processing status
    processing_status.start_processing("Processing regular chat message", total_steps=3)
    
    try:
        # Ensure MCP servers are running
        processing_status.update_step("Initializing MCP servers...", 1)
        await _startup()
        
        # Check if this is a regular chat (FSM in IDLE state with no button context)
        if fsm_manager.get_current_state() == AppState.IDLE and not fsm_manager.context.button_type:
            # Handle as regular chat
            processing_status.update_step("Processing regular chat...", 2)
            chat_history = chat_history + [{"role": "user", "content": user_message}]
            
            print(f"[GUI] Regular Chat - User: {user_message}")
            response = await agent.run(user_message, message_history=pyd_message_history)
            
            chat_history = chat_history + [{"role": "assistant", "content": response.output}]
            pyd_message_history.append({"role": "user", "content": user_message})
            pyd_message_history.append({"role": "assistant", "content": response.output})
            
            # Update costs
            processing_status.update_step("Updating costs...", 3)
            cost_markdown = await _update_costs(response, tracker)
            
            processing_status.complete("Regular chat completed")
            print(f"[GUI] Regular Chat Response: {response.output[:100]}...")
            
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_df, sr_df, tech_df, processing_status.status_message
            )
        
        else:
            # This shouldn't happen in regular flow, but handle gracefully
            processing_status.error("Invalid state for regular message")
            debug_state = _get_debug_state_info(fsm_manager)
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_df, sr_df, tech_df, f"{processing_status.status_message}\n{debug_state}"
            )
            
    except Exception as e:
        processing_status.error(f"Chat error: {str(e)}")
        error_message = f"❌ Error processing message: {str(e)}"
        print(f"[GUI] Error in regular chat: {e}")
        traceback.print_exc()
        
        # Add error message to chat
        chat_history = chat_history + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": error_message}
        ]
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, processing_status.status_message
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
    Enhanced button click handler with comprehensive loading states and error handling.
    """
    print(f"[GUI] Button clicked: {button_type} for {ticker}")
    
    # Start processing with detailed steps
    processing_status.start_processing(f"Processing {button_type} analysis", total_steps=7)
    
    try:
        # Step 1: Initialize FSM transition
        processing_status.update_step("Initializing FSM transition...", 1)
        success = fsm_manager.transition('button_click', 
                                       button_type=button_type, 
                                       ticker=ticker or 'the last mentioned stock')
        
        if not success:
            processing_status.error("FSM transition failed")
            debug_state = _get_debug_state_info(fsm_manager)
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_df, sr_df, tech_df, f"{processing_status.status_message}\n{debug_state}"
            )
        
        # Step 2: Generate enhanced prompt
        processing_status.update_step("Generating structured prompt...", 2)
        prompt_type_map = {
            'snapshot': PromptType.SNAPSHOT,
            'support_resistance': PromptType.SUPPORT_RESISTANCE,
            'technical': PromptType.TECHNICAL
        }
        
        prompt_type = prompt_type_map.get(button_type)
        if prompt_type:
            prompt, ticker_context = prompt_manager.generate_prompt(
                prompt_type=prompt_type,
                ticker=ticker,
                chat_history=chat_history
            )
            fsm_manager.context.prompt = prompt
            fsm_manager.context.ticker = ticker_context.symbol
            
            print(f"[GUI] Enhanced prompt generated for {ticker_context.symbol} (confidence: {ticker_context.confidence})")
        else:
            processing_status.error(f"Unknown button type: {button_type}")
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_df, sr_df, tech_df, processing_status.status_message
            )
        
        # Step 3: Prepare prompt and transition FSM
        processing_status.update_step("Preparing FSM prompt...", 3)
        fsm_manager.transition('prepare_prompt')
        fsm_manager.transition('prompt_ready')
        
        # Step 4: Execute AI processing
        processing_status.update_step(f"Getting AI analysis for {fsm_manager.context.ticker}...", 4)
        await _startup()  # Ensure MCP servers are running
        
        print(f"[GUI] Sending prompt to AI: {fsm_manager.context.prompt[:100]}...")
        response = await agent.run(fsm_manager.context.prompt, message_history=pyd_message_history)
        fsm_manager.context.ai_response = response.output
        fsm_manager.transition('response_received')
        
        # Step 5: Parse AI response
        processing_status.update_step("Parsing structured data...", 5)
        fsm_manager.transition('parse')
        
        # Enhanced parsing with detailed feedback
        data_type_map = {
            'snapshot': DataType.SNAPSHOT,
            'support_resistance': DataType.SUPPORT_RESISTANCE,
            'technical': DataType.TECHNICAL
        }
        
        data_type = data_type_map[button_type]
        parse_result = response_parser.parse_any(
            fsm_manager.context.ai_response, 
            data_type, 
            fsm_manager.context.ticker
        )
        
        # Update appropriate DataFrame
        if button_type == 'snapshot':
            snapshot_df = parse_result.to_dataframe()
        elif button_type == 'support_resistance':
            sr_df = parse_result.to_dataframe()
        elif button_type == 'technical':
            tech_df = parse_result.to_dataframe()
        
        fsm_manager.transition('parse_success')
        
        # Step 6: Update UI and chat history
        processing_status.update_step("Updating display...", 6)
        fsm_manager.transition('update_complete')
        
        # Add to chat history with enhanced formatting
        confidence_emoji = "🎯" if parse_result.confidence.value == "high" else "⚡" if parse_result.confidence.value == "medium" else "⚠️"
        
        enhanced_response = f"{confidence_emoji} **{button_type.replace('_', ' ').title()} Analysis for {fsm_manager.context.ticker}**\n\n{response.output}"
        
        if parse_result.warnings:
            enhanced_response += f"\n\n⚠️ **Parse Warnings:**\n" + "\n".join([f"• {w}" for w in parse_result.warnings])
        
        chat_history = chat_history + [
            {"role": "user", "content": f"📊 {button_type.replace('_', ' ').title()} for {fsm_manager.context.ticker}"},
            {"role": "assistant", "content": enhanced_response}
        ]
        
        # Update message history
        if pyd_message_history is None:
            pyd_message_history = []
        pyd_message_history.append({"role": "user", "content": fsm_manager.context.prompt})
        pyd_message_history.append({"role": "assistant", "content": response.output})
        
        # Step 7: Update costs and finalize
        processing_status.update_step("Finalizing...", 7)
        cost_markdown = await _update_costs(response, tracker)
        
        # Reset FSM for next interaction
        fsm_manager.transition('abort')  # Return to IDLE
        
        # Create detailed debug info
        parse_info = f"""**Parse Results:**
- Confidence: {parse_result.confidence.value.title()} ({len(parse_result.parsed_data)}/{len(parse_result.matched_patterns + parse_result.failed_patterns)} fields)
- Parse Time: {parse_result.parse_time_ms:.1f}ms
- Warnings: {len(parse_result.warnings)}"""
        
        debug_state = f"{_get_debug_state_info(fsm_manager)}\n\n{parse_info}"
        
        processing_status.complete(f"✅ {button_type.replace('_', ' ').title()} analysis complete")
        
        print(f"[GUI] Button processing completed successfully for {fsm_manager.context.ticker}")
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, f"{processing_status.status_message}\n{debug_state}"
        )
        
    except Exception as e:
        processing_status.error(f"Button processing error: {str(e)}")
        print(f"[GUI] Error in button processing: {e}")
        traceback.print_exc()
        
        # Force FSM to error state and provide recovery
        fsm_manager._emergency_transition_to_error(str(e))
        debug_state = _get_debug_state_info(fsm_manager)
        
        # Add error to chat history
        error_message = f"❌ Error processing {button_type} analysis: {str(e)}\n\nPlease try again or check your ticker symbol."
        
        chat_history = chat_history + [
            {"role": "user", "content": f"📊 {button_type.replace('_', ' ').title()} for {ticker or 'unknown ticker'}"},
            {"role": "assistant", "content": error_message}
        ]
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, f"{processing_status.status_message}\n{debug_state}"
        )


# -------- Utility Functions --------

async def _update_costs(response, tracker: TokenCostTracker) -> str:
    """Update cost tracking with enhanced formatting"""
    try:
        if hasattr(response, "usage"):
            await tracker.add_response(response)
        
        cost_markdown = f"""## 💰 Cost Tracking
**Total Requests:** {getattr(tracker, 'total_requests', 0)}
**Total Tokens:** {getattr(tracker, 'total_tokens', 0):,}
**Estimated Cost:** ${getattr(tracker, 'total_cost', getattr(tracker, 'total_costs', 0.0)):.4f}

**Last Request:**
- Input: {getattr(tracker, 'last_input_tokens', 0):,} tokens
- Output: {getattr(tracker, 'last_output_tokens', 0):,} tokens
- Cost: ${getattr(tracker, 'last_cost', 0.0):.4f}
"""
        return cost_markdown
    except Exception:
        return "Cost tracking unavailable"


def _get_debug_state_info(fsm_manager: StateManager) -> str:
    """Get enhanced debug information about FSM state"""
    state_info = [
        f"**FSM State:** {fsm_manager.get_current_state().name}",
        f"**Button Type:** {fsm_manager.context.button_type or 'None'}",
        f"**Ticker:** {fsm_manager.context.ticker or 'None'}",
        f"**Error Attempts:** {getattr(fsm_manager.context, 'error_attempts', getattr(fsm_manager.context, 'error_recovery_attempts', 0))}",
        f"**Total Transitions:** {len(fsm_manager.context.transition_history)}",
    ]
    
    if fsm_manager.context.error_message:
        state_info.append(f"**Error:** {fsm_manager.context.error_message}")
    
    # Add ticker context info if available
    if hasattr(fsm_manager.context, 'ticker_context'):
        ticker_ctx = fsm_manager.context.ticker_context
        if isinstance(ticker_ctx, dict):
            state_info.append(f"**Ticker Source:** {ticker_ctx.get('source', 'unknown')}")
            state_info.append(f"**Ticker Confidence:** {ticker_ctx.get('confidence', 0):.2f}")
    
    # Add recent transitions
    if fsm_manager.context.transition_history:
        recent_transitions = fsm_manager.context.transition_history[-3:]
        state_info.append("**Recent Transitions:**")
        for trans in recent_transitions:
            if hasattr(trans, 'from_state') and hasattr(trans, 'to_state'):
                state_info.append(f"  • {trans.from_state} → {trans.to_state} ({trans.event})")
    
    return "\n".join(state_info)


def _clear_enhanced():
    """Enhanced clear function with status reset"""
    processing_status.reset()
    fsm_manager = StateManager()
    empty_df = pd.DataFrame()
    return (
        [],  # chatbot
        [],  # pyd_history_state
        TokenCostTracker(),  # tracker_state
        "Cost tracking cleared",  # costs
        "",  # export_md
        fsm_manager,  # fsm_state
        empty_df,  # snapshot_df_display
        empty_df,  # sr_df_display
        empty_df,  # tech_df_display
        "**FSM Reset** - Ready for new analysis"  # debug_display
    )


def export_markdown(chat_history: List[Dict], tracker: TokenCostTracker) -> str:
    """Export chat session to markdown with enhanced formatting"""
    lines: List[str] = [
        "# 📊 Stock Market Analysis Chat Export\n",
        f"**Export Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total Messages:** {len(chat_history)}",
        f"**Total Cost:** ${getattr(tracker, 'total_cost', getattr(tracker, 'total_costs', 0.0)):.4f}",
        f"**Total Tokens:** {getattr(tracker, 'total_tokens', 0):,}\n",
        "---\n"
    ]
    
    for i, message in enumerate(chat_history, 1):
        role = message["role"].title()
        content = message["content"]
        
        if role == "User":
            lines.append(f"## 👤 Message {i} (User)\n")
        else:
            lines.append(f"## 🤖 Message {i} (Assistant)\n")
        
        lines.append(f"{content}\n")
        lines.append("---\n")
    
    lines.extend([
        f"\n## 💰 Final Cost Summary",
        f"- **Requests:** {getattr(tracker, 'total_requests', 0)}",
        f"- **Tokens:** {getattr(tracker, 'total_tokens', 0):,}",
        f"- **Cost:** ${getattr(tracker, 'total_cost', getattr(tracker, 'total_costs', 0.0)):.4f}",
    ])
    
    return "\n".join(lines)


# -------- Enhanced Gradio Interface --------

def create_enhanced_chat_interface():
    """Create the final enhanced chat interface with all Phase 5 features"""
    
    with gr.Blocks(
        theme=gr.themes.Soft(),
        title="🏦 Enhanced Stock Market Analysis Chat",
        css="""
        .processing-status {
            background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #007acc;
            margin: 10px 0;
        }
        .error-status {
            background: linear-gradient(45deg, #fff5f5, #ffe6e6);
            border-left-color: #cc0000;
        }
        .success-status {
            background: linear-gradient(45deg, #f0fff4, #e6ffe6);
            border-left-color: #00cc00;
        }
        .button-enhanced {
            transition: all 0.3s ease;
        }
        .button-enhanced:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        """
    ) as demo:
        
        # -------- Header --------
        gr.Markdown(
            """
            # 🏦 Enhanced Stock Market Analysis Chat
            
            **Phase 5 Complete:** Advanced FSM-driven analysis with structured data parsing, 
            enhanced prompt templates, loading states, and comprehensive error handling.
            
            ### Features:
            - 🎯 **Smart Ticker Detection** - Automatically extracts ticker symbols from context
            - 📊 **Structured Data Parsing** - High-accuracy extraction with confidence scoring  
            - 🔄 **Real-time Processing Status** - Live progress updates and loading states
            - ⚠️ **Enhanced Error Handling** - User-friendly error messages and recovery
            - 🧠 **FSM State Management** - Robust workflow with comprehensive debugging
            """
        )
        
        # -------- Main Chat Interface --------
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="💬 Chat History",
                    height=400,
                    show_label=True,
                    container=True
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Ask about stocks or use the buttons below for structured analysis...",
                        label="Your Message",
                        container=False,
                        scale=4
                    )
                    send = gr.Button("Send", variant="primary", scale=1, elem_classes=["button-enhanced"])
                
                # Processing Status Display
                status_display = gr.Markdown(
                    "🟢 Ready for analysis",
                    label="Processing Status",
                    elem_classes=["processing-status"]
                )
                
                with gr.Row():
                    clear = gr.Button("Clear Chat", variant="secondary", elem_classes=["button-enhanced"])
                    ticker_input = gr.Textbox(
                        placeholder="Ticker (e.g., AAPL)", 
                        label="Stock Ticker",
                        scale=2
                    )
        
        # -------- Enhanced Stock Analysis Buttons --------
        gr.Markdown("## 📊 Structured Stock Analysis")
        gr.Markdown("Click these buttons to get structured stock data with enhanced parsing and error handling:")
        
        with gr.Row():
            snapshot_btn = gr.Button(
                "📈 Stock Snapshot", 
                variant="secondary", 
                scale=1,
                elem_classes=["button-enhanced"]
            )
            sr_btn = gr.Button(
                "🎯 Support & Resistance", 
                variant="secondary", 
                scale=1,
                elem_classes=["button-enhanced"]
            )
            tech_btn = gr.Button(
                "🔧 Technical Analysis", 
                variant="secondary", 
                scale=1,
                elem_classes=["button-enhanced"]
            )
        
        # -------- Enhanced Stock Data Display Area --------
        gr.Markdown("### 📋 Structured Data Display")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("**📈 Stock Snapshot**")
                snapshot_df_display = gr.Dataframe(
                    label="Current Stock Data",
                    interactive=False,
                    wrap=True
                )
            
            with gr.Column():
                gr.Markdown("**🎯 Support & Resistance**")
                sr_df_display = gr.Dataframe(
                    label="Key Price Levels",
                    interactive=False,
                    wrap=True
                )
            
            with gr.Column():
                gr.Markdown("**🔧 Technical Analysis**")
                tech_df_display = gr.Dataframe(
                    label="Technical Indicators",
                    interactive=False,
                    wrap=True
                )
        
        # -------- Enhanced Debug and Monitoring --------
        with gr.Accordion("🔍 System Monitoring & Debug", open=False):
            debug_display = gr.Markdown("FSM Debug info will appear here")
        
        with gr.Accordion("💰 Cost Tracking & Export", open=False):
            costs = gr.Markdown()
            export_md = gr.Textbox(label="Markdown export", lines=8)
            export_btn = gr.Button("Export Chat to Markdown", elem_classes=["button-enhanced"])
        
        # -------- State Management --------
        # Traditional state
        pyd_history_state = gr.State([])
        tracker_state = gr.State(TokenCostTracker())
        costs_state = gr.State("")
        
        # Enhanced FSM state
        fsm_state = gr.State(StateManager())
        
        # Enhanced DataFrame states
        snapshot_df_state = gr.State(pd.DataFrame())
        sr_df_state = gr.State(pd.DataFrame())
        tech_df_state = gr.State(pd.DataFrame())
        
        # -------- Event Handlers with Enhanced Features --------
        
        # Enhanced message handling with loading states
        msg.submit(
            handle_user_message,
            inputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display, status_display
            ]
        )
        
        send.click(
            handle_user_message,
            inputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display, status_display
            ]
        )
        
        # Enhanced stock analysis buttons with comprehensive error handling
        snapshot_btn.click(
            lambda ticker, *args: handle_button_click('snapshot', ticker, *args),
            inputs=[
                ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display, status_display
            ]
        )
        
        sr_btn.click(
            lambda ticker, *args: handle_button_click('support_resistance', ticker, *args),
            inputs=[
                ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display, status_display
            ]
        )
        
        tech_btn.click(
            lambda ticker, *args: handle_button_click('technical', ticker, *args),
            inputs=[
                ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display, status_display
            ]
        )
        
        # Enhanced clear with status reset
        clear.click(
            _clear_enhanced,
            inputs=[],
            outputs=[
                chatbot, pyd_history_state, tracker_state, costs, export_md,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display, status_display
            ]
        )
        
        # Enhanced export functionality
        export_btn.click(export_markdown, [chatbot, tracker_state], [export_md])
        
        # Update debug display on FSM state changes
        fsm_state.change(
            _get_debug_state_info,
            inputs=[fsm_state],
            outputs=[debug_display]
        )
    
    return demo


# -------- Application Entry Point --------

if __name__ == "__main__":
    # Initialize enhanced logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting Enhanced Stock Market Analysis Chat (Phase 5)")
    print("🎯 Features: FSM + Enhanced Parsing + Prompt Templates + Loading States + Error Handling")
    
    # Create and launch the enhanced interface
    demo = create_enhanced_chat_interface()
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        share=False
    )
