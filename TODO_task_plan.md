# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

## 📋 COMPREHENSIVE CACHING REMOVAL IMPLEMENTATION PLAN

Based on comprehensive codebase audit, this plan removes ALL caching features from the Market Parser application to eliminate over-engineering and prepare for future OpenAI native prompt caching implementation.

## 🔍 AUDIT FINDINGS SUMMARY

### **Agent Creation Cache (ACTIVELY USED)**

- **Location**: `src/backend/main.py` lines 221-301
- **Class**: `AgentCache` with TTL-based caching
- **Global Instances**: `gui_agent_cache`, `cli_agent_cache`
- **Configuration**: `enable_agent_caching`, `agent_cache_ttl`, `max_cache_size`
- **Usage**: Both GUI and CLI paths actively use agent caching
- **Methods**: `get_cached_agent()`, `cache_agent()`, `clear_cache()`, `get_cache_stats()`

### **TTL Response Cache (DEFINED BUT NOT USED)**

- **Location**: `src/backend/main.py` lines 313-533
- **Implementation**: `TTLCache` from cachetools library
- **Global Instance**: `response_cache`
- **Constants**: `CACHE_TTL_SECONDS = 900`, `CACHE_MAX_SIZE = 1000`
- **Functions**: `generate_cache_key()`, `get_cached_response()`, `cache_response()`, `invalidate_cache_by_ticker()`, `clear_all_cache()`
- **API Endpoints**: Cache management endpoints (lines 958-1006)
- **Status**: **FUNCTIONS DEFINED BUT NOT ACTUALLY USED IN APPLICATION LOGIC**

### **Dependencies**

- **Library**: `cachetools>=6.2.0` in `pyproject.toml`
- **Import**: `from cachetools import TTLCache` in main.py

### **Configuration**

- **File**: `config/app.config.json` lines 32-34
- **Settings**: `enableAgentCaching`, `agentCacheTTL`, `maxCacheSize`

---

## 🎯 IMPLEMENTATION TASKS

### **PHASE 1: AGENT CACHE REMOVAL**

#### **Task 1.1: Remove AgentCache Class and Related Code**

- [ ] **Remove AgentCache class** (lines 221-295)
  - Remove `__init__()` method
  - Remove `_generate_cache_key()` method
  - Remove `get_cached_agent()` method
  - Remove `cache_agent()` method
  - Remove `_cleanup_cache()` method
  - Remove `get_cache_stats()` method
  - Remove `clear_cache()` method

#### **Task 1.2: Remove Global Agent Cache Variables**

- [ ] **Remove global cache instances** (lines 300-301)
  - Remove `gui_agent_cache = None`
  - Remove `cli_agent_cache = None`

#### **Task 1.3: Update create_agent() Function**

- [ ] **Simplify create_agent() function** (lines 406-446)
  - Remove `agent_cache=None` parameter
  - Remove agent caching logic (lines 418-425, 437-444)
  - Remove conditional caching checks
  - Always create new agent instances

#### **Task 1.4: Update GUI Agent Usage**

- [ ] **Update GUI agent creation** (line 757)
  - Change `create_agent(shared_mcp_server, gui_agent_cache)` to `create_agent(shared_mcp_server)`

#### **Task 1.5: Update CLI Agent Usage**

- [ ] **Update CLI agent creation** (line 1048)
  - Change `create_agent(server, cli_agent_cache)` to `create_agent(server)`

#### **Task 1.6: Remove Agent Cache Initialization**

- [ ] **Remove GUI cache initialization** (lines 633-637)
  - Remove agent cache initialization in lifespan function
  - Remove `gui_agent_cache` global variable usage

- [ ] **Remove CLI cache initialization** (lines 1018-1024)
  - Remove CLI agent cache initialization
  - Remove cache initialization print statement

#### **Task 1.7: Remove Agent Cache Cleanup**

- [ ] **Remove CLI cache cleanup** (lines 1117-1123)
  - Remove cache statistics printing
  - Remove cache cleanup logic

### **PHASE 2: RESPONSE CACHE REMOVAL**

#### **Task 2.1: Remove Response Cache Infrastructure**

- [ ] **Remove cache imports** (line 25)
  - Remove `from cachetools import TTLCache`

- [ ] **Remove cache constants** (lines 314-315)
  - Remove `CACHE_TTL_SECONDS = 900`
  - Remove `CACHE_MAX_SIZE = 1000`

- [ ] **Remove cache instances** (line 316)
  - Remove `response_cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)`

- [ ] **Remove cache statistics** (line 319)
  - Remove `cache_stats = {"hits": 0, "misses": 0, "evictions": 0, "current_size": 0}`

#### **Task 2.2: Remove Response Cache Functions**

- [ ] **Remove generate_cache_key()** (lines 449-454)
- [ ] **Remove get_cached_response()** (lines 457-472)
- [ ] **Remove cache_response()** (lines 475-497)
- [ ] **Remove invalidate_cache_by_ticker()** (lines 500-518)
- [ ] **Remove clear_all_cache()** (lines 524-534)

#### **Task 2.3: Remove Cache Management API Endpoints**

- [ ] **Remove cache metrics endpoint** (lines 958-970)
  - Remove `@app.get("/api/v1/cache/metrics")`
  - Remove `get_cache_metrics()` function

- [ ] **Remove ticker cache invalidation endpoint** (lines 973-988)
  - Remove `@app.delete("/api/v1/cache/ticker/{ticker}")`
  - Remove `invalidate_ticker_cache()` function

- [ ] **Remove clear all cache endpoint** (lines 991-1005)
  - Remove `@app.delete("/api/v1/cache/all")`
  - Remove `clear_all_cache_endpoint()` function

### **PHASE 3: CONFIGURATION CLEANUP**

#### **Task 3.1: Remove Caching Configuration from Settings Class**

- [ ] **Remove caching settings** (lines 92-94)
  - Remove `enable_agent_caching: bool = True`
  - Remove `agent_cache_ttl: int = 300`
  - Remove `max_cache_size: int = 50`

#### **Task 3.2: Remove Configuration Loading**

- [ ] **Remove config loading** (lines 160-162)
  - Remove `self.enable_agent_caching = agent_config["enableAgentCaching"]`
  - Remove `self.agent_cache_ttl = agent_config["agentCacheTTL"]`
  - Remove `self.max_cache_size = agent_config["maxCacheSize"]`

#### **Task 3.3: Update Configuration File**

- [ ] **Remove caching config from app.config.json**
  - Remove `"enableAgentCaching": true`
  - Remove `"agentCacheTTL": 300`
  - Remove `"maxCacheSize": 50`

### **PHASE 4: DEPENDENCY CLEANUP**

#### **Task 4.1: Remove cachetools Dependency**

- [ ] **Update pyproject.toml**
  - Remove `"cachetools>=6.2.0"` from dependencies

#### **Task 4.2: Update Documentation**

- [ ] **Remove caching references from documentation**
  - Update any documentation that mentions caching features
  - Remove cache-related comments and docstrings

### **PHASE 5: TESTING AND VALIDATION**

#### **Task 5.1: Code Quality Checks**

- [ ] **Run linting**
  - Execute `npm run lint` for frontend
  - Execute `uv run pylint src/backend/main.py` for backend
  - Fix any linting issues

#### **Task 5.2: CLI Testing**

- [ ] **Test CLI functionality**
  - Run `test_7_prompts_comprehensive.sh`
  - Verify CLI works without caching
  - Test agent creation and execution

#### **Task 5.3: GUI Testing**

- [ ] **Test GUI functionality**
  - Use Playwright tools to test GUI
  - Execute tests from `tests/playwright/test_prompts.md`
  - Verify GUI works without caching

#### **Task 5.4: Integration Testing**

- [ ] **Test both interfaces**
  - Verify no caching-related errors
  - Test agent creation performance
  - Verify all endpoints work correctly

### **PHASE 6: DOCUMENTATION AND MEMORY UPDATES**

#### **Task 6.1: Update Project Memories**

- [ ] **Update Serena memories**
  - Create new memory about caching removal
  - Update existing memories that reference caching
  - Document the removal process and rationale

#### **Task 6.2: Update Project Documentation**

- [ ] **Update CLAUDE.md**
  - Remove references to caching features
  - Update architecture description
  - Update performance metrics

#### **Task 6.3: Create Removal Summary**

- [ ] **Document removal process**
  - Create summary of what was removed
  - Document rationale for removal
  - Note future OpenAI native caching plans

---

## 🚨 CRITICAL IMPLEMENTATION NOTES

### **Agent Cache Removal Priority**

- **HIGH PRIORITY**: Agent caching is actively used and must be removed carefully
- **Impact**: Will affect both GUI and CLI performance (agents will be created fresh each time)
- **Testing**: Must thoroughly test agent creation and execution after removal

### **Response Cache Removal**

- **LOW RISK**: Response caching functions are defined but not actually used
- **Impact**: Minimal - no functional impact on application
- **Cleanup**: Can be removed safely without affecting functionality

### **Configuration Changes**

- **Breaking Change**: Removing caching configuration will require config file updates
- **Backward Compatibility**: Not maintained - caching features completely removed

### **Performance Impact**

- **Agent Creation**: Will be slower as agents created fresh each time
- **Memory Usage**: Will be lower without cache storage
- **Response Time**: May be slightly slower without response caching (if it was used)

---

## ✅ SUCCESS CRITERIA

1. **All caching code removed** from `src/backend/main.py`
2. **No caching dependencies** in `pyproject.toml`
3. **No caching configuration** in `config/app.config.json`
4. **All tests pass** (CLI and GUI)
5. **No linting errors** after removal
6. **Application functions correctly** without caching
7. **Documentation updated** to reflect changes
8. **Project memories updated** with removal details

---

## 🔄 TOOL USAGE REQUIREMENTS

**MANDATORY**: Use ALL available tools throughout implementation:

- **Serena Tools**: For code analysis, symbol manipulation, pattern search
- **Filesystem Tools**: For batch file operations and project management
- **Standard Read/Write/Edit**: For single-file modifications
- **Sequential-Thinking**: For complex problem analysis and planning
- **Context7**: For research and best practices
- **Playwright**: For GUI testing and validation

**CONTINUOUS USAGE**: Never stop using tools - continue throughout entire process until all tasks are completed.

---

## 📝 IMPLEMENTATION ORDER

1. **Phase 1**: Agent Cache Removal (HIGH PRIORITY)
2. **Phase 2**: Response Cache Removal (LOW RISK)
3. **Phase 3**: Configuration Cleanup
4. **Phase 4**: Dependency Cleanup
5. **Phase 5**: Testing and Validation
6. **Phase 6**: Documentation and Memory Updates

**Total Estimated Tasks**: 25+ individual tasks across 6 phases
**Estimated Time**: 2-3 hours for complete implementation
**Risk Level**: Medium (due to agent cache active usage)
