# Research Task Plan: Markdown-Only Output Formatting

**Date**: October 18, 2025
**Status**: Research Complete - Ready for Planning Phase
**Objective**: Implement consolidated Markdown-only output formatting for CLI and Gradio UI

---

## Executive Summary

Research confirms that implementing consolidated Markdown-only output formatting is **SIMPLE and STRAIGHTFORWARD**. Both CLI and Gradio already have built-in Markdown support. The task reduces to:

1. **Remove Rich Console Markdown rendering** from CLI (keep for status messages only)
2. **Ensure AI agent outputs pure Markdown** (already mostly happening)
3. **Let Gradio render Markdown natively** (already supported, just needs activation)

**Estimated Complexity**: LOW (2-3 file changes, minimal code modifications)
**Risk Level**: LOW (Gradio natively supports Markdown, minimal breaking changes)

---

## Key Research Findings

### 1. Gradio ChatInterface Markdown Support

**CONFIRMED**: Gradio Chatbot component NATIVELY supports Markdown rendering.

**Source**: `/gradio/components/chatbot.py` (lines 372-374, 408)

```python
sanitize_html: bool = True,
render_markdown: bool = True,  # ← DEFAULT is TRUE
line_breaks: bool = True,  # ← GitHub-flavored Markdown line breaks
```

**Documentation Quote**:
> "Creates a chatbot that displays user-submitted messages and responses. **Supports a subset of Markdown including bold, italics, code, tables.**"

**Critical Parameters:**
- `render_markdown=True` (DEFAULT) - Enables Markdown rendering
- `line_breaks=True` (DEFAULT) - GitHub-flavored Markdown
- Supports: **bold**, *italics*, `code`, **tables**, lists, headers

**Current Project Status:**
- ✅ `gradio_app.py` uses `type="messages"` (correct)
- ❓ `render_markdown` not explicitly set (defaults to True)
- ❓ Current streaming returns plain text (no Markdown awareness)

---

### 2. Markdown Table Formatting Standards

**Source**: Context7 - `python-markdown2` library + Markdown Guide

**Standard Table Syntax:**
```markdown
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

**Alignment Options:**
| Alignment | Syntax | Use Case |
|-----------|--------|----------|
| Default (left) | `\| -------- \|` | Text (Symbol, Type) |
| Left | `\| :--- \|` | Explicit left align |
| Center | `\| :----: \|` | Headers, labels |
| Right | `\| ----: \|` | Numbers (Price, Volume, %) |

**Financial Data Best Practices:**

**Options Chain Table:**
```markdown
| Strike ($) | Bid ($) | Ask ($) | Volume | Open Interest | Delta |
| ---------: | ------: | ------: | -----: | ------------: | ----: |
| 450.00     | 2.35    | 2.40    | 1,250  | 5,830         | 0.45  |
| 455.00     | 1.85    | 1.90    | 890    | 3,210         | 0.38  |
```

**OHLC Price History:**
```markdown
| Date | Open ($) | High ($) | Low ($) | Close ($) | Volume |
| :--- | -------: | -------: | ------: | --------: | -----: |
| 2025-10-17 | 585.20 | 587.45 | 583.10 | 585.30 | 25M |
| 2025-10-16 | 583.50 | 585.80 | 582.00 | 584.10 | 22M |
```

**Technical Analysis Indicators:**
```markdown
| Indicator | Value | Signal |
| :-------- | ----: | :----- |
| RSI-14 | 67.5 | Approaching Overbought |
| MACD | 1.23 | Bullish |
| SMA-20 | 580.25 | Support Level |
| SMA-50 | 572.10 | Bullish Above |
```

**Multi-Ticker Comparison:**
```markdown
| Symbol | Price ($) | Change ($) | Change (%) | Volume |
| :----- | --------: | ---------: | ---------: | -----: |
| SPY    | 585.30    | +2.15      | +0.37%     | 25M    |
| QQQ    | 485.70    | +3.20      | +0.66%     | 18M    |
| IWM    | 225.40    | -0.50      | -0.22%     | 12M    |
```

**Key Principles:**
1. Left-align text columns (Symbol, Date, Type)
2. Right-align numeric columns (Price, Volume, Change %)
3. Use pipes on both ends for clarity
4. Keep headers descriptive and concise
5. Support empty cells with blank space between pipes

---

### 3. Current CLI/Gradio Formatting Implementation

**File 1: `src/backend/utils/response_utils.py`**

**Current Implementation:**
```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def print_response(response_text: str):
    console.print("\n[bold green]✅ Query processed successfully![/bold green]")
    console.print("[bold]Agent Response:[/bold]\n")

    # Markdown detection
    has_markdown = any(tag in response_text for tag in ["#", "*", "`", "-", ">"])

    if has_markdown:
        console.print(Markdown(response_text))  # ← Rich renders Markdown
    else:
        console.print(response_text)

    console.print("\n[dim]" + "─" * 50 + "[/dim]\n")
```

**Issue:**
- Uses `Rich.Markdown()` to render Markdown in terminal
- This is TERMINAL-SPECIFIC rendering (colored output, formatted tables)
- Gradio receives this same response but doesn't understand Rich markup
- Solution: Output pure Markdown strings, let each interface render natively

**File 2: `src/backend/cli.py`**

**Current Implementation:**
```python
async def process_query_with_footer(agent, session, user_input):
    # Process query
    result = await process_query(agent, session, user_input)
    response_text = str(result.final_output)

    # Format footer (plain text)
    footer = _format_performance_footer(processing_time, token_usage, model_name)

    # Return complete response with footer
    return response_text + "\n\n" + footer
```

**Status:** ✅ Correct - Returns plain text response + plain text footer

**File 3: `src/backend/gradio_app.py`**

**Current Implementation:**
```python
async def chat_with_agent(message: str, history: List):
    # Call CLI core function - returns complete response with footer
    complete_response = await process_query_with_footer(agent, session, message)

    # Gradio streaming: yield progressive chunks
    sentences = complete_response.replace(". ", ".|").split("|")
    accumulated = ""

    for sentence in sentences:
        accumulated += sentence
        yield accumulated
        await asyncio.sleep(0.05)
```

**Issues:**
- Streams plain text chunks
- No explicit `render_markdown=True` set on Chatbot component
- Streaming is sentence-based, doesn't consider Markdown table boundaries

---

### 4. AI Agent Instructions Analysis

**File: `src/backend/services/agent_service.py`**

**Current Agent Instructions (Critical Sections):**

**Line 500-511**: "PRESERVE ALL TOOL-GENERATED TABLES AND CHARTS"
```
🔴 BLANKET RULE FOR ALL TABLES/CHARTS:
  * ❌ DO NOT reformat tables into bullet points
  * ❌ DO NOT reformat tables into plain text
  * ❌ DO NOT remove column headers
  * ✅ COPY the tool response EXACTLY as returned
  * ✅ Preserve markdown table syntax with pipe separators (|)
  * ✅ Keep all headers and data intact
```

**Line 526-543**: "WHEN TO USE MARKDOWN TABLES"
- Options chain data
- OHLC bars with multiple dates
- Multiple TA indicators (SMA 20/50/200, EMA 20/50/200)
- Multi-ticker comparisons (2+ tickers)
- Multi-dimensional data (ticker + date + metrics)

**Status:** ✅ Agent is ALREADY instructed to output Markdown tables

**Observation:**
- Agent instructions are comprehensive and correct
- The issue is NOT with agent output format
- The issue is with CLI rendering (Rich) vs Gradio rendering (plain text)

---

## Problem Statement

### Current Architecture

```
User Input
    ↓
AI Agent (outputs Markdown tables per instructions)
    ↓
process_query_with_footer() → Returns: Markdown string + plain text footer
    ↓
┌─────────────────────────────┬──────────────────────────────┐
│         CLI Path            │        Gradio Path           │
├─────────────────────────────┼──────────────────────────────┤
│ print_response()            │ chat_with_agent()            │
│   ↓                         │   ↓                          │
│ Rich.Markdown() renders     │ Plain text streaming         │
│ (terminal colors/tables)    │ (no Markdown rendering)      │
│   ↓                         │   ↓                          │
│ Terminal Output             │ Gradio ChatInterface         │
│ ✅ Beautiful formatted      │ ❌ Raw Markdown text         │
└─────────────────────────────┴──────────────────────────────┘
```

### The Issues

1. **CLI**: Uses Rich Console to render Markdown → Works beautifully in terminal
2. **Gradio**: Receives Markdown strings but displays as plain text → Tables show as raw `| Header |` syntax
3. **Inconsistency**: Two different rendering approaches for same Markdown content

---

## Solution Design

### Proposed Architecture

```
User Input
    ↓
AI Agent (outputs pure Markdown tables)
    ↓
process_query_with_footer() → Returns: Pure Markdown string + plain text footer
    ↓
┌─────────────────────────────┬──────────────────────────────┐
│         CLI Path            │        Gradio Path           │
├─────────────────────────────┼──────────────────────────────┤
│ print_response()            │ chat_with_agent()            │
│   ↓                         │   ↓                          │
│ Print pure Markdown         │ Yield Markdown chunks        │
│ (OR keep Rich for terminal) │ Gradio renders natively      │
│   ↓                         │   ↓                          │
│ Terminal Output             │ Gradio ChatInterface         │
│ ✅ Markdown or Rich         │ ✅ Rendered Markdown tables  │
└─────────────────────────────┴──────────────────────────────┘
```

### Key Changes Required

#### Change 1: Update Gradio ChatInterface Configuration

**File**: `src/backend/gradio_app.py`

**Current:**
```python
demo = gr.ChatInterface(
    fn=chat_with_agent,
    type="messages",
    # render_markdown not explicitly set (defaults to True)
)
```

**New:**
```python
demo = gr.ChatInterface(
    fn=chat_with_agent,
    type="messages",
    chatbot=gr.Chatbot(
        render_markdown=True,      # ← Explicit Markdown rendering
        line_breaks=True,           # ← GitHub-flavored Markdown
        sanitize_html=True,         # ← Security
        height=600                  # ← Better table visibility
    )
)
```

#### Change 2: CLI Markdown Handling Decision

**Option A: Keep Rich Console for Terminal** (Recommended)
- Pro: Beautiful terminal output with colors and formatting
- Pro: No breaking changes for CLI users
- Pro: Each interface uses native capabilities
- Con: Two different rendering paths

**Option B: Pure Markdown Everywhere**
- Pro: Single rendering approach
- Pro: Consistent output format
- Con: Terminal output loses colors and Rich formatting
- Con: Worse UX for CLI users

**Recommendation**: Option A - Keep Rich Console for CLI, enable Gradio Markdown rendering

---

## Implementation Summary

### Minimal Changes (Recommended)

1. **Update `gradio_app.py`**: Explicitly set `render_markdown=True`
2. **Test with existing code**: Verify Gradio renders Markdown tables
3. **Keep CLI unchanged**: Rich Console continues working

**Estimated Effort**: 5-10 lines of code
**Risk**: VERY LOW
**Impact**: Gradio immediately renders Markdown tables

---

## Conclusion

**Research Status**: ✅ COMPLETE

**Key Insight**: The implementation is MUCH SIMPLER than expected because:
1. Gradio NATIVELY supports Markdown rendering (just needs activation)
2. AI agent is ALREADY outputting Markdown tables (per instructions)
3. Only gap is Gradio configuration

**Recommended Approach**:
- Enable Gradio Markdown rendering (5-10 lines of code)
- Test thoroughly with existing AI output
- Keep CLI Rich Console for best terminal UX

**Next Phase**: Planning - Generate detailed `TODO_task_plan.md`

---

**Research Completed By**: Claude (Sequential-Thinking + Serena + Context7 + Gradio Docs)
**Date**: October 18, 2025
