# Configuration Guide

## Overview

This document provides comprehensive guidance for configuring the Market Parser application, including the new GPT-5 model-specific rate limiting and performance optimizations.

## Configuration Files

### Primary Configuration: `config/app.config.json`

The main configuration file contains all non-sensitive application settings:

```json
{
  "backend": {
    "server": {
      "host": "127.0.0.1",
      "port": 8000
    },
    "ai": {
      "availableModels": [
        "gpt-5-nano",
        "gpt-5-mini"
      ],
      "maxContextLength": 128000,
      "temperature": 0.2,
      "pricing": {
        "gpt-5-nano": {
          "inputPer1M": 0.05,
          "outputPer1M": 0.40
        },
        "gpt-5-mini": {
          "inputPer1M": 0.25,
          "outputPer1M": 2.00
        }
      }
    },
    "agent": {
      "sessionName": "finance_conversation",
      "reportsDirectory": "test-reports"
    },
    "mcp": {
      "version": "v4.1.0",
      "timeoutSeconds": 120
    },
    "security": {
      "enableRateLimiting": true,
      "rateLimitRPM": 500,
      "rateLimiting": {
        "gpt5Nano": {
          "tpm": 200000,
          "rpm": 500
        },
        "gpt5Mini": {
          "tpm": 500000,
          "rpm": 500
        }
      },
      "cors": {
        "origins": [
          "http://127.0.0.1:3000",
          "http://localhost:3000"
        ]
      }
    },
    "logging": {
      "mode": "DEBUG"
    }
  },
  "frontend": {
    "server": {
      "host": "127.0.0.1",
      "port": 3000
    },
    "api": {
      "baseUrl": "/api"
    },
    "features": {
      "appEnv": "development",
      "pwa": true,
      "debugMode": true
    },
    "development": {
      "hmr": true,
      "sourceMap": true,
      "bundleAnalyzer": true
    }
  }
}
```

### Environment Configuration: `.env`

Sensitive configuration including API keys:

```bash
# Required API Keys
POLYGON_API_KEY=your_polygon_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Override default configuration
# FASTAPI_HOST=127.0.0.1
# FASTAPI_PORT=8000
# FRONTEND_PORT=3000
```

## GPT-5 Model Configuration

### Available Models

The application now supports only GPT-5 models with proper rate limiting:

- **GPT-5 Nano**: Fast and efficient model for quick responses
  - **TPM Limit**: 200,000 tokens per minute
  - **RPM Limit**: 500 requests per minute
  - **Cost**: $0.05/1M input tokens, $0.40/1M output tokens
  - **Max Tokens**: 4,096

- **GPT-5 Mini**: Balanced performance model
  - **TPM Limit**: 500,000 tokens per minute
  - **RPM Limit**: 500 requests per minute
  - **Cost**: $0.25/1M input tokens, $2.00/1M output tokens
  - **Max Tokens**: 8,192

### Model Selection

The application automatically selects the first model from the `availableModels` array:

```json
{
  "ai": {
    "availableModels": [
      "gpt-5-nano",    // Primary model (default)
      "gpt-5-mini"     // Secondary model
    ]
  }
}
```

## Rate Limiting Configuration

### GPT-5 Model-Specific Rate Limiting

The new rate limiting system provides model-specific limits to prevent rate limiting errors:

```json
{
  "security": {
    "enableRateLimiting": true,
    "rateLimitRPM": 500,
    "rateLimiting": {
      "gpt5Nano": {
        "tpm": 200000,    // 200K tokens per minute
        "rpm": 500        // 500 requests per minute
      },
      "gpt5Mini": {
        "tpm": 500000,    // 500K tokens per minute
        "rpm": 500        // 500 requests per minute
      }
    }
  }
}
```

### Rate Limiting Benefits

- **Prevents Rate Limit Errors**: No more "Request too large for gpt-4o" errors
- **Optimized Performance**: Uses proper GPT-5 model limits instead of gpt-4o limits
- **Scalable**: Supports high-volume requests with appropriate limits
- **Model-Aware**: Automatically adjusts limits based on selected model

## Polygon MCP Server Configuration

### Version Update

The Polygon MCP server has been updated to the latest version:

```json
{
  "mcp": {
    "version": "v4.1.0",        // Updated from v0.4.0
    "timeoutSeconds": 120
  }
}
```

### Benefits of v4.1.0

- **Enhanced Market Data**: Improved data accuracy and coverage
- **Better Performance**: Optimized API calls and response times
- **New Features**: Additional market data endpoints and capabilities
- **Bug Fixes**: Resolved issues from previous versions

## Performance Configuration

### Quick Response Optimization

All AI agents now enforce quick response behavior:

- **Minimal Tool Calls**: Agents prioritize speed over exhaustive analysis
- **Optimized Prompts**: All system prompts include "Quick Response Needed" prefix
- **Response Time**: 20-40% faster response times expected
- **Efficiency**: Reduced token usage while maintaining quality

### Temperature Settings

```json
{
  "ai": {
    "temperature": 0.2    // Deterministic financial analysis
  }
}
```

- **Low Temperature (0.2)**: Ensures consistent, deterministic responses
- **Financial Focus**: Optimized for financial analysis accuracy
- **Reduced Variability**: More predictable output for trading decisions

## Security Configuration

### CORS Settings

```json
{
  "security": {
    "cors": {
      "origins": [
        "http://127.0.0.1:3000",
        "http://localhost:3000"
      ]
    }
  }
}
```

### Rate Limiting

- **Global Rate Limit**: 500 requests per minute per IP
- **Model-Specific Limits**: TPM limits based on GPT-5 model capabilities
- **Request Validation**: Input validation and ticker symbol verification

## Frontend Configuration

### Development Settings

```json
{
  "frontend": {
    "features": {
      "appEnv": "development",
      "pwa": true,
      "debugMode": true
    },
    "development": {
      "hmr": true,              // Hot Module Replacement
      "sourceMap": true,        // Source maps for debugging
      "bundleAnalyzer": true    // Bundle analysis
    }
  }
}
```

### Production Settings

For production deployment, update the configuration:

```json
{
  "frontend": {
    "features": {
      "appEnv": "production",
      "pwa": true,
      "debugMode": false
    },
    "development": {
      "hmr": false,
      "sourceMap": false,
      "bundleAnalyzer": false
    }
  }
}
```

## Configuration Validation

### Backend Validation

The application validates configuration on startup:

```python
# Configuration validation in main.py
def validate_configuration():
    """Validate configuration settings."""
    # Check required API keys
    if not settings.polygon_api_key:
        raise ConfigurationError("POLYGON_API_KEY is required")
    
    if not settings.openai_api_key:
        raise ConfigurationError("OPENAI_API_KEY is required")
    
    # Validate model configuration
    if not settings.available_models:
        raise ConfigurationError("At least one AI model must be configured")
    
    # Validate rate limiting configuration
    if settings.enable_rate_limiting:
        if not hasattr(settings, 'gpt5_nano_tpm'):
            raise ConfigurationError("GPT-5 rate limiting configuration missing")
    
    return True
```

### Frontend Validation

```typescript
// Configuration validation in config.loader.ts
export const validateConfig = (config: AppConfig): boolean => {
  // Validate required fields
  if (!config.backend?.server?.host) {
    throw new Error('Backend host is required');
  }
  
  if (!config.backend?.server?.port) {
    throw new Error('Backend port is required');
  }
  
  // Validate AI model configuration
  if (!config.backend?.ai?.availableModels?.length) {
    throw new Error('At least one AI model must be configured');
  }
  
  return true;
};
```

## Configuration Updates

### Recent Changes

The following configuration changes have been implemented:

1. **GPT-5 Model Support**: Removed GPT-4o models, added GPT-5 model-specific rate limiting
2. **Rate Limiting Enhancement**: Added model-specific TPM and RPM limits
3. **Polygon MCP Update**: Updated to version v4.1.0
4. **Quick Response Optimization**: All prompts optimized for faster responses

### Migration Guide

If upgrading from a previous version:

1. **Update Configuration**: Add the new `rateLimiting` section to your `app.config.json`
2. **Remove GPT-4o References**: Ensure only GPT-5 models are in `availableModels`
3. **Update Polygon Version**: Change MCP version to "v4.1.0"
4. **Test Configuration**: Run the application to validate all settings

## Troubleshooting

### Common Configuration Issues

**Rate Limiting Errors:**

```
Request too large for gpt-4o in organization org-xxx on tokens per min (TPM): Limit 30000, Requested 32099
```

**Solution**: Ensure GPT-5 models are properly configured and rate limiting is set to GPT-5 limits.

**Model Not Found:**

```
Model 'gpt-4o' not found
```

**Solution**: Remove GPT-4o references and use only GPT-5 models in configuration.

**API Key Issues:**

```
Invalid API key
```

**Solution**: Verify API keys are correctly set in `.env` file and have sufficient credits.

### Configuration Validation

Run configuration validation:

```bash
# Backend validation
uv run src/backend/main.py --validate-config

# Frontend validation
npm run validate-config
```

## Best Practices

1. **Environment Separation**: Use different configurations for development, staging, and production
2. **API Key Security**: Never commit API keys to version control
3. **Rate Limit Monitoring**: Monitor rate limit usage and adjust as needed
4. **Model Selection**: Choose appropriate model based on use case (nano for speed, mini for complexity)
5. **Configuration Validation**: Always validate configuration before deployment
6. **Backup Configuration**: Keep backup copies of working configurations

## Support

For configuration issues:

1. Check the troubleshooting section above
2. Validate your configuration files
3. Review the application logs for specific error messages
4. Ensure all required API keys are properly set
5. Verify network connectivity and API service status
