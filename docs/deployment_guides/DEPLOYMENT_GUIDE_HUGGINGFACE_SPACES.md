# Deployment Guide: Market Parser to Hugging Face Spaces

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Deployment Methods Comparison](#deployment-methods-comparison)
4. [Method 1: Gradio Share Feature (Quick & Temporary)](#method-1-gradio-share-feature-quick--temporary)
5. [Method 2: Hugging Face Spaces (Permanent & Free)](#method-2-hugging-face-spaces-permanent--free)
6. [Troubleshooting](#troubleshooting)
7. [Additional Resources](#additional-resources)

---

## Introduction

### What is Hugging Face Spaces?

**Hugging Face Spaces** is a free cloud platform that lets you host machine learning applications and demos permanently. Think of it as a "free hosting service" specifically designed for AI/ML apps built with frameworks like Gradio or Streamlit.

**What is Gradio?**

Gradio is a Python library that creates web interfaces for your Python functions. Our Market Parser uses Gradio to provide a chat-style web interface for financial queries.

### Why Deploy to Hugging Face Spaces?

✅ **Free permanent hosting** - Your app stays online 24/7
✅ **No server management** - HF handles all infrastructure
✅ **Easy sharing** - Get a public URL anyone can access
✅ **No local machine required** - App runs in the cloud
✅ **Automatic updates** - Push code changes and app updates automatically

---

## Prerequisites

Before starting, ensure you have:

### Required:
- ✅ **Hugging Face Account** (free) - Sign up at [huggingface.co](https://huggingface.co)
- ✅ **API Keys** (obtained separately):
  - `POLYGON_API_KEY` - From [polygon.io](https://polygon.io) (free tier available)
  - `OPENAI_API_KEY` - From [platform.openai.com](https://platform.openai.com)
  - `TRADIER_API_KEY` (optional) - From [tradier.com](https://tradier.com)

### Optional but Helpful:
- 📝 Basic understanding of Python (not required for deployment)
- 💻 Git installed (for CLI deployment method only)
- 🔧 Text editor (for editing files)

**Important:** You do NOT need to know web development, JavaScript, CSS, or server management!

---

## Deployment Methods Comparison

There are TWO ways to make your Gradio app accessible online. Let's compare them:

### Option A: Gradio Share Feature (`share=True`)

**What it is:** A temporary public link created by Gradio (e.g., `https://abc123.gradio.live`)

**How it works:**
- Add `share=True` to your `demo.launch()` call
- Gradio creates a temporary tunnel to your local machine
- Anyone can access your app via the share link
- Your computer must stay on and running the script

**Pros:**
- ⚡ **Instant** - Works in seconds
- 🎯 **Simple** - Just 1 line of code change
- 🆓 **No account needed** - Start immediately

**Cons:**
- ⏰ **Temporary** - Link expires after inactivity (~72 hours)
- 💻 **Requires local machine running** - Your computer must stay on
- 🔄 **Not persistent** - Stops when you close the script

**Best for:** Quick demos, testing, temporary sharing

---

### Option B: Hugging Face Spaces (Permanent Deployment)

**What it is:** Free permanent cloud hosting for your Gradio app

**How it works:**
- Upload your app files to Hugging Face Spaces
- HF builds and runs your app on their servers
- You get a permanent public URL (e.g., `https://huggingface.co/spaces/username/market-parser`)
- App runs 24/7 without your local machine

**Pros:**
- 🌐 **Permanent** - App stays online forever (free tier)
- 🚀 **No local machine needed** - Runs in the cloud
- 🔄 **Automatic updates** - Push changes, app updates automatically
- 📊 **Usage analytics** - See how many people use your app
- 🔗 **Professional URL** - Shareable link on your portfolio/resume

**Cons:**
- ⚙️ **More setup** - Requires creating files and HF account
- 📚 **Learning curve** - Need to understand Spaces structure
- ⏱️ **Build time** - Takes 2-5 minutes for initial deployment

**Best for:** Production apps, portfolio projects, long-term sharing

---

## Method 1: Gradio Share Feature (Quick & Temporary)

### Step 1: Modify Your App Code

Open `src/backend/gradio_app.py` and find the `demo.launch()` line (around line 114).

**Current code:**
```python
demo.launch(
    server_name="127.0.0.1",
    server_port=8000,
    pwa=True,
    share=False,  # ← Currently False
    show_error=True,
)
```

**Modified code:**
```python
demo.launch(
    share=True,  # ⭐ Enable sharing - creates public URL
    show_error=True,
)
```

**What this does:** Gradio will create a temporary public tunnel and give you a URL like `https://a1b2c3d4.gradio.live`

### Step 2: Run Your App Locally

```bash
# Make sure you're in the project directory
cd /path/to/market-parser-polygon-mcp

# Ensure environment variables are set
# Your .env file should contain:
# POLYGON_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here

# Run the Gradio app
uv run python src/backend/gradio_app.py
```

### Step 3: Get Your Share Link

When the app starts, you'll see output like:

```
Running on local URL:  http://127.0.0.1:8000
Running on public URL: https://a1b2c3d4e5f6.gradio.live  ← Share this link!

This share link expires in 72 hours. For free permanent hosting and GPU upgrades, check out Spaces: https://huggingface.co/spaces
```

**Copy the public URL** and share it with anyone!

### Step 4: Keep Your App Running

⚠️ **Important:** Your computer MUST stay on and the script MUST keep running for the share link to work.

- Closing the terminal = link stops working
- Shutting down computer = link stops working
- Ctrl+C to stop = link stops working

**That's it for Gradio Share!** This method is perfect for quick demos and testing.

---

## Method 2: Hugging Face Spaces (Permanent & Free)

This is the **recommended method** for production deployment. Follow these steps carefully.

### Overview of the Process

1. ✅ Create Hugging Face account (if you don't have one)
2. ✅ Prepare deployment files (app.py, requirements.txt, README.md)
3. ✅ Create a new Space on Hugging Face
4. ✅ Upload your files (via web or git)
5. ✅ Configure environment variables (API keys)
6. ✅ Wait for build to complete (~2-5 minutes)
7. ✅ Access your deployed app!

---

### Step 1: Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click **"Sign Up"** in the top right corner
3. Enter your email, create a username and password
4. Verify your email address
5. ✅ **Done!** You now have a free HF account

**What is a username?** This will be part of your app's URL: `huggingface.co/spaces/YOUR_USERNAME/market-parser`

---

### Step 2: Prepare Deployment Files

Hugging Face Spaces requires specific files at the root of your project. Let's create them.

#### 2.1: Create `app.py` (Main App File)

**Why:** HF Spaces expects the main app file to be named `app.py` at the project root.

**Our situation:** Our Gradio app is at `src/backend/gradio_app.py`, so we need to create a wrapper.

**Create a new file** at the root of your project called `app.py`:

```bash
# Create app.py at the root (same level as README.md)
touch app.py
```

**Add this content to `app.py`:**

```python
"""Hugging Face Spaces deployment entry point for Market Parser.

This file is specifically for HF Spaces deployment.
It imports and runs the main Gradio app from src/backend/gradio_app.py.
"""

# Import the demo from our main app
from backend.gradio_app import demo

# Launch with HF Spaces-compatible settings
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Required for HF Spaces
        server_port=7860,        # HF Spaces default port
        share=False,             # Not needed in HF Spaces
        show_error=True,
    )
```

**What this does:** Creates a simple wrapper that imports your existing Gradio app and launches it with HF Spaces-compatible settings.

---

#### 2.2: Create `requirements.txt` (Dependencies)

**Why:** Tells HF Spaces which Python packages to install.

**Create `requirements.txt`** at the root of your project:

```bash
touch requirements.txt
```

**Add this content** (based on your `pyproject.toml`):

```txt
# Core dependencies
gradio>=5.49.1
openai-agents==0.2.9
openai>=1.99.0,<1.100.0
pydantic>=2.0.0
rich>=13.0.0
python-dotenv>=1.0.0

# API clients
polygon-api-client>=1.14.0
openai-agents-mcp>=0.0.8

# Async support
aiofiles>=24.1.0

# LSP (Language Server Protocol) - optional but included in pyproject.toml
python-lsp-server[all]>=1.13.1
```

**What this does:** Lists all Python packages HF Spaces needs to install to run your app.

**Alternative:** If you prefer, you can copy `pyproject.toml` to the root instead. HF Spaces supports both formats!

---

#### 2.3: Create/Update `README.md` (Space Description)

**Why:** HF Spaces uses README.md as the app's description and documentation page.

**Create or edit `README.md`** at the root:

```markdown
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

# Market Parser - AI Financial Analysis Assistant

An intelligent financial analysis tool powered by OpenAI GPT-5-nano and Polygon.io market data.

## Features

- 📊 Natural language financial queries
- 💹 Real-time stock price analysis
- 📈 Technical analysis and trends
- 🔍 Market data insights
- 🤖 AI-powered responses

## How to Use

1. Type your financial query in the chat box
2. Examples:
   - "What's Tesla's stock price today?"
   - "Show me AAPL volume trends this week"
   - "Analyze NVDA support and resistance levels"
3. Get AI-powered analysis with real market data

## Technology Stack

- **AI Model:** OpenAI GPT-5-nano via Agents SDK
- **Market Data:** Polygon.io API
- **Interface:** Gradio 5.49.1 ChatInterface
- **Language:** Python 3.10+

## API Keys Required

This app requires API keys (configured as Hugging Face Secrets):
- `OPENAI_API_KEY` - OpenAI API access
- `POLYGON_API_KEY` - Polygon.io market data
- `TRADIER_API_KEY` (optional) - Additional market data

## Source Code

[View on GitHub](https://github.com/YOUR_USERNAME/market-parser-polygon-mcp)
```

**What this does:**
- The `---` section (called "frontmatter") configures Space settings
- The markdown below becomes your app's homepage description

**Configuration explained:**
- `title`: Your app's display name
- `emoji`: Icon shown next to your Space
- `sdk: gradio`: Tells HF this is a Gradio app
- `sdk_version`: Gradio version to use
- `app_file: app.py`: Main file to run

---

#### 2.4: Verify Your Files

Your project structure should now look like:

```
market-parser-polygon-mcp/
├── app.py                    ← NEW (HF Spaces entry point)
├── requirements.txt          ← NEW (dependencies)
├── README.md                 ← UPDATED (Space description)
├── .env                      ← KEEP LOCAL (do NOT upload!)
├── pyproject.toml
├── src/
│   └── backend/
│       ├── gradio_app.py     ← Your original app
│       ├── cli.py
│       ├── config.py
│       └── tools/
└── ...
```

**✅ Files ready for deployment:**
- `app.py`
- `requirements.txt`
- `README.md`

**❌ Files to NEVER upload:**
- `.env` (contains your API keys - keep secret!)
- `__pycache__/` (Python cache)
- `.venv/` or `venv/` (virtual environment)

---

### Step 3: Create a New Space on Hugging Face

1. **Log in to Hugging Face** at [huggingface.co](https://huggingface.co)

2. **Click "Spaces"** in the top navigation bar

3. **Click "Create new Space"** button (top right)

4. **Configure your Space:**

   | Field | Value | Explanation |
   |-------|-------|-------------|
   | **Owner** | Your username | Who owns this Space |
   | **Space name** | `market-parser` | URL-friendly name (lowercase, hyphens) |
   | **License** | MIT | How others can use your code |
   | **Select the Space SDK** | Gradio | Framework you're using |
   | **Blank template** | Selected | Start with empty Space |
   | **Space hardware** | CPU basic (free) | Sufficient for our app |
   | **Visibility** | Public | Anyone can access (or choose Private) |

5. **Click "Create Space"**

**What this does:** Creates an empty Hugging Face Space repository where you'll upload your files.

**Your Space URL will be:** `https://huggingface.co/spaces/YOUR_USERNAME/market-parser`

---

### Step 4: Upload Your Files to the Space

You have **two options** for uploading files: Web UI (easier) or Git (more advanced).

#### Option A: Web UI Upload (Recommended for Beginners)

1. **After creating the Space**, you'll see the Space page with a "Files" tab

2. **Click "Files and versions"** tab

3. **Click "Add file" dropdown** → Select "Upload files"

4. **Drag and drop or select these files:**
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - **Entire `src/` folder** (drag the whole folder)

5. **Scroll down to "Commit changes to main"**
   - Add message: `Initial deployment of Market Parser`
   - Click **"Commit changes to main"**

**What this does:** Uploads your files to HF Spaces and triggers an automatic build.

---

#### Option B: Git CLI Upload (Advanced Users)

If you're comfortable with Git:

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/market-parser
cd market-parser

# Copy deployment files
cp /path/to/your/app.py .
cp /path/to/your/requirements.txt .
cp /path/to/your/README.md .
cp -r /path/to/your/src .

# Commit and push
git add .
git commit -m "Initial deployment of Market Parser"
git push
```

**What this does:** Same as web UI, but using Git commands.

---

### Step 5: Configure Environment Variables (API Keys)

**⚠️ CRITICAL SECURITY STEP:** Never upload API keys in your code! Use HF Spaces Secrets.

1. **Go to your Space page:** `https://huggingface.co/spaces/YOUR_USERNAME/market-parser`

2. **Click "Settings"** tab (top right, next to "Files and versions")

3. **Scroll down to "Repository secrets"** section

4. **Click "New secret"** and add each API key:

   | Secret Name | Value | Where to Get |
   |-------------|-------|--------------|
   | `OPENAI_API_KEY` | `sk-proj-...` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
   | `POLYGON_API_KEY` | Your Polygon key | [polygon.io/dashboard/api-keys](https://polygon.io/dashboard/api-keys) |
   | `TRADIER_API_KEY` | Your Tradier key (optional) | [tradier.com/api-keys](https://developer.tradier.com/getting_started) |

5. **For EACH secret:**
   - Enter the **Name** (e.g., `OPENAI_API_KEY`)
   - Enter the **Value** (your actual API key)
   - Click **"Add secret"**

**What this does:**
- Secrets are stored securely on HF servers
- Your Python code accesses them via `os.getenv("OPENAI_API_KEY")`
- Secrets are NEVER visible after saving (even to you!)
- If you lose a key, delete the secret and create a new one

**Security Notes:**
- ✅ **Secrets** = Private (API keys, tokens)
- ✅ **Variables** = Public (non-sensitive config)
- ❌ **Never hardcode** API keys in your code
- ❌ **Never upload** `.env` file to Spaces

---

### Step 6: Monitor the Build Process

After uploading files or adding secrets, HF Spaces automatically builds your app.

1. **Go to the "App"** tab on your Space page

2. **You'll see:** "Building..." or "Starting..."

3. **Click "Logs"** (bottom right) to see build progress

**Build process:**
1. ⏳ Installing dependencies from `requirements.txt` (1-3 minutes)
2. ⏳ Starting your Gradio app (30 seconds)
3. ✅ App running! (green "Running" status)

**Typical build time:** 2-5 minutes for first deployment

**What to look for in logs:**
```
Installing dependencies from requirements.txt...
Successfully installed gradio-5.49.1 openai-agents-0.2.9 ...
Running on local URL:  http://0.0.0.0:7860
```

**If build succeeds:** Status changes to "Running" (green)
**If build fails:** Status shows "Build failed" (red) → See [Troubleshooting](#troubleshooting)

---

### Step 7: Access Your Deployed App!

Once the build completes and status shows **"Running"**:

1. **Your app is live!** 🎉

2. **Access it at:** `https://huggingface.co/spaces/YOUR_USERNAME/market-parser`

3. **Test your app:**
   - Type a financial query in the chat box
   - Example: "What's TSLA stock price today?"
   - Verify the response includes real market data

4. **Share the URL** with anyone - they can use your app instantly!

**Performance notes:**
- First load may take 10-15 seconds (cold start)
- Subsequent loads are faster
- Free tier has usage limits (upgrade if needed)

---

### Step 8: Update Your Deployed App (Future Changes)

When you make code changes:

**Via Web UI:**
1. Go to "Files and versions" tab
2. Click the file you want to edit
3. Click "Edit" button
4. Make changes
5. Commit changes → App rebuilds automatically

**Via Git:**
```bash
cd market-parser
# Make changes to your files
git add .
git commit -m "Update: describe changes"
git push
```

**What happens:** HF Spaces detects the push and automatically rebuilds your app with the new code!

---

## Troubleshooting

### Build Failures

**Problem:** Build fails with "ModuleNotFoundError"

**Solution:** Missing dependency in `requirements.txt`
1. Check build logs for the missing module name
2. Add it to `requirements.txt`
3. Commit and push changes

---

**Problem:** Build fails with "ImportError: cannot import name..."

**Solution:** Project structure issue
1. Verify `src/` folder uploaded correctly
2. Check that `app.py` imports match your structure
3. Try: `from backend.gradio_app import demo` vs `from src.backend.gradio_app import demo`

---

**Problem:** Build fails with "Python version mismatch"

**Solution:** Add a `runtime.txt` file at root:
```txt
python-3.10
```

---

### Runtime Errors

**Problem:** App builds but shows "Error: API key not found"

**Solution:** Environment variables not configured
1. Go to Settings → Repository secrets
2. Verify all secrets added (`OPENAI_API_KEY`, `POLYGON_API_KEY`)
3. Check for typos in secret names (case-sensitive!)
4. Restart Space: Settings → "Factory reboot"

---

**Problem:** App shows "Connection timeout" errors

**Solution:** API rate limits or network issues
1. Check if your API keys have sufficient quota
2. Verify API keys are valid (test locally first)
3. Some APIs may block Hugging Face IPs - check API provider docs

---

**Problem:** App works locally but not on HF Spaces

**Solution:** Environment differences
1. Check HF Spaces logs for specific errors
2. Verify all dependencies in `requirements.txt`
3. Test with `share=True` locally (simulates cloud environment)
4. Some packages require system libraries - may need Docker SDK

---

### Dependency Issues

**Problem:** "ERROR: No matching distribution found for openai-agents==0.2.9"

**Solution:** Package version not available
1. Try latest version: `openai-agents>=0.2.0`
2. Or remove version pin: `openai-agents`
3. Check package exists: [pypi.org/project/openai-agents](https://pypi.org/project/openai-agents)

---

**Problem:** "Killed" error during dependency installation

**Solution:** Out of memory
1. Upgrade Space hardware: Settings → Change hardware → CPU upgrade
2. Or reduce dependencies (remove unused packages)

---

### Common Questions

**Q: Can I keep my Space private?**
A: Yes! Settings → Change visibility to Private. Only you can access it.

**Q: How much does HF Spaces cost?**
A: Free tier is generous! Paid plans available for more resources/uptime.

**Q: Can I use a custom domain?**
A: Not on free tier. Paid plans support custom domains.

**Q: How do I delete a Space?**
A: Settings → Scroll to bottom → Delete Space → Confirm

**Q: Can I add authentication/login?**
A: Yes! See Gradio's `auth` parameter: [Gradio Authentication Docs](https://www.gradio.app/guides/sharing-your-app#authentication)

**Q: What if I hit usage limits?**
A: Upgrade to paid plan or optimize your app to use fewer resources

---

## Additional Resources

### Official Documentation

- **Hugging Face Spaces Docs:** [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/en/spaces)
- **Gradio Docs:** [gradio.app/docs](https://www.gradio.app/docs/)
- **Gradio HF Integration:** [gradio.app/guides/using-hugging-face-integrations](https://www.gradio.app/guides/using-hugging-face-integrations)

### Tutorials and Guides

- **HF Spaces Quickstart:** [huggingface.co/docs/hub/spaces-sdks-gradio](https://huggingface.co/docs/hub/en/spaces-sdks-gradio)
- **Gradio Sharing Guide:** [gradio.app/guides/sharing-your-app](https://www.gradio.app/guides/sharing-your-app)
- **Deploy Gradio to HF:** [pyimagesearch.com/deploy-gradio-apps-on-hugging-face-spaces](https://pyimagesearch.com/2024/12/30/deploy-gradio-apps-on-hugging-face-spaces/)

### Community Support

- **HF Forum:** [discuss.huggingface.co](https://discuss.huggingface.co)
- **Gradio Discord:** [discord.com/invite/feTf9x3ZSB](https://discord.com/invite/feTf9x3ZSB)
- **HF Spaces Examples:** [huggingface.co/spaces](https://huggingface.co/spaces) (browse existing Spaces for inspiration)

### API Documentation

- **Polygon.io API:** [polygon.io/docs](https://polygon.io/docs/stocks)
- **OpenAI API:** [platform.openai.com/docs](https://platform.openai.com/docs)
- **Tradier API:** [developer.tradier.com](https://developer.tradier.com)

---

## Summary

You now have **two deployment options** for Market Parser:

### Quick & Temporary (Gradio Share)
1. Add `share=True` to `demo.launch()`
2. Run locally: `uv run python src/backend/gradio_app.py`
3. Share the generated URL
4. Keep your computer on

### Permanent & Free (Hugging Face Spaces)
1. Create HF account
2. Prepare files: `app.py`, `requirements.txt`, `README.md`
3. Create new Space on HF
4. Upload files via web or git
5. Configure secrets (API keys)
6. Wait for build
7. Access deployed app!

**Recommended:** Start with Gradio Share for testing, then deploy to HF Spaces for production!

---

**Questions or issues?** Check [Troubleshooting](#troubleshooting) or reach out to the Hugging Face community!

**Happy deploying! 🚀📈**
