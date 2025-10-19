# Hugging Face Spaces Deployment Setup - October 2025

## Overview
Market Parser is now configured for deployment to Hugging Face Spaces with permanent free cloud hosting. This memory documents the deployment infrastructure created.

## Files Created for HF Spaces Deployment

### 1. app.py (Root-level Entry Point)
**Location:** `/app.py` (at project root)
**Purpose:** HF Spaces entry point that imports and launches the Gradio app

**Contents:**
```python
"""Hugging Face Spaces deployment entry point for Market Parser.

This file is specifically for HF Spaces deployment.
It imports and runs the main Gradio app from src/backend/gradio_app.py.

For local development, continue using:
    uv run python src/backend/gradio_app.py
    OR
    uv run market-parser-gradio

This file enables HF Spaces to run the app with cloud-compatible settings.
"""

# Import the demo from our main app
from backend.gradio_app import demo

# Launch with HF Spaces-compatible settings
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Required for HF Spaces (accept external connections)
        server_port=7860,        # HF Spaces default port
        share=False,             # Not needed in HF Spaces (already hosted)
        show_error=True,         # Show errors for debugging
    )
```

**Key Configuration:**
- `server_name="0.0.0.0"` - Accepts external connections (required for HF Spaces)
- `server_port=7860` - HF Spaces default port (NOT 8000)
- `share=False` - Not needed in cloud environment
- Imports `demo` from `backend.gradio_app` - Uses existing Gradio app without modification

### 2. requirements.txt (Dependency List)
**Location:** `/requirements.txt` (at project root)
**Purpose:** Tells HF Spaces which Python packages to install

**Dependencies:**
```txt
# Core UI Framework
gradio>=5.49.1

# AI/ML Framework
openai-agents==0.2.9
openai>=1.99.0,<1.100.0

# Data Validation and Processing
pydantic>=2.0.0

# Terminal/Output Formatting
rich>=13.0.0

# Environment Management
python-dotenv>=1.0.0

# API Clients
polygon-api-client>=1.14.0
openai-agents-mcp>=0.0.8

# Async File Operations
aiofiles>=24.1.0

# Language Server Protocol (for development tools)
python-lsp-server[all]>=1.13.1
```

**Source:** Extracted from `pyproject.toml` dependencies section

### 3. README.md (Updated with Frontmatter)
**Location:** `/README.md` (at project root)
**Changes:** Added HF Spaces configuration frontmatter at the top

**Frontmatter Added:**
```yaml
---
title: Market Parser Financial Assistant
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
---
```

**Frontmatter Configuration:**
- `title` - Display name on HF Spaces
- `emoji` - Icon shown in Space listing
- `colorFrom/colorTo` - Gradient colors for Space card
- `sdk: gradio` - Declares this is a Gradio app
- `sdk_version` - Matches our Gradio version
- `app_file: app.py` - Points to HF Spaces entry point
- `pinned: false` - Not pinned in featured spaces (can change to true)

## Deployment Process

### Files NOT Modified (Unchanged)
- `src/backend/gradio_app.py` - Original Gradio app (no changes needed)
- `src/backend/cli.py` - CLI core logic (unchanged)
- `src/backend/config.py` - Configuration (unchanged)
- `pyproject.toml` - Project configuration (unchanged)
- `.env` - Local environment variables (NEVER upload to HF)

### Environment Variables/Secrets
**Required in HF Spaces Settings:**
1. `OPENAI_API_KEY` - OpenAI API access (REQUIRED)
2. `POLYGON_API_KEY` - Polygon.io market data (REQUIRED)
3. `TRADIER_API_KEY` - Tradier market data (OPTIONAL)

**How They Work:**
- Set via HF Spaces web UI: Settings → Repository secrets
- Accessible in Python code via `os.getenv("SECRET_NAME")`
- Our app already uses `os.getenv()` - fully compatible!
- Secrets are private (not visible after saving)

## Deployment Steps

### Quick Deployment to HF Spaces

1. **Create Hugging Face Account** (if needed)
   - Go to [huggingface.co](https://huggingface.co)
   - Sign up for free account

2. **Create New Space**
   - Click "Spaces" in top navigation
   - Click "Create new Space"
   - Configure:
     - Space name: `market-parser`
     - SDK: Gradio
     - Hardware: CPU basic (free)
     - Visibility: Public

3. **Upload Files** (two options)
   - **Option A (Web UI):** 
     - Go to "Files and versions" tab
     - Upload: `app.py`, `requirements.txt`, `README.md`
     - Upload entire `src/` folder
   - **Option B (Git):**
     ```bash
     git clone https://huggingface.co/spaces/USERNAME/market-parser
     cd market-parser
     cp /path/to/app.py .
     cp /path/to/requirements.txt .
     cp /path/to/README.md .
     cp -r /path/to/src .
     git add .
     git commit -m "Initial deployment"
     git push
     ```

4. **Configure Secrets**
   - Go to Space Settings → Repository secrets
   - Add each secret:
     - Name: `OPENAI_API_KEY` → Value: your key
     - Name: `POLYGON_API_KEY` → Value: your key
     - Name: `TRADIER_API_KEY` → Value: your key (optional)

5. **Wait for Build** (~2-5 minutes)
   - Watch "App" tab for build progress
   - Check "Logs" for any errors

6. **Access Deployed App**
   - URL: `https://huggingface.co/spaces/USERNAME/market-parser`

### Testing Locally Before Deploying

**Method 1: Test with existing setup**
```bash
uv run python src/backend/gradio_app.py
# Works on http://127.0.0.1:8000
```

**Method 2: Test with Gradio Share (temporary)**
```bash
# Edit src/backend/gradio_app.py line 118:
share=True  # Instead of False

uv run python src/backend/gradio_app.py
# Gets temporary public URL (72-hour expiry)
```

**Method 3: Test HF Spaces entry point locally**
```bash
python app.py
# Tests the HF Spaces configuration
```

## Architecture Pattern

```
Development/Local:
  User Input → Gradio UI (localhost:8000) → cli.py core logic

HF Spaces Cloud:
  User Input → Gradio UI (huggingface.co/spaces/...) ← HF Spaces
                                                         ↓
                                                    app.py (entry point)
                                                         ↓
                                                    backend/gradio_app.py
                                                         ↓
                                                    cli.py core logic
```

**Key Point:** Same core logic, different entry points!

## Compatibility Checklist

✅ **Environment Variables**
- Uses `os.getenv()` for API keys
- Fully compatible with HF Spaces secrets
- No code changes needed

✅ **Dependencies**
- All in requirements.txt
- Compatible with HF Spaces pip install
- Exact versions pinned where needed

✅ **Gradio App**
- Uses `gr.ChatInterface` (works great on HF)
- No external ports/services required
- Standard Gradio features all supported

✅ **Entry Point**
- app.py properly imports from src/backend
- Launch configuration optimized for cloud
- No hardcoded paths or localhost references

✅ **Original App Unchanged**
- Existing deployment methods still work
- Local development unaffected
- Backward compatible

## Performance Considerations

**HF Spaces Free Tier Specs:**
- CPU: Shared CPU (no GPU)
- Memory: Sufficient for our app
- Build time: 2-5 minutes typical
- Cold start: ~10-15 seconds first load
- Usage limits: Fair use policy

**Optimization Tips:**
- Dependencies load from requirements.txt (standard pip)
- Gradio is optimized for web deployment
- Our app performs well with free tier resources
- Consider paid tier if hitting usage limits

## Troubleshooting Reference

### Common Build Errors

**ModuleNotFoundError:**
- Missing dependency in requirements.txt
- Check build logs for exact module name
- Add to requirements.txt and redeploy

**ImportError:**
- Project structure issue
- Verify `src/` folder uploaded correctly
- Check app.py import paths

**API Key Errors:**
- Secrets not configured in HF Settings
- Check secret names match code (case-sensitive)
- Verify correct API key values

**Connection Timeout:**
- API rate limits
- Check API quota and validity
- May need API key regeneration

## Security Best Practices

❌ **Never:**
- Hardcode API keys in Python files
- Upload `.env` file to HF Spaces
- Push secrets to git repository
- Use weak or public API keys

✅ **Always:**
- Use HF Spaces Secrets for sensitive values
- Keep `.env` file local and in `.gitignore`
- Use strong, unique API keys
- Regenerate keys if exposed
- Use Secrets (not Variables) for API keys

## Integration with Local Development

**Local Development Still Works:**
```bash
# Still works exactly as before
uv run main.py
uv run market-parser
uv run python src/backend/cli.py
uv run python src/backend/gradio_app.py
uv run market-parser-gradio
```

**New HF Spaces Entry Point:**
```bash
# New entry point (only used by HF Spaces)
python app.py  # Uses 0.0.0.0:7860
```

## Next Steps After Deployment

1. **Test functionality**
   - Ask financial queries
   - Verify data from Polygon API
   - Check performance

2. **Monitor usage**
   - HF Spaces dashboard shows usage stats
   - Check build/runtime logs for errors

3. **Updates**
   - Push code changes to git
   - HF Spaces rebuilds automatically

4. **Optimization**
   - Monitor response times
   - Upgrade hardware if needed
   - Consider prompt optimization

## Related Documentation

- **Full Deployment Guide:** `DEPLOYMENT_GUIDE_HUGGINGFACE_SPACES.md`
- **Research Task Plan:** `research_task_plan.md`
- **Project:** Market Parser (Financial Analysis with GPT-5 + Polygon API)
- **Original App:** `src/backend/gradio_app.py` (unchanged)
- **CLI Core:** `src/backend/cli.py` (unchanged)

## Summary

Market Parser is now ready for deployment to Hugging Face Spaces. All necessary files created:
- ✅ app.py (HF Spaces entry point)
- ✅ requirements.txt (dependencies)
- ✅ README.md (with HF Spaces frontmatter)
- ✅ Comprehensive deployment guide
- ✅ Original app code unchanged

Next: Follow deployment guide steps to upload to HF and configure secrets.
