# Playwright Test Report Format Specifications

**Document Purpose:** Standardized format specifications for comprehensive Playwright testing report generation  
**Template Coverage:** CLI and MCP methodologies for B001-B016 test suite execution  
**Compliance Level:** Required for all test reporting across Market Parser application  

---

## Overview

This document defines the standardized format specifications for Playwright test report generation across both CLI and MCP testing methodologies. These specifications ensure consistent, professional, and actionable test reporting that provides comprehensive insights for development and quality assurance.

### Template Files
- **CLI Template:** `.claude/templates/cli_report_template.md`
- **MCP Template:** `.claude/templates/mcp_report_template.md`
- **Integration Guide:** `.claude/templates/template_integration_guide.md`

---

## 🏗️ Report Structure Framework

### Mandatory Report Sections

All reports MUST include these standardized sections in exact order:

1. **Report Header & Metadata**
2. **Executive Summary**
3. **Configuration Details** (Method-specific)
4. **Detailed Test Results (B001-B016)**
5. **Performance Analysis**
6. **Infrastructure Status Report**
7. **Error Analysis & Troubleshooting**
8. **Quality Assurance Validation**
9. **Method-Specific Analysis** (CLI/MCP Deep Dive)
10. **Recommendations & Next Steps**
11. **Appendix & Reference**

### Section-Specific Requirements

#### Report Header & Metadata
```markdown
# Playwright {METHOD} Test Execution Report

**Report Type:** {METHOD} Methodology - Complete B001-B016 Test Suite
**Execution Date:** {TIMESTAMP}
**Report File:** playwright_{METHOD}_test_{TIMESTAMP}.md
**Testing Method:** {METHOD_DESCRIPTION}
**Session Protocol:** {SESSION_PROTOCOL}
```

**Required Variables:**
- `{METHOD}`: "CLI" or "MCP"
- `{TIMESTAMP}`: ISO 8601 format (YYYY-MM-DDTHH-MM-SS)
- `{METHOD_DESCRIPTION}`: Methodology-specific description
- `{SESSION_PROTOCOL}`: Session management approach

---

## 📊 Performance Classification System

### Universal Performance Categories

**Required for both CLI and MCP reports:**

```
😊 Good: ≤30 seconds (optimal performance)
😐 OK: 31-60 seconds (acceptable performance)
😴 Slow: 61-119 seconds (functional but slow)
❌ Timeout: ≥120 seconds (automatic FAIL)
```

### Performance Distribution Template
```markdown
Performance Category    | Count | Percentage | Expected Range
------------------------|-------|------------|----------------
😊 Good (≤30s)         | {GOOD_COUNT}     | {GOOD_PERCENTAGE}%     | {EXPECTED_GOOD_RANGE}
😐 OK (31-60s)         | {OK_COUNT}       | {OK_PERCENTAGE}%       | {EXPECTED_OK_RANGE}
😴 Slow (61-119s)      | {SLOW_COUNT}     | {SLOW_PERCENTAGE}%     | {EXPECTED_SLOW_RANGE}
❌ Timeout (≥120s)     | {TIMEOUT_COUNT} | {TIMEOUT_PERCENTAGE}% | {EXPECTED_TIMEOUT_RANGE}
```

### Method-Specific Performance Expectations

#### CLI Method Expectations
- **Good Range:** 60-80% (inherently faster)
- **OK Range:** 20-40% (acceptable)
- **Slow Range:** 0-10% (investigate if >10%)
- **Timeout Range:** 0% (fix required)

#### MCP Method Expectations  
- **Good Range:** 20-40% (optimistic for MCP)
- **OK Range:** 40-60% (typical for MCP)
- **Slow Range:** 10-30% (expected for MCP)
- **Timeout Range:** 0-5% (investigate if >5%)

---

## 🔧 Method-Specific Configuration Standards

### CLI Configuration Requirements

**Mandatory Configuration Validation:**
```markdown
### CLI Parameters Used
```bash
npx playwright test --timeout=120000 --workers=1 --reporter=line {TEST_FILE}
```

### Configuration Validation
- **Timeout Setting:** ✅ 120000ms (2 minutes) - CORRECT
- **Worker Setting:** ✅ --workers=1 (single session) - CORRECT  
- **Reporter Setting:** ✅ --reporter=line (fast CLI output) - CORRECT
- **Retry Setting:** ✅ --retries=0 (accurate timing) - CORRECT
```

### MCP Configuration Requirements

**Mandatory Tool Validation:**
```markdown
### MCP Tool Configuration Validation
- **mcp__playwright__browser_navigate:** ✅ Available
- **mcp__playwright__browser_click:** ✅ Available
- **mcp__playwright__browser_type:** ✅ Available
- **mcp__playwright__browser_wait_for:** ✅ Available (10s polling)
- **mcp__playwright__browser_snapshot:** ✅ Available
- **mcp__playwright__browser_evaluate:** ✅ Available
- **mcp__playwright__browser_close:** ✅ Available
```

**Single Browser Session Protocol:**
```markdown
### Single Browser Session Protocol
```
Session Lifecycle:
1. browser_navigate → http://localhost:3000/ (ONCE at start)
2. Execute ALL B001-B016 tests in same session
3. browser_close (ONCE at end)
```
```

---

## 📋 Test Results Documentation Standards

### Individual Test Result Format

**Required format for ALL B001-B016 tests:**

```markdown
#### B{ID}: {TEST_NAME}
- **Test ID:** B{ID}
- **Result:** {PASS/FAIL}
- **Duration:** {DURATION}s
- **Classification:** {CLASSIFICATION_EMOJI} {CLASSIFICATION_NAME}
- **{METHOD_SPECIFIC_FIELD}:** {METHOD_SPECIFIC_VALUE}
- **Notes:** {DETAILED_NOTES}
```

### CLI-Specific Test Fields
```markdown
- **CLI Command:** `npx playwright test --timeout=120000 --workers=1 --reporter=line {TEST_FILE}`
- **File:** {TEST_FILE_NAME}
```

### MCP-Specific Test Fields
```markdown
- **MCP Tools Used:** {TOOLS_LIST}
- **Polling Configuration:** 10s intervals ({POLLING_STATUS})
- **Browser State:** {BROWSER_STATE_INFO}
```

### Test Coverage Validation Template
```markdown
### Test Coverage Verification
- **Required Tests:** 16 (B001-B016)
- **Executed Tests:** {EXECUTED_TESTS}
- **Coverage Percentage:** {COVERAGE_PERCENTAGE}%
- **Missing Tests:** {MISSING_TESTS}
```

---

## 🏥 Infrastructure Documentation Standards

### Universal Infrastructure Status
```markdown
### Infrastructure Status
- **Backend Health:** {BACKEND_STATUS} (Port {BACKEND_PORT})
- **Frontend Health:** {FRONTEND_STATUS} (Port {FRONTEND_PORT})
- **Environment Validation:** {ENV_VALIDATION_STATUS}
```

### Health Check Documentation
```markdown
### Server Health Monitoring
```bash
# Backend Health Check Results
curl http://localhost:{BACKEND_PORT}/health
Response: {BACKEND_HEALTH_RESPONSE}
Status: {BACKEND_HEALTH_STATUS}
Response Time: {BACKEND_RESPONSE_TIME}ms

# Frontend Health Check Results  
curl http://localhost:{FRONTEND_PORT}/
Response: {FRONTEND_HEALTH_RESPONSE}
Status: {FRONTEND_HEALTH_STATUS}
Response Time: {FRONTEND_RESPONSE_TIME}ms
```
```

---

## 🚨 Error Analysis & Troubleshooting Standards

### Error Classification Requirements

**Mandatory error categorization:**
```markdown
### {METHOD} Error Patterns
- **Configuration Errors:** {CONFIG_ERROR_COUNT}
- **Timeout Errors:** {TIMEOUT_ERROR_COUNT}
- **Network Errors:** {NETWORK_ERROR_COUNT}
- **{METHOD_SPECIFIC_ERRORS}:** {METHOD_SPECIFIC_ERROR_COUNT}
```

### Error Resolution Template
```markdown
### Error Resolution Recommendations
{ERROR_RESOLUTION_RECOMMENDATIONS}

### Known {METHOD} Method Issues
{KNOWN_METHOD_ISSUES}
```

---

## 📈 Quality Metrics & Validation Standards

### Mandatory Quality Validation Checklist

**Required for ALL reports:**
```markdown
### Quality Assurance Validation

### Test Coverage Verification
- **Required Tests:** 16 (B001-B016)
- **Executed Tests:** {EXECUTED_TESTS}
- **Coverage Percentage:** {COVERAGE_PERCENTAGE}%
- **Missing Tests:** {MISSING_TESTS}

### {METHOD} Configuration Compliance
- ✅ {COMPLIANCE_ITEM_1}
- ✅ {COMPLIANCE_ITEM_2}
- ✅ {COMPLIANCE_ITEM_3}
- ✅ {COMPLIANCE_ITEM_4}

### Evidence Collection Status
- **Execution Logs:** {EXECUTION_LOGS_STATUS}
- **Performance Data:** {PERFORMANCE_DATA_STATUS}
- **Error Screenshots:** {SCREENSHOT_STATUS}
- **Configuration Validation:** {CONFIG_VALIDATION_STATUS}
```

---

## 🎯 Variable Substitution Standards

### Required Variable Naming Convention

**Performance Variables:**
- `{GOOD_COUNT}`, `{OK_COUNT}`, `{SLOW_COUNT}`, `{TIMEOUT_COUNT}`
- `{GOOD_PERCENTAGE}`, `{OK_PERCENTAGE}`, `{SLOW_PERCENTAGE}`, `{TIMEOUT_PERCENTAGE}`
- `{TOTAL_EXECUTION_TIME}`, `{AVERAGE_TEST_TIME}`

**Infrastructure Variables:**
- `{BACKEND_STATUS}`, `{FRONTEND_STATUS}`, `{BACKEND_PORT}`, `{FRONTEND_PORT}`
- `{BACKEND_HEALTH_RESPONSE}`, `{FRONTEND_HEALTH_RESPONSE}`

**Test Result Variables (for each B001-B016):**
- `{B{ID}_RESULT}`, `{B{ID}_DURATION}`, `{B{ID}_CLASSIFICATION}`
- `{B{ID}_NOTES}`, `{B{ID}_{METHOD_SPECIFIC_FIELD}}`

**Timestamp Variables:**
- `{TIMESTAMP}`: Report execution timestamp
- `{GENERATION_TIMESTAMP}`: Report generation timestamp

### Variable Validation Requirements

**All variables MUST be:**
1. **Populated**: No empty or undefined variables in final report
2. **Validated**: Data type and format validation before substitution
3. **Sanitized**: XSS protection and content sanitization
4. **Documented**: Clear meaning and expected format

---

## 📖 Appendix Requirements

### Mandatory Appendix Sections

**All reports MUST include:**

#### Command Reference Section
```markdown
### {METHOD} Command Reference
```bash
# Standard {METHOD} execution pattern
{COMMAND_EXAMPLES}
```
```

#### Performance Thresholds
```markdown
### Performance Thresholds
- **Good Performance Target:** ≤30 seconds
- **Acceptable Performance:** ≤60 seconds  
- **Maximum Tolerance:** ≤120 seconds
- **Automatic Failure:** >120 seconds
```

#### Method Advantages
```markdown
### {METHOD} Method Advantages
- **{ADVANTAGE_1}:** {DESCRIPTION_1}
- **{ADVANTAGE_2}:** {DESCRIPTION_2}
- **{ADVANTAGE_3}:** {DESCRIPTION_3}
```

---

## 🔄 Report Generation Integration Requirements

### File Naming Convention
- **CLI Reports:** `playwright_CLI_test_{TIMESTAMP}.md`
- **MCP Reports:** `playwright_MCP_test_{TIMESTAMP}.md`
- **Timestamp Format:** `YYYY-MM-DDTHH-MM-SS`

### Report Storage Requirements
- **Location:** Project root directory or designated reports folder
- **Permissions:** 0644 (readable by owner and group)
- **Retention:** Maintain last 30 days of reports
- **Backup:** Include in project repository for audit trail

### Quality Gates for Report Generation
1. **Template Validation**: Verify template file exists and is readable
2. **Variable Population**: Ensure all required variables are populated
3. **Format Validation**: Validate markdown syntax and structure
4. **Content Sanitization**: Apply XSS protection and content sanitization
5. **File Writing**: Verify successful file creation with proper permissions

---

## 🏆 Compliance Validation Checklist

### Report Completeness Validation

**Before report finalization, verify:**
- [ ] All mandatory sections present and populated
- [ ] All B001-B016 tests documented with required fields
- [ ] Performance classification applied to all tests
- [ ] Infrastructure status documented with health checks
- [ ] Error analysis includes method-specific error patterns
- [ ] Quality validation includes coverage verification
- [ ] Appendix includes command reference and performance thresholds
- [ ] All variables populated (no {PLACEHOLDER} text remaining)
- [ ] Timestamp format compliant (ISO 8601)
- [ ] File naming convention followed

### Method-Specific Compliance

#### CLI Report Compliance
- [ ] CLI configuration validation completed
- [ ] CLI command examples included
- [ ] CLI performance expectations documented
- [ ] CLI error patterns analyzed

#### MCP Report Compliance  
- [ ] MCP tool availability validated
- [ ] Single browser session protocol documented
- [ ] 10-second polling configuration verified
- [ ] MCP performance expectations set appropriately

---

## 📚 Template Integration Standards

### Template Loading Requirements
1. **Template Discovery**: Automatically locate template files in `.claude/templates/`
2. **Template Validation**: Verify template integrity and required sections
3. **Variable Mapping**: Map execution data to template variables
4. **Content Generation**: Process template with variable substitution
5. **Format Validation**: Validate generated content structure and syntax

### Error Handling Standards
- **Missing Template**: Fallback to basic report format with warning
- **Variable Errors**: Log missing variables and continue with placeholder notation
- **Format Errors**: Validate markdown structure and fix common issues
- **File I/O Errors**: Retry file operations with exponential backoff

---

**Document Version:** 1.0  
**Last Updated:** {CURRENT_TIMESTAMP}  
**Compliance Level:** Mandatory for all Playwright test reporting  
**Next Review:** Quarterly or upon framework updates

---

*These format specifications ensure consistent, professional, and actionable test reporting across all Playwright testing methodologies for the Market Parser application. Adherence to these standards is required for all test execution and reporting activities.*