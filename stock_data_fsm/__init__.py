"""
Stock Data FSM - Finite State Machine for Stock Data GUI Application

This module provides a deterministic finite state machine implementation
for managing the stock data GUI application state transitions.

Public API:
    - AppState: Enum defining all possible application states
    - StateContext: Data container for state transitions
    - StateManager: Main FSM controller with transition logic
    - StateTransitions: Transition rules and validation
"""

from .states import AppState, StateContext
from .transitions import StateTransitions
from .manager import StateManager

__version__ = "1.0.0"
__author__ = "Market Parser Development Team"

__all__ = [
    "AppState",
    "StateContext", 
    "StateTransitions",
    "StateManager"
]
