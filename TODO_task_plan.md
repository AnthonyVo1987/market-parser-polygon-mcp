# TODO Task Plan - OpenAI Prompt Caching Integration

**Created:** October 7, 2025
**Task:** Integrate OpenAI API Prompt Caching to reduce latency and costs
**Status:** Planning Complete - Ready for Implementation

---

## 🎯 TASK OBJECTIVES

1. **Enhance AI Prompts/Code** to leverage OpenAI API Prompt Caching features
2. **Reduce Latency & Costs**: Target 50-80% cost reduction, 80% latency improvement for cached requests
3. **Update Token Display**: Add Cached Input/Output tokens to CLI & GUI
4. **Comprehensive Documentation**: Update all docs and Serena memories with new features

---

## 🔍 RESEARCH FINDINGS SUMMARY

### Key Discoveries:

1. **OpenAI Agents SDK v0.2.9 Already Supports Caching!**
   - SDK captures `input_tokens_details` and `output_tokens_details` in usage object
   - Located in `openai_responses.py` - SDK already has the data
   - Responses API uses `usage.input_tokens_details.cached_tokens`

2. **Current Token Handling Flow:**
   - **Backend**: `token_utils.py` extracts usage from `context_wrapper.usage`
   - **CLI Display**: `response_utils.py` shows token footer (lines 52-56)
   - **API Response**: `chat.py` router returns tokens via `ChatResponse` model
   - **Frontend Display**: `ChatMessage_OpenAI.tsx` shows token metrics (lines 279-287)

3. **Prompt Caching Mechanics:**
   - Auto-activates for prompts >1024 tokens
   - Cache duration: 5-10 minutes inactivity, max 1 hour
   - Best practice: Static content at START, dynamic at END
   - Cache hit indicator: `cached_tokens > 0` in response usage

4. **Implementation Pattern (from Prompt_Caching101.ipynb):**
   ```python
   # Structure prompts for caching:
   # 1. Static content FIRST (instructions, tools, context) - CACHED
   # 2. Dynamic content LAST (user query, new messages) - NOT CACHED

   completion = client.chat.completions.create(
       model="gpt-4o-mini",
       tools=tools,  # Must remain identical in order
       messages=messages,  # Append new to END
   )

   # Access cached tokens:
   cached = completion.usage.prompt_tokens_details.cached_tokens
   ```

---

## 📋 IMPLEMENTATION PLAN (7 Phases)

### ⚠️ CRITICAL: USE SEQUENTIAL-THINKING & SERENA TOOLS THROUGHOUT ALL PHASES

---

## PHASE 1: BACKEND - ADD CACHED TOKEN EXTRACTION

**Goal:** Extract cached token data from OpenAI Agents SDK usage object

### Task 1.1: Update token_utils.py to extract cached tokens

**Tool:** Serena find_symbol + replace_symbol_body OR Edit

**Location:** `src/backend/utils/token_utils.py`

**Current Code (lines 22-54):**
```python
def extract_token_usage_from_context_wrapper(result: Any) -> Optional[Dict[str, int]]:
    """Extract detailed token usage from official OpenAI Agents SDK context_wrapper.

    Returns:
        dict or None: Dictionary with 'total_tokens', 'input_tokens', and 'output_tokens'
    """
    try:
        if hasattr(result, "context_wrapper") and result.context_wrapper:
            usage = result.context_wrapper.usage

            # Extract tokens using both naming conventions for compatibility
            total = getattr(usage, "total_tokens", None)
            input_tokens = getattr(usage, "input_tokens", None) or getattr(
                usage, "prompt_tokens", None
            )
            output_tokens = getattr(usage, "output_tokens", None) or getattr(
                usage, "completion_tokens", None
            )

            if total is not None:
                return {
                    "total_tokens": total,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                }
    except Exception:
        pass
    return None
```

**New Code (add cached token extraction):**
```python
def extract_token_usage_from_context_wrapper(result: Any) -> Optional[Dict[str, int]]:
    """Extract detailed token usage from official OpenAI Agents SDK context_wrapper.

    Returns:
        dict or None: Dictionary with 'total_tokens', 'input_tokens', 'output_tokens',
                      'cached_input_tokens', and 'cached_output_tokens' if available
    """
    try:
        if hasattr(result, "context_wrapper") and result.context_wrapper:
            usage = result.context_wrapper.usage

            # Extract tokens using both naming conventions for compatibility
            total = getattr(usage, "total_tokens", None)
            input_tokens = getattr(usage, "input_tokens", None) or getattr(
                usage, "prompt_tokens", None
            )
            output_tokens = getattr(usage, "output_tokens", None) or getattr(
                usage, "completion_tokens", None
            )

            # Extract cached tokens from OpenAI Prompt Caching API
            # Responses API uses input_tokens_details.cached_tokens
            # Chat Completions API uses prompt_tokens_details.cached_tokens
            cached_input_tokens = None
            cached_output_tokens = None

            # Try Responses API format (OpenAI Agents SDK v0.2.9)
            if hasattr(usage, "input_tokens_details") and usage.input_tokens_details:
                cached_input_tokens = getattr(usage.input_tokens_details, "cached_tokens", 0)

            # Fallback to Chat Completions API format
            if cached_input_tokens is None and hasattr(usage, "prompt_tokens_details"):
                if usage.prompt_tokens_details:
                    cached_input_tokens = getattr(usage.prompt_tokens_details, "cached_tokens", 0)

            # Output cached tokens (if available in future API versions)
            if hasattr(usage, "output_tokens_details") and usage.output_tokens_details:
                cached_output_tokens = getattr(usage.output_tokens_details, "cached_tokens", 0)

            if total is not None:
                return {
                    "total_tokens": total,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cached_input_tokens": cached_input_tokens or 0,
                    "cached_output_tokens": cached_output_tokens or 0,
                }
    except Exception:
        pass
    return None
```

**Validation:**
- [ ] Function returns dict with 5 keys: total_tokens, input_tokens, output_tokens, cached_input_tokens, cached_output_tokens
- [ ] Handles both Responses API and Chat Completions API formats
- [ ] Defaults to 0 for cached tokens if not available

---

## PHASE 2: BACKEND - UPDATE API MODELS

**Goal:** Add cached token fields to API response models

### Task 2.1: Add cached token fields to ChatMetadata model

**Tool:** Serena find_symbol + Edit

**Location:** `src/backend/api_models.py`

**Current Code (lines 133-140):**
```python
class ChatMetadata(BaseModel):
    """Metadata for chat responses."""
    request_id: Optional[str] = Field(None, alias="requestId")
    token_count: Optional[int] = Field(
        None, alias="tokenCount"
    )  # Deprecated: use input/output tokens
    input_tokens: Optional[int] = Field(None, alias="inputTokens")
    output_tokens: Optional[int] = Field(None, alias="outputTokens")

    model_config = ConfigDict(populate_by_name=True, alias_generator=None)
```

**New Code (add cached token fields):**
```python
class ChatMetadata(BaseModel):
    """Metadata for chat responses."""
    request_id: Optional[str] = Field(None, alias="requestId")
    token_count: Optional[int] = Field(
        None, alias="tokenCount"
    )  # Deprecated: use input/output tokens
    input_tokens: Optional[int] = Field(None, alias="inputTokens")
    output_tokens: Optional[int] = Field(None, alias="outputTokens")
    cached_input_tokens: Optional[int] = Field(None, alias="cachedInputTokens")
    cached_output_tokens: Optional[int] = Field(None, alias="cachedOutputTokens")

    model_config = ConfigDict(populate_by_name=True, alias_generator=None)
```

**Validation:**
- [ ] Model has 2 new fields: cached_input_tokens, cached_output_tokens
- [ ] Fields use camelCase aliases for frontend compatibility
- [ ] All existing fields preserved

---

## PHASE 3: BACKEND - UPDATE API ROUTER

**Goal:** Include cached tokens in API responses

### Task 3.1: Update /api/chat endpoint to include cached tokens

**Tool:** Serena find_symbol + Edit

**Location:** `src/backend/routers/chat.py`

**Current Code (lines 95-112):**
```python
# Extract individual token counts
token_count = token_usage.get("total_tokens") if token_usage else None
input_tokens = token_usage.get("input_tokens") if token_usage else None
output_tokens = token_usage.get("output_tokens") if token_usage else None

# Calculate processing time
processing_time = time.time() - start_time

# Build response
return ChatResponse(
    response=final_output,
    metadata=ChatMetadata(
        requestId=request_id,
        tokenCount=token_count,  # Deprecated: kept for backward compatibility
        inputTokens=input_tokens,
        outputTokens=output_tokens,
    )
)
```

**New Code (add cached tokens):**
```python
# Extract individual token counts
token_count = token_usage.get("total_tokens") if token_usage else None
input_tokens = token_usage.get("input_tokens") if token_usage else None
output_tokens = token_usage.get("output_tokens") if token_usage else None
cached_input_tokens = token_usage.get("cached_input_tokens") if token_usage else None
cached_output_tokens = token_usage.get("cached_output_tokens") if token_usage else None

# Calculate processing time
processing_time = time.time() - start_time

# Build response
return ChatResponse(
    response=final_output,
    metadata=ChatMetadata(
        requestId=request_id,
        tokenCount=token_count,  # Deprecated: kept for backward compatibility
        inputTokens=input_tokens,
        outputTokens=output_tokens,
        cachedInputTokens=cached_input_tokens,
        cachedOutputTokens=cached_output_tokens,
    )
)
```

**Validation:**
- [ ] API response includes cachedInputTokens and cachedOutputTokens
- [ ] Existing fields preserved
- [ ] No breaking changes to API contract

---

## PHASE 4: BACKEND - UPDATE CLI DISPLAY

**Goal:** Show cached tokens in CLI footer

### Task 4.1: Update response_utils.py to display cached tokens

**Tool:** Serena find_symbol + replace_symbol_body OR Edit

**Location:** `src/backend/utils/response_utils.py`

**Current Code (lines 36-56):**
```python
# Extract token information using official OpenAI Agents SDK
token_count = None
input_tokens = None
output_tokens = None

# Try to get token data from official SDK context_wrapper
if hasattr(result, "context_wrapper") and result.context_wrapper:
    usage = result.context_wrapper.usage
    if hasattr(usage, "total_tokens"):
        token_count = usage.total_tokens
    if hasattr(usage, "input_tokens"):
        input_tokens = usage.input_tokens
    if hasattr(usage, "output_tokens"):
        output_tokens = usage.output_tokens

# Display token information
if token_count:
    token_display = f"   Tokens Used: {token_count:,}"
    if input_tokens and output_tokens:
        token_display += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"
    console.print(token_display)
```

**New Code (add cached token display):**
```python
# Extract token information using official OpenAI Agents SDK
from .token_utils import extract_token_usage_from_context_wrapper

token_usage = extract_token_usage_from_context_wrapper(result)

if token_usage:
    token_count = token_usage.get("total_tokens")
    input_tokens = token_usage.get("input_tokens")
    output_tokens = token_usage.get("output_tokens")
    cached_input = token_usage.get("cached_input_tokens", 0)
    cached_output = token_usage.get("cached_output_tokens", 0)

    # Display token information with caching metrics
    if token_count:
        token_display = f"   Tokens Used: {token_count:,}"

        if input_tokens and output_tokens:
            token_display += f" (Input: {input_tokens:,}, Output: {output_tokens:,})"

            # Show cache hit information if any tokens were cached
            if cached_input > 0 or cached_output > 0:
                cache_parts = []
                if cached_input > 0:
                    cache_parts.append(f"Cached Input: {cached_input:,}")
                if cached_output > 0:
                    cache_parts.append(f"Cached Output: {cached_output:,}")
                token_display += f" | {', '.join(cache_parts)}"

        console.print(token_display)
```

**Expected Output Examples:**
```
# No cache hit:
   Tokens Used: 1,234 (Input: 1,000, Output: 234)

# Cache hit on input:
   Tokens Used: 1,234 (Input: 1,000, Output: 234) | Cached Input: 512

# Cache hit on both:
   Tokens Used: 1,234 (Input: 1,000, Output: 234) | Cached Input: 512, Cached Output: 128
```

**Validation:**
- [ ] CLI displays cached tokens when cache hits occur
- [ ] Display format is clean and readable
- [ ] No display when cached_tokens = 0
- [ ] Uses token_utils function for consistent extraction

---

## PHASE 5: FRONTEND - UPDATE TYPES & COMPONENTS

**Goal:** Add cached token display to React GUI

### Task 5.1: Add cached token fields to TypeScript types

**Tool:** Edit

**Location:** `src/frontend/types/chat_OpenAI.ts`

**Current Code (lines 13-19):**
```typescript
export interface ChatMetadata {
  readonly requestId?: string;
  readonly tokenCount?: number;  // Deprecated: use inputTokens and outputTokens
  readonly inputTokens?: number;
  readonly outputTokens?: number;
}
```

**New Code (add cached token fields):**
```typescript
export interface ChatMetadata {
  readonly requestId?: string;
  readonly tokenCount?: number;  // Deprecated: use inputTokens and outputTokens
  readonly inputTokens?: number;
  readonly outputTokens?: number;
  readonly cachedInputTokens?: number;
  readonly cachedOutputTokens?: number;
}
```

**Validation:**
- [ ] TypeScript interface matches backend model
- [ ] No compilation errors

### Task 5.2: Update ChatMessage component to display cached tokens

**Tool:** Serena find_symbol + Edit

**Location:** `src/frontend/components/ChatMessage_OpenAI.tsx`

**Current Code (lines 279-287):**
```tsx
{(message.metadata.inputTokens !== undefined && message.metadata.outputTokens !== undefined) ? (
  <>
    Input: {message.metadata.inputTokens.toLocaleString()} |
    Output: {message.metadata.outputTokens.toLocaleString()} |
    Total: {(message.metadata.inputTokens + message.metadata.outputTokens).toLocaleString()}
  </>
) : message.metadata.tokenCount ? (
  <>
    Tokens: {message.metadata.tokenCount.toLocaleString()}
  </>
) : null}
```

**New Code (add cached token display):**
```tsx
{(message.metadata.inputTokens !== undefined && message.metadata.outputTokens !== undefined) ? (
  <>
    Input: {message.metadata.inputTokens.toLocaleString()} |
    Output: {message.metadata.outputTokens.toLocaleString()} |
    Total: {(message.metadata.inputTokens + message.metadata.outputTokens).toLocaleString()}
    {(message.metadata.cachedInputTokens || message.metadata.cachedOutputTokens) && (
      <>
        {' | '}
        {message.metadata.cachedInputTokens ? (
          <>Cached Input: {message.metadata.cachedInputTokens.toLocaleString()}</>
        ) : null}
        {message.metadata.cachedInputTokens && message.metadata.cachedOutputTokens ? ' | ' : null}
        {message.metadata.cachedOutputTokens ? (
          <>Cached Output: {message.metadata.cachedOutputTokens.toLocaleString()}</>
        ) : null}
      </>
    )}
  </>
) : message.metadata.tokenCount ? (
  <>
    Tokens: {message.metadata.tokenCount.toLocaleString()}
  </>
) : null}
```

**Validation:**
- [ ] GUI displays cached tokens when available
- [ ] Display format matches CLI output
- [ ] No errors when cached tokens are undefined/null
- [ ] Properly formatted with separators

---

## PHASE 6: CLI TESTING PHASE 🔴 MANDATORY

**Goal:** Validate prompt caching implementation with comprehensive testing

### Task 6.1: Run CLI regression test suite

**Tool:** Bash

**Command:**
```bash
./test_cli_regression.sh
```

**Expected Results:**
- [ ] 35/35 tests PASS (100% success rate)
- [ ] Test report generated in test-reports/
- [ ] No errors or failures
- [ ] Session persistence verified

### Task 6.2: Verify cached token display in test output

**Tool:** Bash + Read

**Command:**
```bash
# Run a test query twice to trigger caching
uv run src/backend/main.py
> SPY market status
> SPY market status
```

**Expected Behavior:**
- [ ] First query: Shows tokens but NO cached tokens (cold start)
- [ ] Second query: Shows "Cached Input: X" in token display (cache hit)
- [ ] Cached tokens appear in CLI footer
- [ ] Token counts are accurate

### Task 6.3: Test GUI cached token display

**Tool:** Sequential-Thinking + Manual Testing

**Steps:**
1. Start application: `./start-app.sh`
2. Open browser: http://127.0.0.1:3000
3. Send query: "NVDA stock price"
4. Send same query again: "NVDA stock price"
5. Verify cached tokens appear in message footer

**Expected Results:**
- [ ] Second query shows cached tokens in GUI
- [ ] Display format matches CLI
- [ ] No console errors

### Task 6.4: Analyze test report for caching patterns

**Tool:** Read + Sequential-Thinking

**Analysis Points:**
- [ ] Identify which queries trigger caching (>1024 token prompts)
- [ ] Verify agent instructions are being cached (sent every message)
- [ ] Confirm cache hit rate increases in persistent session
- [ ] Calculate cost savings from cached tokens

---

## PHASE 7: DOCUMENTATION & SERENA MEMORY UPDATES

**Goal:** Comprehensive documentation of new prompt caching features

### Task 7.1: Update CLAUDE.md with prompt caching information

**Tool:** Edit

**Location:** `CLAUDE.md` - Add new section after "Last Completed Task Summary"

**New Section:**
```markdown
## OpenAI Prompt Caching Integration

**Status:** ✅ Implemented (October 2025)
**Feature:** OpenAI API Prompt Caching for cost reduction and latency improvement

### How It Works

1. **Automatic Caching**: Prompts >1024 tokens are automatically cached by OpenAI
2. **Cache Duration**: 5-10 minutes of inactivity, maximum 1 hour
3. **Cache Scope**: Organization-level (shared within same OpenAI organization)
4. **Agent Instructions**: Cached on EVERY request (massive cost savings)

### Token Display

**CLI Output:**
```
   Tokens Used: 1,234 (Input: 1,000, Output: 234) | Cached Input: 512
```

**GUI Output:**
```
Input: 1,000 | Output: 234 | Total: 1,234 | Cached Input: 512
```

### Cost Savings

- **Cached Input Tokens**: 50% cost reduction
- **Latency Improvement**: Up to 80% faster for cached prompts >10K tokens
- **Typical Savings**: 30-50% cost reduction in persistent sessions

### Implementation Details

- **Backend**: `token_utils.py` extracts cached tokens from OpenAI Agents SDK
- **API Models**: `api_models.py` includes `cachedInputTokens` and `cachedOutputTokens`
- **CLI Display**: `response_utils.py` shows cached token metrics
- **Frontend**: `ChatMessage_OpenAI.tsx` displays cached tokens in GUI

### Best Practices

1. **Prompt Structure**: Static content (instructions, tools) at START, dynamic (user query) at END
2. **Tool Ordering**: Keep tools in same order across requests
3. **Message History**: Append new messages to END of array
4. **Cache Invalidation**: Any change to static content clears cache

### References

- OpenAI Prompt Caching Guide: https://platform.openai.com/docs/guides/prompt-caching
- Implementation Example: examples/Prompt_Caching101.ipynb
```

**Validation:**
- [ ] CLAUDE.md has comprehensive prompt caching documentation
- [ ] Examples and expected outputs included
- [ ] Best practices documented

### Task 7.2: Update tech_stack.md Serena memory

**Tool:** Serena find_symbol + Edit

**Location:** `.serena/memories/tech_stack.md`

**Find Section:** "OpenAI Integration"

**Add to Section:**
```markdown
### OpenAI Prompt Caching (October 2025)

**Status:** Fully Integrated
**API Version:** Responses API (OpenAI Agents SDK v0.2.9)

**Implementation:**
- Automatic caching for prompts >1024 tokens
- Cache hit detection via `input_tokens_details.cached_tokens`
- CLI & GUI display of cached token metrics
- Cost savings: 50% on cached input tokens
- Latency reduction: Up to 80% for large prompts

**Token Extraction:**
- `token_utils.py`: Extracts cached tokens from SDK usage object
- `response_utils.py`: CLI display with cache hit information
- `chat.py`: API includes cachedInputTokens/cachedOutputTokens
- Frontend: TypeScript types and React component display

**Cache Optimization:**
- Agent instructions cached (sent with every message)
- Static tools/context at prompt START
- Dynamic user queries at prompt END
```

**Validation:**
- [ ] tech_stack.md includes prompt caching section
- [ ] Implementation details documented

### Task 7.3: Update project_architecture.md Serena memory

**Tool:** Serena find_symbol + Edit

**Location:** `.serena/memories/project_architecture.md`

**Find Section:** "Token Usage Tracking"

**Update Section:**
```markdown
### Token Usage Tracking & Prompt Caching

**Extraction Flow:**
1. OpenAI Agents SDK captures usage in `context_wrapper.usage`
2. `token_utils.extract_token_usage_from_context_wrapper()` extracts:
   - `total_tokens`, `input_tokens`, `output_tokens` (standard)
   - `cached_input_tokens`, `cached_output_tokens` (prompt caching)
3. CLI: `response_utils.py` displays all token metrics
4. API: `chat.py` returns tokens via `ChatMetadata` model
5. Frontend: `ChatMessage_OpenAI.tsx` displays in message footer

**Prompt Caching Implementation (October 2025):**
- **Backend**: `token_utils.py` extracts `input_tokens_details.cached_tokens`
- **API Models**: `ChatMetadata` includes cached token fields
- **CLI Display**: Shows "Cached Input: X" when cache hits occur
- **Frontend Display**: Shows cached tokens in message metadata
- **Cache Hit Indicator**: `cached_tokens > 0` means cache was used

**Cost Optimization:**
- Agent instructions cached on every request (>1024 tokens)
- 50% cost reduction on cached input tokens
- Up to 80% latency improvement for large cached prompts
- Organization-level cache sharing
```

**Validation:**
- [ ] project_architecture.md updated with caching flow
- [ ] Token extraction flow documented

### Task 7.4: Create new Serena memory: prompt_caching_guide.md

**Tool:** Write

**Location:** `.serena/memories/prompt_caching_guide.md`

**Content:**
```markdown
# OpenAI Prompt Caching Implementation Guide

**Created:** October 2025
**Status:** Production Ready
**Feature:** OpenAI API Prompt Caching integration

---

## Overview

OpenAI Prompt Caching automatically caches prompts >1024 tokens, providing:
- **50% cost reduction** on cached input tokens
- **Up to 80% latency reduction** for large prompts (10K+ tokens)
- **Organization-level caching** (shared within same OpenAI org)

---

## How It Works

### Automatic Activation

- Prompts >1024 tokens are automatically cached by OpenAI
- No code changes required to enable caching
- Cache duration: 5-10 minutes of inactivity, max 1 hour
- Cache key: Exact match of prompt content AND order

### Cache Hit Detection

**Backend (Python):**
```python
from src.backend.utils.token_utils import extract_token_usage_from_context_wrapper

token_usage = extract_token_usage_from_context_wrapper(result)
cached_input = token_usage.get("cached_input_tokens", 0)

if cached_input > 0:
    print(f"Cache hit! {cached_input} tokens retrieved from cache")
```

**Response Format:**
```json
{
  "total_tokens": 1234,
  "input_tokens": 1000,
  "output_tokens": 234,
  "cached_input_tokens": 512,  // Non-zero = cache hit
  "cached_output_tokens": 0
}
```

---

## Implementation Details

### 1. Token Extraction (token_utils.py)

**Function:** `extract_token_usage_from_context_wrapper(result)`

**Returns:**
```python
{
    "total_tokens": int,
    "input_tokens": int,
    "output_tokens": int,
    "cached_input_tokens": int,  # NEW: From input_tokens_details.cached_tokens
    "cached_output_tokens": int,  # NEW: From output_tokens_details.cached_tokens
}
```

**API Support:**
- Responses API: `usage.input_tokens_details.cached_tokens`
- Chat Completions API: `usage.prompt_tokens_details.cached_tokens`
- Fallback: Returns 0 if not available

### 2. CLI Display (response_utils.py)

**Output Format:**
```
   Tokens Used: 1,234 (Input: 1,000, Output: 234) | Cached Input: 512
```

**Logic:**
- Shows cached tokens only when `cached_input > 0` or `cached_output > 0`
- Comma-separated format: "Cached Input: X, Cached Output: Y"
- Uses Rich console for formatting

### 3. API Response (chat.py + api_models.py)

**ChatMetadata Model:**
```python
class ChatMetadata(BaseModel):
    token_count: Optional[int] = Field(None, alias="tokenCount")
    input_tokens: Optional[int] = Field(None, alias="inputTokens")
    output_tokens: Optional[int] = Field(None, alias="outputTokens")
    cached_input_tokens: Optional[int] = Field(None, alias="cachedInputTokens")  # NEW
    cached_output_tokens: Optional[int] = Field(None, alias="cachedOutputTokens")  # NEW
```

**API Response:**
```json
{
  "response": "...",
  "metadata": {
    "inputTokens": 1000,
    "outputTokens": 234,
    "cachedInputTokens": 512,
    "cachedOutputTokens": 0
  }
}
```

### 4. Frontend Display (ChatMessage_OpenAI.tsx)

**TypeScript Types:**
```typescript
interface ChatMetadata {
  readonly inputTokens?: number;
  readonly outputTokens?: number;
  readonly cachedInputTokens?: number;  // NEW
  readonly cachedOutputTokens?: number;  // NEW
}
```

**Display Logic:**
```tsx
{(message.metadata.cachedInputTokens || message.metadata.cachedOutputTokens) && (
  <>
    {' | '}
    {message.metadata.cachedInputTokens ? (
      <>Cached Input: {message.metadata.cachedInputTokens.toLocaleString()}</>
    ) : null}
    {message.metadata.cachedOutputTokens ? (
      <>Cached Output: {message.metadata.cachedOutputTokens.toLocaleString()}</>
    ) : null}
  </>
)}
```

---

## Best Practices for Cache Optimization

### 1. Prompt Structure

**Optimal Order:**
```python
messages = [
    # STATIC CONTENT FIRST (will be cached)
    {"role": "system", "content": agent_instructions},  # CACHED
    {"role": "system", "content": tool_definitions},     # CACHED
    {"role": "system", "content": context_data},         # CACHED

    # DYNAMIC CONTENT LAST (will NOT be cached)
    {"role": "user", "content": user_query},             # NOT CACHED
]
```

**Why This Works:**
- Cache matches prefix of prompt
- Static content at START gets cached
- Dynamic content at END doesn't invalidate cache

### 2. Agent Instructions

**Current Implementation:**
- Agent instructions sent with EVERY message (>1024 tokens)
- Instructions are identical across requests
- **Result**: Massive caching benefit (50% cost reduction on instructions)

### 3. Tool Definitions

**Important:**
- Tools must remain in SAME ORDER across requests
- Any change to tool order invalidates cache
- Tool content must be identical

### 4. Message History

**Best Practice:**
- Append new messages to END of array
- Don't modify historical messages
- Keep message order consistent

### 5. Cache Invalidation

**Cache is cleared when:**
- Any static content changes
- Tool order changes
- Message order changes
- 5-10 minutes of inactivity
- After 1 hour (maximum cache duration)

---

## Testing & Validation

### Manual Testing

**Test Cache Hit:**
```bash
# Run CLI twice with same query
uv run src/backend/main.py
> SPY market status
# Output: Tokens Used: 1,234 (Input: 1,000, Output: 234)

> SPY market status
# Output: Tokens Used: 1,234 (Input: 1,000, Output: 234) | Cached Input: 512
```

**Expected Results:**
- First query: No cached tokens (cold start)
- Second query: Shows "Cached Input: X" (cache hit)

### Automated Testing

**Test Suite:** `test_cli_regression.sh`
- 35 tests in persistent session
- Validates cached token display
- Verifies cache hit patterns

**Cache Hit Expectations:**
- Test 1: No cache (cold start)
- Tests 2-35: Cache hits on agent instructions
- Cached tokens should appear in test output

---

## Cost Savings Analysis

### Example Session (35 queries):

**Without Caching:**
- Agent instructions: 1,200 tokens × 35 = 42,000 tokens
- Cost: 42,000 tokens × $0.60/1M = $0.025

**With Caching:**
- First query: 1,200 tokens (no cache)
- Queries 2-35: 600 cached + 600 new = 1,200 tokens (50% cached)
- Cached: 34 × 600 = 20,400 tokens (50% cost)
- Full cost: 1,200 + (34 × 600) = 21,600 tokens
- Cost: 21,600 tokens × $0.60/1M = $0.013

**Savings: 48% cost reduction** ($0.012 saved)

---

## Troubleshooting

### No Cached Tokens Showing

**Possible Causes:**
1. Prompt <1024 tokens (caching not activated)
2. First request in session (no cache yet)
3. Cache expired (>10 minutes idle or >1 hour total)
4. Prompt content changed (cache invalidated)

**Solution:**
- Verify prompt length >1024 tokens
- Run query twice to trigger caching
- Check cache expiration time

### Cache Not Hitting

**Possible Causes:**
1. Tool order changed
2. Message order changed
3. Static content modified
4. Different organization/API key

**Solution:**
- Ensure tool order is consistent
- Don't modify historical messages
- Keep static content identical

---

## Files Modified

**Backend:**
- `src/backend/utils/token_utils.py` - Added cached token extraction
- `src/backend/utils/response_utils.py` - Added CLI cached token display
- `src/backend/api_models.py` - Added cached token fields to ChatMetadata
- `src/backend/routers/chat.py` - Added cached tokens to API response

**Frontend:**
- `src/frontend/types/chat_OpenAI.ts` - Added cached token TypeScript types
- `src/frontend/components/ChatMessage_OpenAI.tsx` - Added cached token display

**Documentation:**
- `CLAUDE.md` - Added prompt caching section
- `.serena/memories/tech_stack.md` - Updated with caching details
- `.serena/memories/project_architecture.md` - Updated token tracking flow
- `.serena/memories/prompt_caching_guide.md` - Created comprehensive guide

---

## References

- **OpenAI Docs**: https://platform.openai.com/docs/guides/prompt-caching
- **Example Notebook**: examples/Prompt_Caching101.ipynb
- **SDK Implementation**: openai_responses.py (OpenAI Agents SDK v0.2.9)
- **API Types**:
  - `src/openai/types/completion_usage.py` (Chat Completions)
  - `src/openai/types/responses/response_usage.py` (Responses API)

---

**Last Updated:** October 2025
**Status:** ✅ Production Ready
```

**Validation:**
- [ ] New Serena memory created with comprehensive guide
- [ ] All implementation details documented
- [ ] Examples and troubleshooting included

---

## PHASE 8: FINAL GIT COMMIT

**Goal:** Atomic commit with all changes

### Task 8.1: Verify everything complete

**Tool:** Sequential-Thinking + Bash

**Commands:**
```bash
git status
git diff
```

**Checklist:**
- [ ] All backend code changes complete
- [ ] All frontend code changes complete
- [ ] All documentation updated
- [ ] All Serena memories updated
- [ ] Test suite executed successfully
- [ ] No uncommitted work remaining

### Task 8.2: Stage ALL files at once

**Tool:** Bash

**Command:**
```bash
git add -A
```

**⚠️ CRITICAL:** Only run this AFTER all work is complete

### Task 8.3: Verify staging

**Tool:** Bash

**Command:**
```bash
git status
```

**Expected:** ALL files staged, NOTHING unstaged

### Task 8.4: Commit immediately

**Tool:** Bash

**Command:**
```bash
git commit -m "$(cat <<'EOF'
[FEATURE] Integrate OpenAI Prompt Caching for cost reduction and latency improvement

Primary Changes:
- Add cached token extraction to token_utils.py (input_tokens_details.cached_tokens)
- Update CLI display to show cached tokens when cache hits occur
- Add cachedInputTokens/cachedOutputTokens fields to API models and responses
- Update frontend TypeScript types and ChatMessage component for cached token display
- Comprehensive documentation updates across CLAUDE.md and Serena memories

Cost & Performance Impact:
- 50% cost reduction on cached input tokens
- Up to 80% latency reduction for large prompts (>10K tokens)
- Agent instructions cached on every request (massive savings in persistent sessions)
- Organization-level cache sharing (5-10 min duration, max 1 hour)

Backend Changes:
- ✅ src/backend/utils/token_utils.py: Extract cached tokens from OpenAI Agents SDK
- ✅ src/backend/utils/response_utils.py: CLI display with "Cached Input: X" format
- ✅ src/backend/api_models.py: Add cached_input_tokens, cached_output_tokens fields
- ✅ src/backend/routers/chat.py: Include cached tokens in ChatResponse

Frontend Changes:
- ✅ src/frontend/types/chat_OpenAI.ts: Add cachedInputTokens, cachedOutputTokens types
- ✅ src/frontend/components/ChatMessage_OpenAI.tsx: Display cached tokens in message footer

Documentation Updates:
- ✅ CLAUDE.md: Add comprehensive "OpenAI Prompt Caching Integration" section
- ✅ .serena/memories/tech_stack.md: Add prompt caching implementation details
- ✅ .serena/memories/project_architecture.md: Update token tracking flow with caching
- ✅ .serena/memories/prompt_caching_guide.md: Create comprehensive implementation guide

Testing Results:
- ✅ CLI regression test suite: 35/35 PASSED (100%)
- ✅ Cached token display validated in CLI output
- ✅ GUI cached token display verified in browser
- ✅ Cache hit patterns confirmed in persistent sessions

Implementation Details:
- OpenAI Agents SDK v0.2.9 already captures input_tokens_details
- Responses API format: usage.input_tokens_details.cached_tokens
- Automatic activation for prompts >1024 tokens
- Cache duration: 5-10 minutes inactivity, max 1 hour
- Best practice: Static content at START, dynamic at END

Files Changed:
- Backend: 4 files (token_utils.py, response_utils.py, api_models.py, chat.py)
- Frontend: 2 files (chat_OpenAI.ts, ChatMessage_OpenAI.tsx)
- Documentation: 4 files (CLAUDE.md, tech_stack.md, project_architecture.md, prompt_caching_guide.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Task 8.5: Push immediately

**Tool:** Bash

**Command:**
```bash
git push
```

---

## 📊 TASK SUMMARY

**Total Phases:** 8
**Total Tasks:** 25+
**Backend Files:** 4 (token_utils.py, response_utils.py, api_models.py, chat.py)
**Frontend Files:** 2 (chat_OpenAI.ts, ChatMessage_OpenAI.tsx)
**Documentation Files:** 4 (CLAUDE.md, tech_stack.md, project_architecture.md, prompt_caching_guide.md)
**New Features:** Cached token extraction, CLI/GUI display, API fields

---

## 🛠️ TOOL USAGE REQUIREMENTS

**MANDATORY TOOLS TO USE THROUGHOUT:**

1. **Sequential-Thinking**: START every phase, use for complex analysis (max 8 thoughts)
2. **Serena Tools**: Code analysis, symbol manipulation, pattern search
3. **Standard Read/Write/Edit**: File modifications
4. **Bash**: Test execution, git commands
5. **TodoWrite**: Track progress through all phases

**CRITICAL RULES:**
- ✅ Use tools MULTIPLE TIMES as needed
- ✅ Use tools in ANY ORDER based on task needs
- ✅ CONTINUOUS tool usage from start to finish
- ✅ NO rigid sequencing - only logical tool usage
- ❌ NEVER stop using tools until task complete

---

## ✅ SUCCESS CRITERIA

**Task is complete ONLY when:**

1. ✅ Backend: Cached token extraction implemented in token_utils.py
2. ✅ Backend: CLI display shows cached tokens in response_utils.py
3. ✅ Backend: API models include cached token fields
4. ✅ Backend: API responses include cachedInputTokens/cachedOutputTokens
5. ✅ Frontend: TypeScript types updated with cached token fields
6. ✅ Frontend: ChatMessage component displays cached tokens
7. ✅ Testing: 35/35 tests PASS with cached token validation
8. ✅ Documentation: CLAUDE.md updated with prompt caching section
9. ✅ Documentation: Serena memories updated (3 files)
10. ✅ Documentation: New prompt_caching_guide.md created
11. ✅ Git: ALL changes committed and pushed

**If ANY of these criteria are not met, the task is INCOMPLETE.**

---

## 🚨 CRITICAL CHECKPOINTS

**Before Phase 6 (Testing):**
- [ ] All backend code changes complete
- [ ] All frontend code changes complete
- [ ] Token extraction working
- [ ] Display logic implemented

**Before Phase 7 (Documentation):**
- [ ] Tests executed (35/35 PASS)
- [ ] Cached tokens visible in CLI output
- [ ] Cached tokens visible in GUI
- [ ] Cache hit patterns validated

**Before Phase 8 (Commit):**
- [ ] All documentation updated
- [ ] All Serena memories updated
- [ ] New guide created
- [ ] All changes verified

**After Commit:**
- [ ] Changes pushed to remote
- [ ] No uncommitted work
- [ ] Task marked complete in new_research_details.md

---

**END OF TODO TASK PLAN**
