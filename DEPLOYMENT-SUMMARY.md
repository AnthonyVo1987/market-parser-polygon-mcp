# AWS App Runner Deployment - Summary

## ✅ What Was Done

Your application is now ready for AWS App Runner deployment! Here's what was configured:

### 1. Docker Configuration
- **Dockerfile** - Multi-stage build that:
  - Builds React frontend (Stage 1)
  - Packages Python backend with frontend static files (Stage 2)
  - Uses production configuration
  - Optimized for size and performance

### 2. Backend Updates
- **src/backend/main.py** - Modified to serve React static files from `/dist` directory
- FastAPI now serves both API endpoints AND the React frontend
- Single container approach (simpler deployment)

### 3. Configuration Files
- **config/app.config.production.json** - Production settings:
  - Host: `0.0.0.0` (accepts external connections)
  - CORS: Configured for App Runner URLs
  - Logging: INFO level
  - Reports: `/tmp/reports` (ephemeral storage)

### 4. Deployment Scripts
- **deploy-to-apprunner.sh** - Automated deployment:
  - Creates ECR repository
  - Builds Docker image
  - Pushes to ECR
  - Provides next steps
  
- **test-docker-local.sh** - Local testing:
  - Builds and runs container locally
  - Uses your `.env` file for API keys
  - Test at http://localhost:8000

### 5. Documentation
- **DEPLOYMENT.md** - Complete deployment guide
- **DEPLOYMENT-QUICKSTART.md** - Quick 3-step guide
- **apprunner.yaml** - App Runner configuration
- **apprunner-config.json** - CLI deployment template

### 6. Optimization Files
- **.dockerignore** - Excludes unnecessary files from build
- **start.sh** - Production startup script with proper settings

## 🚀 How to Deploy

### Quick Start (3 Steps)

1. **Test locally:**
   ```bash
   ./test-docker-local.sh
   ```

2. **Push to AWS:**
   ```bash
   ./deploy-to-apprunner.sh
   ```

3. **Create App Runner service** (AWS Console):
   - Use ECR image from step 2
   - Set environment variables (API keys)
   - Configure: 1 vCPU, 2 GB, Port 8000

## 📋 Environment Variables Required

Set these in App Runner:
- `POLYGON_API_KEY` - Your Polygon.io API key
- `OPENAI_API_KEY` - Your OpenAI API key
- `TRADIER_API_KEY` - Your Tradier API key
- `FINNHUB_API_KEY` - Your Finnhub API key (optional)

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     AWS App Runner Container        │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   FastAPI Backend (Port 8000) │  │
│  │   - API Endpoints (/api, /chat)│ │
│  │   - Health Check (/health)    │  │
│  │   - Static File Server (/)    │  │
│  └──────────────────────────────┘  │
│              │                      │
│              ▼                      │
│  ┌──────────────────────────────┐  │
│  │   React Frontend (Static)    │  │
│  │   - Built files in /dist     │  │
│  │   - Served by FastAPI        │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

## 🔍 What Happens During Deployment

1. **Build Phase:**
   - Node.js builds React frontend → `dist/` folder
   - Python installs backend dependencies
   - Production config replaces development config
   - Frontend static files copied to final image

2. **Runtime Phase:**
   - FastAPI starts on port 8000
   - Serves API endpoints: `/api/*`, `/chat`, `/health`
   - Serves React app from `/` (all other routes)
   - Environment variables loaded from App Runner

3. **Access:**
   - App Runner provides HTTPS URL
   - Users access React frontend
   - Frontend calls backend API (same origin)

## 💰 Cost Breakdown

**App Runner Pricing (us-east-1):**
- Provisioned: $0.007/hour per GB = ~$10/month (2 GB)
- Active: $0.064/hour per vCPU = ~$46/month (1 vCPU)
- **Total: ~$56/month** for 24/7 operation

**Additional Costs:**
- ECR storage: ~$0.10/month per GB
- Data transfer: $0.09/GB (first 100 GB free)
- API calls: Polygon.io and OpenAI usage

## 🔒 Security Notes

1. **API Keys**: Currently using environment variables
   - Consider AWS Secrets Manager for production
   - Rotate keys regularly

2. **HTTPS**: Automatically provided by App Runner

3. **CORS**: Configured for App Runner domains
   - Update `config/app.config.production.json` with your URL

4. **IAM**: App Runner uses service role
   - Minimal permissions by default
   - Add ECR pull permissions

## 📊 Monitoring

**CloudWatch Logs:**
- Location: `/aws/apprunner/market-parser/<service-id>`
- Includes: Application logs, access logs, errors

**Metrics:**
- Request count
- Response time
- CPU/Memory usage
- Active instances

**Health Checks:**
- Endpoint: `/health`
- Interval: 5 seconds
- Timeout: 2 seconds

## 🔄 Updates & Rollbacks

**Update deployment:**
```bash
./deploy-to-apprunner.sh v2
# Then trigger deployment in AWS Console
```

**Rollback:**
- App Runner keeps previous deployments
- One-click rollback in console
- Or deploy previous image tag

## ⚠️ Important Notes

1. **Session Storage**: SQLite sessions are ephemeral
   - Consider RDS for persistent sessions
   - Current: In-memory, lost on restart

2. **File Storage**: `/tmp` is ephemeral
   - Reports saved to `/tmp/reports`
   - Consider S3 for persistent storage

3. **Scaling**: Auto-scales 1-10 instances
   - Each instance has own session
   - Consider Redis for shared sessions

4. **Cold Starts**: First request may be slow
   - Keep 1 instance always running
   - Or use provisioned concurrency

## 🐛 Troubleshooting

**Build fails:**
- Run `./test-docker-local.sh` to test locally
- Check Docker logs for errors
- Verify all files are included (check .dockerignore)

**Service unhealthy:**
- Check CloudWatch logs
- Verify environment variables
- Test `/health` endpoint
- Ensure API keys are valid

**Frontend not loading:**
- Verify `dist/` folder exists in container
- Check browser console for errors
- Verify static file mounting in main.py

**API errors:**
- Check API key validity
- Verify rate limits (OpenAI, Polygon)
- Check CloudWatch logs for details

## 📚 Next Steps

1. **Test locally** with Docker
2. **Deploy to App Runner**
3. **Configure custom domain** (optional)
4. **Set up monitoring alerts**
5. **Configure auto-scaling** based on usage
6. **Consider RDS** for persistent sessions
7. **Add S3** for report storage

## 🎯 Production Checklist

- [ ] Test Docker build locally
- [ ] Push image to ECR
- [ ] Create App Runner service
- [ ] Set environment variables
- [ ] Test health endpoint
- [ ] Verify frontend loads
- [ ] Test API functionality
- [ ] Configure CloudWatch alarms
- [ ] Set up custom domain (optional)
- [ ] Document service URL
- [ ] Update CORS if needed
- [ ] Test auto-scaling
- [ ] Review costs after 24 hours

## 📞 Support Resources

- [AWS App Runner Docs](https://docs.aws.amazon.com/apprunner/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [React Production Build](https://react.dev/learn/start-a-new-react-project#deploying-to-production)

---

**Ready to deploy?** Start with `./test-docker-local.sh` to verify everything works!
