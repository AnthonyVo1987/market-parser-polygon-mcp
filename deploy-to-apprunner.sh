#!/bin/bash
# Quick deployment script for AWS App Runner

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Market Parser - AWS App Runner Deployment${NC}\n"

# Check prerequisites
command -v aws >/dev/null 2>&1 || { echo -e "${RED}❌ AWS CLI not installed${NC}"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker not installed${NC}"; exit 1; }

# Check if docker command needs sudo
if ! docker ps >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker requires sudo. Using sudo for docker commands...${NC}"
    DOCKER_CMD="sudo docker"
else
    DOCKER_CMD="docker"
fi

# Get AWS account ID and region
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-1}
REPO_NAME="market-parser"
IMAGE_TAG=${1:-latest}

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "  Account ID: $AWS_ACCOUNT_ID"
echo "  Region: $AWS_REGION"
echo "  Repository: $REPO_NAME"
echo "  Image Tag: $IMAGE_TAG"
echo ""

# Step 1: Create ECR repository if it doesn't exist
echo -e "${YELLOW}📦 Step 1: Checking ECR repository...${NC}"
if ! aws ecr describe-repositories --repository-names $REPO_NAME --region $AWS_REGION >/dev/null 2>&1; then
    echo "Creating ECR repository..."
    aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION
    echo -e "${GREEN}✅ Repository created${NC}"
else
    echo -e "${GREEN}✅ Repository exists${NC}"
fi

# Step 2: Build Docker image
echo -e "\n${YELLOW}🔨 Step 2: Building Docker image...${NC}"
$DOCKER_CMD build -t $REPO_NAME:$IMAGE_TAG .
echo -e "${GREEN}✅ Image built${NC}"

# Step 3: Login to ECR
echo -e "\n${YELLOW}🔐 Step 3: Logging into ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
echo -e "${GREEN}✅ Logged in${NC}"

# Step 4: Tag and push image
echo -e "\n${YELLOW}📤 Step 4: Pushing image to ECR...${NC}"
ECR_IMAGE="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG"
$DOCKER_CMD tag $REPO_NAME:$IMAGE_TAG $ECR_IMAGE
$DOCKER_CMD push $ECR_IMAGE
echo -e "${GREEN}✅ Image pushed${NC}"

# Step 5: Instructions for App Runner
echo -e "\n${GREEN}✅ Deployment preparation complete!${NC}\n"
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "1. Go to AWS Console → App Runner"
echo "2. Create/Update service with this image:"
echo -e "   ${GREEN}$ECR_IMAGE${NC}"
echo ""
echo "3. Set environment variables:"
echo "   - POLYGON_API_KEY"
echo "   - OPENAI_API_KEY"
echo "   - TRADIER_API_KEY"
echo "   - FINNHUB_API_KEY"
echo ""
echo "4. Configure:"
echo "   - Port: 8000"
echo "   - CPU: 1 vCPU"
echo "   - Memory: 2 GB"
echo ""
echo -e "${YELLOW}Or use AWS CLI:${NC}"
echo "aws apprunner create-service \\"
echo "  --service-name market-parser \\"
echo "  --source-configuration '{\"ImageRepository\":{\"ImageIdentifier\":\"$ECR_IMAGE\",\"ImageRepositoryType\":\"ECR\",\"ImageConfiguration\":{\"Port\":\"8000\"}}}' \\"
echo "  --instance-configuration '{\"Cpu\":\"1 vCPU\",\"Memory\":\"2 GB\"}'"
