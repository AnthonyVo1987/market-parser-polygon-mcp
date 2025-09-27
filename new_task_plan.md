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

You are tasked with implementing a Dynamic Adaptive Prompting System for the Market Parser Polygon MCP application.

**CRITICAL REQUIREMENT**: You MUST first READ the complete implementation plan document at `docs/implementation_plans/dynamic_adaptive_prompting_system_implementation_plan.md` to understand all requirements, technical specifications, and implementation details. Do NOT proceed with implementation until you have thoroughly read and understood this document.

**Implementation Scope:**

- Implement a dynamic prompting system that allows users to customize AI interactions
- Make CLI and GUI system prompts identical and dynamic
- Preserve existing button prompt functionality
- Add user customization for verbosity, tool usage, output format, and response style
- Implement comprehensive security, validation, and error handling

**Key Requirements:**

1. **Read the Implementation Plan**: Start by reading `docs/implementation_plans/dynamic_adaptive_prompting_system_implementation_plan.md` completely
2. **Follow the Phased Approach**: Implement according to the 7-phase plan outlined in the document
3. **Maintain Security**: Implement all security specifications and validation requirements
4. **Preserve Functionality**: Ensure existing button prompts remain unchanged
5. **Performance Targets**: Meet all performance benchmarks specified in the plan
6. **Testing**: Implement comprehensive testing as specified in the plan

**Implementation Process:**

1. Read the complete implementation plan document first
2. Follow the detailed task checklist for each phase
3. Implement all technical specifications exactly as documented
4. Test each component according to the testing specifications
5. Validate security requirements and performance benchmarks
6. Update documentation as specified in the plan

**Success Criteria:**

- All functional and non-functional requirements met
- Performance benchmarks achieved
- Security specifications implemented
- Testing coverage >90%
- Existing functionality preserved

**Important Notes:**

- The implementation plan contains all necessary technical details, class structures, and specifications
- Refer back to the plan document whenever you need clarification on requirements
- If context gets overloaded, re-read the plan document to maintain focus
- Follow the exact implementation approach outlined in the plan

Begin by reading the implementation plan document, then proceed with the implementation according to the detailed specifications provided.
