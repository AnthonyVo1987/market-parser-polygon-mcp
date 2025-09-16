# Project Structure Guide

This document explains the organizational principles behind the Market Parser project structure and provides guidelines for future development.

## Overview

The Market Parser project has been reorganized into a logical directory structure that separates concerns, improves maintainability, and provides clear guidelines for developers.

## Directory Organization

### Backend Application (`src/backend/`)

**Purpose**: Contains the FastAPI backend with OpenAI Agents SDK and Polygon.io MCP integration.

```
src/backend/
├── main.py                      # FastAPI application and agent system
├── api_models.py               # Pydantic models for API requests/responses
├── prompt_templates.py         # Prompt generation and template management
└── utils/                      # Backend utilities and logging
    └── logger.py               # Logging configuration
```

**Guidelines:**
- All backend business logic belongs here
- Use FastAPI for API endpoints
- Integrate with OpenAI Agents SDK for financial analysis
- Connect to Polygon.io MCP server for market data

### Frontend Application (`src/frontend/`)

**Purpose**: React TypeScript frontend for the web interface.

```
src/frontend/
├── components/                  # React components
├── hooks/                      # Custom React hooks
├── types/                      # TypeScript type definitions
└── App.tsx                     # Main application component
```

**Guidelines:**
- Modern React 18.2+ patterns with hooks
- TypeScript for type safety
- Responsive design for multiple devices
- PWA capabilities enabled

### Testing Infrastructure (`tests/`)

**Purpose**: Comprehensive Playwright E2E testing for the full application.

```
tests/
├── playwright/                  # Playwright E2E test suite
│   ├── test-b001-market-status.spec.ts    # Market status queries
│   ├── test-b002-stock-analysis.spec.ts   # Individual stock analysis
│   ├── test-b003-multi-ticker.spec.ts     # Multi-ticker queries
│   └── ...                                # B001-B016 test suite
├── helpers/                     # Test utility functions
└── reports/                     # Test execution reports
```

**Guidelines:**
- Use Playwright for comprehensive E2E testing
- Test both frontend UI and backend integration
- Cover market analysis workflows and user interactions
- Generate detailed test reports for debugging

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
├── development/                    # Development workflow and structure guides
├── testing/                       # Playwright testing documentation
├── api/                          # API integration and contracts
├── MCP_Tools_Usage_Guide/        # MCP tool usage guides
├── COMPONENT_STYLING_GUIDE.md    # Frontend styling guidelines
├── TYPOGRAPHY_SYSTEM_GUIDE.md    # Typography system documentation
└── archived/                     # Historical documentation (minimal)
```

**Guidelines:**
- Organize documentation by audience and purpose
- Use clear, descriptive filenames
- Keep documentation current with code changes
- Archive outdated documentation rather than delete

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

**Backend Logic**: Add to `src/backend/` directory with appropriate module naming
**Frontend Components**: Add to `src/frontend/components/` directory
**Tests**: Add to `tests/playwright/` directory for E2E tests
**Documentation**: Add to appropriate `docs/` subdirectory by category
**Configuration**: Environment files at project root (`.env`, `.env.example`)
**Debug Information**: Logs automatically go to `logs/` directory

### Import Patterns

With the current structure, use these import patterns:

```python
# Backend modules
from src.backend.main import app
from src.backend.api_models import ChatRequest, ChatResponse
from src.backend.prompt_templates import PromptTemplateManager, PromptType
from src.backend.utils.logger import get_logger

# React/TypeScript imports (frontend)
import { useState, useEffect } from 'react';
import type { ChatResponse, PromptTemplate } from '../types';
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
# Run all Playwright E2E tests (from project root)
npm run test:playwright

# Run specific test categories
npm run test:playwright -- test-b001-market-status.spec.ts
npm run test:playwright -- test-b00*.spec.ts

# Run tests with browser visible (debugging)
npm run test:playwright:headed

# One-click app startup for testing
npm run start:app
```

### Code Organization Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Testability**: All modules are designed to be easily testable in isolation
3. **Maintainability**: Clear organization makes finding and updating code straightforward
4. **Scalability**: Structure supports growth without major reorganization
5. **Documentation**: Everything is documented for future developers

## Migration Notes

### Current Architecture

The project uses modern architecture with:

- **Backend**: FastAPI + OpenAI Agents SDK + Polygon.io MCP server
- **Frontend**: React 18.2+ with TypeScript and Vite
- **Testing**: Playwright E2E test suite (B001-B016)
- **Development**: One-click startup with `npm run start:app`

### Import Guidelines

Use these patterns for the current structure:

```python
# Backend (Python)
from src.backend.main import app
from src.backend.prompt_templates import PromptTemplateManager

# Frontend (TypeScript)
import type { ChatResponse } from '../types';
import { useChatAPI } from '../hooks/useChatAPI';
```

## Future Considerations

### Planned Enhancements

- **Enhanced MCP Integration**: Additional MCP servers for more data sources
- **Advanced Analytics**: Enhanced financial analysis capabilities
- **Mobile App**: React Native mobile application
- **Performance Optimization**: Caching and response time improvements

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