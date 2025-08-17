# Market Parser API Design Guidelines

## Overview

This document defines the API design standards and guidelines for the Market Parser JSON schema re-architecture. These guidelines ensure consistency, maintainability, and reliability across all financial data endpoints.

## Core Design Principles

### 1. Consistency Over Cleverness
- Follow established HTTP semantics and JSON schema patterns
- Use standardized field names and data types across all schemas
- Maintain consistent error response formats

### 2. Least Privilege Security
- Include only necessary data in responses
- Implement proper field validation and constraints
- Use standardized authentication patterns

### 3. Explicit Error Handling
- Use RFC 9457-compliant error responses
- Provide field-level validation details
- Include actionable error messages

### 4. Documentation by Example
- Include comprehensive example responses
- Provide validation scenarios and edge cases
- Document all schema constraints and business rules

## Schema Design Standards

### Naming Conventions

#### Field Names
- Use `snake_case` for all JSON field names
- Be descriptive but concise: `current_price` not `cp` or `current_stock_price`
- Use consistent terminology across schemas:
  - `ticker_symbol` (not `symbol`, `ticker`, or `stock_symbol`)
  - `timestamp` (not `time`, `date`, or `created_at`)
  - `confidence_score` (not `confidence`, `score`, or `reliability`)

#### Schema Identifiers
- Use clear, hierarchical schema IDs: `https://market-parser.com/schemas/{type}/v{version}`
- Version schemas semantically: `v1.0`, `v1.1`, `v2.0`
- Include schema version in response metadata

### Data Type Standards

#### Monetary Values
```json
{
  "type": "number",
  "minimum": 0.01,
  "maximum": 1000000,
  "multipleOf": 0.01,
  "description": "Price in USD with 2 decimal precision"
}
```

#### Percentages
```json
{
  "type": "number",
  "minimum": -99.99,
  "maximum": 999.99,
  "description": "Percentage value (e.g., 2.5 for 2.5%)"
}
```

#### Ticker Symbols
```json
{
  "type": "string",
  "pattern": "^[A-Z]{1,5}$",
  "description": "Stock ticker symbol in uppercase"
}
```

#### Timestamps
```json
{
  "type": "string",
  "format": "date-time",
  "description": "ISO 8601 timestamp with timezone"
}
```

### Required Headers

#### Request Headers
- `Content-Type: application/json`
- `Accept: application/json`
- `User-Agent: market-parser/1.0`
- `X-Request-ID: {uuid}` (for tracing)

#### Response Headers
- `Content-Type: application/json; charset=utf-8`
- `X-Schema-Version: {version}`
- `X-Response-Time: {milliseconds}ms`
- `X-Request-ID: {uuid}` (echo from request)

## Authentication & Security

### API Key Authentication
```http
Authorization: Bearer {api_key}
X-API-Version: 1.0
```

### Rate Limiting
- **Default**: 100 requests per minute per API key
- **Burst**: 10 requests per second
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

### Security Headers
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

## Response Format Standards

### Successful Response Structure
```json
{
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "ticker_symbol": "AAPL",
    "schema_version": "1.0",
    "confidence_score": 0.95
  },
  "data": {
    // Analysis-specific data structure
  },
  "validation": {
    "data_freshness": "real-time",
    "warnings": []
  }
}
```

### Error Response Structure
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field_errors": [
        {
          "field": "ticker_symbol",
          "error_code": "INVALID_FORMAT",
          "message": "Ticker must be 1-5 uppercase letters",
          "rejected_value": "aapl"
        }
      ]
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

## Endpoint Design Patterns

### REST Resource Structure
```
POST /api/v1/analysis/snapshot
POST /api/v1/analysis/support-resistance  
POST /api/v1/analysis/technical
GET  /api/v1/schemas/{type}
GET  /api/v1/health
```

### Request/Response Examples

#### Snapshot Analysis Request
```http
POST /api/v1/analysis/snapshot HTTP/1.1
Content-Type: application/json
Authorization: Bearer {api_key}
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000

{
  "ticker_symbol": "AAPL",
  "options": {
    "include_validation": true,
    "data_source": "real-time"
  }
}
```

#### Snapshot Analysis Response
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
X-Schema-Version: 1.0
X-Response-Time: 245ms
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000

{
  "metadata": {
    "timestamp": "2025-01-15T10:30:00Z",
    "ticker_symbol": "AAPL",
    "company_name": "Apple Inc.",
    "data_source": "polygon",
    "confidence_score": 0.95,
    "schema_version": "1.0"
  },
  "snapshot_data": {
    "current_price": 150.25,
    "percentage_change": 2.5,
    "dollar_change": 3.75,
    "volume": 45000000,
    "vwap": 149.80,
    "open": 148.50,
    "high": 151.00,
    "low": 147.25,
    "close": 146.50
  },
  "validation": {
    "data_freshness": "real-time",
    "market_status": "open",
    "warnings": []
  }
}
```

## Validation Rules

### Business Logic Validation
1. **Price Consistency**: `high >= current_price >= low`
2. **Volume Validation**: Non-negative integers only
3. **Percentage Bounds**: Daily changes typically -50% to +500%
4. **Support/Resistance Logic**: S3 < S2 < S1 < current_price < R1 < R2 < R3
5. **RSI Bounds**: Must be between 0 and 100
6. **Moving Average Ordering**: Shorter periods generally more reactive

### Data Quality Checks
- **Freshness**: Include data age indicators
- **Completeness**: Flag missing required fields
- **Consistency**: Cross-validate related fields
- **Market Context**: Consider market hours and holidays

## Error Handling Strategies

### Error Categories
1. **Client Errors (4xx)**
   - `400 Bad Request`: Invalid request format
   - `401 Unauthorized`: Invalid or missing API key
   - `422 Unprocessable Entity`: Validation failures
   - `429 Too Many Requests`: Rate limit exceeded

2. **Server Errors (5xx)**
   - `500 Internal Server Error`: Unexpected server error
   - `502 Bad Gateway`: Upstream data source unavailable
   - `503 Service Unavailable`: Temporary service issues
   - `504 Gateway Timeout`: Data source timeout

### Error Response Examples

#### Validation Error (422)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field_errors": [
        {
          "field": "snapshot_data.current_price",
          "error_code": "OUT_OF_RANGE",
          "message": "Price must be between 0.01 and 1,000,000",
          "rejected_value": -5.50
        }
      ]
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

#### Rate Limit Error (429)
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "details": {
      "limit": 100,
      "reset_time": "2025-01-15T10:31:00Z",
      "retry_after": 60
    },
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

## Versioning Strategy

### Schema Versioning
- **Major Version (v1.0 → v2.0)**: Breaking changes
  - Field removal or renaming
  - Type changes (string → number)
  - Required field additions
  
- **Minor Version (v1.0 → v1.1)**: Backward-compatible additions
  - New optional fields
  - New enum values
  - Expanded validation ranges

- **Patch Version (v1.0.1 → v1.0.2)**: Bug fixes
  - Constraint corrections
  - Documentation updates
  - Example improvements

### API Versioning
- **URL Versioning**: `/api/v1/`, `/api/v2/`
- **Header Versioning**: `X-API-Version: 1.0`
- **Deprecation Timeline**: 12 months notice for breaking changes

## Performance Guidelines

### Response Size Optimization
- **Snapshot**: Target < 2KB per response
- **Support/Resistance**: Target < 1KB per response  
- **Technical**: Target < 3KB per response
- **Compression**: Always use gzip compression

### Caching Strategy
- **Response TTL**: 
  - Real-time data: 30 seconds
  - Delayed data: 15 minutes
  - Technical indicators: 5 minutes
- **Cache Headers**: Include `Cache-Control` and `ETag`

### Rate Limits
- **Standard Tier**: 100 requests/minute
- **Premium Tier**: 1000 requests/minute
- **Enterprise Tier**: Custom limits

## Testing & Quality Assurance

### Schema Validation Tests
```python
def test_snapshot_schema_validation():
    """Test snapshot response against JSON schema"""
    response = generate_snapshot_response("AAPL")
    result = schema_registry.validate_response(response, AnalysisType.SNAPSHOT)
    assert result["valid"] == True
```

### API Contract Tests
```python
def test_api_response_structure():
    """Test API response includes all required fields"""
    response = call_snapshot_api("AAPL")
    assert "metadata" in response
    assert "snapshot_data" in response
    assert response["metadata"]["schema_version"] == "1.0"
```

### Performance Tests
- **Response Time**: < 500ms for 95th percentile
- **Throughput**: Handle 1000 concurrent requests
- **Error Rate**: < 0.1% for valid requests

## Documentation Standards

### Schema Documentation
- **Field Descriptions**: Clear, business-focused explanations
- **Validation Rules**: Document all constraints and their business rationale
- **Examples**: Provide realistic example data
- **Error Cases**: Document common validation failures

### API Documentation
- **OpenAPI 3.1**: Complete specification with examples
- **Interactive Docs**: Swagger UI or similar
- **SDK Examples**: Code samples in Python, JavaScript, etc.
- **Postman Collection**: Pre-configured API tests

## Migration Guidelines

### From Text Parsing to JSON Schema
1. **Phase 1**: Implement parallel JSON endpoints
2. **Phase 2**: Update AI prompts for structured output
3. **Phase 3**: Deprecate text parsing endpoints
4. **Phase 4**: Remove legacy parsing code

### Backward Compatibility
- **Bridge Period**: 6 months of parallel operation
- **Response Transformation**: Convert JSON to legacy format
- **Feature Flags**: Control rollout per client
- **Monitoring**: Track adoption metrics

## Compliance & Security

### Data Privacy
- **PII Handling**: No personal data in financial responses
- **Data Retention**: Anonymized logging only
- **GDPR Compliance**: Right to data deletion

### Financial Regulations
- **Disclaimer Requirements**: Include data source disclaimers
- **Real-time vs Delayed**: Clear data freshness indicators
- **Accuracy Limitations**: Document confidence scoring

### Security Standards
- **HTTPS Only**: TLS 1.2+ required
- **API Key Rotation**: Support key lifecycle management  
- **Input Validation**: Strict schema enforcement
- **Output Sanitization**: Prevent data injection

## Monitoring & Observability

### Key Metrics
- **Response Times**: P50, P95, P99 latencies
- **Error Rates**: By error type and endpoint
- **Schema Validation**: Success/failure rates
- **Data Quality**: Confidence score distributions

### Alerting Thresholds
- **Error Rate**: > 1% for 5 minutes
- **Response Time**: P95 > 1000ms for 3 minutes  
- **Validation Failures**: > 5% for 2 minutes
- **Rate Limit Hits**: > 10/minute for any client

### Logging Standards
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "endpoint": "/api/v1/analysis/snapshot",
  "ticker": "AAPL",
  "response_time_ms": 245,
  "status_code": 200,
  "schema_validation": "success",
  "confidence_score": 0.95
}
```

## Implementation Checklist

### Pre-Production
- [ ] Schema validation tests pass
- [ ] API contract tests pass  
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Monitoring configured

### Production Deployment
- [ ] Feature flags configured
- [ ] Rollout plan approved
- [ ] Rollback procedures tested
- [ ] Support team trained
- [ ] Client migration scheduled
- [ ] Success metrics defined

### Post-Production
- [ ] Monitor error rates and performance
- [ ] Track schema validation success rates
- [ ] Collect client feedback
- [ ] Plan iterative improvements
- [ ] Schedule regular schema reviews
- [ ] Update documentation as needed

---

This specification provides a comprehensive foundation for implementing robust, maintainable JSON APIs for financial data analysis.