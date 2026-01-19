#!/bin/bash
# Deployment script for SchoolSharthi

set -e

echo "🚀 Starting SchoolSharthi Deployment..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install it first."
    exit 1
fi

# Configuration
AWS_REGION="ap-south-1"
ECR_REPO="schoolsharthi-backend"
ECS_CLUSTER="schoolsharthi-cluster"
ECS_SERVICE="schoolsharthi-backend"

echo -e "${BLUE}📦 Building Docker image...${NC}"
cd backend
docker build -t $ECR_REPO:latest .

echo -e "${BLUE}🔐 Logging in to ECR...${NC}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo -e "${BLUE}📤 Pushing image to ECR...${NC}"
docker tag $ECR_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

echo -e "${BLUE}🚀 Deploying to ECS...${NC}"
aws ecs update-service \
  --cluster $ECS_CLUSTER \
  --service $ECS_SERVICE \
  --force-new-deployment \
  --region $AWS_REGION

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${BLUE}📊 Check deployment status:${NC}"
echo "aws ecs describe-services --cluster $ECS_CLUSTER --services $ECS_SERVICE --region $AWS_REGION"
