# 🔴 CRITICAL: AI Model Selection Removal Implementation Plan

## 📋 Overview

Complete removal of AI Model Selection implementation and consolidation to single gpt-5-nano model with temperature parameter removal.

## 🎯 Success Criteria

- ✅ No model selection ability in UI or API
- ✅ gpt-5-nano as single default active model
- ✅ No references to gpt-5-mini anywhere
- ✅ No references to temperature parameter anywhere
- ✅ All documentation updated
- ✅ All tests passing

## 📝 Implementation Tasks

### Phase 1: Configuration Updates

#### Task 1.1: Update app.config.json

- [ ] Remove `availableModels` array
- [ ] Remove `gpt-5-mini` model configuration
- [ ] Remove `temperature` parameter
- [ ] Add `default_active_model: "gpt-5-nano"`
- [ ] Verify JSON syntax is valid

#### Task 1.2: Update Backend Configuration

- [ ] Update `src/backend/config.py` to remove `available_models` list
- [ ] Update `src/backend/config.py` to remove `temperature` field
- [ ] Add `default_active_model` field with default "gpt-5-nano"
- [ ] Update configuration loading logic
- [ ] Remove model selection logic from agent service

#### Task 1.3: Update Frontend Configuration

- [ ] Update `src/frontend/config/config.loader.ts` to remove `availableModels`
- [ ] Remove model selection components if they exist
- [ ] Update TypeScript types to remove model selection

### Phase 2: Code Cleanup

#### Task 2.1: Backend Code Updates

- [ ] Update `src/backend/api_models.py` to remove `GPT_5_MINI` enum
- [ ] Update `src/backend/services/agent_service.py` to use single model
- [ ] Remove any model selection API endpoints
- [ ] Update chat endpoints to use default model only
- [ ] Remove temperature parameter from all AI calls

#### Task 2.2: Frontend Code Updates

- [ ] Update `src/frontend/types/ai_models.ts` to remove `GPT_5_MINI`
- [ ] Remove any model selector components
- [ ] Update API service calls to remove model selection
- [ ] Remove model selection from chat interfaces

### Phase 3: Documentation Updates

#### Task 3.1: Configuration Documentation

- [ ] Update `docs/configuration-guide.md` to remove availableModels references
- [ ] Remove gpt-5-mini configuration examples
- [ ] Remove temperature parameter documentation
- [ ] Update configuration examples to show single model setup

#### Task 3.2: API Documentation

- [ ] Update `docs/api/api-integration-guide.md` to remove model selection
- [ ] Remove gpt-5-mini references
- [ ] Remove temperature parameter references
- [ ] Update API examples

#### Task 3.3: Implementation Plans

- [ ] Update `docs/implementation_plans/UI_Enhanced_Playwright_Test_Plan_2025.md`
- [ ] Remove gpt-5-mini test references
- [ ] Update test plans to use single model

#### Task 3.4: Main Documentation

- [ ] Update `README.md` to remove temperature references
- [ ] Remove model selection mentions
- [ ] Update feature descriptions

#### Task 3.5: Archived Documentation

- [ ] Update `docs/archived/IBKR_POLYGON_API_COMPARISON_FINAL.md`
- [ ] Remove gpt-5-mini references
- [ ] Remove temperature references

#### Task 3.6: Test Reports

- [ ] Update `docs/test_reports/comprehensive_test_execution_report_2025-09-09.md`
- [ ] Remove gpt-5-mini references
- [ ] Update test descriptions

#### Task 3.7: Implementation Plans

- [ ] Update `docs/implementation_plans/direct_prompt_migration_scoping.md`
- [ ] Remove temperature optimization references
- [ ] Remove model selection mentions

### Phase 4: Memory Updates

#### Task 4.1: Serena Memory Cleanup

- [ ] Update `.serena/memories/project_overview.md` to remove temperature references
- [ ] Update `.serena/memories/gpt5_optimization_completion_2025_09_28.md`
- [ ] Update `.serena/memories/commit_message_cache.md`
- [ ] Update `.serena/memories/latest_fixes_milestones.md`
- [ ] Create new memory for model selection removal

### Phase 5: Testing and Validation

#### Task 5.1: Code Validation

- [ ] Run linting to ensure no syntax errors
- [ ] Run type checking for TypeScript files
- [ ] Verify all imports are correct
- [ ] Test configuration loading

#### Task 5.2: Functional Testing

- [ ] Test backend server startup
- [ ] Test frontend build
- [ ] Test API endpoints
- [ ] Run comprehensive 7-prompt test suite
- [ ] Verify all tests pass

### Phase 6: Final Verification

#### Task 6.1: Search Verification

- [ ] Search for any remaining `availableModels` references
- [ ] Search for any remaining `gpt-5-mini` references
- [ ] Search for any remaining `temperature` references
- [ ] Verify no model selection UI elements exist

#### Task 6.2: Documentation Review

- [ ] Review all updated documentation
- [ ] Ensure consistency across all docs
- [ ] Verify no outdated information remains

## 🔧 Implementation Notes

### Configuration Structure

```json
{
  "backend": {
    "ai": {
      "default_active_model": "gpt-5-nano"
    }
  }
}
```

### Backend Configuration Class

```python
class AIConfig:
    default_active_model: str = "gpt-5-nano"
    
    def __init__(self, ai_config: dict):
        self.default_active_model = ai_config.get("default_active_model", "gpt-5-nano")
```

### Files to Modify

1. `config/app.config.json`
2. `src/backend/config.py`
3. `src/backend/api_models.py`
4. `src/backend/services/agent_service.py`
5. `src/frontend/config/config.loader.ts`
6. `src/frontend/types/ai_models.ts`
7. All documentation files with references

### Files to Search and Clean

- All `.md` files in `docs/`
- All `.md` files in `.serena/memories/`
- All test report files
- All implementation plan files

## ⚠️ Critical Requirements

- **NO MODEL SELECTION**: Remove all ability to select models
- **SINGLE MODEL ONLY**: Only gpt-5-nano supported
- **NO TEMPERATURE**: Remove all temperature parameter usage
- **COMPLETE CLEANUP**: No references to removed features anywhere
- **TESTING REQUIRED**: Must run comprehensive tests after code changes

## 🚀 Success Metrics

- [ ] 0 references to `availableModels`
- [ ] 0 references to `gpt-5-mini`
- [ ] 0 references to `temperature`
- [ ] All 7 comprehensive tests passing
- [ ] No model selection UI elements
- [ ] Single model configuration working
- [ ] All documentation updated and consistent
