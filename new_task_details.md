# New Task Details

## Task Description

[DOCS] Update Test Plans & Add Custom Test Commands

- DOCUMENTATION TASK(S) ONLY

1. Rename references from "Priority Tests" to "Basic Tests" in  CLAUDE_playwright_mcp_corrected_test_specifications.md

2. Update  CLAUDE_playwright_mcp_corrected_test_specifications.md so that Basic Tests now will have the current 5x test(s):
TEST-P001: Market Status Request
TEST-P002: Single Ticker NVDA Request
TEST-P003: Single Ticker SPY Request
TEST-P004: Single Ticker GME Request
TEST-P005: Multi-Ticker Combined Request

3. Remove Sections for Performance Validation Tests & Complex Query Tests since those tests are actually just Basic test in CLAUDE_playwright_mcp_corrected_test_specifications.md

4. Update ALL docs, especially CLAUDE_playwright_mcp_corrected_test_specifications.md, that references ANY hard coded # of Basic Tests, and Test numbers.  We will constantly modify, add, remove, update, re-classify tests, so we need to remove all potential points of confusion that are hard coded.

- By removing all HARD CODED test #s and Test IDs, future testing can be dynamic such as running JUST Basic Tests, Button Prompt tests etc
- By removing hard code, it allows flexibililty for tests to be constantly modified, added, removed, updated, re-classifed WITHOUT needing to update the hard codes in the test plan
- I.E Running basic test now has 5 x test, but later on it can expand to 20x test, so running basic test again will know to run the full 20x test without need to provide explicit number of tests and\or test ID
- I.E. Running Basic & Button Prompts test will run all exising Basic tests AND all existing Button Prompt tests, without needing to modify any hard codes.

5. Add brand new Claude Code Custom Slash Commands to trigger some test runs:

- Read & Review how to properly create new Slash Commands from: docs/Custom_Slash_Commands.md
- Review and read how the current "new_task.md" command works when user invokes /new_task, to get an idea of how to make sure @agent-tech-lead-orchestrator only orchestrates and delegatges the testing to appropriate specialist(s)
- EACH of the following 3x new test commands need to follow the same procedure: @agent-tech-lead-orchestrator to be invoked to delegate Specialist(s) to USE all relevant MCP Tools and: ENFORCE THAT SPECIALIST CANNOT MAKE UP THEIR OWN TESTS, and if they do not know what test to run, then re-read  CLAUDE_playwright_mcp_corrected_test_specifications.md if needed on the proper test plan, FIRST Read gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md, THEN follow the mandatory server setups, THEN Run the requested Test(s) following Testing Procedures outlined in the doc, git commit & push test report docs to repo WITHOUT trying to fix anything.

Here are the new run test custom commands we are adding:
A. /run_test_basic = Run JUST the Basic Tests
B. /run_test_basic_button = Run JUST the Basic & Button Prompt Tests
C. /run_test_button = Run JUST the Button Prompt Tests

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
- CLAUDE_playwright_mcp_corrected_test_specifications.md only references Basic Tests, No hardcoded test numbers and\or test IDs, no more Performance Validation Tests & Complex Query Tests
- No other docs ever referencing hard coded test numbers or test IDs
- No more references ANYWHERE about "priority tests" label since we changed it to Basic Test Label.  DO NOT REMOVE "PRIORITY" from the chat prompts itself since the PROMPTS are priority, but they are still basic tests
- 3x new custom slash commands stored in .claude/commands for:
A. /run_test_basic = Run JUST the Basic Tests
B. /run_test_basic_button = Run JUST the Basic & Button Prompt Tests
C. /run_test_button = Run JUST the Button Prompt Tests

## Additional Context
