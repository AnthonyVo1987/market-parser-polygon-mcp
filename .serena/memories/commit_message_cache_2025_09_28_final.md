feat: implement official OpenAI token counting with comprehensive code improvements

- Replace custom token counting with official OpenAI Agents SDK method (result.context_wrapper.usage)
- Enable include_usage=True in ModelSettings for official token tracking
- Create shared token_utils.py utility to eliminate code duplication between CLI and API
- Remove old custom token extraction logic from cli.py and chat.py
- Update response_utils.py to display official SDK token data in footer
- Remove list_universal_snapshots tool from agent instructions (confusing/incorrect usage)
- Optimize tool set to 9 tools with clear selection guidance
- Fix all linting issues: 9.99/10 Python score, proper type annotations
- Apply black/isort formatting and create shared utilities for DRY principle
- Add comprehensive Serena memories for token counting and tool optimization
- Validate with 100% test success rate (7/7 tests passing)
- Update project documentation and architecture status

BREAKING CHANGE: AI agent now uses official OpenAI token counting method
PERFORMANCE: Improved tool selection efficiency with 9 optimized tools
TESTING: All comprehensive tests passing with official token counting validation