# New Task Details

[GPT-5] Add Button Prompts

## Task Description

Add Button Prompts for Stock Snapshot, Support & Resistance Levels, & Technical Analysis

<Task 1> Ask Specialist to review & understand current implementation of the 3x Button Prompts from the Gradio UI code to try and integrate into the OpenAI Chat UI

<Task 2> Ask Specialist to use Context7 & Sequential-Thinking tools to Analyze & Research the most up to date, robust best practices, WITHOUT over-engineering for the requested task(s)

1. Prompts should have it's own dedicated file(s) in dedicated prompts folder(s) for optimal best practices for AI Prompt management I.E. .md, JSON format etc. This allows easy modifications & testing of different Prompts without needing to change the code
2. Need to ensure that ALL button prompts MUST be executed without needing user approval or confirmation
3. Between 1-3x max relevant follow up questions to the user after the initial Button Prompt Response

4. Snapshot Button: Daily Ticker Snapshot needs ONLY this data provided, formatted to match the Chat UI Emoji\Sentiment Rules

"ticker": "xxx",
"% Change": The percentage change since the previous day, to 2 decimal points
"Change": The value of the change from the previous day
"Timestamp": The last updated timestamp
"Open": The open price for the symbol in the given time period
"High": The highest price for the symbol in the given time period
"Low": The lowest price for the symbol in the given time period
"Close": The close price for the symbol in the given time period
"Volume": The trading volume of the symbol in the given time period
"VWAP": The volume weighted average price

5. Support & Resistance Levels Button: 3x Support Levels & 3x Resistance Levels

6. Technical Analysis Button

- Focus on Indicators relevant for Options Traders
- Excluding Support Levels\Resistance Levels since another Button Prompt handles this already

<Task 3> Based on the research & planning from Task 1 & 2, implement the plan for the button prompts

<Task(s)> Review\Fix Loop, Doc Updates, Atomic Git Commit & Push, & Final Verification:

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

- User clicking a button prompt will ONLY fill in the Chatbot input with the prompt text, allowing user to optionally modify prompt before sending to the AI Chat
- Button Prompts will NOT automatically send the message yet and leave it up to the user to trigger the actual sending

## Additional Context
