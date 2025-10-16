# AWS App Runner - Quick Start Guide

## 🚀 Deploy in 3 Steps

### Step 1: Test Locally
```bash
./test-docker-local.sh
# Visit http://localhost:8000 to verify
```

### Step 2: Push to AWS
```bash
./deploy-to-apprunner.sh
```

### Step 3: Create App Runner Service

**Via AWS Console:**
1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner)
2. Click "Create service"
3. **Source**: Container registry → Amazon ECR
4. **Image URI**: Copy from script output
5. **Port**: 8000
6. **Environment Variables**:
   ```
   POLYGON_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   TRADIER_API_KEY=your_key_here
   FINNHUB_API_KEY=your_key_here
   ```
7. **Instance**: 1 vCPU, 2 GB Memory
8. Click "Create & deploy"

**Via AWS CLI:**
```bash
# Replace <ACCOUNT_ID> with your AWS account ID
aws apprunner create-service \
  --service-name market-parser \
  --source-configuration file://apprunner-config.json \
  --instance-configuration Cpu=1024,Memory=2048
```

## 📋 What Gets Deployed

- ✅ FastAPI backend (serves API + frontend)
- ✅ React frontend (built static files)
- ✅ All dependencies bundled
- ✅ Production optimized

## 🔍 Verify Deployment

After deployment completes (~5 minutes):

1. **Get Service URL**:
   ```bash
   aws apprunner list-services
   ```

2. **Test Health Endpoint**:
   ```bash
   curl https://your-app-url.awsapprunner.com/health
   ```

3. **Access Frontend**:
   ```
   https://your-app-url.awsapprunner.com
   ```

## 💰 Cost Estimate

- **~$50-70/month** for 24/7 operation
- 1 vCPU, 2 GB Memory
- Includes auto-scaling (1-10 instances)

## 🔧 Update Deployment

```bash
# Make changes to code
# Then run:
./deploy-to-apprunner.sh v2

# Update service in AWS Console or:
aws apprunner start-deployment --service-arn <your-service-arn>
```

## 🐛 Troubleshooting

**Build fails?**
```bash
# Test locally first
./test-docker-local.sh
```

**Service unhealthy?**
- Check CloudWatch logs: `/aws/apprunner/market-parser/`
- Verify environment variables are set
- Ensure API keys are valid

**Frontend not loading?**
- Check browser console for errors
- Verify `/health` endpoint works
- Check CORS settings in production config

## 📚 Full Documentation

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete details.
