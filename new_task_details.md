# New Task Details

## Task Description

[DOCS] Playwright Tests & Github Docs Updates

Task 1. Create new folder gpt5-openai-agents-sdk-polygon-mcp/docs/claude_test_reports

Task 2. Update & Enforce project docs that test reports generated for Claude Code Playwright test reports file must follow new naming convention format: "CLAUDE_playwright_mcp_tests_YY-MM-DD_hh-mm.md" - Where Agent must detect real world Date and time to append to the file name in the requested pacific timestamp format

Task 3. Update Playwright MCP test plan and project docs to reflect new testing strategy:

- ALL testing needs an initial but configurable timeout of 120 seconds PER Playwright Test to allow time for AI to generate and send the response.  Some actions will respond quicker than 120s, so we will just start with an initial test command timeout of 120s for now which SHOULD cover most app actions & prompts
- All test plans must capture results and generate a detailed test report with granular test results and save to the new test report folder following the file naming convention for user review
- Modify test plan to make these first 3x Test User Input Prompts the very first ones to run:
- Test Input: Market Status: Low Verbosity, Raw response format output
- Test Input: Single Ticker Snapshot: NVDA, SPY, WDC, Low Verbosity, Raw response format output
- Test Input: Full Market Snapshot: NVDA, SPY, QQQ, IWM, Low Verbosity, Raw response format output
- Research & Addon more test coverage to test every single of the App's functionality at LEAST 1x time

Task 4. Github MCP Tool Removal: Remove all instances in project docs thats says to use GitHub MCP Tools as primary. Standard GIT Commands will now be the Primary, I will remove Github tool support

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Research & Analyze Task 3. Update Playwright MCP test plan and project docs to reflect new testing strategy

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s)

## Implementation Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Perform all of the requested task(s) based on the newly generated implementation plan todo checklist

## Final Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem, Github, & any other relevant Tools to perform Final 4 Tasks

Final Task 1: Review/Fix Loop

- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle WITH LINT until achieving PASSING code review status

Final Task 2: Task Summary & CLAUDE.md Update

- Generate comprehensive task completion summary
- Update CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
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

- DO NOT RUN TEST PLAN YET - FOLLOW ON TASK to be assigned TBD to run initial basic test plan

- I made a mistake and misunderstood github tools. Basically, for local repo operations of day to day workflow tasks, we should actually be using the standard GIT commands and NOT Github MCP server tools.
- Github MCP server tools are more geared towards AI Agents for Automations of Workflows and remote Repo management.
- Because our current project is still prototyping, we do not need the over-engineering of Github MCP Server
- Use standard git commands from now on for all repo managment operations

## Additional Context
