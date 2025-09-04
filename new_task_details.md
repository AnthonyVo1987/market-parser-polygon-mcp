# New Task Details

[GPT-5] Pre-Migration Prep for new Github repo for gpt5-openai-agents-sdk-polygon-mcp

- I would like to prep the code base for a full migration to use just the new gpt5-openai-agents-sdk-polygon-mcp CLI & Chat GUI

## Task Description

<Task 1> Specialist to Use Context7, Sequential-Thinking, & and any other relevant Tools Analyze, Research, & Understand the current implementation of gpt5-openai-agents-sdk-polygon-mcp CLI & Chat GUI

<Task 2> Specialist to Use Context7, Sequential-Thinking, & and any other relevant Tools Analyze, Research, & Scope out changes needed to have a fully independent gpt5-openai-agents-sdk-polygon-mcp CLI & Chat GUI to be later imported into a brand new Github repo WITH any legacy CLI + Gradio UI code

<Task 3> Ask @agent-tech-lead-orchestrator to use Sequential-Thinking to analyze results from research tasks 1 & 2 and generate a implemenation, delegation, & coordination plan for Specialist(s) to perform all task(s) for the Pre-Migration Prep code changes

<Task 4> Based implementation, delegation, & coordination plan for Specialist(s), perform all the task(s)

<Task 5> Specialist(s) to review and update ALL gpt5-openai-agents-sdk-polygon-mcp docs to reflect the new Pre-Migration Prep

<Task 6> 4x Steps for: Review\Fix Loop, Task Summary & CLAUDE.md Update, Atomic Git Commit & Push, & Final Verification

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

- Completeley working gpt5-openai-agents-sdk-polygon-mcp CLI + GUI with a brand new fresh repo, completely decoupled and removed from the legacy CLI + Gradio UI code
- End Result is a fresh new project for JUST gpt5-openai-agents-sdk-polygon-mcp CLI + GUI ONLY

1. User will create a brand new fresh Github repo for JUST the gpt5-openai-agents-sdk-polygon-mcp implementation
2. User will then try and import\copy & paste \ cherry pick the entire gpt5-openai-agents-sdk-polygon-mcp folder with the Pre-Migration Prep changes
3. User will then run the environment commands to setup, install dependencies\packages for gpt5-openai-agents-sdk-polygon-mcp
4. User can then issue the command to run the gpt5-openai-agents-sdk-polygon-mcp CLI
5. User can then issue the command to run the gpt5-openai-agents-sdk-polygon-mcp GUI
6. Any tests, lint, and\or project configs will be properly setup to run if needed

## Additional Context
