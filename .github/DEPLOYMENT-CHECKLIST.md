# AWS App Runner Deployment Checklist

Use this checklist to ensure a smooth deployment process.

## Pre-Deployment

### Local Testing
- [ ] All tests passing: `./test_cli_regression.sh`
- [ ] Frontend builds successfully: `npm run build`
- [ ] Backend runs without errors: `npm run backend:dev`
- [ ] Environment variables set in `.env`
- [ ] Docker installed and running

### AWS Prerequisites
- [ ] AWS account created
- [ ] AWS CLI installed: `aws --version`
- [ ] AWS CLI configured: `aws configure`
- [ ] IAM permissions for ECR and App Runner
- [ ] Region selected (default: us-east-1)

### API Keys Ready
- [ ] Polygon.io API key valid
- [ ] OpenAI API key valid and has credits
- [ ] Tradier API key valid
- [ ] Finnhub API key (optional)

## Docker Build & Test

### Local Docker Testing
- [ ] Run: `./test-docker-local.sh`
- [ ] Container starts without errors
- [ ] Health endpoint works: `curl http://localhost:8000/health`
- [ ] Frontend loads: http://localhost:8000
- [ ] Can submit queries and get responses
- [ ] No console errors in browser
- [ ] Stop container: `Ctrl+C`

### Build Verification
- [ ] Image size reasonable (< 1 GB)
- [ ] No build warnings or errors
- [ ] All dependencies installed
- [ ] Production config used

## AWS Deployment

### ECR Setup
- [ ] Run: `./deploy-to-apprunner.sh`
- [ ] ECR repository created
- [ ] Docker image built successfully
- [ ] Image pushed to ECR
- [ ] Note ECR image URI

### App Runner Service Creation

#### Via Console
- [ ] Navigate to App Runner console
- [ ] Click "Create service"
- [ ] Select "Container registry" → "Amazon ECR"
- [ ] Choose ECR image
- [ ] Deployment: Manual
- [ ] Service name: `market-parser`
- [ ] Port: `8000`
- [ ] CPU: `1 vCPU`
- [ ] Memory: `2 GB`
- [ ] Add environment variables:
  - [ ] `POLYGON_API_KEY`
  - [ ] `OPENAI_API_KEY`
  - [ ] `TRADIER_API_KEY`
  - [ ] `FINNHUB_API_KEY`
- [ ] Click "Create & deploy"
- [ ] Wait for deployment (~5 minutes)

#### Via CLI (Alternative)
- [ ] Update `apprunner-config.json` with ECR URI
- [ ] Add API keys to config
- [ ] Run create-service command
- [ ] Wait for deployment

## Post-Deployment Verification

### Service Health
- [ ] Service status: "Running"
- [ ] Health checks passing
- [ ] No errors in CloudWatch logs
- [ ] Note service URL

### Functional Testing
- [ ] Visit App Runner URL
- [ ] Frontend loads correctly
- [ ] No console errors
- [ ] Health endpoint: `https://your-url.awsapprunner.com/health`
- [ ] Submit test query: "AAPL stock price"
- [ ] Response received successfully
- [ ] Response time acceptable (< 30s)
- [ ] Try multiple queries
- [ ] Test different tickers

### Performance Check
- [ ] Response times reasonable
- [ ] No timeout errors
- [ ] Memory usage normal
- [ ] CPU usage normal
- [ ] Check CloudWatch metrics

## Monitoring Setup

### CloudWatch
- [ ] Locate log group: `/aws/apprunner/market-parser/`
- [ ] Verify logs appearing
- [ ] No error messages
- [ ] Set up log insights queries (optional)

### Alarms (Optional)
- [ ] Create alarm for unhealthy instances
- [ ] Create alarm for high error rate
- [ ] Create alarm for high response time
- [ ] Set up SNS notifications

## Configuration

### CORS (If Needed)
- [ ] Update `config/app.config.production.json`
- [ ] Add App Runner URL to CORS origins
- [ ] Rebuild and redeploy if changed

### Custom Domain (Optional)
- [ ] Configure custom domain in App Runner
- [ ] Update DNS records
- [ ] Verify SSL certificate
- [ ] Test with custom domain

## Documentation

### Record Information
- [ ] Service URL: `_______________________`
- [ ] Service ARN: `_______________________`
- [ ] ECR Repository: `_______________________`
- [ ] Deployment date: `_______________________`
- [ ] Deployment version/tag: `_______________________`

### Update Documentation
- [ ] Add service URL to README
- [ ] Document any configuration changes
- [ ] Update team wiki/docs
- [ ] Share access with team

## Cost Management

### Initial Review
- [ ] Review App Runner pricing
- [ ] Estimate monthly cost
- [ ] Set up billing alerts
- [ ] Review after 24 hours
- [ ] Review after 7 days

### Optimization (After Testing)
- [ ] Adjust instance size if needed
- [ ] Configure auto-scaling limits
- [ ] Review ECR image retention
- [ ] Clean up old images

## Security Review

### Access Control
- [ ] Review IAM roles
- [ ] Verify least-privilege access
- [ ] Document who has access
- [ ] Set up MFA for AWS account

### Secrets Management
- [ ] Consider AWS Secrets Manager
- [ ] Rotate API keys regularly
- [ ] Document key rotation process
- [ ] Set up key expiration alerts

### Network Security
- [ ] HTTPS enabled (automatic)
- [ ] Review CORS settings
- [ ] Consider VPC connector (if needed)
- [ ] Review security groups (if using VPC)

## Rollback Plan

### Preparation
- [ ] Document current working version
- [ ] Keep previous ECR image tag
- [ ] Test rollback procedure
- [ ] Document rollback steps

### Rollback Steps (If Needed)
1. [ ] Note current version
2. [ ] Identify previous working version
3. [ ] Update service with previous image
4. [ ] Verify service health
5. [ ] Test functionality
6. [ ] Document incident

## Maintenance

### Regular Tasks
- [ ] Monitor CloudWatch logs weekly
- [ ] Review costs monthly
- [ ] Update dependencies monthly
- [ ] Rotate API keys quarterly
- [ ] Review and update documentation

### Update Process
- [ ] Test changes locally
- [ ] Build new Docker image
- [ ] Push to ECR with new tag
- [ ] Update App Runner service
- [ ] Verify deployment
- [ ] Monitor for issues

## Troubleshooting

### Common Issues Checklist
- [ ] Service unhealthy → Check CloudWatch logs
- [ ] Frontend not loading → Verify dist/ folder
- [ ] API errors → Check environment variables
- [ ] Slow responses → Check API rate limits
- [ ] Build failures → Test Docker locally

### Support Resources
- [ ] Bookmark AWS App Runner docs
- [ ] Save CloudWatch log group URL
- [ ] Document support contacts
- [ ] Keep deployment scripts updated

## Sign-Off

### Deployment Team
- [ ] Developer: `_______________________`
- [ ] Reviewer: `_______________________`
- [ ] Date: `_______________________`
- [ ] Approved: `_______________________`

### Production Ready
- [ ] All tests passed
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] Service URL shared

---

**Deployment Status:** ⬜ Not Started | ⬜ In Progress | ⬜ Complete

**Notes:**
```
Add any deployment-specific notes here
```
