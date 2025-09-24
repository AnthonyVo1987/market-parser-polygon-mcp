# Serena Optional Tools Configuration Guide

## Overview

This guide explains how to enable and use the optional Serena tools that have been configured for the market-parser-polygon-mcp project. These tools provide additional functionality beyond the default Serena toolset.

## Configuration

The optional tools have been enabled in the project configuration file at `.serena/project.yml` by adding the following section:

```yaml
included_optional_tools:
  - delete_lines
  - get_current_config
  - initial_instructions
  - insert_at_line
  - replace_lines
  - restart_language_server
  - summarize_changes
  - switch_modes
```

## Available Optional Tools

### 1. `delete_lines`

**Purpose**: Deletes a range of lines within a file.

**Usage**:

- Specify the file path and line range to delete
- Useful for removing specific sections of code or content
- More precise than using standard file editing tools

**Example Use Cases**:

- Remove deprecated functions
- Clean up commented-out code blocks
- Delete specific error handling sections

### 2. `get_current_config`

**Purpose**: Prints the current configuration of the agent, including the active and available projects, tools, contexts, and modes.

**Usage**:

- Provides real-time information about Serena's current state
- Useful for debugging and understanding tool availability
- Shows active modes and contexts

**Example Use Cases**:

- Debugging tool availability issues
- Understanding current project configuration
- Verifying mode and context settings

### 3. `initial_instructions`

**Purpose**: Gets the initial instructions for the current project. Should only be used in settings where the system prompt cannot be set, e.g. in clients you have no control over, like Claude Desktop.

**Usage**:

- Retrieves project-specific instructions and context
- Useful when working with clients that don't support custom system prompts
- Provides project onboarding information

**Example Use Cases**:

- Working with Claude Desktop
- Getting project context in restricted environments
- Understanding project-specific requirements

### 4. `insert_at_line`

**Purpose**: Inserts content at a given line in a file.

**Usage**:

- More precise than standard file editing tools
- Allows insertion at specific line numbers
- Useful for maintaining code structure

**Example Use Cases**:

- Adding imports at the top of files
- Inserting new functions at specific locations
- Adding comments at precise line positions

### 5. `replace_lines`

**Purpose**: Replaces a range of lines within a file with new content.

**Usage**:

- Replaces specific line ranges with new content
- More precise than standard search and replace
- Maintains file structure while updating content

**Example Use Cases**:

- Updating function implementations
- Replacing configuration sections
- Modifying specific code blocks

### 6. `restart_language_server`

**Purpose**: Restarts the language server, may be necessary when edits not through Serena happen.

**Usage**:

- Restarts the language server when it becomes unresponsive
- Useful after external file modifications
- Ensures proper code analysis and symbol recognition

**Example Use Cases**:

- After manual file edits outside of Serena
- When language server becomes unresponsive
- After switching between different development environments

### 7. `summarize_changes`

**Purpose**: Provides instructions for summarizing the changes made to the codebase.

**Usage**:

- Generates summaries of code changes
- Useful for documentation and change tracking
- Provides structured change reports

**Example Use Cases**:

- Creating change logs
- Documenting modifications
- Generating project update summaries

### 8. `switch_modes`

**Purpose**: Activates modes by providing a list of their names.

**Usage**:

- Dynamically switches between different Serena modes
- Allows adaptation to different types of tasks
- Can combine multiple modes for complex workflows

**Example Use Cases**:

- Switching between planning and editing modes
- Activating specialized modes for specific tasks
- Combining modes for complex development workflows

## Mode Examples

Serena supports various modes that can be activated using `switch_modes`:

- `planning`: Focuses on planning and analysis tasks
- `editing`: Optimizes for direct code modification tasks
- `interactive`: Suitable for conversational interaction
- `one-shot`: Configures for single-response tasks
- `no-onboarding`: Skips initial onboarding process
- `onboarding`: Focuses on project onboarding

## Best Practices

1. **Use `get_current_config`** to understand available tools and current state
2. **Use `switch_modes`** to adapt Serena's behavior to your current task
3. **Use `restart_language_server`** when experiencing analysis issues
4. **Use `summarize_changes`** for documenting modifications
5. **Use precise editing tools** (`delete_lines`, `insert_at_line`, `replace_lines`) for surgical code changes

## Troubleshooting

### Language Server Issues

If you experience issues with code analysis or symbol recognition:

1. Use `restart_language_server` to restart the language server
2. Check `get_current_config` to verify tool availability
3. Ensure the project is properly indexed

### Tool Availability

If optional tools are not available:

1. Verify the `included_optional_tools` configuration in `.serena/project.yml`
2. Restart the Serena MCP server
3. Check the project configuration with `get_current_config`

### Mode Management

To switch modes during a session:

1. Use `switch_modes` with the desired mode names
2. Combine multiple modes as needed (e.g., `["planning", "editing"]`)
3. Use `get_current_config` to verify active modes

## Configuration Files

The optional tools are configured in:

- **Project Level**: `.serena/project.yml` (current configuration)
- **Global Level**: `~/.serena/serena_config.yml` (user-wide settings)

## Next Steps

1. **Test the tools**: Try using each optional tool to understand their capabilities
2. **Explore modes**: Experiment with different mode combinations
3. **Customize further**: Modify the configuration as needed for your workflow
4. **Document usage**: Keep track of which tools work best for different tasks

## Additional Resources

- [Serena Documentation](https://github.com/oraios/serena)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Project README](../README.md)

---

*This configuration enables advanced Serena functionality for the market-parser-polygon-mcp project. All optional tools are now available for use in your development workflow.*
