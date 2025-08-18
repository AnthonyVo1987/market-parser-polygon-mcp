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
from src.response_parser import ResponseParser, DataType
# response_validator removed - band-aid fix eliminated for JSON re-architecture
from src.prompt_templates import PromptTemplateManager, PromptType
from src.json_debug_logger import json_debug_logger, create_workflow_id

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
# response_validator initialization removed - band-aid fix eliminated

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
    snapshot_df: pd.DataFrame,
    sr_df: pd.DataFrame,
    tech_df: pd.DataFrame,
    snapshot_json: str,
    sr_json: str,
    tech_json: str,
    debug_state: str,
) -> Tuple[str, List[Dict], List, TokenCostTracker, str, StateManager, pd.DataFrame, pd.DataFrame, pd.DataFrame, str, str, str, str]:
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
            # Sanitize message history to prevent Pydantic AI crashes from None content
            clean_history = sanitize_message_history(pyd_message_history)
            response = await agent.run(user_message, message_history=clean_history)
            
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
                fsm_manager, snapshot_df, sr_df, tech_df, 
                snapshot_json, sr_json, tech_json, processing_status.status_message
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
        
        # Use modern Gradio error handling
        gr.Error(f"Failed to process message: {str(e)}")
        
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
    snapshot_json: str,
    sr_json: str,
    tech_json: str,
    debug_state: str,
) -> Tuple[str, List[Dict], List, TokenCostTracker, str, StateManager, pd.DataFrame, pd.DataFrame, pd.DataFrame, str, str, str, str]:
    """
    Enhanced button click handler with comprehensive loading states and error handling.
    """
    print(f"[GUI] Button clicked: {button_type} for {ticker}")
    
    # Create unique workflow ID for comprehensive JSON debug tracking
    workflow_id = create_workflow_id(button_type, ticker or "unknown")
    print(f"[WORKFLOW DEBUG] 🆔 Created workflow ID: {workflow_id}")
    
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
            gr.Warning("FSM state transition failed. Please try again.")
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
            gr.Error(f"Unknown analysis type: {button_type}")
            return (
                "", chat_history, pyd_message_history, tracker, cost_markdown,
                fsm_manager, snapshot_df, sr_df, tech_df, 
                snapshot_json, sr_json, tech_json, processing_status.status_message
            )
        
        # Step 3: Prepare prompt and transition FSM
        processing_status.update_step("Preparing FSM prompt...", 3)
        fsm_manager.transition('prepare_prompt')
        fsm_manager.transition('prompt_ready')
        
        # Step 4: Execute AI processing
        processing_status.update_step(f"Getting AI analysis for {fsm_manager.context.ticker}...", 4)
        await _startup()  # Ensure MCP servers are running
        
        print(f"[GUI] Sending prompt to AI: {fsm_manager.context.prompt[:100]}...")
        # Sanitize message history to prevent Pydantic AI crashes from None content
        clean_history = sanitize_message_history(pyd_message_history)
        response = await agent.run(fsm_manager.context.prompt, message_history=clean_history)
        fsm_manager.context.ai_response = response.output
        fsm_manager.transition('response_received')
        
        # Start comprehensive JSON workflow tracking
        workflow_metrics = json_debug_logger.start_json_workflow(
            workflow_id, button_type, fsm_manager.context.ticker, response.output
        )
        
        # Step 5: Parse AI response with comprehensive JSON debug logging
        processing_status.update_step("Parsing structured data...", 5)
        fsm_manager.transition('parse')
        
        # 🔍 COMPREHENSIVE JSON WORKFLOW LOGGING
        print(f"[JSON DEBUG] 🚀 Starting JSON parsing workflow for {button_type}")
        print(f"[JSON DEBUG] 🎯 Ticker: {fsm_manager.context.ticker}")
        print(f"[JSON DEBUG] 📄 AI Response size: {len(fsm_manager.context.ai_response)} characters")
        print(f"[JSON DEBUG] 📄 AI Response preview: {repr(fsm_manager.context.ai_response[:200])}...")
        
        # Analyze response for JSON indicators
        json_indicators = {
            'contains_json_block': '```json' in fsm_manager.context.ai_response.lower(),
            'contains_braces': '{' in fsm_manager.context.ai_response and '}' in fsm_manager.context.ai_response,
            'starts_with_brace': fsm_manager.context.ai_response.strip().startswith('{'),
            'brace_count': fsm_manager.context.ai_response.count('{'),
            'quote_count': fsm_manager.context.ai_response.count('"')
        }
        print(f"[JSON DEBUG] 📊 Response analysis: {json_indicators}")
        
        # Enhanced parsing with detailed feedback and JSON workflow
        data_type_map = {
            'snapshot': DataType.SNAPSHOT,
            'support_resistance': DataType.SUPPORT_RESISTANCE,
            'technical': DataType.TECHNICAL
        }
        
        data_type = data_type_map[button_type]
        print(f"[JSON DEBUG] 🔍 Parsing as data type: {data_type}")
        
        parse_start_time = time.time()
        parse_result = response_parser.parse_any(
            fsm_manager.context.ai_response, 
            data_type, 
            fsm_manager.context.ticker
        )
        parse_time = (time.time() - parse_start_time) * 1000
        
        print(f"[JSON DEBUG] ⏱️ Parsing completed in {parse_time:.1f}ms")
        print(f"[JSON DEBUG] 📊 Parse result confidence: {parse_result.confidence.value}")
        print(f"[JSON DEBUG] 📦 Extracted fields: {len(parse_result.parsed_data)}")
        print(f"[JSON DEBUG] ⚠️ Parse warnings: {len(parse_result.warnings)}")
        
        if parse_result.warnings:
            print(f"[JSON DEBUG] ⚠️ Warnings details: {parse_result.warnings}")
            
        if hasattr(parse_result, 'matched_patterns'):
            print(f"[JSON DEBUG] ✅ Matched patterns: {len(parse_result.matched_patterns)}")
            print(f"[JSON DEBUG] ❌ Failed patterns: {len(parse_result.failed_patterns)}")
        
        # Update appropriate DataFrame and JSON output with comprehensive logging
        import json
        
        df_conversion_start = time.time()
        
        if button_type == 'snapshot':
            snapshot_df = parse_result.to_dataframe()
            # Format raw AI response as JSON for display
            try:
                # Try to parse and prettify the JSON from AI response
                parsed_json = json.loads(fsm_manager.context.ai_response)
                raw_json = json.dumps(parsed_json, indent=2)
                snapshot_json = raw_json
                json_valid = True
                json_keys = list(parsed_json.keys()) if isinstance(parsed_json, dict) else []
            except (json.JSONDecodeError, TypeError):
                # If not valid JSON, display raw response
                snapshot_json = fsm_manager.context.ai_response
                json_valid = False
                json_keys = []
                
            # Log raw JSON output for debugging
            json_debug_logger.log_raw_json_output(workflow_id, button_type, snapshot_json, json_valid)
            
        elif button_type == 'support_resistance':
            sr_df = parse_result.to_dataframe()
            try:
                parsed_json = json.loads(fsm_manager.context.ai_response)
                raw_json = json.dumps(parsed_json, indent=2)
                sr_json = raw_json
                json_valid = True
                json_keys = list(parsed_json.keys()) if isinstance(parsed_json, dict) else []
            except (json.JSONDecodeError, TypeError):
                sr_json = fsm_manager.context.ai_response
                json_valid = False
                json_keys = []
                
            # Log raw JSON output for debugging
            json_debug_logger.log_raw_json_output(workflow_id, button_type, sr_json, json_valid)
            
        elif button_type == 'technical':
            tech_df = parse_result.to_dataframe()
            try:
                parsed_json = json.loads(fsm_manager.context.ai_response)
                raw_json = json.dumps(parsed_json, indent=2)
                tech_json = raw_json
                json_valid = True
                json_keys = list(parsed_json.keys()) if isinstance(parsed_json, dict) else []
            except (json.JSONDecodeError, TypeError):
                tech_json = fsm_manager.context.ai_response
                json_valid = False
                json_keys = []
                
            # Log raw JSON output for debugging
            json_debug_logger.log_raw_json_output(workflow_id, button_type, tech_json, json_valid)
        
        df_conversion_time = (time.time() - df_conversion_start) * 1000
        
        # Log DataFrame conversion metrics
        final_df = snapshot_df if button_type == 'snapshot' else sr_df if button_type == 'support_resistance' else tech_df
        json_debug_logger.log_dataframe_conversion(
            workflow_id, df_conversion_time, final_df.shape, json_valid, 
            len(locals().get('raw_json', fsm_manager.context.ai_response)), json_keys
        )
        
        fsm_manager.transition('parse_success')
        
        # Log FSM state transition with JSON context
        json_debug_logger.log_fsm_state_transition(
            workflow_id, 'parse', 'parse_success', 'parsing_complete',
            {'confidence': parse_result.confidence.value, 'field_count': len(parse_result.parsed_data), 'json_valid': json_valid}
        )
        
        # Step 6: Update UI and chat history
        processing_status.update_step("Updating display...", 6)
        fsm_manager.transition('update_complete')
        
        # Log final FSM state transition
        json_debug_logger.log_fsm_state_transition(
            workflow_id, 'parse_success', 'update_complete', 'ui_update',
            {'dataframe_shape': final_df.shape, 'ui_conversion_time_ms': df_conversion_time}
        )
        
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
        
        # Complete comprehensive JSON workflow tracking
        final_metrics = json_debug_logger.complete_workflow(
            workflow_id, parse_result.confidence.value, len(parse_result.parsed_data), True
        )
        print(f"[WORKFLOW DEBUG] 📈 Final workflow metrics: {final_metrics}")
        
        # Modern Gradio success notification
        gr.Info(f"✅ {button_type.replace('_', ' ').title()} analysis completed for {fsm_manager.context.ticker}")
        
        print(f"[GUI] Button processing completed successfully for {fsm_manager.context.ticker}")
        
        return (
            "", chat_history, pyd_message_history, tracker, cost_markdown,
            fsm_manager, snapshot_df, sr_df, tech_df, 
            snapshot_json, sr_json, tech_json, f"{processing_status.status_message}\n{debug_state}"
        )
        
    except Exception as e:
        processing_status.error(f"Button processing error: {str(e)}")
        
        # Log error in comprehensive JSON workflow if workflow was started
        if 'workflow_id' in locals():
            error_context = {
                'button_type': button_type,
                'ticker': ticker,
                'fsm_state': fsm_manager.get_current_state().name if fsm_manager else 'unknown',
                'processing_step': processing_status.current_step,
                'response_size': len(fsm_manager.context.ai_response) if fsm_manager and hasattr(fsm_manager.context, 'ai_response') else 0
            }
            json_debug_logger.log_error_condition(workflow_id, e, error_context)
        
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
        
        # CRITICAL FIX: Clear DataFrames on general error to prevent stale data display
        empty_df = pd.DataFrame()
        
        # Clear the specific DataFrame that failed, keep others intact
        if button_type == 'snapshot':
            snapshot_df = empty_df
        elif button_type == 'support_resistance':
            sr_df = empty_df
        elif button_type == 'technical':
            tech_df = empty_df
        
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
            fsm_manager, snapshot_df, sr_df, tech_df, 
            snapshot_json, sr_json, tech_json, f"{processing_status.status_message}\n{debug_state}"
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
    """Enhanced clear function with status reset and modern user feedback"""
    processing_status.reset()
    fsm_manager = StateManager()
    empty_df = pd.DataFrame()
    
    # Modern Gradio success notification
    gr.Info("Chat cleared successfully! Ready for new analysis.")
    
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
        
        # Enhanced DataFrame states
        snapshot_df_state = gr.State(pd.DataFrame())
        sr_df_state = gr.State(pd.DataFrame())
        tech_df_state = gr.State(pd.DataFrame())
        
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
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state,
                snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display,
                snapshot_json_output, sr_json_output, tech_json_output, status_display
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
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state,
                snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display,
                snapshot_json_output, sr_json_output, tech_json_output, status_display
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
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state,
                snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display,
                snapshot_json_output, sr_json_output, tech_json_output, status_display
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
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state,
                snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display,
                snapshot_json_output, sr_json_output, tech_json_output, status_display
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
                fsm_state, snapshot_df_state, sr_df_state, tech_df_state,
                snapshot_json_state, sr_json_state, tech_json_state, status_display
            ],
            outputs=[
                msg, chatbot, pyd_history_state, tracker_state, costs,
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display,
                snapshot_json_output, sr_json_output, tech_json_output, status_display
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
                fsm_state, snapshot_df_display, sr_df_display, tech_df_display,
                snapshot_json_output, sr_json_output, tech_json_output, status_display
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
    # Initialize comprehensive debug logging for JSON workflows
    logging.basicConfig(
        level=logging.DEBUG,  # Enhanced to DEBUG level for comprehensive JSON logging
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler('comprehensive_json_debug.log', mode='a')  # File output for JSON debugging
        ]
    )
    
    # Configure JSON parser logging specifically
    json_logger = logging.getLogger('json_parser')
    json_logger.setLevel(logging.DEBUG)
    
    # Configure response parser logging for comprehensive debugging
    response_logger = logging.getLogger('response_parser')
    response_logger.setLevel(logging.DEBUG)
    
    print("🚀 Starting Enhanced Stock Market Analysis Chat (Phase 5 + Comprehensive JSON Debug)")
    print("🎯 Features: FSM + Enhanced Parsing + Prompt Templates + Loading States + Error Handling")
    print("🔍 Enhanced Features: Comprehensive JSON Debug Logging + Raw JSON Output + Performance Metrics")
    print(f"[LOGGING] 📄 Debug logs written to: comprehensive_json_debug.log + json_workflow_debug.log")
    print(f"[LOGGING] 📊 Log level: DEBUG (comprehensive JSON tracing enabled)")
    
    # Create and launch the enhanced interface
    demo = create_enhanced_chat_interface()
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        share=False
    )