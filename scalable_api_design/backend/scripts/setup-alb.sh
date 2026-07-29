#!/bin/bash
# ============================================
# SETUP INTERNAL ALB — For accessing API from corporate network
# Safe to run multiple times. All config from .env
# ============================================

set -e

# ─── LOAD CONFIG ───
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | grep -v '^\s*$' | xargs)
fi

# ─── DERIVED CONFIG (all from .env) ───
ACCOUNT_ID="${AWS_ACCOUNT_ID:?AWS_ACCOUNT_ID not set.}"
REGION="${AWS_REGION:-us-east-1}"
VPC_ID="${AWS_VPC_ID:?AWS_VPC_ID not set.}"
SUBNET_ID="${AWS_SUBNET_ID:?AWS_SUBNET_ID not set.}"
SG_ID="${AWS_SG_ID:?AWS_SG_ID not set.}"
ALB_SUBNET_1="${AWS_ALB_SUBNET_1:?AWS_ALB_SUBNET_1 not set.}"
ALB_SUBNET_2="${AWS_ALB_SUBNET_2:?AWS_ALB_SUBNET_2 not set.}"
ALB_SG="${AWS_ALB_SG:?AWS_ALB_SG not set.}"
CERT_ARN="${AWS_CERT_ARN:?AWS_CERT_ARN not set.}"

ALB_NAME="scalable-api-internal-alb"
TG_NAME="scalable-api-tg"
CLUSTER_NAME="scalable-api-cluster"
SERVICE_NAME="scalable-api-service"

# ─── CREATE TARGET GROUP ───
echo "=== Target Group ==="
TG_ARN=$(aws elbv2 describe-target-groups \
    --names $TG_NAME \
    --region $REGION \
    --query "TargetGroups[0].TargetGroupArn" --output text 2>/dev/null || echo "")

if [ -n "$TG_ARN" ] && [ "$TG_ARN" != "None" ] && [ "$TG_ARN" != "" ]; then
    echo "  ↳ Already exists: $TG_ARN"
else
    TG_ARN=$(aws elbv2 create-target-group \
        --name $TG_NAME \
        --protocol HTTP \
        --port 8000 \
        --vpc-id $VPC_ID \
        --target-type ip \
        --health-check-path /health \
        --health-check-interval-seconds 30 \
        --healthy-threshold-count 2 \
        --unhealthy-threshold-count 3 \
        --region $REGION \
        --query "TargetGroups[0].TargetGroupArn" --output text)
    echo "  ↳ Created: $TG_ARN"
fi

# ─── CREATE INTERNAL ALB ───
echo "=== Internal Application Load Balancer ==="
ALB_ARN=$(aws elbv2 describe-load-balancers \
    --names $ALB_NAME \
    --region $REGION \
    --query "LoadBalancers[0].LoadBalancerArn" --output text 2>/dev/null || echo "")

if [ -n "$ALB_ARN" ] && [ "$ALB_ARN" != "None" ] && [ "$ALB_ARN" != "" ]; then
    echo "  ↳ Already exists."
else
    ALB_ARN=$(aws elbv2 create-load-balancer \
        --name $ALB_NAME \
        --subnets $ALB_SUBNET_1 $ALB_SUBNET_2 \
        --security-groups $ALB_SG \
        --scheme internal \
        --type application \
        --region $REGION \
        --query "LoadBalancers[0].LoadBalancerArn" --output text)
    echo "  ↳ Created. Waiting for it to become active..."
    aws elbv2 wait load-balancer-available --load-balancer-arns $ALB_ARN --region $REGION
    echo "  ↳ ALB is active."
fi

# ─── CREATE LISTENER ───
echo "=== HTTPS Listener (port 443) ==="
LISTENER_EXISTS=$(aws elbv2 describe-listeners \
    --load-balancer-arn $ALB_ARN \
    --region $REGION \
    --query "Listeners[?Port==\`443\`].ListenerArn" --output text 2>/dev/null || echo "")

if [ -n "$LISTENER_EXISTS" ] && [ "$LISTENER_EXISTS" != "None" ] && [ "$LISTENER_EXISTS" != "" ]; then
    echo "  ↳ Already exists."
else
    aws elbv2 create-listener \
        --load-balancer-arn $ALB_ARN \
        --protocol HTTPS --port 443 \
        --certificates CertificateArn=$CERT_ARN \
        --default-actions Type=forward,TargetGroupArn=$TG_ARN \
        --region $REGION > /dev/null
    echo "  ↳ Created (HTTPS 443 → target group port 8000)."
fi

# ─── ALLOW ALB SG TO REACH CONTAINER ───
echo "=== Security Group Rules ==="
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8000 \
    --source-group $ALB_SG \
    --region $REGION > /dev/null 2>&1 && echo "  ↳ Added: ALB SG → container port 8000" || echo "  ↳ Rule already exists, skipping."

# ─── UPDATE ECS SERVICE TO USE ALB ───
echo "=== Update ECS Service ==="
echo "  ↳ Scaling down existing service..."
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --desired-count 0 --region $REGION > /dev/null 2>&1
echo "  ↳ Waiting for tasks to stop..."
sleep 10
echo "  ↳ Deleting service..."
aws ecs delete-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --region $REGION > /dev/null 2>&1
sleep 5

echo "  ↳ Creating service with load balancer..."
aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name $SERVICE_NAME \
    --task-definition scalable-api \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SG_ID],assignPublicIp=DISABLED}" \
    --load-balancers "targetGroupArn=$TG_ARN,containerName=scalable-api,containerPort=8000" \
    --region $REGION > /dev/null

echo "  ↳ Service created with ALB."

# ─── WAIT AND SHOW URL ───
echo "=== Waiting for service to stabilize ==="
echo "  ↳ This may take 1-2 minutes..."
aws ecs wait services-stable --cluster $CLUSTER_NAME --services $SERVICE_NAME --region $REGION 2>/dev/null || true

# Get ALB DNS name
ALB_DNS=$(aws elbv2 describe-load-balancers \
    --names $ALB_NAME \
    --region $REGION \
    --query "LoadBalancers[0].DNSName" --output text)

echo ""
echo "========================================="
echo "  YOUR API URL (HTTPS):"
echo "  https://$ALB_DNS/health"
echo "  https://$ALB_DNS/docs"
echo "========================================="
echo ""
echo "Test with:"
echo "  curl -k https://$ALB_DNS/health"
echo "  Browser: https://$ALB_DNS/docs"
