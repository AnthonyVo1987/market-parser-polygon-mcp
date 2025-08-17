"""
State definitions for the Stock Data FSM

This module contains:
- AppState: Enum defining all possible application states
- StateContext: Dataclass containing state transition data
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import time


class AppState(Enum):
    """
    Deterministic application states for the Stock Data GUI.
    
    State Descriptions:
        IDLE: Application waiting for user interaction
        BUTTON_TRIGGERED: User clicked a data request button
        PROMPT_PREPARING: Building AI prompt with ticker information
        AI_PROCESSING: Waiting for AI agent response
        RESPONSE_RECEIVED: AI response received, ready for parsing
        PARSING_RESPONSE: Extracting structured data from response
        UPDATING_UI: Updating GUI components with parsed data
        ERROR: Error state with recovery options
    """
    IDLE = auto()
    BUTTON_TRIGGERED = auto()
    PROMPT_PREPARING = auto()
    AI_PROCESSING = auto()
    RESPONSE_RECEIVED = auto()
    PARSING_RESPONSE = auto()
    UPDATING_UI = auto()
    ERROR = auto()
    
    def __str__(self) -> str:
        """Human-readable state name"""
        return self.name
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return f"AppState.{self.name}"


@dataclass
class TransitionRecord:
    """Record of a single state transition for audit trail"""
    from_state: AppState
    to_state: AppState
    event: str
    timestamp: float
    success: bool
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Validate transition record data"""
        if self.timestamp <= 0:
            self.timestamp = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'from_state': self.from_state.name,
            'to_state': self.to_state.name,
            'event': self.event,
            'timestamp': self.timestamp,
            'success': self.success,
            'error_message': self.error_message
        }


@dataclass
class StateContext:
    """
    Context data container for state transitions.
    
    This dataclass acts as the single source of truth for all state-related
    data, ensuring consistent data flow through state transitions.
    """
    # Core state information
    current_state: AppState = AppState.IDLE
    previous_state: Optional[AppState] = None
    
    # Button interaction data
    button_type: Optional[str] = None  # 'snapshot', 'support_resistance', 'technical'
    ticker: Optional[str] = None
    
    # AI interaction data
    prompt: Optional[str] = None
    ai_response: Optional[str] = None
    
    # Parsed data storage
    parsed_data: Dict[str, Any] = field(default_factory=dict)
    
    # Error handling
    error_message: Optional[str] = None
    error_recovery_attempts: int = 0
    
    # Audit trail
    transition_history: List[TransitionRecord] = field(default_factory=list)
    
    # Metadata
    session_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    
    def __post_init__(self):
        """Initialize context with validation"""
        if not isinstance(self.current_state, AppState):
            raise ValueError(f"current_state must be AppState, got {type(self.current_state)}")
        
        if self.previous_state and not isinstance(self.previous_state, AppState):
            raise ValueError(f"previous_state must be AppState or None, got {type(self.previous_state)}")
    
    def add_transition_record(self, from_state: AppState, to_state: AppState, 
                            event: str, success: bool = True, 
                            error_message: Optional[str] = None) -> None:
        """Add a transition record to the audit trail"""
        record = TransitionRecord(
            from_state=from_state,
            to_state=to_state,
            event=event,
            timestamp=time.time(),
            success=success,
            error_message=error_message
        )
        self.transition_history.append(record)
        self.last_updated = time.time()
    
    def clear_data(self, preserve_history: bool = True) -> None:
        """
        Clear context data while optionally preserving history
        
        Args:
            preserve_history: If True, keeps transition history
        """
        self.button_type = None
        self.ticker = None
        self.prompt = None
        self.ai_response = None
        self.parsed_data.clear()
        self.error_message = None
        self.error_recovery_attempts = 0
        
        if not preserve_history:
            self.transition_history.clear()
        
        self.last_updated = time.time()
    
    def increment_error_attempts(self) -> int:
        """Increment and return error recovery attempts"""
        self.error_recovery_attempts += 1
        self.last_updated = time.time()
        return self.error_recovery_attempts
    
    def reset_error_attempts(self) -> None:
        """Reset error recovery attempt counter"""
        self.error_recovery_attempts = 0
        self.error_message = None
        self.last_updated = time.time()
    
    def get_history_summary(self) -> Dict[str, Any]:
        """Get summary of transition history"""
        if not self.transition_history:
            return {'total_transitions': 0}
        
        return {
            'total_transitions': len(self.transition_history),
            'successful_transitions': sum(1 for r in self.transition_history if r.success),
            'failed_transitions': sum(1 for r in self.transition_history if not r.success),
            'first_transition': self.transition_history[0].timestamp,
            'last_transition': self.transition_history[-1].timestamp,
            'session_duration': time.time() - self.created_at
        }
    
    def to_dict(self, include_history: bool = False) -> Dict[str, Any]:
        """
        Convert context to dictionary for serialization
        
        Args:
            include_history: If True, includes full transition history
        """
        data = {
            'current_state': self.current_state.name,
            'previous_state': self.previous_state.name if self.previous_state else None,
            'button_type': self.button_type,
            'ticker': self.ticker,
            'prompt': self.prompt,
            'ai_response': self.ai_response,
            'parsed_data': self.parsed_data.copy(),
            'error_message': self.error_message,
            'error_recovery_attempts': self.error_recovery_attempts,
            'session_id': self.session_id,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'history_summary': self.get_history_summary()
        }
        
        if include_history:
            data['transition_history'] = [r.to_dict() for r in self.transition_history]
        
        return data
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return f"StateContext(state={self.current_state.name}, button_type={self.button_type})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return (f"StateContext(current_state={self.current_state!r}, "
                f"button_type={self.button_type!r}, ticker={self.ticker!r})")
