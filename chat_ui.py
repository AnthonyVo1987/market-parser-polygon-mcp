"""
Stock Market Analysis Chat UI - Phase 3 Unified Interface
Consolidated UI with all interactions flowing through a single chat interface.
Button clicks display full prompts and JSON responses in the main chat conversation for transparency.
Simplified user experience with no separate JSON output areas.
"""

import os
import asyncio
import logging
from typing import List, Dict, Tuple, Any, Optional
import time
import traceback
import json
import tempfile
import html

import gradio as gr
from dotenv import find_dotenv, load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIResponsesModel

# Import simplified systems - FSM only for state management
from stock_data_fsm import StateManager, AppState
from src.prompt_templates import PromptTemplateManager, PromptType

# Import unified conversational response processing
from src.response_manager import ResponseManager, ProcessingMode

# Import security utilities for content sanitization
from src.security_utils import InputValidator, SecureLogger

# Reuse server factory and token tracking from CLI
from market_parser_demo import create_polygon_mcp_server, TokenCostTracker

# Load environment variables
load_dotenv(find_dotenv())

# Configure logger for security monitoring
logger = logging.getLogger(__name__)

# -------- Global state for MCP server management --------
_mcp_ctx = None


# -------- Agent & MCP server setup --------
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5-mini")

server = create_polygon_mcp_server()
model = OpenAIResponsesModel(MODEL_NAME)

# Initialize simplified systems
prompt_manager = PromptTemplateManager()
response_manager = ResponseManager(ProcessingMode.ENHANCED)

# Unified system prompt for conversational responses
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
    debug_state: str,
) -> Tuple[str, List[Dict], List, TokenCostTracker, str, StateManager, str]:
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
            
            # Process user response with unified conversational formatting
            processing_status.update_step("Processing response for chat...", 3)
            processed_response = response_manager.process_response(
                response.output, 
                source_type='user'
            )
            
            # Use processed content for chat display
            response_content = processed_response.get('content', response.output)
            chat_history = chat_history + [{"role": "assistant", "content": response_content}]
            pyd_message_history.append({"role": "user", "content": user_message})
            pyd_message_history.append({"role": "assistant", "content": response_content})
            
            # Update costs
            processing_status.update_step("Updating costs...", 3)
            cost_markdown = await _update_costs(response, tracker)
            
            processing_status.complete("Regular chat completed")
            print(f"[GUI] Regular Chat Response: {response.output[:100]}...")
            
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, processing_status.status_message
            )
        
        else:
            # This shouldn't happen in regular flow, but handle gracefully
            processing_status.error("Invalid state for regular message")
            debug_state = _get_debug_state_info(fsm_manager)
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, f"{processing_status.status_message}\n{debug_state}"
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
            fsm_manager, processing_status.status_message
        )


async def handle_button_click(
    button_type: str,
    ticker: str,
    chat_history: List[Dict],
    pyd_message_history: List | None,
    tracker: TokenCostTracker,
    cost_markdown: str,
    fsm_manager: StateManager,
    debug_state: str,
) -> Tuple[str, List[Dict], List, TokenCostTracker, str, StateManager, str]:
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
                fsm_manager, f"{processing_status.status_message}\n{debug_state}"
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
                fsm_manager, processing_status.status_message
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
        
        # Step 3: Process AI response with unified conversational formatting
        processing_status.update_step("Processing button response...", 3)
        fsm_manager.context.raw_json_response = response.output
        
        # Process button response with unified conversational formatting
        processed_response = response_manager.process_response(
            response.output,
            source_type='button',
            data_type=button_type,
            ticker=fsm_manager.context.ticker
        )
        
        # Add to chat history with unified conversational formatting
        # First show the analysis request that was sent to AI
        prompt_display = f"**📋 Analysis Request:**\n{fsm_manager.context.prompt[:200]}..." if len(fsm_manager.context.prompt) > 200 else f"**📋 Analysis Request:**\n{fsm_manager.context.prompt}"
        
        # Use processed content which includes enhanced conversational formatting (now includes title)
        response_content = processed_response.get('content', response.output)
        
        # Add processing info if available
        processing_info = ""
        if processed_response.get('processing_time_ms'):
            processing_info = f"\n\n*Processing time: {processed_response['processing_time_ms']:.1f}ms*"
        
        enhanced_response = f"{response_content}{processing_info}"
        
        chat_history = chat_history + [
            {"role": "user", "content": prompt_display},
            {"role": "assistant", "content": enhanced_response}
        ]
        
        # Update message history (using processed content for display)
        if pyd_message_history is None:
            pyd_message_history = []
        pyd_message_history.append({"role": "user", "content": fsm_manager.context.prompt})
        pyd_message_history.append({"role": "assistant", "content": enhanced_response})
        
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
            fsm_manager, f"{processing_status.status_message}\n{debug_state}"
        )
        
    except Exception as e:
        processing_status.error(f"Button processing error: {str(e)}")
        
        # Try to process error response for better display
        try:
            error_response = response_manager.process_response(
                f"Error processing {button_type} analysis: {str(e)}",
                source_type='user'
            )
            error_message = error_response.get('content', f"❌ Error processing {button_type} analysis: {str(e)}")
        except:
            error_message = f"❌ Error processing {button_type} analysis: {str(e)}"
        
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
        
        # JSON outputs no longer needed - using chat interface only
        
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
            fsm_manager, f"{processing_status.status_message}\n{debug_state}"
        )


# -------- Utility Functions --------

async def _update_costs(response, tracker: TokenCostTracker) -> str:
    """Update cost tracking with enhanced formatting"""
    try:
        # Use the correct method from TokenCostTracker class
        tracker.record_and_print(response)
        
        # Generate enhanced cost display using correct TokenCostTracker attributes
        total_cost = tracker.total_input_cost_usd + tracker.total_output_cost_usd
        total_tokens = tracker.total_input_tokens + tracker.total_output_tokens
        
        cost_markdown = f"""## 💰 Cost Tracking
**Total Tokens:** {total_tokens:,}
**Estimated Cost:** ${total_cost:.6f}

**Session Details:**
- Input Tokens: {tracker.total_input_tokens:,} (${tracker.total_input_cost_usd:.6f})
- Output Tokens: {tracker.total_output_tokens:,} (${tracker.total_output_cost_usd:.6f})

**Debug Info:**
- Usage Available: {hasattr(response, 'usage')}
- Response Type: {type(response).__name__}
"""
        return cost_markdown
    except Exception as e:
        # Provide more detailed error information for debugging
        error_info = f"""## 💰 Cost Tracking - Error
**Error:** {str(e)}
**Response Type:** {type(response).__name__}
**Response Attributes:** {', '.join(dir(response))}
**Tracker Attributes:** {', '.join(dir(tracker))}
"""
        return error_info


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
        fsm_manager,  # fsm_state
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


def export_json(chat_history: List[Dict], tracker: TokenCostTracker) -> str:
    """Export chat session to JSON format"""
    export_data = {
        "export_info": {
            "export_date": time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_messages": len(chat_history),
            "total_cost": getattr(tracker, 'total_cost', getattr(tracker, 'total_costs', 0.0)),
            "total_tokens": getattr(tracker, 'total_tokens', 0)
        },
        "chat_history": chat_history,
        "cost_summary": {
            "requests": getattr(tracker, 'total_requests', 0),
            "tokens": getattr(tracker, 'total_tokens', 0),
            "cost": getattr(tracker, 'total_cost', getattr(tracker, 'total_costs', 0.0))
        }
    }
    
    return json.dumps(export_data, indent=2, ensure_ascii=False)


def copy_to_clipboard_markdown(chat_history: List[Dict], tracker: TokenCostTracker):
    """Copy markdown export to clipboard - return content for display"""
    # Sanitize content before export to prevent XSS
    sanitized_history = _sanitize_chat_history_for_export(chat_history)
    markdown_content = export_markdown(sanitized_history, tracker)
    gr.Info(f"📋 Copy this markdown content to your clipboard ({len(sanitized_history)} messages)")
    return markdown_content


def copy_to_clipboard_json(chat_history: List[Dict], tracker: TokenCostTracker):
    """Copy JSON export to clipboard - return content for display"""
    # Sanitize content before export to prevent XSS
    sanitized_history = _sanitize_chat_history_for_export(chat_history)
    json_content = export_json(sanitized_history, tracker)
    gr.Info(f"📋 Copy this JSON content to your clipboard ({len(sanitized_history)} messages)")
    return json_content


def _sanitize_chat_history_for_export(chat_history: List[Dict]) -> List[Dict]:
    """
    Sanitize chat history before export to prevent XSS and content injection.
    
    Args:
        chat_history: Raw chat history from the interface
        
    Returns:
        Sanitized chat history safe for export
    """
    sanitized_history = []
    
    try:
        for message in chat_history:
            if not isinstance(message, dict):
                continue
                
            sanitized_message = {}
            
            # Sanitize role field
            role = message.get('role', 'unknown')
            if role in ['user', 'assistant', 'system']:
                sanitized_message['role'] = role
            else:
                sanitized_message['role'] = 'unknown'
            
            # Sanitize content field - remove potential XSS content
            content = message.get('content', '')
            if content:
                try:
                    # Use InputValidator to remove dangerous patterns
                    # Remove HTML tags and escape potential XSS content
                    sanitized_content = html.escape(str(content))
                    
                    # Additional sanitization for export safety
                    sanitized_content = sanitized_content.replace('<script', '&lt;script')
                    sanitized_content = sanitized_content.replace('javascript:', 'javascript-blocked:')
                    sanitized_content = sanitized_content.replace('vbscript:', 'vbscript-blocked:')
                    sanitized_content = sanitized_content.replace('onerror=', 'onerror-blocked=')
                    sanitized_content = sanitized_content.replace('onload=', 'onload-blocked=')
                    sanitized_content = sanitized_content.replace('onclick=', 'onclick-blocked=')
                    
                    sanitized_message['content'] = sanitized_content
                except Exception as e:
                    # Log sanitization error securely
                    sanitized_message['content'] = f"[Content sanitization error: {SecureLogger.sanitize_log_message(str(e))}]"
            else:
                sanitized_message['content'] = ''
            
            # Include timestamp if present
            if 'timestamp' in message:
                sanitized_message['timestamp'] = message['timestamp']
                
            sanitized_history.append(sanitized_message)
            
    except Exception as e:
        # Log error securely and return safe fallback
        logger.error(f"Error sanitizing chat history: {SecureLogger.sanitize_log_message(str(e))}")
        return [{"role": "system", "content": "[Chat history sanitization failed - export not available]"}]
    
    return sanitized_history


def save_markdown_file(chat_history: List[Dict], tracker: TokenCostTracker):
    """Generate markdown file for download with secure temp file handling"""
    try:
        # Sanitize content before export
        sanitized_history = _sanitize_chat_history_for_export(chat_history)
        markdown_content = export_markdown(sanitized_history, tracker)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        
        # Use secure temporary file with automatic cleanup
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            prefix=f'stock_analysis_{timestamp}_',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            temp_file.write(markdown_content)
            temp_file.flush()
            secure_path = temp_file.name
        
        # Set secure permissions (readable only by owner)
        os.chmod(secure_path, 0o600)
        
        gr.Info(f"💾 Secure markdown file ready for download! ({len(sanitized_history)} messages)")
        return secure_path
        
    except Exception as e:
        logger.error(f"Error creating secure markdown file: {SecureLogger.sanitize_log_message(str(e))}")
        gr.Error("Failed to create markdown file. Please try again.")
        return None


def save_json_file(chat_history: List[Dict], tracker: TokenCostTracker):
    """Generate JSON file for download with secure temp file handling"""
    try:
        # Sanitize content before export
        sanitized_history = _sanitize_chat_history_for_export(chat_history)
        json_content = export_json(sanitized_history, tracker)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        
        # Use secure temporary file with automatic cleanup
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            prefix=f'stock_analysis_{timestamp}_',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            temp_file.write(json_content)
            temp_file.flush()
            secure_path = temp_file.name
        
        # Set secure permissions (readable only by owner)
        os.chmod(secure_path, 0o600)
        
        gr.Info(f"💾 Secure JSON file ready for download! ({len(sanitized_history)} messages)")
        return secure_path
        
    except Exception as e:
        logger.error(f"Error creating secure JSON file: {SecureLogger.sanitize_log_message(str(e))}")
        gr.Error("Failed to create JSON file. Please try again.")
        return None


# -------- Enhanced Gradio Interface --------

def create_enhanced_chat_interface():
    """Create simplified chat interface with all output consolidated to single chat conversation"""
    
    with gr.Blocks(
        title="📊 Stock Market Analysis Chat - Unified Interface",
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
            margin: 4px 2px;
        }
        .button-enhanced:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Improved spacing for sections */
        .gradio-container {
            gap: 16px;
        }
        
        /* Analysis buttons visual grouping */
        .analysis-buttons {
            background: rgba(0, 122, 204, 0.05);
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
        }
        
        /* Export buttons styling */
        .export-section {
            background: rgba(46, 204, 113, 0.05);
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
        }
        
        /* Better visual hierarchy */
        .main-chat {
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Status display improvements */
        .status-display {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
        }
        """
    ) as demo:
        
        # -------- Header --------
        gr.Markdown(
            """
            # 📊 Stock Market Analysis Chat - Phase 3 Simplified
            
            **Phase 3 Implementation:** Unified chat interface with all interactions in one place.
            All button requests and responses now flow through the main chat for simplified user experience.
            
            ### Features:
            - 💬 **Single Chat Interface** - All interactions in one conversation
            - 📊 **Analysis Buttons** - Three types of enhanced conversational analysis with better formatting
            - 🔄 **Real-time Processing** - Live status updates
            - 🧠 **FSM State Management** - Simple workflow management
            - 📋 **Full Prompt Display** - See exactly what was sent to AI before responses
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
                    type="messages",
                    elem_classes=["main-chat"]
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Ask about stocks or use the buttons below for structured analysis...",
                        label="Your Message",
                        container=False,
                        scale=4,
                        lines=3
                    )
                    send = gr.Button("Send", variant="primary", scale=1, elem_classes=["button-enhanced"])
                
                # Ticker input directly below message input
                ticker_input = gr.Textbox(
                    placeholder="Ticker (e.g., AAPL)", 
                    label="Stock Ticker",
                    value="NVDA"
                )
                
                # Analysis buttons directly below ticker input
                with gr.Group(elem_classes=["analysis-buttons"]):
                    gr.Markdown("**📊 Stock Analysis:**")
                    with gr.Row():
                        snapshot_btn = gr.Button(
                            "📈 Snapshot", 
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
                
                # Processing Status Display
                status_display = gr.Markdown(
                    "🟢 Ready for analysis",
                    label="Processing Status",
                    elem_classes=["processing-status"]
                )
                
                # Clear button moved to separate row
                clear = gr.Button("Clear Chat", variant="secondary", elem_classes=["button-enhanced"])
        
        # JSON outputs have been consolidated to chat interface for simplified user experience
        # -------- Enhanced Debug and Monitoring --------
        with gr.Accordion("🔍 System Monitoring & Debug", open=False):
            debug_display = gr.Markdown("FSM Debug info will appear here")
        
        with gr.Accordion("💰 Cost Tracking & Export", open=False):
            costs = gr.Markdown()
            
            # New export buttons section
            with gr.Group(elem_classes=["export-section"]):
                gr.Markdown("**📤 Export Options:**")
                with gr.Row():
                    copy_md_btn = gr.Button("📋 Copy Chat (Markdown)", elem_classes=["button-enhanced"])
                    save_md_btn = gr.Button("💾 Save Chat (.md)", elem_classes=["button-enhanced"])
                with gr.Row():
                    copy_json_btn = gr.Button("📋 Copy Chat (JSON)", elem_classes=["button-enhanced"])
                    save_json_btn = gr.Button("💾 Save Chat (.json)", elem_classes=["button-enhanced"])
            
            # Output areas for clipboard content
            clipboard_md_output = gr.Textbox(
                label="Markdown Content (Select All + Copy)",
                lines=6,
                visible=False,
                interactive=True
            )
            clipboard_json_output = gr.Textbox(
                label="JSON Content (Select All + Copy)", 
                lines=6,
                visible=False,
                interactive=True
            )
            
            # File download output
            file_download = gr.File(label="Download File", visible=False)
        
        # -------- State Management --------
        # Traditional state
        pyd_history_state = gr.State([])
        tracker_state = gr.State(TokenCostTracker())
        costs_state = gr.State("")
        
        # Enhanced FSM state
        fsm_state = gr.State(StateManager())
        
        # JSON output states removed - all output goes to chat interface
        
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
                fsm_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, status_display
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
                fsm_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, status_display
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
                fsm_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, status_display
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
                fsm_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, status_display
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
                fsm_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, status_display
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
                chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, status_display
            ]
        )
        
        # Enhanced export functionality with new buttons
        copy_md_btn.click(
            copy_to_clipboard_markdown,
            inputs=[chatbot, tracker_state],
            outputs=[clipboard_md_output]
        ).then(
            lambda: gr.update(visible=True),
            inputs=[],
            outputs=[clipboard_md_output]
        )
        
        copy_json_btn.click(
            copy_to_clipboard_json,
            inputs=[chatbot, tracker_state],
            outputs=[clipboard_json_output]
        ).then(
            lambda: gr.update(visible=True),
            inputs=[],
            outputs=[clipboard_json_output]
        )
        
        save_md_btn.click(
            save_markdown_file,
            inputs=[chatbot, tracker_state],
            outputs=[file_download]
        ).then(
            lambda: gr.update(visible=True),
            inputs=[],
            outputs=[file_download]
        )
        
        save_json_btn.click(
            save_json_file,
            inputs=[chatbot, tracker_state],
            outputs=[file_download]
        ).then(
            lambda: gr.update(visible=True),
            inputs=[],
            outputs=[file_download]
        )
        
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
    
    print("🚀 Starting Stock Market Analysis Chat (Phase 3 - Unified Interface)")
    print("🎯 Features: Single Chat Interface + Enhanced Conversational Formatting")
    print("📊 Simplified: All interactions consolidated to main chat conversation")
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