# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process.

TOOL USAGE REQUIREMENTS:

- Use tools in ANY ORDER as needed for the specific task
- Use the SAME tool MULTIPLE TIMES if needed
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- Use tools for investigation, analysis, verification, and implementation at every step

MANDATORY TOOL USAGE PATTERNS:

1. START with Sequential-Thinking for task analysis, Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
2. Use Context7 for research and best up to date Implementation Practices & Library documentation lookups
3. Use Serena Tools for code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
4. Use Filesystem Tools for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
5. Use Standard Read/Write/Edit for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management
6. Use Playwright Tools for Testing with Browser automation for React GUI & App Validation
7. REPEAT any tool as needed throughout the process
8. 🔴 NEVER stop using tools - continue using them until task completion

TOOL OVERLAP RESOLUTION:

- Filesystem Tools: Use for 3+ file operations, batch processing, project management, metadata analysis, comprehensive project operations
- Standard Read/Write/Edit: Use for single-file modifications, simple edits, direct file operations
- Serena Tools: Use for complex code analysis, symbol manipulation, pattern search with context
- When in doubt: Use Filesystem for batch/complex operations, Standard for simple single-file operations

VIOLATION PENALTIES:

- If you use tools only once and stop, you're failing
- If you follow a rigid order instead of using tools as needed, you're failing
- If you don't use tools throughout the entire process, you're failing
- If you use wrong tool for the operation (e.g., Standard for batch operations), you're failing

SUCCESS CRITERIA:

- Tools used multiple times throughout the task
- Tools used in different orders based on need
- Continuous tool usage from start to finish
- Correct tool selection based on operation type
- No rigid sequencing - only logical tool usage based on task requirements

REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## New Task Details

---

# **🚀 AI Agent Implementation Prompt: Shared Persistent Agent Implementation Plan - Phases 1-4**

## **📋 MISSION BRIEF**

You are tasked with implementing **Phases 1-4** of the Shared Persistent Agent Implementation Plan for the Market Parser application. This is a **4-day implementation** that will optimize the application through **Session Persistence + Agent Caching + MCP Server Optimization + Error Handling** architecture, improving response times by **4-20 seconds per session** and implementing essential chatbot functionality.

## **🎯 CRITICAL SUCCESS FACTORS**

- **Performance Target:** 4-20s improvement per session (10-40% faster for multi-message sessions)
- **User Experience:** Implement essential conversation memory (CRITICAL for chatbot functionality)
- **Code Quality:** Improve architecture with session persistence and agent caching
- **Risk Management:** Implement comprehensive error handling and monitoring
- **Testing:** Ensure 100% functionality preservation

## **📖 IMPLEMENTATION PLAN REFERENCE**

**MANDATORY:** Read and understand the complete implementation plan at:
`docs/implementation_plans/shared_persistent_agent_implementation_plan.md`

**FOCUS ON PHASES 1-4 ONLY:**

- **Phase 1:** Session Persistence Implementation (Days 1-2)
- **Phase 2:** Agent Caching & Optimization (Days 2-3)
- **Phase 3:** MCP Server Optimization (Days 3-4)
- **Phase 4:** Error Handling & Recovery (Days 4-5)

## **🔧 TECHNICAL REQUIREMENTS**

### **Prerequisites:**

- OpenAI Agents SDK v0.2.9+
- SQLiteSession for conversation persistence
- Existing MCP server infrastructure
- Python 3.8+ with asyncio support
- FastAPI for GUI backend
- Rich console for CLI interface

### **Key Files to Modify:**

- `src/backend/main.py` (primary implementation file)
- `app.config.json` (configuration updates)

## **📅 IMPLEMENTATION PHASES (1-4 ONLY)**

### **Phase 1: Session Persistence Implementation (Days 1-2)**

#### **Task 1.1: Implement CLI Session Persistence**

- [ ] **1.1.1** Create persistent SQLiteSession for CLI ("cli_session")
- [ ] **1.1.2** Replace `session=None` with persistent session in CLI (line 1060)
- [ ] **1.1.3** Add CLI session cleanup on exit
- [ ] **1.1.4** Add CLI session persistence across restarts
- [ ] **1.1.5** Add CLI session size limits and cleanup

**Implementation Details:**

```python
# Current CLI (line 1060):
result = await Runner.run(analysis_agent, prompt_data["user_prompt"], session=None)

# New CLI:
cli_session = SQLiteSession("cli_session")
result = await Runner.run(analysis_agent, prompt_data["user_prompt"], session=cli_session)
```

#### **Task 1.2: Optimize GUI Session Management**

- [ ] **1.2.1** Keep existing `shared_session` for GUI (already optimized)
- [ ] **1.2.2** Integrate with existing `cleanup_session_periodically()`
- [ ] **1.2.3** Add session health monitoring
- [ ] **1.2.4** Add session error recovery
- [ ] **1.2.5** Add session performance monitoring

#### **Task 1.3: Session Configuration Management**

- [ ] **1.3.1** Update configuration for CLI session management
- [ ] **1.3.2** Add session timeout configuration
- [ ] **1.3.3** Add session cleanup interval configuration
- [ ] **1.3.4** Add session size limit configuration
- [ ] **1.3.5** Add session monitoring configuration

**Configuration Updates:**

```json
{
  "agent": {
    "sessionName": "finance_conversation",
    "cliSessionName": "cli_session",
    "sessionTimeoutMinutes": 60,
    "sessionCleanupIntervalMinutes": 30,
    "maxSessionSize": 100,
    "enableSessionPersistence": true,
    "enableAgentCaching": true,
    "agentCacheTTL": 300,
    "maxCacheSize": 50
  },
  "monitoring": {
    "enablePerformanceMonitoring": true,
    "enableErrorTracking": true,
    "enableResourceMonitoring": true,
    "logLevel": "INFO",
    "metricsRetentionDays": 30
  }
}
```

### **Phase 2: Agent Caching & Optimization (Days 2-3)**

#### **Task 2.1: Implement Agent Caching for GUI**

- [ ] **2.1.1** Create agent cache for GUI requests
- [ ] **2.1.2** Cache agents with same parameters (model, instructions, MCP server)
- [ ] **2.1.3** Add agent cache invalidation on configuration changes
- [ ] **2.1.4** Add agent cache cleanup and memory management
- [ ] **2.1.5** Add agent cache performance monitoring

#### **Task 2.2: Implement Agent Caching for CLI**

- [ ] **2.2.1** Create agent cache for CLI sessions
- [ ] **2.2.2** Cache agents with same parameters (model, instructions, MCP server)
- [ ] **2.2.3** Add agent cache invalidation on session changes
- [ ] **2.2.4** Add agent cache cleanup on CLI exit
- [ ] **2.2.5** Add agent cache performance monitoring

**Implementation Details:**

```python
class AgentCache:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_cached_agent(self, model, instructions, mcp_servers):
        cache_key = self._generate_cache_key(model, instructions, mcp_servers)
        if cache_key in self.cache:
            cached_agent, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_agent
        return None
    
    def cache_agent(self, model, instructions, mcp_servers, agent):
        cache_key = self._generate_cache_key(model, instructions, mcp_servers)
        self.cache[cache_key] = (agent, time.time())
```

#### **Task 2.3: Dynamic Instruction Updates**

- [ ] **2.3.1** Modify agent creation to use dynamic date/time context
- [ ] **2.3.2** Update instructions for each request to include current date/time
- [ ] **2.3.3** Add instruction caching with TTL (time-to-live)
- [ ] **2.3.4** Add instruction update monitoring
- [ ] **2.3.5** Add instruction performance optimization

### **Phase 3: MCP Server Optimization (Days 3-4)**

#### **Task 3.1: Optimize GUI MCP Server Usage**

- [ ] **3.1.1** Keep existing `shared_mcp_server` (already optimized)
- [ ] **3.1.2** Add MCP server health monitoring
- [ ] **3.1.3** Add MCP server error recovery
- [ ] **3.1.4** Add MCP server performance monitoring

#### **Task 3.2: Optimize CLI MCP Server Usage**

- [ ] **3.2.1** Create persistent MCP server for CLI sessions
- [ ] **3.2.2** Reuse MCP server across CLI messages
- [ ] **3.2.3** Add MCP server health monitoring for CLI
- [ ] **3.2.4** Add MCP server error recovery for CLI

**Implementation Details:**

```python
# Current CLI MCP server creation (per request):
server = create_polygon_mcp_server()

# New CLI MCP server (persistent):
cli_mcp_server = create_polygon_mcp_server()
# Reuse cli_mcp_server across all CLI messages in session
```

#### **Task 3.3: MCP Server Resource Management**

- [ ] **3.3.1** Add MCP server resource monitoring
- [ ] **3.3.2** Add MCP server memory management
- [ ] **3.3.3** Add MCP server connection pooling
- [ ] **3.3.4** Add MCP server performance optimization

### **Phase 4: Error Handling & Recovery (Days 4-5)**

#### **Task 4.1: Robust Error Handling**

- [ ] **4.1.1** Add agent creation failure detection and recovery
- [ ] **4.1.2** Add session corruption detection and recovery
- [ ] **4.1.3** Add MCP server failure handling
- [ ] **4.1.4** Add cache corruption detection and recovery

#### **Task 4.2: Monitoring & Alerting**

- [ ] **4.2.1** Add agent cache performance monitoring
- [ ] **4.2.2** Add session activity monitoring
- [ ] **4.2.3** Add MCP server health monitoring
- [ ] **4.2.4** Add memory usage monitoring

**Implementation Details:**

```python
class PerformanceMetrics:
    def __init__(self):
        self.agent_creation_time = 0.0
        self.session_access_time = 0.0
        self.mcp_server_response_time = 0.0
        self.cache_hit_rate = 0.0
        self.memory_usage = 0.0
        self.timestamp = time.time()

class PerformanceMonitor:
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
    
    def log_agent_creation_time(self, creation_time: float):
        """Log agent creation time for performance analysis."""
        self.metrics.append(PerformanceMetrics(
            agent_creation_time=creation_time,
            timestamp=time.time()
        ))
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.metrics:
            return {}
        
        recent_metrics = [m for m in self.metrics if time.time() - m.timestamp < 3600]  # Last hour
        
        return {
            "avg_agent_creation_time": sum(m.agent_creation_time for m in recent_metrics) / len(recent_metrics),
            "avg_session_access_time": sum(m.session_access_time for m in recent_metrics) / len(recent_metrics),
            "avg_mcp_server_response_time": sum(m.mcp_server_response_time for m in recent_metrics) / len(recent_metrics),
            "avg_cache_hit_rate": sum(m.cache_hit_rate for m in recent_metrics) / len(recent_metrics),
            "avg_memory_usage": sum(m.memory_usage for m in recent_metrics) / len(recent_metrics),
            "total_requests": len(recent_metrics)
        }
```

## **⚠️ CRITICAL IMPLEMENTATION RULES**

### **1. Phase-by-Phase Execution**

- **MANDATORY:** Complete each phase fully before proceeding to next
- **MANDATORY:** Run validation tests after each phase
- **MANDATORY:** Document any issues or deviations

### **2. Code Quality Standards**

- **MANDATORY:** Preserve all existing functionality
- **MANDATORY:** Follow exact code examples from the plan
- **MANDATORY:** Run linting and tests after each change
- **MANDATORY:** Maintain backward compatibility

### **3. Testing Requirements**

- **MANDATORY:** Test both CLI and GUI after each phase
- **MANDATORY:** Verify conversation memory works across messages
- **MANDATORY:** Measure performance improvements
- **MANDATORY:** Ensure no regression in existing functionality

### **4. Error Handling**

- **MANDATORY:** Implement comprehensive error handling
- **MANDATORY:** Add monitoring and alerting
- **MANDATORY:** Handle edge cases and failures gracefully

## **🎯 SUCCESS METRICS (Phases 1-4)**

### **Performance Targets:**

- **Response Time:** 4-20s improvement per session (10-40% faster)
- **Memory Usage:** <10% increase
- **Error Rate:** <1% increase
- **Cache Hit Rate:** >80%

### **Functionality Targets:**

- **Conversation Memory:** Agents remember previous queries across messages
- **Session Persistence:** Conversation history maintained across restarts
- **Contextual Responses:** Natural follow-up question handling
- **Code Quality:** Improved architecture with proper error handling

## **🚨 ROLLBACK PROCEDURES**

**MANDATORY:** Implement rollback capability for each phase:

- **Phase 1:** Revert session changes, restore `session=None`
- **Phase 2:** Disable agent caching, restore original agent creation
- **Phase 3:** Revert MCP server changes, restore original patterns
- **Phase 4:** Remove monitoring, restore original error handling

## **📝 DELIVERABLES**

### **Daily Deliverables:**

1. **Phase Completion Report** with detailed progress
2. **Testing Results** with performance measurements
3. **Code Changes** with explanations
4. **Issues/Deviations** documentation
5. **Next Phase Preparation** checklist

### **Final Deliverables (After Phase 4):**

1. **Complete Implementation** following all 4 phases
2. **Performance Validation** showing 4-20s improvement per session
3. **Functionality Validation** showing conversation memory works
4. **Error Handling** with comprehensive monitoring
5. **Documentation** reflecting all changes

## **🔍 VALIDATION CHECKLIST**

Before considering implementation complete:

- [ ] All 4 phases completed successfully
- [ ] Performance improvement of 4-20s per session achieved
- [ ] Conversation memory works across messages and restarts
- [ ] All existing functionality preserved
- [ ] Comprehensive error handling implemented
- [ ] Monitoring and alerting setup
- [ ] All tests passing

## **💡 IMPLEMENTATION TIPS**

1. **Start with Phase 1** - Session persistence provides immediate user value
2. **Follow Code Examples** - The plan contains exact code snippets to implement
3. **Test Frequently** - Run tests after each significant change
4. **Document Everything** - Keep detailed logs of all changes and decisions
5. **Monitor Performance** - Track improvements throughout implementation
6. **Plan for Rollback** - Always have a way to revert changes if needed

## **🎯 FINAL SUCCESS CRITERIA**

**Implementation is successful when:**

- ✅ All 4 phases completed per the detailed plan
- ✅ 4-20s performance improvement per session achieved
- ✅ Conversation memory works seamlessly
- ✅ All existing functionality preserved
- ✅ Comprehensive monitoring and error handling in place
- ✅ Ready for Phase 5 (Testing & Validation)

**Remember:** This is implementing **essential chatbot functionality** that users expect, not just a performance optimization. The 4-day investment is absolutely justified for the massive performance gains and critical user experience improvements.

---

**🚀 BEGIN IMPLEMENTATION: Start with Phase 1 and work through all 4 phases systematically. Good luck!**
