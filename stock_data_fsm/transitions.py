"""
State transition rules and guards for the Stock Data FSM

This module contains:
- StateTransitions: Class defining all valid state transitions
- Guard functions: Validation logic for transition conditions
- Action definitions: Actions to execute during transitions
"""

from typing import Dict, Tuple, Optional, Callable, Any
from .states import AppState, StateContext
import logging
import time


# Type aliases for better readability
TransitionKey = Tuple[AppState, str]  # (current_state, event)
GuardFunction = Callable[[StateContext], bool]
ActionName = str
TransitionRule = Tuple[AppState, Optional[GuardFunction], ActionName]


class TransitionGuards:
    """
    Guard functions that validate whether a transition should be allowed.
    
    Guards are pure functions that take StateContext and return bool.
    They should not modify the context - only validate conditions.
    """
    
    @staticmethod
    def has_valid_button_type(context: StateContext) -> bool:
        """Check if button_type is valid"""
        return context.button_type in ['snapshot', 'support_resistance', 'technical']
    
    @staticmethod
    def has_prompt(context: StateContext) -> bool:
        """Check if prompt is available"""
        return context.prompt is not None and len(context.prompt.strip()) > 0
    
    @staticmethod
    def has_ai_response(context: StateContext) -> bool:
        """Check if AI response is available"""
        return context.ai_response is not None and len(context.ai_response.strip()) > 0
    
    @staticmethod
    def has_parsed_data(context: StateContext) -> bool:
        """Check if parsed data is available"""
        return bool(context.parsed_data)
    
    @staticmethod
    def under_max_error_attempts(context: StateContext) -> bool:
        """Check if we haven't exceeded max error recovery attempts"""
        MAX_ERROR_ATTEMPTS = 3
        return context.error_recovery_attempts < MAX_ERROR_ATTEMPTS
    
    @staticmethod
    def is_idle_ready(context: StateContext) -> bool:
        """Check if context is ready to return to IDLE"""
        # Can return to IDLE if no active processing
        return context.current_state != AppState.AI_PROCESSING
    
    @staticmethod
    def has_ticker_or_default(context: StateContext) -> bool:
        """Check if ticker is available or can use default"""
        return (context.ticker is not None and len(context.ticker.strip()) > 0) or True
    
    @staticmethod
    def can_retry_from_error(context: StateContext) -> bool:
        """Check if retry is allowed from error state"""
        return (context.current_state == AppState.ERROR and 
                context.error_recovery_attempts < 5)
    
    @staticmethod
    def can_auto_recover(context: StateContext) -> bool:
        """Check if auto-recovery is allowed based on error age"""
        if context.current_state != AppState.ERROR:
            return False
        
        # Auto-recover if error is older than 30 seconds
        error_age = time.time() - context.last_updated
        return error_age > 30.0
    
    @staticmethod
    def has_recoverable_error(context: StateContext) -> bool:
        """Check if the error is recoverable (not a critical system error)"""
        if not context.error_message:
            return True
        
        # List of non-recoverable error patterns
        critical_errors = [
            'Invalid API key',
            'Network unreachable',
            'System shutdown',
            'Memory allocation failed'
        ]
        
        error_msg = context.error_message.lower()
        return not any(critical in error_msg for critical in critical_errors)
    
    @staticmethod
    def is_valid_data_type(context: StateContext) -> bool:
        """Check if the data type being processed is valid"""
        if not context.button_type:
            return False
        return context.button_type in ['snapshot', 'support_resistance', 'technical']
    
    # === JSON Workflow Guards ===
    
    @staticmethod
    def has_raw_json_response(context: StateContext) -> bool:
        """Check if raw JSON response is available"""
        return context.raw_json_response is not None and len(context.raw_json_response.strip()) > 0
    
    @staticmethod
    def has_valid_json_format(context: StateContext) -> bool:
        """Check if the response contains valid JSON format"""
        if not context.raw_json_response:
            return False
        try:
            import json
            json.loads(context.raw_json_response)
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    
    @staticmethod
    def has_validated_json_data(context: StateContext) -> bool:
        """Check if JSON validation has completed successfully"""
        return (context.validated_json_data is not None and 
                context.json_validation_result is not None and
                context.json_validation_result.get('valid', False))
    
    @staticmethod
    def has_json_schema_type(context: StateContext) -> bool:
        """Check if JSON schema type is determined"""
        return context.json_schema_type in ['snapshot', 'support_resistance', 'technical']
    
    @staticmethod
    def can_retry_json_validation(context: StateContext) -> bool:
        """Check if JSON validation can be retried"""
        return (context.raw_json_response is not None and
                context.error_recovery_attempts < 3)
    
    @staticmethod
    def can_fallback_to_text_parsing(context: StateContext) -> bool:
        """Check if we can fallback to text parsing when JSON fails"""
        return (context.ai_response is not None and
                len(context.ai_response.strip()) > 0)


class StateTransitions:
    """
    Defines all valid state transitions, guards, and actions for the FSM.
    
    This class acts as the central registry for all state transition rules,
    making the FSM behavior completely deterministic and auditable.
    """
    
    def __init__(self):
        """Initialize transition rules and logging"""
        self.logger = logging.getLogger(__name__)
        self._transitions = self._build_transition_table()
        self._validate_transition_table()
    
    def _build_transition_table(self) -> Dict[TransitionKey, TransitionRule]:
        """
        Build the simplified state transition table.
        
        Simplified workflow: IDLE -> BUTTON_TRIGGERED -> AI_PROCESSING -> RESPONSE_RECEIVED -> IDLE
        Error recovery: ERROR -> IDLE (always allow recovery)
        
        Format: (current_state, event) -> (next_state, guard_function, action_name)
        
        Returns:
            Dictionary mapping transition keys to transition rules
        """
        return {
            # === FROM IDLE STATE ===
            (AppState.IDLE, 'button_click'): (
                AppState.BUTTON_TRIGGERED,
                TransitionGuards.has_valid_button_type,
                'on_button_clicked'
            ),
            (AppState.IDLE, 'user_chat'): (
                AppState.IDLE,  # Stay in IDLE for regular chat
                None,
                'on_regular_chat'
            ),
            (AppState.IDLE, 'reset'): (
                AppState.IDLE,
                None,
                'on_reset_context'
            ),
            
            # === FROM BUTTON_TRIGGERED STATE ===
            (AppState.BUTTON_TRIGGERED, 'start_ai_processing'): (
                AppState.AI_PROCESSING,
                None,  # No guards for simplified workflow
                'on_start_ai_processing'
            ),
            (AppState.BUTTON_TRIGGERED, 'error'): (
                AppState.ERROR,
                None,
                'on_error_occurred'
            ),
            
            # === FROM AI_PROCESSING STATE ===
            (AppState.AI_PROCESSING, 'response_received'): (
                AppState.RESPONSE_RECEIVED,
                TransitionGuards.has_ai_response,
                'on_response_received'
            ),
            (AppState.AI_PROCESSING, 'ai_timeout'): (
                AppState.ERROR,
                None,
                'on_ai_timeout'
            ),
            (AppState.AI_PROCESSING, 'ai_error'): (
                AppState.ERROR,
                None,
                'on_ai_error'
            ),
            
            # === FROM RESPONSE_RECEIVED STATE ===
            (AppState.RESPONSE_RECEIVED, 'display_complete'): (
                AppState.IDLE,
                None,
                'on_display_complete'
            ),
            (AppState.RESPONSE_RECEIVED, 'display_error'): (
                AppState.ERROR,
                None,
                'on_display_error'
            ),
            
            # === FROM ERROR STATE - Enhanced Recovery Transitions ===
            (AppState.ERROR, 'retry'): (
                AppState.IDLE,
                None,  # Always allow retry
                'on_retry_from_error'
            ),
            (AppState.ERROR, 'abort'): (
                AppState.IDLE,
                None,
                'on_abort_from_error'
            ),
            (AppState.ERROR, 'reset'): (
                AppState.IDLE,
                None,
                'on_reset_from_error'
            ),
            # CRITICAL: Allow button clicks from ERROR state to recover immediately
            (AppState.ERROR, 'button_click'): (
                AppState.BUTTON_TRIGGERED,
                TransitionGuards.has_valid_button_type,
                'on_error_button_recovery'
            ),
            # Auto-recovery after timeout
            (AppState.ERROR, 'auto_recover'): (
                AppState.IDLE,
                None,
                'on_auto_recover_from_error'
            ),
            # Emergency user recovery
            (AppState.ERROR, 'user_recover'): (
                AppState.IDLE,
                None,
                'on_user_recover_from_error'
            ),
            
            # === EMERGENCY TRANSITIONS (available from any state) ===
            (AppState.BUTTON_TRIGGERED, 'emergency_reset'): (
                AppState.IDLE,
                None,
                'on_emergency_reset'
            ),
            (AppState.AI_PROCESSING, 'emergency_reset'): (
                AppState.IDLE,
                None,
                'on_emergency_reset'
            ),
            (AppState.RESPONSE_RECEIVED, 'emergency_reset'): (
                AppState.IDLE,
                None,
                'on_emergency_reset'
            ),
        }
    
    def _validate_transition_table(self) -> None:
        """Validate the transition table for consistency"""
        # Check for duplicate transitions
        seen_keys = set()
        for key in self._transitions:
            if key in seen_keys:
                raise ValueError(f"Duplicate transition key: {key}")
            seen_keys.add(key)
        
        # Validate that all states have at least one outgoing transition
        states_with_outgoing = {key[0] for key in self._transitions.keys()}
        for state in AppState:
            if state not in states_with_outgoing and state not in [AppState.ERROR]:
                self.logger.warning(f"State {state.name} has no outgoing transitions")
        
        self.logger.info(f"Validated {len(self._transitions)} state transitions")
    
    def get_transition_rule(self, current_state: AppState, event: str) -> Optional[TransitionRule]:
        """
        Get the transition rule for a given state and event.
        
        Args:
            current_state: Current application state
            event: Event that triggered the transition
            
        Returns:
            Transition rule tuple or None if no valid transition exists
        """
        return self._transitions.get((current_state, event))
    
    def is_valid_transition(self, current_state: AppState, event: str, 
                          context: StateContext) -> bool:
        """
        Check if a transition is valid given the current context.
        
        Args:
            current_state: Current application state
            event: Event that triggered the transition
            context: Current state context
            
        Returns:
            True if transition is valid, False otherwise
        """
        rule = self.get_transition_rule(current_state, event)
        if not rule:
            return False
        
        next_state, guard_func, action_name = rule
        
        # If there's a guard function, check it
        if guard_func:
            try:
                return guard_func(context)
            except Exception as e:
                self.logger.error(f"Guard function failed for {current_state}->{event}: {e}")
                return False
        
        return True
    
    def get_available_events(self, current_state: AppState) -> list[str]:
        """
        Get all available events from a given state.
        
        Args:
            current_state: Current application state
            
        Returns:
            List of event names that can be triggered from this state
        """
        return [event for (state, event) in self._transitions.keys() if state == current_state]
    
    def get_reachable_states(self, from_state: AppState) -> list[AppState]:
        """
        Get all states reachable from the given state.
        
        Args:
            from_state: Starting state
            
        Returns:
            List of states that can be reached from the starting state
        """
        reachable = []
        for (state, event), (next_state, guard, action) in self._transitions.items():
            if state == from_state and next_state not in reachable:
                reachable.append(next_state)
        return reachable
    
    def validate_state_machine_completeness(self) -> Dict[str, Any]:
        """
        Validate that the state machine is complete and well-formed.
        
        Returns:
            Dictionary with validation results and statistics
        """
        results = {
            'total_transitions': len(self._transitions),
            'total_states': len(AppState),
            'states_with_outgoing': len({key[0] for key in self._transitions.keys()}),
            'states_with_incoming': len({rule[0] for rule in self._transitions.values()}),
            'unreachable_states': [],
            'dead_end_states': [],
            'validation_passed': True,
            'issues': []
        }
        
        # Find unreachable states (except IDLE which is the starting state)
        reachable_states = {AppState.IDLE}  # Start with IDLE
        for (from_state, event), (to_state, guard, action) in self._transitions.items():
            if from_state in reachable_states:
                reachable_states.add(to_state)
        
        all_states = set(AppState)
        unreachable = all_states - reachable_states
        if unreachable:
            results['unreachable_states'] = [s.name for s in unreachable]
            results['issues'].append(f"Unreachable states: {[s.name for s in unreachable]}")
        
        # Find dead-end states (no outgoing transitions except ERROR)
        states_with_outgoing = {key[0] for key in self._transitions.keys()}
        dead_end_states = all_states - states_with_outgoing
        # ERROR state is allowed to be a dead-end if it has recovery transitions
        if AppState.ERROR in dead_end_states:
            error_outgoing = self.get_available_events(AppState.ERROR)
            if error_outgoing:
                dead_end_states.remove(AppState.ERROR)
        
        if dead_end_states:
            results['dead_end_states'] = [s.name for s in dead_end_states]
            results['issues'].append(f"Dead-end states: {[s.name for s in dead_end_states]}")
        
        results['validation_passed'] = len(results['issues']) == 0
        return results
    
    def get_transition_graph(self) -> Dict[str, list[str]]:
        """
        Get a simplified graph representation of transitions for visualization.
        
        Returns:
            Dictionary mapping state names to lists of reachable state names
        """
        graph = {}
        for state in AppState:
            reachable = self.get_reachable_states(state)
            graph[state.name] = [s.name for s in reachable]
        return graph
