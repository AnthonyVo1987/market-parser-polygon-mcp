"""
Dynamic Prompt Integration for Market Parser

This module provides the integration layer to replace the static get_enhanced_agent_instructions
function with the dynamic prompting system while maintaining backward compatibility.

Features:
- Seamless replacement of static prompt function
- Backward compatibility with existing code
- User input processing for dynamic customization
- Integration with CLI and GUI systems
- Performance monitoring and caching

Author: AI Assistant
Date: September 26, 2025
"""

import logging
from datetime import datetime
from typing import Any, Dict

from .dynamic_prompt_manager import get_dynamic_prompt_manager
from .secure_prompt_manager import SecureDynamicPromptManager
from .security_features import SecurityConfig

logger = logging.getLogger(__name__)


def get_enhanced_agent_instructions(user_input: str = "") -> str:
    """
    Enhanced agent instructions with dynamic customization support.

    This function replaces the static get_enhanced_agent_instructions function
    with a dynamic version that supports user customization while maintaining
    backward compatibility.

    Args:
        user_input: Optional user input for customization

    Returns:
        Enhanced agent instructions string
    """
    try:
        # Get the dynamic prompt manager
        manager = get_dynamic_prompt_manager()

        # Generate dynamic instructions
        return manager.get_enhanced_agent_instructions(user_input)

    except Exception as e:
        logger.error(f"Error generating dynamic prompt: {e}")

        # Fallback to static prompt for backward compatibility
        return _get_static_fallback_prompt()


def get_secure_prompt_manager() -> SecureDynamicPromptManager:
    """
    Get a secure dynamic prompt manager instance.

    Returns:
        SecureDynamicPromptManager instance with security features enabled
    """
    # Create security configuration
    security_config = SecurityConfig(
        enable_rate_limiting=True,
        enable_input_validation=True,
        enable_audit_logging=True,
        enable_circuit_breaker=True,
        max_input_length=5000,
    )

    # Get base template
    base_template = _get_static_fallback_prompt()

    # Create secure manager
    return SecureDynamicPromptManager(
        base_template=base_template,
        config={"cache_size": 100, "cache_ttl": 3600},
        security_config=security_config,
    )


def get_enhanced_agent_instructions_secure(
    user_input: str = "", user_id: str = "anonymous", ip_address: str = "127.0.0.1"
) -> Dict[str, Any]:
    """
    Enhanced agent instructions with full security features.

    Args:
        user_input: Optional user input for customization
        user_id: User identifier for security tracking
        ip_address: Client IP address for security validation

    Returns:
        Dictionary containing prompt and security information
    """
    try:
        # Get the secure prompt manager
        manager = get_secure_prompt_manager()

        # Generate secure prompt with validation
        return manager.generate_prompt(
            user_input=user_input,
            context={"datetime_context": _get_current_datetime_context()},
            user_id=user_id,
            ip_address=ip_address,
        )

    except Exception as e:
        logger.error(f"Error generating secure prompt: {e}")

        # Return error response
        return {
            "success": False,
            "prompt": _get_static_fallback_prompt(),
            "security_info": {
                "validated": False,
                "sanitized": False,
                "threats_detected": [str(e)],
                "rate_limited": False,
            },
            "errors": [str(e)],
            "metadata": {
                "user_id": user_id,
                "ip_address": ip_address,
                "timestamp": datetime.now().timestamp(),
                "processing_time": 0.0,
            },
        }


def _get_static_fallback_prompt() -> str:
    """Fallback static prompt for backward compatibility"""
    datetime_context = _get_current_datetime_context()
    return f"""Quick Response Needed with minimal tool calls: You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Polygon.io MCP server for live market data, prices, and financial information.

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details"""


def _get_current_datetime_context() -> str:
    """Generate current date/time context for AI agent prompts"""
    now = datetime.now()
    return f"""
CURRENT DATE AND TIME CONTEXT:
- Today's date: {now.strftime('%A, %B %d, %Y')}
- Current time: {now.strftime('%I:%M %p %Z')}
- ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}
- Market status: {'Open' if now.weekday() < 5 and 9 <= now.hour < 16 else 'Closed'}

IMPORTANT: Always use the current date and time above for all financial analysis. 
Do NOT use training data cutoff dates or outdated information.
"""


def get_dynamic_prompt_stats() -> Dict[str, Any]:
    """Get dynamic prompt system statistics"""
    try:
        manager = get_dynamic_prompt_manager()
        return manager.get_cache_stats()
    except Exception as e:
        logger.error(f"Error getting dynamic prompt stats: {e}")
        return {"error": str(e)}


def clear_dynamic_prompt_cache() -> None:
    """Clear the dynamic prompt cache"""
    try:
        manager = get_dynamic_prompt_manager()
        manager.clear_cache()
        logger.info("Dynamic prompt cache cleared")
    except Exception as e:
        logger.error(f"Error clearing dynamic prompt cache: {e}")
