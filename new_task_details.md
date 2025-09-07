# New Task Details

## Task Description

[DOC] Update new_task protocol with new Last Completed Task Summary file

1. Create new "LAST_TASK_SUMMARY.md" in top level to now be the new location of the full Last Completed Task Summary that is currently location in CLAUDE.md

2. Change & Enforce CLAUDE.md Last Completed Task Summary section to be at most 20 lines max to provide only high level overview quick glance of the last completed task, and if more details are needed, to refer to LAST_TASK_SUMMARY.md for the full complete Last Completed Task Summary

- This will greatly reduce the project's memory file context token usage in CLAUDE.md, and gives User and AI Coding agents the ability to have a quick glance of the last completed task and also the option to see the full details in a different document
- The quick glance summary may even be the verbatim git commit message if it has enough details to provide the quick glance summary

3. Update CLAUDE.md to enforce Entire project is still in the prototyping stage, so ALL task(s) need to enforce the following prototype principles:

- Do NOT over-engineer ANYTHING
- Does NOT need any of the following: Enterprise Grade, Production Ready, and\or Performance Optmization Solution(s)\Implementation(s)
- Does NOT need Testing, Test Scripts, Unit Tests, CI\CD Pipeline

4. Update our custom Claude Code slash command "/new_task" with the following new changes & procedures:

- MCP Tools are PRIMARY tools for ALL Specialist(s), and fallback to default tools if needed
- If in PLAN mode, Main Agent MUST use @agent-tech-lead-orchestrator to generate the Plan WITH Specialist Assignments. This will fix a gap in the "/new_task" where Plan mode incorrectly uses the Main Agent to generate the plan and also incorrectly has missing Plan WITH Specialist Assignments.  This ensures whether in Plan mode or Not Plan mode, that "/new_task" uses @agent-tech-lead-orchestrator no matter what for the planning WITH Specialist Assignments
- Enforce Entire project is still in the prototyping stage, so ALL task(s) need to enforce the following prototype principles:
- Do NOT over-engineer ANYTHING
- Does NOT need any of the following: Enterprise Grade, Production Ready, and\or Performance Optmization Solution(s)\Implementation(s)
- Does NOT need Testing, Test Scripts, Unit Tests, CI\CD Pipeline

- New expected workflow to update the new_task.md slash command procedures:
A. User invokes "/new_task"
B. Main Agent uses @agent-tech-lead-orchestrator to read, analyze, and review the new task details in "new_task_details.md", regardless if in Plan Mode or non-Plan Mode
C. If in Plan Mode, @agent-tech-lead-orchestrator generates the plan WITH Specialist Assignments
D. If in non-Plan Mode, @agent-tech-lead-orchestrator generates the plan WITH Specialist Assignments
E. Specialist(s) executes the plan from the @agent-tech-lead-orchestrator
F. After a PASSING Review\Fix Loop, perform the following doc updates
- Generate detailed Last Completed Task Summary and overwrite completely the existing LAST_TASK_SUMMARY.md
- Based on the Last Completed Task Summary, Generate a MAX of 20 lines a high level overview quick glance of the last completed task Summary and then update CLAUDE.md with the quick glance summary
G. Enforce Primary use of Github Tools and secondary Git tools for Repo Management Operations I.E. Commit, Push etc to
H. Enforce fully atomic commit where ALL of the following gets committed at the same time:
- Code\File Changes
- Doc Changes
- CLAUDE.md updates
- LAST_TASK_SUMMARY.md updates
I. End result of the commit is that all code, doc, and task summary changes are belong in the same Commit without separating code changes vs doc changes

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Analyze & Research all the requested task(s), reading any project docs that could also be relevant to the task(s)

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

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic Github commit containing ALL changes: code files, CLAUDE.md, LAST_TASK_SUMMARY.md, documentation updates, task summary
- Github Push commit to GitHub repository using provided personal access token
- **CRITICAL**: Must Github push to complete the workflow - Github commit without Github push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly Github committed and Github pushed

**Key Requirements:**

## Requirements

## Additional Context