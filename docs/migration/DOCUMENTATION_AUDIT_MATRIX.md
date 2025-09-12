# Documentation Audit Matrix - Phase 2

## Critical Documentation Assessment

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **CLAUDE.md** | ✓ | ✓ | | `/CLAUDE.md` | **CRITICAL** | Main project instructions |
| **README.md** | ✓ | ✓ | | `/README.md` | **CRITICAL** | Main project documentation |
| **LAST_TASK_SUMMARY.md** | ✓ | ✓ | | `/LAST_TASK_SUMMARY.md` | **CRITICAL** | Task tracking |

## Configuration & Setup Documentation

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **DEVELOPMENT_WORKFLOW.md** | ✓ | ✓ | | `/DEVELOPMENT_WORKFLOW.md` | Important | Development processes |
| **SECURITY.md** | ✓ | ✓ | | `/SECURITY.md` | Important | Security guidelines |
| **.env.example** | ✓ | ✓ | | `/.env.example` | Important | Environment template |
| **pyproject.toml** | ✓ | Update | | `/pyproject.toml` | Important | Needs path updates |

## Legacy System Documentation (TO REMOVE)

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **STRUCTURE.md** | | | ✓ | - | Legacy | References old structure |
| Legacy Gradio docs | | | ✓ | - | Legacy | No longer relevant |
| Old API guides | Partial | Update | Partial | `/docs/api/` | Review | Keep relevant parts |

## Migration-Specific Documentation

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **ENHANCED_10_PHASE_MIGRATION_ORCHESTRATION_PLAN.md** | ✓ | ✓ | | `/docs/migration/` | Active | Migration guide |
| **BRANCH_STRATEGY.md** | ✓ | ✓ | | `/docs/migration/` | New | Created in Phase 1 |

## Testing Documentation

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **PLAYWRIGHT_MCP_TEST_EXECUTION_REPORT_*.md** | ✓ | ✓ | | `/docs/test_reports/` | Important | Test history |
| **playwright_CLI_test_*.md** | ✓ | ✓ | | `/docs/test_reports/` | Important | Test results |
| Testing specifications | ✓ | ✓ | | `/docs/testing/` | Important | Test procedures |

## System-Specific Documentation

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **MCP_TOOL_USAGE_GUIDE.md** | ✓ | ✓ | | `/docs/guides/` | Important | MCP integration |
| **MCP_TIMEOUT_FIXES_IMPLEMENTATION_PLAN.md** | ✓ | ✓ | | `/docs/implementation/` | Important | MCP fixes |
| **api-integration-guide.md** | ✓ | Update | | `/docs/api/` | Important | Needs OpenAI updates |
| **api-security-performance.md** | ✓ | Update | | `/docs/api/` | Important | Needs FastAPI updates |

## Temporary/Working Files

| Document | Keep | Migrate | Remove | New Location | Status | Notes |
|----------|------|---------|--------|--------------|--------|-------|
| **new_task_details.md** | | | ✓ | - | Temporary | Working file |
| **ORCHESTRATION_IMPLEMENTATION_REPORT.md** | Archive | | | `/docs/archive/` | Archive | Historical |

## Documentation State Summary

### Critical Files (Must Migrate)
- CLAUDE.md - Project instructions
- README.md - Main documentation
- LAST_TASK_SUMMARY.md - Task tracking
- DEVELOPMENT_WORKFLOW.md - Workflow processes

### Files Requiring Updates
- pyproject.toml - Path updates for new structure
- api-integration-guide.md - OpenAI system updates
- api-security-performance.md - FastAPI updates

### Files to Remove
- STRUCTURE.md - References old architecture
- new_task_details.md - Temporary working file
- Any Gradio-specific documentation

### New Directory Structure
```
/docs/
├── api/                 # API documentation
├── guides/              # User and development guides
├── implementation/      # Implementation plans
├── migration/           # Migration documentation
├── testing/             # Test specifications
├── test_reports/        # Test execution reports
└── archive/             # Historical documents
```

## Migration Actions Required

1. **Phase 3-4**: Remove legacy files and documentation references
2. **Phase 5**: Update path references in all documentation
3. **Phase 8**: Comprehensive documentation updates for new structure
4. **Phase 10**: Validate all documentation links and references

## Risk Assessment

### High Risk
- CLAUDE.md path updates - Critical for system operation
- README.md installation instructions - Must work with new structure

### Medium Risk
- API documentation updates - Needs OpenAI system alignment
- Test documentation migration - Must preserve test procedures

### Low Risk
- Archive documentation - Historical reference only
- Legacy documentation removal - Cleanup only

## Current Documentation State Recorded

**Audit Date**: 2025-09-11  
**Branch**: migration-experimental  
**Phase**: Phase 2 - Documentation Migration Preparation  
**Total Documents Identified**: 45+ files  
**Action Items**: 12 critical updates, 8 removals, 6 new locations