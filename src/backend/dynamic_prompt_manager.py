"""
Dynamic Prompt Manager Integration for Market Parser

This module provides the integration layer between the DynamicPromptManager
and the existing Market Parser system. It replaces the static get_enhanced_agent_instructions
function with a dynamic system that allows user customization.

Features:
- Seamless integration with existing CLI and GUI systems
- Backward compatibility with current prompt structure
- User instruction parsing and customization
- Performance optimization with caching
- Security validation and error handling

Author: AI Assistant
Date: September 26, 2025
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .dynamic_prompts import DynamicPromptManager, create_dynamic_prompt_manager

logger = logging.getLogger(__name__)


class MarketParserDynamicPromptManager:
    """
    Integration layer for DynamicPromptManager in the Market Parser system.
    
    This class provides a seamless interface between the dynamic prompting system
    and the existing Market Parser architecture, maintaining backward compatibility
    while adding dynamic customization capabilities.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_template = self._create_base_template()
        self.config = self._create_config()
        self.dynamic_manager = create_dynamic_prompt_manager(self.base_template, self.config)
    
    def _create_base_template(self) -> str:
        """Create the base template for financial analysis prompts"""
        return """Quick Response Needed with minimal tool calls: You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Polygon.io MCP server for live market data, prices, and financial information.

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: DATA FIRST → DETAILED ANALYSIS
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details

{verbosity_instruction}
{tool_restriction}
{format_instruction}
{style_instruction}

OUTPUT FORMAT:
A. DATA FIRST
- Format data in bullet point format with 2 decimal points max
- Provide cleaned up raw format data first, then verbal analysis
- Convert JSON response attributes to user-friendly terms
- Include relevant financial data and metrics

B. DETAILED ANALYSIS
- Provide Maximum of 3 KEY TAKEAWAYS/INSIGHTS in numbered/bullet point format
- No actionable recommendations
- Focus on the data only"""
    
    def _create_config(self) -> Dict[str, Any]:
        """Create configuration for the dynamic prompt manager"""
        return {
            'cache_size': 100,
            'security_rules': {
                'max_input_length': 1000,
                'rate_limit': 10,
                'allowed_verbs': ['verbose', 'minimal', 'standard', 'detailed', 'brief', 'concise'],
                'allowed_tools': ['get_snapshot_ticker', 'get_market_status', 'get_full_market_snapshot', 
                                'get_support_resistance_levels', 'get_technical_analysis'],
                'allowed_formats': ['structured', 'narrative', 'bullet points', 'json', 'markdown', 'plain'],
                'allowed_styles': ['formal', 'casual', 'technical', 'professional', 'friendly']
            }
        }
    
    def get_enhanced_agent_instructions(self, user_input: str = "") -> str:
        """
        Generate enhanced agent instructions with dynamic customization.
        
        This method replaces the static get_enhanced_agent_instructions function
        with a dynamic version that allows user customization while maintaining
        backward compatibility.
        
        Args:
            user_input: Optional user input for customization
            
        Returns:
            Enhanced agent instructions string
        """
        try:
            # Get current datetime context
            datetime_context = self._get_current_datetime_context()
            
            # Create context for template processing
            context = {
                'datetime_context': datetime_context,
                'verbosity_instruction': 'Provide balanced information with moderate detail.',
                'tool_restriction': '',
                'format_instruction': 'Format your response in a structured format with clear sections and bullet points.',
                'style_instruction': 'Use a professional, business-appropriate tone.'
            }
            
            # If user input is provided, generate dynamic prompt
            if user_input and user_input.strip():
                return self.dynamic_manager.generate_prompt(user_input, context)
            else:
                # Return base template with default values for backward compatibility
                return self.base_template.format(**context)
                
        except Exception as e:
            self.logger.error(f"Error generating dynamic prompt: {e}")
            # Fallback to base template
            return self.base_template.format(
                datetime_context=self._get_current_datetime_context(),
                verbosity_instruction='Provide balanced information with moderate detail.',
                tool_restriction='',
                format_instruction='Format your response in a structured format with clear sections and bullet points.',
                style_instruction='Use a professional, business-appropriate tone.'
            )
    
    def _get_current_datetime_context(self) -> str:
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
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        return {
            'cache_size': len(self.dynamic_manager.cache.cache),
            'max_size': self.dynamic_manager.cache.max_size,
            'hit_rate': self._calculate_hit_rate()
        }
    
    def _calculate_hit_rate(self) -> float:
        """Calculate cache hit rate (simplified implementation)"""
        # This would be implemented with proper hit/miss tracking
        return 0.0
    
    def clear_cache(self) -> None:
        """Clear the prompt cache"""
        self.dynamic_manager.cache.cache.clear()
        self.dynamic_manager.cache.access_times.clear()


# Global instance for backward compatibility
_dynamic_prompt_manager = None


def get_dynamic_prompt_manager() -> MarketParserDynamicPromptManager:
    """Get the global dynamic prompt manager instance"""
    global _dynamic_prompt_manager
    if _dynamic_prompt_manager is None:
        _dynamic_prompt_manager = MarketParserDynamicPromptManager()
    return _dynamic_prompt_manager


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
    manager = get_dynamic_prompt_manager()
    return manager.get_enhanced_agent_instructions(user_input)