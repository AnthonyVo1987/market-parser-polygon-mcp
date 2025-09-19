# New Task Details

## MANDATORY Tools Usage Guidance for all Task(s)

Prioritize using the following Tools FIRST in any particular order to match the scope & complexity of the task(s), before trying to use standard non-prioritized tools:

- **Serena Tools**: Use for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
- **Sequential-Thinking Tools**: Use for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
- **Context7 Tools**: Use for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups
- **Playwright Tools**: Use for Testing with Browser automation for React GUI & App Validation
- **Filesystem Tools**: Use for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
- **Standard Read/Write/Edit Tools**: Use for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management

- **If more proper Tool Usage details are needed, refer to & read relevant Tools Usage Guides as needed in 'docs/MCP_Tools_Usage_Guide'**

## Task Description

feat: Add AI Model Selector Drop Down Menu in Debug Panel & Set Default Model to 'gpt-5-nano'

# Plan: Add AI Model Selector Dropdown Menu in Debug Panel

## Overview

Implement a new AI Model Selector dropdown menu in the React frontend Debug Panel that allows users to dynamically switch between different OpenAI models for testing and comparison. Set the new default model to 'gpt-5-nano' (from current 'gpt-5-mini') and update all AI responses to include the model name at the end.

## Task 1: Backend Implementation - Model Configuration & API Updates

### 1.1 Update Backend Model Configuration

- **File:** `src/backend/main.py`
  - Modify `Settings` class (lines 96-119):
    - Change default `openai_model` from `"gpt-5-mini"` to `"gpt-5-nano"` (line 113)
    - Add supported models list: `["gpt-5-nano", "gpt-5-mini", "gpt-5-turbo"]`
  - Update `process_financial_query` function (lines 405-524):
    - Accept optional `model` parameter
    - Pass `model` to `OpenAIResponsesModel` instantiation (line 510)
    - Append model name to response: `\n\n[{model_name}]`

### 1.2 Update API Models

- **File:** `src/backend/api_models.py`
  - Add to `ChatRequest` class (lines 25-43):
    - New field: `model: Optional[str] = Field(default="gpt-5-nano", description="OpenAI model to use")`
  - Add to `ChatAnalysisRequest` class (lines 107-126):
    - New field: `model: Optional[str] = Field(default="gpt-5-nano", description="OpenAI model to use")`
  - Add to `ButtonAnalysisRequest` class (lines 130-147):
    - New field: `model: Optional[str] = Field(default="gpt-5-nano", description="OpenAI model to use")`

### 1.3 Update API Endpoints

- **File:** `src/backend/main.py`
  - Update `/chat` endpoint (lines 711-784):
    - Extract `model` from request
    - Pass `model` to `process_financial_query`
  - Update `/api/v1/analysis/{analysis_type}` endpoint (lines 859-942):
    - Extract `model` from request
    - Pass `model` to `process_financial_query`
  - Update `/api/v1/analysis/chat` endpoint (lines 949-987):
    - Extract `model` from request
    - Pass `model` to `process_financial_query`

### 1.4 Add Model Validation

- **File:** `src/backend/main.py`
  - Add model validation function to ensure only supported models are used
  - Return HTTP 400 if invalid model is specified

## Task 2: Frontend Implementation - Debug Panel Model Selector

### 2.1 Update Debug Panel Component

- **File:** `src/frontend/components/DebugPanel.tsx`
  - Add new props to `DebugPanelProps` interface (lines 8-15):
    - `selectedModel: string`
    - `onModelChange: (model: string) => void`
    - `availableModels: string[]`
  - Add dropdown UI in the collapsible content section (after line 171):

    ```html
    <div className="debug-metric">
      <span className="debug-label">AI Model:</span>
      <select
        className="model-selector"
        value={selectedModel}
        onChange={(e) => onModelChange(e.target.value)}
        aria-label="Select AI model"
      >
        {availableModels.map(model => (
          <option key={model} value={model}>{model}</option>
        ))}
      </select>
    </div>
    ```

### 2.2 Update Debug Panel Styles

- **File:** `src/frontend/styles/DebugPanel.css`
  - Add styling for the model selector dropdown:

    ```css
    .model-selector {
      background: rgba(30, 30, 40, 0.7);
      border: 1px solid rgba(139, 92, 246, 0.3);
      color: #e0e0ff;
      padding: 0.5rem;
      border-radius: 4px;
      font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
      font-size: 0.875rem;
    }
    ```

### 2.3 Update ChatInterface Component

- **File:** `src/frontend/components/ChatInterface_OpenAI.tsx`
  - Add state for model selection:

    ```typescript
    const [selectedModel, setSelectedModel] = useState('gpt-5-nano');
    const availableModels = ['gpt-5-nano', 'gpt-5-mini', 'gpt-5-turbo'];
    ```

  - Update `handleSendMessage` function to include model in API requests
  - Pass model props to `DebugPanel` component (lines 473-478):

    ```typescript
    <DebugPanel
      latestResponseTime={latestResponseTime}
      className='main-debug-panel'
      onDebugAction={handleDebugAction}
      selectedModel={selectedModel}
      onModelChange={setSelectedModel}
      availableModels={availableModels}
    />
    ```

### 2.4 Update API Service

- **File:** `src/frontend/services/api.ts`
  - Update API request functions to include model parameter:
    - `sendChatMessage`: Add `model` to request body
    - `getButtonAnalysis`: Add `model` to request body

## Task 3: Documentation Updates

### 3.1 Update `CLAUDE.md`

- Change all references from `"gpt-5-mini"` to `"gpt-5-nano"`
- Add section about the new Model Selector feature
- Update environment configuration section

### 3.2 Update `README.md`

- Change all references from `"gpt-5-mini"` to `"gpt-5-nano"`
- Add feature description for Model Selector
- Update architecture section

### 3.3 Update `.env.example`

- Add comment about model configuration
- Update any example references to use `gpt-5-nano`

### 3.4 Update Other Documentation

- Search and replace all instances of `"gpt-5-mini"` with `"gpt-5-nano"` in:
  - Test documentation
  - API documentation
  - Development guides

## Task 4: Testing & Validation

### 4.1 Manual Testing Plan

1. Start application with `./start-app.sh`
2. Verify default model is "gpt-5-nano"
3. Test model switching:
    - Select each model from dropdown
    - Send test queries
    - Verify responses end with correct model name
4. Test all three core validations:
    - Market Status query
    - NVDA ticker analysis
    - Stock Snapshot button

### 4.2 Playwright MCP Testing

- Execute test plan from `/tests/playwright/mcp_test_script_basic.md`
- Verify model selector is accessible
- Test model switching functionality
- Confirm responses include model names

## Task 5: Code Review & Finalization

### 5.1 Code Review

- Use Serena Tools for comprehensive code analysis
- Use Sequential-Thinking for systematic review
- Verify all changes follow React 18.2+ best practices
- Ensure TypeScript types are properly defined

### 5.2 Git Commit Preparation

- Stage all modified files
- Create comprehensive commit message
- Update `CLAUDE.md` with task summary

### 5.3 Final Verification

- Run `git status` to confirm all changes staged
- Commit with message: "feat: Add AI Model Selector dropdown in Debug Panel & set default to gpt-5-nano"
- Push to repository

## Implementation Order

1. Backend changes first (model configuration, API updates)
2. Frontend changes (Debug Panel, ChatInterface)
3. Documentation updates
4. Testing and validation
5. Code review and commit

## Key Considerations

- Maintain backwards compatibility during transition
- Ensure model name is appended to ALL responses
- Preserve existing functionality while adding new features
- Follow prototyping principles - keep it simple and functional

We will perform a Checkpoint Review & Commit of the current implemntation to save our Progress now.  A new task will be generated later to specify Testing & Validation details for testing out the new feature.

# Final Task 1: Review/Fix Loop

- Use Serena Tools, `mcp__sequential-thinking__sequentialthinking` tool for systematic approach & Use `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` to perform research to have the most update to date best, robust, modern practices, latest documentation, latest framework(s) notes to Perform comprehensive review
- Optional `mcp__filesystem__*` tools for EFFICIENT file operations and examination (Multi-file operations (3+ files))
- Use standard Read/Write/Edit tools for single-file operations
- Continue review/fix cycle until achieving PASSING code review status

# Final Task 2: Task Summary Updates for CLAUDE.md

- Create token & context efficient git commit message of all the changes to prepare for the final commit task(s)
- Update CLAUDE.md "Last Completed Task Summary" section with the VERBATIM COPY of the token & context efficient git commit message between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- This ensures that the git commit message is cached for token & context efficient in order to update CLAUDE.md with, preventing the need to waste tokens by having to regenerate similiar task completion summaries

# Final Task 3: Atomic Git Commit & Push

**MANDATORY PRE-COMMIT CHECKLIST (CRITICAL FOR SUCCESS):**

1. Run `git status` to identify ALL modified files
2. Run `git add .` to stage ALL changes (never commit without staging all)
3. Run `git status` again to verify ALL files are staged
4. Verify specialist work inclusion: ALL frontend, backend, test, and config changes MUST be staged
5. Only then execute `git commit` with comprehensive message

**AGENT PROCESS REQUIREMENTS:**

- Code reviewer MUST verify all specialist work is staged before commit
- NEVER commit without comprehensive staging verification
- Implement explicit git status checks at each phase
- Failure to include all modified files is a CRITICAL VIOLATION

**Commit Requirements:**

- Create single atomic git commit containing ALL : CLAUDE.md, code files, documentation changes, 1x test report if it exist, NO TEST OUTPUT RESULTS\DATA\SCREENSHOTS\VIDEOS ETC
- **CRITICAL**: DO NOT INCLUDE & COMMIT testing artifacts & testing outputs
- the end result of the commit will be NO FILES LEFT CHANGED OR UNSTAGED - No lingering file left uncommitted whatsoever
- git Push commit to repository using provided personal access token
- **CRITICAL**: Must git push to complete the workflow - git commit without git push is incomplete

# Final Task 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly git committed and git pushed

**Key Requirements:**

## Requirements

## Expected Outcome*

## Additional Context

## MANDATORY Tools Usage Guidance for all Task(s)

Prioritize using the following Tools FIRST in any particular order to match the scope & complexity of the task(s), before trying to use standard non-prioritized tools:

- **Serena Tools**: Use for Advanced code analysis, symbol manipulation, pattern search with context, and memory management for complex financial algorithm development and refactoring; Use standard Read/Write/Edit for simple file content modifications
- **Sequential-Thinking Tools**: Use for Investigation, Planning, Scoping, Researching, Complex problem analysis (max 8 thoughts)
- **Context7 Tools**: Use for Researching Best, Robust, & Up to Date Implementation Practices & Library documentation lookups
- **Playwright Tools**: Use for Testing with Browser automation for React GUI & App Validation
- **Filesystem Tools**: Use for Batch File operations (3+), file discovery, configuration management, metadata analysis, project organization, project structure analysis, and documentation generation for comprehensive project management; Use standard Read/Write/Edit for single-file content modifications
- **Standard Read/Write/Edit Tools**: Use for single-file content modifications, simple edits, and direct file operations; use Serena/Filesystem for complex analysis, batch operations, and project management

- **If more proper Tool Usage details are needed, refer to & read relevant Tools Usage Guides as needed in 'docs/MCP_Tools_Usage_Guide'**
