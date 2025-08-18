### THIS DOCUMENT SHOULD NOT BE OPENED OR READ BY AI AGENTS BECAUSE IT IS ONLY FOR TEMPORARY USER SCRATCHPAD AND NOTES


Have @Tech-Lead-Orchestrator follow CLAUDE.md & use SEQUENTIAL THINKING TOOL & CONTEXT7 to research and generate a comprehensive plan for delegation & coordination of implementing the code changes for the following task(s) details:

## High Level Task Goal: Consolidate & Re-Factor Dedicated Structured UI Display Code

## Task Context & Background:
- MANDATORY MCP TOOL USE
- We need to simplify, Consolidate, & refactor the complex Dedicated Structured UI Display because the UI changes may be too complex to implement in Gradio as a true "front end"
- We will temp shelve some of the new UI display code and put notes that a future task TBD will be assigned to re-visit the UI updates, such as even migrating to a true front end like REACT

## Task Details:
- Remove\Retire all code, docs, test cases, FSM code related to the "Structured Stock Analysis -  Structured Data Display for  Stock Snapshot, Support & Resistance, & Technical Analysis"
- We will instead just keep the Raw JSON Outputs for the Snapshot JSON, Support & Resistance JSON, & Technical Analysis JSON

- So here is how the new app flow should be after the removal:
1. Button Prompts will still have a STRUCTURED JSON OUTPUT format that will output into BOTH the Chatbox & THE Raw JSON boxes
2. There will no longer be ANY UI code parsing\conversion needed to display since we will JUST have the raw JSON boxes now
3. The RAW JSON outputs will serve as the "UI display", both in the AI chat AND user can review the raw payload as well
4. The Button prompts should be able to be presses and sent in ANY ORDER with no data dependencies needed
5. An error\failure in ANY operation of the app should NOT block the user from issuing more commands to test out the rest of app. Currently the app\FSM flow incorrectly prevents further user action if a previous action failed and also incorrectly wipes app data for new request. This makes it tough to fully test the app in production if we are stuck on a failure, and can't even test out other commands etc
6. FSM States\Flags\Variables may have to be updated
7. Test scripts also need to be updated
8. Output Console debug logs\messages also need to be updated
9. All docs also need to be updated

## ACTIONS TO BE PERFORM ONLY AFTER INITIAL CODING\TESTING:
- Speciliast to perform Review\Fix Loop until PASSING code review
- ONLY AFTER A PASSING CODE REVIEW, SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes 
- User will then start testing out the new changes




## ACTIONS TO BE PERFORM ONLY AFTER PASSING CODE REVIEW OF ALL CODE\DOC CHANGES:
- ONLY AFTER A PASSING CODE REVIEW, SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes 
- User will then start testing out the new changes



 Ask @Tech-Lead-Orchestrator to follow CLAUDE.md to provide a delegation and coordination plan for Specialist to perform the following task(s)

- The project file and folder structure has gotten completley massive, confusing, and unweildy
- Re-orgranize the entire project structure folder Hierachy using mandatory structured analysis to research best practices for re-organization according to our app's stack and architecture
- There are also multiple chat_ui_enhanced, xxx_final, xx_old etc so we need to clean up all these redundant files and dupe files for the entire project. remove all back up files
- This is a non exhaustive list, but I can see that we need folders for:
- Test scripts, which are currently incorrectly un organized in top level folder, confusing the user which files are actual source code vs test files
- Log files - similiar to above where they are currently incorrectly un organized in top level folder
- Etc - re-organize anything else not mentioned

- Once the re-organization is complete, update all project docs like CLAUDE.md, README.md etc with the new file and folder structure
- Code review afterwards with using structured analysis

## ACTIONS TO BE PERFORM ONLY AFTER PASSING CODE REVIEW OF ALL CODE\DOC CHANGES:
- SPECIALIST to perform git status and then an automous ATOMIC commit and push to the github repo for ALL Doc\Code\File changes ONLY AFTER A PASSING CODE REVIEW
- Provide Summary (NO DOCS needs) of MCP Tool Calls (NOT standard Claude Code tools) used by EACH Specialist involved so user can verify the proper tool calls used for the task(s)
- User will then start testing out the new changes





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


