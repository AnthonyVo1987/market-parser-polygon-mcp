# New Task Details

## Task Description

[TEST] Run The 6x Basic Test Suite

- Re-run the same 6x tests with some modifications: Adjust the test prompts to now enforce "raw JSON Output format, no verbosity, no emojis"
- Save results to new report

- Read this doc to understand the Playwright MCP Testing Procedure gpt5-openai-agents-sdk-polygon-mcp/docs/test_specifications/CLAUDE_playwright_mcp_corrected_test_specifications.md
- Read this doc to understand the 8x basic tests & reporting format: gpt5-openai-agents-sdk-polygon-mcp/docs/test_reports/playwright_mcp_dynamic_port_validation_report_2025-01-09.md

## Research Task(s) - Use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- USE ALL MANDATED MCP TOOLS to Read & Understand the Method 3: Hybrid GitHub MCP + Git Workflow from OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md

## Planning Task(s) - Use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- IF RESEARCH FROM Tasks were NOT performed, this is a VIOLATION and task must be restarted from the beginning
- Based on the research task(s), USE SEQUENTIAL-THINKING AND ALL MANDATED MCP TOOLS generate fully detailed, granular, implementation plan task breakdown todo checklist to complete all the requested task(s) to migrate using Method 3: Hybrid GitHub MCP + Git Workflow from OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md

## Implementation Task(s) - Use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Perform all of the requested task(s) based on the newly generated implementation plan todo checklist
- STOP AFTER new repo has been fully cloned to local user folder so user can review the new repo if it is ready or not
- There will be additional add-on task to perform more setup, installation, cli run\test, gui run\test, but for now, we will checkpoint after repo is pushed and cloned to perform the migration in phases

## Final Task(s) - Use to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to perform Final 3 Tasks

Final Task 1: Review/Fix Loop

- Perform comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle WITH LINT until achieving PASSING code review status

Final Task 2: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic git commit containing ALL changes: code files, docs etc
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 3: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome

- New Github repo created with new name, and gpt5-openai-agents-sdk-polygon-mcp OpenAI CLI & REACT GUI migrated and committed  and pushed to new repo, and then new repo cloned to local folder that user created
- There will be additional add-on task to perform more setup, installation, cli run\test, gui run\test, but for now, we will checkpoint after repo is pushed and cloned

## Additional Context
