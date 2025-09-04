# New Task Details

[GPT-5] Add Chat Buttons for Save & Copy to .md & JSON format

## Task Description

Add .md & JSON format Save & Copy to Clipboard Chat Buttons for the OpenAI GPT-5 Chat UI code

Task 1. Perform Research & generate a plan to implement 4x new buttons to the OpenAI GPT-5 Chat UI code that can Save and\or Copy to clipboard the entire contents of the OpenAI GPT-5 Chat

- Copy to Clipboard .md format Button
- Copy to Clipboard .json format Button
- Save to .md format file Button
- Save to .json format file Button

Task 2. Based on the research & plan from Task 1, implement the plan

## Requirements

## Expected Outcome

## Additional Context

## MANDATORY POST-TASK ACTIONS

After completing the primary task execution, the following 4-step procedure MUST be executed to ensure production readiness and quality assurance:

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
