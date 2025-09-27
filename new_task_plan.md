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

# **🚀 AI Agent Implementation Prompt: Shared Persistent Agent Implementation Plan**

## **📋 MISSION BRIEF**

You are tasked with implementing the **Shared Persistent Agent Implementation Plan** for the Market Parser application. This is a **7-day, 6-phase implementation** that will optimize the application through **Session Persistence + Agent Caching** architecture, improving response times by **4-20 seconds per session** and implementing essential chatbot functionality.

## **🎯 CRITICAL SUCCESS FACTORS**

- **Performance Target:** 4-20s improvement per session (10-40% faster for multi-message sessions)
- **User Experience:** Implement essential conversation memory (CRITICAL for chatbot functionality)
- **Code Quality:** Remove dead code and improve architecture
- **Risk Management:** Implement comprehensive error handling and monitoring
- **Testing:** Ensure 100% functionality preservation

## **📖 IMPLEMENTATION PLAN REFERENCE**

**MANDATORY:** Read and understand the complete implementation plan at:
`docs/implementation_plans/shared_persistent_agent_implementation_plan.md`

This document contains:

- **6 Phases** with detailed task breakdowns
- **25+ Granular Tasks** with specific implementation details
- **Code Examples** and configuration updates
- **Testing Strategies** and validation procedures
- **Rollback Procedures** for each phase
- **Success Metrics** and performance targets

## **🔧 TECHNICAL REQUIREMENTS**

### **Prerequisites:**6

- OpenAI Agents SDK v0.2.9+
- SQLiteSession for conversation persistence
- Existing MCP server infrastructure
- Python 3.8+ with asyncio support
- FastAPI for GUI backend
- Rich console for CLI interface

### **Key Files to Modify:**

- `src/backend/main.py` (primary implementation file)
- `app.config.json` (configuration updates)
- `src/backend/optimized_agent_instructions.py` (remove - dead code)
- Test files and documentation

## **📅 IMPLEMENTATION PHASES**

### **Phase 0: Dead Code Cleanup (Day 1)**

- Remove `guardrail_agent` (lines 290-301)
- Remove `finance_analysis_agent` (lines 304-309)
- Remove `finance_guardrail()` function (lines 312-319)
- Remove entire `optimized_agent_instructions.py` file
- Remove unused imports and dependencies
- **Validation:** Run linting, tests, verify no broken references

### **Phase 1: Session Persistence Implementation (Days 1-2)**

- **CLI:** Create persistent SQLiteSession, replace `session=None`
- **GUI:** Optimize existing `shared_session` management
- **Configuration:** Update session management settings
- **Implementation:** Follow exact code examples in the plan

### **Phase 2: Agent Caching & Optimization (Days 2-3)**

- **GUI:** Implement agent cache with same parameters
- **CLI:** Implement agent cache for CLI sessions
- **Dynamic Instructions:** Update date/time context for each request
- **Performance:** Add caching with TTL and cleanup

### **Phase 3: MCP Server Optimization (Days 3-4)**

- **GUI:** Optimize existing `shared_mcp_server`
- **CLI:** Create persistent MCP server for CLI sessions
- **Resource Management:** Add monitoring and connection pooling

### **Phase 4: Error Handling & Recovery (Days 4-5)**

- **Robust Error Handling:** Agent creation, session corruption, MCP server failures
- **Monitoring & Alerting:** Performance monitoring, health checks, memory usage
- **Recovery Procedures:** Automatic recovery and fallback mechanisms

### **Phase 5: Testing & Validation (Days 5-6)**

- **Functionality Testing:** Session persistence, agent caching, conversation memory
- **Performance Testing:** Measure 4-20s improvement per session
- **Integration Testing:** End-to-end validation

### **Phase 6: Documentation & Deployment (Days 6-7)**

- **Documentation:** Update all relevant docs
- **Configuration:** Update deployment instructions
- **Monitoring:** Setup monitoring and alerting

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
- **MANDATORY:** Implement rollback procedures
- **MANDATORY:** Handle edge cases and failures gracefully

## **🎯 SUCCESS METRICS**

### **Performance Targets:**

- **Response Time:** 4-20s improvement per session (10-40% faster)
- **Memory Usage:** <10% increase
- **Error Rate:** <1% increase
- **Cache Hit Rate:** >80%

### **Functionality Targets:**

- **Conversation Memory:** Agents remember previous queries across messages
- **Session Persistence:** Conversation history maintained across restarts
- **Contextual Responses:** Natural follow-up question handling
- **Code Quality:** 100% dead code removal, cleaner architecture

## **🚨 ROLLBACK PROCEDURES**

**MANDATORY:** Implement rollback capability for each phase:

- **Phase 0:** Restore removed dead code from git history
- **Phase 1:** Revert session changes, restore `session=None`
- **Phase 2:** Disable agent caching, restore original agent creation
- **Phase 3:** Revert MCP server changes, restore original patterns
- **Phase 4:** Remove monitoring, restore original error handling
- **Phase 5:** Revert test changes, restore original test suite
- **Phase 6:** Revert documentation, restore original docs

## **📝 DELIVERABLES**

### **Daily Deliverables:**

1. **Phase Completion Report** with detailed progress
2. **Testing Results** with performance measurements
3. **Code Changes** with explanations
4. **Issues/Deviations** documentation
5. **Next Phase Preparation** checklist

### **Final Deliverables:**

1. **Complete Implementation** following all 6 phases
2. **Performance Validation** showing 4-20s improvement per session
3. **Functionality Validation** showing conversation memory works
4. **Updated Documentation** reflecting all changes
5. **Monitoring Setup** with alerts and dashboards

## **🔍 VALIDATION CHECKLIST**

Before considering implementation complete:

- [ ] All 6 phases completed successfully
- [ ] Performance improvement of 4-20s per session achieved
- [ ] Conversation memory works across messages and restarts
- [ ] All existing functionality preserved
- [ ] Dead code completely removed
- [ ] Comprehensive error handling implemented
- [ ] Monitoring and alerting setup
- [ ] Documentation updated
- [ ] Rollback procedures tested
- [ ] All tests passing

## **💡 IMPLEMENTATION TIPS**

1. **Start with Phase 0** - Dead code cleanup is low-risk and provides immediate value
2. **Follow Code Examples** - The plan contains exact code snippets to implement
3. **Test Frequently** - Run tests after each significant change
4. **Document Everything** - Keep detailed logs of all changes and decisions
5. **Monitor Performance** - Track improvements throughout implementation
6. **Plan for Rollback** - Always have a way to revert changes if needed

## **🎯 FINAL SUCCESS CRITERIA**

**Implementation is successful when:**

- ✅ All 6 phases completed per the detailed plan
- ✅ 4-20s performance improvement per session achieved
- ✅ Conversation memory works seamlessly
- ✅ All existing functionality preserved
- ✅ Comprehensive monitoring and error handling in place
- ✅ Documentation updated and deployment ready

**Remember:** This is implementing **essential chatbot functionality** that users expect, not just a performance optimization. The 7-day investment is absolutely justified for the massive performance gains and critical user experience improvements.

---

**🚀 BEGIN IMPLEMENTATION: Start with Phase 0 and work through all 6 phases systematically. Good luck!**
