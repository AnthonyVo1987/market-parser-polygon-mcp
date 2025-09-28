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

## Backend Modularization Implementation Plan

### Phase 1: Research and Analysis ✅ COMPLETED
- [x] Use Context7 to research FastAPI modularization best practices
- [x] Use Serena tools to analyze current main.py structure (881 lines)
- [x] Identify modularization opportunities and responsibilities

### Phase 2: Create Modular Structure

#### 2.1 Configuration Module
- [ ] **Task**: Extract Settings class to `src/backend/config.py`
  - Move Settings class (lines 67-191) to separate module
  - Update imports in main.py
  - Ensure configuration loading works correctly

#### 2.2 Dependencies Module  
- [ ] **Task**: Create `src/backend/dependencies.py`
  - Extract shared dependencies like `get_model_rate_limits`
  - Create dependency functions for MCP server and session management
  - Add proper type hints and documentation

#### 2.3 Router Modules
- [ ] **Task**: Create `src/backend/routers/` directory structure
  - Create `__init__.py` for package
  - Create `chat.py` for chat endpoint (lines 508-603)
  - Create `health.py` for health check endpoints (lines 642-648)
  - Create `models.py` for model management (lines 651-750)
  - Create `system.py` for system status (lines 618-633)

#### 2.4 Services Module
- [ ] **Task**: Create `src/backend/services/` directory structure
  - Create `__init__.py` for package
  - Create `mcp_service.py` for MCP server management
  - Create `agent_service.py` for agent creation and management
  - Create `prompt_service.py` for prompt templates and instructions

#### 2.5 Utils Module
- [ ] **Task**: Create `src/backend/utils/` directory structure
  - Create `__init__.py` for package
  - Create `response_utils.py` for print_response and print_error functions
  - Create `datetime_utils.py` for datetime context functions
  - Create `validation_utils.py` for input validation

#### 2.6 CLI Module
- [ ] **Task**: Create `src/backend/cli.py`
  - Extract CLI functionality (lines 757-880) to separate module
  - Maintain CLI session management
  - Keep CLI entry point functionality

### Phase 3: Refactor Main Application

#### 3.1 Update Main.py
- [ ] **Task**: Refactor main.py to use modular structure
  - Import from new modules
  - Remove extracted code
  - Update FastAPI app setup
  - Include all routers
  - Maintain lifespan management

#### 3.2 Update Imports
- [ ] **Task**: Fix all import statements
  - Update relative imports
  - Ensure proper package structure
  - Test import resolution

### Phase 4: Testing and Validation

#### 4.1 Linting
- [ ] **Task**: Run comprehensive linting
  - Execute `npm run lint` for all linting
  - Fix any pylint issues
  - Fix any ESLint issues
  - Maintain code quality standards

#### 4.2 CLI Testing
- [ ] **Task**: Test CLI functionality
  - Execute `test_7_prompts_comprehensive.sh`
  - Verify CLI session management works
  - Test agent creation and MCP server functionality
  - Fix any issues found

#### 4.3 GUI Testing
- [ ] **Task**: Test GUI functionality using Playwright
  - Execute `tests/playwright/test_prompts.md`
  - Verify API endpoints work correctly
  - Test chat functionality
  - Test model management
  - Test health checks
  - Fix any issues found

### Phase 5: Documentation and Memory Updates

#### 5.1 Update Project Memories
- [ ] **Task**: Use Serena tools to update project memories
  - Create memory for modularization completion
  - Update architecture documentation
  - Document new file structure
  - Update development guidelines

#### 5.2 Update Documentation
- [ ] **Task**: Update project documentation
  - Update CLAUDE.md with new structure
  - Update README.md if needed
  - Document new module responsibilities
  - Update development setup instructions

### Expected File Structure After Modularization

```
src/backend/
├── __init__.py
├── main.py                    # Simplified main application (100-150 lines)
├── config.py                  # Settings and configuration
├── dependencies.py            # Shared dependencies
├── cli.py                     # CLI functionality
├── api_models.py              # Existing API models
├── routers/
│   ├── __init__.py
│   ├── chat.py               # Chat endpoints
│   ├── health.py             # Health check endpoints
│   ├── models.py             # Model management endpoints
│   └── system.py             # System status endpoints
├── services/
│   ├── __init__.py
│   ├── mcp_service.py        # MCP server management
│   ├── agent_service.py      # Agent creation and management
│   └── prompt_service.py     # Prompt templates and instructions
└── utils/
    ├── __init__.py
    ├── response_utils.py     # Response formatting
    ├── datetime_utils.py     # DateTime context
    └── validation_utils.py   # Input validation
```

### Success Criteria

- [ ] Main.py reduced from 881 lines to ~100-150 lines
- [ ] All functionality preserved and working
- [ ] Clean separation of concerns
- [ ] Proper FastAPI modularization patterns followed
- [ ] All tests passing (CLI and GUI)
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Project memories updated

### Implementation Notes

- Follow FastAPI best practices for APIRouter usage
- Maintain backward compatibility
- Preserve all existing functionality
- Use proper Python package structure with __init__.py files
- Implement proper error handling and logging
- Maintain performance characteristics
- Follow existing code style and conventions

### Risk Mitigation

- Test each module extraction individually
- Maintain git commits for each major change
- Keep backup of original main.py
- Test thoroughly after each phase
- Use Serena tools for code analysis throughout
- Use Playwright for comprehensive GUI testing