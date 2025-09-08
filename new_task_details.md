# New Task Details

## Task Description

[TEST] Re-run Incorrect Playwright MCP Test Plan & Fix Issues

Task 1. Fix Incorrect Playwright MCP Report dupes and formatting:

- There are MULTIPLE dupe Test reports for no rhyme or reason - There should only be a single report that is the "final report"
- Remove all extra reports this is a violation
- Here is the expected flow: Requested to run Test plan, Generate brand new CLAUDE_playwright_mcp_tests_xxx.md, update new doc as the test plan run, and once test plan finshes, clean up and finalize the report
- End results is a single report per full test plan run

Task 2. Fix incorrect Playwright MCP Test Plan

- Current MCP Test plan and results are completly invalidated because you incorrectly did NOT enforce 120 second timeout. The first 3x inital test are using a stupid ass 5 second timeout for some riduculous reeason when I already stressed Ai responses always need UP to 120 seconds. So some of the failures in the report are BOGUS and false positives
- ENSURE all test provide AT LEAST 120 seconds to respond

Task 3. Re-Run the FIXED corrected proper 120sec timeout FULL test plan AGAIN with the proper reporting docs. DO NOT FIX any issues on your own

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Research & Analyze testing task(s) by FIRST reading project reference guide docs, and then ONLY if further details needed use Context7, and then finally ONLY if more details needed, Web Search\Fetch last

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

- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever

## Additional Context
