### THIS DOCUMENT SHOULD NOT BE OPENED OR READ BY AI AGENTS BECAUSE IT IS ONLY FOR TEMPORARY USER SCRATCHPAD AND NOTES



claude "[DOCS] Use @Tech-Lead-Orchestrator to follow CLAUDE.md to scope out a plan for the delegation and coordination for Specialists perform the task(s)"

- The project file and folder structure has gotten completley massive, confusing, and unweildy
- Re-orgranize the entire project structure folder Hierachy using mandatory structured analysis to research best practices for re-organization according to our app's stack and architecture
- There are also multiple chat_ui_enhanced, xxx_final, xx_old etc so we need to clean up all these redundant files and dupe files for the entire project. remove all back up files
- This is a non exhaustive list, but I can see that we need folders for:
- Test scripts, which are currently incorrectly un organized in top level folder, confusing the user which files are actual source code vs test files
- Log files - similiar to above where they are currently incorrectly un organized in top level folder
- Etc - re-organize anything else not mentioned

- Once the re-organization is complete, update all project docs like CLAUDE.md, README.md etc with the new file and folder structure
- Code review after wards with using structured analysis

## ACTIONS TO BE PERFORM ONLY AFTER PASSING CODE REVIEW OF ALL CODE\DOC CHANGES:
- SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes ONLY AFTER A PASSING CODE REVIEW
- User will then start testing out the new changes



## ACTIONS TO BE PERFORM ONLY AFTER PASSING CODE REVIEW OF ALL CODE\DOC CHANGES:
- SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes ONLY AFTER A PASSING CODE REVIEW
- User will then start testing out the new changes



## ACTIONS TO BE PERFORM ONLY AFTER CHANGES
- SPECIALIST to Start an Code\Doc Review and Fix Loop until we get a passing code review
- If PASSING code review, SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes
- User will then start testing out the new changes
##




Scope out and update the scope doc to enforce a "single source of truth FSM (Finite State Machine)"
- Current scope already has some state management, but let's make it a full on deterministic FSM
- So research the best practices to implement a FSM according to our app's architecture, app stack, and the scope doc details


- Update the entire implementation plan with the updated details

## ACTIONS TO BE PERFORM ONLY AFTER CHANGES
- Start an automous Code\Doc Review and Fix Loop until we get a passing code review
- If PASSING code review, perform an autonomous ATOMIC git commit and push to the repo for ALL Doc\Code\File changes
- User will then start testing the code



###




 the feasibility, complexity, and initial implementation plan and task breakdown for new potential feature with the following details:

USE STRUCTURED ANALYSIS AND ANY OTHER AVAILABLE RESEARCH METHODS AS NEEDED TO ENSURE MOST UP TO DATE AND ROBUST BEST PRACTICES

## High Level Goal: Scope new feat: Add GUI elements to be update\populated with data from certain new AI prompts actions


## Details

1. Add GUI elements that will be later updated and populated with data from responses:
- Stock Snapshot
- Support & Resistance Levels - 3 levels EACH
- Technical Analysis - RSI, MACD, EMA 5\10\20\50\200, SMA 5\10\20\50\200

2. Add some Button Prompts that user can click that will insert in specific Prompts for the AI Agent Chat:
- Current Stock Snapshot
- Support & Resistance Levels - 3 levels EACH
- Technical Analysis - RSI, MACD, EMA 5\10\20\50\200, SMA 5\10\20\50\200

3. After a button prompt is completed with a proper chat response, the app\ai agent etc now needs to update the corresponding GUI elements with the response data

4. ONLY the button prompts are allowed to update the new GUI elements. Any other chat interactions from user will NOT trigger the new gui updates

5. Generate a new.md doc in the docs folder for the new scoping details

## ACTIONS TO BE PERFORM ONLY AFTER CHANGES
- Start an automous Code\Doc Review and Fix Loop until we get a passing code review
- If PASSING code review, perform an autonomous ATOMIC git commit and push to the repo for ALL Doc\Code\File changes
- User will then start testing the changes


Have @Tech-Lead-Orchestrator come up with a delegation and coordination plan for the following task(s):

## Task Goal: Documentation consolidation and cleanup operations (COMPLETED)

## MANDATORY APPROACH:
- Refer to CLAUDE.md documentation for structured analysis and best practices
- Use built-in analysis and reasoning capabilities for research

## Details
- Consolidated generic task rules from old files into CLAUDE.md
- CLAUDE.md is now the single source of truth on AI Agent operating procedures for the entire project
- Updated workflow: user assigns tasks to tech lead Orchestrator with details, then CLAUDE.md must be followed for planning, delegation, coordination, and starting tasks by appropriate SPECIALIST

## ACTIONS TO BE PERFORM ONLY AFTER CHANGES
- Start an automous Code\Doc Review and Fix Loop until we get a passing code review
- If PASSING code review, perform an autonomous ATOMIC git commit and push to the repo for ALL Doc\Code\File changes
- User will then start testing the changes


