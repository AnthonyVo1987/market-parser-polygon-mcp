# New Task Details

## Task Description

[OpenAI] Pre-Migration Test & Fix Issues from Development Deployment Server Testing for both CLI & GUI

## Task 1. Run Standalone OpenAI CLI and perform simple test to ask "NVDA Daily Snapshot for the last trading & keep response minimal and less verbose"

- You will need to set a terminal\bash timeout of at least 120 seconds to allow the terminal\bash commands to respond because reponses are NOT instant
- Confirm that the CLI app start up and also is able to respond to the test query
- Fix any issue seen from logs

## Task 2. Run Standalone OpenAI GUI using default Vite dev server method(s) and perform simple test to WebFetch the localhost website to trigger the  Web App to try and load

- Reminder that just starting the dev server is NOT complete - the web site\web app\ local host url MUST be browsed\fetched to trigger the full GUI test
- You will need to set a terminal\bash timeout of at least 120 seconds to allow the terminal\bash commands to respond because reponses are NOT instant
- Confirm that the app starts up OK
- Fix any issue seen from logs

## Task 3. Run Standalone OpenAI GUI using Live Server dev server method(s) and perform simple test to WebFetch the localhost website to trigger the Web App to try and load

- Reminder that just starting the dev server is NOT complete - the web site\web app\ local host url MUST be browsed\fetched to trigger the full GUI test
- You will need to set a terminal\bash timeout of at least 120 seconds to allow the terminal\bash commands to respond because reponses are NOT instant
- Confirm that the app starts up OK
- Fix any issue seen from logs

## Task 4. Create new .md doc in OpenAI folder to track status & results from all the pre-migration Testing Tasks 1, 2, & 3

- Update any other project docs if needed from fixes

## Research Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- Analyze & Research all the requested Task 1, Task 2, & Task 3, reading any project docs that could also be relevant to the task(s)

## Planning Task(s) - Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Research, Analyze, & Perform the following task(s)

- IF RESEARCH FROM ALL 3x Task were NOT performed, this is a VIOLATION and task must be restarted from the beginning
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

## Expected Outcome

- CLI tested with a proper AI response back
- Vite & Live Serve GUI methods tested WITH an explicit local host url test to trigger the actual dev server to load\compile the app because JUST starting dev servers does NOT test the actuall at all

## Additional Context
