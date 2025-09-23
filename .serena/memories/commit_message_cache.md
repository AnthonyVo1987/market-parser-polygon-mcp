feat: Remove responseTime usage from test files (Phase 4 implementation)

- Remove responseTime calculations from all MCP test files
- Update priority_tests.js, comprehensive_tests.js, remaining_comprehensive_tests.js
- Update test_framework.js and mcp_test_runner.js report generation
- Update performance_accessibility_browser_tests.js performance metrics
- Remove responseTime references from Playwright test documentation
- Update test execution guides and MCP test script documentation
- Maintain test functionality while removing responseTime dependencies
- Align with CLI/GUI performance optimization goals

Files modified:
- tests/mcp/priority_tests.js
- tests/mcp/comprehensive_tests.js  
- tests/mcp/remaining_comprehensive_tests.js
- tests/mcp/test_framework.js
- tests/mcp/mcp_test_runner.js
- tests/mcp/performance_accessibility_browser_tests.js
- tests/playwright/UI_complete_test_execution_guide.md
- tests/playwright/complete_test_execution_guide.md
- tests/playwright/mcp_test_script_basic.md
- new_task_details.md