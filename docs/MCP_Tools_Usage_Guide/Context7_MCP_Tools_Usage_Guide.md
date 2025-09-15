# Context7 MCP Tools Usage Guide - Market Parser Application

> **Target Audience**: AI Coding Agents working on Market Parser application  
> **Purpose**: Focused Context7 MCP tools usage guide for our React/FastAPI/Pydantic AI tech stack  
> **Last Updated**: 2025-09-15

## Executive Summary

Context7 MCP provides two essential tools for accessing up-to-date documentation and code examples for libraries used in our Market Parser application. This guide focuses specifically on correct usage patterns for our React 18.2+/Vite 5.2+ frontend and FastAPI/OpenAI Agents SDK/OpenAI GPT-5-mini backend stack.

## Market Parser Tech Stack Context

**Frontend Stack:**
- React 18.2+ with functional components and hooks
- Vite 5.2+ build system (262ms startup)
- TypeScript with full type safety
- Custom CSS with responsive design
- npm package management

**Backend Stack:**
- FastAPI with Python 3.10+
- OpenAI Agents SDK (v0.2.8) for agent framework
- OpenAI GPT-5-mini via OpenAI Agents SDK
- Polygon.io MCP server integration via uvx
- uv package management
- Rich console for emoji-based responses

**Testing & Development:**
- Playwright for E2E testing
- ESLint/Prettier for code quality
- Static ports: Backend (8000), Frontend dev (3000), Frontend prod (5500)

## Context7 MCP Tools Overview

Context7 provides two sequential tools that must be used together:

1. **`mcp__context7__resolve-library-id`** - Resolves library names to Context7-compatible IDs
2. **`mcp__context7__get-library-docs`** - Retrieves documentation using resolved IDs

## Tool 1: resolve-library-id

### Purpose
Converts human-readable library names into Context7-compatible library IDs required for documentation retrieval.

### Correct Usage Conditions for Market Parser App

✅ **Use when researching:**
- React patterns and hooks: `"react"`
- Vite build optimization: `"vite"`
- TypeScript patterns: `"typescript"`
- FastAPI development: `"fastapi"`
- OpenAI Agents SDK: `"openai-agents"`
- OpenAI SDK integration: `"openai"`
- Playwright testing: `"playwright"`
- npm package management: `"npm"`
- Python package management: `"uv"`

### Incorrect Usage Conditions

❌ **Do NOT use for:**
- Generic programming concepts (use existing knowledge)
- Project-specific code analysis (use filesystem tools)
- Debugging existing code (use other analysis tools)
- Internal API documentation (use codebase files)

### Correct Tool Input

```javascript
mcp__context7__resolve-library-id
{
  "libraryName": "react"  // Exact library name, lowercase, no spaces
}
```

### Expected Tool Output

```json
{
  "libraries": [
    {
      "title": "React",
      "context7CompatibleLibraryID": "/facebook/react",
      "description": "React library for building user interfaces",
      "codeSnippets": 1234,
      "trustScore": 9.8
    }
  ]
}
```

### Correct Examples for Market Parser App

**Frontend Development Research:**
```javascript
// Research React 18+ patterns
mcp__context7__resolve-library-id({"libraryName": "react"})
// Expected: "/facebook/react"

// Research Vite build optimization
mcp__context7__resolve-library-id({"libraryName": "vite"})
// Expected: "/vitejs/vite"

// Research TypeScript patterns
mcp__context7__resolve-library-id({"libraryName": "typescript"})
// Expected: "/microsoft/typescript"
```

**Backend Development Research:**
```javascript
// Research FastAPI patterns
mcp__context7__resolve-library-id({"libraryName": "fastapi"})
// Expected: "/tiangolo/fastapi"

// Research OpenAI Agents SDK usage
mcp__context7__resolve-library-id({"libraryName": "openai-agents"})
// Expected: "/openai/openai-agents"

// Research OpenAI SDK
mcp__context7__resolve-library-id({"libraryName": "openai"})
// Expected: "/openai/openai-python"
```

**Testing & Development Research:**
```javascript
// Research Playwright testing
mcp__context7__resolve-library-id({"libraryName": "playwright"})
// Expected: "/microsoft/playwright"

// Research ESLint patterns
mcp__context7__resolve-library-id({"libraryName": "eslint"})
// Expected: "/eslint/eslint"
```

### Incorrect Examples

❌ **Wrong Input Formats:**
```javascript
// Don't guess Context7 IDs
mcp__context7__resolve-library-id({"libraryName": "/facebook/react"})

// Don't use complex descriptions
mcp__context7__resolve-library-id({"libraryName": "React library for building UIs"})

// Don't use version numbers
mcp__context7__resolve-library-id({"libraryName": "react@18.2"})
```

## Tool 2: get-library-docs

### Purpose
Retrieves up-to-date documentation and code examples using Context7-compatible library IDs from resolve-library-id.

### Correct Usage Conditions for Market Parser App

✅ **Use when needing:**
- Current API syntax and patterns
- Modern React hooks patterns (useState, useEffect, useCallback)
- Vite configuration and optimization techniques
- FastAPI routing and dependency injection patterns
- OpenAI Agents SDK implementation patterns
- OpenAI Agents SDK implementation patterns
- Playwright testing automation patterns
- ESLint configuration for TypeScript/React

### Incorrect Usage Conditions

❌ **Do NOT use for:**
- Basic programming concepts that don't change
- Project-specific implementation details
- Debugging sessions for existing code
- Internal documentation or comments

### Correct Tool Input

```javascript
mcp__context7__get-library-docs
{
  "context7CompatibleLibraryID": "/facebook/react",  // From resolve-library-id
  "topic": "hooks useState useEffect",              // Optional: focus area
  "tokens": 5000                                    // Optional: response size
}
```

### Expected Tool Output

```json
{
  "documentation": "## React Hooks\n\n### useState Hook\n...",
  "codeSnippets": [
    {
      "title": "useState Hook Example",
      "code": "const [count, setCount] = useState(0);",
      "language": "javascript"
    }
  ],
  "version": "18.2.0"
}
```

### Correct Examples for Market Parser App

**Frontend Development Patterns:**
```javascript
// Research React hooks for our components
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "topic": "hooks useState useEffect useCallback",
  "tokens": 6000
})

// Research Vite build optimization for our 262ms startup
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/vitejs/vite",
  "topic": "performance optimization build speed",
  "tokens": 5000
})

// Research TypeScript patterns for our frontend
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/microsoft/typescript",
  "topic": "react typescript strict mode",
  "tokens": 4000
})
```

**Backend Development Patterns:**
```javascript
// Research FastAPI for our backend API
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/tiangolo/fastapi",
  "topic": "dependency injection cors middleware",
  "tokens": 7000
})

// Research OpenAI Agents SDK patterns
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/openai/openai-agents",
  "topic": "agent framework conversation management",
  "tokens": 8000
})

// Research OpenAI Agents SDK integration
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/openai/openai-python",
  "topic": "agents sdk conversation management",
  "tokens": 6000
})
```

**Testing & Development Patterns:**
```javascript
// Research Playwright for our E2E testing
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/microsoft/playwright",
  "topic": "browser automation react testing",
  "tokens": 5000
})

// Research ESLint configuration for our TypeScript/React setup
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/eslint/eslint",
  "topic": "typescript react configuration rules",
  "tokens": 4000
})
```

### Incorrect Examples

❌ **Wrong Usage Patterns:**
```javascript
// Don't use without resolving library ID first
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/guess/library-name"  // Wrong: not resolved
})

// Don't request excessive tokens for simple queries
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "tokens": 50000  // Wrong: excessive for simple query
})

// Don't use vague topics
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "topic": "everything"  // Wrong: too broad
})
```

## Market Parser App Integration Patterns

### Pattern 1: Frontend Component Development

```javascript
// 1. Research latest React patterns
mcp__context7__resolve-library-id({"libraryName": "react"})
// Result: "/facebook/react"

// 2. Get specific React hooks documentation
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "topic": "functional components hooks typescript",
  "tokens": 5000
})

// 3. Apply patterns to our Market Parser React components
// Use filesystem tools to implement changes
```

### Pattern 2: Backend API Development

```javascript
// 1. Research FastAPI patterns
mcp__context7__resolve-library-id({"libraryName": "fastapi"})
// Result: "/tiangolo/fastapi"

// 2. Get FastAPI documentation for our use case
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/tiangolo/fastapi",
  "topic": "cors middleware dependency injection pydantic",
  "tokens": 6000
})

// 3. Implement patterns in our Python backend
// Use filesystem tools for code changes
```

### Pattern 3: Testing Implementation

```javascript
// 1. Research Playwright testing
mcp__context7__resolve-library-id({"libraryName": "playwright"})
// Result: "/microsoft/playwright"

// 2. Get Playwright documentation for React testing
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/microsoft/playwright",
  "topic": "react component testing browser automation",
  "tokens": 5000
})

// 3. Implement tests for our Market Parser application
// Use filesystem tools to create test files
```

## Best Practices for Market Parser App

### Research Workflow

1. **Always resolve library ID first** - Never guess Context7 format
2. **Use specific topics** - Focus on our exact use case
3. **Appropriate token limits** - 4000-8000 for detailed research
4. **Sequential usage** - resolve-library-id → get-library-docs
5. **Document findings** - Save patterns for team reference

### Token Allocation Guidelines

- **Basic API usage**: 3000-4000 tokens
- **Pattern research**: 5000-6000 tokens  
- **Comprehensive guides**: 7000-8000 tokens
- **Quick reference**: 2000-3000 tokens

### Market Parser Specific Libraries to Research

**Frontend Development:**
- `react` - React 18.2+ patterns and hooks
- `vite` - Build optimization and configuration
- `typescript` - Type safety for React components
- `eslint` - Linting configuration for our setup

**Backend Development:**
- `fastapi` - API development patterns
- `openai-agents` - OpenAI Agents SDK framework
- `openai` - OpenAI API integration
- `uvicorn` - ASGI server configuration

**Testing & Quality:**
- `playwright` - E2E testing automation
- `pytest` - Python testing patterns
- `vitest` - Vite-based testing for frontend

**Package Management:**
- `npm` - Frontend dependency management
- `uv` - Python package management and virtual environments

**AI & Data Processing:**
- `openai-agents` - OpenAI Agents SDK for agent framework (use "openai-agents")
- `openai` - OpenAI API integration and models
- `instructor` - Structured LLM outputs with Pydantic validation

## Common Mistakes to Avoid

### 1. Skipping Library ID Resolution
❌ **Wrong:**
```javascript
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/react/react"  // Guessed format
})
```

✅ **Correct:**
```javascript
mcp__context7__resolve-library-id({"libraryName": "react"})
// Then use the actual resolved ID
```

### 2. Using Outdated Library Names
❌ **Wrong:**
```javascript
mcp__context7__resolve-library-id({"libraryName": "create-react-app"})  // Deprecated
```

✅ **Correct:**
```javascript
mcp__context7__resolve-library-id({"libraryName": "vite"})  // Current build tool
```

### 3. Too Broad Topic Queries
❌ **Wrong:**
```javascript
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "topic": "everything react"
})
```

✅ **Correct:**
```javascript
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "topic": "useState useEffect functional components"
})
```

### 4. Inefficient Token Usage
❌ **Wrong:**
```javascript
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "tokens": 15000  // Excessive for basic query
})
```

✅ **Correct:**
```javascript
mcp__context7__get-library-docs({
  "context7CompatibleLibraryID": "/facebook/react",
  "tokens": 5000  // Appropriate for detailed research
})
```

## Integration with Other MCP Tools

### Systematic Development Pattern

```javascript
// 1. Use sequential thinking for planning
mcp__sequential_thinking__sequentialthinking({
  "thought": "Planning React component development approach..."
})

// 2. Research patterns with Context7
mcp__context7__resolve-library-id({"libraryName": "react"})
mcp__context7__get-library-docs({...})

// 3. Implement using filesystem tools
mcp__filesystem__read_text_file({...})  // Read existing code
mcp__filesystem__edit_file({...})       // Apply new patterns

// 4. Test and validate
// Use appropriate testing tools
```

### Market Parser Development Workflow

1. **Analysis** - Use sequential thinking to break down requirements
2. **Research** - Use Context7 to get current patterns for our tech stack
3. **Implementation** - Use filesystem tools to apply patterns
4. **Testing** - Use Playwright MCP for E2E validation
5. **Documentation** - Update project documentation with findings

## Quick Reference Commands

### Frontend Development
```javascript
// React patterns research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "react"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/facebook/react", "topic": "hooks"})

// Vite optimization research  
// Step 1: mcp__context7__resolve-library-id({"libraryName": "vite"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/vitejs/vite", "topic": "performance"})

// TypeScript patterns research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "typescript"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/microsoft/typescript", "topic": "react"})
```

### Backend Development
```javascript
// FastAPI patterns research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "fastapi"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/tiangolo/fastapi", "topic": "middleware"})

// OpenAI Agents SDK research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "openai-agents"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/openai/openai-agents", "topic": "agents"})

// OpenAI SDK research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "openai"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/openai/openai-python", "topic": "agents"})
```

### Testing & Quality
```javascript
// Playwright testing research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "playwright"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/microsoft/playwright", "topic": "react"})

// ESLint configuration research
// Step 1: mcp__context7__resolve-library-id({"libraryName": "eslint"})
// Step 2: mcp__context7__get-library-docs({"context7CompatibleLibraryID": "/eslint/eslint", "topic": "typescript"})
```

## Conclusion

Context7 MCP tools are essential for staying current with our Market Parser application's tech stack. Use these tools systematically to research React 18.2+, Vite 5.2+, FastAPI, OpenAI Agents SDK, and OpenAI API patterns. Always resolve library IDs first, use specific topics, and apply findings using filesystem tools for implementation.

Remember: Context7 provides current, authoritative documentation - use it whenever working with external libraries in our Market Parser application to avoid outdated patterns and ensure optimal implementation.