# New Task Details

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

## Task Description

[PLAYWRIGHT] Integrate Playwright CLI Testing into OpenAI Codebase

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- incorrect assumption that MCP tools could only be called through Claude's interface - ALL TOOLS can be called so pure PLaywright CLI is feasible

*ALL TASKS MUST BE PERFORMED WITH MCP TOOLS*

- Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

1. Read doc to understand the Playwright CLI Integration: gpt5-openai-agents-sdk-polygon-mcp/docs/PLAYWRIGHT_TESTING_INTEGRATION_GUIDE.md
2. Read doc to understand the Playwright MCP Testing Procedure & Playwright CLI Integration: gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md
3. Read doc to understand the 6x basic tests & reporting format for the new CLI Integration: gpt5-openai-agents-sdk-polygon-mcp/docs/test_reports/playwright_mcp_dynamic_port_validation_report_2025-01-09.md
4. Use Sequential-Thinking, Context7 Tools, and any other tools to research how to integrate PlayWright CLI Testing into our OpenAI codebase based on research
5. Use Sequential-Thinking, Context7 Tools, and any other tools to research how to create initial Playwright CLI Basic Test scripts to run the 6x Basic Tests from playwright_mcp_dynamic_port_validation_report_2025-01-09.md

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

*ALL TASKS MUST BE PERFORMED WITH MCP TOOLS*

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s)

## Implementation Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

*ALL TASKS MUST BE PERFORMED WITH MCP TOOLS*

- Based on all the research & newly generated implementation plan task breakdown todo checklist:

6. Integrate Playwright CLI Testing
7. Generate initial Playwright CLI Test Script for 6x Basic Test from playwright_mcp_dynamic_port_validation_report_2025-01-09.md
8. Run new CLI 6x Basic Tests, fixing any issues in test scripts, & saving report based on same format of playwright_mcp_dynamic_port_validation_report_2025-01-09.md

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
- Create single atomic git commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, task summary
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

*ALL TASKS MUST BE PERFORMED WITH MCP TOOLS*

## Expected Outcome*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*

- All 6/6 tests PASSED with same results to the baseline gpt5-openai-agents-sdk-polygon-mcp/docs/test_reports/playwright_mcp_dynamic_port_validation_report_2025-01-09.md
- All code fixes, doc updates, test reports, and 6/6 test ALL PASS and everything is committed and pushed atomically

## Additional Context

*IF IN PLAN MODE, MAIN AGENT MUST USE @agent-tech-lead-orchestrator to generate initial plan WITH AI Specialists Delegation & Coordination assignments; a Plan WITH any Specialists from @agent-tech-lead-orchestrator is an IMMEDIATE TASK VIOLATION AND TASK MUST BE ABORTED FOR NON COMPLIANCE*
