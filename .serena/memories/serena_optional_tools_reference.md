# Serena Optional Tools Reference - CCB Project

## Enabled Optional Tools

The following optional tools have been enabled in .serena/project.yml:

### delete_lines

- **Purpose**: Deletes a range of lines within a file
- **Usage**: Requires reading file first with read_file tool
- **Example**: Delete lines 10-15 from a file
- **Safety**: Always verify line numbers before deletion

### get_current_config

- **Purpose**: Prints current configuration including active project, tools, and modes
- **Usage**: Call anytime to check current state
- **Output**: Shows active project, available tools, current modes
- **Troubleshooting**: Use to verify project activation and tool availability

### initial_instructions

- **Purpose**: Gets initial instructions for the current project
- **Usage**: Call to understand Serena's behavior and guidelines
- **Content**: Detailed instructions on tool usage, code reading strategies, editing approaches
- **When to Use**: At start of new tasks or when unsure about best practices

### insert_at_line

- **Purpose**: Inserts content at a given line in a file
- **Usage**: Specify line number and content to insert
- **Example**: Insert comment at line 5
- **Note**: Pushes existing content down

### replace_lines

- **Purpose**: Replaces a range of lines within a file with new content
- **Usage**: Requires reading file first, then specify start/end lines
- **Example**: Replace lines 20-25 with new code
- **Safety**: Always read file first to verify line numbers

### restart_language_server

- **Purpose**: Restarts the language server (clangd for C++)
- **Usage**: Call when language server issues occur
- **When to Use**: After configuration changes, when symbol analysis fails
- **Output**: Returns "OK" when successful

### summarize_changes

- **Purpose**: Provides instructions for summarizing codebase changes
- **Usage**: Call to get guidance on documenting changes
- **Content**: Instructions on what to include in change summaries
- **When to Use**: After completing development tasks

### switch_modes

- **Purpose**: Activates different operational modes
- **Available Modes**: planning, interactive, editing, onboarding, one-shot, no-onboarding
- **Usage**: Specify list of modes to activate
- **Example**: switch_modes(['planning']) for analysis-only mode
- **Note**: Some tools become unavailable in certain modes

## Tool Usage Patterns

- **Analysis Tasks**: Use planning mode with symbol analysis tools
- **Development Tasks**: Use interactive + editing modes
- **File Operations**: Use line-based tools for small changes, symbol-based for large changes
- **Troubleshooting**: Use get_current_config and restart_language_server
- **Documentation**: Use summarize_changes and write_memory

## Safety Guidelines

- Always read files before line-based operations
- Use version control before major changes
- Test tools in safe environments first
- Keep backups of important configurations
- Verify tool results before proceeding
