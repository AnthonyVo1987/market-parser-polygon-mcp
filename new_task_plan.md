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
Use Context7 Tools, Openai cookbook tools to perform focused, incremental, comprehensive, systematic, investigation, & analysis to provide scoping for:

Task 1. Remove ALL OpenAI Rate limiting code\config so that we can have maximum model performance

Task 2. Research and optimize all AI Output Response from  OpenAI Responses API config\properties\attributes for OpenAI gpt-5-nano & OpenAI gpt-5-mini models being used in our app. You have to check the from OpenAI for some of the attributes.  Verify and fix to make sure the app is actually using the settings:

- max_context_length: Output should be set to max for both models.
- temperature: should be set higher to .2 for Financial Analysis
- Enable adaptive thinking\reasoning to allow model to adjust it's reasoning as needed to match the complexity of the tasks
- Set verbosity to LOW
- adjust anything else that can be optmized for every AI response

Task 3. Research and optimize all OpenAI Agents SDK AI Agent config\properties\attributes for OpenAI gpt-5-nano & OpenAI gpt-5-mini models being used in our app. Verify and fix to make sure the app is actually using the settings:

- adjust anything else that can be optmized for every AI agent
- Fix the Agent's "max_tokens" setting because it makes no sense to be so low that does not even match the gpt-5 models.  are they even being used correctly?  these models have 400K total context window and a max output of 128K tokens.

src/backend/routers/models.py
async def get_available_models():
    """Get list of available AI models"""
    try:
        models = [
            AIModel(
                id=AIModelId.GPT_5_NANO,
                name="GPT-5 Nano",
                description="Fast and efficient model for quick responses",
                is_default=True,
                cost_per_1k_tokens=0.15,
                max_tokens=4096,
            ),
            AIModel(
                id=AIModelId.GPT_5_MINI,
                name="GPT-5 Mini",
                description="Balanced performance model",
                is_default=False,
                cost_per_1k_tokens=0.25,
                max_tokens=8192,
            ),
            # Removed GPT_4O and GPT_4O_MINI models
        ]

<Planning Task>
Based on the Research, Analysis & Scoping from previous task(s), delete the current 'TODO_task_plan.md' and then Generate a brand new granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md' for you to Implement the requested task(s) with 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s), NEVER stop using tools, continue using them until tasks completion, Comprehensive Documentation Updates & Cleanup, removal etc to reflect the latest updates to remove outdated info

<Implementation Task>
Implement the granular detailed Implementation Plan TODO Task Checklist file 'TODO_task_plan.md'

<Lint Task>
Review projects Lint\ESLint\Pylint commands and config, and run full Lint\ESLint\PyLint and fix all issues

<CLI Testing Task>
Perform some testing of CLI version executing test_7_prompts_comprehensive.sh (uv run src/backend/main.py), fix any issues

<Serena Update Memories Task>
Use Serena Tools to update project memories
