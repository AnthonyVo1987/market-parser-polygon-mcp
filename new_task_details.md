# New Task Details

## Task Description

[OpenAI] Pre-migration Docs Prep & Updates: OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md

Task 1. Update OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md with detailed guides & steps how to use either of the projects' currently supported development environments using default Vite and\or Live Server for setting up, running, testing, & debugging

Task 2. Disable the automatic Lighthouse CI Github Workflow for now temporarily because prototyping is still too early to run CI yet

Task 3. REMOVE all references to outdated Scenario B: Architecture Migration & Modernization:
Transform text-based parsing to JSON schema-driven architecture
Migrate from regex extraction to structured data validation
Implement modern API patterns and error handling
Enhance UI with state management and responsive design

Task 4. Comprehensive review of all docs in entire standalone project folder(s) gpt5-openai-agents-sdk-polygon-mcp to ensure up to date and accurate before migration

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Analzye & Research all the requested task(s), reading any docs that could also be relevant
- /gpt5-openai-agents-sdk-polygon-mcp/OPENAI_STANDALONE_APP_MIGRATION_GUIDE.md
- /gpt5-openai-agents-sdk-polygon-mcp/OpenAI_Vite_Optimization_Plan.md
- /gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_USAGE.md
- /gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI/LIVE_SERVER_DOCUMENTATION_TEMPLATES.md

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

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

- Delete previous task(s) details file if it still exists in the project: "/new_task_details_copy.md"

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic Github commit containing ALL changes: code files, documentation updates, and task summary
- Github Push commit to GitHub repository using provided personal access token
- **CRITICAL**: Must Github push to complete the workflow - Github commit without Github push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly Github committed and Github pushed

**Key Requirements:**

## Requirements

- NONE OF THE Apps will migrate to this legacy outdated Scenario B, so need to remove references from all docs to remove confusion for user
- There is only a single Scenario A for the Standalone Migration

- Entire project is still prototyping, so do NOT implement: Enterprise Grade, Production Ready, Performance Optmization, Testing \ Test Scripts
- Do NOT over-engineer
- ALL file\doc changes fully reviewed, fixed, committed, and pushed to the repo

## Additional Context
