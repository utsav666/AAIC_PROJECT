#!/bin/bash
# ============================================
# ONE-TIME SETUP — Safe to run multiple times
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
LOG_GROUP="/ecs/scalable-api"
SECRET_NAME="scalable-api/llm-api-key"

# ─── ECR ───
echo "=== ECR Repository ==="
if aws ecr describe-repositories --repository-names $REPO_NAME --region $REGION > /dev/null 2>&1; then
    echo "  ↳ Already exists, skipping."
else
    aws ecr create-repository --repository-name $REPO_NAME --region $REGION > /dev/null
    echo "  ↳ Created."
fi

# ─── ECS CLUSTER ───
echo "=== ECS Cluster ==="
CLUSTER_STATUS=$(aws ecs describe-clusters --clusters $CLUSTER_NAME --region $REGION \
    --query "clusters[?status=='ACTIVE'].clusterName" --output text 2>/dev/null)
if [ -n "$CLUSTER_STATUS" ]; then
    echo "  ↳ Already exists, skipping."
else
    aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION > /dev/null
    echo "  ↳ Created."
fi

# ─── CLOUDWATCH LOG GROUP ───
echo "=== CloudWatch Log Group ==="
if aws logs describe-log-groups --log-group-name-prefix $LOG_GROUP --region $REGION \
    --query "logGroups[?logGroupName=='$LOG_GROUP'].logGroupName" --output text 2>/dev/null | grep -q "$LOG_GROUP"; then
    echo "  ↳ Already exists, skipping."
else
    aws logs create-log-group --log-group-name $LOG_GROUP --region $REGION
    echo "  ↳ Created."
fi

# ─── SECRETS MANAGER ───
echo "=== Secrets Manager ==="
if aws secretsmanager describe-secret --secret-id $SECRET_NAME --region $REGION > /dev/null 2>&1; then
    echo "  ↳ Already exists, skipping."
    echo "  ↳ To update: aws secretsmanager put-secret-value --secret-id $SECRET_NAME --secret-string NEW_VALUE --region $REGION"
else
    echo "Enter your LLM API key:"
    read -s LLM_KEY
    aws secretsmanager create-secret --name $SECRET_NAME --secret-string "$LLM_KEY" --region $REGION > /dev/null
    echo "  ↳ Created."
fi

# ─── VPC INFO ───
echo ""
echo "=== VPC Info (pick subnet + security group for deploy.sh) ==="
echo ""
echo "--- Subnets ---"
aws ec2 describe-subnets --region $REGION \
    --query "Subnets[*].{ID:SubnetId,AZ:AvailabilityZone,VPC:VpcId,Public:MapPublicIpOnLaunch}" \
    --output table

echo ""
echo "--- Security Groups ---"
aws ec2 describe-security-groups --region $REGION \
    --query "SecurityGroups[*].{ID:GroupId,Name:GroupName,VPC:VpcId}" \
    --output table

echo ""
echo "=== Setup Complete ==="
echo "Pick SUBNET_ID and SG_ID from above → put them in deploy.sh"
