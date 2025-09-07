# New Task Details

## Task Description

[TEST] Fix Playwright Commit Violations

Task 1. Update Playwright MCP test plan in PLAYWRIGHT_TESTING_INTEGRATION_GUIDE.md and project docs to reflect new testing strategy below:
A. ALL testing needs an initial but configurable timeout of 120 seconds PER Playwright Test to allow time for AI to generate and send the response.  Some actions will respond quicker than 120s, so we will just start with an initial test command timeout of 120s for now which SHOULD cover most app actions & prompts.  Remove\fix ANY timeouts lower then 120s
B. All test plans must capture results and generate a detailed test report with granular test results and save to the new test report folder following the file naming convention for user review
C. Modify test plan to make these FIRST 3x Test User Input Prompts the very first ones to run:

- Test Input: Market Status: Low Verbosity, Raw response format output
- Test Input: Single Ticker Snapshot: NVDA, SPY, WDC, Low Verbosity, Raw response format output
- Test Input: Full Market Snapshot: NVDA, SPY, QQQ, IWM, Low Verbosity, Raw response format output
D. After the first 3x initial test, Research & Addon more test coverage to test every single of the App's functionality at LEAST 1x time

Task 2. Perform a "dry run" ONLY of updated intial Playwright Comprehensive MCP Test Plan. AFTER EACH Test Plan Module, Record\Update test report .md so that we can capture the test data & details immediately after a finished Test for efficient Cache Token usage.

Task 3. Finalize Test report with an initial High Level Summary section of the test results, a section for suggested next actions\investigations, and then finally the fully detailed granular test results and details.  DO NOT ATTEMPT TO DEBUG\FIX ISSUES flagged from report YET, because user needs to review ALL test reports

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Research & Analyze testing task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last:
Research Task 1. Playwright MCP test plan in PLAYWRIGHT_TESTING_INTEGRATION_GUIDE.md and project docs to reflect new testing strategy below:
A. ALL testing needs an initial but configurable timeout of 120 seconds PER Playwright Test to allow time for AI to generate and send the response.  Some actions will respond quicker than 120s, so we will just start with an initial test command timeout of 120s for now which SHOULD cover most app actions & prompts. Remove\fix ANY timeouts lower then 120s
B. All test plans must capture results and generate a detailed test report with granular test results and save to the new test report folder following the file naming convention for user review
C. Modify test plan to make these FIRST 3x Test User Input Prompts the very first ones to run:
- Test Input: Market Status: Low Verbosity, Raw response format output
- Test Input: Single Ticker Snapshot: NVDA, SPY, WDC, Low Verbosity, Raw response format output
- Test Input: Full Market Snapshot: NVDA, SPY, QQQ, IWM, Low Verbosity, Raw response format output
D. After the first 3x initial test, Research & Addon more test coverage to test every single of the App's functionality at LEAST 1x time

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

- Generate detailed task completion summary & OVERWRITE LAST_TASK_SUMMARY.md
- Based on detailed task completion summary, generate high level task completion summary & Update CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic git commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, task summary
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome

PLAYWRIGHT_TESTING_INTEGRATION_GUIDE.md Updated with Playwright MCP test plan to reflect new testing strategy below:
A. ALL testing needs an initial but configurable timeout of 120 seconds PER Playwright Test to allow time for AI to generate and send the response.  Some actions will respond quicker than 120s, so we will just start with an initial test command timeout of 120s for now which SHOULD cover most app actions & prompts.  Remove\fix ANY timeouts lower then 120s
B. All test plans must capture results and generate a detailed test report with granular test results and save to the new test report folder following the file naming convention for user review
C. Modify test plan to make these FIRST 3x Test User Input Prompts the very first ones to run:

- Test Input: Market Status: Low Verbosity, Raw response format output
- Test Input: Single Ticker Snapshot: NVDA, SPY, WDC, Low Verbosity, Raw response format output
- Test Input: Full Market Snapshot: NVDA, SPY, QQQ, IWM, Low Verbosity, Raw response format output
D. After the first 3x initial test, Research & Addon more test coverage to test every single of the App's functionality at LEAST 1x time

## Additional Context
