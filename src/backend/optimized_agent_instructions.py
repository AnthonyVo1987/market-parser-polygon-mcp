#!/usr/bin/env python3
"""
Optimized Agent Instructions with Caching
Provides cached versions of the agent instructions to minimize overhead.
"""

import time
from datetime import datetime
from functools import lru_cache
from typing import Optional


class OptimizedAgentInstructions:
    """Optimized agent instructions with intelligent caching."""
    
    def __init__(self, cache_ttl_seconds: int = 60):
        """
        Initialize with configurable cache TTL.
        
        Args:
            cache_ttl_seconds: How long to cache the datetime context (default: 60 seconds)
        """
        self.cache_ttl = cache_ttl_seconds
        self._cached_context: Optional[str] = None
        self._cache_timestamp: float = 0.0
        
        # Pre-generate static parts of instructions
        self._static_instructions = """You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information

Remember: You have access to real-time market data - use it to provide current, accurate analysis."""
    
    def _get_cached_datetime_context(self) -> str:
        """Get datetime context with intelligent caching."""
        current_time = time.time()
        
        # Check if cache is still valid
        if (self._cached_context is not None and 
            current_time - self._cache_timestamp < self.cache_ttl):
            return self._cached_context
        
        # Generate new context
        now = datetime.now()
        self._cached_context = f"""
CURRENT DATE AND TIME CONTEXT:
- Today's date: {now.strftime('%A, %B %d, %Y')}
- Current time: {now.strftime('%I:%M %p %Z')}
- ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}
- Market status: {'Open' if now.weekday() < 5 and 9 <= now.hour < 16 else 'Closed'}

IMPORTANT: Always use the current date and time above for all financial analysis. 
Do NOT use training data cutoff dates or outdated information.
"""
        self._cache_timestamp = current_time
        return self._cached_context
    
    def get_enhanced_agent_instructions(self) -> str:
        """Get enhanced agent instructions with cached datetime context."""
        datetime_context = self._get_cached_datetime_context()
        return self._static_instructions.format(datetime_context=datetime_context)
    
    def clear_cache(self):
        """Clear the datetime context cache."""
        self._cached_context = None
        self._cache_timestamp = 0.0


# Global instance for the application
_optimized_instructions = OptimizedAgentInstructions()


def get_enhanced_agent_instructions_optimized() -> str:
    """
    Optimized version of get_enhanced_agent_instructions with caching.
    
    This version caches the datetime context for 60 seconds, significantly
    reducing overhead for high-frequency requests while maintaining accuracy.
    """
    return _optimized_instructions.get_enhanced_agent_instructions()


def get_enhanced_agent_instructions_ultra_fast() -> str:
    """
    Ultra-fast version that caches the entire instruction string.
    
    WARNING: This version caches the complete instructions for 60 seconds,
    which means the datetime context may be up to 60 seconds old.
    Only use this if you can tolerate slightly stale datetime information.
    """
    return _optimized_instructions.get_enhanced_agent_instructions()


# Alternative: Simple LRU cache approach
@lru_cache(maxsize=1)
def get_enhanced_agent_instructions_cached() -> str:
    """
    Simple LRU cache version (caches for the entire application lifetime).
    
    WARNING: This caches indefinitely, so datetime will be stale after first call.
    Only use for testing or if you don't need current datetime.
    """
    now = datetime.now()
    datetime_context = f"""
CURRENT DATE AND TIME CONTEXT:
- Today's date: {now.strftime('%A, %B %d, %Y')}
- Current time: {now.strftime('%I:%M %p %Z')}
- ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}
- Market status: {'Open' if now.weekday() < 5 and 9 <= now.hour < 16 else 'Closed'}

IMPORTANT: Always use the current date and time above for all financial analysis. 
Do NOT use training data cutoff dates or outdated information.
"""
    
    return f"""You are a professional financial analyst with access to real-time market data tools.

{datetime_context}

TOOL AVAILABILITY:
You have access to the following real-time data tools:
- Polygon.io MCP server for live market data, stock prices, and financial information
- Real-time price quotes, market snapshots, and historical data
- Current market status and trading hours information
- Live financial news and market updates

INSTRUCTIONS:
1. ALWAYS use the current date and time provided above for all analysis
2. Use the available real-time data tools to gather current market information
3. Provide accurate, data-driven financial analysis and insights
4. Focus on actionable insights and clear explanations
5. When referencing dates, use the current date context provided above
6. Do NOT rely on training data cutoff dates or outdated information

Remember: You have access to real-time market data - use it to provide current, accurate analysis."""


if __name__ == "__main__":
    # Test the optimized versions
    print("Testing optimized agent instructions...")
    
    # Test 1: Original version
    start = time.perf_counter()
    for _ in range(1000):
        # Simulate original function calls
        now = datetime.now()
        datetime_context = f"""
CURRENT DATE AND TIME CONTEXT:
- Today's date: {now.strftime('%A, %B %d, %Y')}
- Current time: {now.strftime('%I:%M %p %Z')}
- ISO format: {now.strftime('%Y-%m-%d %H:%M:%S')}
- Market status: {'Open' if now.weekday() < 5 and 9 <= now.hour < 16 else 'Closed'}

IMPORTANT: Always use the current date and time above for all financial analysis. 
Do NOT use training data cutoff dates or outdated information.
"""
    original_time = (time.perf_counter() - start) * 1000
    
    # Test 2: Optimized version
    start = time.perf_counter()
    for _ in range(1000):
        get_enhanced_agent_instructions_optimized()
    optimized_time = (time.perf_counter() - start) * 1000
    
    print(f"Original version (1000 calls): {original_time:.3f}ms")
    print(f"Optimized version (1000 calls): {optimized_time:.3f}ms")
    print(f"Performance improvement: {((original_time - optimized_time) / original_time * 100):.1f}%")
