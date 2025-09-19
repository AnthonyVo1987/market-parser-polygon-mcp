# Code Style and Conventions

## Python Backend
- **Line length**: 100 characters
- **Formatter**: Black with `--line-length 100`
- **Import sorting**: isort with `--profile black --line-length 100`
- **Linting**: pylint for code quality
- **Type checking**: mypy for static type analysis
- **Docstrings**: Google style docstrings preferred
- **Naming**: snake_case for functions/variables, PascalCase for classes

## TypeScript/React Frontend
- **Formatter**: Prettier
- **Linting**: ESLint with TypeScript parser
- **Max warnings**: 150 (configured in package.json)
- **Naming**: camelCase for functions/variables, PascalCase for components
- **Components**: Function components with TypeScript interfaces
- **Hooks**: Custom hooks start with `use` prefix

## File Organization
- **Backend**: `src/backend/` with main.py, api_models.py, prompt_templates.py
- **Frontend**: `src/frontend/` with components/, hooks/, services/, utils/
- **Tests**: `/tests/playwright/` for MCP testing only
- **Configs**: Root level (.eslintrc.cjs, .prettierrc.cjs, pyproject.toml)

## Git Conventions
- **Commits**: Use conventional commits (feat:, fix:, docs:, etc.)
- **Branches**: Feature branches from master
- **PR Reviews**: Required for main branch
- **Co-authored**: Include Claude co-authorship in commits

## Environment Configuration
- **API Keys**: Store in .env (POLYGON_API_KEY, OPENAI_API_KEY)
- **Log Mode**: LOG_MODE=NONE for performance (default)
- **Fixed Ports**: Backend 8000, Frontend Dev 3000, Production 5500
- **No dynamic configuration**: Hard-coded for simplicity