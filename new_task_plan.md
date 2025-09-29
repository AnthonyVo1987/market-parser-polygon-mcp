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

<Research, Investigation, Analysis, Scoping Task(s)>
Research Using Context7 Tools, Openai cookbook tools, openai gpt-5 prompting guides, to perform focused, incremental, comprehensive, systematic, investigation, & analysis to provide scoping for:

Task 1. Consolidate and streamline the current 3x Prompts to remove redundancies and improving performance and converting to TRUE a 2-tier architecture for AI Agent Prompts:

1. AI Agent Instructions: Becomes now the single source of truth "System Prompt" for ALL AI interactions
2. System Prompt Instructions: Duplicate and Redundant to AI Agent Instructions, so remove all of this and any code\prompts
3. Message Prompts: Streamline by removing the dupe instructions that matches AI Agent Instructions. Messages will always be sent with the AI Agent Instructions as part of the "prompt prefix", and the actual message gets appended and combined with the prompt prefix to send the whole message.  So currently we have the exact same AI instruction as part of the message too, which is dupe and redudant.  So fix the prompts\code.

Context:

1. **System Prompt Instructions are redundant** - The `Agent.instructions` parameter automatically becomes the system message
2. **Message Prompts can be simplified** - User messages can be sent directly without duplicate instructions
3. **AI Agent Instructions are the foundation** - They define the agent's behavior and become the system prompt

### **🔧 What Actually Happens:**

- **Agent Creation**: `Agent(instructions="...")` sets the system prompt
- **User Message**: `Runner.run(agent, "user query")` sends the message directly
- **SDK Magic**: The OpenAI Agents SDK automatically constructs the proper message array with system + user + history

### **📊 Simplified Architecture:**

1. **Tier 1: Agent Instructions** → System prompt (static)
2. **Tier 2: User Messages** → Dynamic user input (simple queries)

<Planning Task>
Based on the Research, Analysis & Scoping from previous task(s), delete the current 'TODO_task_plan.md' and then Generate a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to Implement the requested task(s) with 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s), NEVER stop using tools, continue using them until tasks completion, Comprehensive Documentation Updates & Cleanup, removal etc to reflect the latest updates to remove outdated info

<Implementation Task>
Implement the granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md'

<CLI Testing Task>
YOU MUST RUN 'test_7_prompts_comprehensive.sh' to perform  testing of CLI version, fix any issues until you get all 7x test to pass with 7x different response times.

<Serena Update Memories Task>
Use Serena Tools to update project memories to reflect all the new changes and new app architecture
