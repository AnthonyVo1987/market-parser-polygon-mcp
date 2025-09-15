# New Task Details

## Task Description: Playwright MCP Tools Usage Guide Research & Generation

Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Run LINT & Fix any Lint issues from the requested doc only

Final Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Comprehensive doc review OF JUST REQUESTED DOC ONLY & fix any issues found

Final Task 2: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Ignore the other .md doc file that are being worked on in parallel and JUST commit the requested docs only
- Create single atomic git commit containing ONLY THE requested doc ONLY!!!
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Requested docs to Run LINT, Review, & commit, push, sync:

[docs/MCP_Tools_Usage_Guide/Context7_MCP_Tools_Usage_Guide.md]

###

Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Run LINT & Fix any Lint issues from the new docs/MCP_Tools_Usage_Guide

Final Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Comprehensive doc review OF JUST REQUESTED DOC ONLY & fix any issues found
- DO NOT COMMIT NEW DOCS YET AND WAIT FOR USER REVIEW

Final Task 2: Task Summary Updates for LAST_TASK_SUMMARY.md & CLAUDE.md & New Usaage guide:

- Generate detailed task completion summary & OVERWRITE the doc "LAST_TASK_SUMMARY.md"
- Based on detailed task completion summary, generate high level task completion summary 10 lines MAX for updating CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Ignore the other .md doc file that are being worked on in parallel and JUST commit the requested docs only
- Create single atomic git commit containing ONLY THE RELEVANT changes: CLAUDE.md, LAST_TASK_SUMMARY.md, & JUST the requested doc ONLY!!!
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Requested docs to Run LINT, Review, & commit, push, sync:

- [docs/MCP_Tools_Usage_Guide/Sequential-Thinking_MCP_Tools_Usage_Guide.md]

Perform 2nd Sanity Check Doc review of the new Tools Usage Guide vs Our codebase, and fix any issues if found during the review.

Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

Update the guide for the EACH of the playwright tools with the proper expected testing procedure:

- We have a "per test timeout of 120s", ALL AI Responses on average take between ~30s - 90s, we need to ensure the AI Agents can tell the difference between, starting a test and NOT EXPECTING AN IMMEDIATE RESPONSE WITHIN 5 SECONDS BECAUSE THAT IS TOO EARLY, POLLING EVERY 30s for a response and NOT just polling a single time of 30s, and then the TIMEOUT of 120s.  Need to clarify the proper tool call inputs\outputs to handle this proper test case because there have been improper tool usage that causes false positives where PLaywright tools were used with incorrect inputs, such as timeout of 5s \ 30s, and\or improperly detcting a 30s Polling as a timeout failure when it is polling etc.

Here is the expectation for ALL PLaywright Tool calls:

- AI Agent uses Playwright Tool Call to send an AI message through either Input User Send Prompt and\or Button Prompts
- AI Agents should POLL every 30sec to see if there was a response
- If there was a CORRECT response within that 30sec, AI Agent can then move onto the next test since there was a sucessful response before the max timeout of 120s, so no need to wait the full 120s max timeout if we already got a CORRECT response
- If there was NO CORRECT response during the first 30sec, AI agent just polls every 30sec to see if CORRECT response or not later on
- ONLY if after multiple 30s polling AND we reached max timeout of 120s WITHOUT a CORRECT response, THEN AI Agent can mark as a TRUE Timeout failure

Task 2. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Comprehensive doc review OF JUST THE NEW DOC ONLY, & fix any issues found
- DO NOT COMMIT NEW DOCS YET AND WAIT FOR USER REVIEW

Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Analyze our codebase, then Perform Research & generate a new doc for the requested MCP Tools Usage Guide TARGETED SPECIFICALLY FOR AI Coding Agents to properly utilize the tools for our app development
- The Usage guide needs to be tailored and focused on proper usage of the tools specifically for OUR APP, so that AI Coding Agents know how to properly use the tools for our app, so avoid generic usage since we want specific use guide for our app
- Need to go into details on EACH of the the tools: Correct Cases\Conditions to use the tool, Incorrect Cases\Conditions to use the tool , Correct Tool inputs , Correct expected Tool output, Correct examples of usage, Incorrect examples of usage
- Usage Guide needs to be written that is "straight to the point with less fluff" so that an AI Agent can fully understand the proper tool usage. Too much verbosity and fluff may confuse the AI Agent

Requested MCP Tools: Context7
New Doc Location: "docs/MCP_Tools_Usage_Guide/Context7_MCP_Tools_Usage_Guide.md"

Task 2. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform:

- Comprehensive doc review OF JUST THE NEW DOC ONLY, & fix any issues found
- DO NOT COMMIT NEW DOCS YET AND WAIT FOR USER REVIEW

## Final Task(s) - SPECIALISTS(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to perform Final 4 Tasks

Final Task 1: Review/Fix Loop

- SPECIALISTS performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Optional `mcp__filesystem__*` tools for EFFICIENT file operations and examination
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

## Requirements

## Expected Outcome*

*All Files, Docs atomically commited after all tasks are complete*

## Additional Context
