"""Agent management for the Market Parser application."""

from agents import Agent, ModelSettings
from agents.mcp import MCPServerStdio
from openai.types.shared import Reasoning

from ..config import settings
from ..utils.datetime_utils import get_current_datetime_context


def get_enhanced_agent_instructions():
    """
    Generate enhanced agent instructions for financial analysis.

    Returns:
        Enhanced agent instructions string
    """
    datetime_context = get_current_datetime_context()
    return f"""You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Use Polygon.io MCP server for live market data, prices, and financial information.
🔴 CRITICAL: YOU MUST ONLY USE THE FOLLOWING 9 SUPPORTED TOOLS: [get_snapshot_ticker, get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg, get_market_status, list_ticker_news] 🔴
🔴 CRITICAL: YOU MUST NOT USE ANY OTHER TOOLS. 🔴

📋 TOOL GUIDANCE FOR COMMON SCENARIOS:
🎯 SINGLE Stock Ticker Real-Time Price, Data, Quotes, Snapshots, etc:
   → USE: get_snapshot_ticker() tool
   → DO NOT USE: get_snapshot_all() for single tickers

🎯 MULTIPLE Stock Tickers Real-Time Price, Data, Quotes, Snapshots, etc:
   → USE: get_snapshot_all() tool (supports multiple tickers in one call)
   → DO NOT USE: get_snapshot_ticker() multiple times for multiple tickers

🎯 SINGLE OPTIONS Ticker Real-Time Price, Data, Quotes, Snapshots, etc:
   → USE: get_snapshot_option() tool
   → DO NOT USE: get_snapshot_ticker() for options

🎯 Market Status, Hours, Open/Closed Status:
   → USE: get_market_status() tool

🎯 Historical Data, Aggregates, OHLC Data:
   → USE: get_aggs(), get_daily_open_close_agg(), get_previous_close_agg() tools

🎯 News Data for Tickers:
   → USE: list_ticker_news() tool

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using ONLY the 10 allowed tools above
3. ALWAYS check the tool guidance above before making tool calls
4. Structure responses: Format data in bullet point format with 2 decimal points max
5. Include ticker symbols
6. Respond quickly with minimal tool calls
7. Keep responses concise - avoid unnecessary details
8. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations"""


def get_optimized_model_settings():
    """Get optimized ModelSettings for GPT-5 financial analysis.

    Returns:
        ModelSettings: Optimized configuration for GPT-5 models with token usage tracking
    """
    return ModelSettings(
        reasoning=Reasoning(effort="low"),
        verbosity="low",
        max_tokens=128000,
        include_usage=True,  # Enable official token usage tracking
        extra_args={"service_tier": "flex", "user": "financial_analysis_agent"},
    )


def create_agent(mcp_server: MCPServerStdio):
    """Create a financial analysis agent with optimized GPT-5 configuration.

    Args:
        mcp_server (MCPServerStdio): The MCP server instance to use

    Returns:
        Agent: The financial analysis agent with optimized settings
    """
    analysis_agent = Agent(
        name="Financial Analysis Agent",
        instructions=get_enhanced_agent_instructions(),
        tools=[],  # Removed save_analysis_report - superseded by GUI Copy/Export buttons
        mcp_servers=[mcp_server],
        model=settings.default_active_model,
        model_settings=get_optimized_model_settings(),
    )

    return analysis_agent
