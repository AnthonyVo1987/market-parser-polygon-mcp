# New Task Details

## Task Description

[TEST] FIX AGAIN Incorrect Playwright MCP Test Plan

- Your last commit of test plan changes are STILL incorrect and not what I want from Commit 'd5875d0dc7ad667e61c4ad1484f8cd6ea7666a56'
- THERE IS NO ENFORCEMENT OF JSON OUTPUT only so you completely made up a requirement
- RAW OUTPUT FORMAT, LOW\NO VERBOSITY DOES NOT MEAN JSON ONLY. EMOJIS ARE ALLOWED
- docs/claude_test_reports/CLAUDE_playwright_mcp_corrected_test_specifications.md

A. Here are the new updated priority test prompts to use and replace the current incorrect test::

1. "Market Status: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
2. "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
3. "Single Ticker Snapshot: SPY, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
4. "Single Ticker Snapshot: GME, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
5. "Full Market Snapshot with multiple Tickers: NVDA, SPY, QQQ, IWM: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"

B. Fix the rest of the entire test plan to ENFORCE BASIC FUNCTIONALITY TESTING ONLY AND PROMPTS SHOULD BE STRAIGHT FORWARD with low\no verbosity only, NOT JSON ONLY output, Emoji allowed

- EVERY single test MUST include these instructions in the test to unify a common practice: PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity
- REMOVE ALL OUTPUT FORMAT EXAMPLES SHOWING EXPECTED OUTPUT OF JSON ONLY BECAUSE THAT IS NOT WHAT I WANT
- multiple test files need to be updated

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Research & Analyze task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

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

- DO NOT RUN TESTS - THIS IS PURELY UPDATING AND FIXING TEST PLAN DOCS
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever

## Additional Context
