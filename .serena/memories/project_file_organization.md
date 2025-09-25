# Project File Organization Standards

## File Organization Rules
- **Documentation**: All `.md` files go in `docs/` folder
- **Backend Code**: All Python backend code goes in `src/backend/` folder
- **Scripts**: Analysis and utility scripts go in `scripts/` folder
- **Tests**: Test files go in `tests/` folder
- **Root Directory**: Keep clean - no scattered files

## Recent File Moves
- `PERFORMANCE_ANALYSIS_REPORT.md` → `docs/PERFORMANCE_ANALYSIS_REPORT.md`
- `optimized_agent_instructions.py` → `src/backend/optimized_agent_instructions.py`
- `performance_analysis.py` → `scripts/performance_analysis.py` (created scripts folder)

## Project Structure
```
market-parser-polygon-mcp/
├── docs/                    # All documentation
├── scripts/                 # Analysis and utility scripts
├── src/
│   ├── backend/            # Backend Python code
│   └── frontend/           # Frontend React code
├── tests/                  # Test files
└── ... (other project files)
```

## Benefits
- Clean root directory
- Logical file grouping
- Better maintainability
- Professional project structure
- Follows standard conventions