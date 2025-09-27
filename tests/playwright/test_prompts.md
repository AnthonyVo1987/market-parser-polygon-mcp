# Standardized Test Prompts

**Document Purpose:** This is the single source of truth for all
standardized test prompts used in Market Parser testing. All AI agents
and testing procedures MUST use these exact prompts to ensure
consistent, quick responses and avoid false failures.

**Target Audience:** AI Coding Agents, Test Specialists, and anyone
performing Market Parser testing
**Expected Outcome:** Consistent 20-45 second response times with minimal
tool calls (improved from 30-60 seconds with GPT-5 optimization)
**Methodology:** Quick response prompts designed to leverage GPT-5 model
efficiency and quick response optimization system

---

## CRITICAL TESTING RULES

**MANDATORY REQUIREMENTS:**

- ✅ Use ONLY these prompts for testing
- ✅ Copy prompts EXACTLY as written
- ✅ Expected response time: 20-45 seconds (improved with GPT-5 optimization)
- ✅ All prompts now include "Quick Response Needed with minimal tool calls" prefix
- ❌ DO NOT create custom prompts
- ❌ DO NOT modify these prompts
- ❌ DO NOT use complex, open-ended queries

---

## Quick Response Test Prompts

### 1. Market Status Query

#### Test Prompt 1: Market Status Query

"Current Market Status"

### 2. Single Stock Snapshot

#### Test Prompt 2: Single Stock Snapshot

"Single Stock Snapshot NVDA"

### 3. Full Market Snapshot

#### Test Prompt 3: Full Market Snapshot

"Full Market Snapshot: SPY, QQQ, IWM"

### 4. Closing Price Query

#### Test Prompt 4: Closing Price Query

"GME closing price today"

### 5. Performance Analysis

#### Test Prompt 5: Performance Analysis

"SOUN performance this week"

### 6. Support & Resistance

#### Test Prompt 6: Support & Resistance

"NVDA Support & Resistance Levels"

### 7. Technical Analysis

#### Test Prompt 7: Technical Analysis

"SPY Technical Analysis"

---

## Usage Guidelines

### For AI Agents

1. **Read this file first** before any testing
2. **Select appropriate prompt** based on test requirements
3. **Copy prompt exactly** as written (includes "Quick Response Needed" prefix)
4. **Expect 20-45 second response time** (improved with GPT-5 optimization)
5. **Report actual response time** for performance classification
6. **Verify quick response optimization** is working correctly

### For Test Documentation

1. **Reference this file** in all test guides
2. **Include individual prompts** for quick reference
3. **Link to this file** for comprehensive prompt list
4. **Update this file** if prompts need modification

### Performance Classification

- **SUCCESS:** < 30 seconds (excellent performance with GPT-5 optimization)
- **GOOD:** 30-45 seconds (good performance, within expected range)
- **SLOW_PERFORMANCE:** 45-90 seconds (acceptable but investigate optimization)
- **TIMEOUT:** > 90 seconds (failure - investigate GPT-5 configuration)

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
**Version:** 2.0
**Status:** Production Ready with GPT-5 Optimization
