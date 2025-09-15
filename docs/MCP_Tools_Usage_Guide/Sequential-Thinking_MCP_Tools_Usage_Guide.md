# Sequential-Thinking MCP Tool Usage Guide for Market Parser

**Target Audience:** AI Coding Agents working on Market Parser financial application

**Application Context:** FastAPI backend + React frontend + Polygon.io financial data + OpenAI
GPT-5-mini via OpenAI Agents SDK

## Tool Overview

Sequential-thinking tool enables systematic, multi-step problem solving with structured thought
processes. Use for complex tasks requiring logical breakdown and iterative reasoning.

**Primary Function:** `mcp__sequential-thinking__sequentialthinking`

## Correct Usage Scenarios

### ✅ WHEN TO USE

1. **Complex Backend API Integration**
   - Adding new Polygon.io endpoints to FastAPI
   - Implementing multi-step financial calculations
   - Debugging MCP server connectivity issues

2. **Multi-Component Frontend Development**
   - Building responsive React components with complex state
   - Integrating new chat features with existing UI
   - Implementing cross-platform optimizations

3. **Full-Stack Feature Implementation**
   - End-to-end financial analysis features
   - New emoji-based sentiment indicators
   - Performance optimization across backend and frontend

4. **Architecture Decisions**
   - Major structural changes to FastAPI routes
   - React component refactoring decisions
   - Database schema modifications

5. **Bug Investigation**
   - Cross-stack issues (API + React + MCP server)
   - Performance bottlenecks requiring multiple investigation steps
   - Integration failures between services

6. **Test Automation and Validation**
   - Playwright test suite implementation (B001-B016 tests)
   - End-to-end testing across React frontend and FastAPI backend
   - Cross-browser compatibility testing for financial components

7. **Real-Time Data Integration**
   - WebSocket implementation for live market data streaming
   - MCP server timeout and reconnection handling
   - Real-time emoji sentiment indicator updates

### ❌ WHEN NOT TO USE

1. **Simple Single-Step Tasks**
   - Reading single files
   - Making simple text edits
   - Running basic commands

2. **Well-Defined Patterns**
   - Standard React component creation following existing patterns
   - Simple API endpoint additions using established templates
   - Routine documentation updates

3. **Immediate Actions**
   - Emergency bug fixes requiring immediate action
   - Simple configuration changes
   - Basic file operations

## Tool Parameters

### Required Parameters

#### `thought`

- **Type:** String
- **Purpose:** Current reasoning step
- **Format:** Clear, specific statement of current thinking
- **Context:** Should relate to Market Parser development task

#### `nextThoughtNeeded`

- **Type:** Boolean
- **Purpose:** Indicates if more thinking is required
- **Usage:**
  - `true` - Continue to next thought
  - `false` - Analysis complete, ready to act

#### `thoughtNumber`

- **Type:** Integer (minimum: 1)
- **Purpose:** Current step in sequence
- **Pattern:** Increment by 1 for each thought

#### `totalThoughts`

- **Type:** Integer (minimum: 1)
- **Purpose:** Estimated total thoughts needed
- **Behavior:** Can be adjusted up/down during process

### Optional Parameters

#### `isRevision`

- **Type:** Boolean
- **Purpose:** Indicates current thought revises previous thinking
- **Usage:** Set to `true` when reconsidering earlier decisions

#### `revisesThought`

- **Type:** Integer
- **Purpose:** Which thought number is being revised
- **Required when:** `isRevision` is `true`

#### `branchFromThought`

- **Type:** Integer
- **Purpose:** Starting point for alternative approach
- **Usage:** When exploring different solution paths

#### `branchId`

- **Type:** String
- **Purpose:** Identifier for current branch
- **Usage:** Track alternative solution approaches

#### `needsMoreThoughts`

- **Type:** Boolean
- **Purpose:** More thoughts needed beyond original estimate
- **Usage:** Extend analysis when complexity increases
- **Auto-Trigger:** Tool may automatically set this when reaching `totalThoughts` but analysis
  incomplete
- **Prototype Limit:** Avoid extending beyond 8 total thoughts for prototype stage

## Expected Tool Outputs

### Successful Response Structure

```json
{
  "thoughtNumber": 1,
  "totalThoughts": 5,
  "nextThoughtNeeded": true,
  "branches": [],
  "thoughtHistoryLength": 1
}
```

### Key Response Elements

- **thoughtNumber:** Confirms current step
- **totalThoughts:** May be updated by tool (auto-adjusted based on complexity)
- **nextThoughtNeeded:** Tool's assessment of continuation need
- **branches:** Available alternative paths (for exploring multiple solution approaches)
- **thoughtHistoryLength:** Total thoughts processed (includes revisions and branches)

### Tool Behavior Notes

- **Automatic Extension:** Tool may increase `totalThoughts` if analysis requires more depth
- **Branch Management:** Tool tracks alternative solution paths automatically
- **Revision Handling:** Previous thoughts remain accessible when using `isRevision`
- **Prototype Stage Limits:** Keep total thoughts under 8 for rapid prototyping approach

## Correct Usage Examples

### Example 1: Complex Backend Feature

```json
{
  "thought": "Need to add real-time stock alerts to FastAPI backend. First step: analyze existing WebSocket infrastructure and determine integration points with Polygon.io streaming API.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 6
}
```

**Context:** Multi-step API integration requiring analysis of existing infrastructure

### Example 2: Frontend Component Architecture

```json
{
  "thought": "Creating responsive financial chart component requires state management strategy. Must consider: data fetching patterns, chart library integration, mobile responsiveness, and emoji sentiment display.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 4
}
```

**Context:** Complex React component with multiple integration requirements

### Example 3: Cross-Stack Performance Issue

```json
{
  "thought": "API response times degraded after emoji enhancement. Need systematic analysis: 1) Profile FastAPI endpoints, 2) Check React render performance, 3) Verify MCP server latency, 4) Analyze database queries.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 5
}
```

**Context:** Systematic debugging across full stack requiring multiple investigation steps

### Example 4: Thought Revision

```json
{
  "thought": "Actually, the performance issue isn't in the database layer. Previous analysis missed React component re-rendering caused by emoji state updates. Need to focus on React optimization instead.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 3,
  "totalThoughts": 5,
  "isRevision": true,
  "revisesThought": 2
}
```

**Context:** Revising previous analysis based on new evidence

### Example 5: Branch Exploration

```json
{
  "thought": "Alternative approach: Instead of modifying existing chat component, create new specialized financial-data component with built-in emoji sentiment analysis.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 3,
  "totalThoughts": 6,
  "branchFromThought": 2,
  "branchId": "alternative-component-approach"
}
```

**Context:** Exploring alternative solution path during component design

### Example 6: Playwright Test Implementation

```json
{
  "thought": "Need to implement B001-B016 Playwright test suite for financial chat interface. Step 1: Analyze existing test patterns, identify critical user flows: message input, analysis buttons, emoji sentiment display, export functionality.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 5
}
```

**Context:** Systematic approach to comprehensive test automation

### Example 7: WebSocket Integration Planning

```json
{
  "thought": "Adding real-time stock price updates requires WebSocket integration. Must consider: 1) FastAPI WebSocket endpoint design, 2) React component state management for live data, 3) Polygon.io streaming API integration, 4) Connection error handling and reconnection logic.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 6
}
```

**Context:** Complex real-time data streaming implementation across full stack

### Example 8: Market Parser Emoji Sentiment Enhancement

```json
{
  "thought": "Enhancing emoji sentiment indicators in Market Parser chat interface. Need to: 1) Analyze current emoji integration in ChatMessage_OpenAI component, 2) Research financial sentiment emoji patterns, 3) Design real-time sentiment update logic, 4) Integrate with FastAPI response formatting.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 5
}
```

**Context:** Market Parser specific feature requiring financial context and cross-stack emoji
integration

## Incorrect Usage Examples

### Example 1: Simple Task

```json
{
  "thought": "Need to read the package.json file to check dependencies.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 3
}
```

**WHY WRONG:** Use Read tool directly for simple file reading. Sequential thinking adds unnecessary
overhead.

### Example 2: Vague Thinking

```json
{
  "thought": "Working on the frontend stuff and need to make it better.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 4
}
```

**WHY WRONG:** Lacks specificity and clear direction. Thoughts must be concrete and actionable.

### Example 3: Single-Step Decision

```json
{
  "thought": "Should I use TypeScript interface or type alias for this component prop?",
  "nextThoughtNeeded": false,
  "thoughtNumber": 1,
  "totalThoughts": 1
}
```

**WHY WRONG:** Simple decision doesn't require sequential analysis. Use direct coding judgment.

### Example 4: Immediate Action Needed

```json
{
  "thought": "Production API is returning 500 errors. Let me systematically analyze all possible causes...",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 8
}
```

**WHY WRONG:** Emergency fixes need immediate action, not extended analysis. Check logs and fix
directly.

### Example 5: Over-Analysis for Prototype

```json
{
  "thought": "Need to design perfect scalable architecture for the financial data caching system with fault tolerance, distributed processing, and enterprise-grade performance optimization.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 12
}
```

**WHY WRONG:** Violates prototyping principles. Focus on basic functionality first, not enterprise
architecture.

### Example 6: Missing Market Parser Context

```json
{
  "thought": "Need to implement a new feature for the application.",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 3
}
```

**WHY WRONG:** Too generic. Should specify financial application context, tech stack, and specific
Market Parser requirements.

## Integration with Market Parser Prototyping Approach

### Prototyping-Aligned Usage

- **Focus on functionality first** - Use sequential thinking to ensure features work
- **Avoid over-engineering** - Limit thoughts to 3-5 for prototype stage
- **Rapid iteration** - Use to plan quick implementation cycles
- **Simple solutions preferred** - Guide thinking toward minimal viable implementations

### Coordination with Other Tools

1. **Start with sequential-thinking** for complex planning
2. **Use context7** for research during thought process
3. **Apply MCP filesystem tools** for implementation
4. **End with code-reviewer** for validation

### Quality Gates

- Maximum 8 thoughts for prototype stage tasks
- Each thought must advance toward working solution
- Avoid perfectionist analysis patterns
- Focus on user-facing functionality

## Common Pitfalls

1. **Analysis Paralysis** - Don't exceed 8 thoughts for prototype tasks
2. **Generic Thinking** - Always relate thoughts to Market Parser context
3. **Perfectionist Patterns** - Remember prototyping stage goals
4. **Scope Creep** - Keep thoughts focused on specific task
5. **Tool Overuse** - Use only for genuinely complex tasks

## Success Patterns

1. **Start with clear problem statement** related to financial app functionality
2. **Break into logical steps** that build toward working solution
3. **Consider both backend and frontend** implications
4. **Include error handling** and edge cases in planning
5. **End with actionable implementation plan** ready for coding

### Market Parser Specific Success Patterns

1. **Financial Context First** - Always frame thoughts in terms of market data, financial analysis,
   or trading functionality
2. **Emoji Integration Awareness** - Consider sentiment indicator implications for any UI changes
3. **OpenAI Agents SDK Constraints** - Plan around async agent patterns and MCP server limitations
4. **Cross-Platform Responsiveness** - Think mobile-first for React components serving financial
   professionals
5. **Real-Time Data Considerations** - Factor in Polygon.io API rate limits and data freshness
   requirements
6. **Prototype Stage Efficiency** - Prioritize working financial features over perfect architecture

## Tool Chain Examples

### Backend API Development

```
sequential-thinking → context7 (FastAPI/OpenAI Agents SDK docs) → backend-developer → code-reviewer
```

**Use Case:** Adding new Polygon.io endpoint integration

### Frontend Component Creation

```
sequential-thinking → context7 (React/Vite docs) → react-component-architect → playwright testing
```

**Use Case:** Building responsive financial chart components

### Full-Stack Feature Implementation

```
sequential-thinking → api-architect → backend-developer → react-component-architect → code-reviewer
```

**Use Case:** End-to-end emoji sentiment analysis feature

### Performance Investigation

```
sequential-thinking → performance-optimizer → code-reviewer
```

**Use Case:** Diagnosing and fixing API response time issues

### Bug Resolution

```
sequential-thinking → code-archaeologist → backend-developer/react-component-architect → code-reviewer
```

**Use Case:** Cross-stack integration failures between FastAPI and React

### Test Automation Development

```
sequential-thinking → context7 (Playwright docs) → react-component-architect → code-reviewer
```

**Use Case:** Implementing comprehensive B001-B016 test suite

### Documentation Creation

```
sequential-thinking → documentation-specialist → code-reviewer
```

**Use Case:** Creating or updating comprehensive API documentation

### Real-Time Feature Implementation

```
sequential-thinking → api-architect → backend-developer → react-component-architect → performance-optimizer → code-reviewer
```

**Use Case:** WebSocket-based live market data streaming

### Migration and Refactoring

```
sequential-thinking → code-archaeologist → team-configurator → backend-developer/react-component-architect → code-reviewer
```

**Use Case:** Major architectural changes or technology migration

---

**Remember:** Sequential-thinking tool is for complex analysis. For simple tasks, use direct action
tools. Always align with prototyping stage principles - functional solutions over perfect
architecture.
