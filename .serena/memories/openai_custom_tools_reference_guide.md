# OpenAI Custom Tools Reference Guide

## Overview
Comprehensive reference guide for creating OpenAI AI Agent optimized custom tools using the OpenAI Agents SDK v0.2.9. This guide covers best practices, patterns, and examples for building tools that AI agents can effectively use.

## Location
`docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md`

## Key Topics Covered

### 1. Tool Creation Methods
- **@function_tool Decorator** (Primary Method)
  - Automatic schema generation from function signatures
  - Docstring parsing for descriptions
  - Type hints to Pydantic schema conversion
  - Simplest approach for most use cases

- **FunctionTool Class** (Manual Method)
  - Fine-grained control over tool definition
  - Custom schema specifications
  - Advanced context handling
  - Used when decorator limitations are reached

### 2. Parameter Schema Design
- **Pydantic Models**: Primary method for structured parameters
  - Field descriptions with `Field(description="...")`
  - Validation rules and constraints
  - Nested models for complex structures
  - Auto-generated JSON schemas

- **TypedDict**: Alternative for simpler structures
  - Less validation overhead
  - Good for basic parameter structures

- **Annotated Types**: Inline parameter descriptions
  - `Annotated[str, "Description here"]`
  - Works seamlessly with @function_tool
  - Clean, readable signatures

### 3. Tool Descriptions
- **Docstring Parsing**: Automatic extraction
  - Supports Google, NumPy, Sphinx styles
  - First line becomes tool description
  - Args/Returns sections parsed automatically
  
- **Best Practices**:
  - Clear, action-oriented descriptions
  - Specify what the tool does, not how
  - Include example usage in docstring
  - Mention prerequisites or limitations

### 4. Error Handling Patterns
- **Custom Error Handlers**: `failure_error_function` parameter
  - Return helpful messages to AI agent
  - Guide agent toward correct usage
  - Avoid exposing internal errors
  
- **Validation Strategies**:
  - Use Pydantic for parameter validation
  - Raise ValueError with clear messages
  - Return error states vs raising exceptions
  - Provide recovery suggestions

### 5. Tool Context (RunContextWrapper)
- **Access Agent State**: `ctx.agent.name`, `ctx.agent.instructions`
- **Dependency Injection**: `ctx.context` for custom data
- **Must be first parameter** in function signature
- Type: `RunContextWrapper[Any]`

### 6. Advanced Features
- **Async Tools**: Full async/await support
  - Use `async def` with @function_tool
  - Perfect for I/O operations
  - Non-blocking tool execution

- **Return Types**:
  - Simple types: `str`, `int`, `bool`
  - Pydantic models: Auto-serialized to JSON
  - Lists and dicts: Structured data
  - Avoid returning large objects

- **File Operations**: Common pattern for file handling
  - Validate file paths
  - Use context managers
  - Return file metadata, not raw content
  - Handle missing files gracefully

### 7. Best Practices (12 Key Guidelines)

1. **Keep Tools Focused**: One clear purpose per tool
2. **Use Type Hints**: Enable automatic schema generation
3. **Write Clear Docstrings**: AI agents rely on descriptions
4. **Validate Inputs**: Use Pydantic for validation
5. **Handle Errors Gracefully**: Return helpful error messages
6. **Return Structured Data**: Use Pydantic models for complex returns
7. **Use Meaningful Names**: Action verbs (get_*, create_*, analyze_*)
8. **Provide Defaults**: Make optional parameters truly optional
9. **Test Thoroughly**: Unit tests + integration tests
10. **Document Limitations**: State what tool cannot do
11. **Keep It Simple**: Prefer simple over complex
12. **Use Async When Appropriate**: For I/O-bound operations

### 8. Common Patterns

**Weather Tool Pattern**:
```python
@function_tool
def get_weather(
    city: Annotated[str, "The city to get weather for"],
    units: Annotated[str, "Temperature units"] = "celsius"
) -> Weather:
    """Get current weather for a city."""
    return Weather(city=city, temp="22C", conditions="Sunny")
```

**Code Execution Pattern**:
```python
@function_tool(failure_error_function=handle_code_error)
def run_code(code: str, input_files: List[str]) -> str:
    """Execute code with custom error handling."""
    if not code:
        raise ValueError("Code cannot be empty")
    # Execute and return results
```

**Context-Aware Pattern**:
```python
@function_tool
def context_aware_tool(
    ctx: RunContextWrapper[Any],
    user_input: str
) -> str:
    """Tool that accesses agent context."""
    agent_name = ctx.agent.name
    return f"Processed by {agent_name}: {user_input}"
```

### 9. Integration with Agents

```python
from agents import Agent, Runner, function_tool

@function_tool
def my_custom_tool(param: str) -> str:
    """Tool description here."""
    return f"Processed: {param}"

agent = Agent(
    name="My Agent",
    instructions="You help with tasks using custom tools.",
    tools=[my_custom_tool],  # Add tools here
    model="gpt-4o"
)

runner = Runner(agent=agent)
result = runner.run("Use the tool to process 'test'")
```

### 10. Testing Recommendations
- **Unit Tests**: Test tool functions directly
- **Integration Tests**: Test with actual Agent runner
- **Mock External APIs**: Use pytest fixtures
- **Validate Schemas**: Test parameter validation
- **Error Cases**: Test all error paths

## Research Sources
- OpenAI Agents Python SDK documentation
- `examples/basic/tools.py` from openai-agents-python
- `tools.py` from openai-cookbook portfolio collaboration example
- Official OpenAI Agents SDK v0.2.9 reference

## Usage in This Project
This reference guide serves as the authoritative source for creating custom tools for the Market Parser project's AI agent. When implementing new tools for financial analysis or data processing, follow the patterns and best practices outlined in this guide.

## Related Files
- `docs/OPENAI_CUSTOM_TOOLS_REFERENCE.md` - Full reference guide
- `src/backend/main.py` - Current agent implementation
- Future custom tools should reference this guide

## Last Updated
Created: 2025-10-04 via comprehensive /research command workflow
Status: Production-ready reference documentation
