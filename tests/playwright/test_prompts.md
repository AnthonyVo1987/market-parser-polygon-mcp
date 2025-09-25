# Standardized Test Prompts

**Document Purpose:** This is the single source of truth for all
standardized test prompts used in Market Parser testing. All AI agents
and testing procedures MUST use these exact prompts to ensure
consistent, quick responses and avoid false failures.

**Target Audience:** AI Coding Agents, Test Specialists, and anyone
performing Market Parser testing
**Expected Outcome:** Consistent 30-60 second response times with minimal
tool calls
**Methodology:** Quick response prompts designed to avoid complex
processing that could cause timeouts

---

## CRITICAL TESTING RULES

**MANDATORY REQUIREMENTS:**

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 30-60 seconds
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

---

## Quick Response Test Prompts

### 1. Market Status Query

#### Test Prompt 1: Market Status Query

"Quick Response Needed with minimal tool calls: What is the current Market Status?"

### 2. Single Stock Snapshot

#### Test Prompt 2: Single Stock Snapshot

"Quick Response Needed with minimal tool calls: Based on Market Status Date, Single Stock Snapshot NVDA"

### 3. Full Market Snapshot

#### Test Prompt 3: Full Market Snapshot

"Quick Response Needed with minimal tool calls: Based on Market Status Date, Full Market Snapshot: SPY, QQQ, IWM"

### 4. Closing Price Query

#### Test Prompt 4: Closing Price Query

"Quick Response Needed with minimal tool calls: Based on Market Status Date, what was the closing price of GME today?"

### 5. Performance Analysis

#### Test Prompt 5: Performance Analysis

"Quick Response Needed with minimal tool calls: Based on Market Status Date, how is SOUN performance doing this week?"

### 6. Top Gainers

#### Test Prompt 6: Top Gainers

"Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Gainers"

### 7. Top Losers

#### Test Prompt 7: Top Losers

"Quick Response Needed with minimal tool calls: Based on Market Status Date, Top Market Movers Today for Losers"

### 8. Support & Resistance

#### Test Prompt 8: Support & Resistance

"Quick Response Needed with minimal tool calls: Based on Market Status Date, Support & Resistance Levels NVDA"

### 9. Technical Analysis

#### Test Prompt 9: Technical Analysis

"Quick Response Needed with minimal tool calls: Based on Market Status Date, Technical Analysis SPY"

---

## Usage Guidelines

### For AI Agents

1. **Read this file first** before any testing
2. **Select appropriate prompt** based on test requirements
3. **Copy prompt exactly** as written
4. **Expect 30-60 second response time**
5. **Report actual response time** for performance classification

### For Test Documentation

1. **Reference this file** in all test guides
2. **Include individual prompts** for quick reference
3. **Link to this file** for comprehensive prompt list
4. **Update this file** if prompts need modification

### Performance Classification

- **SUCCESS:** < 45 seconds (excellent performance)
- **SLOW_PERFORMANCE:** 45-120 seconds (acceptable for AI responses)
- **TIMEOUT:** > 120 seconds (failure - investigate)

---

## Integration Notes

This file is referenced by:

- `CLAUDE.md` - Main project guidance
- `AGENTS.md` - Agent instructions
- `README.md` - Project documentation
- `tests/playwright/mcp_test_script_basic.md` - MCP testing guide
- `tests/playwright/complete_test_execution_guide.md` - Complete test
  guide
- `tests/playwright/UI_complete_test_execution_guide.md` - UI test guide
- All other test documentation files

**Last Updated:** 2025-01-09
**Version:** 1.0
**Status:** Production Ready
