# OpenAI AI Agent Custom Tools - Comprehensive Reference Guide

**Version:** 1.0
**Last Updated:** October 2025
**SDK Version:** OpenAI Agents SDK v0.2.9+

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Tool Creation Methods](#tool-creation-methods)
4. [Parameter Schema Design](#parameter-schema-design)
5. [Tool Descriptions & Docstrings](#tool-descriptions--docstrings)
6. [Return Values](#return-values)
7. [Error Handling](#error-handling)
8. [Advanced Features](#advanced-features)
9. [Testing & Validation](#testing--validation)
10. [Common Patterns & Examples](#common-patterns--examples)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Introduction

### Why Custom Tools Matter

Custom tools enable OpenAI AI Agents to take actions, access data, and integrate with external systems. Well-designed tools:

- **Improve agent capability** - Extend what agents can accomplish
- **Enable real-world integration** - Connect to APIs, databases, files, etc.
- **Enhance reliability** - Properly structured tools reduce errors
- **Optimize performance** - Clear schemas help the AI make better decisions

### Tool Design Philosophy

**Key Principles:**
1. **Clear purpose** - Each tool should do one thing well
2. **Descriptive naming** - Tool and parameter names should be self-explanatory
3. **Comprehensive documentation** - Detailed docstrings help the AI understand usage
4. **Type safety** - Use Python type hints for automatic schema generation
5. **Graceful error handling** - Return helpful error messages, not exceptions

---

## Quick Start

### Simplest Possible Tool

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_current_time() -> str:
    """Get the current time in UTC."""
    from datetime import datetime
    return datetime.utcnow().isoformat()

agent = Agent(
    name="Time Assistant",
    instructions="You help users with time-related questions.",
    tools=[get_current_time],
)

# Use the agent
result = await Runner.run(agent, input="What time is it?")
```

**What happens automatically:**
- ✅ Tool name: `get_current_time` (from function name)
- ✅ Description: `"Get the current time in UTC."` (from docstring)
- ✅ Schema: Auto-generated (no parameters)
- ✅ Execution: Function called when AI invokes the tool

---

## Tool Creation Methods

### Method 1: @function_tool Decorator (Recommended)

**Use when:** Creating most custom tools (90% of use cases)

**Advantages:**
- Simple and concise
- Automatic schema generation
- Docstring parsing for descriptions
- Supports both sync and async functions

**Basic Example:**

```python
from agents import function_tool
from typing import Annotated

@function_tool
def get_weather(
    city: Annotated[str, "The city to get weather for"],
    units: Annotated[str, "Temperature units: 'celsius' or 'fahrenheit'"] = "celsius"
) -> str:
    """Get current weather information for a specified city.

    Args:
        city: The name of the city (e.g., "San Francisco", "Tokyo")
        units: Temperature units to use

    Returns:
        A description of the current weather conditions.
    """
    # Your implementation here
    return f"Weather in {city}: 22°{units[0].upper()}, sunny"
```

**With Pydantic Models:**

```python
from pydantic import BaseModel, Field
from agents import function_tool

class WeatherResponse(BaseModel):
    city: str = Field(description="The city name")
    temperature_range: str = Field(description="Temperature range in Celsius")
    conditions: str = Field(description="Weather conditions")

@function_tool
def get_weather(city: str) -> WeatherResponse:
    """Get current weather for a city."""
    return WeatherResponse(
        city=city,
        temperature_range="14-20C",
        conditions="Sunny with wind"
    )
```

**Async Functions:**

```python
@function_tool
async def fetch_data_from_api(endpoint: str) -> str:
    """Fetch data from an external API asynchronously."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint)
        return response.text
```

### Method 2: Manual FunctionTool Creation

**Use when:** Need fine-grained control over tool definition

**Advantages:**
- Full control over schema
- Custom tool invocation logic
- Can reuse existing functions without modification

**Example:**

```python
from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel
from typing import Any

class ProcessUserArgs(BaseModel):
    username: str
    age: int

async def run_process_user(ctx: RunContextWrapper[Any], args: str) -> str:
    """Custom processing logic for the tool."""
    parsed = ProcessUserArgs.model_validate_json(args)
    # Your logic here
    return f"Processed: {parsed.username}, age {parsed.age}"

tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data from text",
    params_json_schema=ProcessUserArgs.model_json_schema(),
    on_invoke_tool=run_process_user,
)
```

### Method 3: Tool Overrides with @function_tool

**Use when:** Need to customize auto-generated tool properties

```python
from agents import function_tool

@function_tool(
    name_override="custom_tool_name",
    description_override="Custom description that overrides docstring",
    docstring_style="google"  # or "numpy", "sphinx"
)
def my_function(param: str) -> str:
    """Original docstring (will be overridden)."""
    return param
```

---

## Parameter Schema Design

### Supported Parameter Types

**Primitive Types:**

```python
@function_tool
def example_primitives(
    text: str,           # String parameter
    count: int,          # Integer parameter
    price: float,        # Float parameter
    enabled: bool,       # Boolean parameter
) -> str:
    """Example with primitive types."""
    return f"{text} x {count}"
```

**Optional Parameters:**

```python
from typing import Optional

@function_tool
def with_optional(
    required_param: str,
    optional_param: Optional[str] = None,
    default_value: int = 10
) -> str:
    """Parameters with defaults are optional."""
    return required_param
```

**Complex Types with TypedDict:**

```python
from typing_extensions import TypedDict

class Location(TypedDict):
    lat: float
    long: float

@function_tool
def get_location_data(location: Location) -> str:
    """Accept complex structured data.

    Args:
        location: Geographic coordinates with latitude and longitude
    """
    return f"Location: {location['lat']}, {location['long']}"
```

**Complex Types with Pydantic:**

```python
from pydantic import BaseModel, Field

class SearchFilters(BaseModel):
    query: str = Field(description="Search query text")
    max_results: int = Field(default=10, ge=1, le=100, description="Maximum results")
    include_archived: bool = Field(default=False, description="Include archived items")

@function_tool
def search_database(filters: SearchFilters) -> str:
    """Search database with complex filters."""
    return f"Searching for: {filters.query}"
```

**Lists and Arrays:**

```python
from typing import List

@function_tool
def process_batch(
    items: List[str],
    categories: List[str] = ["general"]
) -> str:
    """Process multiple items at once.

    Args:
        items: List of items to process
        categories: Categories to assign to items
    """
    return f"Processed {len(items)} items"
```

**Unions and Enums:**

```python
from typing import Literal, Union
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@function_tool
def create_task(
    title: str,
    priority: Union[Priority, Literal["urgent"]] = Priority.MEDIUM
) -> str:
    """Create a task with priority level."""
    return f"Task created with priority: {priority}"
```

### Parameter Validation with Pydantic

**Field Constraints:**

```python
from pydantic import BaseModel, Field, constr, conint

class ValidatedInput(BaseModel):
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(ge=0, le=150)  # Greater than or equal to 0, less than or equal to 150
    username: constr(min_length=3, max_length=20)
    count: conint(gt=0)  # Greater than 0

@function_tool
def register_user(data: ValidatedInput) -> str:
    """Register a new user with validated data."""
    return f"User {data.username} registered"
```

**Custom Validators:**

```python
from pydantic import BaseModel, field_validator

class UserData(BaseModel):
    username: str
    email: str

    @field_validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

@function_tool
def create_user(data: UserData) -> str:
    """Create user with custom validation."""
    return f"Created: {data.username}"
```

---

## Tool Descriptions & Docstrings

### Docstring Best Practices

**What AI Agents Need:**
1. **Clear purpose** - What the tool does
2. **When to use it** - Context for tool selection
3. **Parameter details** - What each parameter means
4. **Return value format** - What to expect back
5. **Constraints/limitations** - What the tool can't do

**Good Docstring Example:**

```python
@function_tool
def get_stock_price(
    ticker: str,
    date: Optional[str] = None
) -> str:
    """Get the stock price for a specific ticker symbol.

    Use this tool when the user asks about stock prices, market values,
    or wants to check the current or historical price of a publicly traded company.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL", "TSLA").
                Must be a valid ticker from a major exchange.
        date: Optional ISO date (YYYY-MM-DD) for historical prices.
              If not provided, returns the most recent price.

    Returns:
        A JSON string containing the ticker, date, price, and currency.
        Format: {"ticker": "AAPL", "date": "2025-10-04", "price": 175.50, "currency": "USD"}

    Note:
        - Only supports major US exchanges (NYSE, NASDAQ)
        - Historical data limited to last 5 years
        - Prices delayed by 15 minutes during market hours
    """
    # Implementation
    pass
```

**Bad Docstring Example:**

```python
@function_tool
def get_price(symbol: str) -> str:
    """Gets price."""  # ❌ Too vague
    pass
```

### Docstring Styles Supported

**Google Style (Default):**

```python
@function_tool
def example_google(param1: str, param2: int) -> str:
    """Summary line here.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value
    """
    pass
```

**NumPy Style:**

```python
@function_tool(docstring_style="numpy")
def example_numpy(param1: str, param2: int) -> str:
    """Summary line here.

    Parameters
    ----------
    param1 : str
        Description of param1
    param2 : int
        Description of param2

    Returns
    -------
    str
        Description of return value
    """
    pass
```

**Sphinx Style:**

```python
@function_tool(docstring_style="sphinx")
def example_sphinx(param1: str, param2: int) -> str:
    """Summary line here.

    :param param1: Description of param1
    :param param2: Description of param2
    :return: Description of return value
    """
    pass
```

---

## Return Values

### Return Value Best Practices

**Guidelines:**
1. **Return strings** for simple text responses
2. **Return Pydantic models** for structured data
3. **Return JSON strings** when you need flexibility
4. **Always return something** - never return None
5. **Include metadata** when helpful (timestamps, sources, etc.)

**String Returns (Simple):**

```python
@function_tool
def get_greeting(name: str) -> str:
    """Generate a personalized greeting."""
    return f"Hello, {name}! Welcome to our service."
```

**Pydantic Model Returns (Structured):**

```python
from pydantic import BaseModel
from datetime import datetime

class AnalysisResult(BaseModel):
    status: str
    data: dict
    timestamp: str
    source: str

@function_tool
def analyze_data(input_data: str) -> AnalysisResult:
    """Analyze input data and return structured results."""
    return AnalysisResult(
        status="completed",
        data={"result": "analysis complete"},
        timestamp=datetime.utcnow().isoformat(),
        source="internal_analyzer"
    )
```

**JSON String Returns (Flexible):**

```python
import json

@function_tool
def fetch_user_profile(user_id: str) -> str:
    """Fetch user profile and return as JSON string."""
    profile = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "preferences": {"theme": "dark", "notifications": True}
    }
    return json.dumps(profile)
```

**Lists and Collections:**

```python
from typing import List

@function_tool
def list_available_options() -> List[str]:
    """Return list of available options."""
    return ["option1", "option2", "option3"]
```

---

## Error Handling

### Error Handling Strategies

**Strategy 1: Return Error Messages (Recommended)**

```python
import json

@function_tool
def safe_divide(a: float, b: float) -> str:
    """Safely divide two numbers.

    Returns error message if division by zero.
    """
    if b == 0:
        return json.dumps({
            "error": "Division by zero",
            "message": "Cannot divide by zero. Please provide a non-zero divisor."
        })

    result = a / b
    return json.dumps({"result": result})
```

**Strategy 2: Custom Error Handler with failure_error_function**

```python
from agents import function_tool

def handle_code_error(ctx, error):
    """Custom error handler that returns helpful message to AI."""
    return (
        f"Error executing code: {str(error)}. "
        "Please check your input and try again. "
        "Common issues: missing files, invalid syntax, missing dependencies."
    )

@function_tool(failure_error_function=handle_code_error)
def run_code(code: str, input_files: List[str]) -> str:
    """Execute code with custom error handling."""
    if not code:
        raise ValueError("Code cannot be empty")
    if not input_files:
        raise ValueError("Must provide input files")

    # Implementation
    return "Code executed successfully"
```

**Strategy 3: Validation Before Processing**

```python
from pydantic import BaseModel, ValidationError
import json

class FileRequest(BaseModel):
    filename: str
    operation: str

@function_tool
def process_file(request: str) -> str:
    """Process file with validation."""
    try:
        data = FileRequest.model_validate_json(request)
    except ValidationError as e:
        return json.dumps({
            "error": "Invalid request format",
            "details": e.errors()
        })

    # Process valid request
    return f"Processed {data.filename} with {data.operation}"
```

**Strategy 4: Try-Except with Context**

```python
@function_tool
def fetch_external_data(url: str) -> str:
    """Fetch data from external source with error handling."""
    try:
        import httpx
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        return response.text
    except httpx.TimeoutException:
        return json.dumps({
            "error": "Request timeout",
            "message": "The external service took too long to respond. Please try again."
        })
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"HTTP {e.response.status_code}",
            "message": f"Server returned error: {e.response.text}"
        })
    except Exception as e:
        return json.dumps({
            "error": "Unexpected error",
            "message": str(e)
        })
```

---

## Advanced Features

### Using Tool Context

**Access Agent State:**

```python
from agents import RunContextWrapper, function_tool
from typing import Any

@function_tool
def context_aware_tool(
    ctx: RunContextWrapper[Any],  # MUST be first parameter
    user_input: str
) -> str:
    """Tool that accesses agent context.

    Args:
        ctx: Agent runtime context (automatically provided)
        user_input: User's input string
    """
    # Access agent information
    agent_name = ctx.agent.name

    # Access custom context data (if set)
    custom_data = ctx.context

    # Access session information
    # session = ctx.session

    return f"Agent '{agent_name}' processed: {user_input}"
```

**Custom Context with Dependency Injection:**

```python
from dataclasses import dataclass

@dataclass
class DatabaseConnection:
    connection_string: str

    def query(self, sql: str):
        # Database logic
        return {"result": "data"}

@function_tool
def query_database(
    ctx: RunContextWrapper[DatabaseConnection],
    query: str
) -> str:
    """Query database using injected connection."""
    db = ctx.context
    result = db.query(query)
    return json.dumps(result)

# When creating agent, provide context
db_context = DatabaseConnection(connection_string="postgresql://...")
agent = Agent(
    name="DB Agent",
    tools=[query_database],
)

# Run with context
result = await Runner.run(agent, input="Get users", context=db_context)
```

### Async Tools

```python
import asyncio

@function_tool
async def parallel_fetch(urls: List[str]) -> str:
    """Fetch multiple URLs in parallel."""
    import httpx

    async def fetch_one(url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.text

    results = await asyncio.gather(*[fetch_one(url) for url in urls])
    return json.dumps({"results": results})
```

### Tool Name and Description Overrides

```python
@function_tool(
    name_override="search_knowledge_base",
    description_override="Search the company knowledge base for relevant information. Use this when users ask about internal policies, procedures, or documentation."
)
def internal_search(query: str) -> str:
    """Original docstring (will be overridden)."""
    # Implementation
    return "Search results..."
```

---

## Testing & Validation

### Unit Testing Tools

```python
import pytest
import json
from my_tools import get_weather

def test_get_weather_basic():
    """Test basic weather tool functionality."""
    result = get_weather(city="Tokyo")

    # For string returns
    assert "Tokyo" in result
    assert "sunny" in result.lower() or "cloudy" in result.lower()

def test_get_weather_structured():
    """Test weather tool with Pydantic model return."""
    result = get_weather(city="Tokyo")

    # For Pydantic returns
    assert result.city == "Tokyo"
    assert isinstance(result.temperature_range, str)
    assert result.conditions

def test_get_weather_error_handling():
    """Test weather tool error cases."""
    result = get_weather(city="")
    data = json.loads(result)

    assert "error" in data
    assert data["error"] == "Invalid city name"
```

### Integration Testing with Agents

```python
import pytest
from agents import Agent, Runner

@pytest.mark.asyncio
async def test_agent_with_tool():
    """Test agent using the custom tool."""
    agent = Agent(
        name="Weather Agent",
        tools=[get_weather],
        instructions="You provide weather information."
    )

    result = await Runner.run(
        agent,
        input="What's the weather in Tokyo?"
    )

    assert result.final_output
    assert "tokyo" in result.final_output.lower()
```

### Validating Tool Schemas

```python
from agents import Agent, FunctionTool
import json

# Create agent with your tool
agent = Agent(name="Test", tools=[get_weather])

# Inspect generated schema
for tool in agent.tools:
    if isinstance(tool, FunctionTool):
        print(f"Tool Name: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Schema: {json.dumps(tool.params_json_schema, indent=2)}")
```

---

## Common Patterns & Examples

### Pattern 1: File Operations

```python
from pathlib import Path
import json

@function_tool
def read_file(filename: str, n_lines: int = 10) -> str:
    """Read and preview file contents.

    Args:
        filename: Path to the file
        n_lines: Number of lines to preview

    Returns:
        JSON with file content or error
    """
    try:
        path = Path(filename)
        if not path.exists():
            return json.dumps({"error": "File not found", "file": filename})

        with open(path, 'r') as f:
            lines = f.readlines()[:n_lines]

        return json.dumps({
            "file": filename,
            "preview": ''.join(lines),
            "total_lines": len(lines)
        })
    except Exception as e:
        return json.dumps({"error": str(e), "file": filename})
```

### Pattern 2: API Integration

```python
import httpx
import json

@function_tool
async def call_external_api(
    endpoint: str,
    method: str = "GET",
    params: Optional[dict] = None
) -> str:
    """Call external API with error handling.

    Args:
        endpoint: API endpoint URL
        method: HTTP method (GET, POST, etc.)
        params: Query parameters or request body
    """
    try:
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(endpoint, params=params)
            elif method.upper() == "POST":
                response = await client.post(endpoint, json=params)
            else:
                return json.dumps({"error": f"Unsupported method: {method}"})

            response.raise_for_status()
            return json.dumps({
                "status": response.status_code,
                "data": response.json()
            })
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"HTTP {e.response.status_code}",
            "message": str(e)
        })
    except Exception as e:
        return json.dumps({"error": "Request failed", "message": str(e)})
```

### Pattern 3: Data Processing with Validation

```python
from pydantic import BaseModel, Field, field_validator
from typing import List
import json

class DataRecord(BaseModel):
    id: str
    value: float
    category: str

    @field_validator('value')
    def value_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('value must be positive')
        return v

@function_tool
def process_records(records_json: str) -> str:
    """Process and validate data records.

    Args:
        records_json: JSON array of records

    Returns:
        Processing results with statistics
    """
    try:
        data = json.loads(records_json)
        validated_records = [DataRecord(**r) for r in data]

        total = len(validated_records)
        sum_values = sum(r.value for r in validated_records)

        return json.dumps({
            "status": "success",
            "total_records": total,
            "sum": sum_values,
            "average": sum_values / total if total > 0 else 0
        })
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON format"})
    except ValueError as e:
        return json.dumps({"error": "Validation error", "message": str(e)})
```

### Pattern 4: Database Operations

```python
from agents import function_tool, RunContextWrapper
from typing import Any, List
import json

class DatabaseContext:
    """Example database context."""
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def execute_query(self, sql: str) -> List[dict]:
        # Actual database logic
        return [{"id": 1, "name": "Example"}]

@function_tool
def db_query(
    ctx: RunContextWrapper[DatabaseContext],
    query: str
) -> str:
    """Execute database query safely.

    Args:
        ctx: Database context
        query: SQL query to execute
    """
    try:
        db = ctx.context
        results = db.execute_query(query)
        return json.dumps({
            "status": "success",
            "rows": len(results),
            "data": results
        })
    except Exception as e:
        return json.dumps({
            "error": "Query failed",
            "message": str(e)
        })
```

---

## Best Practices

### 1. Naming Conventions

**DO:**
- ✅ Use clear, descriptive names: `get_weather`, `search_database`, `send_email`
- ✅ Use verbs for actions: `create_`, `update_`, `delete_`, `fetch_`, `process_`
- ✅ Be specific: `get_stock_price` not just `get_price`

**DON'T:**
- ❌ Use abbreviations: `get_wx`, `proc_data`
- ❌ Use vague names: `do_thing`, `helper`, `util`
- ❌ Use misleading names: `get_all_data` when it only gets recent data

### 2. Parameter Design

**DO:**
- ✅ Use type hints for all parameters
- ✅ Provide clear parameter descriptions
- ✅ Use Pydantic for complex validation
- ✅ Set sensible defaults for optional parameters
- ✅ Use Literal types for enums/choices

**DON'T:**
- ❌ Use `Any` type unless absolutely necessary
- ❌ Have too many parameters (>5 suggests refactoring)
- ❌ Use ambiguous parameter names (`data`, `info`, `stuff`)

### 3. Documentation

**DO:**
- ✅ Write comprehensive docstrings
- ✅ Explain when to use the tool
- ✅ Document constraints and limitations
- ✅ Provide example usage in docstring
- ✅ Describe return value format

**DON'T:**
- ❌ Skip docstrings
- ❌ Write vague descriptions
- ❌ Forget to document edge cases

### 4. Error Handling

**DO:**
- ✅ Return error messages as structured data
- ✅ Provide actionable error messages
- ✅ Include error codes/types
- ✅ Use custom error handlers for complex cases
- ✅ Validate inputs early

**DON'T:**
- ❌ Let exceptions bubble up unhandled
- ❌ Return generic "error occurred" messages
- ❌ Hide error details from the AI

### 5. Return Values

**DO:**
- ✅ Use consistent return formats
- ✅ Return structured data when possible
- ✅ Include metadata (timestamps, sources, etc.)
- ✅ Return JSON strings for complex data
- ✅ Always return something (never None)

**DON'T:**
- ❌ Mix return formats in the same tool
- ❌ Return raw exceptions or stack traces
- ❌ Return empty strings without context

### 6. Performance

**DO:**
- ✅ Use async for I/O-bound operations
- ✅ Set reasonable timeouts
- ✅ Cache results when appropriate
- ✅ Limit data size in responses
- ✅ Validate inputs before expensive operations

**DON'T:**
- ❌ Make synchronous calls to external APIs
- ❌ Return massive amounts of data
- ❌ Perform expensive operations without validation

### 7. Security

**DO:**
- ✅ Validate and sanitize all inputs
- ✅ Use parameterized queries for databases
- ✅ Limit file system access to specific directories
- ✅ Implement rate limiting for expensive operations
- ✅ Log tool usage for audit trails

**DON'T:**
- ❌ Execute arbitrary code from parameters
- ❌ Allow SQL injection
- ❌ Expose sensitive data in error messages
- ❌ Grant unrestricted file system access

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Tool Not Being Called

**Symptoms:** Agent doesn't use your tool even though it seems relevant

**Solutions:**
1. **Improve tool description** - Make it clearer when to use the tool
2. **Check tool name** - Ensure it's descriptive and relevant
3. **Verify parameter schema** - Ensure parameters are clear and properly typed
4. **Add examples in docstring** - Show the AI how to use it

```python
# BAD
@function_tool
def tool(x: str) -> str:
    """Does something."""
    pass

# GOOD
@function_tool
def search_product_database(
    query: str,
    category: Optional[str] = None
) -> str:
    """Search the product database for items matching the query.

    Use this tool when the user asks about products, inventory, or
    wants to find items by name, description, or category.

    Examples of when to use:
    - "Find red shoes"
    - "What products do we have in electronics?"
    - "Search for wireless headphones"

    Args:
        query: Search terms (product name, keywords, description)
        category: Optional category filter (e.g., "electronics", "clothing")
    """
    pass
```

#### Issue 2: Schema Generation Fails

**Symptoms:** Error during agent creation about schema

**Solutions:**
1. **Use supported types** - Stick to primitives, Pydantic, TypedDict
2. **Avoid complex generics** - Simplify type hints
3. **Check Pydantic version** - Ensure compatibility
4. **Use manual FunctionTool** - For unsupported types

```python
# If automatic schema fails, create manually
from pydantic import BaseModel

class MyParams(BaseModel):
    param1: str
    param2: int

tool = FunctionTool(
    name="my_tool",
    description="Tool description",
    params_json_schema=MyParams.model_json_schema(),
    on_invoke_tool=my_function
)
```

#### Issue 3: Type Validation Errors

**Symptoms:** Tool called but fails with validation error

**Solutions:**
1. **Add field validators** - Catch issues early
2. **Provide clear error messages** - Help AI fix the issue
3. **Use constrained types** - Built-in Pydantic validation
4. **Test with malformed input** - Ensure robust validation

```python
from pydantic import BaseModel, field_validator, ValidationError
import json

class StrictParams(BaseModel):
    email: str
    age: int

    @field_validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email must contain @ symbol')
        return v

    @field_validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

@function_tool
def register(params_json: str) -> str:
    """Register with validation."""
    try:
        data = StrictParams.model_validate_json(params_json)
        return json.dumps({"status": "success"})
    except ValidationError as e:
        return json.dumps({
            "error": "Validation failed",
            "details": e.errors(),
            "help": "Please provide valid email and age (0-150)"
        })
```

#### Issue 4: Async/Await Issues

**Symptoms:** "coroutine was never awaited" or similar

**Solutions:**
1. **Use `async def`** for async tools
2. **Use `await`** for async operations
3. **Don't mix sync/async** incorrectly

```python
# CORRECT
@function_tool
async def fetch_data(url: str) -> str:
    """Async tool."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# INCORRECT
@function_tool
def fetch_data(url: str) -> str:  # Not async
    """Sync tool trying to use async."""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(url)  # ❌ await in non-async function
        return response.text
```

#### Issue 5: Context Not Available

**Symptoms:** `ctx.context` is None or missing

**Solutions:**
1. **Pass context when running** - Provide context to `Runner.run()`
2. **Check context type** - Ensure type matches RunContextWrapper generic
3. **Use optional context** - Handle cases where context might not be provided

```python
@function_tool
def context_tool(
    ctx: RunContextWrapper[Optional[MyContext]],
    param: str
) -> str:
    """Tool with optional context."""
    if ctx.context is None:
        return json.dumps({
            "error": "Context not available",
            "message": "This tool requires context to be set"
        })

    # Use context
    data = ctx.context.get_data()
    return json.dumps({"result": data})

# When running, provide context
my_context = MyContext(...)
result = await Runner.run(agent, input="...", context=my_context)
```

#### Issue 6: Tool Returns Not Parsed Correctly

**Symptoms:** AI can't understand tool output

**Solutions:**
1. **Return consistent format** - Always JSON for structured data
2. **Include structure hints** - Describe format in docstring
3. **Validate JSON** - Ensure valid JSON when using json.dumps
4. **Use Pydantic models** - Automatic serialization

```python
@function_tool
def well_formatted_tool(query: str) -> str:
    """Tool with clear return format.

    Returns:
        JSON string with format:
        {
            "status": "success" | "error",
            "data": <result data>,
            "message": <optional message>
        }
    """
    result = {"status": "success", "data": query, "message": "Processed"}
    return json.dumps(result)  # Always valid JSON
```

---

## Summary

### Quick Reference Checklist

When creating a new tool, ensure:

- [ ] **Clear, descriptive name** (verb + noun format)
- [ ] **Comprehensive docstring** with purpose, args, returns, examples
- [ ] **Type hints on all parameters** (enables auto-schema generation)
- [ ] **Error handling** that returns helpful messages
- [ ] **Consistent return format** (JSON or Pydantic model)
- [ ] **Input validation** (Pydantic validators or manual checks)
- [ ] **Async for I/O operations** (API calls, file operations)
- [ ] **Security considerations** (input sanitization, access control)
- [ ] **Testing** (unit tests and integration tests)
- [ ] **Documentation** of limitations and constraints

### Resources

**Official Documentation:**
- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Tools Guide](https://openai.github.io/openai-agents-python/tools/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

**Example Repositories:**
- [OpenAI Agents Examples](https://github.com/openai/openai-agents-python/tree/main/examples)
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook/tree/main/examples/agents_sdk)

---

**End of Reference Guide**

*This guide is maintained for use with OpenAI Agents SDK v0.2.9+. For questions or issues, refer to the official documentation or examples repository.*
