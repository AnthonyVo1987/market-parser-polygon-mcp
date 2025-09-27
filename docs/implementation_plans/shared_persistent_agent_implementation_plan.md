# Shared Persistent Agent Implementation Plan

## Executive Summary

This document outlines the implementation plan for optimizing the Market Parser application through **Session Persistence + Agent Caching** architecture. The plan addresses performance bottlenecks in agent creation while maintaining conversation memory and improving response times by 0.4-2.0 seconds per session.

## Current Architecture Analysis

### **Current Issues Identified:**
1. **Agent Recreation Overhead:** GUI creates new agent per request, CLI creates new agent per message
2. **Session Management:** CLI uses `session=None` (no persistence), GUI uses shared session
3. **Dead Code:** Unused global agents and optimized_agent_instructions.py
4. **Date/Time Context:** Agent instructions include stale date/time for persistent agents
5. **MCP Server Mismatch:** GUI and CLI use different MCP server patterns

### **Performance Impact:**
- **Current:** 5 agent creations per 5-message session
- **Target:** 0.4-2.0s improvement per session (1.3-3.2% faster)
- **Memory:** Conversation history across messages and restarts

## Implementation Strategy

### **Core Approach:**
- **Session Persistence:** Maintain conversation history across messages and restarts
- **Agent Caching:** Cache agents with same parameters to reduce creation overhead
- **Dynamic Instructions:** Update date/time context for each request
- **Separate Optimization:** Different approaches for CLI and GUI architectures
- **Dead Code Cleanup:** Remove all unused code and dependencies

### **Prerequisites & Dependencies:**
- OpenAI Agents SDK v0.2.9+
- SQLiteSession for conversation persistence
- Existing MCP server infrastructure
- Python 3.8+ with asyncio support
- FastAPI for GUI backend
- Rich console for CLI interface

### **Development Environment Setup:**
- Ensure all existing dependencies are installed
- Verify OpenAI API key configuration
- Confirm Polygon MCP server connectivity
- Set up development database for session testing
- Configure logging for performance monitoring

## Phase 0: Dead Code Cleanup (Day 1)

### **Task 0.1: Remove All Dead Code**
- [ ] **0.1.1** Remove `guardrail_agent` (lines 290-301) - never used
- [ ] **0.1.2** Remove `finance_analysis_agent` (lines 304-309) - never used  
- [ ] **0.1.3** Remove `finance_guardrail()` function (lines 312-319) - never used
- [ ] **0.1.4** Remove entire `optimized_agent_instructions.py` file - never used
- [ ] **0.1.5** Remove unused imports and dependencies
- [ ] **0.1.6** Verify no broken references after cleanup

**Validation:**
- Run linting to ensure no broken imports
- Run tests to verify functionality remains intact
- Check for any remaining references to removed code
- Verify no circular import dependencies
- Confirm all test cases pass
- Check for any runtime errors in both CLI and GUI
- Validate that removed code doesn't affect existing functionality

## Phase 1: Session Persistence Implementation (Days 1-2)

### **Task 1.1: Implement CLI Session Persistence**
- [ ] **1.1.1** Create persistent SQLiteSession for CLI ("cli_session")
- [ ] **1.1.2** Replace `session=None` with persistent session in CLI
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

### **Task 1.2: Optimize GUI Session Management**
- [ ] **1.2.1** Keep existing `shared_session` for GUI (already optimized)
- [ ] **1.2.2** Integrate with existing `cleanup_session_periodically()`
- [ ] **1.2.3** Add session health monitoring
- [ ] **1.2.4** Add session error recovery
- [ ] **1.2.5** Add session performance monitoring

**Implementation Details:**
```python
# Current GUI (line 740):
result = await Runner.run(analysis_agent, prompt_data["user_prompt"], session=shared_session)

# Enhanced GUI:
# Add monitoring and error recovery around existing shared_session usage
```

### **Task 1.3: Session Configuration Management**
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

## Phase 2: Agent Caching & Optimization (Days 2-3)

### **Task 2.1: Implement Agent Caching for GUI**
- [ ] **2.1.1** Create agent cache for GUI requests
- [ ] **2.1.2** Cache agents with same parameters (model, instructions, MCP server)
- [ ] **2.1.3** Add agent cache invalidation on configuration changes
- [ ] **2.1.4** Add agent cache cleanup and memory management
- [ ] **2.1.5** Add agent cache performance monitoring

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

### **Task 2.2: Implement Agent Caching for CLI**
- [ ] **2.2.1** Create agent cache for CLI sessions
- [ ] **2.2.2** Cache agents with same parameters (model, instructions, MCP server)
- [ ] **2.2.3** Add agent cache invalidation on session changes
- [ ] **2.2.4** Add agent cache cleanup on CLI exit
- [ ] **2.2.5** Add agent cache performance monitoring

### **Task 2.3: Dynamic Instruction Updates**
- [ ] **2.3.1** Modify agent creation to use dynamic date/time context
- [ ] **2.3.2** Update instructions for each request to include current date/time
- [ ] **2.3.3** Add instruction caching with TTL (time-to-live)
- [ ] **2.3.4** Add instruction update monitoring
- [ ] **2.3.5** Add instruction performance optimization

**Implementation Details:**
```python
def get_dynamic_agent_instructions():
    """Generate agent instructions with current date/time context."""
    datetime_context = get_current_datetime_context()
    return f"""Quick Response Needed with minimal tool calls: You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Polygon.io MCP server for live market data, prices, and financial information.

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Structure responses: DATA FIRST → DETAILED ANALYSIS
4. Include ticker symbols
5. Respond quickly with minimal tool calls
6. Keep responses concise - avoid unnecessary details

OUTPUT FORMAT:
A. DATA FIRST
- Format data in bullet point format with 2 decimal points max
- Provide cleaned up raw format data first, then verbal analysis
- Convert JSON response attributes to user-friendly terms
- Include relevant financial data and metrics

B. DETAILED ANALYSIS
- Provide Maximum of 3 KEY TAKEAWAYS/INSIGHTS in numbered/bullet point format
- No actionable recommendations
- Focus on the data only"""
```

## Phase 3: MCP Server Optimization (Days 3-4)

### **Task 3.1: Optimize GUI MCP Server Usage**
- [ ] **3.1.1** Keep existing `shared_mcp_server` (already optimized)
- [ ] **3.1.2** Add MCP server health monitoring
- [ ] **3.1.3** Add MCP server error recovery
- [ ] **3.1.4** Add MCP server performance monitoring
- [ ] **3.1.5** Add MCP server cleanup on shutdown

### **Task 3.2: Optimize CLI MCP Server Usage**
- [ ] **3.2.1** Create persistent MCP server for CLI sessions
- [ ] **3.2.2** Reuse MCP server across CLI messages
- [ ] **3.2.3** Add MCP server health monitoring for CLI
- [ ] **3.2.4** Add MCP server error recovery for CLI
- [ ] **3.2.5** Add MCP server cleanup on CLI exit

**Implementation Details:**
```python
# Current CLI (line 1023):
server = create_polygon_mcp_server()

# New CLI:
cli_mcp_server = create_polygon_mcp_server()
# Reuse cli_mcp_server across all CLI messages in the session
```

### **Task 3.3: MCP Server Resource Management**
- [ ] **3.3.1** Add MCP server resource monitoring
- [ ] **3.3.2** Add MCP server memory management
- [ ] **3.3.3** Add MCP server connection pooling
- [ ] **3.3.4** Add MCP server performance optimization
- [ ] **3.3.5** Add MCP server error handling and logging

## Phase 4: Error Handling & Recovery (Days 4-5)

### **Task 4.1: Robust Error Handling**
- [ ] **4.1.1** Add agent creation failure detection and recovery
- [ ] **4.1.2** Add session corruption detection and recovery
- [ ] **4.1.3** Add MCP server failure handling
- [ ] **4.1.4** Add cache corruption detection and recovery
- [ ] **4.1.5** Add comprehensive error logging

### **Task 4.2: Monitoring & Alerting**
- [ ] **4.2.1** Add agent cache performance monitoring
- [ ] **4.2.2** Add session activity monitoring
- [ ] **4.2.3** Add MCP server health monitoring
- [ ] **4.2.4** Add memory usage monitoring
- [ ] **4.2.5** Add error rate monitoring and alerting

**Monitoring Implementation:**
```python
import time
import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PerformanceMetrics:
    agent_creation_time: float
    session_activity_count: int
    mcp_server_health_score: float
    memory_usage_mb: float
    error_count: int
    timestamp: datetime

class PerformanceMonitor:
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.logger = logging.getLogger(__name__)
        self.max_metrics_history = 1000
    
    def log_agent_creation_time(self, duration: float):
        """Log agent creation time for performance analysis."""
        self.logger.info(f"Agent creation time: {duration:.3f}s")
        self._add_metric('agent_creation_time', duration)
    
    def log_session_activity(self, session_id: str, activity: str):
        """Log session activity for monitoring."""
        self.logger.debug(f"Session {session_id}: {activity}")
        self._add_metric('session_activity', {
            'session_id': session_id,
            'activity': activity,
            'timestamp': time.time()
        })
    
    def log_mcp_server_health(self, health_score: float):
        """Log MCP server health status."""
        self.logger.info(f"MCP server health: {health_score:.2f}")
        self._add_metric('mcp_server_health', health_score)
    
    def log_memory_usage(self, usage_mb: float):
        """Log memory usage in MB."""
        self.logger.info(f"Memory usage: {usage_mb:.2f} MB")
        self._add_metric('memory_usage', usage_mb)
    
    def log_error(self, error_type: str, error_message: str):
        """Log error occurrences."""
        self.logger.error(f"Error - {error_type}: {error_message}")
        self._add_metric('error', {
            'type': error_type,
            'message': error_message,
            'timestamp': time.time()
        })
    
    def _add_metric(self, metric_type: str, value: Any):
        """Add metric to history with size limit."""
        if len(self.metrics) >= self.max_metrics_history:
            self.metrics.pop(0)  # Remove oldest metric
        
        self.metrics.append(PerformanceMetrics(
            agent_creation_time=0.0,
            session_activity_count=0,
            mcp_server_health_score=1.0,
            memory_usage_mb=0.0,
            error_count=0,
            timestamp=datetime.now()
        ))
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.metrics:
            return {'status': 'no_data'}
        
        return {
            'total_metrics': len(self.metrics),
            'avg_agent_creation_time': self._calculate_average('agent_creation_time'),
            'total_sessions': len(set(m.session_id for m in self.metrics if hasattr(m, 'session_id'))),
            'avg_mcp_health': self._calculate_average('mcp_server_health'),
            'avg_memory_usage': self._calculate_average('memory_usage'),
            'total_errors': sum(1 for m in self.metrics if m.error_count > 0),
            'last_updated': self.metrics[-1].timestamp.isoformat() if self.metrics else None
        }
    
    def _calculate_average(self, metric_type: str) -> float:
        """Calculate average for specific metric type."""
        values = [getattr(m, metric_type, 0) for m in self.metrics if hasattr(m, metric_type)]
        return sum(values) / len(values) if values else 0.0
```

## Phase 5: Testing & Validation (Days 5-6)

### **Task 5.1: Functionality Testing**
- [ ] **5.1.1** Test CLI session persistence
- [ ] **5.1.2** Test GUI session management
- [ ] **5.1.3** Test agent caching functionality
- [ ] **5.1.4** Test conversation memory across messages
- [ ] **5.1.5** Test error recovery mechanisms

**Detailed Testing Strategy:**

1. **CLI Session Persistence Test:**
   - Start CLI session
   - Send multiple messages
   - Verify conversation history is maintained
   - Restart CLI and verify session persistence
   - Test session cleanup on exit
   - Verify session size limits

2. **GUI Session Management Test:**
   - Send multiple requests via GUI
   - Verify shared session works correctly
   - Test session cleanup and monitoring
   - Verify session health monitoring
   - Test session error recovery

3. **Agent Caching Test:**
   - Send multiple requests with same parameters
   - Verify agent is cached and reused
   - Test cache invalidation
   - Test cache TTL expiration
   - Verify cache memory management

4. **MCP Server Optimization Test:**
   - Test persistent MCP server for CLI
   - Verify MCP server health monitoring
   - Test MCP server error recovery
   - Verify MCP server cleanup

5. **Error Handling Test:**
   - Test agent creation failure recovery
   - Test session corruption recovery
   - Test MCP server failure handling
   - Test cache corruption recovery
   - Verify comprehensive error logging

### **Task 5.2: Performance Testing**
- [ ] **5.2.1** Measure response time improvements (target: 0.4-2.0s faster)
- [ ] **5.2.2** Test memory usage with caching
- [ ] **5.2.3** Test performance under load
- [ ] **5.2.4** Validate conversation memory functionality
- [ ] **5.2.5** Test resource cleanup and management

**Performance Test Script:**
```python
import time
import asyncio
import json
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class TestResult:
    prompt: str
    duration: float
    success: bool
    error_message: str = None
    memory_usage_mb: float = 0.0
    agent_cache_hit: bool = False

class PerformanceTestSuite:
    def __init__(self):
        self.test_prompts = [
            "Current Market Status",
            "Single Stock Snapshot NVDA",
            "Full Market Snapshot: SPY, QQQ, IWM",
            "GME closing price today",
            "SOUN performance this week",
            "NVDA Support & Resistance Levels",
            "SPY Technical Analysis"
        ]
        self.results: List[TestResult] = []
    
    async def run_performance_test(self) -> List[TestResult]:
        """Run comprehensive performance test suite."""
        print("🚀 Starting Performance Test Suite...")
        
        for i, prompt in enumerate(self.test_prompts, 1):
            print(f"📋 Running test {i}/{len(self.test_prompts)}: {prompt}")
            
            result = await self._test_single_prompt(prompt)
            self.results.append(result)
            
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"   {status} - Duration: {result.duration:.3f}s")
            
            if not result.success:
                print(f"   Error: {result.error_message}")
        
        return self.results
    
    async def _test_single_prompt(self, prompt: str) -> TestResult:
        """Test a single prompt and measure performance."""
        start_time = time.perf_counter()
        start_memory = self._get_memory_usage()
        
        try:
            # Execute prompt with new implementation
            # This would call the actual implementation
            response = await self._execute_prompt(prompt)
            
            end_time = time.perf_counter()
            end_memory = self._get_memory_usage()
            
            duration = end_time - start_time
            memory_usage = end_memory - start_memory
            
            return TestResult(
                prompt=prompt,
                duration=duration,
                success=True,
                memory_usage_mb=memory_usage,
                agent_cache_hit=self._check_cache_hit(prompt)
            )
            
        except Exception as e:
            end_time = time.perf_counter()
            duration = end_time - start_time
            
            return TestResult(
                prompt=prompt,
                duration=duration,
                success=False,
                error_message=str(e)
            )
    
    async def _execute_prompt(self, prompt: str) -> str:
        """Execute the prompt using the new implementation."""
        # This would be replaced with actual implementation call
        await asyncio.sleep(0.1)  # Simulate processing time
        return f"Response for: {prompt}"
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    
    def _check_cache_hit(self, prompt: str) -> bool:
        """Check if agent cache was hit for this prompt."""
        # This would check actual cache hit status
        return True  # Simulate cache hit
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        if not self.results:
            return {'error': 'No test results available'}
        
        successful_tests = [r for r in self.results if r.success]
        failed_tests = [r for r in self.results if not r.success]
        
        return {
            'summary': {
                'total_tests': len(self.results),
                'successful_tests': len(successful_tests),
                'failed_tests': len(failed_tests),
                'success_rate': len(successful_tests) / len(self.results) * 100
            },
            'performance': {
                'avg_duration': sum(r.duration for r in successful_tests) / len(successful_tests) if successful_tests else 0,
                'min_duration': min(r.duration for r in successful_tests) if successful_tests else 0,
                'max_duration': max(r.duration for r in successful_tests) if successful_tests else 0,
                'avg_memory_usage': sum(r.memory_usage_mb for r in successful_tests) / len(successful_tests) if successful_tests else 0
            },
            'cache_performance': {
                'cache_hit_rate': sum(1 for r in successful_tests if r.agent_cache_hit) / len(successful_tests) * 100 if successful_tests else 0
            },
            'errors': [
                {
                    'prompt': r.prompt,
                    'error': r.error_message
                } for r in failed_tests
            ]
        }

# Usage example:
async def main():
    test_suite = PerformanceTestSuite()
    results = await test_suite.run_performance_test()
    report = test_suite.generate_report()
    
    print("\n📊 Performance Test Report:")
    print(json.dumps(report, indent=2))
```

### **Task 5.3: Integration Testing**
- [ ] **5.3.1** Test dead code removal doesn't break functionality
- [ ] **5.3.2** Test session persistence integration
- [ ] **5.3.3** Test agent caching integration
- [ ] **5.3.4** Test MCP server optimization
- [ ] **5.3.5** Test monitoring and alerting

## Phase 6: Documentation & Deployment (Days 6-7)

### **Task 6.1: Update Documentation**
- [ ] **6.1.1** Document session persistence architecture
- [ ] **6.1.2** Document agent caching system
- [ ] **6.1.3** Document MCP server optimization
- [ ] **6.1.4** Document dead code cleanup
- [ ] **6.1.5** Document monitoring and maintenance procedures

### **Task 6.2: Configuration & Deployment**
- [ ] **6.2.1** Update configuration documentation
- [ ] **6.2.2** Add deployment instructions
- [ ] **6.2.3** Add monitoring setup instructions
- [ ] **6.2.4** Add backup and recovery procedures
- [ ] **6.2.5** Add performance tuning guidelines

## Expected Outcomes

### **Performance Improvements:**
- **CLI:** 0.4-2.0s faster per 5-message session
- **GUI:** 0.4-2.0s faster per 5-message session
- **Overall:** 1.3-3.2% response time improvement

### **User Experience Improvements:**
- **Conversation Memory:** Agents remember previous queries across messages
- **Contextual Responses:** Natural follow-up question handling
- **Faster Subsequent Requests:** Agent caching reduces creation overhead
- **Session Persistence:** Conversation history maintained across restarts

### **Code Quality Improvements:**
- **Dead Code Removal:** Cleaner, more maintainable codebase
- **Simplified Architecture:** Session persistence + agent caching approach
- **Better Resource Management:** Proper cleanup and monitoring
- **Enhanced Error Handling:** Robust failure detection and recovery

## Risk Assessment & Mitigation

### **High Risk:**
- **Agent Cache Corruption:** Implement cache validation and recovery
- **Session Data Loss:** Implement session backup and recovery
- **MCP Server Failures:** Implement health monitoring and failover

### **Medium Risk:**
- **Memory Leaks:** Implement memory monitoring and cleanup
- **Performance Degradation:** Implement performance monitoring and alerts
- **Configuration Errors:** Implement configuration validation

### **Low Risk:**
- **Dead Code Removal:** Thorough testing and validation
- **Documentation Updates:** Incremental updates with validation

## Rollback Strategy

### **Phase-by-Phase Rollback:**
1. **Phase 0 Rollback:** Restore removed dead code from git history
2. **Phase 1 Rollback:** Revert session changes, restore original session=None
3. **Phase 2 Rollback:** Disable agent caching, restore original agent creation
4. **Phase 3 Rollback:** Revert MCP server changes, restore original patterns
5. **Phase 4 Rollback:** Remove monitoring, restore original error handling
6. **Phase 5 Rollback:** Revert test changes, restore original test suite
7. **Phase 6 Rollback:** Revert documentation, restore original docs

### **Emergency Rollback:**
- Git reset to last known good commit
- Restore configuration files from backup
- Restart all services to clear caches
- Verify system functionality with original implementation
- Clear all session data and caches
- Restart MCP servers
- Verify API connectivity
- Run smoke tests to confirm system stability

### **Rollback Validation:**
- [ ] All services start successfully
- [ ] CLI functionality works as expected
- [ ] GUI functionality works as expected
- [ ] No error logs in system
- [ ] Performance metrics return to baseline
- [ ] All tests pass
- [ ] User acceptance testing confirms functionality

## Success Metrics

### **Performance Metrics:**
- Response time improvement: 0.4-2.0s per session
- Memory usage: <10% increase
- Error rate: <1% increase
- Cache hit rate: >80%

### **Quality Metrics:**
- Code coverage: >90%
- Test pass rate: 100%
- Documentation coverage: 100%
- Dead code removal: 100%

## Implementation Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| Phase 0 | Day 1 | Dead code cleanup, validation |
| Phase 1 | Days 1-2 | Session persistence implementation |
| Phase 2 | Days 2-3 | Agent caching and optimization |
| Phase 3 | Days 3-4 | MCP server optimization |
| Phase 4 | Days 4-5 | Error handling and monitoring |
| Phase 5 | Days 5-6 | Testing and validation |
| Phase 6 | Days 6-7 | Documentation and deployment |

## Implementation Checklist

### **Pre-Implementation:**
- [ ] Review and approve implementation plan
- [ ] Set up development environment
- [ ] Create feature branch for implementation
- [ ] Set up monitoring and logging infrastructure
- [ ] Create backup of current system
- [ ] Verify all dependencies are available
- [ ] Set up test environment
- [ ] Configure development tools

### **Post-Implementation:**
- [ ] Run full test suite
- [ ] Verify performance improvements
- [ ] Update documentation
- [ ] Deploy to staging environment
- [ ] Conduct user acceptance testing
- [ ] Deploy to production
- [ ] Monitor system performance
- [ ] Document lessons learned
- [ ] Update team on implementation results
- [ ] Schedule follow-up performance review

## Conclusion

This implementation plan provides a comprehensive approach to optimizing the Market Parser application through session persistence and agent caching. The plan addresses current performance bottlenecks while maintaining system reliability and improving user experience through conversation memory.

The phased approach ensures systematic implementation with proper testing and validation at each stage, minimizing risk while maximizing performance improvements.

**Key Success Factors:**
- Thorough testing at each phase
- Comprehensive error handling and recovery
- Detailed monitoring and alerting
- Clear rollback strategy
- Incremental implementation with validation
- Regular performance monitoring
- Continuous integration and deployment
- Team collaboration and communication
- Documentation maintenance
- User feedback integration