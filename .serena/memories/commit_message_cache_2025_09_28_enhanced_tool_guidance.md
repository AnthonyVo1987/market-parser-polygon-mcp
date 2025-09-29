feat: implement enhanced tool guidance architecture with scenario-based tool selection

- Add comprehensive tool guidance for common financial data scenarios in agent_service.py
- Restrict AI agent to 10 specific Polygon MCP tools with explicit tool selection guidance
- Implement scenario-based tool recommendations (single vs multiple tickers, options, etc.)
- Add tool guidance for optimal API usage patterns and performance optimization
- Update agent instructions with clear tool selection logic and usage examples
- Eliminate MCP Proxy dependency issues with client-side tool filtering approach
- Add comprehensive testing validation with 100% test success rate (7/7 tests passed)
- Create detailed Serena memories for enhanced tool guidance architecture
- Update project documentation with new tool guidance implementation details
- Add test reports showing improved performance (21-44s response times)
- Remove outdated TODO_task_plan.md and update new_task_plan.md with current tasks

BREAKING CHANGE: AI agent now restricted to 10 specific tools with mandatory tool guidance
PERFORMANCE: Multi-ticker queries now use single get_snapshot_all() call vs multiple individual calls
TESTING: All 7 comprehensive tests passing with enhanced tool selection validation