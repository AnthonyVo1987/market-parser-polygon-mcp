# AWS MCP Servers Guide for App Runner Deployment

Complete guide for configuring AWS MCP servers to enable AI agents to deploy applications to AWS App Runner with full documentation, troubleshooting, and monitoring capabilities.

**Source:** https://github.com/awslabs/mcp

## Essential AWS MCP Servers

### 1. AWS Knowledge Base (Documentation)
```bash
npx -y @aws/mcp-server-aws-kb
```
**Purpose:** AWS documentation, best practices, troubleshooting guides  
**Use Cases:**
- Query AWS service documentation
- Get deployment best practices
- Find troubleshooting solutions
- Learn AWS service capabilities

### 2. AWS Bedrock (AI-Powered Assistance)
```bash
npx -y @aws/mcp-server-bedrock
```
**Purpose:** AI-powered AWS guidance and code generation  
**Use Cases:**
- Generate AWS CloudFormation templates
- Get AI-powered AWS recommendations
- Automated code generation for AWS services

### 3. AWS CloudWatch (Monitoring & Logs)
```bash
npx -y @aws/mcp-server-cloudwatch
```
**Purpose:** View logs, metrics, troubleshoot deployment issues  
**Use Cases:**
- View App Runner logs
- Monitor application metrics
- Debug deployment failures
- Track performance

### 4. AWS ECR (Container Registry)
```bash
npx -y @aws/mcp-server-ecr
```
**Purpose:** Manage Docker images, push/pull containers  
**Use Cases:**
- Create ECR repositories
- Push Docker images
- Manage image tags
- List available images

### 5. AWS IAM (Permissions & Roles)
```bash
npx -y @aws/mcp-server-iam
```
**Purpose:** Create/manage IAM roles for App Runner  
**Use Cases:**
- Create service roles
- Manage permissions
- Configure access policies
- Security best practices

### 6. AWS Secrets Manager (API Keys)
```bash
npx -y @aws/mcp-server-secrets-manager
```
**Purpose:** Securely store API keys instead of environment variables  
**Use Cases:**
- Store API keys securely
- Rotate secrets automatically
- Reference secrets in App Runner
- Better security than env vars

### 7. AWS App Runner (Deployment)
```bash
npx -y @aws/mcp-server-apprunner
```
**Purpose:** Create, deploy, manage App Runner services  
**Use Cases:**
- Create App Runner services
- Deploy applications
- Update configurations
- Manage auto-scaling

### 8. AWS Cost Explorer (Cost Monitoring)
```bash
npx -y @aws/mcp-server-cost-explorer
```
**Purpose:** Monitor deployment costs  
**Use Cases:**
- Track spending
- Forecast costs
- Optimize resource usage
- Budget alerts

## MCP Configuration File

Create `.mcp_aws_deployment.json` in your project root:

```json
{
  "mcpServers": {
    "aws-kb": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-aws-kb"],
      "description": "AWS documentation and knowledge base"
    },
    "aws-bedrock": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-bedrock"],
      "description": "AI-powered AWS assistance"
    },
    "aws-cloudwatch": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-cloudwatch"],
      "description": "Logs and monitoring"
    },
    "aws-ecr": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-ecr"],
      "description": "Container registry management"
    },
    "aws-iam": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-iam"],
      "description": "Identity and access management"
    },
    "aws-secrets": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-secrets-manager"],
      "description": "Secure secrets storage"
    },
    "aws-apprunner": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-apprunner"],
      "description": "App Runner service management"
    },
    "aws-costs": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-cost-explorer"],
      "description": "Cost monitoring and optimization"
    }
  }
}
```

## Deployment Workflow with MCP Servers

### Phase 1: Project Analysis
**Server:** `aws-kb`
- Query best practices for FastAPI + React deployment
- Understand App Runner requirements
- Learn about container deployment

### Phase 2: Container Setup
**Servers:** `aws-ecr`, `aws-iam`
1. Create ECR repository
2. Configure IAM roles for ECR access
3. Build Docker image locally
4. Push image to ECR

### Phase 3: Secrets Management
**Server:** `aws-secrets`
1. Store API keys in Secrets Manager
2. Configure secret rotation
3. Grant App Runner access to secrets

### Phase 4: Deployment
**Server:** `aws-apprunner`
1. Create App Runner service
2. Configure from ECR image
3. Set environment variables
4. Configure auto-scaling
5. Deploy service

### Phase 5: Monitoring
**Servers:** `aws-cloudwatch`, `aws-costs`
1. View deployment logs
2. Monitor application metrics
3. Track costs
4. Set up alerts

### Phase 6: Troubleshooting
**Servers:** `aws-kb`, `aws-cloudwatch`, `aws-bedrock`
1. Query error messages in CloudWatch
2. Search AWS KB for solutions
3. Use Bedrock for AI-powered debugging
4. Apply fixes and redeploy

## Installation Instructions

### For Claude Code (VS Code Extension)

1. **Open VS Code Settings** (Ctrl+Shift+P → "Preferences: Open User Settings (JSON)")

2. **Add MCP configuration:**

```json
{
  "claude.mcpServers": {
    "aws-kb": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-aws-kb"]
    },
    "aws-cloudwatch": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-cloudwatch"]
    },
    "aws-ecr": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-ecr"]
    },
    "aws-iam": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-iam"]
    },
    "aws-secrets": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-secrets-manager"]
    },
    "aws-apprunner": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-apprunner"]
    },
    "aws-costs": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-cost-explorer"]
    }
  }
}
```

3. **Reload VS Code** (Ctrl+Shift+P → "Developer: Reload Window")

4. **Verify MCP servers** are loaded in Claude Code output panel

### For Cursor IDE

1. **Create MCP config file** in your project root:

```bash
mkdir -p .cursor
touch .cursor/mcp_config.json
```

2. **Add configuration to `.cursor/mcp_config.json`:**

```json
{
  "mcpServers": {
    "aws-kb": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-aws-kb"]
    },
    "aws-cloudwatch": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-cloudwatch"]
    },
    "aws-ecr": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-ecr"]
    },
    "aws-iam": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-iam"]
    },
    "aws-secrets": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-secrets-manager"]
    },
    "aws-apprunner": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-apprunner"]
    },
    "aws-costs": {
      "command": "npx",
      "args": ["-y", "@aws/mcp-server-cost-explorer"]
    }
  }
}
```

3. **Restart Cursor** to load MCP servers

4. **Verify** by asking Cursor to list available MCP tools

## Prerequisites

1. **Node.js 18+** - Required for npx
2. **AWS CLI configured** - Run `aws configure`
3. **AWS credentials** - Access key and secret key
4. **Appropriate IAM permissions** - ECR, App Runner, CloudWatch, IAM

## Testing MCP Server Connection

### Test in Claude Code
1. Open Claude Code panel in VS Code
2. Ask: "List available MCP tools"
3. Verify AWS servers appear in the list
4. Test: "Query AWS KB for App Runner documentation"

### Test in Cursor
1. Open Cursor chat
2. Ask: "What MCP servers are available?"
3. Verify AWS servers are loaded
4. Test: "Use AWS KB to explain ECR"

### Test via Command Line
```bash
# Test AWS KB
npx -y @aws/mcp-server-aws-kb --help

# Test ECR
npx -y @aws/mcp-server-ecr --help

# Test App Runner
npx -y @aws/mcp-server-apprunner --help
```

## Common Use Cases

### Deploy New Application
```
1. Use aws-kb to understand App Runner requirements
2. Use aws-ecr to create repository and push image
3. Use aws-iam to create service role
4. Use aws-secrets to store API keys
5. Use aws-apprunner to create service
6. Use aws-cloudwatch to verify deployment
7. Use aws-costs to monitor spending
```

### Troubleshoot Deployment Failure
```
1. Use aws-cloudwatch to view error logs
2. Use aws-kb to search for error solutions
3. Use aws-bedrock for AI-powered debugging
4. Use aws-apprunner to update configuration
5. Use aws-cloudwatch to verify fix
```

### Optimize Costs
```
1. Use aws-costs to analyze spending
2. Use aws-kb to learn optimization strategies
3. Use aws-apprunner to adjust instance size
4. Use aws-costs to verify savings
```

## Additional AWS MCP Servers

For more advanced use cases, consider:

- `@aws/mcp-server-s3` - File storage
- `@aws/mcp-server-rds` - Database management
- `@aws/mcp-server-lambda` - Serverless functions
- `@aws/mcp-server-vpc` - Network configuration
- `@aws/mcp-server-route53` - DNS management

Full list: https://github.com/awslabs/mcp

## Security Best Practices

1. **Use Secrets Manager** - Never hardcode API keys
2. **Least Privilege IAM** - Grant minimum required permissions
3. **Enable CloudWatch Logs** - Monitor all activities
4. **Regular Cost Reviews** - Use Cost Explorer weekly
5. **Rotate Credentials** - Use Secrets Manager rotation

## Support Resources

- **AWS MCP Servers Repo:** https://github.com/awslabs/mcp
- **AWS Documentation:** https://docs.aws.amazon.com/
- **App Runner Guide:** https://docs.aws.amazon.com/apprunner/
- **MCP Protocol:** https://modelcontextprotocol.io/

## Troubleshooting

**MCP server not found:**
```bash
npm install -g npx
npx clear-npx-cache
```

**AWS credentials error:**
```bash
aws configure
aws sts get-caller-identity
```

**Permission denied:**
- Check IAM permissions
- Verify AWS CLI is configured
- Ensure service role has correct policies

---

**Ready to deploy?** Configure these MCP servers in your AI coding assistant and start deploying to AWS App Runner!
