# New Task Details

## Task Description

feat: Add new Console Log Toggle as part of the Developer Card Section for the user to be able to switch the Console Log Output verbosity mode on the fly from either DEBUG vs PRODUCTION mode console logs.  DEBUG will be the default mode & show ALL console log messages for full debugging capability during development.  PRODUCTION will only show the warn and error level messages for better performance and more User expected experience.  Need to remove the hard coded configs & code for the Console Message Level.  After implementing, perform quick Playwright MCP Tools method to test our the new code & fix any issues:

Expected Outcome: App starts up with default DEBUG level messages. Debug mode tests will show full console messages.  Then toggling PRODUCTION mode and re-issuing the same tests will now show less console messages for the same actions vs DEBUG mode

Test Plan: YUsing same single instance browser running each test one at a time sequentially:

1. DEBUG MODE: User Input: "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
2. DEBUG MODE: Button Prompt Stock Snapshot
3. Toggle on PRODUCTION mode to re-test for apples to apples comparison of logs
4. PRODUCITON MODE: User Input: "Single Ticker Snapshot: NVDA, PRIORITY FAST REQUEST NEEDING QUICK RESPONSE WITH MINIMAL TOOL CALLS ONLY & LOW Verbosity"
5. PRODUCITON MODE: Button Prompt Stock Snapshot

  ⎿  Console Log Toggle Feature Implementation Plan

     1. Enhance Logger.ts for Dynamic Mode Switching

     - Add a logMode property that can be 'DEBUG' or 'PRODUCTION' (default: 'DEBUG')
     - Create public methods setLogMode() and getLogMode() for mode management
     - Modify the shouldLog() method to respect the current mode:
       - DEBUG mode: Show all messages (debug, info, warn, error)
       - PRODUCTION mode: Show only warn and error messages
     - Store mode preference in localStorage for persistence
     - Expose mode change event for UI updates

     2. Add Console Log Toggle to DebugPanel Component

     - Add a toggle switch UI element with labels "DEBUG" and "PRODUCTION"
     - Position it within the collapsible debug panel content
     - Implement state management for the toggle using React hooks
     - Connect toggle to logger's setLogMode() method
     - Apply glassmorphic styling consistent with the existing UI
     - Add proper ARIA labels for accessibility

     3. Update DebugPanel Styles

     - Add CSS for the toggle switch component
     - Include hover states and transitions
     - Ensure responsive design for mobile/tablet/desktop
     - Apply the amber/orange debug theme colors

     4. Test Implementation with Playwright

     - Start the app and verify default DEBUG mode
     - Test Query 1: Submit "Single Ticker Snapshot: NVDA..." in DEBUG mode
     - Test Query 2: Click "Stock Snapshot" button in DEBUG mode
     - Toggle to PRODUCTION mode
     - Test Query 3: Submit same ticker query in PRODUCTION mode
     - Test Query 4: Click "Stock Snapshot" button in PRODUCTION mode
     - Verify console output differences between modes
     - Check localStorage persistence of mode preference

     5. Fix Any Issues Found During Testing

     - Address any console errors or warnings
     - Ensure smooth toggle transitions
     - Verify mode persistence across page refreshes

     Expected Outcomes:

     - DEBUG mode: Full verbose console output for development
     - PRODUCTION mode: Minimal console output (only warnings/errors)
     - Toggle state persists in localStorage
     - Seamless mode switching without page reload

- START_SCRIPT_README.md
- start-app.sh
- start-app-xterm.sh

Use `mcp__sequential-thinking__sequentialthinking` tools for systematic approach & any other Tools needed to perform the following task(s):

1. Update both one click start up scripts with the following changes:

- Remove the automatic browser launch step to allow user to use ANY browser to start their testing and\or maybe user wants to just start both frontend & backend dev servers without testing browser yet
- Replace the automatic browser launch with new messages instead to notify User that app ready to be loaded and provide the exactly URL that user can click\copy link to launch the web app in their browser of choice

## Task 1. Use `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform research & implementing the following

We are currently in the middle of streamlining & consolidating Project Docs due to the massive re-architectural changes that have been implemented in our project. Review our legacy archived docs/archived/CLAUDE_LEGACY.md & docs/archived/README_LEGACY.md in order to perform the following for Each doc:

## Final Task(s)

MUST USE Context7 & Sequential-Thinking Tools to perform: Final Task 1: Review/Fix Loop

- Performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Optional `mcp__filesystem__*` tools for EFFICIENT file operations and examination.
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle until achieving PASSING code review status

Final Task 2: Task Summary Updates for CLAUDE.md

- Create token & context efficient git commit message of all the changes to prepare for the final commit task(s)
- Update CLAUDE.md "Last Completed Task Summary" section with the VERBATIM COPY of the token & context efficient git commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- This ensures that the git commit message is cached for token & context efficient in order to update CLAUDE.md with, preventing the need to waste tokens by having to regenerate similiar task completion summaries

Final Task 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic git commit containing ALL changes: CLAUDE.md, code files, documentation changes, 1x test report if it exist
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome*

*All Files, Docs atomically commited after all tasks are complete*

## Additional Context
