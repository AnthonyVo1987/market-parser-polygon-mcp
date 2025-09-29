# 🔴 CRITICAL: MANDATORY TOOL USAGE Implementation Plan - Token Counting with Official OpenAI Agents SDK

## **PHASE 1: REMOVE OLD TOKEN COUNTING IMPLEMENTATION** 🔴 CRITICAL: DO FIRST

### **Task 1.1: Remove CLI Token Extraction Logic**

- **File**: `src/backend/cli.py`
- **Actions**:
  - Remove `_extract_token_count()` function (lines 119-129)
  - Remove token extraction call (line 88)
  - Remove `token_count=token_count` from ResponseMetadata (line 96)
  - Replace with comment: "Token counting handled by official OpenAI Agents SDK"

### **Task 1.2: Remove API Token Extraction Logic**

- **File**: `src/backend/routers/chat.py`
- **Actions**:
  - Remove token extraction logic (lines 95-107)
  - Remove `tokenCount=token_count` from ResponseMetadata (line 118)
  - Replace with comment: "Token counting handled by official OpenAI Agents SDK"

### **Task 1.3: Update Footer Display Logic**

- **File**: `src/backend/utils/response_utils.py`
- **Actions**:
  - Remove custom token extraction logic (lines 36-61)
  - Replace with official SDK method using `result.context_wrapper.usage`
  - Maintain existing footer format with enhanced token display

### **Task 1.4: Clean Up API Models**

- **File**: `src/backend/api_models.py`
- **Actions**:
  - Keep `token_count` field in ResponseMetadata (needed for API responses)
  - Remove any unused token-related fields if any

## **PHASE 2: IMPLEMENT OFFICIAL OPENAI AGENTS SDK TOKEN COUNTING**

### **Task 2.1: Enable Usage Tracking in ModelSettings**

- **File**: `src/backend/services/agent_service.py`
- **Actions**:
  - Add `include_usage=True` to `get_optimized_model_settings()` function
  - Update function docstring to mention token usage tracking

### **Task 2.2: Update CLI Token Access**

- **File**: `src/backend/cli.py`
- **Actions**:
  - Add function to extract token data from `result.context_wrapper.usage`
  - Update ResponseMetadata creation to include token data
  - Add error handling for missing usage data

### **Task 2.3: Update API Token Access**

- **File**: `src/backend/routers/chat.py`
- **Actions**:
  - Add function to extract token data from `result.context_wrapper.usage`
  - Update ResponseMetadata creation to include token data
  - Add error handling for missing usage data

### **Task 2.4: Update Footer Display with Official SDK Method**

- **File**: `src/backend/utils/response_utils.py`
- **Actions**:
  - Replace custom token extraction with `result.context_wrapper.usage`
  - Update token display format to show: `total_tokens (input_tokens, output_tokens)`
  - Add error handling for missing usage data
  - Maintain existing emoji and formatting

## **PHASE 3: TESTING AND VALIDATION**

### **Task 3.1: CLI Testing**

- **Command**: `./test_7_prompts_comprehensive.sh`
- **Validation**:
  - All 7 tests must pass
  - Verify token counts appear in footer
  - Check for 7 different response times
  - Detect and re-run any false failures

### **Task 3.2: API Testing**

- **Validation**:
  - Test API endpoints return token data in metadata
  - Verify footer display works in both CLI and API responses
  - Check error handling for missing usage data

## **PHASE 4: DOCUMENTATION AND CLEANUP**

### **Task 4.1: Update Code Comments**

- **Files**: All modified files
- **Actions**:
  - Add comments explaining official SDK usage
  - Remove outdated comments about performance issues
  - Document new token counting approach

### **Task 4.2: Update Serena Memories**

- **Actions**:
  - Create memory for official token counting implementation
  - Update project status with new architecture
  - Document performance improvements

## **IMPLEMENTATION DETAILS**

### **Token Data Access Pattern**

```python
# Official SDK method
if hasattr(result, 'context_wrapper') and result.context_wrapper:
    usage = result.context_wrapper.usage
    total_tokens = usage.total_tokens
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    requests = usage.requests
```

### **Footer Display Format**

```
📊 Performance Metrics:
   ⏱️  Response Time: {processing_time:.3f}s
   🤖  Model: {model_name}
   🔢  Tokens Used: {total_tokens:,} (Input: {input_tokens:,}, Output: {output_tokens:,})
```

### **Error Handling**

- Graceful fallback if `context_wrapper` is missing
- Graceful fallback if `usage` data is unavailable
- Maintain existing footer structure even without token data

## **SUCCESS CRITERIA**

✅ **All old token counting code removed**
✅ **Official SDK method implemented**
✅ **Token counts appear in footer for both CLI and API**
✅ **All 7 CLI tests pass**
✅ **Performance impact minimal**
✅ **Error handling robust**
✅ **Code comments updated**
✅ **Serena memories updated**

## **FILES TO MODIFY**

1. `src/backend/services/agent_service.py` - Enable usage tracking
2. `src/backend/cli.py` - Remove old logic, add new method
3. `src/backend/routers/chat.py` - Remove old logic, add new method
4. `src/backend/utils/response_utils.py` - Update footer display
5. `src/backend/api_models.py` - Keep existing fields

## **TESTING COMMANDS**

```bash
# CLI Testing
./test_7_prompts_comprehensive.sh

# API Testing
curl -X POST http://127.0.0.1:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Tesla stock price"}'
```

## **PERFORMANCE EXPECTATIONS**

- **Minimal Impact**: Official SDK method is optimized
- **Real-time**: Token counts available immediately
- **Reliable**: More accurate than custom metadata approach
- **Maintainable**: Uses official SDK patterns

---

**🔴 CRITICAL: MANDATORY TOOL USAGE THROUGHOUT IMPLEMENTATION**

- Use all tools continuously during implementation
- Test after each major change
- Verify both CLI and API functionality
- Update documentation as you go
