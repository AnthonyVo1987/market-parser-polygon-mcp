# Claude Code Slash Commands Reference Guide

**Version:** 1.0  
**Created:** 2025-01-07  
**Target Audience:** AI coding agents and developers creating Claude Code custom slash commands

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Technical Specifications](#technical-specifications)
3. [Syntax and Format Guide](#syntax-and-format-guide)
4. [Specialist Integration](#specialist-integration)
5. [MCP Tool Requirements](#mcp-tool-requirements)
6. [Workflow Implementation](#workflow-implementation)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)
9. [Examples and Templates](#examples-and-templates)
10. [Troubleshooting Guide](#troubleshooting-guide)

---

## Introduction and Overview

### What are Claude Code Custom Slash Commands

Claude Code slash commands are custom automation tools that extend Claude's capabilities within the Claude Code IDE environment. They are implemented as markdown files with YAML frontmatter that define reusable workflows, analysis patterns, and automation sequences.

### How They Work

**Architecture:**
- Markdown files with YAML frontmatter configuration
- Stored in project directories and loaded by Claude Code
- Executed as structured prompts with defined parameters
- Can invoke specialist agents and coordinate multi-step workflows

**Execution Model:**
- Commands are invoked using `/command-name` syntax
- Claude Code parses the markdown content and frontmatter
- Executes the defined workflow with specified tools and constraints
- Can operate in Plan mode (analysis) or Direct mode (execution)

**File Naming vs Invocation:**
- File: `my-analysis-command.md`
- Invocation: `/my-analysis-command`
- Naming convention: kebab-case with descriptive names

---

## Technical Specifications

### Required Markdown Format

All slash commands must follow this structure:

```markdown
---
description: "Brief description of what this command does"
category: "Category Name"
# Additional frontmatter fields...
---

# Command Name

Command content and instructions...
```

### Frontmatter Requirements

**Required Fields:**
```yaml
description: "Clear, concise description of command purpose"
category: "Logical grouping category"
```

**Optional Fields:**
```yaml
argument-hint: "Description of expected arguments"
allowed-tools: ["tool1", "tool2", "tool3"]  # Restrict available tools
model: "claude-sonnet-4"  # Specify model requirements
```

### File Structure and Organization

**Recommended Directory Structure:**
```
project-root/
├── .claude/
│   └── commands/
│       ├── analysis/
│       │   ├── code-review.md
│       │   └── security-audit.md
│       ├── development/
│       │   ├── feature-implementation.md
│       │   └── bug-fix-workflow.md
│       └── documentation/
│           ├── api-documentation.md
│           └── readme-update.md
```

---

## Syntax and Format Guide

### Proper Markdown Structure

**Standard Template:**
```markdown
---
description: "Command description"
category: "Category"
argument-hint: "Expected arguments format"
---

# Command Title

## Overview
Brief explanation of command purpose and scope.

## Workflow Steps
1. **Step 1**: Description
2. **Step 2**: Description
3. **Step 3**: Description

## Execution Instructions
Detailed instructions for execution, including:
- Tool requirements
- Specialist assignments
- Quality gates
- Expected outputs

## Examples
Practical usage examples and expected results.
```

### Section Organization Patterns

**Consistent Header Hierarchy:**
- `# Command Name` (H1) - Main title
- `## Section Name` (H2) - Major sections
- `### Subsection` (H3) - Detailed breakdowns
- `#### Details` (H4) - Specific implementation details

### Content Formatting Standards

**Code Blocks:**
````markdown
```language
code content
```
````

**Task Lists:**
```markdown
- [ ] Task 1
- [ ] Task 2
- [x] Completed task
```

**Specialist Assignments:**
```markdown
**@specialist-name**: Specific task description
```

---

## Specialist Integration

### Agent Invocation Syntax

**Standard Pattern:**
```markdown
**@agent-name**: Task description with specific requirements
```

**Available Specialists:**
- `@code-reviewer`: Quality assurance and security reviews
- `@backend-developer`: Backend development tasks
- `@react-component-architect`: Frontend React development
- `@api-architect`: API design and integration
- `@documentation-specialist`: Documentation creation and updates
- `@code-archaeologist`: Deep analysis and architectural decisions

### Specialist Coordination Patterns

**Sequential Coordination:**
```markdown
## Workflow Steps

1. **@code-archaeologist**: Analyze current architecture and identify requirements
2. **@backend-developer**: Implement backend functionality based on analysis
3. **@api-architect**: Design API contracts and integration patterns
4. **@react-component-architect**: Build frontend components
5. **@code-reviewer**: MANDATORY quality review before completion
```

**Parallel Coordination:**
```markdown
## Parallel Tasks

**Execute simultaneously:**
- **@backend-developer**: Implement API endpoints
- **@react-component-architect**: Build React components
- **@documentation-specialist**: Update API documentation

**Then:**
- **@code-reviewer**: Review all changes together
```

### Role Assignment and Responsibility Delegation

**Clear Responsibility Matrix:**
```markdown
| Task Category | Specialist | Responsibilities | Required Tools |
|---------------|------------|------------------|----------------|
| Code Quality | @code-reviewer | Security, standards, validation | filesystem, sequential-thinking |
| Backend Logic | @backend-developer | Python, APIs, data processing | filesystem, context7 |
| Frontend UI | @react-component-architect | React, components, UX | filesystem, context7 |
```

---

## MCP Tool Requirements

### Enforcing MCP Tool Usage

**Standard Enforcement Pattern:**
```markdown
## MCP Tool Requirements

**ALL specialists MUST use MCP tools:**
- `mcp__sequential-thinking__sequentialthinking` - For systematic analysis
- `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` - For research
- `mcp__filesystem__*` - For file operations

**Failure to use required MCP tools will result in work rejection.**
```

### Required Tool Patterns

**Analysis Pattern:**
```markdown
1. Use `mcp__sequential-thinking__sequentialthinking` for systematic problem breakdown
2. Use `mcp__context7__resolve-library-id` to find relevant documentation
3. Use `mcp__context7__get-library-docs` to fetch current best practices
4. Use `mcp__filesystem__*` for all file operations
```

**Development Pattern:**
```markdown
1. `mcp__filesystem__read_text_file` - Read existing code
2. `mcp__context7__get-library-docs` - Verify current patterns
3. `mcp__filesystem__edit_file` - Implement changes
4. `mcp__sequential-thinking__sequentialthinking` - Validate approach
```

### Tool Compliance Enforcement

**Validation Checkpoints:**
```markdown
## Quality Gates

**Before proceeding to next step, verify:**
- [ ] All specialists used required MCP tools
- [ ] Sequential thinking documented decision process
- [ ] Context7 provided current best practices
- [ ] Filesystem operations completed successfully
```

---

## Workflow Implementation

### Complex Multi-Step Workflows

**Structured Workflow Template:**
```markdown
## Implementation Workflow

### Phase 1: Analysis and Planning
1. **@code-archaeologist**: 
   - Use `mcp__sequential-thinking__sequentialthinking` for systematic analysis
   - Use `mcp__filesystem__read_multiple_files` to examine current state
   - Document findings and recommendations

### Phase 2: Development
2. **@backend-developer**:
   - Use `mcp__context7__get-library-docs` for current best practices
   - Use `mcp__filesystem__edit_file` for implementation
   - Follow established patterns and security requirements

### Phase 3: Integration
3. **@api-architect**:
   - Design clean API contracts
   - Ensure frontend-backend compatibility
   - Document integration patterns

### Phase 4: Quality Assurance
4. **@code-reviewer**:
   - MANDATORY security and quality review
   - Validate all changes meet standards
   - Approve before final implementation
```

### Conditional Logic Implementation

**Plan vs Execution Modes:**
```markdown
## Execution Modes

**Plan Mode** (analysis only):
- Generate detailed implementation plan
- Identify potential issues and dependencies
- Provide time and resource estimates
- No actual code changes

**Execute Mode** (full implementation):
- Follow planned approach with real changes
- Update code, documentation, and tests
- Validate results and complete workflow
- Commit changes with proper messages
```

**Conditional Branching:**
```markdown
## Conditional Workflow

**IF** project uses React:
- **@react-component-architect**: Handle frontend implementation
- Use React-specific MCP documentation

**ELSE IF** project uses Vue:
- **@frontend-developer**: Handle Vue implementation
- Use Vue-specific documentation patterns

**ELSE**:
- **@backend-developer**: Focus on backend-only solution
```

### Quality Gates and Validation Checkpoints

**Standard Quality Gates:**
```markdown
## Quality Validation Checkpoints

### Checkpoint 1: Requirements Validation
- [ ] All requirements clearly understood
- [ ] Dependencies identified and available
- [ ] Resource requirements estimated

### Checkpoint 2: Implementation Validation
- [ ] Code follows established patterns
- [ ] Security requirements satisfied
- [ ] Performance impact assessed

### Checkpoint 3: Integration Validation
- [ ] Components integrate correctly
- [ ] API contracts maintained
- [ ] Documentation updated

### Checkpoint 4: Final Approval
- [ ] **@code-reviewer** approval obtained
- [ ] All tests passing
- [ ] Ready for deployment/merge
```

---

## Best Practices

### Command Naming Conventions

**Guidelines:**
- Use kebab-case: `feature-implementation.md`
- Be descriptive: `security-audit-comprehensive.md`
- Include scope: `api-documentation-update.md`
- Avoid abbreviations: `documentation` not `docs`

**Examples:**
- `code-review-security-focused.md`
- `backend-api-implementation.md`
- `react-component-optimization.md`
- `database-migration-workflow.md`

### Single Responsibility Principle

**Good Examples:**
```markdown
# API Documentation Update
Focused solely on updating API documentation

# Security Audit
Comprehensive security analysis only

# Feature Implementation
Complete feature development workflow
```

**Bad Examples:**
```markdown
# Everything Workflow
# Mixed Tasks Command
# General Purpose Tool
```

### Clear Documentation Standards

**Required Documentation Elements:**
```markdown
## Command Documentation Requirements

1. **Purpose**: Clear statement of command objective
2. **Scope**: What is included and excluded
3. **Prerequisites**: Required tools, permissions, environment
4. **Inputs**: Expected parameters and formats
5. **Outputs**: Deliverables and success criteria
6. **Examples**: Practical usage demonstrations
```

### Maintenance and Update Guidelines

**Version Control:**
```markdown
---
description: "Command description"
category: "Category"
version: "1.2.0"
last-updated: "2025-01-07"
author: "Agent Name"
---
```

**Change Log Pattern:**
```markdown
## Change Log

### v1.2.0 (2025-01-07)
- Enhanced MCP tool integration
- Added React component support
- Improved error handling

### v1.1.0 (2025-01-05)
- Added specialist coordination
- Updated documentation patterns

### v1.0.0 (2025-01-01)
- Initial implementation
```

---

## Common Patterns

### Task Automation Workflows

**Standard Automation Template:**
```markdown
---
description: "Automate routine development tasks"
category: "Automation"
---

# Task Automation

## Automated Tasks
1. Code formatting and linting
2. Dependency updates
3. Documentation synchronization
4. Test execution and validation

## Implementation
**@backend-developer**: Execute automation sequence
- Use `mcp__filesystem__read_multiple_files` to check current state
- Apply automated improvements
- Validate results and report status
```

### Analysis and Research Commands

**Research Pattern:**
```markdown
---
description: "Research and analyze technical topics"
category: "Analysis"
---

# Technical Research

## Research Methodology
1. **@code-archaeologist**: Use `mcp__sequential-thinking__sequentialthinking` 
   - Break down research questions systematically
   - Identify key areas for investigation

2. **Research Execution**: Use `mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs`
   - Gather current best practices
   - Analyze existing solutions
   - Document findings and recommendations

## Deliverables
- Comprehensive analysis report
- Recommendations with rationale
- Implementation guidance
```

### Code Generation and Modification

**Code Generation Template:**
```markdown
---
description: "Generate or modify code following established patterns"
category: "Development"
---

# Code Generation Workflow

## Generation Process
1. **@code-archaeologist**: Analyze existing patterns
   - Use `mcp__filesystem__read_multiple_files`
   - Document current architecture

2. **@backend-developer** or **@react-component-architect**: Generate code
   - Use `mcp__context7__get-library-docs` for current standards
   - Use `mcp__filesystem__write_file` or `mcp__filesystem__edit_file`
   - Follow established patterns and conventions

3. **@code-reviewer**: Validate generated code
   - Security and quality review
   - Standards compliance verification
```

### Documentation and Reporting

**Documentation Pattern:**
```markdown
---
description: "Create or update project documentation"
category: "Documentation"
---

# Documentation Update

## Documentation Workflow
1. **@documentation-specialist**: Lead documentation efforts
   - Use `mcp__filesystem__read_multiple_files` to understand current state
   - Use `mcp__sequential-thinking__sequentialthinking` for systematic approach
   - Create comprehensive, accurate documentation

## Quality Standards
- Clear, actionable content
- Consistent formatting and structure
- Practical examples and templates
- Easy navigation and reference
```

---

## Examples and Templates

### Well-Structured Command Example

```markdown
---
description: "Implement comprehensive feature with testing and documentation"
category: "Development"
argument-hint: "feature-name and requirements description"
---

# Feature Implementation Workflow

## Overview
Comprehensive workflow for implementing new features with full testing, documentation, and quality assurance.

## Prerequisites
- Feature requirements clearly defined
- Development environment setup
- Required dependencies available

## Workflow Steps

### Phase 1: Analysis and Planning
1. **@code-archaeologist**: Systematic analysis
   - Use `mcp__sequential-thinking__sequentialthinking` for requirement breakdown
   - Use `mcp__filesystem__read_multiple_files` to understand current architecture
   - Document implementation approach and dependencies

### Phase 2: Backend Implementation
2. **@backend-developer**: Core functionality
   - Use `mcp__context7__get-library-docs` for current best practices
   - Use `mcp__filesystem__edit_file` for implementation
   - Include comprehensive error handling and validation

### Phase 3: API Design
3. **@api-architect**: Integration contracts
   - Design clean, RESTful API interfaces
   - Ensure backward compatibility
   - Document API specifications

### Phase 4: Frontend Implementation
4. **@react-component-architect**: User interface
   - Use `mcp__context7__get-library-docs` for React best practices
   - Build responsive, accessible components
   - Integrate with backend APIs

### Phase 5: Documentation
5. **@documentation-specialist**: Comprehensive documentation
   - Update API documentation
   - Create user guides and examples
   - Update architecture documentation

### Phase 6: Quality Assurance
6. **@code-reviewer**: Final validation (MANDATORY)
   - Security and performance review
   - Code quality and standards compliance
   - Integration testing validation

## Success Criteria
- [ ] Feature implemented according to requirements
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code review approved
- [ ] Performance benchmarks met

## Example Usage
`/feature-implementation "user authentication" "OAuth2 integration with social login"`
```

### Template Patterns for Common Use Cases

**Quick Analysis Template:**
```markdown
---
description: "Quick analysis of specific codebase aspect"
category: "Analysis"
---

# Quick Analysis: [ASPECT]

## Analysis Target
[Specify what to analyze]

## Approach
**@code-archaeologist**: 
- Use `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Use `mcp__filesystem__read_multiple_files` to examine relevant files
- Provide concise findings and recommendations

## Deliverable
Brief analysis report with actionable insights.
```

**Simple Update Template:**
```markdown
---
description: "Update specific component or documentation"
category: "Maintenance"
---

# Update: [COMPONENT_NAME]

## Update Requirements
[Specify what needs updating]

## Implementation
**@[appropriate-specialist]**:
- Use `mcp__filesystem__read_text_file` to check current state
- Use `mcp__context7__get-library-docs` if research needed
- Use `mcp__filesystem__edit_file` to make updates
- Validate changes work correctly

**@code-reviewer**: Quick validation review

## Success Criteria
- [ ] Update completed successfully
- [ ] No breaking changes introduced
- [ ] Documentation reflects changes
```

### Real-World Implementation Samples

**Security Audit Command:**
```markdown
---
description: "Comprehensive security audit of codebase"
category: "Security"
---

# Security Audit

## Audit Scope
- Authentication and authorization mechanisms
- Input validation and sanitization
- API security and rate limiting
- Dependency vulnerabilities
- Configuration security

## Execution Workflow

### Phase 1: Automated Security Scanning
**@code-archaeologist**:
- Use `mcp__sequential-thinking__sequentialthinking` for systematic approach
- Use `mcp__filesystem__read_multiple_files` to examine security-critical files
- Document findings with severity levels

### Phase 2: Manual Security Review
**@code-reviewer**: 
- Deep dive into authentication flows
- Review API security implementation
- Validate input sanitization
- Check for common security vulnerabilities

### Phase 3: Remediation Planning
**@backend-developer**:
- Prioritize security issues by risk level
- Create implementation plan for fixes
- Estimate effort and timeline

## Deliverables
- Security audit report with findings
- Prioritized remediation plan
- Implementation timeline
```

**API Documentation Generation:**
```markdown
---
description: "Generate comprehensive API documentation"
category: "Documentation"
---

# API Documentation Generation

## Documentation Scope
- All API endpoints with examples
- Request/response schemas
- Authentication requirements
- Error handling patterns

## Implementation Process

### Phase 1: API Analysis
**@api-architect**:
- Use `mcp__filesystem__read_multiple_files` to analyze API code
- Use `mcp__sequential-thinking__sequentialthinking` for systematic documentation
- Extract all endpoints, parameters, and responses

### Phase 2: Documentation Creation
**@documentation-specialist**:
- Use `mcp__context7__get-library-docs` for OpenAPI best practices
- Generate comprehensive API documentation
- Include practical examples and use cases
- Create developer-friendly reference guide

### Phase 3: Validation
**@code-reviewer**:
- Verify technical accuracy
- Ensure completeness and clarity
- Validate examples work correctly

## Success Criteria
- [ ] All endpoints documented
- [ ] Examples tested and working
- [ ] Clear, developer-friendly format
- [ ] Searchable and navigable structure
```

---

## Troubleshooting Guide

### Common Issues and Solutions

**Issue: Command Not Recognized**
```
Symptoms: `/command-name` not found or not executing
Solutions:
1. Check file naming: ensure kebab-case and .md extension
2. Verify frontmatter: description and category required
3. Check file location: must be in accessible directory
4. Validate YAML syntax: use YAML validator
```

**Issue: MCP Tools Not Working**
```
Symptoms: "Tool not found" or execution errors
Solutions:
1. Verify tool names: use exact MCP tool identifiers
2. Check tool availability: ensure MCP tools are loaded
3. Validate parameters: match required parameter schemas
4. Use proper tool invocation syntax in commands
```

**Issue: Specialist Assignment Failures**
```
Symptoms: Agents not responding to @specialist assignments
Solutions:
1. Use exact specialist names from agent configuration
2. Provide clear, specific task descriptions
3. Include required tools and success criteria
4. Ensure specialists are available in current environment
```

**Issue: Workflow Execution Stalls**
```
Symptoms: Commands start but don't complete
Solutions:
1. Add explicit quality gates and checkpoints
2. Include timeout and error handling instructions
3. Break complex workflows into smaller steps
4. Add progress reporting requirements
```

### Debug Approaches for Failed Commands

**Systematic Debugging Process:**

1. **Validate Command Structure**
   ```markdown
   ## Debug Checklist
   - [ ] Valid YAML frontmatter
   - [ ] Required fields present
   - [ ] Markdown syntax correct
   - [ ] Clear section organization
   ```

2. **Test Tool Integration**
   ```markdown
   ## Tool Testing
   - [ ] MCP tools available and responding
   - [ ] Tool parameters match schemas
   - [ ] Required permissions present
   - [ ] Network connectivity for external tools
   ```

3. **Validate Specialist Assignments**
   ```markdown
   ## Agent Testing
   - [ ] Specialist names correct
   - [ ] Task descriptions specific and actionable
   - [ ] Success criteria clearly defined
   - [ ] Required tools specified for each specialist
   ```

4. **Workflow Logic Verification**
   ```markdown
   ## Workflow Testing
   - [ ] Step dependencies clearly defined
   - [ ] No circular dependencies
   - [ ] Error handling included
   - [ ] Success criteria measurable
   ```

### Validation and Testing Strategies

**Command Validation Framework:**
```markdown
## Pre-Deployment Validation

### Syntax Validation
1. YAML frontmatter parser check
2. Markdown structure validation
3. Tool name and parameter verification
4. Specialist assignment syntax check

### Functional Testing
1. Execute command in isolated environment
2. Verify all tools respond correctly
3. Confirm specialist assignments work
4. Validate output meets expectations

### Integration Testing
1. Test command with real project data
2. Verify integration with existing workflows
3. Confirm no conflicts with other commands
4. Validate performance impact acceptable
```

**Testing Checklist Template:**
```markdown
## Command Testing Checklist

### Basic Functionality
- [ ] Command loads without errors
- [ ] Frontmatter parsed correctly
- [ ] Instructions clear and actionable
- [ ] All required tools available

### Tool Integration
- [ ] MCP tools respond correctly
- [ ] Tool parameters validated
- [ ] Error handling works properly
- [ ] Outputs in expected format

### Specialist Coordination
- [ ] All specialists assigned correctly
- [ ] Task descriptions sufficiently detailed
- [ ] Success criteria clearly defined
- [ ] Quality gates implemented

### Workflow Execution
- [ ] Steps execute in correct order
- [ ] Dependencies handled properly
- [ ] Error recovery works
- [ ] Final deliverables produced
```

### Performance Optimization Tips

**Optimization Strategies:**

1. **Efficient Tool Usage**
   ```markdown
   ## Performance Best Practices
   - Use `mcp__filesystem__read_multiple_files` instead of multiple single reads
   - Cache Context7 documentation lookups when possible
   - Minimize sequential-thinking steps for simple tasks
   - Group related file operations together
   ```

2. **Workflow Optimization**
   ```markdown
   ## Workflow Efficiency
   - Execute independent tasks in parallel
   - Minimize context switching between specialists
   - Use conditional logic to skip unnecessary steps
   - Implement early exit conditions for common scenarios
   ```

3. **Resource Management**
   ```markdown
   ## Resource Optimization
   - Specify exact tool requirements in frontmatter
   - Use appropriate model for task complexity
   - Implement timeout and retry logic
   - Clean up temporary resources
   ```

**Performance Monitoring:**
```markdown
## Performance Metrics

### Execution Time Tracking
- Command initialization time
- Tool execution duration
- Specialist response times
- Overall workflow completion time

### Resource Usage Monitoring
- File operation counts
- API call frequencies
- Memory usage patterns
- Network request volumes

### Optimization Targets
- < 30 seconds for simple commands
- < 5 minutes for complex workflows
- Minimal redundant operations
- Efficient resource utilization
```

---

## Conclusion

This comprehensive guide provides the foundation for creating, maintaining, and optimizing Claude Code slash commands. By following these patterns and best practices, AI coding agents can build robust, maintainable automation tools that enhance development workflows and maintain code quality standards.

For additional support or to report issues with this guide, please reference the project documentation or create an issue in the project repository.

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-07  
**Next Review:** 2025-04-07