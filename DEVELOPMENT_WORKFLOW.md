# Development Workflow

This document outlines the unified code quality workflow for the Market Parser project, which includes both Python and JavaScript/TypeScript components.

## Quick Start

### Install Dependencies
```bash
# Python dependencies
uv install

# JavaScript dependencies (React frontend)
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm install
cd ../..
```

### Run Quality Checks
```bash
# Run all quality checks
npm run quality-check

# Or run individual components:
npm run lint        # Lint all code
npm run format      # Format all code
npm run type-check  # Type check all code
```

## Project Structure

```
market-parser-polygon-mcp/
├── src/                           # Python source code
├── stock_data_fsm/               # FSM implementation
├── tests/                        # Python tests
├── scripts/                      # Utility scripts
├── gpt5-openai-agents-sdk-polygon-mcp/
│   ├── src/                      # OpenAI integration Python code
│   └── frontend_OpenAI/          # React TypeScript frontend
├── package.json                  # Unified npm scripts
├── pyproject.toml               # Python project config
├── .pre-commit-config.yaml      # Git hooks
└── scripts/quality_check.py     # Comprehensive quality checker
```

## Code Quality Tools

### Python Tools
- **Black**: Code formatting (line length: 100)
- **isort**: Import organization (black profile)
- **Pylint**: Static analysis and linting
- **mypy**: Type checking
- **pytest**: Testing framework

### JavaScript/TypeScript Tools
- **ESLint**: Linting with TypeScript support
- **Prettier**: Code formatting
- **TypeScript**: Type checking

## Available Commands

### Unified Commands (from project root)
```bash
npm run lint           # Lint Python + JS/TS
npm run format         # Format Python + JS/TS
npm run type-check     # Type check Python + JS/TS
npm run quality-check  # Run comprehensive quality analysis
npm run test           # Run all tests
```

### Python-Specific Commands
```bash
npm run lint:python        # Pylint + mypy
npm run format:python      # Black + isort
npm run type-check:python  # mypy only
npm run test:python        # pytest
```

### JavaScript-Specific Commands
```bash
npm run lint:js        # ESLint
npm run format:js      # Prettier
npm run type-check:js  # TypeScript compiler
npm run test:js        # Jest (if configured)
```

## Git Hooks (Pre-commit)

Automatic quality checks are enforced via pre-commit hooks:

### Setup Pre-commit Hooks
```bash
# Install pre-commit (if not already installed)
pip install pre-commit

# Install the hooks
pre-commit install
```

### What Gets Checked
- Python: Black formatting, isort, Pylint, mypy
- JavaScript/TypeScript: ESLint, Prettier, TypeScript compilation
- General: Trailing whitespace, file endings, merge conflicts

## IDE Integration

### VS Code
The `.vscode/settings.json` file is configured for:
- Auto-format on save (Black for Python, Prettier for JS/TS)
- ESLint integration with auto-fix
- Python type checking with mypy
- Import organization on save

### Recommended Extensions
- Python: `ms-python.python`
- ESLint: `dbaeumer.vscode-eslint`
- Prettier: `esbenp.prettier-vscode`
- TypeScript: Built-in VS Code support

## Quality Standards

### Python Code Standards
- Line length: 100 characters
- Import organization: Black profile with isort
- Type hints: Required for new code (mypy strict mode)
- Docstrings: Required for public functions and classes

### JavaScript/TypeScript Standards
- ESLint configuration extends `@typescript-eslint/recommended`
- Prettier formatting with consistent rules
- Strict TypeScript configuration
- React hooks rules enforced

## Development Workflow

### Before Committing
1. Run `npm run quality-check` to ensure all standards are met
2. Fix any reported issues
3. Run tests: `npm run test`
4. Commit changes (pre-commit hooks will run automatically)

### Adding New Code
1. Follow existing patterns and conventions
2. Add appropriate type hints (Python) or types (TypeScript)
3. Write tests for new functionality
4. Update documentation if needed

### Handling Quality Check Failures
1. **Formatting Issues**: Run `npm run format` to auto-fix
2. **Linting Issues**: Review and fix manually, or use IDE quick-fixes
3. **Type Issues**: Add/fix type annotations
4. **Test Failures**: Fix failing tests before committing

## Troubleshooting

### Common Issues

**Python ModuleNotFoundError**:
```bash
# Ensure you're using uv for Python dependencies
uv install
```

**ESLint not finding TypeScript files**:
```bash
# Check that you're in the correct directory
cd gpt5-openai-agents-sdk-polygon-mcp/frontend_OpenAI
npm run lint
```

**Pre-commit hooks failing**:
```bash
# Re-install hooks
pre-commit uninstall
pre-commit install

# Skip hooks temporarily (not recommended)
git commit --no-verify
```

### Performance Tips
- Use `npm run format` before `npm run lint` to fix formatting issues first
- Run `npm run type-check` separately if you only need type validation
- Use IDE integration for real-time feedback during development

## Continuous Integration

The quality checks are designed to be CI-friendly:
- Exit codes indicate success/failure
- Detailed output for debugging
- Parallel execution where possible
- Minimal dependencies (uses uv and npm)

For CI/CD pipelines, run:
```bash
npm run quality-check  # Comprehensive validation
npm run test          # Full test suite
```