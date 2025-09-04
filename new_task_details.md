# New Task Details

[GPT-5] Run LINT \ PyLint \ ESLint & fix any Lint issues for gpt5-openai-agents-sdk-polygon-mcp

## Task Description

<Task 1> Specialist to Use relevant MCP Tools to run & fix all the Linting for the code in gpt5-openai-agents-sdk-polygon-mcp

- Lint needs to be run for the entire tech stack of the OpenAI Code
- If something needs additional Lint config to properly run lint, then auto download\setup what may be needed to run Lint properly

<Task 2> 4x Steps for: Review\Fix Loop, Task Summary & CLAUDE.md Update, Atomic Git Commit & Push, & Final Verification

### Step 1: Review/Fix Loop

- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle until achieving PASSING code review status

### Step 2: Task Summary & CLAUDE.md Update

- Generate comprehensive task completion summary
- Update CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

### Step 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic commit containing ALL changes: code files, documentation updates, and task summary
- Push commit to GitHub repository using provided personal access token
- **CRITICAL**: Must push to complete the workflow - commit without push is incomplete

### Step 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly committed and pushed

**Key Requirements:**

- Single atomic commit prevents code vs documentation separation
- All changes (code + docs + summary) must be committed together
- Task summary generation occurs BEFORE git commit to ensure inclusion
- Automated workflow ensures consistency and completeness

## Requirements

## Expected Outcome

- All lint issues fixed for our OpenAI Tech Stack

## Additional Context
