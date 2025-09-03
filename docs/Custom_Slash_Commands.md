# Claude Code Custom Slash Commands Reference Guide

## Table of Contents
- [Overview](#overview)
- [Command Structure and Syntax](#command-structure-and-syntax)
- [Creating Custom Commands](#creating-custom-commands)
- [Advanced Features](#advanced-features)
- [Command Organization](#command-organization)
- [Best Practices](#best-practices)
- [Examples and Templates](#examples-and-templates)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Overview

Custom slash commands in Claude Code allow you to create reusable prompts stored as Markdown files. These commands streamline repetitive tasks, ensure consistency across your team, and can be customized with arguments for dynamic behavior.

### Command Types
- **Built-in Commands**: Predefined commands provided by Claude Code (e.g., `/config`, `/permissions`, `/vim`)
- **Custom Commands**: User-defined commands stored as Markdown files
- **MCP Commands**: Commands exposed by Model Context Protocol servers (format: `/mcp__<server>__<prompt>`)

### Command Scopes
- **Project Commands**: Shared with team members (`.claude/commands/` directory)
- **Personal Commands**: Available across all your projects (`~/.claude/commands/` directory)

## Command Structure and Syntax

### Basic Syntax
```
/<command-name> [arguments]
```

### File Structure
Commands are stored as Markdown files where:
- **Filename** (without `.md` extension) becomes the command name
- **File content** becomes the prompt sent to Claude
- **Arguments** can be passed using `$ARGUMENTS` placeholder

## Creating Custom Commands

### Project-Specific Commands
Create commands that all team members can use:

```bash
# Create commands directory
mkdir -p .claude/commands

# Create a basic command
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md

# Use the command
> /optimize
```

### Personal Commands
Create commands for your personal use across all projects:

```bash
# Create personal commands directory
mkdir -p ~/.claude/commands

# Create a personal command
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md

# Use the command
> /security-review
```

### Commands with Arguments
Create flexible commands that accept dynamic input:

```bash
# Create command with argument placeholder
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md

# Use with arguments
> /fix-issue 123
```

## Advanced Features

### Frontmatter Configuration
Use YAML frontmatter to configure command behavior:

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

#### Frontmatter Options
- **allowed-tools**: Restrict which tools Claude can use
- **argument-hint**: Provide guidance for command arguments
- **description**: Human-readable description of the command
- **model**: Specify which Claude model to use

### Bash Command Execution
Execute bash commands and include their output in the prompt:

```markdown
---
allowed-tools: Bash(git status:*), Bash(git log:*)
---

## Current Repository Status

Current status: !`git status --porcelain`
Recent commits: !`git log --oneline -5`

Please analyze the current state and suggest next steps.
```

### File References
Reference file contents directly in commands:

```bash
# Reference a specific file
> Review the implementation in @src/utils/helpers.js

# Reference multiple files
> Compare @src/old-version.js with @src/new-version.js
```

## Command Organization

### Directory Structure
Commands can be organized using subdirectories:

```
.claude/
└── commands/
    ├── git/
    │   ├── commit.md
    │   └── review.md
    ├── testing/
    │   ├── unit-test.md
    │   └── integration-test.md
    └── docs/
        └── update.md
```

### Namespacing
Use descriptive names and organize by function:
- `git-commit.md` - Git-related commit command
- `test-unit.md` - Unit testing command
- `review-security.md` - Security review command
- `docs-update.md` - Documentation update command

## Best Practices

### Command Design
1. **Single Purpose**: Each command should have one clear purpose
2. **Clear Naming**: Use descriptive, hyphenated names (e.g., `fix-bug`, `review-code`)
3. **Consistent Format**: Follow a standard structure across commands
4. **Proper Documentation**: Include clear descriptions and examples

### Content Guidelines
1. **Imperative Mood**: Write prompts in present tense imperative mood
2. **Specific Instructions**: Provide clear, actionable guidance
3. **Context Inclusion**: Use bash commands or file references for relevant context
4. **Error Handling**: Consider edge cases and provide guidance

### Team Collaboration
1. **Version Control**: Include `.claude/commands/` in your repository
2. **Documentation**: Document custom commands in your project README
3. **Standards**: Establish team conventions for command structure
4. **Review Process**: Review command changes like any other code

## Examples and Templates

### Basic Code Review Command
```markdown
<!-- .claude/commands/review.md -->
---
description: Perform a comprehensive code review
argument-hint: [file-pattern]
---

Please perform a thorough code review focusing on:
- Code quality and readability
- Performance considerations
- Security vulnerabilities
- Best practices adherence
- Documentation completeness

$ARGUMENTS
```

### Git Commit Command
```markdown
<!-- .claude/commands/commit.md -->
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit with proper message
---

## Current Changes

Status: !`git status --porcelain`
Staged changes: !`git diff --cached`
Unstaged changes: !`git diff`

Create a commit with a conventional commit message following this format:
- feat: new feature
- fix: bug fix  
- docs: documentation changes
- style: formatting changes
- refactor: code refactoring
- test: adding tests
- chore: maintenance

Use present tense and keep the first line under 50 characters.
```

### Issue Analysis Command
```markdown
<!-- .claude/commands/analyze-issue.md -->
---
description: Analyze and plan solution for GitHub issue
argument-hint: [issue-number]
---

Please analyze issue #$ARGUMENTS and provide:

1. **Problem Summary**: Brief description of the issue
2. **Root Cause Analysis**: Likely causes and affected components  
3. **Solution Approach**: Step-by-step implementation plan
4. **Testing Strategy**: How to verify the fix works
5. **Risk Assessment**: Potential side effects or complications

Include relevant code examples and file references where applicable.
```

### Documentation Update Command
```markdown
<!-- .claude/commands/update-docs.md -->
---
description: Update project documentation
allowed-tools: Read(*), Bash(find:*)
---

Current documentation structure: !`find docs/ -name "*.md" | head -20`

Please review and update the documentation ensuring:
- Accuracy with current codebase
- Clear examples and usage instructions  
- Proper formatting and structure
- Updated links and references
- Comprehensive coverage of new features

Focus on: $ARGUMENTS
```

### Testing Command Template
```markdown
<!-- .claude/commands/create-tests.md -->
---
description: Create comprehensive tests for code
argument-hint: [file-path]
---

For the code in $ARGUMENTS, please create:

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test component interactions
3. **Edge Cases**: Test boundary conditions and error scenarios
4. **Mock Requirements**: Identify external dependencies to mock

Follow these testing principles:
- Arrange-Act-Assert pattern
- Descriptive test names
- Independent, repeatable tests
- Comprehensive coverage of happy path and error cases
```

## Troubleshooting

### Common Issues

#### Command Not Found
**Problem**: Command doesn't appear when typing `/`
**Solutions**:
- Verify file is in correct directory (`.claude/commands/` or `~/.claude/commands/`)
- Check file extension is `.md`
- Ensure filename follows valid naming conventions (no spaces, use hyphens)
- Restart Claude Code session

#### Arguments Not Substituted
**Problem**: `$ARGUMENTS` appears literally in output
**Solutions**:
- Verify exact spelling: `$ARGUMENTS` (case-sensitive)
- Check that arguments were provided when invoking command
- Ensure no extra spaces around `$ARGUMENTS`

#### Bash Commands Not Executing
**Problem**: Commands with `!` prefix not running
**Solutions**:
- Add required tools to `allowed-tools` in frontmatter
- Verify bash command syntax is correct
- Check that tools are available in current environment
- Use absolute paths if necessary

#### Permission Errors
**Problem**: Claude cannot execute certain commands
**Solutions**:
- Review and update `allowed-tools` in command frontmatter
- Check Claude Code permission settings with `/permissions`
- Verify file permissions on referenced scripts
- Use appropriate tool restrictions

### Debugging Commands

#### Test Command Syntax
```bash
# Check if command file exists
ls -la .claude/commands/your-command.md

# View command content
cat .claude/commands/your-command.md

# Test bash commands separately
git status --porcelain
```

#### Validate Frontmatter
```yaml
# Valid frontmatter example
---
allowed-tools: Bash(git:*), Read(*)
argument-hint: [description]
description: Test command
---
```

## References

### Official Documentation
- [Claude Code Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)

### Community Resources
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) - Comprehensive collection of slash commands and resources
- [Claude Code Cookbook](https://github.com/wasabeef/claude-code-cookbook) - Collection of settings and custom commands

### Tools and Integrations
- [MCP Servers](https://docs.anthropic.com/en/docs/claude-code/mcp) - Model Context Protocol integration
- [GitHub Actions](https://docs.anthropic.com/en/docs/claude-code/github-actions) - CI/CD integration
- [IDE Integrations](https://docs.anthropic.com/en/docs/claude-code/ide-integrations) - Editor plugins

---

*This reference guide was generated using Claude Code research and best practices from the community. For the latest information, refer to the official Claude Code documentation.*