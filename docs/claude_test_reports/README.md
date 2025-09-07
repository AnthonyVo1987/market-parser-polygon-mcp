# Claude Test Reports Directory

## Overview
This directory contains comprehensive test reports generated during Playwright MCP testing sessions. All reports follow standardized formatting and Pacific timezone naming conventions.

## Naming Convention
**Format**: `CLAUDE_playwright_mcp_tests_YY-MM-DD_hh-mm.md`
**Timezone**: Pacific Standard Time (PST) / Pacific Daylight Time (PDT)

### Example Filenames
- `CLAUDE_playwright_mcp_tests_25-01-15_14-30.md` (January 15, 2025 at 2:30 PM PT)
- `CLAUDE_playwright_mcp_tests_25-01-15_09-45.md` (January 15, 2025 at 9:45 AM PT)

## Report Structure
Each test report contains:
1. **High-Level Summary Section** - Executive overview and priority test results
2. **Suggested Next Actions Section** - Recommended immediate actions and investigations
3. **Detailed Granular Test Results Section** - Comprehensive test-by-test analysis

## Test Categories Covered
- **Priority Tests** (3 tests) - MUST PASS before comprehensive testing
- **Template Button Interactions** (8 tests)
- **Message Input Variations** (6 tests)
- **Export Functionality** (5 tests)  
- **Responsive Design** (4 tests)
- **Backend API Integration** (7 tests)
- **Error Handling** (6 tests)
- **Performance Validation** (4 tests)
- **Accessibility Testing** (5 tests)
- **Cross-Browser Compatibility** (3 tests)

**Total**: 51 tests (3 priority + 48 comprehensive)

## Usage Instructions

### For Test Execution
1. Run priority tests FIRST using the sequences defined in the Playwright testing guide
2. Only proceed to comprehensive testing after ALL priority tests pass
3. Generate reports using Pacific timezone naming convention
4. Store all reports in this directory

### For Report Analysis
1. Always review High-Level Summary first for critical issues
2. Check Suggested Next Actions for immediate follow-up items
3. Dive into Detailed Results for specific test failures
4. Use reports to track testing progress over time

## Report Template
See `TEMPLATE_playwright_mcp_test_report.md` for the standardized report format that should be used for all test executions.

## Integration with Testing Framework
This directory is referenced in:
- `/gpt5-openai-agents-sdk-polygon-mcp/docs/PLAYWRIGHT_TESTING_INTEGRATION_GUIDE.md`
- Priority test execution sequences
- Comprehensive test coverage documentation

All test reports should be generated automatically during MCP test execution and stored here for analysis and tracking.