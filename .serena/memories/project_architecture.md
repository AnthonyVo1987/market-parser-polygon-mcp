# Project Architecture

## Overview

Market Parser is a Python CLI, React web application, and Gradio ChatInterface for natural language financial queries using Direct Polygon/Tradier API integration and OpenAI GPT-5-Nano via the OpenAI Agents SDK v0.2.9.

**Key Architectural Changes (Oct 2025):**
- **Performance Metrics Footer Consolidation** (Oct 17, 2025) - Single source of truth in CLI core ⭐ NEW
- **Persistent Agent Architecture** (ONE agent per lifecycle, CLI = core, GUI = wrapper)
- **Migrated from MCP to Direct API** (70% performance improvement)
- **Added Gradio ChatInterface** (port 7860) ⭐ - Third frontend option

## Performance Metrics Footer Architecture (Oct 17, 2025) ⭐ NEW

### Problem Solved

**Before (❌ Code Duplication):**
- Footer duplicated 3x across CLI, React, and Gradio (~200 lines duplicate code)
- Each interface independently extracted metadata and formatted footer

**After (✅ Single Source of Truth):**
- Footer generated ONCE in CLI core (`process_query_with_footer()`)
- All interfaces receive complete response with footer included
- Zero duplication (~100 lines deleted, 17% code reduction)

### Implementation

#### Core Functions (src/backend/cli.py)

**1. `_format_performance_footer()`** - Canonical formatter (plain text, 30 lines)
**2. `process_query_with_footer()`** - Wrapper function (40 lines)

Returns complete response with footer:
```
[Agent Response]

Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299) | Cached Input: 11,776
   Model: gpt-5-nano
```

#### Interface Integration

**CLI**: Deleted ~50 lines from `print_response()` - now displays complete response
**React**: Deleted ~50 lines from `chat.py` endpoint - now returns complete response  
**React Frontend**: Deleted ~40 lines from `ChatMessage_OpenAI.tsx` - footer rendered as markdown
**Gradio**: Deleted ~60 lines from `chat_with_agent()` - now streams complete response

### Benefits

1. **Zero Duplication**: Footer logic exists ONCE (single source of truth)
2. **Scalability**: New UI frameworks need zero footer code
3. **Maintainability**: Footer changes update 1 function only
4. **Consistency**: Identical footer across all interfaces

### Testing Results

**Bug Fix**: Fixed critical import error (`extract_token_usage_from_context_wrapper`)
**Test Suite**: 39/39 PASSED (100%), 9.67s avg (EXCELLENT), footer verified in all responses

**Files Changed**: 5 files (cli.py, response_utils.py, chat.py, ChatMessage_OpenAI.tsx, gradio_app.py)

(NOTE: Full project architecture documentation continues - this is the new consolidated footer section only)