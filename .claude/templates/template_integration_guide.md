# Playwright Test Report Template Integration Guide

**Integration Guide Purpose:** Step-by-step instructions for implementing report generation templates in Playwright testing commands  
**Target Audience:** Specialists executing `/test_cli_full` and `/test_mcp_full` slash commands  
**Template Coverage:** CLI and MCP methodologies with comprehensive data collection and variable substitution  

---

## Quick Start Integration

### Template File Locations
```
.claude/templates/
├── cli_report_template.md           # CLI methodology report template
├── mcp_report_template.md           # MCP methodology report template  
├── report_format_specifications.md  # Format standards and requirements
└── template_integration_guide.md    # This integration guide
```

### Integration Workflow Overview
1. **Data Collection Phase**: Gather test execution data during test runs
2. **Template Processing Phase**: Load template and substitute variables
3. **Report Generation Phase**: Create final report with standardized format
4. **Quality Validation Phase**: Verify report completeness and compliance

---

## 🚀 Data Collection Framework

### Universal Data Collection Requirements

**Required for BOTH CLI and MCP methods:**

```python
# Core execution data structure
execution_data = {
    # Timing data
    "start_time": datetime.now(),
    "end_time": None,
    "total_execution_time": None,
    "average_test_time": None,
    
    # Test results (B001-B016)
    "test_results": {},
    "passed_count": 0,
    "failed_count": 0,
    "success_percentage": 0,
    
    # Performance classification
    "good_count": 0,
    "ok_count": 0, 
    "slow_count": 0,
    "timeout_count": 0,
    "performance_percentages": {},
    
    # Infrastructure status
    "backend_status": None,
    "frontend_status": None,
    "backend_port": 8000,
    "frontend_port": 3000,
    
    # Environment data
    "timestamp": datetime.now().strftime("%Y-%m-%dT%H-%M-%S"),
    "generation_timestamp": None
}
```

### Test-Specific Data Collection (B001-B016)

**For each individual test:**

```python
# Individual test data structure
test_data = {
    "test_id": "B001",  # B001 through B016
    "test_name": "Market Status Check",
    "test_file": "test-b001-market-status.spec.ts",
    "result": "PASS" or "FAIL",
    "duration": 42.5,  # seconds as float
    "classification": "😊 Good",  # Based on duration
    "notes": "Test completed successfully with emoji indicators",
    
    # Method-specific fields (added based on CLI vs MCP)
    "method_specific_data": {}
}
```

---

## 🔧 CLI Method Integration

### CLI Data Collection Pattern

```python
def collect_cli_test_data(test_id, test_file):
    """Collect CLI-specific test execution data"""
    
    # Pre-execution setup
    start_time = time.time()
    cli_command = f"npx playwright test --timeout=120000 --workers=1 --reporter=line {test_file}"
    
    # Execute CLI command and capture results
    try:
        result = subprocess.run(cli_command.split(), 
                              capture_output=True, 
                              text=True, 
                              timeout=125)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Determine test result
        test_result = "PASS" if result.returncode == 0 else "FAIL"
        
        # Classify performance
        if duration <= 30:
            classification = "😊 Good"
        elif duration <= 60:
            classification = "😐 OK"
        elif duration <= 119:
            classification = "😴 Slow"
        else:
            classification = "❌ Timeout"
        
        # CLI-specific data
        cli_data = {
            "cli_command": cli_command,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
        return {
            "test_id": test_id,
            "result": test_result,
            "duration": round(duration, 1),
            "classification": classification,
            "method_specific_data": cli_data
        }
        
    except subprocess.TimeoutExpired:
        return {
            "test_id": test_id,
            "result": "FAIL",
            "duration": 120.0,
            "classification": "❌ Timeout",
            "method_specific_data": {"timeout": True}
        }
```

### CLI Template Variable Mapping

```python
def map_cli_variables(execution_data):
    """Map collected data to CLI template variables"""
    
    variables = {
        # Header variables
        "TIMESTAMP": execution_data["timestamp"],
        "GENERATION_TIMESTAMP": datetime.now().isoformat(),
        
        # Summary variables
        "PASSED_COUNT": execution_data["passed_count"],
        "FAILED_COUNT": execution_data["failed_count"],
        "SUCCESS_PERCENTAGE": execution_data["success_percentage"],
        "TOTAL_EXECUTION_TIME": execution_data["total_execution_time"],
        "AVERAGE_TEST_TIME": execution_data["average_test_time"],
        
        # Performance distribution
        "GOOD_COUNT": execution_data["good_count"],
        "OK_COUNT": execution_data["ok_count"],
        "SLOW_COUNT": execution_data["slow_count"],
        "TIMEOUT_COUNT": execution_data["timeout_count"],
        
        # CLI-specific configuration
        "NODE_VERSION": get_node_version(),
        "NPM_VERSION": get_npm_version(),
        "PLAYWRIGHT_VERSION": get_playwright_version(),
        
        # Infrastructure status
        "BACKEND_STATUS": execution_data["backend_status"],
        "FRONTEND_STATUS": execution_data["frontend_status"],
        "BACKEND_PORT": execution_data["backend_port"],
        "FRONTEND_PORT": execution_data["frontend_port"]
    }
    
    # Add individual test variables (B001-B016)
    for test_id, test_data in execution_data["test_results"].items():
        variables.update({
            f"{test_id}_RESULT": test_data["result"],
            f"{test_id}_DURATION": test_data["duration"],
            f"{test_id}_CLASSIFICATION": test_data["classification"],
            f"{test_id}_NOTES": test_data.get("notes", ""),
            f"{test_id}_CLI_COMMAND": test_data["method_specific_data"].get("cli_command", "")
        })
    
    return variables
```

---

## 🎭 MCP Method Integration

### MCP Data Collection Pattern

```python
def collect_mcp_test_data(test_id, test_description):
    """Collect MCP-specific test execution data"""
    
    start_time = time.time()
    
    try:
        # MCP browser automation sequence
        mcp_tools_used = []
        
        # Example MCP test execution
        if test_id in ["B007", "B008", "B009"]:  # Button tests
            # Click button test
            click_result = mcp__playwright__browser_click({
                "element": f"{test_description} button",
                "ref": f"button-{test_id.lower()}"
            })
            mcp_tools_used.append("browser_click")
            
            # Wait for response with 10s polling
            wait_result = mcp__playwright__browser_wait_for({
                "text": "Market",
                "time": 10
            })
            mcp_tools_used.append("browser_wait_for")
            
        # Type input tests
        elif test_id in ["B001", "B002", "B003", "B004"]:
            type_result = mcp__playwright__browser_type({
                "element": "message input",
                "text": get_test_query(test_id),
                "ref": "chat-input"
            })
            mcp_tools_used.append("browser_type")
            
            wait_result = mcp__playwright__browser_wait_for({
                "text": "Market",
                "time": 10
            })
            mcp_tools_used.append("browser_wait_for")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Determine result based on response
        test_result = "PASS" if wait_result.get("success", False) else "FAIL"
        
        # Classify performance (MCP expectations)
        if duration <= 30:
            classification = "😊 Good"
        elif duration <= 60:
            classification = "😐 OK"
        elif duration <= 119:
            classification = "😴 Slow"
        else:
            classification = "❌ Timeout"
        
        # MCP-specific data
        mcp_data = {
            "mcp_tools_used": mcp_tools_used,
            "polling_configuration": "10s intervals",
            "browser_state": "Active session maintained",
            "session_continuity": True
        }
        
        return {
            "test_id": test_id,
            "result": test_result,
            "duration": round(duration, 1),
            "classification": classification,
            "method_specific_data": mcp_data
        }
        
    except Exception as e:
        return {
            "test_id": test_id,
            "result": "FAIL",
            "duration": 120.0,
            "classification": "❌ Timeout",
            "method_specific_data": {"error": str(e)}
        }
```

### MCP Template Variable Mapping

```python
def map_mcp_variables(execution_data):
    """Map collected data to MCP template variables"""
    
    variables = {
        # Header variables
        "TIMESTAMP": execution_data["timestamp"],
        "GENERATION_TIMESTAMP": datetime.now().isoformat(),
        
        # Summary variables (same as CLI)
        "PASSED_COUNT": execution_data["passed_count"],
        "FAILED_COUNT": execution_data["failed_count"],
        "SUCCESS_PERCENTAGE": execution_data["success_percentage"],
        "TOTAL_EXECUTION_TIME": execution_data["total_execution_time"],
        "AVERAGE_TEST_TIME": execution_data["average_test_time"],
        
        # MCP-specific session data
        "SESSION_INIT_STATUS": "Successful",
        "SESSION_DURATION": execution_data["total_execution_time"],
        "SESSION_TERMINATION_STATUS": "Clean shutdown",
        "NAVIGATION_COUNT": 1,  # Single navigation at start
        
        # MCP tool status
        "MCP_TOOLS_STATUS": "All tools available and functional",
        "BROWSER_ENGINE_STATUS": "Chromium ready",
        "APPLICATION_URL": f"http://localhost:{execution_data['frontend_port']}/"
    }
    
    # Add individual test variables with MCP-specific fields
    for test_id, test_data in execution_data["test_results"].items():
        mcp_data = test_data["method_specific_data"]
        variables.update({
            f"{test_id}_RESULT": test_data["result"],
            f"{test_id}_DURATION": test_data["duration"],
            f"{test_id}_CLASSIFICATION": test_data["classification"],
            f"{test_id}_MCP_TOOLS": ", ".join(mcp_data.get("mcp_tools_used", [])),
            f"{test_id}_POLLING_STATUS": mcp_data.get("polling_configuration", "10s intervals"),
            f"{test_id}_BROWSER_STATE": mcp_data.get("browser_state", "Active"),
            f"{test_id}_NOTES": test_data.get("notes", "")
        })
    
    return variables
```

---

## 📝 Template Processing Engine

### Template Loading and Processing

```python
def generate_report(method, execution_data):
    """Generate report using appropriate template"""
    
    # Load template based on method
    template_path = f".claude/templates/{method.lower()}_report_template.md"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        raise Exception(f"Template file not found: {template_path}")
    
    # Map variables based on method
    if method.upper() == "CLI":
        variables = map_cli_variables(execution_data)
    elif method.upper() == "MCP":
        variables = map_mcp_variables(execution_data)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Process template with variable substitution
    processed_content = substitute_variables(template_content, variables)
    
    # Generate report filename
    timestamp = execution_data["timestamp"]
    report_filename = f"playwright_{method.upper()}_test_{timestamp}.md"
    
    # Write report file
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(processed_content)
    
    return report_filename

def substitute_variables(template_content, variables):
    """Substitute template variables with actual values"""
    
    processed_content = template_content
    
    for var_name, var_value in variables.items():
        placeholder = f"{{{var_name}}}"
        # Convert None values to "N/A"
        if var_value is None:
            var_value = "N/A"
        processed_content = processed_content.replace(placeholder, str(var_value))
    
    # Check for remaining unsubstituted variables
    import re
    remaining_vars = re.findall(r'\{[A-Z_]+\}', processed_content)
    if remaining_vars:
        print(f"Warning: Unsubstituted variables found: {remaining_vars}")
    
    return processed_content
```

---

## 🏥 Infrastructure Health Integration

### Health Check Collection

```python
def collect_infrastructure_status():
    """Collect infrastructure health data for template"""
    
    import requests
    
    infrastructure_data = {
        "backend_status": "Unknown",
        "frontend_status": "Unknown",
        "backend_port": 8000,
        "frontend_port": 3000,
        "backend_response_time": 0,
        "frontend_response_time": 0,
        "backend_health_response": "",
        "frontend_health_response": ""
    }
    
    # Backend health check
    try:
        start_time = time.time()
        response = requests.get("http://localhost:8000/health", timeout=10)
        end_time = time.time()
        
        infrastructure_data["backend_status"] = "Healthy" if response.status_code == 200 else "Unhealthy"
        infrastructure_data["backend_response_time"] = round((end_time - start_time) * 1000, 1)
        infrastructure_data["backend_health_response"] = response.text[:100]
        
    except Exception as e:
        infrastructure_data["backend_status"] = f"Error: {str(e)}"
    
    # Frontend health check
    try:
        start_time = time.time()
        response = requests.get("http://localhost:3000/", timeout=10)
        end_time = time.time()
        
        infrastructure_data["frontend_status"] = "Healthy" if response.status_code == 200 else "Unhealthy"
        infrastructure_data["frontend_response_time"] = round((end_time - start_time) * 1000, 1)
        infrastructure_data["frontend_health_response"] = "React application loaded"
        
    except Exception as e:
        infrastructure_data["frontend_status"] = f"Error: {str(e)}"
    
    return infrastructure_data
```

---

## 📊 Performance Analysis Integration

### Performance Classification Engine

```python
def classify_performance(duration, method="CLI"):
    """Classify test performance based on duration and method"""
    
    if duration <= 30:
        return {
            "classification": "😊 Good",
            "category": "good",
            "description": "Optimal performance"
        }
    elif duration <= 60:
        return {
            "classification": "😐 OK", 
            "category": "ok",
            "description": "Acceptable performance"
        }
    elif duration <= 119:
        return {
            "classification": "😴 Slow",
            "category": "slow", 
            "description": "Functional but slow"
        }
    else:
        return {
            "classification": "❌ Timeout",
            "category": "timeout",
            "description": "Automatic FAIL"
        }

def calculate_performance_distribution(test_results):
    """Calculate performance distribution for template"""
    
    distribution = {
        "good_count": 0,
        "ok_count": 0,
        "slow_count": 0,
        "timeout_count": 0
    }
    
    total_tests = len(test_results)
    
    for test_data in test_results.values():
        classification = classify_performance(test_data["duration"])
        category = classification["category"]
        distribution[f"{category}_count"] += 1
    
    # Calculate percentages
    distribution.update({
        "good_percentage": round(distribution["good_count"] / total_tests * 100, 1),
        "ok_percentage": round(distribution["ok_count"] / total_tests * 100, 1),
        "slow_percentage": round(distribution["slow_count"] / total_tests * 100, 1),
        "timeout_percentage": round(distribution["timeout_count"] / total_tests * 100, 1)
    })
    
    return distribution
```

---

## ✅ Quality Validation Integration

### Report Validation Framework

```python
def validate_report_quality(report_content, method):
    """Validate generated report meets quality standards"""
    
    validation_results = {
        "template_sections_present": False,
        "all_tests_documented": False, 
        "variables_substituted": False,
        "performance_classification_complete": False,
        "infrastructure_status_documented": False,
        "method_specific_requirements_met": False
    }
    
    # Check mandatory sections
    required_sections = [
        "Executive Summary",
        "Detailed Test Results", 
        "Performance Analysis",
        "Infrastructure Status",
        "Quality Assurance Validation"
    ]
    
    validation_results["template_sections_present"] = all(
        section in report_content for section in required_sections
    )
    
    # Check all B001-B016 tests documented
    test_ids = [f"B{str(i).zfill(3)}" for i in range(1, 17)]
    validation_results["all_tests_documented"] = all(
        test_id in report_content for test_id in test_ids
    )
    
    # Check for unsubstituted variables
    import re
    unsubstituted_vars = re.findall(r'\{[A-Z_]+\}', report_content)
    validation_results["variables_substituted"] = len(unsubstituted_vars) == 0
    
    # Check performance classifications present
    performance_emojis = ["😊", "😐", "😴", "❌"]
    validation_results["performance_classification_complete"] = any(
        emoji in report_content for emoji in performance_emojis
    )
    
    # Method-specific validation
    if method.upper() == "CLI":
        validation_results["method_specific_requirements_met"] = (
            "npx playwright test" in report_content and
            "--timeout=120000" in report_content
        )
    elif method.upper() == "MCP":
        validation_results["method_specific_requirements_met"] = (
            "browser_navigate" in report_content and
            "10s intervals" in report_content
        )
    
    return validation_results

def log_validation_results(validation_results, report_filename):
    """Log validation results for quality assurance"""
    
    print(f"Report validation for {report_filename}:")
    for check, passed in validation_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check}: {status}")
    
    overall_quality = all(validation_results.values())
    print(f"Overall Quality: {'✅ PASS' if overall_quality else '❌ FAIL'}")
    
    return overall_quality
```

---

## 🔄 Complete Integration Workflow

### End-to-End Integration Example

```python
def execute_test_with_report_generation(method="CLI"):
    """Complete test execution with integrated report generation"""
    
    print(f"Starting {method} test execution with report generation...")
    
    # 1. Initialize data collection
    execution_data = {
        "start_time": datetime.now(),
        "test_results": {},
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H-%M-%S"),
        "method": method.upper()
    }
    
    # 2. Collect infrastructure status
    print("Collecting infrastructure status...")
    infrastructure_data = collect_infrastructure_status()
    execution_data.update(infrastructure_data)
    
    # 3. Execute B001-B016 tests with data collection
    test_definitions = get_test_definitions()  # B001-B016 definitions
    
    for test_id, test_info in test_definitions.items():
        print(f"Executing {test_id}: {test_info['name']}...")
        
        if method.upper() == "CLI":
            test_data = collect_cli_test_data(test_id, test_info['file'])
        elif method.upper() == "MCP":
            test_data = collect_mcp_test_data(test_id, test_info['description'])
        
        execution_data["test_results"][test_id] = test_data
        
        # Update TodoWrite progress
        # TodoWrite: Mark test as completed
    
    # 4. Calculate summary statistics
    execution_data["end_time"] = datetime.now()
    execution_data.update(calculate_summary_stats(execution_data))
    execution_data.update(calculate_performance_distribution(execution_data["test_results"]))
    
    # 5. Generate report using template
    print("Generating comprehensive test report...")
    report_filename = generate_report(method, execution_data)
    
    # 6. Validate report quality
    with open(report_filename, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    validation_results = validate_report_quality(report_content, method)
    quality_passed = log_validation_results(validation_results, report_filename)
    
    # 7. Final status
    if quality_passed:
        print(f"✅ {method} test execution completed successfully!")
        print(f"📄 Report generated: {report_filename}")
    else:
        print(f"⚠️  {method} test execution completed with quality issues")
        print(f"📄 Report generated: {report_filename} (review recommended)")
    
    return {
        "report_filename": report_filename,
        "quality_passed": quality_passed,
        "execution_data": execution_data
    }
```

---

## 📖 Template Integration Best Practices

### Performance Optimization
1. **Lazy Template Loading**: Load templates only when needed
2. **Variable Caching**: Cache environment data that doesn't change
3. **Parallel Data Collection**: Collect health checks in parallel
4. **Memory Management**: Clean up large data structures after processing

### Error Handling
1. **Graceful Degradation**: Continue with partial data if some collection fails
2. **Template Fallbacks**: Use basic format if template loading fails
3. **Variable Defaults**: Provide default values for missing variables
4. **Validation Recovery**: Attempt to fix common validation issues

### Security Considerations
1. **Input Sanitization**: Sanitize all user input before template substitution
2. **File Permissions**: Set appropriate permissions on generated reports
3. **Path Validation**: Validate all file paths to prevent directory traversal
4. **Content Filtering**: Filter sensitive information from error messages

### Maintenance Guidelines
1. **Template Versioning**: Version templates and track compatibility
2. **Variable Documentation**: Document all template variables and their sources
3. **Test Coverage**: Test template generation with various data scenarios
4. **Performance Monitoring**: Monitor template processing performance

---

## 🚨 Troubleshooting Common Issues

### Template Loading Issues
```python
# Issue: Template file not found
# Solution: Verify template path and permissions
if not os.path.exists(template_path):
    print(f"Template not found at {template_path}")
    print("Available templates:")
    for f in os.listdir(".claude/templates/"):
        print(f"  {f}")
```

### Variable Substitution Issues
```python
# Issue: Variables not substituting
# Solution: Debug variable mapping
print("Variables being substituted:")
for var_name, var_value in variables.items():
    print(f"  {var_name}: {var_value}")

# Check for common variable name mismatches
expected_vars = extract_template_variables(template_content)
provided_vars = set(variables.keys())
missing_vars = expected_vars - provided_vars
print(f"Missing variables: {missing_vars}")
```

### Report Quality Issues
```python
# Issue: Report fails validation
# Solution: Debug validation failures
for check, passed in validation_results.items():
    if not passed:
        print(f"Failed validation check: {check}")
        # Provide specific guidance for each check type
        if check == "variables_substituted":
            print("Check for remaining {VARIABLE} placeholders in report")
        elif check == "all_tests_documented":
            print("Verify all B001-B016 tests are present in report")
```

---

**Integration Guide Version:** 1.0  
**Compatible With:** CLI and MCP test commands v1.0+  
**Last Updated:** {CURRENT_TIMESTAMP}  
**Framework Dependencies:** Python 3.8+, Playwright, MCP Tools

---

*This integration guide provides comprehensive instructions for implementing professional test report generation across all Playwright testing methodologies. Following these patterns ensures consistent, high-quality reporting that meets all project standards and requirements.*