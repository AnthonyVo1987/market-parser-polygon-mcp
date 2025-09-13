# Project Structure Guide

This document explains the organizational principles behind the Market Parser project structure and provides guidelines for future development.

## Overview

The Market Parser project has been reorganized into a logical directory structure that separates concerns, improves maintainability, and provides clear guidelines for developers.

## Directory Organization

### Core Application Modules (`src/`)

**Purpose**: Contains all core application logic and shared components.

```
src/
├── __init__.py                   # Package initialization
├── response_parser.py           # AI response parsing utilities
├── json_parser.py              # JSON parsing with fallback strategies  
├── json_schemas.py             # Schema definitions and validation
├── prompt_templates.py         # Structured prompt templates
├── schema_validator.py         # Validation logic and business rules
├── json_debug_logger.py        # Debug logging for JSON workflows
├── security_utils.py           # Input validation and security utilities
└── example_json_responses.py   # Example responses for testing/development
```

**Guidelines:**
- All reusable application logic belongs here
- Modules should be focused on a single responsibility
- Use clear, descriptive names for modules
- Include comprehensive docstrings and type hints

### State Management (`stock_data_fsm/`)

**Purpose**: Finite State Machine implementation for GUI workflow management.

```
stock_data_fsm/
├── __init__.py
├── states.py                    # Application states and context data
├── transitions.py              # State transition rules and validation
├── manager.py                  # FSM controller and orchestration
└── tests/                      # FSM-specific test suite
    ├── __init__.py
    ├── test_states.py
    ├── test_transitions.py
    ├── test_manager.py
    └── test_integration.py
```

**Guidelines:**
- Keep FSM logic separate from business logic
- Include comprehensive tests for state transitions
- Document state diagrams in comments or docs
- Maintain deterministic behavior

### Comprehensive Testing (`tests/`)

**Purpose**: All test files consolidated for easy test management and execution.

```
tests/
├── __init__.py
├── test_integration.py         # Main integration tests
├── test_actual_integration.py  # Real API integration tests
├── test_prompt_templates.py    # Prompt template validation
├── test_response_parser.py     # Response parsing tests
├── test_json_schemas.py        # Schema validation tests
├── test_production_*.py        # Production scenario tests
├── run_*.py                    # Test runners and execution scripts
└── validate_*.py               # Fix validation scripts
```

**Guidelines:**
- Organize tests by functionality, not by file structure
- Use descriptive test names that explain the scenario
- Include both unit and integration tests
- Maintain production scenario tests for real-world validation

### Logging and Debug Information (`logs/`)

**Purpose**: Centralized location for all application logs and debug information.

```
logs/
├── json_workflow_debug.log     # JSON processing workflow logs
├── production_*.log            # Production scenario logs
├── debug_*.log                 # General debug information
└── comprehensive_*.log         # Comprehensive test results
```

**Guidelines:**
- Use structured logging with timestamps
- Separate logs by functionality or environment
- Include sufficient context for debugging
- Rotate logs to prevent disk space issues

### Utility Scripts (`scripts/`)

**Purpose**: Development utilities, demonstrations, and one-off scripts.

```
scripts/
├── debug_parser_data_sources.py  # Parser debugging utilities
├── demo_json_prompts.py          # JSON prompt demonstrations
└── simple_test.py                # Simple testing utilities
```

**Guidelines:**
- Use scripts for development tasks and demonstrations
- Include clear documentation in script headers
- Make scripts executable and self-contained
- Consider moving frequently-used scripts to main codebase

### Configuration Management (`config/`)

**Purpose**: Future home for configuration files and environment-specific settings.

```
config/
└── (ready for future configuration files)
```

**Guidelines:**
- Use for environment-specific configurations
- Separate development, staging, and production configs
- Never commit sensitive information
- Use clear naming conventions

### Documentation (`docs/`)

**Purpose**: Comprehensive project documentation with organized subdirectories.

```
docs/
├── JSON_ARCHITECTURE_GUIDE.md     # JSON system architecture
├── USER_GUIDE_JSON_FEATURES.md    # User-facing JSON features
├── TROUBLESHOOTING_JSON.md        # JSON troubleshooting guide
├── FEATURE_SCOPE_STOCK_DATA_GUI.md # GUI feature specifications
├── DEPLOYMENT_GUIDE_AWS.md        # AWS deployment instructions
├── MIGRATION_GUIDE.md             # Migration procedures
├── reports/                       # Technical reports and analysis
│   ├── README.md                  # Reports index
│   ├── COMPREHENSIVE_BUG_FIX_REPORT.md
│   ├── JSON_RESPONSE_IMPLEMENTATION_REPORT.md
│   └── *.md                      # Various technical reports
└── scratchpad.md                 # Development notes and ideas
```

**Guidelines:**
- Organize documentation by audience and purpose
- Use clear, descriptive filenames
- Maintain a reports subfolder for technical analysis
- Keep documentation current with code changes

### Project Assets (`images/`)

**Purpose**: Static assets including logos, diagrams, and screenshots.

```
images/
└── logo.png                      # Project logo
```

**Guidelines:**
- Use descriptive filenames
- Optimize images for web display
- Include alt text in documentation
- Consider version control impact of binary files

## File Placement Guidelines

### Where to Put New Files

**Business Logic**: Add to `src/` directory with appropriate module naming
**Tests**: Add to `tests/` directory with `test_` prefix
**Documentation**: Add to `docs/` directory or `docs/reports/` for technical reports
**Utilities**: Add to `scripts/` directory for development tools
**Configuration**: Add to `config/` directory for environment settings
**Debug Information**: Logs automatically go to `logs/` directory

### Import Patterns

With the new structure, use these import patterns:

```python
# Core modules from src/
from src.response_parser import ResponseParser
from src.prompt_templates import PromptTemplateManager
from src.json_schemas import StockDataSchema
from src.schema_validator import SchemaValidator
from src.json_debug_logger import JSONDebugLogger

# FSM components
from stock_data_fsm.states import AppState, StateContext
from stock_data_fsm.manager import StateManager
from stock_data_fsm.transitions import StateTransitions

# Security utilities
from src.security_utils import validate_input, sanitize_data
```

## Development Workflow

### Adding New Features

1. **Plan**: Document in `docs/` if significant
2. **Implement**: Add code to appropriate `src/` module
3. **Test**: Create tests in `tests/` directory
4. **Document**: Update relevant documentation
5. **Validate**: Run full test suite

### Testing Strategy

```bash
# Run all OpenAI Playwright tests
cd tests/playwright
npx playwright test

# Run specific test categories
npx playwright test test-b001-market-status.spec.ts
npx playwright test test-b00*.spec.ts

# Run FSM-specific tests
uv run pytest stock_data_fsm/tests/

# Run production validation
uv run python tests/run_production_tests.py
```

### Code Organization Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Testability**: All modules are designed to be easily testable in isolation
3. **Maintainability**: Clear organization makes finding and updating code straightforward
4. **Scalability**: Structure supports growth without major reorganization
5. **Documentation**: Everything is documented for future developers

## Migration Notes

### From Old Structure

The reorganization moved files as follows:

- `prompt_templates.py` → `src/prompt_templates.py`
- `response_parser.py` → `src/response_parser.py`
- `test_*.py` → `tests/test_*.py`
- Various JSON modules → `src/json_*.py`
- Utility scripts → `scripts/`
- Log files → `logs/`

### Updating Imports

Update any existing imports to use the new structure:

```python
# Old imports
from prompt_templates import PromptTemplateManager
from response_parser import ResponseParser

# New imports  
from src.prompt_templates import PromptTemplateManager
from src.response_parser import ResponseParser
```

## Future Considerations

### Planned Enhancements

- **Config Management**: Environment-specific configurations in `config/`
- **Plugin System**: Extensible architecture for new data sources
- **API Layer**: RESTful API endpoints for external integration
- **Monitoring**: Enhanced observability and metrics collection

### Scalability Patterns

- **Microservices**: Structure supports future service extraction
- **Containerization**: Clear boundaries for Docker packaging
- **Testing**: Comprehensive test strategy supports CI/CD
- **Documentation**: Structure scales with team growth

## Maintenance Guidelines

### Regular Tasks

1. **Review Structure**: Periodically assess if organization still serves the project
2. **Clean Logs**: Implement log rotation and cleanup procedures
3. **Update Documentation**: Keep docs current with code changes
4. **Test Coverage**: Maintain comprehensive test coverage
5. **Security Review**: Regular security audits of dependencies and patterns

### Quality Gates

- All new modules must include tests
- Documentation must be updated with significant changes
- Code must pass linting and type checking
- Performance must not regress
- Security guidelines must be followed

This structure provides a solid foundation for continued development while maintaining clarity and organization as the project grows.