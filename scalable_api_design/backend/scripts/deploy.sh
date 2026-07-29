#!/bin/bash
# ============================================
# DEPLOY — Run every time you change code
# ============================================

set -e

# ─── LOAD CONFIG ───
# Priority: environment variables (GitHub Secrets in CI/CD) > .env file (local dev)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

# Only load .env if it exists (won't exist in CI/CD)
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | grep -v '^\s*$' | xargs)
fi

# ─── DERIVED CONFIG ───
ACCOUNT_ID="${AWS_ACCOUNT_ID:?AWS_ACCOUNT_ID not set. Set in .env or as env var.}"
REGION="${AWS_REGION:-us-east-1}"
REPO_NAME="scalable-api"
CLUSTER_NAME="scalable-api-cluster"
SERVICE_NAME="scalable-api-service"
IMAGE="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

# VPC config
SUBNET_ID="${AWS_SUBNET_ID:?AWS_SUBNET_ID not set. Set in .env or as env var.}"
SG_ID="${AWS_SG_ID:?AWS_SG_ID not set. Set in .env or as env var.}"

# ─── BUILD ───
echo "=== Step 1: Build Docker Image ==="
cd "$SCRIPT_DIR/../"
docker build --platform linux/amd64 --no-cache -t $REPO_NAME .

# ─── PUSH ───
echo "=== Step 2: Login to ECR ==="
aws ecr get-login-password --region $REGION | \
    docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

echo "=== Step 3: Tag and Push ==="
docker tag $REPO_NAME:latest $IMAGE:latest
docker push $IMAGE:latest

# ─── TASK DEFINITION ───
echo "=== Step 4: Register Task Definition ==="
cat > /tmp/task-def.json << EOF
{
  "family": "scalable-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::${ACCOUNT_ID}:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "scalable-api",
      "image": "${IMAGE}:latest",
      "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
      "environment": [
        {"name": "APP_ENV", "value": "prod"},
        {"name": "LLM_PROVIDER", "value": "${LLM_PROVIDER}"},
        {"name": "LLM_BASE_URL", "value": "${LLM_BASE_URL}"},
        {"name": "LLM_MODEL", "value": "${LLM_MODEL}"}
      ],
      "secrets": [
        {
          "name": "LLM_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:${REGION}:${ACCOUNT_ID}:secret:scalable-api/llm-api-key"
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
          "awslogs-region": "${REGION}",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
EOF

aws ecs register-task-definition \
    --cli-input-json file:///tmp/task-def.json \
    --region $REGION > /dev/null

# ─── DEPLOY ───
echo "=== Step 5: Deploy ==="
SERVICE_EXISTS=$(aws ecs describe-services \
    --cluster $CLUSTER_NAME \
    --services $SERVICE_NAME \
    --region $REGION \
    --query "services[?status=='ACTIVE'].serviceName" \
    --output text 2>/dev/null)

if [ -z "$SERVICE_EXISTS" ]; then
    echo "  ↳ Creating new service..."
    aws ecs create-service \
        --cluster $CLUSTER_NAME \
        --service-name $SERVICE_NAME \
        --task-definition scalable-api \
        --desired-count 1 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SG_ID],assignPublicIp=ENABLED}" \
        --region $REGION > /dev/null
    echo "  ↳ Service created."
else
    echo "  ↳ Stopping old tasks..."
    OLD_TASKS=$(aws ecs list-tasks \
        --cluster $CLUSTER_NAME \
        --service-name $SERVICE_NAME \
        --region $REGION \
        --query "taskArns[]" --output text 2>/dev/null)

    if [ -n "$OLD_TASKS" ]; then
        for TASK in $OLD_TASKS; do
            aws ecs stop-task --cluster $CLUSTER_NAME --task "$TASK" --region $REGION > /dev/null 2>&1
            echo "  ↳ Stopped: $(echo $TASK | awk -F'/' '{print $NF}')"
        done
    fi

    echo "  ↳ Updating service with new task definition..."
    aws ecs update-service \
        --cluster $CLUSTER_NAME \
        --service $SERVICE_NAME \
        --task-definition scalable-api \
        --force-new-deployment \
        --region $REGION > /dev/null
    echo "  ↳ Redeployment triggered."
fi

# ─── CLEANUP OLD TASK DEFINITIONS ───
echo "=== Step 6: Cleanup old task definitions ==="
OLD_DEFS=$(aws ecs list-task-definitions \
    --family-prefix scalable-api \
    --status ACTIVE \
    --sort DESC \
    --region $REGION \
    --query "taskDefinitionArns[1:]" --output text 2>/dev/null)

if [ -n "$OLD_DEFS" ] && [ "$OLD_DEFS" != "None" ]; then
    for DEF in $OLD_DEFS; do
        aws ecs deregister-task-definition --task-definition "$DEF" --region $REGION > /dev/null 2>&1
        echo "  ↳ Deregistered: $(echo $DEF | awk -F'/' '{print $NF}')"
    done
else
    echo "  ↳ No old definitions to clean up."
fi

# ─── WAIT FOR DEPLOYMENT ───
echo "=== Step 7: Waiting for new task to start ==="
echo "  ↳ This may take 1-2 minutes..."
aws ecs wait services-stable \
    --cluster $CLUSTER_NAME \
    --services $SERVICE_NAME \
    --region $REGION 2>/dev/null && echo "  ↳ Service is stable and running." || echo "  ↳ Timeout waiting. Check manually."

echo ""
echo "=== Deploy Complete ==="
echo "Check status:"
echo "  aws ecs describe-services --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION --query 'services[0].{Status:status,Running:runningCount,Desired:desiredCount}'"
