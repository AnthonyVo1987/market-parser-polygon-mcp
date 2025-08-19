"""
State Manager - Main FSM controller with transition logic

This module contains:
- StateManager: Primary FSM controller class
- Action implementations for state transitions
- Error recovery mechanisms
- Comprehensive logging support
"""

import logging
import time
import uuid
from typing import Dict, Callable, Any, Optional, List
from .states import AppState, StateContext, TransitionRecord
from .transitions import StateTransitions


class StateActions:
    """
    Action functions executed during state transitions.
    
    Actions are functions that perform side effects during transitions,
    such as data manipulation, logging, or preparation for next states.
    """
    
    def __init__(self, logger: logging.Logger):
        """Initialize with logger instance"""
        self.logger = logger
    
    # === Button Click Actions ===
    
    def on_button_clicked(self, context: StateContext, **kwargs) -> None:
        """Action when user clicks a data request button"""
        button_type = kwargs.get('button_type', context.button_type)
        context.button_type = button_type
        context.reset_error_attempts()
        
        self.logger.info(f"Button clicked: {button_type}")
        
        # Set ticker from kwargs or use default
        ticker = kwargs.get('ticker')
        if ticker:
            context.ticker = ticker.strip().upper()
        elif not context.ticker:
            context.ticker = 'LAST_MENTIONED'  # Placeholder for AI to interpret
        
        self.logger.debug(f"Button action completed: type={button_type}, ticker={context.ticker}")
    
    def on_regular_chat(self, context: StateContext, **kwargs) -> None:
        """Action for regular chat messages (non-button triggered)"""
        message = kwargs.get('message', '')
        self.logger.info(f"Regular chat message: {message[:50]}...")
        # For regular chat, we don't change context data
    
    # === Simplified AI Processing Actions ===
    
    def on_start_ai_processing(self, context: StateContext, **kwargs) -> None:
        """Action when starting AI processing (simplified workflow)"""
        # Build prompt based on button type
        ticker = context.ticker or 'the last mentioned stock'
        
        prompts = {
            'snapshot': f"Provide a comprehensive stock snapshot for {ticker}. Include: Current price, Percentage change, $ Change, Volume, VWAP (Volume Weighted Average Price), Open, High, Low, Close. Format numbers clearly with appropriate units.",
            'support_resistance': f"Analyze support and resistance levels for {ticker}. Provide: 3 support levels (S1, S2, S3) with prices, 3 resistance levels (R1, R2, R3) with prices, Brief explanation of each level's significance. Use recent price action and technical analysis.",
            'technical': f"Provide technical analysis indicators for {ticker}: RSI (14-day), MACD (12,26,9) with signal line status, Moving Averages: EMA and SMA for 5, 10, 20, 50, 200 days, Current trend assessment based on these indicators. Include specific values and interpretations."
        }
        
        context.prompt = prompts.get(context.button_type)
        if not context.prompt:
            raise ValueError(f"Unknown button type: {context.button_type}")
        
        self.logger.info(f"Starting AI processing for {context.button_type}: {len(context.prompt)} characters")
        context.parsed_data['ai_start_time'] = time.time()
    
    # === AI Processing Actions ===
    
    def on_response_received(self, context: StateContext, **kwargs) -> None:
        """Action when AI response is received (simplified for single chat output)"""
        response = kwargs.get('ai_response', context.ai_response)
        if response:
            context.ai_response = response
        
        # Extract JSON for display using simplified method
        self.on_extract_json_for_display(context, **kwargs)
        
        # Calculate AI processing time
        start_time = context.parsed_data.get('ai_start_time')
        if start_time:
            processing_time = time.time() - start_time
            context.parsed_data['ai_processing_time'] = processing_time
            self.logger.info(f"AI response received in {processing_time:.2f}s: {len(response)} characters")
        else:
            self.logger.info(f"AI response received: {len(response)} characters")
        
        self.logger.debug(f"Response preview: {response[:200]}...")
    
    def on_ai_timeout(self, context: StateContext, **kwargs) -> None:
        """Action when AI processing times out"""
        timeout_duration = kwargs.get('timeout', 'unknown')
        context.error_message = f"AI processing timed out after {timeout_duration}"
        context.increment_error_attempts()
        self.logger.error(context.error_message)
    
    def on_ai_error(self, context: StateContext, **kwargs) -> None:
        """Action when AI processing encounters an error"""
        error_msg = kwargs.get('error', 'Unknown AI processing error')
        context.error_message = error_msg
        context.increment_error_attempts()
        self.logger.error(f"AI processing error: {error_msg}")
    
    # === Parsing Actions ===
    
    def on_start_parsing(self, context: StateContext, **kwargs) -> None:
        """Action when starting to parse AI response"""
        self.logger.info(f"Starting to parse response for {context.button_type}")
        context.parsed_data['parse_start_time'] = time.time()
    
    def on_parse_success(self, context: StateContext, **kwargs) -> None:
        """Action when parsing succeeds"""
        parsed_data = kwargs.get('parsed_data', {})
        if parsed_data:
            context.parsed_data.update(parsed_data)
        
        parse_time = time.time() - context.parsed_data.get('parse_start_time', time.time())
        context.parsed_data['parse_time'] = parse_time
        
        self.logger.info(f"Parsing successful in {parse_time:.2f}s: {len(parsed_data)} data points")
        self.logger.debug(f"Parsed data keys: {list(parsed_data.keys())}")
    
    def on_parse_failed_fallback(self, context: StateContext, **kwargs) -> None:
        """Action when parsing fails but we fallback to raw display"""
        context.parsed_data['raw_response'] = context.ai_response
        context.parsed_data['parse_fallback'] = True
        self.logger.warning("Parsing failed, using raw response as fallback")
    
    def on_parse_error(self, context: StateContext, **kwargs) -> None:
        """Action when parsing encounters a critical error"""
        error_msg = kwargs.get('error', 'Unknown parsing error')
        context.error_message = error_msg
        context.increment_error_attempts()
        self.logger.error(f"Parsing error: {error_msg}")
    
    # === UI Update Actions ===
    
    def on_update_complete(self, context: StateContext, **kwargs) -> None:
        """Action when UI update is complete"""
        update_time = kwargs.get('update_time', 0)
        context.parsed_data['ui_update_time'] = update_time
        
        total_time = time.time() - context.created_at
        self.logger.info(f"UI update complete in {update_time:.2f}s. Total cycle: {total_time:.2f}s")
        
        # Clear processing data but keep results
        context.prompt = None
        context.ai_response = None
        context.reset_error_attempts()
    
    def on_update_error(self, context: StateContext, **kwargs) -> None:
        """Action when UI update fails"""
        error_msg = kwargs.get('error', 'Unknown UI update error')
        context.error_message = error_msg
        context.increment_error_attempts()
        self.logger.error(f"UI update error: {error_msg}")
    
    # === Simplified Display Actions ===
    
    def on_display_complete(self, context: StateContext, **kwargs) -> None:
        """Action when display is complete (simplified workflow)"""
        total_time = time.time() - context.created_at
        self.logger.info(f"Display complete. Total cycle: {total_time:.2f}s")
        
        # Clear processing data but keep results for JSON display
        context.prompt = None
        context.reset_error_attempts()
        
        # Keep ai_response and raw_json_response for display
    
    def on_display_error(self, context: StateContext, **kwargs) -> None:
        """Action when display encounters an error"""
        error_msg = kwargs.get('error', 'Unknown display error')
        context.error_message = error_msg
        context.increment_error_attempts()
        self.logger.error(f"Display error: {error_msg}")
    
    # === Error Recovery Actions ===
    
    def on_error_occurred(self, context: StateContext, **kwargs) -> None:
        """Generic error action"""
        error_msg = kwargs.get('error', 'Unknown error occurred')
        context.error_message = error_msg
        context.increment_error_attempts()
        self.logger.error(f"Error occurred: {error_msg}")
    
    def on_retry_from_error(self, context: StateContext, **kwargs) -> None:
        """Action when retrying from error state"""
        previous_error = context.error_message
        self.logger.info(f"Retrying after error: {previous_error}")
        context.clear_data(preserve_history=True)
    
    def on_abort_from_error(self, context: StateContext, **kwargs) -> None:
        """Action when aborting from error state"""
        self.logger.info(f"Aborting after error: {context.error_message}")
        context.clear_data(preserve_history=True)
    
    def on_reset_from_error(self, context: StateContext, **kwargs) -> None:
        """Action when resetting from error state"""
        self.logger.info("Resetting context from error state")
        context.clear_data(preserve_history=False)
    
    # === Utility Actions ===
    
    def on_abort_to_idle(self, context: StateContext, **kwargs) -> None:
        """Action when aborting current operation and returning to idle"""
        self.logger.info("Operation aborted, returning to idle")
        context.clear_data(preserve_history=True)
    
    def on_reset_context(self, context: StateContext, **kwargs) -> None:
        """Action to reset the entire context"""
        self.logger.info("Context reset requested")
        context.clear_data(preserve_history=False)
    
    def on_emergency_reset(self, context: StateContext, **kwargs) -> None:
        """Emergency reset action from any state"""
        self.logger.warning("Emergency reset triggered")
        context.clear_data(preserve_history=True)
        context.error_message = "Emergency reset"
    
    # === Simplified JSON Display Actions ===
    
    def on_extract_json_for_display(self, context: StateContext, **kwargs) -> None:
        """Action to extract JSON from AI response for chat display (simplified)"""
        ai_response = context.ai_response
        if not ai_response:
            context.raw_json_response = '{"message": "No AI response available"}'
            return
        
        # Try to extract JSON from the response for display purposes
        import json
        import re
        
        # Look for JSON blocks in the response
        json_match = re.search(r'```json\s*({[\s\S]*?})\s*```', ai_response, re.IGNORECASE)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON object
            json_match = re.search(r'({[\s\S]*})', ai_response)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Fallback: store entire response with indication
                context.raw_json_response = f'{{"message": "Response contains no JSON structure", "content": "{ai_response[:100]}..."}}'
                return
        
        # Test if it's valid JSON for display
        try:
            json.loads(json_str)
            context.raw_json_response = json_str
            self.logger.info(f"JSON extracted for display: {len(json_str)} characters")
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.debug(f"JSON extraction for display failed: {e}")
            # Store anyway for debug purposes
            context.raw_json_response = f'{{"message": "Invalid JSON structure found", "raw_content": "{json_str[:100]}..."}}'
    
    # === Enhanced Error Recovery Actions ===
    
    def on_error_button_recovery(self, context: StateContext, **kwargs) -> None:
        """Action when user clicks button from ERROR state to recover"""
        button_type = kwargs.get('button_type', context.button_type)
        previous_error = context.error_message
        
        self.logger.info(f"Button recovery initiated: {button_type} (previous error: {previous_error})")
        
        # Clear error state but preserve attempt count
        context.error_message = None
        context.button_type = button_type
        
        # Set ticker from kwargs or use default
        ticker = kwargs.get('ticker')
        if ticker:
            context.ticker = ticker.strip().upper()
        elif not context.ticker:
            context.ticker = 'LAST_MENTIONED'
        
        self.logger.info(f"Error recovery via button click: {button_type} for {context.ticker}")
    
    def on_auto_recover_from_error(self, context: StateContext, **kwargs) -> None:
        """Action for automatic error recovery after timeout"""
        previous_error = context.error_message
        recovery_reason = kwargs.get('reason', 'timeout')
        
        self.logger.info(f"Auto-recovery triggered: {recovery_reason} (previous error: {previous_error})")
        
        # Clear error data and reset to clean state
        context.clear_data(preserve_history=True)
        context.error_message = f"Auto-recovered from: {previous_error}"
        
        # Reset error attempts to allow fresh start
        context.reset_error_attempts()
    
    def on_user_recover_from_error(self, context: StateContext, **kwargs) -> None:
        """Action for manual user-initiated recovery"""
        previous_error = context.error_message
        recovery_method = kwargs.get('method', 'manual')
        
        self.logger.info(f"User recovery initiated: {recovery_method} (previous error: {previous_error})")
        
        # Clear error state but keep some context for user feedback
        context.error_message = None
        context.reset_error_attempts()
        
        # Preserve any valid ticker or button_type that might be useful
        if not context.ticker and kwargs.get('ticker'):
            context.ticker = kwargs['ticker'].strip().upper()
        
        self.logger.info(f"User recovery completed: {recovery_method}")


class StateManager:
    """
    Main FSM controller providing deterministic state management.
    
    This class orchestrates all state transitions, executes actions,
    validates guards, handles errors, and provides comprehensive logging.
    """
    
    def __init__(self, session_id: Optional[str] = None, 
                 log_level: int = logging.INFO):
        """
        Initialize the State Manager.
        
        Args:
            session_id: Unique session identifier
            log_level: Logging level for state transitions
        """
        # Generate session ID if not provided
        self.session_id = session_id or str(uuid.uuid4())[:8]
        
        # Initialize logging
        self.logger = self._setup_logging(log_level)
        
        # Initialize components
        self.transitions = StateTransitions()
        self.actions = StateActions(self.logger)
        
        # Initialize context
        self.context = StateContext(session_id=self.session_id)
        
        # Action registry
        self._action_registry = self._build_action_registry()
        
        # Statistics
        self._stats = {
            'total_transitions': 0,
            'successful_transitions': 0,
            'failed_transitions': 0,
            'error_recoveries': 0,
            'session_start': time.time()
        }
        
        self.logger.info(f"StateManager initialized with session {self.session_id}")
        
        # Validate the FSM is well-formed
        validation = self.transitions.validate_state_machine_completeness()
        if not validation['validation_passed']:
            self.logger.warning(f"FSM validation issues: {validation['issues']}")
    
    def _setup_logging(self, log_level: int) -> logging.Logger:
        """Setup structured logging for the FSM"""
        logger = logging.getLogger(f"stock_fsm.{self.session_id}")
        logger.setLevel(log_level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _build_action_registry(self) -> Dict[str, Callable]:
        """Build simplified registry of action functions"""
        return {
            'on_button_clicked': self.actions.on_button_clicked,
            'on_regular_chat': self.actions.on_regular_chat,
            'on_start_ai_processing': self.actions.on_start_ai_processing,
            'on_response_received': self.actions.on_response_received,
            'on_ai_timeout': self.actions.on_ai_timeout,
            'on_ai_error': self.actions.on_ai_error,
            'on_display_complete': self.actions.on_display_complete,
            'on_display_error': self.actions.on_display_error,
            'on_error_occurred': self.actions.on_error_occurred,
            'on_retry_from_error': self.actions.on_retry_from_error,
            'on_abort_from_error': self.actions.on_abort_from_error,
            'on_reset_from_error': self.actions.on_reset_from_error,
            'on_abort_to_idle': self.actions.on_abort_to_idle,
            'on_reset_context': self.actions.on_reset_context,
            'on_emergency_reset': self.actions.on_emergency_reset,
            'on_error_button_recovery': self.actions.on_error_button_recovery,
            'on_auto_recover_from_error': self.actions.on_auto_recover_from_error,
            'on_user_recover_from_error': self.actions.on_user_recover_from_error,
            'on_extract_json_for_display': self.actions.on_extract_json_for_display,
        }
    
    # === Core FSM Operations ===
    
    def transition(self, event: str, **kwargs) -> bool:
        """
        Execute a state transition if valid.
        
        Args:
            event: Event name triggering the transition
            **kwargs: Additional data passed to action functions
            
        Returns:
            True if transition succeeded, False if invalid or failed
        """
        current_state = self.context.current_state
        transition_key = (current_state, event)
        
        self._stats['total_transitions'] += 1
        
        # Check if transition exists
        rule = self.transitions.get_transition_rule(current_state, event)
        if not rule:
            self.logger.warning(f"Invalid transition: {current_state.name} + '{event}'")
            self._stats['failed_transitions'] += 1
            return False
        
        next_state, guard_func, action_name = rule
        
        # Validate guard condition
        if guard_func:
            try:
                # Special handling for transitions with kwargs
                if event == 'button_click' and 'button_type' in kwargs:
                    # Temporarily set button_type for guard check
                    original_button_type = self.context.button_type
                    try:
                        self.context.button_type = kwargs['button_type']
                        guard_passed = guard_func(self.context)
                    finally:
                        # Always restore original button_type, even if guard function throws
                        self.context.button_type = original_button_type
                elif event == 'response_received' and 'ai_response' in kwargs:
                    # Temporarily set ai_response for guard check
                    original_ai_response = self.context.ai_response
                    try:
                        self.context.ai_response = kwargs['ai_response']
                        guard_passed = guard_func(self.context)
                    finally:
                        # Always restore original ai_response
                        self.context.ai_response = original_ai_response
                else:
                    guard_passed = guard_func(self.context)
                    
                if not guard_passed:
                    self.logger.info(f"Guard failed: {current_state.name} -{event}-> {next_state.name}")
                    self._stats['failed_transitions'] += 1
                    return False
            except Exception as e:
                self.logger.error(f"Guard function error: {e}")
                self._emergency_transition_to_error(f"Guard error: {e}")
                self._stats['failed_transitions'] += 1
                return False
        
        # Record the transition attempt
        self.logger.info(f"Transitioning: {current_state.name} -{event}-> {next_state.name}")
        
        # Execute the transition
        try:
            # Update state
            previous_state = self.context.current_state
            self.context.previous_state = previous_state
            self.context.current_state = next_state
            
            # Execute action if defined
            if action_name and action_name in self._action_registry:
                self._action_registry[action_name](self.context, **kwargs)
            elif action_name:
                self.logger.warning(f"Action not found: {action_name}")
            
            # Record successful transition
            self.context.add_transition_record(
                from_state=previous_state,
                to_state=next_state,
                event=event,
                success=True
            )
            
            self._stats['successful_transitions'] += 1
            self.logger.debug(f"Transition completed successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Transition action failed: {e}")
            
            # Record failed transition
            self.context.add_transition_record(
                from_state=current_state,
                to_state=next_state,
                event=event,
                success=False,
                error_message=str(e)
            )
            
            # Emergency transition to error state
            self._emergency_transition_to_error(f"Action error: {e}")
            self._stats['failed_transitions'] += 1
            
            return False
    
    def _emergency_transition_to_error(self, error_message: str) -> None:
        """Emergency transition to ERROR state bypassing normal rules"""
        previous_state = self.context.current_state
        self.context.previous_state = previous_state
        self.context.current_state = AppState.ERROR
        self.context.error_message = error_message
        self.context.increment_error_attempts()
        
        self.context.add_transition_record(
            from_state=previous_state,
            to_state=AppState.ERROR,
            event="emergency_error",
            success=True,
            error_message=error_message
        )
        
        self.logger.error(f"Emergency transition to ERROR: {error_message}")
    
    # === State Query Methods ===
    
    def get_current_state(self) -> AppState:
        """Get the current state"""
        return self.context.current_state
    
    def get_previous_state(self) -> Optional[AppState]:
        """Get the previous state"""
        return self.context.previous_state
    
    def is_in_state(self, state: AppState) -> bool:
        """Check if currently in specified state"""
        return self.context.current_state == state
    
    def can_transition(self, event: str, **kwargs) -> bool:
        """Check if a transition is valid from current state"""
        # Special handling for button_click
        if event == 'button_click' and 'button_type' in kwargs:
            original_button_type = self.context.button_type
            self.context.button_type = kwargs['button_type']
            result = self.transitions.is_valid_transition(
                self.context.current_state, event, self.context
            )
            self.context.button_type = original_button_type
            return result
        else:
            return self.transitions.is_valid_transition(
                self.context.current_state, event, self.context
            )
    
    def get_available_events(self) -> List[str]:
        """Get all events available from current state"""
        events = self.transitions.get_available_events(self.context.current_state)
        
        # If in ERROR state, check if auto-recovery is available
        if self.is_in_state(AppState.ERROR):
            from .transitions import TransitionGuards
            if TransitionGuards.can_auto_recover(self.context):
                if 'auto_recover' not in events:
                    events.append('auto_recover')
        
        return events
    
    # === Error Recovery ===
    
    def recover_from_error(self, strategy: str = 'retry', return_details: bool = False, **kwargs):
        """
        Attempt to recover from error state.
        
        Args:
            strategy: Recovery strategy ('retry', 'abort', 'reset', 'auto', 'user')
            return_details: If True, returns dict with details; if False, returns bool (backward compatibility)
            **kwargs: Additional parameters for recovery actions
            
        Returns:
            bool or Dict[str, Any]: Success status (bool) or detailed feedback (dict)
        """
        if not self.is_in_state(AppState.ERROR):
            self.logger.warning("Not in error state, cannot recover")
            if return_details:
                return {
                    'success': False,
                    'message': 'System is not in error state',
                    'status': 'not_in_error'
                }
            return False
        
        self._stats['error_recoveries'] += 1
        previous_error = self.context.error_message
        
        recovery_events = {
            'retry': 'retry',
            'abort': 'abort', 
            'reset': 'reset',
            'auto': 'auto_recover',
            'user': 'user_recover'
        }
        
        event = recovery_events.get(strategy, 'abort')
        success = self.transition(event, **kwargs)
        
        if success:
            self.logger.info(f"Error recovery successful using strategy: {strategy}")
            if return_details:
                return {
                    'success': True,
                    'message': f'System recovered from error. Previous issue: {previous_error}',
                    'status': 'recovered',
                    'strategy_used': strategy,
                    'previous_error': previous_error
                }
            return True
        else:
            self.logger.error(f"Error recovery failed using strategy: {strategy}")
            if return_details:
                return {
                    'success': False,
                    'message': f'Failed to recover using {strategy}. Please try manual reset.',
                    'status': 'recovery_failed',
                    'strategy_attempted': strategy,
                    'current_error': self.context.error_message
                }
            return False
    
    def check_auto_recovery(self) -> bool:
        """
        Check if auto-recovery should be triggered and execute if needed.
        
        Returns:
            True if auto-recovery was triggered and succeeded
        """
        if not self.is_in_state(AppState.ERROR):
            return False
        
        # Check if auto-recovery conditions are met
        from .transitions import TransitionGuards
        if TransitionGuards.can_auto_recover(self.context):
            self.logger.info("Auto-recovery conditions met, attempting recovery")
            return self.recover_from_error('auto', reason='timeout')
        
        return False
    
    def force_recovery(self, message: str = "System reset by user") -> Dict[str, Any]:
        """
        Force recovery from any state - emergency function.
        
        Args:
            message: Reason for forced recovery
            
        Returns:
            Recovery status information
        """
        current_state = self.context.current_state
        
        self.logger.warning(f"Force recovery initiated from {current_state.name}: {message}")
        
        # Force transition to IDLE regardless of current state
        self._emergency_transition_to_idle(message)
        
        return {
            'success': True,
            'message': f'System forcibly recovered from {current_state.name}',
            'status': 'force_recovered',
            'previous_state': current_state.name,
            'reason': message
        }
    
    def _emergency_transition_to_idle(self, reason: str) -> None:
        """Emergency transition to IDLE state bypassing normal rules"""
        previous_state = self.context.current_state
        self.context.previous_state = previous_state
        self.context.current_state = AppState.IDLE
        self.context.clear_data(preserve_history=True)
        self.context.error_message = None
        self.context.reset_error_attempts()
        
        self.context.add_transition_record(
            from_state=previous_state,
            to_state=AppState.IDLE,
            event="emergency_idle",
            success=True,
            error_message=reason
        )
        
        self.logger.info(f"Emergency transition to IDLE completed: {reason}")
    
    # === Statistics and Monitoring ===
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get FSM performance statistics"""
        session_duration = time.time() - self._stats['session_start']
        
        stats = self._stats.copy()
        stats.update({
            'session_duration': session_duration,
            'current_state': self.context.current_state.name,
            'error_attempts': self.context.error_recovery_attempts,
            'context_summary': self.context.get_history_summary(),
            'success_rate': (self._stats['successful_transitions'] / 
                           max(1, self._stats['total_transitions']) * 100)
        })
        
        return stats
    
    def get_context_dict(self, include_history: bool = False) -> Dict[str, Any]:
        """Get context as dictionary for serialization"""
        return self.context.to_dict(include_history=include_history)
    
    def validate_fsm_health(self) -> Dict[str, Any]:
        """Perform health check on the FSM"""
        return {
            'fsm_validation': self.transitions.validate_state_machine_completeness(),
            'context_health': {
                'current_state': self.context.current_state.name,
                'error_attempts': self.context.error_recovery_attempts,
                'has_errors': bool(self.context.error_message),
                'data_integrity': bool(self.context.parsed_data) if self.context.button_type else True
            },
            'statistics': self.get_statistics()
        }
    
    # === Serialization Support for Gradio ===
    
    def __getstate__(self) -> Dict[str, Any]:
        """Support for pickle serialization (Gradio State compatibility)"""
        return {
            'session_id': self.session_id,
            'context_dict': self.context.to_dict(include_history=True),
            'stats': self._stats
        }
    
    def __setstate__(self, state: Dict[str, Any]) -> None:
        """Support for pickle deserialization (Gradio State compatibility)"""
        self.session_id = state['session_id']
        self._stats = state['stats']
        
        # Reinitialize components
        self.logger = self._setup_logging(logging.INFO)
        self.transitions = StateTransitions()
        self.actions = StateActions(self.logger)
        self._action_registry = self._build_action_registry()
        
        # Restore context
        context_dict = state['context_dict']
        self.context = StateContext(session_id=self.session_id)
        self.context.current_state = AppState[context_dict['current_state']]
        if context_dict['previous_state']:
            self.context.previous_state = AppState[context_dict['previous_state']]
        
        # Restore other context fields
        for field in ['button_type', 'ticker', 'prompt', 'ai_response', 
                     'raw_json_response', 'parsed_data', 'error_message', 'error_recovery_attempts']:
            if field in context_dict:
                setattr(self.context, field, context_dict[field])
    
    def __str__(self) -> str:
        """String representation"""
        return f"StateManager(session={self.session_id}, state={self.context.current_state.name})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return (f"StateManager(session_id='{self.session_id}', "
                f"current_state={self.context.current_state!r}, "
                f"transitions={self._stats['total_transitions']})")
