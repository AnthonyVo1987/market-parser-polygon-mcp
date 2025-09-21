# New Task Details

## 🔴 CRITICAL: YOU MUST ALWAYS USE THESE TOOLS FIRST in any particular order to perform all task(s)

- __Serena Tools__: Use for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
- __Sequential-Thinking Tools__: Use for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
- __Context7 Tools__: Use for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups
- __Filesystem Tools__: Use for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
- __Standard Read/Write/Edit Tools__: Use for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
- __Playwright Tools__: Use for Testing with Browser automation for React GUI & App Validation

## Task Description

UI Enhancements & Optimizations

Let's streamline our UI to be more simple and obvious to it easier for testing because We've got too many complicated components that are confusing AI Agents using Playwright Tools to Test

Create a TODO Task Checklist and Use Mandatory Tools to perform these tasks: USE Context7, Serena, Sequential-Thinking & any other tools needed to perform research on the best up to date practices to implement each of the following requests:

Research Task 1. Remove expandable\collapsible display components and convert them to be fully displayed at all times on any of the UI cards.  Make the rest of those cards or grids fully static, and always display all components. So you have to lay them out and organize them.so that everything is always displayed.  There are only 2x sections that have expand\collapse, so both sections need to now display the full components, so you need to also expand the dimensions to make sure everything is fully displayed

Research Task 2. Re-label & emphasize the differentiate of the "AI Chatbot Input" vs "Stock Ticker Input". On multiple occasions, Ai Agents get confused and enter in a prompt in the "Stock Ticker Input" and\or they enter in Ticker in "AI Chatbot Input". "AI Chatbot Input" is for any user prompts and messages like a normal chatbot , so let's also increase the size of the chatbot input to be at LEAST 4 rows and make it very obvious that this is for "AI Chatbot Input".  Then, re-work\re-label or make somethign obvious that and name the Stock Input as "Button Prompt Stock Ticker", to emphasis this is only a ticker box for the button prompts.

Research Task 3. Re-work our loading\in progress indicators.  When somebody presses SEND for either a message in the AI input chat box or from the button prompt, let's make it obvious that the message is sent and it is in progress.  Let's put some big words or label on the screen that says "MESSAGE SENT - PLEASE WAIT FOR AI RESPONSE", and Let's just put it in the middle of the screen in front of the chat box to make it very obvious that the message was sent. Now it will be obvious that a message is SENT, BUT we have to wait.  Do not add animations. let's also remove the current loading spinner because it does not seem to be effective. This new change to loading indicator will help prevent false positive failures in testing.

Planning Task:
Based on all the analysis from Research Tasks 1, 2, & 3, generate a fully detailed granular implementation plan TODO Task Checklist for all of the requested changes and save it in a new .md doc in docs/implementation_plans folder. After creating the new plan doc, ask user to review the doc first.  DO NOT IMPLEMENT ANY CODE YET - ALL OF THESE TASKS ARE PURELY SCOPING AND PLANNING
