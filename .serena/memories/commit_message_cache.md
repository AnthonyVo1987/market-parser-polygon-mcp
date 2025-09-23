fix: Restore MCP server integration with dynamic agent creation

🔧 MCP Integration Fixes:
- Restore dynamic agent creation in chat_endpoint with mcp_servers=[shared_mcp_server]
- Fix Runner.run call to use session=shared_session instead of context=context
- Initialize result variable to prevent "referenced before assignment" error
- Update cli_async function with same dynamic agent pattern
- Add openai-agents-mcp>=0.0.8 dependency to pyproject.toml

📊 Functionality Restored:
- Polygon MCP tools now accessible to AI agent (confirmed with AAPL query)
- Real-time market data integration working correctly
- Persistent MCP server state maintained through FastAPI lifespan
- Both CLI and API endpoints using proper MCP server integration

✅ Testing Results:
- AAPL query returned real market data: $256.08 current price
- MCP server initialization and shutdown working properly
- No more "referenced before assignment" errors

Files Modified:
- src/backend/main.py (MCP integration fixes)
- pyproject.toml (added openai-agents-mcp dependency)
- new_task_plan.md (updated task details)

Status: MCP server integration fully restored and working