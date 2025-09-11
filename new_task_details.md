# New Task Details

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

## Task Description

[Consolidated Playwright Test Plan Instructions for CLI & MCP Method]

Task 1. [Specialist] Review Integration Guide: gpt5-openai-agents-sdk-polygon-mcp/docs/PLAYWRIGHT_TESTING_INTEGRATION_GUIDE.md

Task 2. [Specialist] Review testing procedures: gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md

Task 3. [Specialist] Review Full test plan files from gpt5-openai-agents-sdk-polygon-mcp/tests/playwright

Task 4. [Specialist] Review CORRECT Playwright CLI commands (npx playwright test) Methodlogy & Test Results: gpt5-openai-agents-sdk-polygon-mcp/docs/test_reports/playwright_CLI_test_25-09-10_18-30.md

Task 5. [Specialist] Review CORRECT Playwright MCP Tool Methodlogy & Test Results: gpt5-openai-agents-sdk-polygon-mcp/docs/test_reports/playwright_MCP_test_25-09-10_16-35.md

Task 6. [Specialist] Generate a brand new consolidated, single source of truth comprehensive Playwright Testing Plan & Procedure .md doc in gpt5-openai-agents-sdk-polygon-mcp/tests/playwright that will be the ONLY doc needed for AI Agents to read, and properly run tests for EITHER Playwright CLI commands (npx playwright test) Methodlogy OR Playwright MCP Tool Methodlogy.

- The new doc should spell out the entire proper testing procedure that SPELLS out exact testing methodolgy with all the corrective actions and lessons learned
- It should have dedicated sections for Playwright CLI commands (npx playwright test) Methodlogy AND Playwright MCP Tool Methodlogy, that spells out the test plan checklist whenever tests are requested to be run:

Test Plan Checklist for Playwright CLI commands (npx playwright test) Method:

- Perform the test plan by marking off each TODO Test Task:
☐ Kill all existing dev servers for fresh test run
☐ Start fresh backend server (FastAPI)
☐ Start fresh frontend server (Vite)
☐ Verify both servers operational before testing
☐ Execute TEST B001 - Market Status Check using Playwright CLI commands (npx playwright test)
☐ Execute TEST B002 - NVDA Ticker Analysis using Playwright CLI commands (npx playwright test)
☐ Execute TEST B003 - SPY Ticker Analysis using Playwright CLI commands (npx playwright test)
☐ Execute TEST B004 - GME Ticker Analysis using Playwright CLI commands (npx playwright test)
☐ Execute TEST B005 - Multi-Ticker Analysis using Playwright CLI commands (npx playwright test)
☐ Execute TEST B006 - Empty Message Handling using Playwright CLI commands (npx playwright test)
☐ Execute TEST B007 - Stock Snapshot Button using Playwright CLI commands (npx playwright test)
☐ Execute TEST B008 - Support Resistance Button using Playwright CLI commands (npx playwright test)
☐ Execute TEST B009 - Technical Analysis Button using Playwright CLI commands (npx playwright test)
☐ Execute TEST B010 - Multi-Button Interaction using Playwright CLI commands (npx playwright test)
☐ Execute TEST B011 - Button State Validation using Playwright CLI commands (npx playwright test)
☐ Execute TEST B012 - Button Error Handling using Playwright CLI commands (npx playwright test)
☐ Execute TEST B013 - Button Performance Validation using Playwright CLI commands (npx playwright test)
☐ Execute TEST B014 - Button Accessibility using Playwright CLI commands (npx playwright test)
☐ Execute TEST B015 - Button UI Consistency using Playwright CLI commands (npx playwright test)
☐ Execute TEST B016 - Button Integration using Playwright CLI commands (npx playwright test)
☐ CRITICAL: Verify 16/16 test coverage completed AND verify that B001-B016 requirements were ran and NOT custom tests
☐ Use @documentation-specialist to generate comprehensive test report

Test Plan Checklist for Playwright MCP Tools Method:

- Perform the test plan by marking off each TODO Test Task:
☐ Kill all existing dev servers for fresh test run
☐ Start fresh backend server (FastAPI)
☐ Start fresh frontend server (Vite)
☐ Verify both servers operational before testing
☐ Execute TEST B001 - Market Status Check using Playwright MCP Tools Method
☐ Execute TEST B002 - NVDA Ticker Analysis using Playwright MCP Tools Method
☐ Execute TEST B003 - SPY Ticker Analysis using Playwright MCP Tools Method
☐ Execute TEST B004 - GME Ticker Analysis using Playwright MCP Tools Method
☐ Execute TEST B005 - Multi-Ticker Analysis using Playwright MCP Tools Method
☐ Execute TEST B006 - Empty Message Handling using Playwright MCP Tools Method
☐ Execute TEST B007 - Stock Snapshot Button using Playwright MCP Tools Method
☐ Execute TEST B008 - Support Resistance Button using Playwright MCP Tools Method
☐ Execute TEST B009 - Technical Analysis Button using Playwright MCP Tools Method
☐ Execute TEST B010 - Multi-Button Interaction using Playwright MCP Tools Method
☐ Execute TEST B011 - Button State Validation using Playwright MCP Tools Method
☐ Execute TEST B012 - Button Error Handling using Playwright MCP Tools Method
☐ Execute TEST B013 - Button Performance Validation using Playwright MCP Tools Method
☐ Execute TEST B014 - Button Accessibility using Playwright MCP Tools Method
☐ Execute TEST B015 - Button UI Consistency using Playwright MCP Tools Method
☐ Execute TEST B016 - Button Integration using Playwright MCP Tools Method
☐ CRITICAL: Verify 16/16 test coverage completed AND verify that B001-B016 requirements were ran and NOT custom tests
☐ Use @documentation-specialist to generate comprehensive test report

Task 7. Add documentation steps to handle test report format rules:

ONLY After all tests have completed running for FULL test coverage, use @agent-documentation-specialist to generate a fully detailed granular test report with the following requirements:

1. Match same reporting style from playwright_CLI_test_25-09-10_18-30.md / playwright_MCP_test_25-09-10_16-35.md
2. Include ALL testing requirments, such as the 120s timeout PER test, 30sec polling etc, execution time etc
3. Include any details if dev server ports\address needed the dynamic adjustment for a proper run
4. EACH Test needs to have it's own "mini-dedicated section\module report" to add more granular details during that specific test's execution run & also include the specific test file names\file locations for EACH test
5. Detect the current REAL world date and Pacific timestamp for the report file name *I.E. YY-MM-DD_hh-mm.md: 25-09-10_13-45 for Sept 10, 2025 at 1:45 PM Pacific etc*
6. Report file name should now be saved in a new standardized report name format, depending if Playwright MCP and\or Playwright CLI method was used to the the tests: "playwright_MCP_test_YY-MM-DD_hh-mm.md" vs "playwright_CLI_test_YY-MM-DD_hh-mm.md"
7. Save test report to gpt5-openai-agents-sdk-polygon-mcp/docs/test_reports
8. ONLY A SINGLE test report .md doc is needed - every test run will only have a single source of truth for the entire test execution run and test results in the same doc

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s):

Task 5. [Specialist] Based on all research, analysis, & investigation, fix all the issues

## Implementation Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Based on all the research & newly generated implementation plan task breakdown todo checklist:

## Testing Task(s) - Specialist(s) to use Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

## Final Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to perform Final 4 Tasks

Final Task 1: Review/Fix Loop

- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle WITH LINT until achieving PASSING code review status

Final Task 2: Task Summary Updates for LAST_TASK_SUMMARY.md & CLAUDE.md

- Generate detailed task completion summary & OVERWRITE the doc "LAST_TASK_SUMMARY.md"
- Based on detailed task completion summary, generate high level task completion summary 20 lines MAX for updating CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic git commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, test reports, task summary etc
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**
*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

## Requirements

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

## Expected Outcome*

- Both Playwright CLI commands (npx playwright test) & Playwright MCP Tools Method will run the EXACT SAME MATCHING TESTS with the only difference being the methodology
- NO SEPARATE TESTS PLANS FOR Playwright CLI commands (npx playwright test) VS Playwright MCP Tools Method

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

- All code fixes, doc updates, 1x single test report saved in correct location with correct naming format playwright_MCP_test_YY-MM-DD_hh-mm.md, and everything is committed and pushed atomically

## Additional Context

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*
