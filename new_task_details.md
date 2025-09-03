# New Task Details

[DOCS] Fix New Task Custom Slash Commands & Task Summary Sequence

## Task Description

Task A. Perform Research on creating new optimal Claude Code Custom Slash Commands for our project

Task B. After the research, generate a new Custom_Slash_Commands.md in the docs folder to serve as a reference guide on how to properly add, modify, & update existing & new Custom Slash Commands

Task C. Fix "/new_task" slash command to perform the 4x Review\Fix Loop actions TO BE PERFORM AFTER ALL TASK(S) ARE COMPLETE

1. Specialist to start Review\Fix Loop until PASSING review with MANDATORY Sequential-Thinking & Filesystem Tool Usage, and OPTIONAL Context7 tool call(s) if review needs any specific changes that may need Context7 up to date documentation\best practices etc
2. ONLY AFTER A PASSING CODE REVIEW, Specialist to perform automous git status, automous ATOMIC GIT commit and GIT PUSH to the github repo for ALL Doc\Code\File changes
3. After commit, Specialist to perform final git status to verify successful commit
4. DO NOT FORGET TO PUSH SINCE I ALREADY PROVIDED A GITHUB PERSONAL ACCESS TOKEN - IF YOU DO NOT PUSH, YOU HAVE NOT COMPLETED THE ATOMIC COMMIT & PUSH!!!

Task D. Fix "Last Completed Task Summary" Logic to prevent multiple non-atomic commits where code changes & doc updates are incorrectly separated

- You may need to find the optimal place for this logic, either in CLAUDE.md, "/new_task", and\or both etc

Task E. PAUSE after Tasks A, B, C, & D are fininshed so user can review and approve the changes or not

## Requirements

## Expected Outcome

- User invokes "/new_task" command with details in the "new_task_details.md"
- Task(s) get implemented
- Once all task(s) are finished, the Review\Fix Loop gets triggered
- After a PASSING Review\Fix Loop, Generate a the task completion summary, THEN update CLAUDE.md with the task completion summary
- After CLAUDE.md has been updated\overwritten with the most up to date task completion summary, THEN the atomic commit & push is performed
- End result is that changes are autonmously reviewed\fixed in the automated worfklow, and then task completion summary committed and checked in ATOMICALLY with ALL file and doc changes
- This ensures that we do NOT have multiple commits for a task, where the file changes are committed first, and then the task summary gets committed in a separate commit to CLAUDE.md , which is the WRONG way to handle it
- Everything gets committed in a single atomic commit for ALL tasks and prevents multiple non-atomic commits where code changes & doc updates are incorrectly separated

## Additional Context

- I requested to add the 4x Review\Fix loop actions to the custom /new_task command, but you incorrectly implemented it 100% badly from the last couple of commits
- You added all of these extra rules, procedures I never asked for and overstepped your boundaries; it looked NOTHING like my 4x rules and you over engineered, over complicated the rules
- So I manually reverted the terrible bad updates so you can fix them
