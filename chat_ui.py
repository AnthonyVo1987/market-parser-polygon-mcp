"""
Simplified Stock Market Analysis Chat UI - Phase 2 Implementation
Simplified version with FSM integration and raw JSON outputs only.
Removed all structured data displays and complex parsing for UI simplification.
"""

import os
import asyncio
import logging
from typing import List, Dict, Tuple, Any, Optional
import time
import traceback
import json

import gradio as gr
from dotenv import find_dotenv, load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel

# Import simplified systems - FSM only for state management
from stock_data_fsm import StateManager, AppState
from src.prompt_templates import PromptTemplateManager, PromptType

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

# Initialize simplified systems
prompt_manager = PromptTemplateManager()

# Simplified system prompt for raw JSON output
base_system_prompt = (
    "You are an expert financial analyst. Note that when using Polygon tools, prices are already stock split adjusted. "
    "Use the latest data available. Always double check your math. "
    "For any questions about the current date, use the 'get_today_date' tool. "
    "For long or complex queries, break the query into logical subtasks and process each subtask in order."
)

# Use base system prompt without enhancement for simplicity
system_prompt = base_system_prompt

agent = Agent(
    model=model,
    mcp_servers=[server],
    system_prompt=system_prompt,
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

def sanitize_message_history(history):
    """Remove invalid messages from history before sending to AI to prevent Pydantic AI crashes"""
    if not history:
        return []
    
    sanitized = []
    for msg in history:
        # Handle dict format messages
        if isinstance(msg, dict):
            if msg.get('content') is not None and msg.get('content') != "":
                sanitized.append(msg)
        # Handle tuple/list format messages
        elif isinstance(msg, (list, tuple)) and len(msg) >= 2:
            if msg[1] is not None and msg[1] != "":
                # Convert to standard dict format
                sanitized.append({'role': msg[0] if len(msg) > 0 else 'user', 'content': msg[1]})
    
    return sanitized


async def handle_user_message(
    user_message: str,
    chat_history: List[Dict],
    pyd_message_history: List | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
    fsm_manager: StateManager,
    snapshot_json: str,
    sr_json: str,
    tech_json: str,
    debug_state: str,
) -> Tuple[str, List[Dict], List, TokenCostTracker, str, StateManager, str, str, str, str]:
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
            print(f"[DEBUG] Regular chat using empty history (pyd_message_history for UI only)")
            # CRITICAL FIX: Regular chat MUST use empty history - pyd_message_history causes crashes
            # pyd_message_history is ONLY for UI display, NEVER for agent.run()
            response = await agent.run(user_message, message_history=[])
            
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
                fsm_manager, snapshot_json, sr_json, tech_json, processing_status.status_message
            )
        
        else:
            # This shouldn't happen in regular flow, but handle gracefully
            processing_status.error("Invalid state for regular message")
            debug_state = _get_debug_state_info(fsm_manager)
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_json, sr_json, tech_json, f"{processing_status.status_message}\n{debug_state}"
            )
            
    except Exception as e:
        processing_status.error(f"Chat error: {str(e)}")
        error_message = f"❌ Error processing message: {str(e)}"
        print(f"[GUI] Error in regular chat: {e}")
        traceback.print_exc()
        
        # Use modern Gradio error handling
        gr.Error(f"Failed to process message: {str(e)}")
        
        # Add error message to chat
        chat_history = chat_history + [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": error_message}
        ]
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_json, sr_json, tech_json, processing_status.status_message
        )


async def handle_button_click(
    button_type: str,
    ticker: str,
    chat_history: List[Dict],
    pyd_message_history: List | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
    fsm_manager: StateManager,
    snapshot_json: str,
    sr_json: str,
    tech_json: str,
    debug_state: str,
) -> Tuple[str, List[Dict], List, TokenCostTracker, str, StateManager, str, str, str, str]:
    """
    Enhanced button click handler with comprehensive loading states and error handling.
    """
    print(f"[GUI] Button clicked: {button_type} for {ticker}")
    
    # Start processing with simplified steps
    processing_status.start_processing(f"Processing {button_type} analysis", total_steps=4)
    
    try:
        # Step 1: Initialize FSM transition
        processing_status.update_step("Initializing FSM transition...", 1)
        success = fsm_manager.transition('button_click', 
                                       button_type=button_type, 
                                       ticker=ticker or 'the last mentioned stock')
        
        if not success:
            processing_status.error("FSM transition failed")
            debug_state = _get_debug_state_info(fsm_manager)
            gr.Warning("FSM state transition failed. Please try again.")
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_json, sr_json, tech_json, f"{processing_status.status_message}\n{debug_state}"
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
            gr.Error(f"Unknown analysis type: {button_type}")
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_json, sr_json, tech_json, processing_status.status_message
            )
        
        # Step 3: Prepare prompt and transition FSM to AI processing
        processing_status.update_step("Starting AI processing...", 3)
        fsm_manager.transition('start_ai_processing')
        
        # Step 4: Execute AI processing
        processing_status.update_step(f"Getting AI analysis for {fsm_manager.context.ticker}...", 4)
        await _startup()  # Ensure MCP servers are running
        
        # Enhanced debug logging for message history contamination tracking
        print(f"[DEBUG] Button: {button_type}, Ticker: {ticker}")
        print(f"[DEBUG] Current prompt: {fsm_manager.context.prompt[:50]}...")
        print(f"[DEBUG] UI message history length (for display only): {len(pyd_message_history) if pyd_message_history else 0}")
        print(f"[DEBUG] Agent message history: [] (empty for ALL actions)")
        if pyd_message_history:
            print(f"[DEBUG] Message history preview: {str(pyd_message_history)[:100]}...")
        
        print(f"[GUI] Sending prompt to AI: {fsm_manager.context.prompt[:100]}...")
        
        # CRITICAL FIX: Use empty message history for button actions to prevent contamination
        # Button actions are INDEPENDENT analyses, not conversational continuations
        # Each button should start fresh with the AI agent to avoid prompt contamination
        response = await agent.run(fsm_manager.context.prompt, message_history=[])
        fsm_manager.context.ai_response = response.output
        fsm_manager.transition('response_received')
        
        # Success confirmation logging
        print(f"[DEBUG] ✅ {button_type} completed successfully - no message history contamination")
        
        # Step 3: Process AI response and extract JSON
        processing_status.update_step("Processing response...", 3)
        fsm_manager.context.raw_json_response = response.output
        
        # CRITICAL FIX: ACTUALLY preserve input values - Python doesn't do this automatically!
        # Variables assigned inside if blocks create LOCAL variables that SHADOW parameters
        # Must explicitly preserve input values BEFORE any if statements
        
        # Initialize with input values to preserve them
        new_snapshot_json = snapshot_json  # Preserve input
        new_sr_json = sr_json             # Preserve input  
        new_tech_json = tech_json         # Preserve input
        
        # Then only update the relevant one
        if button_type == 'snapshot':
            try:
                parsed_json = json.loads(response.output)
                new_snapshot_json = json.dumps(parsed_json, indent=2)
            except (json.JSONDecodeError, TypeError):
                new_snapshot_json = response.output
        elif button_type == 'support_resistance':
            try:
                parsed_json = json.loads(response.output)
                new_sr_json = json.dumps(parsed_json, indent=2)  
            except (json.JSONDecodeError, TypeError):
                new_sr_json = response.output
        elif button_type == 'technical':
            try:
                parsed_json = json.loads(response.output)
                new_tech_json = json.dumps(parsed_json, indent=2)
            except (json.JSONDecodeError, TypeError):
                new_tech_json = response.output
        
        # Finally assign back to original variables
        snapshot_json = new_snapshot_json
        sr_json = new_sr_json  
        tech_json = new_tech_json
        
        # JSON Data Status Debug - Show which JSON outputs have data
        print(f"[DEBUG] JSON Data Status - Snapshot: {'✓' if snapshot_json else '✗'}, S&R: {'✓' if sr_json else '✗'}, Technical: {'✓' if tech_json else '✗'}")
        
        # Add to chat history with simple formatting
        enhanced_response = f"📊 **{button_type.replace('_', ' ').title()} Analysis for {fsm_manager.context.ticker}**\n\n{response.output}"
        
        chat_history = chat_history + [
            {"role": "user", "content": f"📊 {button_type.replace('_', ' ').title()} for {fsm_manager.context.ticker}"},
            {"role": "assistant", "content": enhanced_response}
        ]
        
        # Update message history
        if pyd_message_history is None:
            pyd_message_history = []
        pyd_message_history.append({"role": "user", "content": fsm_manager.context.prompt})
        pyd_message_history.append({"role": "assistant", "content": response.output})
        
        # Step 4: Update costs and finalize
        processing_status.update_step("Finalizing...", 4)
        cost_markdown = await _update_costs(response, tracker)
        
        # Complete display and return FSM to IDLE for next interaction
        fsm_manager.transition('display_complete')  # Proper RESPONSE_RECEIVED -> IDLE transition
        
        # Clear button type to allow regular chat after button completion
        fsm_manager.context.button_type = None  # Clear for regular chat
        
        # Simple debug info
        debug_state = _get_debug_state_info(fsm_manager)
        
        processing_status.complete(f"✅ {button_type.replace('_', ' ').title()} analysis complete")
        
        # Modern Gradio success notification
        gr.Info(f"✅ {button_type.replace('_', ' ').title()} analysis completed for {fsm_manager.context.ticker}")
        
        print(f"[GUI] Button processing completed successfully for {fsm_manager.context.ticker}")
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_json, sr_json, tech_json, f"{processing_status.status_message}\n{debug_state}"
        )
        
    except Exception as e:
        processing_status.error(f"Button processing error: {str(e)}")
        
        # Log error for debugging
        print(f"[GUI] Error in button processing: {e}")
        traceback.print_exc()
        
        # Enhanced error categorization for better user experience
        error_str = str(e).lower()
        if 'connection' in error_str or 'timeout' in error_str:
            gr.Warning("Connection timeout. Please check your internet connection and try again.")
        elif 'authentication' in error_str or 'unauthorized' in error_str:
            gr.Error("Authentication failed. Please check your API keys.")
        elif 'rate limit' in error_str or 'quota' in error_str:
            gr.Warning("Rate limit exceeded. Please wait a moment and try again.")
        else:
            gr.Error(f"Failed to process {button_type.replace('_', ' ').title()} analysis: {str(e)}")
        
        # Clear JSON outputs on error
        if button_type == 'snapshot':
            snapshot_json = ""
        elif button_type == 'support_resistance':
            sr_json = ""
        elif button_type == 'technical':
            tech_json = ""
        
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
            fsm_manager, snapshot_json, sr_json, tech_json, f"{processing_status.status_message}\n{debug_state}"
        )


# -------- Utility Functions --------

async def _update_costs(response, tracker: TokenCostTracker) -> str:
    """Update cost tracking with enhanced formatting"""
    try:
        if hasattr(response, "usage") and hasattr(tracker, "add_response"):
            await tracker.add_response(response)
        elif hasattr(response, "usage") and hasattr(tracker, "track_response"):
            # Alternative method name
            await tracker.track_response(response)
        
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
    
    # Ticker is already included above, no need to duplicate
    
    # Add recent transitions
    if fsm_manager.context.transition_history:
        recent_transitions = fsm_manager.context.transition_history[-3:]
        state_info.append("**Recent Transitions:**")
        for trans in recent_transitions:
            if hasattr(trans, 'from_state') and hasattr(trans, 'to_state'):
                state_info.append(f"  • {trans.from_state} → {trans.to_state} ({trans.event})")
    
    return "\n".join(state_info)


def _clear_enhanced():
    """Enhanced clear function with status reset and modern user feedback"""
    processing_status.reset()
    fsm_manager = StateManager()
    
    # Modern Gradio success notification
    gr.Info("Chat cleared successfully! Ready for new analysis.")
    
    return (
        [],  # chatbot
        [],  # pyd_history_state
        TokenCostTracker(),  # tracker_state
        "Cost tracking cleared",  # costs
        "",  # export_md
        fsm_manager,  # fsm_state
        "",  # snapshot_json_output
        "",  # sr_json_output
        "",  # tech_json_output
        "**FSM Reset** - Ready for new analysis"  # debug_display
    )


def export_markdown(chat_history: List[Dict], tracker: TokenCostTracker) -> str:
    """Export chat session to markdown with enhanced formatting and user feedback"""
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
    
    # Modern Gradio success notification
    gr.Info(f"Chat exported successfully! {len(chat_history)} messages exported.")
    
    return "\n".join(lines)


# -------- Enhanced Gradio Interface --------

def create_enhanced_chat_interface():
    """Create simplified chat interface with JSON outputs only"""
    
    with gr.Blocks(
        title="📊 Simplified Stock Market Analysis Chat",
        css="""
        .processing-status {
            background: linear-gradient(45deg, #f0f8ff, #e6f3ff);
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #007acc;
            margin: 10px 0;
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
            # 📊 Simplified Stock Market Analysis Chat
            
            **Phase 2 Implementation:** Simplified FSM-driven analysis with raw JSON outputs only.
            Removed structured data displays for streamlined functionality.
            
            ### Features:
            - 💬 **Chat Interface** - Natural language stock market queries
            - 📊 **Analysis Buttons** - Three types of structured analysis
            - 📄 **Raw JSON Output** - Pure JSON responses without parsing
            - 🔄 **Real-time Processing** - Live status updates
            - 🧠 **FSM State Management** - Simple workflow management
            """
        )
        
        # -------- Main Chat Interface --------
        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    label="💬 Chat History",
                    height=400,
                    show_label=True,
                    container=True,
                    type="messages"
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
                        value="NVDA",
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
        
        # -------- JSON Output Display Area --------
        gr.Markdown("### 🔧 Raw JSON Outputs")
        gr.Markdown("View the raw JSON responses from each analysis button:")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("**📈 Snapshot JSON**")
                snapshot_json_output = gr.Code(
                    label="Stock Snapshot Raw JSON",
                    language="json",
                    interactive=False,
                    lines=10,
                    value=""
                )
            
            with gr.Column():
                gr.Markdown("**🎯 Support & Resistance JSON**")
                sr_json_output = gr.Code(
                    label="Support & Resistance Raw JSON", 
                    language="json",
                    interactive=False,
                    lines=10,
                    value=""
                )
            
            with gr.Column():
                gr.Markdown("**🔧 Technical Analysis JSON**")
                tech_json_output = gr.Code(
                    label="Technical Analysis Raw JSON",
                    language="json", 
                    interactive=False,
                    lines=10,
                    value=""
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
        
        # JSON output states
        snapshot_json_state = gr.State("")
        sr_json_state = gr.State("")
        tech_json_state = gr.State("")
        
        # -------- Event Handlers with Enhanced Features --------
        
        # Modern async handlers with direct function references
        from functools import partial
        
        # Use partial application instead of lambda wrappers for better performance
        handle_snapshot_click = partial(handle_button_click, 'snapshot')
        handle_sr_click = partial(handle_button_click, 'support_resistance') 
        handle_tech_click = partial(handle_button_click, 'technical')
        
        # Enhanced message handling with modern event chaining
        msg_event = msg.submit(
            handle_user_message,
            inputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_json_output, sr_json_output, tech_json_output, status_display
            ]
        )
        
        # Modern event chaining pattern: chain input focus after message sent
        msg_event.then(
            lambda: gr.update(value=""),
            inputs=[],
            outputs=[msg]
        )
        
        send_event = send.click(
            handle_user_message,
            inputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_json_output, sr_json_output, tech_json_output, status_display
            ]
        )
        
        # Chain input clearing for send button as well
        send_event.then(
            lambda: gr.update(value=""),
            inputs=[],
            outputs=[msg]
        )
        
        # Enhanced stock analysis buttons with comprehensive error handling and state management
        snapshot_event = snapshot_btn.click(
            handle_snapshot_click,
            inputs=[
                ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_json_output, sr_json_output, tech_json_output, status_display
            ]
        )
        
        # Modern UX: Chain button state management to prevent double-clicks
        snapshot_event.then(
            lambda: [gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)],
            inputs=[],
            outputs=[snapshot_btn, sr_btn, tech_btn]
        )
        
        sr_event = sr_btn.click(
            handle_sr_click,
            inputs=[
                ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_json_output, sr_json_output, tech_json_output, status_display
            ]
        )
        
        # Modern UX: Chain button state management for Support & Resistance
        sr_event.then(
            lambda: [gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)],
            inputs=[],
            outputs=[snapshot_btn, sr_btn, tech_btn]
        )
        
        tech_event = tech_btn.click(
            handle_tech_click,
            inputs=[
                ticker_input, chatbot, pyd_history_state, tracker_state, costs_state,
                fsm_state, snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_json_output, sr_json_output, tech_json_output, status_display
            ]
        )
        
        # Modern UX: Chain button state management for Technical Analysis
        tech_event.then(
            lambda: [gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)],
            inputs=[],
            outputs=[snapshot_btn, sr_btn, tech_btn]
        )
        
        # Enhanced clear with status reset
        clear.click(
            _clear_enhanced,
            inputs=[],
            outputs=[
                chatbot, pyd_history_state, tracker_state, costs, export_md,
                fsm_state, snapshot_json_output, sr_json_output, tech_json_output, status_display
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
    # Initialize basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]  # Console output only
    )
    
    print("🚀 Starting Simplified Stock Market Analysis Chat (Phase 2)")
    print("🎯 Features: FSM + Raw JSON Output + Simple Error Handling")
    print("📊 Simplified: Removed structured data displays and complex parsing")
    print(f"[LOGGING] 📄 Basic logging enabled")
    
    # Create and launch the enhanced interface
    demo = create_enhanced_chat_interface()
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        share=False
    )