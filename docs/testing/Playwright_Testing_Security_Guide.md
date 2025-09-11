# Playwright Testing Security Best Practices Guide

**Secure Testing Environment and Safe Command Usage Guidelines**

This guide provides comprehensive security guidelines for safely using the Market Parser Playwright testing system, addressing vulnerabilities and establishing secure testing practices.

---

## 🛡️ Security Overview

### Security-First Testing Philosophy

The Market Parser Playwright testing system implements a security-first approach to ensure safe testing operations while maintaining comprehensive functionality. This guide addresses critical security considerations identified through code reviews and establishes mandatory security protocols.

### Threat Model

**Potential Security Risks:**
- **API Key Exposure**: Sensitive credentials leaked through logs or reports
- **Command Injection**: Malicious input through test parameters
- **Resource Exhaustion**: System overload through excessive testing
- **Network Exposure**: Testing services accessible from external networks
- **Data Leakage**: Sensitive financial data exposed in test artifacts
- **Environment Pollution**: Test data contaminating production systems

**Mitigation Strategy:**
- Environment isolation and validation
- Input sanitization and parameter validation
- Resource monitoring and limits
- Network security controls
- Data classification and handling procedures
- Comprehensive audit logging

---

## 🔒 Environment Security

### Secure Environment Configuration

#### API Key Management
```bash
# SECURE: Proper API key configuration
create_secure_env() {
    # Ensure .env file has restrictive permissions
    if [ -f ".env" ]; then
        chmod 600 .env
        echo "✅ .env file permissions secured (600)"
    else
        echo "❌ CRITICAL: .env file missing"
        echo "Create .env file with proper API keys before testing"
        return 1
    fi
    
    # Validate API key format without exposing values
    if grep -q "^POLYGON_API_KEY=" .env && [ $(grep "^POLYGON_API_KEY=" .env | wc -c) -gt 20 ]; then
        echo "✅ Polygon API key format appears valid"
    else
        echo "❌ SECURITY ERROR: Invalid or missing Polygon API key"
        return 1
    fi
    
    if grep -q "^OPENAI_API_KEY=" .env && [ $(grep "^OPENAI_API_KEY=" .env | wc -c) -gt 20 ]; then
        echo "✅ OpenAI API key format appears valid"
    else
        echo "❌ SECURITY ERROR: Invalid or missing OpenAI API key"
        return 1
    fi
}

# INSECURE: Never do this
# echo "API_KEY=$POLYGON_API_KEY" # Exposes key in process list
# cat .env                       # Exposes keys in logs
```

#### Environment Isolation Validation
```bash
# Comprehensive environment security check
validate_environment_security() {
    echo "🔍 Validating environment security..."
    
    # Check for development environment indicators
    if [ "$NODE_ENV" = "production" ]; then
        echo "🚨 SECURITY ALERT: Production environment detected"
        echo "Testing should only be performed in development environments"
        return 1
    fi
    
    # Verify network isolation
    local public_ip=$(curl -s --max-time 5 ipinfo.io/ip 2>/dev/null)
    if [ ! -z "$public_ip" ]; then
        echo "⚠️ SECURITY WARNING: Public internet access detected"
        echo "Consider running tests in isolated network environment"
        echo "Public IP: $public_ip"
    fi
    
    # Check for suspicious processes
    local suspicious_processes=$(ps aux | grep -E "(mining|crypto|bot|crawler)" | grep -v grep)
    if [ ! -z "$suspicious_processes" ]; then
        echo "🚨 SECURITY ALERT: Suspicious processes detected"
        echo "$suspicious_processes"
        return 1
    fi
    
    # Validate file permissions
    if [ -f ".env" ]; then
        local env_perms=$(stat -c "%a" .env)
        if [ "$env_perms" != "600" ]; then
            echo "⚠️ SECURITY WARNING: .env file permissions too open: $env_perms"
            echo "Recommend: chmod 600 .env"
        fi
    fi
    
    echo "✅ Environment security validation complete"
    return 0
}
```

#### Network Security Controls
```bash
# Network security validation and controls
network_security_check() {
    echo "🌐 Validating network security..."
    
    # Check listening ports
    local listening_ports=$(netstat -tlnp 2>/dev/null | grep LISTEN)
    
    # Validate backend server binding
    if echo "$listening_ports" | grep -q ":8000.*0.0.0.0"; then
        echo "⚠️ SECURITY WARNING: Backend server listening on all interfaces"
        echo "Consider binding to localhost only for development"
    elif echo "$listening_ports" | grep -q ":8000.*127.0.0.1"; then
        echo "✅ Backend server properly bound to localhost"
    fi
    
    # Validate frontend server binding
    if echo "$listening_ports" | grep -E ":3000|:3001|:3002|:3003" | grep -q "0.0.0.0"; then
        echo "⚠️ SECURITY WARNING: Frontend server may be externally accessible"
        echo "Ensure development environment is isolated"
    fi
    
    # Check for firewall status
    if command -v ufw >/dev/null 2>&1; then
        local ufw_status=$(ufw status | head -1)
        echo "🔥 Firewall status: $ufw_status"
    fi
    
    # Validate CORS configuration security
    local cors_test=$(curl -s -H "Origin: http://malicious.example.com" \
                          -H "Access-Control-Request-Method: POST" \
                          -X OPTIONS http://localhost:8000/templates 2>/dev/null)
    
    if echo "$cors_test" | grep -q "Access-Control-Allow-Origin: http://malicious.example.com"; then
        echo "🚨 SECURITY ALERT: CORS configuration allows external origins"
        echo "CORS should be restricted to localhost origins only"
    else
        echo "✅ CORS configuration appears secure"
    fi
    
    echo "✅ Network security validation complete"
}
```

---

## 🔐 Input Security and Validation

### Command Parameter Security

#### Safe Parameter Validation
```javascript
// Secure input validation for testing commands
class SecureInputValidator {
    constructor() {
        // Define whitelists for allowed inputs
        this.allowedTestIds = /^B00[1-9]$|^B01[0-6]$/;
        this.allowedTickers = /^[A-Z]{1,5}$/;
        this.allowedMethods = ['CLI', 'MCP'];
        this.maxStringLength = 100;
    }
    
    validateTestParameters(params) {
        const validated = {};
        
        // Validate test ID
        if (params.testId) {
            if (!this.allowedTestIds.test(params.testId)) {
                throw new SecurityError('Invalid test identifier: ' + params.testId);
            }
            validated.testId = params.testId;
        }
        
        // Validate ticker symbols
        if (params.ticker) {
            const cleanTicker = params.ticker.replace(/[^A-Z0-9]/g, '').toUpperCase();
            if (!this.allowedTickers.test(cleanTicker)) {
                throw new SecurityError('Invalid ticker symbol: ' + params.ticker);
            }
            if (cleanTicker.length > 5) {
                throw new SecurityError('Ticker symbol too long: ' + cleanTicker);
            }
            validated.ticker = cleanTicker;
        }
        
        // Validate method
        if (params.method && !this.allowedMethods.includes(params.method)) {
            throw new SecurityError('Invalid testing method: ' + params.method);
        }
        
        // Validate string lengths
        Object.keys(params).forEach(key => {
            if (typeof params[key] === 'string' && params[key].length > this.maxStringLength) {
                throw new SecurityError(`Parameter ${key} exceeds maximum length`);
            }
        });
        
        return validated;
    }
    
    sanitizeOutput(output) {
        // Remove sensitive information from output
        let sanitized = output
            .replace(/api_key[=:]\s*[^\s&"']*/gi, 'api_key=***')
            .replace(/token[=:]\s*[^\s&"']*/gi, 'token=***')
            .replace(/password[=:]\s*[^\s&"']*/gi, 'password=***')
            .replace(/secret[=:]\s*[^\s&"']*/gi, 'secret=***');
            
        // Remove potential SQL injection patterns
        sanitized = sanitized.replace(/(\b(DROP|DELETE|INSERT|UPDATE|SELECT)\s+)/gi, '[SQL_COMMAND_REMOVED]');
        
        // Remove potential XSS patterns
        sanitized = sanitized.replace(/<script[^>]*>.*?<\/script>/gi, '[SCRIPT_REMOVED]');
        
        return sanitized;
    }
}

// Usage example
const validator = new SecureInputValidator();

try {
    const safeParams = validator.validateTestParameters({
        testId: 'B001',
        ticker: 'NVDA',
        method: 'CLI'
    });
    console.log('✅ Parameters validated:', safeParams);
} catch (error) {
    console.error('🚨 Security validation failed:', error.message);
}
```

#### Command Injection Prevention
```bash
# Secure command execution patterns
execute_secure_command() {
    local test_id="$1"
    local method="$2"
    
    # Input validation
    if ! [[ "$test_id" =~ ^B00[1-9]$|^B01[0-6]$ ]]; then
        echo "🚨 SECURITY ERROR: Invalid test ID format: $test_id"
        return 1
    fi
    
    if [[ "$method" != "CLI" && "$method" != "MCP" ]]; then
        echo "🚨 SECURITY ERROR: Invalid method: $method"
        return 1
    fi
    
    # Secure command construction using arrays
    local cmd_array=()
    
    if [ "$method" = "CLI" ]; then
        cmd_array=("npx" "playwright" "test" "--timeout=120000" "--workers=1" "test-${test_id,,}.spec.ts")
    else
        echo "🚨 MCP method requires different validation approach"
        return 1
    fi
    
    # Execute with proper quoting and validation
    echo "🔒 Executing secure command: ${cmd_array[*]}"
    "${cmd_array[@]}"
    
    return $?
}

# INSECURE: Never construct commands like this
# eval "npx playwright test --timeout=120000 $user_input"  # Command injection risk
# bash -c "playwright test $test_id"                       # Shell injection risk
# system("npx playwright test " . $user_input);           # Command injection risk
```

---

## 📊 Data Security and Privacy

### Sensitive Data Handling

#### Financial Data Classification
```javascript
// Data classification and handling for financial information
class FinancialDataSecurity {
    constructor() {
        this.sensitiveFields = [
            'price', 'volume', 'market_cap', 'revenue',
            'earnings', 'balance_sheet', 'insider_trading',
            'api_key', 'token', 'secret', 'password'
        ];
        
        this.piiFields = [
            'email', 'phone', 'address', 'ssn', 'account_number'
        ];
    }
    
    classifyData(data) {
        const classification = {
            public: {},
            sensitive: {},
            pii: {},
            redacted: {}
        };
        
        Object.keys(data).forEach(key => {
            const value = data[key];
            
            if (this.piiFields.some(field => key.toLowerCase().includes(field))) {
                classification.pii[key] = this.redactPII(value);
                classification.redacted[key] = '***PII_REDACTED***';
            } else if (this.sensitiveFields.some(field => key.toLowerCase().includes(field))) {
                if (key.toLowerCase().includes('api_key') || 
                    key.toLowerCase().includes('token') ||
                    key.toLowerCase().includes('secret')) {
                    classification.redacted[key] = '***CREDENTIAL_REDACTED***';
                } else {
                    classification.sensitive[key] = value;
                }
            } else {
                classification.public[key] = value;
            }
        });
        
        return classification;
    }
    
    redactPII(value) {
        if (typeof value !== 'string') return value;
        
        // Redact common PII patterns
        return value
            .replace(/\b\d{3}-\d{2}-\d{4}\b/g, 'XXX-XX-XXXX')  // SSN
            .replace(/\b\d{3}-\d{3}-\d{4}\b/g, 'XXX-XXX-XXXX')  // Phone
            .replace(/\b[\w.-]+@[\w.-]+\.\w+\b/g, '***@***.***'); // Email
    }
    
    createSecureTestData(originalData) {
        const classified = this.classifyData(originalData);
        
        // Return only public and non-sensitive data for testing
        return {
            ...classified.public,
            metadata: {
                classification: 'test_data',
                timestamp: new Date().toISOString(),
                redacted_fields: Object.keys(classified.redacted)
            }
        };
    }
}
```

#### Secure Test Report Generation
```bash
# Secure test report generation with data sanitization
generate_secure_test_report() {
    local test_results="$1"
    local report_file="$2"
    
    echo "📝 Generating secure test report..."
    
    # Create temporary file with secure permissions
    local temp_report=$(mktemp --suffix=.md)
    chmod 600 "$temp_report"
    
    # Generate report header
    cat > "$temp_report" << EOF
# Playwright Test Execution Report
**Generated**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Environment**: Development (Isolated)
**Classification**: Internal Testing Data

## Security Notice
This report contains development testing data only.
All sensitive information has been redacted for security.

---

EOF
    
    # Process test results and sanitize sensitive data
    while IFS= read -r line; do
        # Remove API keys and tokens
        sanitized_line=$(echo "$line" | sed -E 's/(api_key[=:])[^[:space:]&"]*/\1***/gi')
        sanitized_line=$(echo "$sanitized_line" | sed -E 's/(token[=:])[^[:space:]&"]*/\1***/gi')
        
        # Redact potential sensitive financial data patterns
        sanitized_line=$(echo "$sanitized_line" | sed -E 's/\$[0-9]{4,}/\$****/g')
        
        # Remove potential PII
        sanitized_line=$(echo "$sanitized_line" | sed -E 's/\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b/XXX-XX-XXXX/g')
        
        echo "$sanitized_line" >> "$temp_report"
        
    done < "$test_results"
    
    # Add security footer
    cat >> "$temp_report" << EOF

---

## Security Summary
- All API keys and tokens redacted
- No PII included in this report
- Financial data patterns anonymized
- Report generated in secure environment

**Document Classification**: Internal Testing Data Only
**Retention Policy**: Delete after 30 days
EOF
    
    # Move to final location with secure permissions
    mv "$temp_report" "$report_file"
    chmod 600 "$report_file"
    
    echo "✅ Secure test report generated: $report_file"
    echo "🔒 File permissions: $(stat -c "%a" "$report_file")"
}
```

---

## 🚨 Incident Response and Security Monitoring

### Security Event Detection

#### Real-Time Security Monitoring
```bash
# Security monitoring during test execution
security_monitor() {
    echo "🛡️ Starting security monitoring..."
    
    local monitor_pid=$$
    local log_file="/tmp/security_monitor_$$.log"
    
    # Monitor for suspicious activities
    while true; do
        # Check for unusual network connections
        local external_connections=$(netstat -tn | grep ESTABLISHED | grep -v "127.0.0.1\|::1" | wc -l)
        if [ "$external_connections" -gt 5 ]; then
            echo "⚠️ SECURITY WARNING: High external connection count: $external_connections" | tee -a "$log_file"
        fi
        
        # Monitor CPU usage for suspicious spikes
        local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
        if (( $(echo "$cpu_usage > 95" | bc -l) )); then
            echo "⚠️ SECURITY WARNING: Extreme CPU usage: ${cpu_usage}%" | tee -a "$log_file"
        fi
        
        # Check for unexpected process creation
        local process_count=$(ps aux | wc -l)
        if [ "$process_count" -gt 300 ]; then
            echo "⚠️ SECURITY WARNING: High process count: $process_count" | tee -a "$log_file"
        fi
        
        # Monitor file system changes in sensitive directories
        if command -v inotifywait >/dev/null 2>&1; then
            timeout 5 inotifywait -q -e create,modify,delete .env /tmp 2>/dev/null && {
                echo "⚠️ SECURITY WARNING: Sensitive file system activity detected" | tee -a "$log_file"
            }
        fi
        
        sleep 10
    done &
    
    local monitor_bg_pid=$!
    echo "🔍 Security monitor started (PID: $monitor_bg_pid)"
    
    # Cleanup function
    trap "kill $monitor_bg_pid 2>/dev/null; rm -f $log_file" EXIT
    
    return 0
}
```

#### Security Incident Response
```bash
# Security incident response procedures
security_incident_response() {
    local incident_type="$1"
    local incident_details="$2"
    
    echo "🚨 SECURITY INCIDENT DETECTED"
    echo "Type: $incident_type"
    echo "Details: $incident_details"
    echo "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
    
    case "$incident_type" in
        "credential_exposure")
            echo "📞 IMMEDIATE ACTION REQUIRED:"
            echo "1. Revoke exposed API keys immediately"
            echo "2. Generate new API keys"
            echo "3. Update .env file with new keys"
            echo "4. Restart all services"
            echo "5. Review logs for unauthorized access"
            ;;
            
        "suspicious_network")
            echo "📞 NETWORK SECURITY INCIDENT:"
            echo "1. Isolate system from network if possible"
            echo "2. Check for malware/suspicious processes"
            echo "3. Review network logs"
            echo "4. Consider reimaging system if compromised"
            ;;
            
        "resource_exhaustion")
            echo "📞 RESOURCE SECURITY INCIDENT:"
            echo "1. Stop all non-essential processes"
            echo "2. Kill suspicious high-resource processes"
            echo "3. Check for denial-of-service attacks"
            echo "4. Monitor system recovery"
            ;;
            
        "data_breach")
            echo "📞 DATA SECURITY INCIDENT:"
            echo "1. Identify scope of data exposure"
            echo "2. Secure all data sources immediately"
            echo "3. Document incident details"
            echo "4. Notify relevant stakeholders"
            ;;
            
        *)
            echo "📞 UNKNOWN SECURITY INCIDENT:"
            echo "1. Document all available details"
            echo "2. Isolate affected systems"
            echo "3. Escalate to security team"
            ;;
    esac
    
    # Log incident for review
    local incident_log="security_incident_$(date +%Y%m%d_%H%M%S).log"
    {
        echo "SECURITY INCIDENT REPORT"
        echo "========================"
        echo "Timestamp: $(date -u)"
        echo "Type: $incident_type"
        echo "Details: $incident_details"
        echo "System: $(uname -a)"
        echo "User: $(whoami)"
        echo "Working Directory: $(pwd)"
        echo "Environment Variables:"
        env | grep -E "(NODE_ENV|ENVIRONMENT)" | head -5
        echo "Process List:"
        ps aux | head -10
        echo "Network Connections:"
        netstat -tn | grep ESTABLISHED | head -5
    } > "$incident_log"
    
    chmod 600 "$incident_log"
    echo "📝 Incident logged to: $incident_log"
}
```

---

## 🔧 Security Configuration Templates

### Secure Environment Templates

#### Production-Ready .env Template
```bash
# Secure .env template with validation
create_secure_env_template() {
    cat > .env.secure.template << 'EOF'
# Market Parser Playwright Testing - Secure Configuration Template
# WARNING: This file contains sensitive information - never commit to version control

# API Keys (Required)
# Obtain from: https://polygon.io/dashboard
POLYGON_API_KEY=your_polygon_api_key_here

# Obtain from: https://platform.openai.com/api-keys  
OPENAI_API_KEY=your_openai_api_key_here

# Security Configuration
NODE_ENV=development
ENVIRONMENT=testing
SECURITY_MODE=enabled

# Server Configuration (Secure Defaults)
FASTAPI_HOST=127.0.0.1  # Localhost only - more secure than 0.0.0.0
FASTAPI_PORT=8000
VITE_API_URL=http://127.0.0.1:8000

# CORS Configuration (Restrictive)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003

# Timeout Configuration (Conservative)
MCP_TIMEOUT_SECONDS=120
REQUEST_TIMEOUT=30

# Logging Configuration
LOG_LEVEL=INFO
AUDIT_LOGGING=true
SENSITIVE_DATA_REDACTION=true

# Performance Limits (Security-focused)
MAX_CONCURRENT_REQUESTS=10
MAX_REQUEST_SIZE=1MB
RATE_LIMIT_ENABLED=true
EOF

    echo "🔒 Secure .env template created: .env.secure.template"
    echo "📝 Copy to .env and add your actual API keys"
    echo "🔧 Adjust configuration as needed for your environment"
}
```

#### Docker Security Configuration
```dockerfile
# Secure Docker configuration for Playwright testing
# Dockerfile.secure
FROM node:18-alpine

# Create non-root user
RUN addgroup -g 1001 -S playwright && \
    adduser -S playwright -u 1001 -G playwright

# Set working directory with proper permissions
WORKDIR /app
RUN chown playwright:playwright /app

# Switch to non-root user
USER playwright

# Copy package files
COPY --chown=playwright:playwright package*.json ./
COPY --chown=playwright:playwright requirements.txt ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=playwright:playwright . .

# Set secure file permissions
RUN chmod -R 644 /app && \
    chmod 755 /app

# Security labels
LABEL security.level="development"
LABEL security.classification="internal-testing"

# Expose only necessary ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run as non-root user
USER playwright

# Secure entrypoint
CMD ["npm", "run", "start:secure"]
```

---

## 📋 Security Checklist and Compliance

### Pre-Testing Security Checklist

```markdown
## Security Validation Checklist

### Environment Security
- [ ] .env file exists with restrictive permissions (600)
- [ ] API keys are valid and properly formatted
- [ ] NODE_ENV is set to 'development' or 'testing'
- [ ] No suspicious processes running
- [ ] System resources within normal ranges
- [ ] Network environment is isolated/development only

### Server Security  
- [ ] Backend server bound to localhost (127.0.0.1) when possible
- [ ] Frontend server not externally accessible
- [ ] CORS configured for localhost origins only
- [ ] Health endpoints respond correctly
- [ ] No unauthorized listening ports

### Data Security
- [ ] Test data contains no real PII or sensitive information
- [ ] Output sanitization enabled
- [ ] Logging configured to redact sensitive data
- [ ] Temporary files use secure permissions
- [ ] No credentials in command line arguments

### Testing Security
- [ ] Input validation enabled for all parameters
- [ ] Command injection protection active
- [ ] Resource monitoring configured
- [ ] Timeout limits properly set
- [ ] Error handling prevents information disclosure

### Post-Testing Security
- [ ] Test reports contain no sensitive information
- [ ] Temporary files cleaned up
- [ ] No credentials left in logs
- [ ] System returned to clean state
- [ ] Security incidents documented if any occurred

## Compliance Requirements

### Development Environment
- Must not contain production data
- Must be isolated from production networks  
- Must use test/development API keys only
- Must implement proper access controls

### Data Handling
- All sensitive data must be redacted in outputs
- No PII should be processed during testing
- Financial data should be anonymized where possible
- Audit trail required for all testing activities

### Security Monitoring
- Resource usage monitoring required
- Network activity monitoring recommended
- Process monitoring for suspicious activity
- Incident response procedures must be followed
```

---

## 🎓 Security Training and Best Practices

### Security Awareness Training

#### Common Security Mistakes to Avoid
```bash
# ❌ INSECURE PRACTICES - Never do these:

# 1. Exposing API keys in commands
echo "Starting with key: $POLYGON_API_KEY"  # Visible in process list
npx playwright test --api-key=$API_KEY     # Exposed in commands

# 2. Insecure file permissions
chmod 777 .env                             # World readable/writable
cp .env /tmp/backup.env                    # Unsecured backup

# 3. Command injection vulnerabilities
eval "npx playwright test $user_input"     # Code injection risk
bash -c "test --param $untrusted_data"     # Shell injection

# 4. Information disclosure in logs
echo "Full response: $response" >> test.log  # May contain sensitive data
curl -v http://api.example.com             # Verbose output with headers

# 5. Insecure network configuration
uvicorn app:main --host 0.0.0.0 --port 8000  # Binds to all interfaces
CORS_ORIGINS="*"                           # Allows all origins
```

#### Secure Development Patterns
```bash
# ✅ SECURE PRACTICES - Always do these:

# 1. Secure API key handling
if [ -f ".env" ] && [ "$(stat -c %a .env)" = "600" ]; then
    source .env                            # Load from secure file
else
    echo "❌ .env file missing or insecure permissions"
    exit 1
fi

# 2. Input validation and sanitization
validate_ticker() {
    local ticker="$1"
    # Remove non-alphanumeric characters
    ticker=$(echo "$ticker" | tr -cd '[:alnum:]')
    # Convert to uppercase
    ticker=$(echo "$ticker" | tr '[:lower:]' '[:upper:]')
    # Validate length and format
    if [[ "$ticker" =~ ^[A-Z]{1,5}$ ]]; then
        echo "$ticker"
    else
        echo "❌ Invalid ticker format: $1" >&2
        return 1
    fi
}

# 3. Secure command execution
execute_playwright_test() {
    local test_id="$1"
    
    # Validate input
    if ! [[ "$test_id" =~ ^B00[1-9]$|^B01[0-6]$ ]]; then
        echo "❌ Invalid test ID: $test_id" >&2
        return 1
    fi
    
    # Use array to prevent injection
    local cmd=(npx playwright test --timeout=120000 --workers=1 "test-${test_id,,}.spec.ts")
    
    # Execute with proper error handling
    "${cmd[@]}" 2>&1 | tee "test_${test_id}_output.log"
    return "${PIPESTATUS[0]}"
}

# 4. Secure logging and output
log_test_result() {
    local test_id="$1"
    local result="$2"
    local sanitized_result
    
    # Sanitize sensitive information
    sanitized_result=$(echo "$result" | sed -E 's/(api_key[=:])[^[:space:]&"]*/\1***/gi')
    sanitized_result=$(echo "$sanitized_result" | sed -E 's/\$[0-9]{4,}/\$****/g')
    
    # Log to secure file
    echo "$(date -u): Test $test_id: $sanitized_result" >> test_results.log
    chmod 600 test_results.log
}
```

---

## 📞 Security Support and Escalation

### Security Contact Information

```markdown
## Security Support Contacts

### Internal Security Team
- **Primary**: Security Team Lead
- **Secondary**: Development Team Security Officer
- **Emergency**: Security Incident Response Team

### Escalation Procedures

#### Level 1: Minor Security Issues
- Configuration problems
- Permission issues
- Basic environment security

**Response Time**: 24 hours
**Contact**: Development team security representative

#### Level 2: Moderate Security Issues
- Suspicious network activity
- Potential credential exposure
- System resource abuse

**Response Time**: 4 hours
**Contact**: Security team escalation point

#### Level 3: Critical Security Incidents
- Confirmed credential compromise
- Active security breach
- System compromise indicators

**Response Time**: Immediate
**Contact**: Emergency security response team

### Documentation Requirements

All security incidents must be documented with:
- Incident timestamp and duration
- Affected systems and data
- Actions taken to mitigate
- Root cause analysis
- Preventive measures implemented
```

---

## 🏁 Conclusion

This Security Best Practices Guide provides comprehensive guidelines for safely using the Market Parser Playwright testing system. By following these security protocols, teams can conduct thorough testing while maintaining strong security posture.

### Key Security Principles

1. **Defense in Depth**: Multiple security layers protect against various threats
2. **Least Privilege**: Minimal access rights and permissions
3. **Input Validation**: All inputs are validated and sanitized
4. **Environment Isolation**: Testing occurs in secure, isolated environments
5. **Continuous Monitoring**: Real-time security monitoring during testing
6. **Incident Response**: Clear procedures for handling security events

### Implementation Priority

**High Priority (Immediate Implementation):**
- API key security and environment validation
- Input sanitization and validation
- Secure file permissions and data handling

**Medium Priority (Implement Soon):**
- Network security controls and monitoring
- Comprehensive audit logging
- Automated security checks

**Low Priority (Ongoing Improvement):**
- Advanced threat detection
- Security awareness training
- Compliance reporting automation

### Additional Resources

- **Quick Start Guide**: Basic security practices for immediate use
- **User Manual**: Detailed security procedures and protocols
- **Quality Assurance Guide**: Security integration with QA processes
- **Incident Response Playbook**: Detailed incident handling procedures

For security concerns or questions, refer to the escalation procedures outlined in this guide and contact the appropriate security personnel based on the severity and urgency of the issue.