# Manual Deployment Guide

## Prerequisites
- Docker installed locally
- AWS CLI configured with your lab role
- Account ID: <YOUR_AWS_ACCOUNT_ID>
- Region: us-east-1

---

## Step 1: Create Deployment Files

### Dockerfile (backend/Dockerfile)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

### .dockerignore (backend/.dockerignore)
```
__pycache__
*.pyc
.env
.git
tests/
scripts/
infra/
*.md
.env.example
```

---

## Step 2: Test Docker Locally

```bash
cd backend

# Build
docker build -t scalable-api .

# Run with env vars
docker run -p 8000:8000 \
  -e APP_ENV=dev \
  -e LLM_PROVIDER=claude \
  -e LLM_API_KEY=<YOUR_LLM_API_KEY> \
  -e LLM_BASE_URL=<YOUR_LLM_BASE_URL> \
  -e LLM_MODEL=<YOUR_LLM_MODEL> \
  scalable-api

# Test health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "tenant_id": "test"}'
```

---

## Step 3: Create ECR Repository

```bash
aws ecr create-repository \
  --repository-name scalable-api \
  --region us-east-1
```

---

## Step 4: Push Image to ECR

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag scalable-api:latest \
  <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/scalable-api:latest

# Push image
docker push \
  <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/scalable-api:latest
```

---

## Step 5: Store Secrets in AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name scalable-api/llm-api-key \
  --secret-string "<YOUR_LLM_API_KEY>" \
  --region us-east-1
```

---

## Step 6: Create ECS Cluster

```bash
aws ecs create-cluster \
  --cluster-name scalable-api-cluster \
  --region us-east-1
```

---

## Step 7: Create CloudWatch Log Group

```bash
aws logs create-log-group \
  --log-group-name /ecs/scalable-api \
  --region us-east-1
```

---

## Step 8: Register Task Definition

Save as `scripts/task-definition.json`:

```json
{
  "family": "scalable-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "scalable-api",
      "image": "<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/scalable-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "APP_ENV", "value": "prod"},
        {"name": "LLM_PROVIDER", "value": "claude"},
        {"name": "LLM_BASE_URL", "value": "<YOUR_LLM_BASE_URL>"},
        {"name": "LLM_MODEL", "value": "<YOUR_LLM_MODEL>"}
      ],
      "secrets": [
        {
          "name": "LLM_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<ACCOUNT_ID>:secret:scalable-api/llm-api-key"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/scalable-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register it:
```bash
aws ecs register-task-definition \
  --cli-input-json file://scripts/task-definition.json \
  --region us-east-1
```

---

## Step 9: Find VPC Subnet and Security Group

```bash
# List subnets
aws ec2 describe-subnets --region us-east-1 \
  --query "Subnets[*].{ID:SubnetId,AZ:AvailabilityZone,VPC:VpcId}" \
  --output table

# List security groups
aws ec2 describe-security-groups --region us-east-1 \
  --query "SecurityGroups[*].{ID:GroupId,Name:GroupName,VPC:VpcId}" \
  --output table
```

Pick a public subnet and a security group that allows inbound port 8000.

---

## Step 10: Create ECS Service

```bash
aws ecs create-service \
  --cluster scalable-api-cluster \
  --service-name scalable-api-service \
  --task-definition scalable-api \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[SUBNET_ID],securityGroups=[SG_ID],assignPublicIp=ENABLED}" \
  --region us-east-1
```

Replace `SUBNET_ID` and `SG_ID` with values from Step 9.

---

## Step 11: Verify Deployment

```bash
# Check service status
aws ecs describe-services \
  --cluster scalable-api-cluster \
  --services scalable-api-service \
  --region us-east-1

# Check running tasks
aws ecs list-tasks \
  --cluster scalable-api-cluster \
  --region us-east-1

# Get task public IP
aws ecs describe-tasks \
  --cluster scalable-api-cluster \
  --tasks TASK_ARN \
  --region us-east-1

# Test the deployed API
curl http://TASK_PUBLIC_IP:8000/health
```

---

## Redeploy After Code Changes

```bash
# Rebuild
docker build -t scalable-api .

# Tag and push
docker tag scalable-api:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/scalable-api:latest
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/scalable-api:latest

# Force new deployment
aws ecs update-service \
  --cluster scalable-api-cluster \
  --service scalable-api-service \
  --force-new-deployment \
  --region us-east-1
```

---

## Cleanup (if needed)

```bash
# Delete service
aws ecs update-service --cluster scalable-api-cluster --service scalable-api-service --desired-count 0
aws ecs delete-service --cluster scalable-api-cluster --service scalable-api-service

# Delete cluster
aws ecs delete-cluster --cluster scalable-api-cluster

# Delete ECR repo
aws ecr delete-repository --repository-name scalable-api --force

# Delete secret
aws secretsmanager delete-secret --secret-id scalable-api/llm-api-key --force-delete-without-recovery

# Delete log group
aws logs delete-log-group --log-group-name /ecs/scalable-api
```
