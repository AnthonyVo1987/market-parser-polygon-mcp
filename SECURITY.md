# Security Guidelines

## Critical Security Requirements

### 🔒 API Key Management

**NEVER** commit API keys to version control. This project requires several API keys:

- `POLYGON_API_KEY` - For real-time market data
- `OPENAI_API_KEY` - For AI agent processing  
- `ANTHROPIC_API_KEY` - Optional for alternative AI models
- `GEMINI_API_KEY` - Optional for additional AI capabilities

### 🛡️ Secure Setup Process

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to .env:**
   ```bash
   # Edit .env with your actual keys
   POLYGON_API_KEY=your_actual_key_here
   OPENAI_API_KEY=your_actual_key_here
   ```

3. **Verify .env is ignored:**
   ```bash
   # Ensure .env is in .gitignore
   grep -q "^.env$" .gitignore && echo "✅ .env is protected" || echo "❌ Add .env to .gitignore"
   ```

### 🔍 Input Validation

All user inputs are validated:
- Stock ticker symbols are sanitized and validated against known patterns
- Numeric inputs are type-checked and range-validated  
- Query strings are length-limited and content-filtered

### 📝 Secure Logging

- **Production logs NEVER contain:**
  - API keys or tokens
  - Full API response bodies
  - User personal information
  - Raw debug output

- **Debug mode restrictions:**
  - Only enable in development environments
  - Automatic sanitization of sensitive data
  - Structured logging with severity levels

### 🚨 Security Incident Response

If API keys are accidentally exposed:

1. **Immediately revoke** the exposed keys at provider dashboards
2. **Generate new keys** and update .env file
3. **Check git history** for any committed keys
4. **Review logs** for unauthorized usage

### 🔐 Production Deployment

- Use environment variables instead of .env files
- Enable TLS/SSL for all network communications
- Implement rate limiting on API endpoints
- Regular security audits of dependencies
- Monitor for unusual API usage patterns

### ⚠️ Known Security Considerations

- This application processes external API data from financial markets
- AI responses may contain market-sensitive information
- Rate limiting prevents abuse but doesn't guarantee data freshness
- MCP server connections should be encrypted in production

### 📞 Reporting Security Issues

Report security vulnerabilities privately to the maintainers.
Do NOT open public issues for security vulnerabilities.