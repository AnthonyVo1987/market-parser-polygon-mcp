feat: Add standardized test prompts documentation system

📋 Documentation Standardization:
- Create tests/playwright/test_prompts.md as single source of truth for all test prompts
- Add 10 standardized test prompts designed for 30-60 second responses
- Include usage guidelines, performance classification, and integration notes

📚 Main Documentation Updates:
- Update CLAUDE.md, AGENTS.md, README.md with standardized prompts
- Add both individual prompts and references to test_prompts.md
- Ensure consistent formatting across all documentation files

🧪 Test Documentation Updates:
- Update tests/playwright/mcp_test_script_basic.md with prompts + reference
- Update tests/playwright/complete_test_execution_guide.md with prompts + reference  
- Update tests/playwright/UI_complete_test_execution_guide.md with prompts + reference
- Maintain dual documentation approach for quick reference and comprehensive docs

🔧 Backend Import Fixes:
- Fix ImportError handling in src/backend/main.py with proper fallback imports
- Fix ImportError handling in src/backend/api_models.py for AnalysisIntent import
- Ensure both relative and absolute imports work correctly

🎨 Linting Fixes:
- Fix markdown linting issues (H1 headings, ordered list numbering)
- Fix duplicate heading in README.md (Features → Application Features)
- Fix emphasis-as-heading issues in test documentation files

✅ Result: Standardized test prompts ensure consistent 30-60 second response times and prevent false failures from complex prompts across all Market Parser testing scenarios