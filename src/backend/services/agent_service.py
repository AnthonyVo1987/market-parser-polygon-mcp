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
🔴 CRITICAL: YOU MUST NOT USE THE FOLLOWING UNSUPPORTED TOOLS: [list_trades, get_last_trade, list_quotes, get_last_quote] 🔴

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: Format data in bullet point format with 2 decimal points max
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details
7. Do NOT provide any of the following UNLESS SPECIFICALLY REQUESTED: analysis, key takeways, actionable recommendations"""


def get_optimized_model_settings():
    """Get optimized ModelSettings for GPT-5 financial analysis.

    Returns:
        ModelSettings: Optimized configuration for GPT-5 models
    """
    return ModelSettings(
        reasoning=Reasoning(effort="low"),
        verbosity="low",
        max_tokens=128000,
        extra_args={
            "service_tier": "flex",
            "user": "financial_analysis_agent"
        }
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
        model=settings.available_models[0],
        model_settings=get_optimized_model_settings(),
    )

    return analysis_agent
