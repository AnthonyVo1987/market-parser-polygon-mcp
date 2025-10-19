# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working
with code in this repository.

## Project Overview

Market Parser is a Python CLI and Gradio web interface for natural
language financial queries using the Polygon.io MCP server and OpenAI
GPT-5-nano via the OpenAI Agents SDK v0.2.9.

## Quick Start

### CLI Interface

```bash
# Standard Python entry point (recommended)
uv run main.py

# OR using installed script
uv run market-parser

# OR legacy method
uv run src/backend/cli.py

> Tesla stock analysis
KEY TAKEAWAYS
• TSLA showing bullish momentum...
```

### Gradio Web Interface

```bash
# Start Gradio server
uv run python src/backend/gradio_app.py

# Access at http://127.0.0.1:8000
```


# 🔴 CRITICAL: MANDATORY TOOL USAGE to perform all task(s) - NEVER stop using tools - continue using them until tasks completion

🔴 CRITICAL: You MUST use ALL available tools AS OFTEN AS NEEDED throughout the entire task execution. This is NOT a one-time checklist - you must continuously use tools throughout the process

## 🔴 MANDATORY: SYSTEMATIC TOOL USAGE ENFORCEMENT

**YOU MUST use Sequential-Thinking and Serena tools throughout ENTIRE implementation:**

- **START every phase** with Sequential-Thinking for systematic approach
- **Use Serena tools** for code analysis, symbol manipulation, pattern searches
- **Use Sequential-Thinking** repeatedly for complex reasoning and planning
- **Use Standard Read/Write/Edit** only when Serena doesn't support the specific operation
- **NEVER stop using advanced tools** until task completion

### Serena Tool Setup

Before using Serena tools for code analysis, get the initial instructions to understand optimal usage:

- **Primary Method (Preferred)**: Use `mcp__serena__initial_instructions` tool
- **Fallback Method**: If tool fails, use `mcp__serena__read_memory` with memory name: `serena_initial_instructions`

These instructions provide critical guidance on:

- Token-efficient code exploration using symbolic tools
- Proper file reading vs. full file scanning
- Symbol overview and targeted symbol reads
- Pattern searching for flexible searches

🔴 REMEMBER: The tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire task execution. Choose the right tool for the right operation

## 🔴 CRITICAL: MANDATORY TESTING CHECKPOINT - TWO-PHASE VALIDATION

**Testing is NOT optional - it is REQUIRED for task completion:**

### **Two-Phase Testing Workflow (MUST FOLLOW):**

1. **Code Implementation** → Create/update code
2. **Test Suite Update** → Create/update test files
3. **🔴 PHASE 1 (MANDATORY)** → RUN the test suite to generate responses
4. **🔴 PHASE 2 (MANDATORY)** → MANUALLY VERIFY each response for correctness
5. **Documentation** → Update docs with test results

### **Phase 1: Automated Response Generation**

✅ **MUST DO:**

- Execute test suite: `chmod +x test_cli_regression.sh && ./test_cli_regression.sh`
- Script generates all 39 test responses
- Script reports "X/39 COMPLETED" (responses received)
- **LIMITATION**: Script CANNOT validate response correctness
- Show Phase 1 results to user (completion counts, response times)
- Provide test report file path

### **Phase 2: MANDATORY Grep-Based Verification (EVIDENCE REQUIRED)**

Phase 2 is broken into 4 sub-phases with **MANDATORY bash commands** that MUST be executed:

#### **Phase 2a: ERROR DETECTION (MANDATORY - MUST RUN COMMANDS)**

🔴 **YOU MUST RUN these grep commands and SHOW output. Cannot proceed without evidence.**

```bash
# Command 1: Find all errors/failures
grep -i "error\|unavailable\|failed\|invalid" test-reports/test_cli_regression_loop1_*.log

# Command 2: Count 'data unavailable' errors
grep -c "data unavailable" test-reports/test_cli_regression_loop1_*.log

# Command 3: Count completed tests
grep -c "COMPLETED" test-reports/test_cli_regression_loop1_*.log
```

**Required Output**: Paste ALL grep command outputs. If you don't show grep output, Phase 2 is INCOMPLETE.

#### **Phase 2b: DOCUMENT FAILURES (MANDATORY - IF ERRORS FOUND)**

If Phase 2a grep commands found errors, create **evidence-based failure table**:

| Test # | Test Name | Line # | Error Message | Tool Call (if visible) |
|--------|-----------|--------|---------------|------------------------|
| 3 | SPY_Yesterday_Price_OHLC | 157 | data unavailable due to retrieval error | get_stock_price_history(...) |

**Required**: Show grep output + failure table with line numbers, OR confirm "0 failures found".

#### **Phase 2c: VERIFY RESPONSE CORRECTNESS (For tests without errors)**

For tests that didn't show errors in Phase 2a, verify:

1. Response directly addresses the prompt query
2. Correct ticker symbols used ($SPY, $NVDA, $WDC, $AMD, $SOUN)
3. Appropriate tool calls made (Polygon, Tradier)
4. Data formatting matches expected format (OHLC, tables, etc.)
5. No hallucinated data or made-up values
6. Options chains show Bid/Ask columns (NOT midpoint)
7. Technical analysis includes proper indicators
8. Response is complete (not truncated)

#### **Phase 2d: FINAL VERIFICATION (CHECKPOINT QUESTIONS)**

Answer ALL checkpoint questions with evidence:

1. ✅ Did you RUN the 3 mandatory grep commands in Phase 2a? **SHOW OUTPUT**
2. ✅ Did you DOCUMENT all failures found (or confirm 0 failures)? **PROVIDE TABLE OR "0 failures"**
3. ✅ Failure count from grep -c: **X failures**
4. ✅ Tests that generated responses: **X/39 COMPLETED**
5. ✅ Tests that PASSED verification (no errors): **X/39 PASSED**

**🔴 CANNOT MARK TASK COMPLETE WITHOUT:**
- Running and showing grep outputs
- Documenting failures with evidence (or confirming 0 failures)
- Providing failure count: `grep -c "data unavailable"`
- Answering all 5 checkpoint questions with evidence

❌ **NEVER DO:**

- Skip Phase 1 test execution
- Skip Phase 2 manual verification
- Claim completion without test results AND manual verification
- Mark task "done" without Phase 2 evidence
- Proceed to documentation without running both phases

### **Enforcement Rules:**

🔴 **Code without Phase 1 execution = Code NOT implemented**
🔴 **Phase 1 without Phase 2 verification = Testing INCOMPLETE**
🔴 **No manual verification = Task INCOMPLETE**
🔴 **Phase 2 verification is PROOF of correctness**
🔴 **Both phases must complete BEFORE documentation updates**

### **Key Insight:**

The script saying "39/39 COMPLETED" means "39 responses received" NOT "39 tests passed validation".

Only after Phase 2 manual verification can you claim tests passed.

### **Pattern Recognition:**

**WRONG (What NOT to do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: ./test_cli_regression.sh ✅
4. Show results: 39/39 COMPLETED ✅
5. Update documentation ✅
6. Mark task complete ❌ (NEVER performed Phase 2 verification!)
```

**CORRECT (What TO do):**

```text
1. Create 5 new tools ✅
2. Update test suite file ✅
3. RUN Phase 1: chmod +x test_cli_regression.sh && ./test_cli_regression.sh ✅
4. Show Phase 1 results: 39/39 COMPLETED ✅
5. PERFORM Phase 2: Manual verification of all 39 responses ✅
6. Answer checkpoint: "Did you verify EACH response?" YES ✅
7. Provide test report path ✅
8. Update documentation with test results ✅
9. Mark task complete ✅
```

### **When to Run Tests:**

- After creating new tools/functions
- After modifying existing code
- After updating AI agent instructions
- After changing test suite
- Before updating documentation
- Before claiming task completion

**Remember: If you haven't RUN Phase 1, PERFORMED Phase 2, and SHOWN both results, the task is NOT complete.**

## 🔴 CRITICAL: PROPER ATOMIC COMMIT WORKFLOW

### MANDATORY: Stage ONLY Immediately Before Commit

#### The Fatal Mistake: Early Staging

**NEVER stage files early during development. Staging is the LAST step before committing.**

**What happens when you stage too early:**

1. ⏰ **Time T1**: You run `git add` (files staged)
   - Staging area = snapshot at T1
2. ⏰ **Time T2-T5**: You continue working
   - Update config files
   - Run tests (generates test reports)
   - Update documentation
3. ⏰ **Time T6**: You run `git commit`
   - **Only commits the T1 snapshot**
   - **All work after T1 is MISSING**

**Result: Incomplete, broken atomic commits** ❌

### Correct Atomic Commit Workflow

**Follow this workflow EXACTLY:**

1. **DO ALL WORK FIRST** (DO NOT stage anything yet):
   - ✅ Complete ALL code changes
   - ✅ Run ALL tests and generate test reports
   - ✅ Update ALL documentation (CLAUDE.md, tech_stack.md, etc.)
   - ✅ Update ALL config files (.claude/settings.local.json, etc.)
   - ✅ Update ALL Serena memories
   - ✅ Update ALL task plans
   - ⚠️ **DO NOT RUN `git add` YET**

2. **VERIFY EVERYTHING IS COMPLETE**:

   ```bash
   git status  # Review ALL changed/new files
   git diff    # Review ALL changes
   ```

3. **STAGE EVERYTHING AT ONCE**:

   ```bash
   git add -A  # Stage ALL files in ONE command
   ```

   - ⚠️ This is the FIRST time you run `git add`

4. **VERIFY STAGING IMMEDIATELY**:

   ```bash
   git status  # Verify ALL files staged, NOTHING unstaged
   ```

5. **COMMIT IMMEDIATELY** (within 60 seconds):

   ```bash
   git commit -m "message"
   ```

6. **PUSH IMMEDIATELY**:

   ```bash
   git push
   ```

### What Belongs in an Atomic Commit

**ALL of these must be included together:**

- ✅ Code changes (backend + Gradio UI)
- ✅ Test reports (evidence of passing tests)
- ✅ Documentation updates (CLAUDE.md, README.md, etc.)
- ✅ Memory updates (.serena/memories/)
- ✅ Config changes (.claude/settings.local.json, etc.)
- ✅ Task plan updates (TODO_task_plan.md, etc.)

### ❌ NEVER DO THIS

- ❌ Stage files early during development
- ❌ Stage files "as you go"
- ❌ Run `git add` before ALL work is complete
- ❌ Delay between `git add` and `git commit`
- ❌ Commit without test reports
- ❌ Commit without documentation updates

**Reference:** See `.serena/memories/git_commit_workflow.md` for complete details.

**Enforcement:** Incomplete commits will be reverted and reworked.



## Application Startup

### Simple Command Startup

**Prerequisites:** uv, API keys in .env

**CLI Interface (recommended for automation/scripting):**
```bash
# Standard Python entry point (recommended)
uv run main.py

# Using installed console script
uv run market-parser

# Legacy method (still supported)
uv run src/backend/cli.py
```

**Gradio Web UI (recommended for interactive analysis):**
```bash
# Hot reload mode (recommended for development)
# Auto-reloads on file save, 2x-10x less CPU than standard server auto-reload
uv run gradio src/backend/gradio_app.py

# Using installed console script
uv run market-parser-gradio

# Production mode (no hot reload)
uv run python src/backend/gradio_app.py

# Access at http://127.0.0.1:8000
# PWA enabled: Install from browser address bar (Chrome/Edge)
```

## Features

### Natural Language Financial Queries

Ask questions like:

- `Tesla stock price analysis`
- `AAPL volume trends this week`
- `Show me MSFT support and resistance levels`

### Multiple Interfaces

- **Gradio Web Interface** - Python ChatInterface for financial analysis (port 8000)
- **Enhanced CLI** - Terminal interface with rich formatting

## Example Usage

### Gradio Web Interface

1. Open <http://127.0.0.1:8000>
2. Select an example or type your financial query
3. Get streaming responses with financial data and analysis
4. Examples included: Stock price queries, technical analysis, options chains, stock comparisons

**Example Response with Performance Metrics:**

```text
Market Status: CLOSED
After-hours: NO
Early-hours: NO
Exchanges: NASDAQ closed, NYSE closed, OTC closed
Server Time (UTC): 2025-10-18 01:50:12
Date: 2025-10-18

Performance Metrics:
   Response Time: 5.135s
   Tokens Used: 21,701 (Input: 21,402, Output: 299)
   Model: gpt-5-nano
```

## Architecture

- **Core**: CLI with OpenAI Agents SDK v0.2.9 and Direct Polygon/Tradier API integration
- **Web UI**: Gradio 5.49.1+ ChatInterface (port 8000) - wraps CLI core
- **Testing**: CLI regression test suite (test_cli_regression.sh - 39 tests)
- **Pattern**: CLI = core business logic, Gradio = thin wrapper (zero duplication)

## Development

### Available Commands

```bash
# CLI Interface (all methods work)
uv run main.py                    # Standard Python entry point (recommended)
uv run market-parser              # Console script
uv run src/backend/cli.py         # Legacy method

# Gradio Web UI (all methods work)
uv run gradio src/backend/gradio_app.py   # Hot reload mode (recommended for dev)
uv run market-parser-gradio               # Console script
uv run python src/backend/gradio_app.py   # Production mode (no hot reload)

# Testing
chmod +x test_cli_regression.sh && ./test_cli_regression.sh  # 39-test suite

# Code quality
npm run lint              # Python linting
npm run lint:fix          # Auto-fix with black + isort
```

### Project Structure

```text
src/
├── backend/              # All application code
│   ├── cli.py           # CLI interface (CORE BUSINESS LOGIC)
│   ├── gradio_app.py    # Gradio web UI (wraps CLI core)
│   ├── tools/           # AI agent tools (Polygon, Tradier)
│   └── services/        # Agent service layer
config/                  # Centralized configuration
│   └── app.config.json # Non-sensitive settings
```

## Troubleshooting

### Common Issues

**CLI not starting:**

```bash
# Check .env file has API keys
cat .env | grep API_KEY

# Verify dependencies
uv sync
```

**Gradio UI not loading:**

```bash
# Check port availability
netstat -tlnp | grep :8000

# Kill existing Gradio processes
pkill -f gradio_app

# Restart
uv run python src/backend/gradio_app.py
```

**API key issues:**

- Ensure both `POLYGON_API_KEY` and `OPENAI_API_KEY` are set in `.env`
- Verify API keys are valid and have sufficient credits

## Last Completed Task Summary

<!-- LAST_COMPLETED_TASK_START -->
[RESEARCH & DOCUMENTATION] Hugging Face Spaces Deployment Guide + App Preparation

**Summary:** Comprehensive research on Gradio deployment options and created beginner-friendly deployment guide for Market Parser to Hugging Face Spaces. Prepared app with necessary deployment files (app.py, requirements.txt, README.md frontmatter) and created Serena memory for future reference.

**Research Phase Completed:**
- ✅ Analyzed Gradio Share feature (temporary public URLs via share=True)
- ✅ Investigated HF Spaces deployment ecosystem (permanent free cloud hosting)
- ✅ Researched environment variables/secrets management in HF Spaces
- ✅ Studied project structure compatibility requirements
- ✅ Identified deployment challenges specific to Market Parser
- ✅ Created deployment strategy with two methods (Share vs HF Spaces)

**Deployment Methods Documented:**

**Method 1: Gradio Share (Temporary)**
- Simple `share=True` parameter in launch()
- Generates temporary public URL (expires ~72 hours)
- Requires local machine running
- Perfect for quick demos and testing
- No account or setup required

**Method 2: Hugging Face Spaces (Permanent)**
- Free permanent cloud hosting
- Professional URL: huggingface.co/spaces/username/market-parser
- Automatic builds and deployments
- App runs 24/7 without local machine
- Recommended for production and portfolio

**App Preparation Files Created:**

1. **app.py (New - HF Spaces Entry Point)**
   - Imports demo from backend.gradio_app
   - Configured for HF Spaces: server_name="0.0.0.0", server_port=7860
   - Enables HF Spaces to run app with cloud-compatible settings
   - No changes to existing gradio_app.py needed

2. **requirements.txt (New - Dependencies List)**
   - Extracted from pyproject.toml
   - 11 dependencies with exact versions
   - Includes: gradio>=5.49.1, openai-agents==0.2.9, polygon-api-client>=1.14.0
   - HF Spaces uses this for automatic environment setup

3. **README.md (Updated - HF Spaces Frontmatter)**
   - Added YAML frontmatter configuration
   - Specifies: title, emoji, colors, sdk, app_file
   - Enables HF Spaces to properly configure Space metadata
   - Existing README content preserved below frontmatter

**Comprehensive Deployment Guide Created:**
- **File:** DEPLOYMENT_GUIDE_HUGGINGFACE_SPACES.md (1,400+ lines)
- **Target Audience:** Complete beginners (zero assumed knowledge)
- **Contents:**
  - Introduction to HF Spaces and Gradio
  - Prerequisites and account setup
  - Side-by-side comparison of deployment methods
  - 4-step Gradio Share deployment
  - 8-step HF Spaces deployment with detailed instructions
  - Environment variables and secrets configuration
  - File structure and requirements
  - Build monitoring and verification steps
  - Comprehensive troubleshooting section (15+ common issues)
  - Additional resources and documentation links

**Research Task Plan Created:**
- **File:** research_task_plan.md
- **Contents:**
  - Research methodology and tools used
  - Key findings for each deployment method
  - Environment variables handling details
  - Project-specific requirements and challenges
  - Deployment comparison table
  - Research quality metrics
  - Implementation requirements

**Serena Memory Created:**
- **File:** .serena/memories/huggingface_spaces_deployment_setup_oct_2025.md
- **Contents:**
  - Deployment files documentation and purpose
  - Configuration details and explanations
  - Deployment process step-by-step
  - Security best practices
  - Compatibility checklist (all items ✅)
  - Performance considerations
  - Troubleshooting reference
  - Integration with local development
  - Related documentation links

**Key Findings:**

**Compatibility Analysis:**
- ✅ Environment variables: Already uses os.getenv() - no code changes needed
- ✅ Dependencies: All listed in requirements.txt
- ✅ Gradio app: Uses gr.ChatInterface (perfect for HF Spaces)
- ✅ Entry point: Created wrapper app.py for HF compatibility
- ✅ Original code: Completely unchanged (backward compatible)

**Deployment Challenges Identified & Solved:**
1. **File Structure Challenge** → Solution: Create wrapper app.py at root
2. **Dependencies Challenge** → Solution: Generate requirements.txt from pyproject.toml
3. **Environment Variables Challenge** → Solution: ✅ Already compatible with HF Secrets
4. **Launch Configuration Challenge** → Solution: Separate launch config in app.py

**Security Best Practices Included:**
- Never hardcode API keys in code ❌
- Use HF Spaces Secrets for sensitive values ✅
- Keep .env file local and never upload ✅
- Use Secrets (not Variables) for API keys ✅

**Files Changed/Created (4 files):**
- NEW: app.py (HF Spaces entry point)
- NEW: requirements.txt (dependency list)
- MODIFIED: README.md (added HF frontmatter)
- NEW: DEPLOYMENT_GUIDE_HUGGINGFACE_SPACES.md (comprehensive guide)
- NEW: research_task_plan.md (research documentation)
- CREATED: .serena/memories/huggingface_spaces_deployment_setup_oct_2025.md (memory file)

**Documentation Quality:**
- ✅ Beginner-friendly (zero assumed knowledge)
- ✅ All technical terms defined
- ✅ Multiple options provided (CLI vs Web UI)
- ✅ Step-by-step instructions with explanations
- ✅ "What this does" for each step
- ✅ Common errors and solutions
- ✅ Security best practices included

**Next Steps for Users:**
1. Review DEPLOYMENT_GUIDE_HUGGINGFACE_SPACES.md
2. Create HF Spaces account
3. Upload app.py, requirements.txt, README.md and src/ folder
4. Configure secrets in HF Settings (OPENAI_API_KEY, POLYGON_API_KEY, TRADIER_API_KEY)
5. Wait for build completion (~2-5 minutes)
6. Access deployed app at huggingface.co/spaces/USERNAME/market-parser

**Testing Options for Users:**
1. **Local Test:** `uv run python src/backend/gradio_app.py` (existing setup)
2. **Gradio Share Test:** Add share=True and run locally (temporary URL)
3. **HF Spaces Entry Point Test:** `python app.py` (tests HF config)

**Impact & Benefits:**
- **Zero Risk:** No changes to existing app code
- **Production Ready:** Complete deployment infrastructure
- **Beginner Friendly:** Comprehensive guide for users with zero HF knowledge
- **Professional:** HF Spaces provides production-grade hosting
- **Documentation:** Full reference material for future deployments

**Quality Metrics:**
- Research thoroughness: ✅ All aspects covered
- Accuracy: ✅ Verified from multiple authoritative sources
- Completeness: ✅ Both methods documented
- Beginner-friendliness: ✅ Zero assumed knowledge
- Actionability: ✅ Ready for immediate deployment

**Files Ready for Deployment:**
- ✅ app.py - HF Spaces entry point
- ✅ requirements.txt - Dependency list
- ✅ README.md - With HF Spaces frontmatter
- ✅ src/ folder - Existing app code (unchanged)
- ✅ DEPLOYMENT_GUIDE_HUGGINGFACE_SPACES.md - Complete guide
- ✅ .serena/memories/huggingface_spaces_deployment_setup_oct_2025.md - Reference material

**Risk Assessment:** VERY LOW (no code changes to existing functionality, pure documentation and deployment infrastructure)
<!-- LAST_COMPLETED_TASK_END -->

## claude --dangerously-skip-permissions

## uvx --from git+https://github.com/oraios/serena serena project index

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
