#!/bin/bash

# DOM Tree Extraction - Google Cloud Run Deployment Script
# Phase 7: Google Cloud Deployment

set -e  # Exit on any error

# Configuration
PROJECT_ID=${1:-"your-project-id"}  # Pass as first argument or set default
REGION=${2:-"us-central1"}
SERVICE_NAME="dom-tree-scraper"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 DOM Tree Extraction - Google Cloud Run Deployment"
echo "=================================================="
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo "Image: $IMAGE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Authenticating with Google Cloud..."
    gcloud auth login
fi

# Set project
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push Docker image
echo "🐳 Building and pushing Docker image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --timeout 120s \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars "ENVIRONMENT=production" \
    --port 8080

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --format 'value(status.url)')

echo ""
echo "✅ Deployment completed successfully!"
echo "Service URL: $SERVICE_URL"
echo ""

# Test the deployed service
echo "🧪 Testing deployed service..."

# Test health endpoint
echo "Testing health endpoint..."
if curl -s "$SERVICE_URL/health" | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
fi

# Test root endpoint
echo "Testing root endpoint..."
if curl -s "$SERVICE_URL/" | grep -q "DOM Tree Extraction API"; then
    echo "✅ Root endpoint working"
else
    echo "❌ Root endpoint failed"
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "📚 Useful commands:"
echo "  View logs: gcloud logs tail --service=$SERVICE_NAME --region=$REGION"
echo "  Update service: gcloud run services update $SERVICE_NAME --region=$REGION"
echo "  Delete service: gcloud run services delete $SERVICE_NAME --region=$REGION"
echo ""
echo "🌐 Access your API at: $SERVICE_URL"
echo "📖 API Documentation: $SERVICE_URL/docs" 