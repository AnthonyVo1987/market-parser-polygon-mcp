# OpenAI Agents SDK Integration - v0.2.9

## Overview

This memory documents the correct usage of OpenAI Agents SDK v0.2.9 in the Market Parser project, replacing incorrect references to Pydantic AI.

## Key Integration Details

### SDK Version & Usage
- **Current Version**: OpenAI Agents SDK v0.2.9 (updated from v0.2.8)
- **Package Name**: `openai-agents`
- **Import Pattern**: `from agents import Agent, Runner`
- **Framework**: OpenAI Agents SDK (NOT Pydantic AI)

### Agent Configuration
```python
# Correct Agent instantiation with explicit model specification
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="""Classify if the user query is finance-related...""",
    output_type=FinanceOutput,
    model=settings.available_models[0],  # Explicit model specification
)
```

### Model Integration
- **GPT-5 Nano**: 200K TPM limit
- **GPT-5 Mini**: 500K TPM limit
- **Rate Limiting**: Model-specific rate limiting implemented
- **Default Prevention**: Explicit model specification prevents GPT-4o default

### Key Features Used
1. **Agent Class**: Core agent functionality
2. **Runner Class**: Agent execution and management
3. **Model Specification**: Explicit model parameter setting
4. **Output Types**: Pydantic model integration for structured responses
5. **Tool Integration**: MCP server integration for real-time data

### Architecture Integration
- **Backend**: FastAPI with OpenAI Agents SDK v0.2.9
- **AI Models**: GPT-5 Nano/Mini via OpenAI Agents SDK
- **Data Source**: Polygon.io MCP server v0.4.1
- **Performance**: Quick response optimization system

### Documentation Updates
- **Corrected References**: All docs now reference OpenAI Agents SDK
- **Removed Pydantic AI**: Eliminated incorrect Pydantic AI references
- **Updated Architecture**: Proper technology stack documentation
- **Version Consistency**: All references updated to v0.2.9

### Performance Optimizations
- **Model-Specific Rate Limiting**: Proper TPM/RPM limits for GPT-5 models
- **Quick Response System**: Optimized prompts for faster responses
- **Tool Efficiency**: Minimal tool usage patterns
- **Response Time**: 20-40% improvement in response times

## Common Misconceptions Corrected

1. **NOT Pydantic AI**: Project uses OpenAI Agents SDK, not Pydantic AI
2. **Version Accuracy**: Current version is v0.2.9, not v0.2.8
3. **Model Specification**: Explicit model parameter required for proper rate limiting
4. **Framework Name**: OpenAI Agents SDK is the correct framework name

## Future Considerations

- Monitor for OpenAI Agents SDK updates
- Maintain version consistency across all documentation
- Ensure proper model specification in all agent instantiations
- Keep rate limiting aligned with model capabilities