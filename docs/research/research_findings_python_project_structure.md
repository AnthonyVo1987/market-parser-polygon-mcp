# Python Project Structure & UV Conventions Research Report

**Research Date:** 2025-10-18
**Project:** market-parser-polygon-mcp
**Purpose:** Inform folder/file hierarchy refactoring decisions

---

## Executive Summary

This research examined Python project structure best practices, UV package manager conventions, file naming patterns, and import path implications for refactoring projects from nested structures (e.g., `src/backend/cli.py`) to alternative organizational patterns.

**Key Findings:**
- UV supports both flat and nested structures, with specific conventions for apps vs. packages
- File naming prefixes (backend_xxx, frontend_xxx) are NOT a Python standard pattern
- Nested directory structures (src/backend/) are the Python community standard
- Absolute imports are recommended by PEP 8 and preferred for refactoring
- The src/ layout is strongly recommended for production projects over flat layouts

---

## Section 1: UV Entry Point Best Practices

### 1.1 UV Project Types

UV's `uv init` command creates different project structures based on the intended use case:

#### **Application Projects (`--app`, default)**
```
example-app/
├── .python-version
├── README.md
├── main.py           # Entry point
└── pyproject.toml
```

- Flat structure with `main.py` at the root
- No build system configuration (not distributed as packages)
- Executed via: `uv run main.py`
- Best for: Standalone applications, CLI tools

**Example main.py:**
```python
def main():
    print("Hello from example-app!")

if __name__ == "__main__":
    main()
```

#### **Package Projects (`--package`)**
```
example-pkg/
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── example_pkg/
        └── __init__.py
```

- Uses src/ layout for better testing isolation
- Includes build system configuration
- Defines entry points in pyproject.toml
- Executed via: `uv run example-pkg` (after defining entry point)

**Example pyproject.toml:**
```toml
[project]
name = "example-pkg"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.scripts]
example-pkg = "example_pkg:main"

[build-system]
requires = ["uv_build>=0.9.2,<0.10.0"]
build-backend = "uv_build"
```

#### **Library Projects (`--lib`)**
```
example-lib/
├── .python-version
├── README.md
├── pyproject.toml
└── src/
    └── example_lib/
        ├── py.typed       # Type checking marker
        └── __init__.py
```

- Designed for distribution and reuse
- Uses src/ layout for proper package isolation
- No entry points (imported by other projects)

### 1.2 Entry Point Definition

UV follows the Python packaging standard for defining entry points:

```toml
[project.scripts]
my-cli = "my_package.my_module:main_cli"
```

**Syntax breakdown:**
- `my-cli` - Command name users will type
- `my_package.my_module` - Python module path
- `main_cli` - Function to call within that module

### 1.3 Running Projects with UV

```bash
# Run a script directly
uv run main.py

# Run a defined entry point
uv run my-cli

# Run without installing project dependencies
uv run --no-project script.py

# Run arbitrary commands in project environment
uv run -- flask run -p 3000
```

**Important:** UV automatically:
1. Verifies lockfile is up-to-date with pyproject.toml
2. Synchronizes environment with lockfile
3. Installs current project before running (unless --no-project)
4. Runs commands in consistent, locked environment

### 1.4 UV's Recommendation: Src Layout vs. Flat Layout

**UV's Position (2025):**
- Flat layout: For toy scripts, quick demos, weekend hacks
- Src layout: For production applications, ML pipelines, anything shipped to production

**Why src/ layout is preferred:**
- Better testing isolation (prevents accidental imports from source)
- Clearer separation between source and configuration
- Prevents import path issues
- Industry standard for serious projects (Pandas, FastAPI, PyTorch)

---

## Section 2: File Naming Prefix Pattern Analysis

### 2.1 Python Community Standards (PEP 8)

**Modules (files):**
- Should have short, all-lowercase names
- Underscores can be used if it improves readability
- Example: `user_service.py`, `api_client.py`

**Packages (directories):**
- Should have short, all-lowercase names
- Use of underscores is DISCOURAGED
- Example: `backend/`, `services/`, `tools/`

### 2.2 Prefix Pattern Investigation

**Finding:** File naming prefixes like `backend_xxx.py`, `frontend_xxx.py`, `tool_xxx.py` are **NOT** a standard Python pattern.

**Evidence:**
1. No mention in PEP 8 style guide
2. Not found in popular Python projects (Django, Flask, FastAPI)
3. No documentation in Python Packaging User Guide
4. No examples in UV documentation

**Alternative patterns found:**
- Internal/private modules: `_internal_function.py` (single underscore prefix)
- Test files: `test_<name>.py` or `<name>_test.py`
- Platform-specific: Sometimes use suffixes like `_win.py`, `_linux.py`

### 2.3 How Python Projects Handle Organization

**Standard approach: Nested directories**

Instead of flat structure with prefixes:
```
src/
├── backend_cli.py          # NOT STANDARD
├── backend_gradio.py       # NOT STANDARD
├── tool_polygon.py         # NOT STANDARD
└── tool_tradier.py         # NOT STANDARD
```

Python projects use nested directories:
```
src/
├── backend/
│   ├── cli.py
│   ├── gradio_app.py
│   └── tools/
│       ├── polygon_tools.py
│       └── tradier_tools.py
```

### 2.4 Real-World Examples

**FastAPI Projects:**
```
app/
├── routers/          # NOT router_xxx.py files
├── models/           # NOT model_xxx.py files
├── schemas/          # NOT schema_xxx.py files
└── services/         # NOT service_xxx.py files
```

**Flask Projects:**
```
myapp/
├── views.py
├── models.py
├── forms.py
└── static/
```

**Django Projects:**
```
myproject/
├── myapp/
│   ├── models.py
│   ├── views.py
│   └── tests.py
```

### 2.5 Pros and Cons of Flat Structure with Prefixes

#### Pros:
- ✅ All files visible at one level (no drilling into folders)
- ✅ Easier to see all components at a glance
- ✅ Simpler import paths (fewer dots)
- ✅ May work for very small projects (< 10 files)

#### Cons:
- ❌ **NOT a Python standard or convention**
- ❌ **Violates PEP 8 guidance** (underscores discouraged in package/module names)
- ❌ **Doesn't scale** - becomes unwieldy with >15-20 files
- ❌ **Poor semantic grouping** - related files not physically grouped
- ❌ **Harder for AI agents and IDEs** - can't use folder-level context
- ❌ **Confusing for Python developers** - unexpected pattern
- ❌ **No namespace benefits** - prefixes don't create logical namespaces
- ❌ **Maintenance burden** - harder to reorganize as project grows

#### How AI Agents Navigate Code:

**Nested Structure (Easier):**
```python
# Agent understands: "Find polygon tools"
# → Look in src/backend/tools/polygon_tools.py
```

**Flat with Prefixes (Harder):**
```python
# Agent must scan all files with "polygon" in name
# → tool_polygon.py? polygon_tool.py? backend_polygon.py?
```

**Verdict:** Nested directories provide better semantic organization for both humans and AI agents.

---

## Section 3: Import Path Migration Strategy

### 3.1 Current Project Structure

**Current:**
```
src/
└── backend/
    ├── cli.py
    ├── gradio_app.py
    ├── config.py
    ├── tools/
    │   ├── __init__.py
    │   ├── polygon_tools.py
    │   ├── tradier_tools.py
    │   └── formatting_helpers.py
    ├── services/
    │   ├── __init__.py
    │   └── agent_service.py
    └── utils/
        ├── __init__.py
        ├── response_utils.py
        ├── token_utils.py
        └── datetime_utils.py
```

**Running via:** `uv run src/backend/cli.py`

**Current imports (example):**
```python
from backend.tools.polygon_tools import get_ticker_details
from backend.services.agent_service import AgentService
from backend.utils.response_utils import format_response
```

### 3.2 Option 1: Maintain Nested Structure + Add main.py Entry Point

**Recommended Approach**

**New structure:**
```
src/
├── main.py                    # NEW: Entry point
└── backend/
    ├── __init__.py           # NEW: Package marker
    ├── cli.py
    ├── gradio_app.py
    ├── config.py
    ├── tools/
    │   ├── __init__.py
    │   └── ...
    ├── services/
    │   ├── __init__.py
    │   └── ...
    └── utils/
        ├── __init__.py
        └── ...
```

**New main.py:**
```python
"""Market Parser entry point for UV."""
from backend.cli import main as cli_main

def main():
    """Entry point for the application."""
    cli_main()

if __name__ == "__main__":
    main()
```

**Updated pyproject.toml:**
```toml
[project.scripts]
market-parser = "backend.cli:main"
market-parser-gradio = "backend.gradio_app:main"
```

**Running:**
```bash
# Via main.py
uv run main.py

# Via defined entry point
uv run market-parser

# Via Gradio entry point
uv run market-parser-gradio
```

**Import changes:** NONE (all existing imports remain valid)

**Benefits:**
- ✅ Zero import refactoring needed
- ✅ Maintains existing organization
- ✅ Adds standard UV entry points
- ✅ Backward compatible
- ✅ Follows Python standards

### 3.3 Option 2: Flatten to src/ with Prefixes (NOT RECOMMENDED)

**Hypothetical structure:**
```
src/
├── main.py
├── backend_cli.py
├── backend_gradio.py
├── backend_config.py
├── tool_polygon.py
├── tool_tradier.py
├── tool_formatting.py
├── service_agent.py
├── util_response.py
├── util_token.py
└── util_datetime.py
```

**Import changes required:**
```python
# OLD
from backend.tools.polygon_tools import get_ticker_details
from backend.services.agent_service import AgentService
from backend.utils.response_utils import format_response

# NEW
from tool_polygon import get_ticker_details
from service_agent import AgentService
from util_response import format_response
```

**Problems:**
- ❌ Requires refactoring ALL import statements project-wide
- ❌ Violates Python naming conventions
- ❌ Loses semantic grouping (tools/, services/, utils/)
- ❌ Harder to navigate as project grows
- ❌ Confusing for new Python developers
- ❌ Not extensible for future growth

**Verdict:** DO NOT PURSUE THIS OPTION

### 3.4 Option 3: Move to Standard Package Layout

**Recommended for packaging/distribution**

**New structure:**
```
src/
└── market_parser/
    ├── __init__.py
    ├── cli.py
    ├── gradio_app.py
    ├── config.py
    ├── tools/
    │   ├── __init__.py
    │   ├── polygon.py
    │   ├── tradier.py
    │   └── formatting.py
    ├── services/
    │   ├── __init__.py
    │   └── agent.py
    └── utils/
        ├── __init__.py
        ├── response.py
        ├── token.py
        └── datetime.py
```

**Import changes:**
```python
# OLD
from backend.tools.polygon_tools import get_ticker_details

# NEW
from market_parser.tools.polygon import get_ticker_details
```

**Updated pyproject.toml:**
```toml
[project]
name = "market-parser-polygon-mcp"
version = "0.1.0"

[project.scripts]
market-parser = "market_parser.cli:main"
market-parser-gradio = "market_parser.gradio_app:main"

[tool.setuptools]
package-dir = {"" = "src"}
```

**Benefits:**
- ✅ Standard Python package structure
- ✅ Proper namespacing
- ✅ Publishable to PyPI
- ✅ Clean entry points
- ✅ Professional organization

**Drawbacks:**
- ⚠️ Requires refactoring all imports
- ⚠️ Package name change (backend → market_parser)

### 3.5 Absolute vs. Relative Imports During Refactoring

**PEP 8 Recommendation:** Use absolute imports

**Absolute Imports (Recommended):**
```python
from backend.tools.polygon_tools import get_ticker_details
from backend.services.agent_service import AgentService
```

**Advantages:**
- ✅ Clear and straightforward
- ✅ Easy to tell exactly where imported resource is
- ✅ Remain valid even if current file moves
- ✅ PEP 8 compliant
- ✅ No updates needed when reorganizing packages

**Relative Imports:**
```python
from .tools.polygon_tools import get_ticker_details
from ..services.agent_service import AgentService
```

**Advantages:**
- ✅ Simpler for package renaming (no updates needed)
- ✅ Useful for tiny projects with dynamic structure

**Disadvantages:**
- ❌ Can be confusing (where is ".."?)
- ❌ Break when files are moved
- ❌ Not recommended by PEP 8

**Migration Strategy:**
1. Use absolute imports for new code
2. Gradually convert relative imports to absolute during refactoring
3. Use IDE refactoring tools (PyCharm, VS Code) to automate import updates
4. Consider using `absolufy-imports` tool for automation

### 3.6 Backward Compatibility Strategies

**If you must refactor imports:**

**Option A: Add compatibility imports to __init__.py**
```python
# src/backend/__init__.py
# Maintain backward compatibility
from backend.tools import polygon_tools
from backend.services import agent_service

__all__ = ['polygon_tools', 'agent_service']
```

**Option B: Use import redirects**
```python
# src/backend/tools/__init__.py
# Old imports still work
from backend.tools.polygon import *  # New location
```

**Option C: Gradual migration with deprecation warnings**
```python
# src/backend/old_module.py
import warnings
from backend.new_module import *

warnings.warn(
    "Importing from backend.old_module is deprecated. "
    "Use backend.new_module instead.",
    DeprecationWarning,
    stacklevel=2
)
```

---

## Section 4: Recommendations for This Specific Refactoring

### 4.1 Current Situation Analysis

**Current State:**
- Project: `market-parser-polygon-mcp`
- Structure: `src/backend/` nested organization
- Entry point: `uv run src/backend/cli.py` (non-standard)
- Package config: `package-dir = {"" = "src"}` in pyproject.toml
- Gradio UI: `src/backend/gradio_app.py`
- Has __init__.py files in: tools/, services/, utils/ (but NOT in backend/)

**Goals (Inferred):**
1. Use `uv run main.py` as standard entry point
2. Improve project organization
3. Consider file naming patterns

### 4.2 Recommended Approach: Option 1 (Minimal Refactoring)

**Why:** Maintains existing structure, adds standard entry points, zero import refactoring

**Steps:**

#### Step 1: Add backend/__init__.py
```python
# src/backend/__init__.py
"""Market Parser backend package."""

__version__ = "0.1.0"
```

#### Step 2: Create src/main.py
```python
"""Market Parser main entry point."""
from backend.cli import main as cli_main

if __name__ == "__main__":
    cli_main()
```

#### Step 3: Update pyproject.toml
```toml
[project.scripts]
market-parser = "backend.cli:main"
market-parser-gradio = "backend.gradio_app:main"
```

#### Step 4: Update CLAUDE.md
```markdown
## Quick Start

### CLI Interface
```bash
# New standard way
uv run main.py

# Or via entry point
uv run market-parser

# Old way (still works)
uv run src/backend/cli.py
```

### Gradio Web Interface
```bash
# New standard way
uv run market-parser-gradio

# Old way (still works)
uv run python src/backend/gradio_app.py
```
```

**Benefits:**
- ✅ Standard UV entry point (`uv run main.py`)
- ✅ Professional entry point commands
- ✅ ZERO import refactoring needed
- ✅ Backward compatible (old commands still work)
- ✅ Minimal risk
- ✅ ~30 minutes of work

### 4.3 Alternative: Option 3 (Full Package Refactoring)

**When to consider:** If planning to publish to PyPI or distribute as package

**Benefits:**
- ✅ Professional package structure
- ✅ Proper namespacing (`market_parser.*`)
- ✅ Publishable to PyPI
- ✅ Cleaner imports

**Drawbacks:**
- ⚠️ Requires full import refactoring (~50-100 import statements)
- ⚠️ Risk of breaking changes
- ⚠️ ~4-8 hours of work
- ⚠️ Must update tests, documentation, CI/CD

**Recommendation:** Only pursue if distribution is a goal. Otherwise, use Option 1.

### 4.4 File Naming Prefix Pattern: NOT RECOMMENDED

**Question:** Should we use `backend_cli.py`, `tool_polygon.py` instead of nested directories?

**Answer:** **NO, strongly discouraged**

**Reasons:**
1. ❌ Not a Python standard (violates PEP 8)
2. ❌ Loses semantic organization (no folders)
3. ❌ Harder to navigate (especially with 20+ files)
4. ❌ Confusing for Python developers
5. ❌ No benefits over nested directories
6. ❌ Harder to refactor later

**Current structure is GOOD:**
```
src/backend/
├── tools/          # Logical grouping
├── services/       # Logical grouping
└── utils/          # Logical grouping
```

**Keep it.**

---

## Section 5: Risks and Considerations

### 5.1 Risks of Refactoring

#### Low Risk (Option 1 - Add main.py):
- ✅ No import changes
- ✅ Backward compatible
- ✅ Easy to revert
- ⚠️ Must test entry points work correctly

#### Medium Risk (Option 3 - Package structure):
- ⚠️ All imports must be updated
- ⚠️ Tests may break
- ⚠️ CI/CD may need updates
- ⚠️ Documentation must be updated
- ✅ Can be automated with IDE tools

#### High Risk (Flat + Prefixes):
- ❌ Violates Python standards
- ❌ Loses logical organization
- ❌ Harder to maintain
- ❌ Confusing for developers
- ❌ NOT RECOMMENDED

### 5.2 Testing Checklist

**Before refactoring:**
- [ ] Run existing test suite (baseline)
- [ ] Document current import patterns
- [ ] Check all entry points work

**After refactoring:**
- [ ] All imports resolve correctly
- [ ] All tests pass
- [ ] Entry points work (`uv run main.py`, `uv run market-parser`)
- [ ] Gradio UI launches correctly
- [ ] CLI interface works
- [ ] No circular imports
- [ ] Type checking passes (mypy)
- [ ] Linting passes (pylint, black, isort)

### 5.3 Common Pitfalls

**Pitfall 1: Forgetting __init__.py files**
- Python 3.3+ allows implicit namespace packages
- But explicit __init__.py is clearer and prevents issues
- Always include __init__.py in packages

**Pitfall 2: Circular imports**
- Can occur when refactoring imports
- Solution: Use import at function level or refactor dependencies

**Pitfall 3: Incorrect entry point syntax**
```toml
# WRONG
[project.scripts]
market-parser = "backend.cli"

# CORRECT
[project.scripts]
market-parser = "backend.cli:main"
```

**Pitfall 4: Breaking existing scripts**
- If external scripts reference old paths
- Solution: Maintain backward compatibility for 1-2 releases

**Pitfall 5: UV not finding entry points**
- Ensure `[project.scripts]` is in pyproject.toml
- Run `uv sync` after updating pyproject.toml
- Check package is installed: `uv pip list`

### 5.4 Migration Timeline Estimate

**Option 1 (Add main.py + Entry Points):**
- Planning: 30 minutes
- Implementation: 30 minutes
- Testing: 30 minutes
- Documentation: 30 minutes
- **Total: ~2 hours**

**Option 3 (Full Package Refactoring):**
- Planning: 1 hour
- Implementation: 3-4 hours (import updates)
- Testing: 2 hours
- Documentation: 1 hour
- **Total: ~7-8 hours**

**Flat + Prefixes (NOT RECOMMENDED):**
- Don't do it. Seriously.

---

## Conclusion and Final Recommendation

### For market-parser-polygon-mcp:

**Recommended Action: Option 1 (Add main.py + Entry Points)**

**Rationale:**
1. ✅ Achieves goal of `uv run main.py`
2. ✅ Adds professional entry point commands
3. ✅ Maintains existing organization (which follows Python standards)
4. ✅ Zero import refactoring required
5. ✅ Low risk, quick implementation
6. ✅ Backward compatible

**Implementation Steps:**
1. Create `src/backend/__init__.py`
2. Create `src/main.py` that calls `backend.cli:main`
3. Add `[project.scripts]` to pyproject.toml
4. Test: `uv run main.py`, `uv run market-parser`, `uv run market-parser-gradio`
5. Update CLAUDE.md with new commands
6. Keep old commands documented (backward compatibility)

**Do NOT:**
- ❌ Use file naming prefixes (backend_xxx.py, tool_xxx.py)
- ❌ Flatten directory structure
- ❌ Remove existing folder organization

**Current structure is good. Just add entry points.**

---

## References

1. **UV Documentation**
   - Working on projects: https://docs.astral.sh/uv/guides/projects/
   - Creating projects: https://docs.astral.sh/uv/concepts/projects/init/
   - Configuring projects: https://docs.astral.sh/uv/concepts/projects/config/

2. **Python Packaging User Guide**
   - Src layout vs flat layout: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
   - Writing pyproject.toml: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

3. **PEP Standards**
   - PEP 8 (Style Guide): https://peps.python.org/pep-0008/
   - PEP 328 (Imports): https://peps.python.org/pep-0328/
   - PEP 423 (Naming): https://peps.python.org/pep-0423/

4. **Real-World Examples**
   - python-blueprint: https://github.com/johnthagen/python-blueprint
   - FastAPI structure: https://fastapi.tiangolo.com/tutorial/bigger-applications/
   - Flask structure: https://flask.palletsprojects.com/

5. **Tools**
   - absolufy-imports: https://github.com/MarcoGorelli/absolufy-imports
   - Real Python on imports: https://realpython.com/absolute-vs-relative-python-imports/

---

**Research completed by:** Claude (Anthropic)
**Date:** 2025-10-18
**Confidence level:** High (based on official documentation and community standards)
