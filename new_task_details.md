# New Task Details

[GPT-5] Cleanup & Consolidate Dupe OpenAI Standalone Migration Guide

## Task Description

There are 2x nearly duplicate and redundant OpenAI Standalone Migration docs that needs to be consolidated into a single OpenAI Standalone Migration Guide

<Research Task 1> Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, Investigate, & perform the following task(s):

- Read & Review the contents of /docs/MIGRATION_GUIDE.md

<Research Task 2> Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, Investigate, & perform the following task(s):

- Read & Review the contents of /gpt5-openai-agents-sdk-polygon-mcp/MIGRATION_GUIDE.md

<Planning Task 3> Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, Investigate, & perform the following task(s):

- Based on analysis from Research Tasks 1 & 2, come up with a plan to consolidate both docs into a single new single source of truth migration doc

<Task 4> Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, Investigate, & perform the following task(s):

- Implement the new single source of truth migration doc plan by creating a brand new doc: "/gpt5-openai-agents-sdk-polygon-mcp/OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md"

<Closing_Tasks> Specialist(s) to use Context7, Sequential-Thinking, Filesystem, Github, & any other relevant Tools to perform 4x Final Steps for: Review\Fix Loop, Task Summary & CLAUDE.md Update, Atomic Github Commit & Github Push, & Final Verification

### Step 1: Review/Fix Loop

- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle until achieving PASSING code review status
- ONLY AFTER A PASSING REVIEW, delete both deprecated older migration docs so we now have a single source of truth doc for the migration

### Step 2: Task Summary & CLAUDE.md Update

- Generate comprehensive task completion summary
- Update CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

### Step 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic Github commit containing ALL changes: code files, documentation updates, and task summary
- Github Push commit to GitHub repository using provided personal access token
- **CRITICAL**: Must Github push to complete the workflow - Github commit without Github push is incomplete

### Step 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly Github committed and Github pushed

**Key Requirements:**

## Requirements

## Expected Outcome

## Additional Context
