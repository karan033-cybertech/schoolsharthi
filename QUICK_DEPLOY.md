# Quick Deployment Guide

## Prerequisites

1. AWS Account
2. Vercel Account
3. GitHub Account
4. Docker installed
5. AWS CLI configured

## Step-by-Step Deployment

### 1. Backend (AWS ECS Fargate)

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name schoolsharthi-backend --region ap-south-1

# 2. Build and push image
cd backend
docker build -t schoolsharthi-backend .
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
docker tag schoolsharthi-backend:latest $AWS_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/schoolsharthi-backend:latest
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/schoolsharthi-backend:latest

# 3. Create ECS cluster
aws ecs create-cluster --cluster-name schoolsharthi-cluster --region ap-south-1

# 4. Create task definition (use task-definition.json)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 5. Create service
aws ecs create-service \
  --cluster schoolsharthi-cluster \
  --service-name schoolsharthi-backend \
  --task-definition schoolsharthi-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### 2. Database (RDS)

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier schoolsharthi-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username postgres \
  --master-user-password YourSecurePassword123! \
  --allocated-storage 20 \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name default \
  --region ap-south-1
```

### 3. S3 Bucket

```bash
# Create bucket
aws s3 mb s3://schoolsharthi-notes --region ap-south-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket schoolsharthi-notes \
  --versioning-configuration Status=Enabled
```

### 4. Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

### 5. Environment Variables

**Backend (ECS Task Definition):**
- `DATABASE_URL` - RDS connection string
- `SECRET_KEY` - JWT secret key
- `AWS_REGION` - ap-south-1
- `S3_BUCKET_NAME` - schoolsharthi-notes
- `OPENAI_API_KEY` - Your OpenAI API key

**Frontend (Vercel):**
- `NEXT_PUBLIC_API_URL` - Your backend API URL

### 6. CI/CD Setup

1. Add GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`

2. Push to main branch - automatic deployment!

## Cost Estimate

**Monthly Costs (Optimized):**
- RDS (db.t3.micro): $15
- ECS Fargate: $8
- S3: $2
- CloudFront: $4
- Vercel: $0 (Hobby) or $20 (Pro)
- **Total: ~$30-50/month**

## Troubleshooting

### Backend not starting
- Check CloudWatch logs: `/ecs/schoolsharthi-backend`
- Verify environment variables
- Check security groups

### Database connection issues
- Verify security group allows ECS to RDS
- Check RDS endpoint
- Verify credentials

### Frontend API errors
- Check CORS settings
- Verify `NEXT_PUBLIC_API_URL`
- Check network tab in browser

## Monitoring

```bash
# View ECS logs
aws logs tail /ecs/schoolsharthi-backend --follow

# Check service status
aws ecs describe-services \
  --cluster schoolsharthi-cluster \
  --services schoolsharthi-backend

# Monitor costs
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

## Security Checklist

- [ ] Use AWS Secrets Manager for sensitive data
- [ ] Enable SSL/TLS certificates
- [ ] Configure security groups properly
- [ ] Use IAM roles instead of access keys
- [ ] Enable CloudWatch logging
- [ ] Set up WAF rules (optional)
- [ ] Regular security audits

## Next Steps

1. Set up monitoring alerts
2. Configure backup schedules
3. Set up staging environment
4. Implement auto-scaling
5. Set up cost alerts

For detailed information, see `DEPLOYMENT_PLAN.md`
