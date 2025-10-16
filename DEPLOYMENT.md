# AWS App Runner Deployment Guide

This guide covers deploying the Market Parser application to AWS App Runner.

## Architecture Overview

The deployment uses a **single container** approach:
- **FastAPI backend** (port 8000) - Serves API endpoints
- **React frontend** - Built as static files, served by FastAPI
- **Multi-stage Docker build** - Optimized for production

## Prerequisites

1. **AWS Account** with App Runner access
2. **AWS CLI** installed and configured
3. **Docker** installed locally (for testing)
4. **API Keys** for:
   - Polygon.io (`POLYGON_API_KEY`)
   - OpenAI (`OPENAI_API_KEY`)
   - Tradier (`TRADIER_API_KEY`)
   - Finnhub (`FINNHUB_API_KEY`) - optional

## Deployment Steps

### Option 1: Deploy via AWS Console (Recommended for First Time)

1. **Build and Test Locally**
   ```bash
   # Test Docker build
   docker build -t market-parser .
   
   # Test locally with your API keys
   docker run -p 8000:8000 \
     -e POLYGON_API_KEY="your_key" \
     -e OPENAI_API_KEY="your_key" \
     -e TRADIER_API_KEY="your_key" \
     market-parser
   
   # Access at http://localhost:8000
   ```

2. **Push to ECR (Elastic Container Registry)**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name market-parser
   
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin \
     <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
   
   # Tag and push
   docker tag market-parser:latest \
     <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/market-parser:latest
   
   docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/market-parser:latest
   ```

3. **Create App Runner Service**
   - Go to AWS Console → App Runner
   - Click "Create service"
   - **Source**: Container registry → Amazon ECR
   - Select your ECR image
   - **Deployment settings**: Manual
   - **Service name**: market-parser
   - **Port**: 8000
   - **Environment variables**: Add all API keys
     - `POLYGON_API_KEY`
     - `OPENAI_API_KEY`
     - `TRADIER_API_KEY`
     - `FINNHUB_API_KEY`
   - **Instance configuration**: 
     - CPU: 1 vCPU
     - Memory: 2 GB
   - Click "Create & deploy"

### Option 2: Deploy via AWS CLI

```bash
# Create App Runner service
aws apprunner create-service \
  --service-name market-parser \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/market-parser:latest",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "POLYGON_API_KEY": "your_key",
          "OPENAI_API_KEY": "your_key",
          "TRADIER_API_KEY": "your_key",
          "FINNHUB_API_KEY": "your_key"
        }
      }
    },
    "AutoDeploymentsEnabled": false
  }' \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }'
```

### Option 3: Deploy from GitHub (Automatic Builds)

1. **Connect GitHub Repository**
   - In App Runner console, choose "Source code repository"
   - Connect your GitHub account
   - Select repository: `market-parser-polygon-mcp`
   - Branch: `main`

2. **Build Settings**
   - Build command: Uses `Dockerfile` automatically
   - Start command: `./start.sh`
   - Port: `8000`

3. **Environment Variables**
   - Add all API keys in the console

## Configuration Updates

### Production CORS Settings

Update `config/app.config.json` for production:

```json
{
  "backend": {
    "security": {
      "cors": {
        "origins": [
          "https://your-app-runner-url.awsapprunner.com"
        ]
      }
    }
  }
}
```

Or use environment variable in App Runner:
- `CORS_ORIGINS`: `https://your-app-runner-url.awsapprunner.com`

### Health Check Configuration

App Runner will automatically use the `/health` endpoint:
- Path: `/health`
- Interval: 5 seconds
- Timeout: 2 seconds
- Healthy threshold: 1
- Unhealthy threshold: 5

## Monitoring & Logs

### View Logs
```bash
# Get service ARN
aws apprunner list-services

# View logs
aws apprunner describe-service --service-arn <service-arn>
```

### CloudWatch Logs
- Logs are automatically sent to CloudWatch
- Log group: `/aws/apprunner/market-parser/<service-id>`

## Scaling Configuration

App Runner auto-scales based on:
- **Min instances**: 1
- **Max instances**: 10 (configurable)
- **Concurrency**: 100 requests per instance

Update scaling:
```bash
aws apprunner update-service \
  --service-arn <service-arn> \
  --auto-scaling-configuration-arn <config-arn>
```

## Cost Estimation

**App Runner Pricing** (us-east-1):
- **Provisioned container**: $0.007/hour per GB memory
- **Active container**: $0.064/hour per vCPU
- **Build**: $0.005/build minute

**Example** (1 vCPU, 2 GB, 24/7):
- ~$50-70/month for continuous operation
- Additional costs: ECR storage, data transfer

## Troubleshooting

### Build Failures
```bash
# Test Docker build locally
docker build -t market-parser .

# Check logs
docker logs <container-id>
```

### Runtime Errors
- Check CloudWatch logs
- Verify environment variables are set
- Ensure API keys are valid

### Frontend Not Loading
- Verify `dist/` directory exists in container
- Check FastAPI static file mounting
- Inspect browser console for errors

## Security Best Practices

1. **API Keys**: Use AWS Secrets Manager instead of environment variables
2. **HTTPS**: App Runner provides automatic HTTPS
3. **IAM Roles**: Use least-privilege IAM roles
4. **VPC**: Consider VPC connector for private resources

## Updating the Application

```bash
# Build new image
docker build -t market-parser:v2 .

# Push to ECR
docker tag market-parser:v2 \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/market-parser:v2
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/market-parser:v2

# Update App Runner service
aws apprunner update-service \
  --service-arn <service-arn> \
  --source-configuration ImageRepository={ImageIdentifier=<account-id>.dkr.ecr.us-east-1.amazonaws.com/market-parser:v2}
```

## Rollback

```bash
# List previous deployments
aws apprunner list-operations --service-arn <service-arn>

# Rollback to previous image
aws apprunner update-service \
  --service-arn <service-arn> \
  --source-configuration ImageRepository={ImageIdentifier=<previous-image>}
```

## Additional Resources

- [AWS App Runner Documentation](https://docs.aws.amazon.com/apprunner/)
- [App Runner Pricing](https://aws.amazon.com/apprunner/pricing/)
- [ECR Documentation](https://docs.aws.amazon.com/ecr/)
