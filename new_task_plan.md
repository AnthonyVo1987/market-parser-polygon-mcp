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

## Complete Implementation Plan for Environment Variable Migration

Based on my analysis using Serena tools, Sequential-thinking tools, and Context7 research, here's the comprehensive implementation plan for migrating environment variables to a centralized configuration file:

### 1. **Items to Migrate from .env Files to Configuration File**

**Backend Configuration:**

- ~~`OPENAI_MODEL`~~ → **REMOVED** - Handled by AI Model Selector feature
- `LOG_MODE` → Default: "DEBUG"
- `AGENT_SESSION_NAME` → Default: "finance_conversation"
- `MAX_CONTEXT_LENGTH` → Default: 128000
- `REPORTS_DIRECTORY` → Default: "test-reports"
- `ENABLE_RATE_LIMITING` → Default: true
- `RATE_LIMIT_RPM` → Default: 500
- `POLYGON_MCP_VERSION` → Default: "v0.4.0"
- `MCP_TIMEOUT_SECONDS` → Default: 120
- OpenAI pricing configurations

**Frontend Configuration:**

- `VITE_APP_ENV` → Default: "development"
- `VITE_DEBUG_MODE` → Default: true
- `VITE_PWA_ENABLED` → Default: true
- `VITE_HMR_ENABLED` → Default: true
- `VITE_SOURCE_MAP` → Default: true
- `VITE_BUNDLE_ANALYZER` → Default: true

### 2. **Environment Files to Delete**

- `.env.development`
- `.env.production`
- `.env.staging`
- Update `.env.example` to only show API key placeholders

### 3. **New Configuration Structure**

**File: `config/app.config.json`**

```json
{
  "backend": {
    "server": {
      "host": "127.0.0.1",
      "port": 8000
    },
    "ai": {
      "availableModels": ["gpt-5-nano", "gpt-5-mini", "gpt-4o", "gpt-4o-mini"],
      "maxContextLength": 128000,
      "pricing": {
        "gpt-5-nano": {
          "inputPer1M": 0.05,
          "outputPer1M": 0.40
        },
        "gpt-5-mini": {
          "inputPer1M": 0.25,
          "outputPer1M": 2.00
        },
        "gpt-4o": {
          "inputPer1M": 5.00,
          "outputPer1M": 15.00
        },
        "gpt-4o-mini": {
          "inputPer1M": 0.15,
          "outputPer1M": 0.60
        }
      }
    },
    "agent": {
      "sessionName": "finance_conversation",
      "reportsDirectory": "test-reports"
    },
    "mcp": {
      "version": "v0.4.0",
      "timeoutSeconds": 120
    },
    "security": {
      "enableRateLimiting": true,
      "rateLimitRPM": 500,
      "cors": {
        "origins": ["http://127.0.0.1:3000", "http://localhost:3000"]
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

### 4. **Code Changes Required**

**Backend (`src/backend/main.py`):**

- Create a `ConfigSettings` class that loads from `config/app.config.json`
- Update `Settings` class to read from config file instead of hardcoded values
- **Remove `openai_model` from Settings class** - The AI Model Selector will manage this
- Update all references to `settings.openai_model` to use the model from the AI Model Selector state
- Remove CORS_ORIGINS from environment, use config file

**Frontend:**

- Create a config loader utility that reads from `config/app.config.json`
- Update `vite.config.ts` to read server configuration from config file
- Update components to use config values instead of `import.meta.env`
- **AI Model Selector remains the single source of truth for model selection**

### 5. **Benefits of This Approach**

1. **Single Source of Truth**: All non-sensitive configuration in one file
2. **No Model Conflicts**: AI Model Selector exclusively manages model selection
3. **Cloud-Ready**: No dependency on environment-specific variables
4. **Type Safety**: Can generate TypeScript interfaces from JSON schema
5. **Searchable**: Configuration is now part of codebase, not hidden in env vars
6. **Version Control**: Configuration changes are tracked in git
7. **Predictable**: Static values ensure consistent behavior across deployments
8. **Development-Friendly**: Debug settings enabled by default for active development

### 6. **Migration Steps**

1. Create `config/` directory and `app.config.json` file
2. Update backend to load configuration from JSON file
3. **Remove all `openai_model` references from Settings class**
4. **Update backend endpoints to get model from AI Model Selector state/request**
5. Update frontend to load configuration from JSON file
6. Remove references to migrated environment variables
7. Delete unnecessary .env files
8. Update .env.example to only show API key format
9. Update documentation

### 7. **Key Implementation Details**

**Backend Configuration Loading (Python):**

```python
import json
from pathlib import Path

class ConfigSettings:
    def __init__(self):
        config_path = Path(__file__).parent.parent.parent / "config" / "app.config.json"
        with open(config_path) as f:
            self.config = json.load(f)
        
        # Backend settings
        self.backend = self.config["backend"]
        self.frontend = self.config["frontend"]
```

**Frontend Configuration Loading (TypeScript):**

```typescript
// config/config.loader.ts
import appConfig from '../../config/app.config.json';

export interface AppConfig {
  backend: {
    server: { host: string; port: number };
    ai: { availableModels: string[]; maxContextLength: number; pricing: any };
    agent: { sessionName: string; reportsDirectory: string };
    mcp: { version: string; timeoutSeconds: number };
    security: { enableRateLimiting: boolean; rateLimitRPM: number; cors: { origins: string[] } };
    logging: { mode: string };
  };
  frontend: {
    server: { host: string; port: number };
    api: { baseUrl: string };
    features: { appEnv: string; pwa: boolean; debugMode: boolean };
    development: { hmr: boolean; sourceMap: boolean; bundleAnalyzer: boolean };
  };
}

export const config: AppConfig = appConfig;
```

### 8. **Updated .env.example**

```env
# Market Parser Environment Configuration
# Copy this file to .env and fill in your actual API keys
# NEVER commit the actual .env file to version control

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔑 API KEYS ONLY - All other settings in config/app.config.json
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Required API Keys
POLYGON_API_KEY=your_polygon_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CONTEXT7_API_KEY=your_context7_api_key_here
GITHUB_PAT=your_github_personal_access_token_here
```

### 9. **Summary of Changes**

- **Removed**: Default model configuration - AI Model Selector manages this
- **Migrated**: All non-sensitive settings to `config/app.config.json`
- **Hardcoded**: Server addresses and ports for predictable cloud deployment
- **Simplified**: Only API keys remain in `.env` file
- **Enabled**: Full debug/development settings as defaults
- **Centralized**: Single configuration file for entire application

This approach ensures:

- No conflicts between configuration and feature-managed settings
- Easy deployment to cloud platforms (AWS, Azure, Google Cloud)
- Clear separation between secrets (API keys) and configuration
- Full visibility of all settings in version control
- Consistent behavior across all environments
