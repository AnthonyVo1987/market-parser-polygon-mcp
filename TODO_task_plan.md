# TODO Task Plan: Complete Removal of Legacy Polygon MCP Tools

**Task**: Completely remove and retire ALL Polygon MCP Tools and Polygon Server Creation endpoints since migration to direct Polygon Python API calls is complete and validated.

**Commit Reference**: fe380fa4a96369a6a518b70656bae0c4e0c8c9a3 (migration complete, all 16/16 tests passing)

**Expected Outcome**: Absolutely ZERO references to legacy Polygon MCP Server tools anywhere in code, comments, docs, memories, or project files.

---

## Research Summary: What Needs to be Removed

### 6 Legacy Polygon MCP Tools to Remove:
1. ✅ `get_snapshot_all` → REPLACED by `get_stock_quote_multi` (direct API)
2. ✅ `get_snapshot_option` → REPLACED by `get_options_quote_single` (direct API)
3. ✅ `list_aggs` → REPLACED by `get_OHLC_bars_custom_date_range` (direct API)
4. ✅ `get_daily_open_close_agg` → REPLACED by `get_OHLC_bars_specific_date` (direct API)
5. ✅ `get_previous_close_agg` → REPLACED by `get_OHLC_bars_previous_close` (direct API)
6. ✅ `get_aggs` → REMOVED (not relevant for analysis)

### Files Found with Legacy References:

**CODE FILES (8 files):**
1. `src/backend/cli.py` - Imports and uses `create_polygon_mcp_server()`
2. `src/backend/dependencies.py` - MCP server dependency injection
3. `src/backend/__init__.py` - Exports `create_polygon_mcp_server`
4. `src/backend/main.py` - Creates and manages MCP server lifecycle
5. `src/backend/routers/chat.py` - Uses MCP server for agent creation
6. `src/backend/services/agent_service.py` - References 18 tools (should be 12), mentions MCP tools
7. `src/backend/services/mcp_service.py` - Creates Polygon MCP server (ENTIRE FILE TO DELETE)
8. `src/backend/services/__init__.py` - Exports `create_polygon_mcp_server`

**DOCUMENTATION FILES (2 files):**
1. `CLAUDE.md` - References all 6 MCP tools, mentions "backward compatibility"
2. `TODO_task_plan.md` - Migration plan (will be replaced by this file)

**SERENA MEMORY FILES (5 files):**
1. `.serena/memories/project_architecture.md` - Lists MCP tools
2. `.serena/memories/performance_baseline_oct_2025.md` - References MCP tool usage
3. `.serena/memories/ai_agent_instructions_oct_2025.md` - Old tool selection rules
4. `.serena/memories/tech_stack.md` - Lists MCP tools as "backward compatibility"
5. `.serena/memories/finnhub_tool_swap_oct_2025.md` - Migration history

**TEST REPORTS (26 files):**
- `test-reports/*.txt` - Historical test outputs showing MCP tool usage (keep for history)

**TOOL CODE (2 files):**
- `src/backend/tools/polygon_tools.py` - Direct API implementations (keep, no MCP references in code)
- No MCP tool implementations exist (they were accessed via MCP server)

---

## PHASE 1: CODE CLEANUP - Remove MCP Server Infrastructure

### 1.1 Delete MCP Service File
- [ ] **DELETE ENTIRE FILE**: `src/backend/services/mcp_service.py`
  - Contains `create_polygon_mcp_server()` function
  - No longer needed since we use direct API

### 1.2 Update `src/backend/services/__init__.py`
- [ ] Remove import: `from .mcp_service import create_polygon_mcp_server`
- [ ] Remove from `__all__`: `"create_polygon_mcp_server"`
- [ ] Update to export only: `["create_agent", "get_enhanced_agent_instructions"]`

### 1.3 Update `src/backend/services/agent_service.py`
- [ ] **Remove MCP server parameter from `create_agent()` function**
  - Current: `def create_agent(mcp_server: MCPServerStdio):`
  - New: `def create_agent():`
- [ ] **Remove MCP import**: `from agents.mcp import MCPServerStdio`
- [ ] **Remove `mcp_servers` parameter from Agent initialization**
  - Current: `mcp_servers=[mcp_server],`
  - New: Remove this line entirely
- [ ] **Update AI agent instructions - CRITICAL TOOL COUNT UPDATE**
  - Current: `18 SUPPORTED TOOLS: [get_stock_quote, ..., get_snapshot_all, get_snapshot_option, list_aggs, get_daily_open_close_agg, get_previous_close_agg]`
  - **New: 12 SUPPORTED TOOLS: [get_stock_quote, get_market_status_and_date_time, get_stock_quote_multi, get_options_quote_single, get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close, get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd]**
- [ ] **Remove all 6 MCP tools from instructions:**
  - Remove `get_snapshot_all` references (RULE #2, examples, incorrect calls)
  - Remove `get_snapshot_option` references (RULE #3, examples, incorrect calls)
  - Remove `list_aggs` references (if any)
  - Remove `get_daily_open_close_agg` references (if any)
  - Remove `get_previous_close_agg` references (fallback sequences)
  - Remove `get_aggs` references (already marked as REMOVED)
- [ ] **Update RULE #2**: Remove fallback mention of `get_snapshot_all`
- [ ] **Update RULE #7**: Remove fallback mentions of MCP tools
- [ ] **Update examples section**: Remove all MCP tool examples
- [ ] **Verify final tool list**: 1 Finnhub + 11 Polygon Direct = 12 total

### 1.4 Update `src/backend/dependencies.py`
- [ ] **Remove MCP server dependency injection (ENTIRE FILE CLEANUP)**
  - Remove import: `from agents.mcp import MCPServerStdio`
  - Remove global: `_shared_mcp_server: Optional[MCPServerStdio] = None`
  - Remove function: `set_shared_resources(mcp_server: MCPServerStdio, session: SQLiteSession)`
  - Remove function: `get_mcp_server() -> Optional[MCPServerStdio]`
- [ ] **Keep only session-related code**
  - Keep: `_shared_session: Optional[SQLiteSession] = None`
  - Update: `set_shared_resources(session: SQLiteSession)` (remove mcp_server param)
  - Keep: `get_session() -> Optional[SQLiteSession]`

### 1.5 Update `src/backend/main.py`
- [ ] Remove import: `from .services import create_polygon_mcp_server`
- [ ] Remove global: `shared_mcp_server = None`
- [ ] Remove from lifespan startup:
  - Remove: `shared_mcp_server = create_polygon_mcp_server()`
  - Remove: `await shared_mcp_server.__aenter__()`
- [ ] Remove from lifespan shutdown:
  - Remove: `if shared_mcp_server: await shared_mcp_server.__aexit__(None, None, None)`
- [ ] Update `set_shared_resources()` call:
  - Current: `set_shared_resources(shared_mcp_server, shared_session)`
  - New: `set_shared_resources(shared_session)`

### 1.6 Update `src/backend/routers/chat.py`
- [ ] Remove import: `from ..dependencies import get_mcp_server, get_session`
  - New: `from ..dependencies import get_session`
- [ ] Remove import: `from ..services import create_agent, create_polygon_mcp_server`
  - New: `from ..services import create_agent`
- [ ] Remove MCP server retrieval:
  - Remove: `shared_mcp_server = get_mcp_server()`
- [ ] Remove MCP server health check and recovery:
  - Remove entire block: `if shared_mcp_server is None: ...`
- [ ] Update agent creation:
  - Current: `analysis_agent = create_agent(shared_mcp_server)`
  - New: `analysis_agent = create_agent()`

### 1.7 Update `src/backend/cli.py`
- [ ] Remove import: `from .services import create_agent, create_polygon_mcp_server`
  - New: `from .services import create_agent`
- [ ] Remove MCP server creation:
  - Remove: `server = create_polygon_mcp_server()`
- [ ] Remove MCP server initialization comments
- [ ] Update agent creation:
  - Find: `create_agent(server)` or similar
  - New: `create_agent()`

### 1.8 Update `src/backend/__init__.py`
- [ ] Remove from imports: `create_polygon_mcp_server,`
- [ ] Remove from `__all__`: `"create_polygon_mcp_server",`

---

## PHASE 2: DOCUMENTATION CLEANUP

### 2.1 Update `CLAUDE.md`
- [ ] **Remove Migration Section** (lines 20-62):
  - Remove all 5 tool migration bullet points
  - Remove "Remaining MCP Tools (6)" section
  - Remove "Migration rationale" section
- [ ] **Update "Last Completed Task Summary"**:
  - Add new task summary for MCP removal
  - Document final tool count: 12 tools (1 Finnhub + 11 Polygon Direct)
- [ ] **Search for any remaining references to:**
  - `get_snapshot_all`
  - `get_snapshot_option`
  - `list_aggs`
  - `get_daily_open_close_agg`
  - `get_previous_close_agg`
  - `get_aggs`
  - "MCP" in context of Polygon tools
  - "backward compatibility" related to Polygon

### 2.2 Verify No References in Other Docs
- [ ] Check `README.md` for any MCP tool mentions
- [ ] Check `new_research_details.md` (template file, should be clean)
- [ ] Check any other documentation files in root directory

---

## PHASE 3: SERENA MEMORY UPDATES

### 3.1 Update `.serena/memories/tech_stack.md`
- [ ] **Update Polygon.io Tools Section** (around line 292):
  - Remove: "MCP server (6 tools): get_snapshot_all, get_snapshot_option, list_aggs, get_daily_open_close_agg, get_previous_close_agg (backward compatibility)"
  - Update tool count: "Direct API (11 tools total)"
- [ ] **Update tool list** (lines 464-482):
  - Remove all 6 MCP tool entries
  - Keep only 11 direct API tools + 1 Finnhub tool
- [ ] **Remove any migration notes** about MCP tools

### 3.2 Update `.serena/memories/project_architecture.md`
- [ ] **Remove MCP Tools Section** (around line 171):
  - Remove: "Polygon.io MCP (get_snapshot_all, get_snapshot_option, get_aggs, etc.)"
- [ ] **Remove tool list** (lines 188-193):
  - Remove all MCP tool entries
- [ ] **Update "Financial Data Tools" section** (line 348):
  - Remove: "Tools: get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg"
  - Add: "Tools: 11 Polygon Direct API tools (see tech_stack.md for full list)"
- [ ] **Remove migration roadmap** (line 543):
  - Remove: "Phase 2: Migrate snapshot tools (get_snapshot_all, get_snapshot_option)"
  - Remove: "Phase 3: Migrate aggregate tools (get_aggs, list_aggs, etc.)"

### 3.3 Update `.serena/memories/ai_agent_instructions_oct_2025.md`
- [ ] **Remove outdated tool selection rules**:
  - Remove: "get_snapshot_all()" references (lines 9-11, 15, 22, 26, 29, 70, 103, 110)
  - Remove: "get_snapshot_option()" references (line 71)
  - Remove: "get_aggs()" references (line 47, 73)
  - Remove: "get_previous_close_agg()" fallback references (line 47)
- [ ] **Add note**: "DEPRECATED: This memory file contains outdated tool references. See agent_service.py for current tool list."
- [ ] **OR DELETE this memory file entirely** (it's now redundant with agent_service.py)

### 3.4 Update `.serena/memories/performance_baseline_oct_2025.md`
- [ ] **Remove expected tool references**:
  - Remove: "Expected Tool: get_snapshot_all(tickers=['SPY','QQQ','IWM'], market_type='stocks')" (line 58)
  - Remove: "Expected Tool: get_aggs() with weekly timespan" (line 70)
  - Remove: "Expected Tool: get_aggs() with weekly/daily aggregates" (line 76)
  - Remove: "Expected Tool: get_aggs() for trend analysis" (line 82)
- [ ] **Update performance metrics**:
  - Remove: "Multi-Ticker Test (Test 3): 100% correct use of get_snapshot_all()" (line 104)
  - Remove: "Aggregate Tests (Test 5, 6, 7): 100% correct use of get_aggs()" (line 105)
- [ ] **Remove tool confusion analysis**:
  - Remove: "Tool Selection Confusion: AI agent confused between get_snapshot_ticker() and get_snapshot_all()" (line 113)
  - Remove: "RULE #2: Multiple tickers = ALWAYS use get_snapshot_all()" (line 121)
- [ ] **Add note**: "Baseline metrics from Oct 2025 using legacy MCP tools. Current tools use direct Polygon API."

### 3.5 Update `.serena/memories/finnhub_tool_swap_oct_2025.md`
- [ ] **Remove MCP tool list** (lines 37, 46, 206-211):
  - Remove all references to: get_snapshot_all, get_snapshot_option, get_aggs, list_aggs, get_daily_open_close_agg, get_previous_close_agg
- [ ] **Add note**: "Historical reference - MCP tools fully replaced by direct API tools as of commit fe380fa"

### 3.6 Create New Memory: `polygon_mcp_removal_history.md`
- [ ] **Document the complete removal**:
  - Migration completed in commit fe380fa
  - All 6 MCP tools replaced with 5 direct API tools
  - MCP server infrastructure removed
  - Final tool count: 12 (1 Finnhub + 11 Polygon Direct)
  - Reason for removal: Direct API is faster, more reliable, no MCP server overhead

---

## PHASE 4: CLI TESTING - MANDATORY CHECKPOINT

### 4.1 Run Comprehensive Test Suite
- [ ] **Execute test script**:
  ```bash
  ./test_16_prompts_persistent_session.sh
  ```

### 4.2 Verify Test Results
- [ ] All 16/16 tests PASS (100% success rate)
- [ ] Test report generated in `test-reports/`
- [ ] No errors or failures in output
- [ ] Session persistence verified (single session)
- [ ] No MCP tool calls in test output
- [ ] All responses use direct API tools only

### 4.3 Expected Tool Usage in Tests
- [ ] **Test 1** (Market Status): `get_market_status_and_date_time()`
- [ ] **Test 2** (NVDA): `get_stock_quote(ticker='NVDA')`
- [ ] **Test 3** (SPY, QQQ, IWM): `get_stock_quote_multi(tickers=['SPY','QQQ','IWM'], market_type='stocks')`
- [ ] **Test 4** (SPY close): `get_stock_quote(ticker='SPY')` OR `get_OHLC_bars_previous_close()`
- [ ] **Test 5** (Weekly change): `get_OHLC_bars_custom_date_range()` for date range
- [ ] **Test 6** (Support/Resistance): `get_OHLC_bars_custom_date_range()` for historical analysis
- [ ] **Test 7** (Technical Analysis): Multiple tools (OHLC, TA indicators)
- [ ] **Test 8** (SMA): `get_ta_sma(ticker='SPY', ...)`
- [ ] **Test 9** (EMA): `get_ta_ema(ticker='NVDA', window=20, ...)`
- [ ] **Test 10** (RSI): `get_ta_rsi(ticker='SPY', ...)`
- [ ] **Test 11** (MACD): `get_ta_macd(ticker='AAPL', ...)`
- [ ] **Test 12** (Multi-ticker): `get_stock_quote_multi(tickers=['AAPL','MSFT','GOOGL'], market_type='stocks')`
- [ ] **Test 13** (Options): `get_options_quote_single(underlying_asset='SPY', option_contract='O:SPY251219C00650000')`
- [ ] **Test 14** (OHLC range): `get_OHLC_bars_custom_date_range(ticker='AAPL', from_date='2024-01-01', to_date='2024-03-31', ...)`
- [ ] **Test 15** (TSLA date): `get_OHLC_bars_specific_date(ticker='TSLA', date='2024-12-13', ...)`
- [ ] **Test 16** (Previous close): `get_OHLC_bars_previous_close(ticker='SPY', ...)`

### 4.4 Show Test Evidence to User
- [ ] Display test summary output (X/X PASS, response times)
- [ ] Provide test report file path
- [ ] Confirm no MCP tool usage detected
- [ ] Performance metrics (avg response time should be similar or faster without MCP overhead)

### 4.5 Test Failure Handling
- [ ] If any test fails: STOP and analyze failure
- [ ] Check if failure is due to missing MCP tools
- [ ] Verify all agent instructions correctly reference direct API tools
- [ ] Fix issues and re-test until 100% pass rate

---

## PHASE 5: FINAL VERIFICATION

### 5.1 Code Quality Checks
- [ ] **Run Pylint on modified files**:
  ```bash
  pylint src/backend/services/agent_service.py
  pylint src/backend/dependencies.py
  pylint src/backend/main.py
  pylint src/backend/routers/chat.py
  pylint src/backend/cli.py
  ```
- [ ] **Expected**: 10.00/10 score for all files
- [ ] **Fix any issues** if score drops

### 5.2 Search for Remaining References
- [ ] **Final pattern search for MCP tool names**:
  ```bash
  # Should return ZERO results in code/docs/memories (test-reports excluded)
  grep -r "get_snapshot_all" --exclude-dir=test-reports --exclude-dir=.git .
  grep -r "get_snapshot_option" --exclude-dir=test-reports --exclude-dir=.git .
  grep -r "list_aggs" --exclude-dir=test-reports --exclude-dir=.git .
  grep -r "get_daily_open_close_agg" --exclude-dir=test-reports --exclude-dir=.git .
  grep -r "get_previous_close_agg" --exclude-dir=test-reports --exclude-dir=.git .
  grep -r "get_aggs" --exclude-dir=test-reports --exclude-dir=.git .
  ```
- [ ] **Verify**: Only historical test reports contain references

### 5.3 Import Verification
- [ ] **Check Python imports** for MCP-related code:
  ```bash
  grep -r "from agents.mcp import MCPServerStdio" src/
  grep -r "create_polygon_mcp_server" src/
  ```
- [ ] **Expected**: ZERO results (all MCP imports removed)

### 5.4 Tool Count Verification
- [ ] **Verify agent instructions** show exactly 12 tools:
  ```bash
  grep "SUPPORTED TOOLS" src/backend/services/agent_service.py
  ```
- [ ] **Expected**: "12 SUPPORTED TOOLS: [get_stock_quote, get_market_status_and_date_time, get_stock_quote_multi, get_options_quote_single, get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close, get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd]"

---

## PHASE 6: DOCUMENTATION & COMMIT

### 6.1 Update CLAUDE.md Last Completed Task
- [ ] **Add new task summary**:
  ```markdown
  ## Last Completed Task Summary

  <!-- LAST_COMPLETED_TASK_START -->
  [CLEANUP] Complete removal of legacy Polygon MCP Tools and server infrastructure

  - Removed 6 legacy Polygon MCP tools (get_snapshot_all, get_snapshot_option, list_aggs, get_daily_open_close_agg, get_previous_close_agg, get_aggs)
  - Deleted MCP server infrastructure (mcp_service.py, dependency injection, lifecycle management)
  - Updated AI agent instructions to reference only 12 direct API tools (was 18)
  - Cleaned up all code, documentation, and Serena memories
  - Final tool count: 12 (1 Finnhub + 11 Polygon Direct API)
  - All 16/16 tests passing with direct API tools only
  - Pylint score: 10.00/10 for all modified files

  Migration Complete:
  ✅ Commit fe380fa: Migrated 6 MCP tools to 5 direct API tools
  ✅ This commit: Removed all legacy MCP infrastructure and references

  Tool Evolution:
  - **Before Migration:** 10 tools (7 Polygon MCP + 1 Finnhub + 2 Polygon Direct)
  - **After Migration:** 18 tools (6 Polygon MCP + 1 Finnhub + 11 Polygon Direct)
  - **After Cleanup:** 12 tools (0 Polygon MCP + 1 Finnhub + 11 Polygon Direct) ⭐ FINAL

  BREAKING CHANGE: Removed Polygon MCP server and all MCP-based tools. All financial queries now use direct Polygon Python API.
  <!-- LAST_COMPLETED_TASK_END -->
  ```

### 6.2 Create Git Commit
- [ ] **Stage all modified files**:
  ```bash
  git add -A
  ```
- [ ] **Verify changes**:
  ```bash
  git status
  git diff --cached
  ```
- [ ] **Create commit** with proper format:
  ```bash
  git commit -m "$(cat <<'EOF'
  [CLEANUP] Complete removal of legacy Polygon MCP Tools and server infrastructure

  - Deleted MCP server infrastructure (entire mcp_service.py file)
  - Removed MCP server dependency injection from dependencies.py
  - Removed MCP server lifecycle management from main.py
  - Removed MCP server usage from routers/chat.py and cli.py
  - Updated agent_service.py to use direct API tools only (12 tools, was 18)
  - Removed all 6 legacy MCP tool references from AI agent instructions:
    * get_snapshot_all → replaced by get_stock_quote_multi
    * get_snapshot_option → replaced by get_options_quote_single
    * list_aggs → replaced by get_OHLC_bars_custom_date_range
    * get_daily_open_close_agg → replaced by get_OHLC_bars_specific_date
    * get_previous_close_agg → replaced by get_OHLC_bars_previous_close
    * get_aggs → removed (not relevant)

  Documentation & Memory Updates:
  ✅ Updated CLAUDE.md: Removed migration section, updated tool counts
  ✅ Updated tech_stack.md: Removed MCP tools, updated to 11 direct API tools
  ✅ Updated project_architecture.md: Removed MCP references
  ✅ Updated ai_agent_instructions_oct_2025.md: Removed outdated tool rules
  ✅ Updated performance_baseline_oct_2025.md: Added historical note
  ✅ Updated finnhub_tool_swap_oct_2025.md: Marked as historical
  ✅ Created polygon_mcp_removal_history.md: Documented complete removal

  Testing & Quality Assurance:
  ✅ All 16/16 tests PASSING (100% success rate)
  ✅ Test report: test-reports/mcp_removal_test_TIMESTAMP.txt
  ✅ No MCP tool usage detected in test outputs
  ✅ Pylint score: 10.00/10 for all modified files
  ✅ Zero MCP references remaining in code/docs/memories

  Final Tool Count: 12 tools total
  - 1 Finnhub tool: get_stock_quote
  - 11 Polygon Direct API tools: get_market_status_and_date_time, get_stock_quote_multi, get_options_quote_single, get_OHLC_bars_custom_date_range, get_OHLC_bars_specific_date, get_OHLC_bars_previous_close, get_ta_sma, get_ta_ema, get_ta_rsi, get_ta_macd

  BREAKING CHANGE: Removed Polygon MCP server and all MCP-based tools. All financial queries now use direct Polygon Python API with no MCP overhead.

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>
  EOF
  )"
  ```

### 6.3 Push Changes
- [ ] **Push to remote**:
  ```bash
  git push
  ```
- [ ] **Verify push** was successful

---

## Success Criteria Checklist

**Code:**
- [✓] All MCP server code removed (mcp_service.py deleted)
- [✓] All MCP imports removed from codebase
- [✓] Agent created without MCP server parameter
- [✓] All 6 MCP tools removed from agent instructions
- [✓] Tool count updated to 12 (was 18)
- [✓] Pylint 10.00/10 on all modified files

**Documentation:**
- [✓] CLAUDE.md updated with removal task summary
- [✓] No MCP tool references in project docs
- [✓] Migration sections removed from CLAUDE.md

**Serena Memories:**
- [✓] tech_stack.md: MCP tools removed, tool count updated
- [✓] project_architecture.md: MCP references removed
- [✓] ai_agent_instructions_oct_2025.md: Outdated rules removed or file deleted
- [✓] performance_baseline_oct_2025.md: Historical note added
- [✓] finnhub_tool_swap_oct_2025.md: Historical note added
- [✓] New memory created: polygon_mcp_removal_history.md

**Testing:**
- [✓] All 16/16 tests passing (100% success rate)
- [✓] No MCP tool usage in test outputs
- [✓] Test report generated and path provided to user
- [✓] Performance metrics similar or better (no MCP overhead)

**Verification:**
- [✓] Zero grep results for MCP tool names (excluding test-reports)
- [✓] Zero grep results for MCP imports
- [✓] Agent instructions show exactly 12 tools
- [✓] All changes committed and pushed

---

## Timeline Estimate

- **PHASE 1** (Code Cleanup): 45 minutes
  - 8 files to modify
  - 1 file to delete
  - Import updates, function signature changes

- **PHASE 2** (Documentation): 20 minutes
  - 2 files to update
  - Remove migration sections

- **PHASE 3** (Serena Memories): 30 minutes
  - 5 files to update
  - 1 new memory file to create

- **PHASE 4** (CLI Testing): 15 minutes
  - Run test suite
  - Verify results
  - Show evidence to user

- **PHASE 5** (Verification): 15 minutes
  - Pylint checks
  - Pattern searches
  - Import verification

- **PHASE 6** (Documentation & Commit): 15 minutes
  - Update CLAUDE.md
  - Git commit and push

**Total Estimated Time: 2.5 hours**

---

## Risk Mitigation

**Risk 1: Tests fail due to missing MCP tools**
- Mitigation: Agent instructions correctly updated with direct API tools
- Fallback: Verify all 12 tools are imported and available in create_agent()

**Risk 2: Breaking change affects production**
- Mitigation: All tests passing before deployment
- Fallback: Keep this branch separate, test thoroughly before merging

**Risk 3: Performance degradation without MCP server**
- Mitigation: Direct API calls are actually faster (no MCP overhead)
- Validation: Compare response times in test reports

**Risk 4: Missed MCP references**
- Mitigation: Comprehensive grep searches in Phase 5
- Validation: Final verification ensures zero references

---

## Notes

- **Historical test reports** in `test-reports/` will be preserved as they document the migration journey
- **Tool count evolution** shows clear progression: 10 → 18 → 12
- **Direct API benefits**: Faster, more reliable, no MCP server overhead, simpler codebase
- **Breaking change** is acceptable as migration is complete and validated
