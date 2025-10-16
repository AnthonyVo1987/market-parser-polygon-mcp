# RULE #13: ERROR TRANSPARENCY - Verbatim Error Reporting

**Implemented**: 2025-10-15  
**Location**: agent_service.py (lines 462-489)  
**Status**: Active ✅

## Rule Statement

When tool calls fail, you MUST report the EXACT verbatim error message received. NEVER use vague phrases like "API Issue", "data unavailable", or "failed to retrieve" without specifics.

## Why This Rule Exists

Vague error messages waste debugging time:
- ❌ "There was an API issue" → What issue? Why? Where? No actionable info
- ❌ "Data unavailable" → Why unavailable? Market closed? Bad ticker? API down?
- ❌ "Failed to retrieve" → Failed how? Rate limited? Timeout? Invalid params?

Exact errors enable immediate root cause identification:
- ✅ "API error: Request timed out after 10s for NVDA" → Need to increase timeout or retry
- ✅ "Failed to retrieve: 'str' object has no attribute 'get'" → Code bug in response handling
- ✅ "No historical data available for INVALID from 2025-01-01 to 2025-01-31" → Invalid ticker or date range

## Implementation Details

### Where the Rule Applies
- After ANY tool call returns an error
- In agent responses to users
- When providing fallback error messages
- In response analysis sections

### What Constitutes "Verbatim"
Include the exact error message from the tool response:
- Full error text (not summarized)
- Error type/code if available
- Relevant parameters that caused the error
- Timestamp if time-sensitive

### Correct Error Reporting Patterns

**Pattern 1: Tool Returns Error JSON**
```
Tool returns: {"error": "Timeout", "message": "Request timed out after 10s", "ticker": "NVDA"}
✅ CORRECT: "API Timeout Error: Request timed out after 10s for NVDA"
❌ WRONG: "Unable to retrieve NVDA data"
```

**Pattern 2: Tool Returns Exception Message**
```
Tool returns: "Failed to retrieve: 'str' object has no attribute 'get'"
✅ CORRECT: "API error: str object has no attribute get - likely a response format issue"
❌ WRONG: "There was an API issue"
```

**Pattern 3: Tool Returns Specific Code Error**
```
Tool returns: "No historical data available for INVALID from 2025-01-01 to 2025-01-31"
✅ CORRECT: "No historical data available for INVALID from 2025-01-01 to 2025-01-31. Verify ticker symbol and date range."
❌ WRONG: "Data unavailable for the requested period"
```

## Integration with Error Detection

This rule works with the grep-based Phase 2 verification:
- Exact error messages are searchable with grep
- No vague messages hiding actual issues
- Phase 2a grep commands can find specific errors
- Enables rapid root cause analysis

## Historical Impact

**Before RULE #13:**
- Interval selection issue appeared to be a model problem
- Generic "data unavailable" responses masked the real issue
- Took multiple iterations to find the underlying code bug

**After RULE #13:**
- Exact error message: "'str' object has no attribute 'get'"
- Immediately pointed to code handling dict vs array
- Bug found and fixed in one iteration
- Enables faster debugging and issue resolution

## Success Metrics
- ✅ Zero vague error messages in 39/39 test responses
- ✅ All errors traceable to specific root causes
- ✅ Phase 2 grep commands find exact error text
- ✅ Debugging time reduced significantly

## Related Documentation
- Location: src/backend/services/agent_service.py (lines 462-489)
- Commit: e6cdda2 ([INTERVAL-FIX] Weekly/Monthly Interval Bug Fix + Error Transparency Rule)
- Test Report: test-reports/test_cli_regression_loop1_2025-10-15_17-38.log
