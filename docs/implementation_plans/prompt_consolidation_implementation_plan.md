# Prompt Consolidation Implementation Plan

## Executive Summary

This document provides a comprehensive, granular implementation plan for consolidating the Market Parser application's prompt management system from multiple scattered files into a single, unified, manageable system. The consolidation will eliminate code duplication, reduce complexity, and create a single source of truth for all prompt-related functionality.

**Consolidation Scope:** Merge 2 active prompt systems into 1 unified system, remove dead code
**Estimated Effort:** 1-2 days for experienced developer
**Risk Level:** Low (minimal functional changes, backward compatibility maintained)
**Dependencies:** None (self-contained consolidation)

## Critical Findings from Comprehensive Review

### ❌ Major Issues Discovered in Original Plan

1. **INCORRECT ASSUMPTION**: Original plan assumed `optimized_agent_instructions.py` was actively used, but it's **COMPLETELY UNUSED DEAD CODE**
2. **MISSING DEPENDENCY**: Original plan missed that `AnalysisIntent` is imported in `api_models.py` and used in API responses
3. **OVER-ENGINEERING**: Original plan was unnecessarily complex for the actual consolidation needed
4. **INACCURATE SCOPE**: Original plan included migration of systems that don't exist in the active codebase

### ✅ Actual Current Architecture

**ACTIVE SYSTEMS (Only 2 need consolidation):**

1. **`get_enhanced_agent_instructions()`** in `main.py` (used 3 times)
2. **`DirectPromptManager`** in `direct_prompts.py` (used 6 times)

**DEAD CODE (Can be removed):**

1. **`optimized_agent_instructions.py`** - Completely unused
2. **`prompt_templates.py`** - Mostly disabled/removed code

**CRITICAL DEPENDENCIES:**

- `AnalysisIntent` enum used in `api_models.py` for API responses
- Import patterns use try/except for relative vs absolute imports

## Current System Analysis

### 1. Active Prompt Systems

#### System 1: Enhanced Agent Instructions (`main.py`)

**Location:** `src/backend/main.py` lines 252-275
**Usage Points:** 3 references in `main.py`
**Function:** `get_enhanced_agent_instructions()`
**Purpose:** Generates basic prompt for financial analysis agent

```python
def get_enhanced_agent_instructions():
    """Generate enhanced agent instructions with current date/time context and tool awareness."""
    datetime_context = get_current_datetime_context()
    return f"""Quick Response Needed with minimal tool calls: You are a financial analyst with real-time market data access.

{datetime_context}

TOOLS: Polygon.io MCP server for live market data, prices, and financial information.

INSTRUCTIONS:
1. Use current date/time above for all analysis
2. Gather real-time data using available tools
3. Provide data-driven insights with actionable recommendations
4. Structure responses: KEY TAKEAWAYS → DETAILED ANALYSIS
5. Include ticker symbols and specific metrics
6. Respond quickly with minimal tool calls
7. Keep responses concise and actionable - avoid unnecessary details

OUTPUT FORMAT:
KEY TAKEAWAYS:
• [Bullet point insights]

DETAILED ANALYSIS:
[Specific data, metrics, and actionable recommendations]"""
```

#### System 2: Direct Prompt Manager (`direct_prompts.py`)

**Location:** `src/backend/direct_prompts.py` lines 31-268
**Usage Points:** 6 references in `main.py`
**Class:** `DirectPromptManager`
**Purpose:** Manages direct prompt generation for different analysis types

**Key Methods:**

- `generate_direct_prompt()` - Generates prompts for AI model
- `extract_ticker_from_message()` - Extracts ticker symbols
- `detect_analysis_intent()` - Detects analysis intent
- `_build_system_prompts()` - Builds system prompts for different analysis types

**Analysis Intents:**

- `SNAPSHOT` - Market snapshots with real-time data
- `SUPPORT_RESISTANCE` - Technical analysis with support/resistance levels
- `TECHNICAL` - Comprehensive technical analysis
- `GENERAL` - General financial analysis

### 2. Dead Code Systems

#### Dead System 1: Optimized Agent Instructions (`optimized_agent_instructions.py`)

**Status:** COMPLETELY UNUSED
**Evidence:** No imports or references found in entire codebase
**Action:** Safe to delete

#### Dead System 2: Prompt Templates (`prompt_templates.py`)

**Status:** Mostly disabled/removed code
**Evidence:** Only referenced in comments, not actively used
**Action:** Safe to clean up remaining references

### 3. Critical Dependencies

#### API Model Dependencies

**File:** `src/backend/api_models.py`
**Dependency:** `AnalysisIntent` enum imported and used in:

- `template_type: AnalysisIntent = Field(alias="templateId")`
- `analysis_type: Optional[AnalysisIntent] = None`
- `supported_analysis_types: List[AnalysisIntent]`

**Import Pattern:**

```python
try:
    from .direct_prompts import AnalysisIntent
except ImportError:
    from direct_prompts import AnalysisIntent
```

#### Main Application Dependencies

**File:** `src/backend/main.py`
**Dependencies:**

- `DirectPromptManager` imported and used 6 times
- `get_enhanced_agent_instructions()` used 3 times

**Import Pattern:**

```python
try:
    from .direct_prompts import DirectPromptManager
except ImportError:
    from direct_prompts import DirectPromptManager
```

## Implementation Plan

### Phase 1: Analysis and Preparation

#### Task 1.1: Remove Dead Code

**Objective:** Clean up unused files and references

**Steps:**

1. **Delete Dead Files**
   - Delete `src/backend/optimized_agent_instructions.py`
   - Clean up any remaining `prompt_templates.py` references

2. **Verify No Dependencies**
   - Confirm no imports or references to deleted files
   - Run tests to ensure no broken dependencies

**Validation Criteria:**

- Dead files removed successfully
- No broken imports or references
- All tests pass

#### Task 1.2: Analyze Current Usage Patterns

**Objective:** Document exact usage patterns for consolidation

**Steps:**

1. **Document Usage Points**
   - `get_enhanced_agent_instructions()`: 3 usage points in `main.py`
   - `DirectPromptManager`: 6 usage points in `main.py`
   - `AnalysisIntent`: Used in `api_models.py` for API responses

2. **Document Import Patterns**
   - Try/except import pattern for relative vs absolute imports
   - API model dependencies

**Validation Criteria:**

- All usage points documented
- Import patterns understood
- Dependencies mapped

### Phase 2: Consolidation Design

#### Task 2.1: Create Unified Prompt Manager

**Objective:** Design unified system architecture

**Steps:**

1. **Design Unified Architecture**
   - Single file: `src/backend/unified_prompts.py`
   - Class: `UnifiedPromptManager`
   - Methods: Consolidate all functionality from both systems

2. **Design Backward Compatibility**
   - Maintain existing method signatures
   - Preserve `AnalysisIntent` enum for API compatibility
   - Maintain try/except import pattern

**Validation Criteria:**

- Architecture designed and documented
- Backward compatibility ensured
- All functionality preserved

#### Task 2.2: Plan Migration Strategy

**Objective:** Create step-by-step migration plan

**Steps:**

1. **Create Migration Steps**
   - Step-by-step implementation plan
   - Testing strategy
   - Rollback plan

2. **Identify Risks and Mitigations**
   - Risk assessment
   - Mitigation strategies
   - Testing approach

**Validation Criteria:**

- Migration plan complete
- Risks identified and mitigated
- Testing strategy defined

### Phase 3: Implementation

#### Task 3.1: Create Unified System

**Objective:** Implement unified prompt management system

**Steps:**

1. **Create Unified File**
   - Create `src/backend/unified_prompts.py`
   - Implement `UnifiedPromptManager` class
   - Consolidate all prompt logic

2. **Implement Core Methods**
   - `get_enhanced_agent_instructions()` - From main.py
   - `generate_direct_prompt()` - From DirectPromptManager
   - `detect_analysis_intent()` - From DirectPromptManager
   - `extract_ticker_from_message()` - From DirectPromptManager
   - `_build_system_prompts()` - From DirectPromptManager

3. **Preserve AnalysisIntent Enum**
   - Move `AnalysisIntent` enum to unified file
   - Maintain all enum values
   - Ensure API compatibility

**Code Structure:**

```python
# src/backend/unified_prompts.py
from enum import Enum
from typing import Dict, Any, Optional
import re
import logging

class AnalysisIntent(Enum):
    SNAPSHOT = "snapshot"
    SUPPORT_RESISTANCE = "support_resistance"
    TECHNICAL = "technical"
    GENERAL = "general"

class UnifiedPromptManager:
    """Unified prompt management system consolidating all prompt functionality."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system_prompts = self._build_system_prompts()
        self.user_prompts = self._build_user_prompts()
    
    def get_enhanced_agent_instructions(self) -> str:
        """Generate enhanced agent instructions with current date/time context."""
        # Implementation from main.py
    
    def generate_direct_prompt(self, user_message: str, analysis_intent: AnalysisIntent) -> Dict[str, Any]:
        """Generate direct prompt for AI model."""
        # Implementation from DirectPromptManager
    
    def detect_analysis_intent(self, message: str) -> AnalysisIntent:
        """Detect analysis intent from user message."""
        # Implementation from DirectPromptManager
    
    def extract_ticker_from_message(self, message: str) -> Optional[str]:
        """Extract ticker symbol from user message."""
        # Implementation from DirectPromptManager
    
    def _build_system_prompts(self) -> Dict[AnalysisIntent, str]:
        """Build optimized system prompts for different analysis types."""
        # Implementation from DirectPromptManager
    
    def _build_user_prompts(self) -> Dict[AnalysisIntent, str]:
        """Build optimized user prompt templates."""
        # Implementation from DirectPromptManager
```

**Validation Criteria:**

- Unified file created successfully
- All methods implemented
- AnalysisIntent enum preserved
- All functionality consolidated

#### Task 3.2: Update Imports

**Objective:** Update all imports to use unified system

**Steps:**

1. **Update main.py Imports**
   - Replace `DirectPromptManager` import with `UnifiedPromptManager`
   - Update usage to use unified system
   - Maintain try/except import pattern

2. **Update api_models.py Imports**
   - Replace `AnalysisIntent` import with unified system
   - Maintain try/except import pattern

3. **Update Usage Patterns**
   - Update all 9 usage points to use unified system
   - Maintain backward compatibility

**Import Updates:**

```python
# main.py
try:
    from .unified_prompts import UnifiedPromptManager, AnalysisIntent
except ImportError:
    from unified_prompts import UnifiedPromptManager, AnalysisIntent

# api_models.py
try:
    from .unified_prompts import AnalysisIntent
except ImportError:
    from unified_prompts import AnalysisIntent
```

**Validation Criteria:**

- All imports updated successfully
- Try/except pattern maintained
- All usage points updated
- No broken imports

#### Task 3.3: Remove Old Files

**Objective:** Remove old prompt files after successful migration

**Steps:**

1. **Remove Old Files**
   - Delete `src/backend/direct_prompts.py`
   - Delete `src/backend/optimized_agent_instructions.py`
   - Clean up any remaining references

2. **Verify No Broken References**
   - Confirm no remaining imports or references
   - Run tests to ensure functionality

**Validation Criteria:**

- Old files removed successfully
- No broken references
- All tests pass

### Phase 4: Testing and Validation

#### Task 4.1: Functional Testing

**Objective:** Ensure all functionality works correctly

**Steps:**

1. **Test All Usage Points**
   - Test all 9 usage points work correctly
   - Verify API responses still work
   - Test CLI functionality

2. **Test Analysis Intents**
   - Test SNAPSHOT analysis
   - Test SUPPORT_RESISTANCE analysis
   - Test TECHNICAL analysis
   - Test GENERAL analysis

3. **Test Ticker Extraction**
   - Test ticker extraction with various inputs
   - Verify accuracy of extraction
   - Test edge cases

**Validation Criteria:**

- All usage points work correctly
- All analysis intents work
- Ticker extraction works
- No functional regressions

#### Task 4.2: Performance Testing

**Objective:** Ensure no performance regressions

**Steps:**

1. **Measure Performance**
   - Measure prompt generation speed
   - Measure analysis intent detection speed
   - Measure ticker extraction speed

2. **Compare Performance**
   - Compare with original performance
   - Ensure no regressions
   - Document improvements

**Validation Criteria:**

- No performance regressions
- Performance maintained or improved
- Metrics documented

#### Task 4.3: Integration Testing

**Objective:** Test complete system integration

**Steps:**

1. **Test API Integration**
   - Test all API endpoints
   - Verify API responses
   - Test error handling

2. **Test CLI Integration**
   - Test CLI functionality
   - Verify prompt generation
   - Test error handling

3. **Test Frontend Integration**
   - Test frontend functionality
   - Verify prompt generation
   - Test error handling

**Validation Criteria:**

- All integrations work correctly
- No broken functionality
- Error handling works

### Phase 5: Documentation and Cleanup

#### Task 5.1: Update Documentation

**Objective:** Update all documentation to reflect new system

**Steps:**

1. **Update Code Comments**
   - Update comments in unified file
   - Document new architecture
   - Update method documentation

2. **Update API Documentation**
   - Update API documentation
   - Document new system
   - Update examples

3. **Update README**
   - Update README if needed
   - Document new architecture
   - Update examples

**Validation Criteria:**

- Documentation updated
- Comments accurate
- Examples work

#### Task 5.2: Final Cleanup

**Objective:** Final cleanup and validation

**Steps:**

1. **Remove Dead Code**
   - Remove any remaining dead code
   - Clean up unused imports
   - Remove unused variables

2. **Final Validation**
   - Run all tests
   - Verify functionality
   - Check for any issues

**Validation Criteria:**

- No dead code remaining
- All tests pass
- No issues found

## Risk Assessment

### Low Risk Items

1. **Dead Code Removal**

   - Risk: Minimal (files are unused)
   - Mitigation: Verify no dependencies before deletion

2. **Import Updates**

   - Risk: Low (maintaining same interface)
   - Mitigation: Maintain try/except import pattern

3. **Method Consolidation**

   - Risk: Low (preserving existing functionality)
   - Mitigation: Maintain backward compatibility

### Medium Risk Items

1. **API Compatibility**

   - Risk: Medium (AnalysisIntent enum usage)
   - Mitigation: Preserve enum exactly as-is

2. **Usage Pattern Changes**

   - Risk: Medium (9 usage points to update)
   - Mitigation: Update all usage points systematically

### High Risk Items

None identified - this is a low-risk consolidation

## Success Criteria

### Functional Success Criteria

1. **All Functionality Preserved**

   - All 9 usage points work correctly
   - All analysis intents work
   - Ticker extraction works
   - API responses work

2. **No Breaking Changes**

   - API compatibility maintained
   - Import patterns preserved
   - Method signatures preserved

3. **Code Quality Improved**

   - Single source of truth for prompts
   - Reduced code duplication
   - Better maintainability

### Performance Success Criteria

1. **No Performance Regressions**

   - Prompt generation speed maintained
   - Analysis intent detection speed maintained
   - Ticker extraction speed maintained

2. **Potential Performance Improvements**

   - Reduced memory usage (fewer files)
   - Faster imports (fewer files)
   - Better code organization

### Quality Success Criteria

1. **Code Organization**

   - Single file for all prompt functionality
   - Clear separation of concerns
   - Better maintainability

2. **Documentation**

   - Updated documentation
   - Clear code comments
   - Accurate examples

## Testing Strategy

### Unit Testing

1. **Test All Methods**

   - Test `get_enhanced_agent_instructions()`
   - Test `generate_direct_prompt()`
   - Test `detect_analysis_intent()`
   - Test `extract_ticker_from_message()`

2. **Test Analysis Intents**

   - Test all 4 analysis intents
   - Test intent detection accuracy
   - Test prompt generation

3. **Test Ticker Extraction**

   - Test various ticker formats
   - Test false positive filtering
   - Test edge cases

### Integration Testing

1. **Test API Integration**

   - Test all API endpoints
   - Test API responses
   - Test error handling

2. **Test CLI Integration**

   - Test CLI functionality
   - Test prompt generation
   - Test error handling

3. **Test Frontend Integration**

   - Test frontend functionality
   - Test prompt generation
   - Test error handling

### Performance Testing

1. **Measure Performance**

   - Measure prompt generation speed
   - Measure analysis intent detection speed
   - Measure ticker extraction speed

2. **Compare Performance**

   - Compare with original performance
   - Ensure no regressions
   - Document improvements

## Rollback Plan

### Rollback Triggers

1. **Functional Issues**

   - Any broken functionality
   - API compatibility issues
   - Import errors

2. **Performance Issues**

   - Significant performance regressions
   - Memory usage issues
   - Startup time issues

### Rollback Procedure

1. **Immediate Rollback**

   - Revert to previous commit
   - Restore original files
   - Verify functionality

2. **Investigation**

   - Investigate root cause
   - Fix issues
   - Re-test

3. **Re-implementation**

   - Implement fixes
   - Test thoroughly
   - Deploy again

## Conclusion

This prompt consolidation implementation plan provides a comprehensive, low-risk approach to consolidating the Market Parser application's prompt management system. The plan addresses the critical findings from the comprehensive review and provides a clear path to a unified, maintainable prompt system.

**Key Benefits:**

- **Simplified Architecture**: 2 files → 1 file
- **Reduced Complexity**: Single prompt management system
- **Better Maintainability**: Single source of truth for prompts
- **No Breaking Changes**: Backward compatibility maintained
- **Low Risk**: Minimal functional changes

**Expected Outcomes:**

- Single unified prompt management system
- Eliminated code duplication
- Improved maintainability
- Preserved functionality
- Better code organization

The implementation should be straightforward and low-risk, with comprehensive testing to ensure no regressions. The plan provides clear success criteria and rollback procedures to ensure a successful consolidation.
