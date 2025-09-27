# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
5. Use Standard Read/Write/Edit for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation, pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## New Task Details

Use ALL your Mandatory Toolkit Tools to THINK LONG CONSTANTLY to systematically follow and perform all tasks in new_task_plan.md with a systematic approach

## New Feature Requirements\ User Story Context\Background

Let's make some adjustments to our system prompts that will be used for both the CLI version chat and the gui AI input chat.  Review and understand the new Feature requirments below first, and then perform the 9x tasks:

- Make the generic system prompt for both manual inputs, CLI and the GUI version are the same
- So we will have to make changes in the CLI version, and that change will be inherited in the gui version for user input prompts.  so in the end, effectively, there should be minimal changes to GUI proompts since CLi system prompt changes should be inherited by the GUI if implemented correctly
- We are NOT going to  touch the direct button prompts yet for, snapshot, support resistance, or technical analysis.  Let's just focus on the generic AI chat bot prompts that the user can input whatever they want
- Instead of having such a rigid structure on output format and how to respond, let's make it a lot more dynamic, adaptable and less strict.
- Let's have it extremely adaptive in that the user can specify the exact tool calls used, the verbosity, the depth of the analysis, and the output formatting to allow overriding of the default system prompt. That way generic user input for CLI and GUI is no longer static.
- For example, we need to have it generic because the user may request different tool calls and output formats and verbosity when performing manual AI input chats for CLI and GUI.
- That way, we don't have to always change the actual code in the prompt code when we are testing our prompts, which is the current non-efficient implementation where we have to make code changes every time we want to update a prompt which is not very feasible and efficient.
- We want a more dynamic and adjustable and less strict and adaptive prompting, where we can still keep the same code and not have to recompile, and the user can just tweak and adjust their prompts to get the requested data, analysis depth, and output format and verbosity they need for that specific prompt
- for example, we need the ability to have the user request just the raw data, some detailed analysis, and key takeaways. Or Maybe the user wants some emojis in the next response. And then Maybe the user only wants a specific tool to be used for the message. Or maybe user wants HIGH verbosity on one messages, and the next message maybe they just want a single bullet point etc.  or the user may want multiple tool calls to be used, or onyl SPECIFIC tool calls etc. Or the user may want to have the output formatted completely differently, with more verbosity.
- We just need to allow the user to do it with extremely customizable, dynamic and adaptive response requirements, depending on whatever the user wants
- So by default, using the AI input chat for CLI just needs to enforce minimal tool calls, less verbosity, and straight to the point with no analysis, just the facts. That's it. And then the gui version just inherits the CLI changes.
- This will allow the user with their prompts to adjust how they want. Whether they want more verbosity, more tool calls, different output formatting. Who knows? So at least this way, we have a hybrid approach. - We do have a standardized system  prompt in general that focuses on financial analysis, quick response, low verbosity, and minimal tool calls, no analysis as the basic default, which then can be adaptive to the next user request to override some of the defaults.
- this is the best of both worlds on that, if we enforce minimal tool calls, quick responses, and straight to the point with no addional analysis, that's just the generic system prompt for all responses. And then, the user can always specify in their prompt, if they want more verbosity, more tool calls, different output formatting etc So that way, we're no longer strict.
- So there is no longer going to be a static output format style for the user input prompts for CLI and the GUI version however, we will leave the button prompts alone for now since they are more static
- It should be totally adaptive. We're focused on the generic input chats first, and then we'll deal with the button prompts later, since they are less dynamic and more strict. - But at least with this new dynamic prompting, it allows us to be as detailed or not as detailed, as much as the user wants. without needing to change the code.
- Basically, for the responses, they can have different type of data and responses they want just by tweaking their prompt. and specifying different levels of analysis, verbosity, tool calls, formatting options for output, etc And the button prompts are left alone

## New Tasks details

## Task 1. After reviewing the New Feature Requirements\ User Story Context\Background above, use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to scope out the requiremnts to implement the new feature from the New Feature Requirements\ User Story Context\Background.  generate a initial scoping doc .md file and save to 'docs/implementation_plans' folder

## Task 2. use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to generate a detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 3. Review #1: use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  Fix any issues you find.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 4. Review #2:  use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  Fix any issues you find.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 5. Review #3:  use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  Fix any issues you find.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 6. Use mandatory tools toolkit to create a new .md doc file in 'docs/implementation_plans' of the new detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature

## Task 7. Doc Review: use Context7 tools, OpenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan doc created in Task 6. Fix any issues you find

## Task 8. Provide User a prompt - no docs needed, for user to copy and paste and have an AI Agent implement the full feature with mandatory toolkit tool use for all tasks in the plan generated from the reviewed new plan doc from task 7

## Task 9. Use Serena tools to update project memories

Use the following 3x Test prompts in the same session validate.  Each test prompt takes at least 30-90s test  prompt, so be sure to set a timeout fo 120s PER prompt to allow some breathing room.  Reminder that to test teh new feature ALL the prompts need to be sent in the same session sequentially.. IE. Test Prompt 1 first, and then detect response or timeout before moving onto the next test prompt.   Generate final .md test report

### 1. Market Status Query

#### Test Prompt 1: Market Status Query

"Current Market Status"

### 2. Single Stock Snapshot

#### Test Prompt 2: Single Stock Snapshot

"Single Stock Snapshot NVDA"

### 3. Full Market Snapshot

#### Test Prompt 3: Full Market Snapshot

"Full Market Snapshot: SPY, QQQ, IWM"

Answer

uvx --from git+<https://github.com/oraios/serena> serena project index ~/Github/market-parser-polygon-mcp

Validate changes by testing the CLI with some test prompts: uv run src/backend/main.py:
Test Prompt 1: "Current Market Status"
Test Prompt 2: "Single Stock Snapshot NVDA"
Test Prompt 3: "NVDA Support & Resistance Levels"

1. Completely remove the functionality to save reports in the CLI, since that functionality has been completely replaced with all the Copy\Export buttons.  Update all docs to reflect the new app behavior.  Currently the CLI Backend has a tool to save reports, but this feature has already been superceded by better features, so just retire\remove it

1. Use OpenAI Cookbook Doc Tools to fetch and research the "OpenAI GPT-5 Prompting Guide" for some tasks related to prompts optmizations for our project

2. Based on OpenAI GPT-5 Prompting Guide" and Context7 Research, update and optimize ALL of our prompts using the techniques and strategies from the prompting guide with some requirments & adjustments:

- Enforce LOW Verbosity for all responses
- Ensure that the existing core goals of prompts do not get accidentally removed as part of the optmizations, such as making sure to keep business critical logic such: Using accurate date and time, quick responses with minimal tool calls, ensuring AI Agent knows it has all tools for real-time data etc.
- The core goals of the prompts may be optimized better, BUT the core messaging should still be the same for keep the same functionality

3. Update project to use latest OpenAI Agents SDK version

4. Search for ALL docs and Fix and update ALL docs to reflect OpenAI Agents SDK version and remove the incorrect Pydantic AI statements since Pydantic AI is NOT part of our app's stack at all

5. Update Serena memories with the latest enhancements to the Prompt Optimizations

I made some manual fixes for some issues I caught:

1. Fixed typo for wrong Polygon MCP server version to use the corrected version "v0.4.1""
2. Updated tests/playwright/test_prompts.md to remove the Prompt Prefix "Quick Response Needed with minimal tool calls" since the enhanced code directly handles it now

Update Serena Memories with the latest fixes I made

## Task 1. Use Context7 Tools & Web Fetch tools to investigate and scope out a potential fix for the bug symptoms below

- We are incorrectly getting OpenAI Rate-Limited Using our gpt-5-nano and\or gpt-5-mini models, due to mismatching rate limits that do not match the rate limites for the model.  We could be incorrectly configured for rate limiting by being incorrectly limited based on gpt-4o model, which has lower rate limits AND is not even a model that is currently supported in the app
- We enabled the rate limit config settings in config/app.config.json, so also need to review it.  It's possible we are simply just misconfigured to have proper rate limits and\or we are missing some additional configs to specific the actual model and expected TPM rate limits etc

- Here is the incorrect error message showing gpt-4o model rate limit of 30,000 TPM, which does NOT match gpt-5-nano \ gpt-5-mini rate limits:

## 🤖 AI Assistant - 9/24/2025, 6:05:16 PM

Error: Unable to process request. Error code: 429 - {'error': {'message': 'Request too large for gpt-4o in organization org-lAuyrzHd2vdxsszI3LECrcWP on tokens per min (TPM): Limit 30000, Requested 32099. The input or output tokens must be reduced in order to run successfully. Visit <https://platform.openai.com/account/rate-limits> to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}

- Per some web resources, here are the official expected rate limits for different models for users in Tier 1 and up:

Here's the data from the screenshot converted into a markdown table:

| MODEL                     | TOKEN LIMITS | REQUEST AND OTHER LIMITS | BATCH QUEUE LIMITS |
| :------------------------ | :----------- | :----------------------- | :----------------- |
| gpt-5-mini                | 500,000 TPM  | 500 RPM                  | 5,000,000 TPD      |
| gpt-5-nano                | 200,000 TPM  | 500 RPM                  | 2,000,000 TPD      |
| gpt-4o                    | 30,000 TPM   | 500 RPM                  | 90,000 TPD         |

## Task 2. Provide your implementation plan so user can review and approve your fix or not.  Do not create any new docs for the plan

Error: Unable to process request. Error code: 429 - {'error': {'message': 'Rate limit reached for gpt-4o in organization org-lAuyrzHd2vdxsszI3LECrcWP on tokens per min (TPM): Limit 30000, Used 11897, Requested 18892. Please try again in 1.578s. Visit <https://platform.openai.com/account/rate-limits> to learn more.', 'type': 'tokens', 'param': None, 'code': 'rate_limit_exceeded'}}

Perform all task(s) in new_task_details.md

Mark off completed tasks and phases as part of the review workflow: docs/implementation_plans/cli_gui_performance_optimization_implementation_plan.md

## Give me a prompt I can use to assign an AI Agent to read docs/implementation_plans/cli_gui_performance_optimization_implementation_plan.md then perform the new tasks below

## Task Details

1. Perform Comprehensive Systematic granular Code\Doc Audit & Code\Review Review to verify ALL Tasks have been correctly implemented from Phases 1 - Phase 5 from docs/implementation_plans/cli_gui_performance_optimization_implementation_plan.md
2. Fix any tasks that may not have been correctly implemented
3. Mark off correctly completed tasks with green checks in docs/implementation_plans/cli_gui_performance_optimization_implementation_plan.md

Requirements:

## Follow Mandatory Tools Toolkit Usage for ALL Tasks

## 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion!!!! 🔴

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
5. Use Standard Read/Write/Edit for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. 🔴 REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation, pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

###

## New Feature Requirements\ User Story Context\Background

Let's make some adjustments to our system prompts that will be used for both the CLI version chat and the gui AI input chat.  Review and understand the new Feature requirments below first, and then perform the 9x tasks:

- Make the generic system prompt for both manual inputs, CLI and the GUI version are the same
- So we will have to make changes in the CLI version, and that change will be inherited in the gui version for user input prompts.  so in the end, effectively, there should be minimal changes to GUI proompts since CLi system prompt changes should be inherited by the GUI if implemented correctly
- We are NOT going to  touch the direct button prompts yet for, snapshot, support resistance, or technical analysis.  Let's just focus on the generic AI chat bot prompts that the user can input whatever they want
- Instead of having such a rigid structure on output format and how to respond, let's make it a lot more dynamic, adaptable and less strict.
- Let's have it extremely adaptive in that the user can specify the exact tool calls used, the verbosity, the depth of the analysis, and the output formatting to allow overriding of the default system prompt. That way generic user input for CLI and GUI is no longer static.
- For example, we need to have it generic because the user may request different tool calls and output formats and verbosity when performing manual AI input chats for CLI and GUI.
- That way, we don't have to always change the actual code in the prompt code when we are testing our prompts, which is the current non-efficient implementation where we have to make code changes every time we want to update a prompt which is not very feasible and efficient.
- We want a more dynamic and adjustable and less strict and adaptive prompting, where we can still keep the same code and not have to recompile, and the user can just tweak and adjust their prompts to get the requested data, analysis depth, and output format and verbosity they need for that specific prompt
- for example, we need the ability to have the user request just the raw data, some detailed analysis, and key takeaways. Or Maybe the user wants some emojis in the next response. And then Maybe the user only wants a specific tool to be used for the message. Or maybe user wants HIGH verbosity on one messages, and the next message maybe they just want a single bullet point etc.  or the user may want multiple tool calls to be used, or onyl SPECIFIC tool calls etc. Or the user may want to have the output formatted completely differently, with more verbosity.
- We just need to allow the user to do it with extremely customizable, dynamic and adaptive response requirements, depending on whatever the user wants
- So by default, using the AI input chat for CLI just needs to enforce minimal tool calls, less verbosity, and straight to the point with no analysis, just the facts. That's it. And then the gui version just inherits the CLI changes.
- This will allow the user with their prompts to adjust how they want. Whether they want more verbosity, more tool calls, different output formatting. Who knows? So at least this way, we have a hybrid approach. - We do have a standardized system  prompt in general that focuses on financial analysis, quick response, low verbosity, and minimal tool calls, no analysis as the basic default, which then can be adaptive to the next user request to override some of the defaults.
- this is the best of both worlds on that, if we enforce minimal tool calls, quick responses, and straight to the point with no addional analysis, that's just the generic system prompt for all responses. And then, the user can always specify in their prompt, if they want more verbosity, more tool calls, different output formatting etc So that way, we're no longer strict.
- So there is no longer going to be a static output format style for the user input prompts for CLI and the GUI version however, we will leave the button prompts alone for now since they are more static
- It should be totally adaptive. We're focused on the generic input chats first, and then we'll deal with the button prompts later, since they are less dynamic and more strict. - But at least with this new dynamic prompting, it allows us to be as detailed or not as detailed, as much as the user wants. without needing to change the code.
- Basically, for the responses, they can have different type of data and responses they want just by tweaking their prompt. and specifying different levels of analysis, verbosity, tool calls, formatting options for output, etc And the button prompts are left alone

## New Tasks details

## Task 1. After reviewing the New Feature Requirements\ User Story Context\Background above, use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to scope out the requiremnts to implement the new feature from the New Feature Requirements\ User Story Context\Background.  generate a initial scoping doc .md file and save to 'docs/implementation_plans' folder

## Task 2. use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to generate a detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 3. Review #1: use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  Fix any issues you find.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 4. Review #2:  use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  Fix any issues you find.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 5. Review #3:  use Context7 tools, OPenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature.  Fix any issues you find.  DO NOT CREATE NEW DOCS FOR THE PLAN YET SO USER CAN REVIEW

## Task 6. Use mandatory tools toolkit to create a new .md doc file in 'docs/implementation_plans' of the new detailed granular TODO Checklist Tsk Implementation PLan for an AI Agent to implement the new feature

## Task 7. Doc Review: use Context7 tools, OpenAi cookbook tools, and any other mandatory toolkit tools to perform a comprehensive review of the detailed granular TODO Checklist Tsk Implementation PLan doc created in Task 6. Fix any issues you find

## Task 8. Provide User a prompt - no docs needed, for user to copy and paste and have an AI Agent implement the full feature with mandatory toolkit tool use for all tasks in the plan generated from the reviewed new plan doc from task 7

## Task 9. Use Serena tools to update project memories
