# New Task Details

## Task Description

[TEST] Fix Incorrect Playwrite MCP Timeout Procedure & Update Timeouts back down to 120s

Task A. Convert the MCP Polygon Timeout to a more visible config type variable\setting so that it is more obvious to change this timeout, because right now it is buried beneath the code and not obvious how to change it. Update timeout back down to 120s from now on since we profiled and 180s is too long since we found out that it was a testing issue and a timeout of 120s is more reasonable

- market-parser-polygon-mcp/gpt5-openai-agents-sdk-polygon-mcp/src/main.py- create_polygon_mcp_server()

Task B. Update CLAUDE_playwright_mcp_corrected_test_specifications.md Priority Test(s)

- Reduce the Priority Tests to JUST have these 3x quick tests:

1. Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity
2. Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity
3. Full Market Snapshot with multiple Tickers: SPY, QQQ, IWM: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity

- Move the 8x Button test TEST-P006: Snapshot Button Response Time - TEST-P013: Button Visual Feedback back out of priority.  End result is priority test is just 3x test for now since there are lingering issues with button test that will will fix later on TBD

 Task C. Update CLAUDE_playwright_mcp_corrected_test_specifications.md with updated corrected actions Test Plan Procedures:

- New 120s timeout enforcement for ALL test
- New proper 30s polling and proper timeout detection and timer restart\stop for each test
- ENTIRE comprhensive test plan suite needs to be updated with the correct testing procedure to prevent false positive triggers

Task D. Migrate entire market-parser-polygon-mcp/docs/claude_test_reports to proper folder underneath OpenAI docs folder

- gpt5-openai-agents-sdk-polygon-mcp/docs is the proper folder

Task E. Update ALL relevant project docs with the udpated & corrected new testing methodology

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last
- market-parser-polygon-mcp/docs/claude_test_reports/CLAUDE_playwright_mcp_corrected_test_specifications.md

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s)

## Implementation Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Perform all of the requested task(s) based on the newly generated implementation plan todo checklist

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

## Requirements

## Expected Outcome

- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever

## Additional Context
