# /research - Comprehensive Research Workflow

## Description

Execute a comprehensive research workflow using ALL available advanced tools systematically. This command provides a robust, self-contained workflow for researching any topic related to OpenAI, GPT-5, OpenAI Agents, or any other subject using the enhanced research methodology.

## Usage

Type `/research` in Chat to execute the comprehensive research workflow for the requested topic(s) in 'new_research_details.md'

---

# 🔍 COMPREHENSIVE RESEARCH WORKFLOW

## 🚨 CRITICAL: MANDATORY ADVANCED TOOL USAGE

**You MUST use ALL available advanced tools AS OFTEN AS NEEDED throughout the entire research process. This is NOT a one-time checklist - you must continuously use advanced tools throughout the process.**

### 🛠️ ADVANCED TOOL USAGE REQUIREMENTS

**PRIORITIZE ADVANCED TOOLKIT OVER STANDARD TOOLS:**

- **Sequential-Thinking Tools**: MANDATORY START for every phase - use for systematic research planning, complex reasoning, and holistic approach
- **Context7 Tools**: Use for generic research and library documentation
- **OpenAI Documentation Tools**: Use for OpenAI-specific research with proper fallback workflow
- **Serena Tools**: Use for code analysis, symbol searches, and pattern matching when researching codebases
- **Standard Read/Write/Edit**: Use for file operations and project analysis when researching local projects, and as fallback when advanced tools don't support the specific action needed

**CONTINUOUS TOOL USAGE PATTERNS:**

- **MANDATORY**: Start EVERY phase with Sequential-Thinking for systematic approach
- Use tools in ANY ORDER as needed for the specific research topic
- Use the SAME tool MULTIPLE TIMES as needed throughout the entire process
- NEVER treat tool lists as a rigid sequence
- ALWAYS use tools when they would be helpful, even if you've used them before
- **PROACTIVELY** use advanced tools if a task requires it - don't wait for explicit instruction
- Use tools for investigation, analysis, verification, and implementation at every step
- **NEVER STOP** using advanced tools unless the action is only supported by Standard Tools

---

## 📋 SYSTEMATIC RESEARCH WORKFLOW

### **PHASE 1: RESEARCH PLANNING & ANALYSIS**

1. **MANDATORY START: Sequential-Thinking** for systematic research planning and holistic approach
2. **Analyze the research topic** using Sequential-Thinking to understand scope and requirements
3. **Plan research strategy** using Sequential-Thinking to determine which tools and sources to use
4. **Continue using Sequential-Thinking** throughout the phase for complex reasoning and planning
5. **Proactively use advanced tools** as the research scope requires

**MANDATORY ACTIONS:**

- **START with Sequential-Thinking** for systematic research planning
- Analyze the research topic thoroughly using Sequential-Thinking
- Plan comprehensive research strategy using Sequential-Thinking
- **Continue using Sequential-Thinking** throughout the phase for complex reasoning
- **Proactively use advanced tools** as the research scope requires

### **PHASE 2: DOCUMENTATION RESEARCH**

**For OpenAI, GPT-5, OpenAI Agents topics:**

1. **MANDATORY START: Sequential-Thinking** for systematic documentation research planning
2. **FIRST: Try OpenAI documentation tools** with specific technical terms for semantic documentation search:
   - OpenAI Cookbook: `mcp__docs-openai-cookbook__search_openai_cookbook_docs`
   - OpenAI Python: `mcp__docs-openai-python__search_openai_python_docs`
   - OpenAI Agents: `mcp__docs-openai-agents__search_openai_agents_docs`
3. **FALLBACK: If no results**, retry same query with code search tools (automatically finds .ipynb files):
   - OpenAI Cookbook: `mcp__docs-openai-cookbook__search_openai_cookbook_code`
   - OpenAI Python: `mcp__docs-openai-python__search_openai_python_code`
   - OpenAI Agents: `mcp__docs-openai-agents__search_openai_agents_code`
4. **BACKUP: Use Context7** with broader search terms if both documentation tools fail
5. **Continue using Sequential-Thinking** to analyze and synthesize findings
6. **Proactively use advanced tools** throughout the documentation research process

**For other topics:**

1. **MANDATORY START: Sequential-Thinking** for systematic research planning
2. **Use Context7 Tools** for generic research and library documentation
3. **Continue using Sequential-Thinking** to analyze and synthesize findings
4. **Proactively use advanced tools** as the research scope requires

**MANDATORY ACTIONS:**

- **START with Sequential-Thinking** for systematic documentation research planning
- **DECISION POINT**: If researching OpenAI topics → Use OpenAI documentation tools first
- **DECISION POINT**: If researching other topics → Use Context7 tools directly
- **DECISION POINT**: If documentation search returns "No results" → Switch to code search tools
- **DECISION POINT**: If both documentation and code search fail → Use Context7 with broader terms
- Follow the enhanced research workflow with proper fallbacks
- **Continue using Sequential-Thinking** to analyze findings
- **Proactively use advanced tools** throughout the documentation research process

### **PHASE 3: CODE IMPLEMENTATION RESEARCH**

**For code patterns, examples, and snippets:**

1. **MANDATORY START: Sequential-Thinking** for systematic code research planning
2. **Use OpenAI code search tools** with specific patterns (e.g., "import openai", "class Agent", "def run("):
   - OpenAI Cookbook: `mcp__docs-openai-cookbook__search_openai_cookbook_code`
   - OpenAI Python: `mcp__docs-openai-python__search_openai_python_code`
   - OpenAI Agents: `mcp__docs-openai-agents__search_openai_agents_code`
3. **Try broader terms** if specific patterns fail
4. **Use Context7** for generic code research as backup
5. **Continue using Sequential-Thinking** to analyze code patterns and examples
6. **Proactively use advanced tools** for additional code analysis as needed

**MANDATORY ACTIONS:**

- **START with Sequential-Thinking** for systematic code research planning
- Use OpenAI code search tools with specific technical patterns:
  - `mcp__docs-openai-cookbook__search_openai_cookbook_code`
  - `mcp__docs-openai-python__search_openai_python_code`
  - `mcp__docs-openai-agents__search_openai_agents_code`
- Try broader terms if specific patterns fail
- **Continue using Sequential-Thinking** to analyze code patterns
- **Proactively use advanced tools** for comprehensive code research

### **PHASE 4: COMPREHENSIVE SYNTHESIS**

1. **MANDATORY START: Sequential-Thinking** for systematic synthesis planning
2. **Use Serena Tools** to organize and structure findings if researching codebases
3. **Use Standard Read/Write/Edit** for comprehensive project analysis if researching local projects
4. **Continue using Sequential-Thinking** to synthesize all research findings
5. **Proactively use advanced tools** for additional analysis and verification
6. **Use all available tools** to ensure comprehensive coverage

**MANDATORY ACTIONS:**

- **START with Sequential-Thinking** for systematic synthesis planning
- **SYNTHESIS STRATEGY**: Organize findings by source and relevance
- **CROSS-REFERENCE**: Compare findings from different tools and sources
- **VERIFY CONSISTENCY**: Ensure information from different sources aligns
- **PRIORITIZE FINDINGS**: Rank information by reliability and relevance
- **IDENTIFY GAPS**: Note areas where information is missing or incomplete
- **CREATE COHERENT NARRATIVE**: Synthesize findings into comprehensive analysis
- Use appropriate tools based on research type and scope
- **Continue using Sequential-Thinking** to synthesize findings comprehensively
- **Proactively use advanced tools** for thorough analysis and verification
- Ensure comprehensive coverage using all available tools

---

## 🛠️ TOOL SELECTION MAPPING

### **OpenAI Documentation Tools:**

- **OpenAI Cookbook**: `mcp__docs-openai-cookbook__*`
- **OpenAI Python SDK**: `mcp__docs-openai-python__*`
- **OpenAI Agents Python**: `mcp__docs-openai-agents__*`

### **Generic Research Tools:**

- **Context7**: `mcp_context7_*` (for library documentation and generic research)

### **Code Analysis Tools:**

- **Serena Tools**: `mcp_serena_*` (for codebase analysis and symbol searches)
- **Standard Read/Write/Edit**: For file operations and project management

### **Reasoning Tools:**

- **Sequential-Thinking**: `mcp_sequential-thinking_sequentialthinking` (MANDATORY for all phases)

---

## 🔍 ENHANCED RESEARCH WORKFLOW

### **For Documentation Research:**

1. **FIRST**: Try OpenAI documentation tools with specific technical terms:
   - `mcp__docs-openai-cookbook__search_openai_cookbook_docs`
   - `mcp__docs-openai-python__search_openai_python_docs`
   - `mcp__docs-openai-agents__search_openai_agents_docs`
2. **FALLBACK**: If no results, retry same query with OpenAI code search tools:
   - `mcp__docs-openai-cookbook__search_openai_cookbook_code`
   - `mcp__docs-openai-python__search_openai_python_code`
   - `mcp__docs-openai-agents__search_openai_agents_code`
3. **BACKUP**: Use Context7 with broader search terms
4. **NOTE**: Code search tools automatically find .ipynb documentation files

### **For Code Implementation Research:**

1. **PRIMARY**: Use OpenAI code search tools with specific patterns (e.g., "import openai", "class Agent", "def run("):
   - `mcp__docs-openai-cookbook__search_openai_cookbook_code`
   - `mcp__docs-openai-python__search_openai_python_code`
   - `mcp__docs-openai-agents__search_openai_agents_code`
2. **FALLBACK**: Try broader terms if specific patterns fail
3. **BACKUP**: Use Context7 for generic code research

### **For Generic Research:**

1. **PRIMARY**: Use Context7 with specific search terms
2. **FALLBACK**: Try broader terms if specific searches fail
3. **BACKUP**: Use web search for additional information

---

## 🚨 ERROR HANDLING GUIDANCE

### **OpenAI Documentation Tools Error Handling:**

- **If tool returns "No results"**: This is normal - proceed to fallback code search tools
- **If tool returns "GitHub API request failed"**: Try again with simpler query or use Context7
- **If tool returns empty results**: Try broader search terms or alternative terminology
- **If tool times out**: Wait and retry, or switch to Context7 for generic research

### **Context7 Tools Error Handling:**

- **If library not found**: Try alternative library names or broader search terms
- **If no documentation available**: Use web search as backup
- **If API rate limited**: Wait and retry, or use alternative research methods

### **Serena Tools Error Handling:**

- **If symbol not found**: Try alternative symbol names or broader search patterns
- **If codebase analysis fails**: Use standard read/write tools for file analysis
- **If pattern search returns no results**: Try simpler patterns or different file types

### **Sequential-Thinking Error Handling:**

- **If thinking process stalls**: Break down the problem into smaller components
- **If reasoning becomes circular**: Take a step back and approach from different angle
- **If analysis becomes too complex**: Focus on one aspect at a time

---

## 📝 QUERY OPTIMIZATION TIPS

### **Documentation Queries:**

- Use specific technical terms (e.g., "function calling" not "functions")
- Try both singular and plural forms
- Use exact API method names when searching code
- Include relevant context terms

### **Code Pattern Queries:**

- Use exact import statements (e.g., "import openai")
- Use specific class names (e.g., "class Agent")
- Use exact method signatures (e.g., "def run(")
- Include decorators and annotations (e.g., "@function_tool")

### **Generic Research Queries:**

- Start with specific terms and broaden if needed
- Include relevant context and domain information
- Try alternative terminology and synonyms
- Use library-specific terms when researching frameworks

---

## 🚫 CRITICAL BOUNDARIES & RESTRICTIONS

### **DO NOT PERFORM:**

- ❌ **NO ASSUMPTIONS** - Always verify information through multiple sources
- ❌ **NO INCOMPLETE RESEARCH** - Ensure comprehensive coverage of the topic
- ❌ **NO TOOL LIMITATIONS** - Use all available tools as needed

### **MUST DO:**

- ✅ **COMPREHENSIVE COVERAGE** - Research all relevant aspects of the topic
- ✅ **MULTIPLE SOURCES** - Verify information through different tools and sources
- ✅ **USE ALL ADVANCED TOOLS** continuously throughout the research process
- ✅ **SYNTHESIZE FINDINGS** - Provide comprehensive analysis and synthesis

---

## ⏰ TIME MANAGEMENT GUIDANCE

### **When to Stop Researching and Start Synthesizing:**

- **Time Limit**: Set a maximum research time (e.g., 30-45 minutes for complex topics)
- **Information Saturation**: Stop when new sources provide diminishing returns
- **Coverage Threshold**: Stop when you have information from at least 3 different sources
- **Quality Threshold**: Stop when you have high-quality, reliable information
- **Scope Completion**: Stop when you've covered all relevant aspects of the topic

### **Research Time Allocation:**

- **Phase 1 (Planning)**: 5-10 minutes
- **Phase 2 (Documentation)**: 15-20 minutes
- **Phase 3 (Code Research)**: 10-15 minutes
- **Phase 4 (Synthesis)**: 10-15 minutes
- **Total**: 40-60 minutes maximum

### **Signs to Stop Researching:**

- ✅ Found comprehensive information from multiple reliable sources
- ✅ Information from different sources is consistent and complementary
- ✅ Have both high-level concepts and specific implementation details
- ✅ Can answer the research question with confidence
- ✅ Have actionable insights and recommendations

---

## 🔄 ITERATIVE RESEARCH PATTERN

**For Each Research Session:**

1. **MANDATORY START**: Use Sequential-Thinking to analyze the research topic and plan systematic approach
2. **PLAN**: Use Sequential-Thinking to determine research strategy and tool selection
3. **DOCUMENTATION**: Use appropriate documentation tools with proper fallback workflow
4. **CODE**: Use code search tools for implementation patterns and examples
5. **CONTINUE THINKING**: Use Sequential-Thinking throughout for complex reasoning and analysis
6. **PROACTIVE RESEARCH**: Use advanced tools proactively as the research scope requires
7. **SYNTHESIS**: Use all advanced tools to synthesize comprehensive findings
8. **VERIFICATION**: Use multiple sources to verify and cross-reference information
9. **COMPREHENSIVE REPORT**: Provide detailed analysis and actionable insights

**CRITICAL**: Never stop using advanced tools unless the specific action is only supported by Standard Tools

---

## 📋 RESULT FORMATTING GUIDANCE

### **Research Report Structure:**

1. **Executive Summary**: 2-3 sentence overview of key findings
2. **Research Question**: Clearly state what was being researched
3. **Methodology**: Brief description of tools and approach used
4. **Key Findings**: Organized by topic with supporting evidence
5. **Source Analysis**: Reliability and relevance of each source
6. **Gaps Identified**: Areas where information was missing or incomplete
7. **Recommendations**: Actionable insights based on findings
8. **Next Steps**: Suggested follow-up research or actions

### **Information Organization:**

- **By Source Type**: Group findings by documentation, code, and generic research
- **By Reliability**: Prioritize official documentation over community sources
- **By Relevance**: Rank information by how directly it answers the research question
- **By Completeness**: Note which aspects are well-covered vs. lacking

### **Evidence Presentation:**

- **Direct Quotes**: Include relevant quotes with proper attribution
- **Code Examples**: Show specific code patterns and implementations
- **Cross-References**: Link related findings from different sources
- **Visual Hierarchy**: Use headers, bullet points, and formatting for clarity

### **Quality Indicators:**

- ✅ **Comprehensive**: Covers all relevant aspects of the topic
- ✅ **Verified**: Information confirmed through multiple sources
- ✅ **Actionable**: Provides specific recommendations and next steps
- ✅ **Well-Sourced**: All claims backed by reliable evidence
- ✅ **Organized**: Clear structure and logical flow

---

## 📚 AVAILABLE RESEARCH SOURCES

**OpenAI Documentation:**

- OpenAI Cookbook: Examples and guides for OpenAI APIs
- OpenAI Python SDK: Python SDK documentation and examples
- OpenAI Agents Python: Agents framework documentation and examples

**Generic Research:**

- Context7: Comprehensive library documentation and research
- Web Search: Additional information and current updates

**Code Analysis:**

- Serena Tools: Advanced codebase analysis and symbol searches
- Standard Read/Write/Edit: Local project analysis and file operations

**Note**: This research workflow is designed to be comprehensive and robust, using all available tools to ensure no information is missed.

---

## 📖 EXAMPLES OF SUCCESSFUL RESEARCH SESSIONS

### **Example 1: Researching "OpenAI Function Calling"**

**Research Question**: "How to implement function calling with OpenAI API?"

**Process:**

1. **Sequential-Thinking**: Analyzed scope - need both documentation and code examples
2. **Documentation Research**: Used `mcp__docs-openai-cookbook__search_openai_cookbook_docs` with "function calling"
3. **Fallback**: When docs returned limited results, used `mcp__docs-openai-cookbook__search_openai_cookbook_code` with "function calling"
4. **Code Research**: Found multiple .ipynb examples with implementation patterns
5. **Context7 Backup**: Used `mcp_context7_resolve-library-id` for "openai function calling" to get additional context
6. **Synthesis**: Combined documentation concepts with working code examples

**Result**: Comprehensive guide with both theoretical understanding and practical implementation examples.

### **Example 2: Researching "Python Async Programming"**

**Research Question**: "Best practices for async programming in Python?"

**Process:**

1. **Sequential-Thinking**: Identified need for generic research (not OpenAI-specific)
2. **Context7 Research**: Used `mcp_context7_resolve-library-id` for "python async" to find relevant libraries
3. **Documentation**: Used `mcp_context7_get-library-docs` to get comprehensive async programming guides
4. **Code Examples**: Used Serena tools to find async patterns in local codebase
5. **Synthesis**: Combined official documentation with practical examples

**Result**: Complete async programming guide with official docs, best practices, and real-world examples.

### **Example 3: Researching "Custom Cursor Commands"**

**Research Question**: "How to create custom slash commands in Cursor?"

**Process:**

1. **Sequential-Thinking**: Identified need for Cursor-specific documentation
2. **Context7 Research**: Used `mcp_context7_resolve-library-id` for "cursor custom slash commands"
3. **Documentation**: Found comprehensive guides on command structure and format
4. **Code Analysis**: Used Serena tools to analyze existing commands in the project
5. **Synthesis**: Combined external documentation with local implementation patterns

**Result**: Complete guide for creating custom Cursor commands with working examples.

---

## 🎯 SUCCESS CRITERIA

**You have successfully completed the research when:**

- ✅ The research topic has been thoroughly analyzed using Sequential-Thinking
- ✅ All relevant documentation sources have been searched using proper fallback workflow
- ✅ Code implementation patterns have been researched using appropriate tools
- ✅ Sequential-Thinking and ALL advanced tools have been used repeatedly throughout the process
- ✅ Advanced tools have been used proactively as the research scope required
- ✅ Multiple sources have been used to verify and cross-reference information
- ✅ Comprehensive synthesis and analysis have been provided
- ✅ Actionable insights and recommendations have been delivered

---

## 🚨 VIOLATION PENALTIES

**If you fail to use advanced tools continuously:**

- ❌ Not starting every phase with Sequential-Thinking = FAILURE
- ❌ Using tools only once and stopping = FAILURE
- ❌ Following rigid order instead of using tools as needed = FAILURE  
- ❌ Not using tools throughout the entire process = FAILURE
- ❌ Not using advanced tools proactively when research requires it = FAILURE
- ❌ Using wrong tool for the operation = FAILURE
- ❌ Stopping advanced tool usage when Standard Tools could be used = FAILURE
- ❌ Not following the enhanced research workflow with proper fallbacks = FAILURE

**SUCCESS PATTERN:**

- ✅ Sequential-Thinking used at START of every phase
- ✅ Tools used multiple times throughout the research process
- ✅ Tools used in different orders based on research needs
- ✅ Continuous, repeated, and proactive tool usage from start to finish
- ✅ Correct tool selection based on research type and scope
- ✅ No rigid sequencing - only logical tool usage based on research requirements
- ✅ Advanced tools used proactively as research scope requires
- ✅ Enhanced research workflow followed with proper fallbacks

---

**REMEMBER: The advanced tool list is your toolkit - use every tool as often as needed, in any order, throughout the entire research process. START every phase with Sequential-Thinking, use tools repeatedly and proactively as the research scope requires, and NEVER stop using advanced tools unless the specific action is only supported by Standard Tools.**

---

## 🚀 EXECUTION INSTRUCTIONS

**When this command is invoked, the AI Agent should:**

1. **IMMEDIATELY START** with Sequential-Thinking to analyze the research topic and plan systematic approach
2. **FOLLOW THE COMPLETE WORKFLOW** outlined above using ALL advanced tools systematically
3. **CONTINUE USING ADVANCED TOOLS** throughout the entire research process
4. **PROVIDE COMPREHENSIVE SYNTHESIS** of all findings with actionable insights
5. **VERIFY INFORMATION** through multiple sources and cross-referencing

**This command is SELF-CONTAINED and provides comprehensive research capabilities for any topic.**

---

## 🔧 TROUBLESHOOTING COMMON ISSUES

### **Issue: All Tools Return "No Results"**

**Symptoms**: Every search tool returns empty results or "No results found"
**Solutions**:

- Try broader, more general search terms
- Use alternative terminology and synonyms
- Check if the topic is too specific or niche
- Use Context7 with very general terms as backup
- Consider if the research question needs to be rephrased

### **Issue: Conflicting Information from Different Sources**

**Symptoms**: Different tools provide contradictory information
**Solutions**:

- Prioritize official documentation over community sources
- Check publication dates and version information
- Look for consensus among multiple sources
- Note the discrepancies in your synthesis
- Use Sequential-Thinking to analyze the differences

### **Issue: Research Becomes Too Broad or Unfocused**

**Symptoms**: Finding too much information that doesn't directly answer the research question
**Solutions**:

- Refocus on the specific research question
- Use more targeted search terms
- Set stricter criteria for what information to include
- Use Sequential-Thinking to narrow the scope
- Stop researching and start synthesizing with what you have

### **Issue: Tools Keep Failing or Timing Out**

**Symptoms**: Tools return errors or time out repeatedly
**Solutions**:

- Wait a few minutes and retry
- Use simpler, shorter search queries
- Switch to alternative tools (e.g., Context7 instead of OpenAI tools)
- Use standard read/write tools for local file analysis
- Break down the research into smaller, more manageable pieces

### **Issue: Information Overload - Too Much to Synthesize**

**Symptoms**: Overwhelming amount of information that's hard to organize
**Solutions**:

- Use Sequential-Thinking to categorize information
- Focus on the most relevant and reliable sources
- Create a structured outline before synthesizing
- Prioritize information that directly answers the research question
- Consider doing multiple focused research sessions instead of one large one

### **Issue: Research Question is Too Vague or Ambiguous**

**Symptoms**: Not sure what to search for or how to proceed
**Solutions**:

- Use Sequential-Thinking to break down the question into specific components
- Start with very broad searches to understand the topic area
- Refine the research question based on initial findings
- Ask clarifying questions about what specific information is needed
- Focus on one aspect of the question at a time

### **Issue: Can't Find Recent or Up-to-Date Information**

**Symptoms**: All sources seem outdated or don't cover recent developments
**Solutions**:

- Use web search for the most recent information
- Check if the topic has changed significantly recently
- Look for official announcements or changelogs
- Use Context7 to find the most recent versions of libraries
- Note the age of information in your synthesis

**Remember**: If you encounter persistent issues, use Sequential-Thinking to analyze the problem and adjust your approach accordingly.
