# New Task Details

## Task Description

[OpenAI] Review & Finish Progress of Previously Interrupted Task: Update OpenAI_Vite_Optimization_Plan.md with Deep Dive Enhancements

- You were previously in the middle of a task but you got interrupted and crashed
- This task is to review the previous progress and finished the previous task

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Read & Review the previous task details that were copied to "/new_task_details_copy.md"
- Read & Review the potentially partially updated doc from the previous task "OpenAI_Vite_Optimization_Plan.md"

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Based on the research task, generate a plan to review, analyze, & fully complete any remaining items from the previous task(s)

## Implementation Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Follow the newly generated implementation plan to update the OpenAI_Vite_Optimization_Plan.md

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

- Entire project is still prototyping, so do NOT implement: Enterprise Grade, Production Ready, Performance Optmization, Testing \ Test Scripts
- Do NOT over-engineer
- ALL file\doc changes fully reviewed, fixed, committed, and pushed to the repo

## Additional Context