# SchoolSharthi Deployment Plan

Complete deployment guide for AWS backend, Vercel frontend, RDS database, S3 storage, and AI scaling with cost optimization for rural students.

## Architecture Overview

```
┌─────────────────┐
│   Vercel        │  Frontend (Next.js)
│   (CDN + Edge)  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  CloudFront     │  CDN + WAF
│  (Optional)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐
│  API Gateway    │────▶│  ECS/Fargate │────▶│  RDS         │
│  (Optional)     │     │  FastAPI     │     │  PostgreSQL  │
└─────────────────┘     └──────────────┘     └──────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  S3          │
                         │  (Files)     │
                         └──────────────┘
```

## 1. Backend Deployment (AWS)

### Option A: AWS ECS Fargate (Recommended for Low Cost)

#### 1.1 Create ECR Repository
```bash
aws ecr create-repository --repository-name schoolsharthi-backend --region ap-south-1
```

#### 1.2 Build and Push Docker Image
```bash
cd backend
docker build -t schoolsharthi-backend .
docker tag schoolsharthi-backend:latest <account-id>.dkr.ecr.ap-south-1.amazonaws.com/schoolsharthi-backend:latest
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/schoolsharthi-backend:latest
```

#### 1.3 Create ECS Task Definition
```json
{
  "family": "schoolsharthi-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.ap-south-1.amazonaws.com/schoolsharthi-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "from-secrets"},
        {"name": "SECRET_KEY", "value": "from-secrets"},
        {"name": "AWS_REGION", "value": "ap-south-1"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:ap-south-1:<account-id>:secret:schoolsharthi/db-url"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:ap-south-1:<account-id>:secret:schoolsharthi/secret-key"
        },
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:ap-south-1:<account-id>:secret:schoolsharthi/openai-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/schoolsharthi-backend",
          "awslogs-region": "ap-south-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 1.4 Create ECS Cluster and Service
```bash
# Create cluster
aws ecs create-cluster --cluster-name schoolsharthi-cluster --region ap-south-1

# Create service
aws ecs create-service \
  --cluster schoolsharthi-cluster \
  --service-name schoolsharthi-backend \
  --task-definition schoolsharthi-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:ap-south-1:xxx:targetgroup/xxx,containerName=backend,containerPort=8000"
```

### Option B: AWS Elastic Beanstalk (Simpler, Higher Cost)

#### 1.1 Create Application
```bash
eb init -p python-3.11 schoolsharthi-backend --region ap-south-1
eb create schoolsharthi-env --instance-type t3.micro --min-instances 1 --max-instances 2
```

#### 1.2 Configure Environment Variables
```bash
eb setenv DATABASE_URL=$DATABASE_URL SECRET_KEY=$SECRET_KEY AWS_REGION=ap-south-1
```

### Option C: AWS Lambda + API Gateway (Ultra Low Cost)

See `lambda_deployment/` directory for serverless setup.

## 2. Database (AWS RDS)

### 2.1 Create RDS PostgreSQL Instance
```bash
aws rds create-db-instance \
  --db-instance-identifier schoolsharthi-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username postgres \
  --master-user-password <secure-password> \
  --allocated-storage 20 \
  --storage-type gp3 \
  --vpc-security-group-ids sg-xxx \
  --db-subnet-group-name schoolsharthi-subnet-group \
  --backup-retention-period 7 \
  --multi-az \
  --publicly-accessible false \
  --region ap-south-1
```

### 2.2 Cost Optimization
- Use `db.t3.micro` for development (free tier eligible)
- Use `db.t3.small` for production (~$15/month)
- Enable automated backups (7 days retention)
- Use Multi-AZ only for production
- Use Reserved Instances for 1-3 year commitment (40-60% savings)

### 2.3 Connection String
```
postgresql://postgres:password@schoolsharthi-db.xxxxx.ap-south-1.rds.amazonaws.com:5432/schoolsharthi
```

## 3. File Storage (S3)

### 3.1 Create S3 Bucket
```bash
aws s3 mb s3://schoolsharthi-notes --region ap-south-1
aws s3api put-bucket-versioning --bucket schoolsharthi-notes --versioning-configuration Status=Enabled
aws s3api put-bucket-encryption --bucket schoolsharthi-notes --server-side-encryption-configuration '{
  "Rules": [{
    "ApplyServerSideEncryptionByDefault": {
      "SSEAlgorithm": "AES256"
    }
  }]
}'
```

### 3.2 Configure CORS
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://schoolsharthi.vercel.app"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

### 3.3 Create IAM Policy for S3 Access
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::schoolsharthi-notes/*"
    }
  ]
}
```

### 3.4 Cost Optimization
- Use S3 Intelligent-Tiering for automatic cost optimization
- Set lifecycle policies to move old files to Glacier
- Enable S3 Transfer Acceleration only if needed
- Use CloudFront for frequently accessed files

## 4. Frontend Deployment (Vercel)

### 4.1 Connect Repository
1. Push code to GitHub
2. Import project in Vercel
3. Connect GitHub repository

### 4.2 Configure Environment Variables
In Vercel Dashboard → Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL=https://api.schoolsharthi.com
```

### 4.3 Vercel Configuration (`vercel.json`)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["bom1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.schoolsharthi.com/api/:path*"
    }
  ]
}
```

### 4.4 Custom Domain Setup
1. Add domain in Vercel Dashboard
2. Configure DNS records:
   - A record: `@` → Vercel IP
   - CNAME: `www` → cname.vercel-dns.com

## 5. AI Scaling

### 5.1 OpenAI API Optimization
- Use `gpt-3.5-turbo` instead of `gpt-4` (10x cheaper)
- Implement response caching for common queries
- Rate limiting per user
- Batch requests when possible

### 5.2 Caching Strategy
```python
# Use Redis for caching AI responses
import redis
redis_client = redis.Redis(host='elasticache-endpoint', port=6379)

async def get_cached_response(query_hash: str):
    cached = redis_client.get(query_hash)
    if cached:
        return json.loads(cached)
    return None

async def cache_response(query_hash: str, response: str, ttl=3600):
    redis_client.setex(query_hash, ttl, json.dumps(response))
```

### 5.3 Elasticache Setup
```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id schoolsharthi-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --region ap-south-1
```

### 5.4 Cost Optimization
- Cache common queries (1 hour TTL)
- Use streaming responses for long answers
- Implement request queuing for high traffic
- Monitor API usage and set budgets

## 6. CI/CD Pipeline

### 6.1 GitHub Actions Workflow (`.github/workflows/deploy.yml`)
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-south-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build, tag, and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: schoolsharthi-backend
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ./backend
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster schoolsharthi-cluster \
            --service schoolsharthi-backend \
            --force-new-deployment \
            --region ap-south-1

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
```

### 6.2 Secrets Management
Store in GitHub Secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## 7. Security

### 7.1 AWS Security Groups
```bash
# Backend Security Group
aws ec2 create-security-group \
  --group-name schoolsharthi-backend-sg \
  --description "Security group for backend" \
  --vpc-id vpc-xxx

# Allow HTTPS from ALB
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 8000 \
  --source-group sg-alb-xxx

# RDS Security Group
aws ec2 authorize-security-group-ingress \
  --group-id sg-rds-xxx \
  --protocol tcp \
  --port 5432 \
  --source-group sg-backend-xxx
```

### 7.2 SSL/TLS Certificates
```bash
# Request certificate in ACM
aws acm request-certificate \
  --domain-name api.schoolsharthi.com \
  --validation-method DNS \
  --region ap-south-1
```

### 7.3 WAF Rules (Optional)
- Rate limiting: 100 requests/minute per IP
- SQL injection protection
- XSS protection
- Geographic restrictions (if needed)

### 7.4 Environment Variables Security
- Use AWS Secrets Manager for sensitive data
- Never commit `.env` files
- Rotate secrets regularly
- Use IAM roles instead of access keys where possible

## 8. Monitoring & Logging

### 8.1 CloudWatch Setup
```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/schoolsharthi-backend

# Create CloudWatch alarms
aws cloudwatch put-metric-alarm \
  --alarm-name schoolsharthi-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### 8.2 Application Monitoring
- Use Sentry for error tracking
- CloudWatch Logs Insights for querying logs
- Set up SNS alerts for critical issues

## 9. Cost Optimization for Rural Students

### 9.1 Monthly Cost Estimate (Optimized)

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| RDS (db.t3.micro) | Single AZ, 20GB | $15 |
| ECS Fargate | 0.25 vCPU, 0.5GB | $8 |
| S3 Storage | 100GB, Intelligent-Tiering | $2 |
| CloudFront | 50GB transfer | $4 |
| Vercel | Hobby Plan | $0 (or $20) |
| Elasticache | cache.t3.micro | $12 |
| Data Transfer | 100GB | $9 |
| **Total** | | **~$50/month** |

### 9.2 Cost Reduction Strategies

1. **Use AWS Free Tier**
   - RDS: 750 hours/month free for 12 months
   - S3: 5GB free forever
   - Lambda: 1M requests free

2. **Reserved Instances**
   - 1-year commitment: 40% savings
   - 3-year commitment: 60% savings

3. **Spot Instances** (for non-critical workloads)
   - Up to 90% savings
   - Use for batch processing

4. **S3 Lifecycle Policies**
   - Move old files to Glacier (cheaper)
   - Delete unused files after 1 year

5. **CDN Caching**
   - Reduce origin requests
   - Lower data transfer costs

6. **Database Optimization**
   - Use connection pooling
   - Optimize queries
   - Use read replicas for scaling reads

### 9.3 Scaling Strategy
- Start with minimum resources
- Auto-scale based on demand
- Use scheduled scaling for known patterns
- Monitor costs with AWS Cost Explorer

## 10. Deployment Checklist

### Pre-Deployment
- [ ] Set up AWS account
- [ ] Create IAM users/roles
- [ ] Configure VPC and subnets
- [ ] Set up RDS instance
- [ ] Create S3 bucket
- [ ] Configure security groups
- [ ] Set up SSL certificates
- [ ] Configure secrets in Secrets Manager

### Deployment
- [ ] Build and push Docker image
- [ ] Create ECS cluster and service
- [ ] Deploy frontend to Vercel
- [ ] Configure environment variables
- [ ] Set up custom domains
- [ ] Configure DNS records
- [ ] Test all endpoints

### Post-Deployment
- [ ] Set up monitoring and alerts
- [ ] Configure backup schedules
- [ ] Set up CI/CD pipeline
- [ ] Document runbooks
- [ ] Set up cost alerts
- [ ] Performance testing
- [ ] Security audit

## 11. Disaster Recovery

### 11.1 Backup Strategy
- RDS automated backups (7 days)
- S3 versioning enabled
- Database snapshots before major changes
- Export critical data monthly

### 11.2 Recovery Plan
1. RDS: Restore from snapshot (15-30 minutes)
2. S3: Versioning allows point-in-time recovery
3. Application: Redeploy from Git (5-10 minutes)
4. DNS: Failover to backup region (if configured)

## 12. Maintenance Windows

- Schedule maintenance during low-traffic hours
- Use blue-green deployments for zero downtime
- Test in staging environment first
- Monitor during and after deployment

## 13. Support & Documentation

- API documentation: `/docs` endpoint (FastAPI)
- Runbooks for common issues
- Contact information for emergencies
- Status page for users

## Quick Start Commands

```bash
# Deploy backend
cd backend
docker build -t schoolsharthi-backend .
# ... push to ECR and deploy to ECS

# Deploy frontend
cd frontend
vercel --prod

# Run database migrations
python backend/init_db.py

# Monitor logs
aws logs tail /ecs/schoolsharthi-backend --follow
```

## Estimated Monthly Costs

**Development/Staging:** ~$30/month
**Production (Low Traffic):** ~$50/month
**Production (Medium Traffic):** ~$100/month
**Production (High Traffic):** ~$200-500/month

All costs can be optimized further based on actual usage patterns.
