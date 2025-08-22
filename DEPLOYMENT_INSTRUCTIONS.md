# Deployment Instructions - DOM Tree Extraction Service

## 🚀 **Complete GCP Deployment Guide**

This document provides step-by-step instructions for deploying the DOM Tree Extraction service to Google Cloud Platform (GCP) using Google Cloud Run.

## 📋 **Prerequisites**

### **Required Tools**
- **Google Cloud SDK**: Command-line tools for GCP
- **Docker**: For local container testing (optional)
- **Git**: For source code management
- **Terminal/Command Prompt**: For executing commands

### **GCP Requirements**
- **Google Cloud Account**: Active account with billing enabled
- **Project**: GCP project with sufficient permissions
- **APIs**: Cloud Run, Cloud Build, and Container Registry enabled

## 🔧 **Step 1: Install Google Cloud SDK**

### **macOS (using Homebrew)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Google Cloud SDK
brew install --cask google-cloud-sdk

# Initialize and authenticate
gcloud init
gcloud auth login
```

### **Windows**
```bash
# Download and install from:
# https://cloud.google.com/sdk/docs/install#windows

# Initialize and authenticate
gcloud init
gcloud auth login
```

### **Linux (Ubuntu/Debian)**
```bash
# Add Google Cloud SDK distribution URI
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install
sudo apt-get update && sudo apt-get install google-cloud-sdk

# Initialize and authenticate
gcloud init
gcloud auth login
```

## 🌐 **Step 2: Set Up Google Cloud Project**

### **Create or Select Project**
```bash
# List existing projects
gcloud projects list

# Create new project (if needed)
gcloud projects create [PROJECT_ID] --name="[PROJECT_NAME]"

# Set active project
gcloud config set project [PROJECT_ID]

# Enable billing (required for Cloud Run)
# Note: This must be done through the GCP Console
# Visit: https://console.cloud.google.com/billing
```

### **Enable Required APIs**
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Verify enabled APIs
gcloud services list --enabled
```

### **Set Up IAM Permissions**
```bash
# Grant Cloud Build service account necessary permissions
gcloud projects add-iam-policy-binding [PROJECT_ID] \
    --member="serviceAccount:[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding [PROJECT_ID] \
    --member="serviceAccount:[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com" \
    --role="roles/containerregistry.ServiceAgent"
```

## 📁 **Step 3: Prepare Source Code**

### **Clone or Download Project**
```bash
# Clone from repository (if available)
git clone [REPOSITORY_URL]
cd dom-tree-scraper

# Or download and extract project files
# Ensure all required files are present:
# - app.py
# - Dockerfile
# - requirements.txt
# - src/ directory
# - deploy.sh
```

### **Verify Project Structure**
```bash
# Check project structure
ls -la

# Expected files:
# - app.py (FastAPI application)
# - Dockerfile (Container configuration)
# - requirements.txt (Python dependencies)
# - deploy.sh (Deployment script)
# - src/ (Source code directory)
```

## 🐳 **Step 4: Deploy Using Automated Script**

### **Make Script Executable**
```bash
# Make deployment script executable
chmod +x deploy.sh

# Verify script permissions
ls -la deploy.sh
```

### **Run Deployment**
```bash
# Deploy to Cloud Run
./deploy.sh [PROJECT_ID]

# Example:
./deploy.sh my-project-123
```

### **What the Script Does**
1. **Sets Project**: Configures active GCP project
2. **Enables APIs**: Activates required GCP services
3. **Builds Image**: Uses Cloud Build to create Docker image
4. **Pushes Image**: Uploads image to Container Registry
5. **Deploys Service**: Creates Cloud Run service
6. **Tests Deployment**: Verifies service functionality

## 🔨 **Step 5: Manual Deployment (Alternative)**

If you prefer manual deployment or need to customize the process:

### **Build and Push Docker Image**
```bash
# Build Docker image
gcloud builds submit --tag gcr.io/[PROJECT_ID]/dom-tree-scraper

# Verify image creation
gcloud container images list --repository=gcr.io/[PROJECT_ID]
```

### **Deploy to Cloud Run**
```bash
# Deploy service
gcloud run deploy dom-tree-scraper \
    --image gcr.io/[PROJECT_ID]/dom-tree-scraper \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --timeout 120s \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10

# Get service URL
gcloud run services describe dom-tree-scraper \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

## ✅ **Step 6: Verify Deployment**

### **Test Health Endpoint**
```bash
# Test health check
curl "https://[SERVICE_URL]/health"

# Expected response:
# {"status":"healthy","timestamp":"...","service":"dom-tree-extractor","version":"1.0.0"}
```

### **Test Tree Extraction**
```bash
# Test with example.com
curl "https://[SERVICE_URL]/api/v1/div-tree?url=https://example.com"

# Test default target
curl "https://[SERVICE_URL]/api/v1/div-tree"
```

### **Check Service Status**
```bash
# View service details
gcloud run services describe dom-tree-scraper \
    --platform managed \
    --region us-central1

# View service logs
gcloud logs tail --service=dom-tree-scraper --region=us-central1
```

## 🔍 **Step 7: Troubleshooting**

### **Common Issues and Solutions**

#### **1. Billing Not Enabled**
```bash
# Error: "Billing account required"
# Solution: Enable billing in GCP Console
# Visit: https://console.cloud.google.com/billing
```

#### **2. API Not Enabled**
```bash
# Error: "API not enabled"
# Solution: Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

#### **3. Permission Denied**
```bash
# Error: "Permission denied"
# Solution: Grant necessary IAM roles
gcloud projects add-iam-policy-binding [PROJECT_ID] \
    --member="serviceAccount:[PROJECT_NUMBER]@cloudbuild.gserviceaccount.com" \
    --role="roles/storage.admin"
```

#### **4. Build Failure**
```bash
# Error: "Build step failure"
# Solution: Check build logs
gcloud builds log [BUILD_ID]

# Common causes:
# - Dockerfile syntax errors
# - Missing dependencies
# - Resource constraints
```

#### **5. Service Deployment Failure**
```bash
# Error: "Service deployment failed"
# Solution: Check service logs
gcloud logs tail --service=dom-tree-scraper --region=us-central1

# Common causes:
# - Image not found
# - Port configuration issues
# - Resource allocation problems
```

## 📊 **Step 8: Monitor and Maintain**

### **View Service Metrics**
```bash
# View service metrics in GCP Console
# Visit: https://console.cloud.google.com/run
# Select your service and view metrics
```

### **Update Service**
```bash
# Update service with new image
gcloud run services update dom-tree-scraper \
    --image gcr.io/[PROJECT_ID]/dom-tree-scraper:latest \
    --region us-central1
```

### **Scale Service**
```bash
# Update scaling configuration
gcloud run services update dom-tree-scraper \
    --max-instances 20 \
    --min-instances 1 \
    --region us-central1
```

### **Delete Service**
```bash
# Remove service (if needed)
gcloud run services delete dom-tree-scraper \
    --platform managed \
    --region us-central1
```

## 🔐 **Step 9: Security Considerations**

### **Authentication (Optional)**
```bash
# Deploy with authentication required
gcloud run deploy dom-tree-scraper \
    --image gcr.io/[PROJECT_ID]/dom-tree-scraper \
    --platform managed \
    --region us-central1 \
    --no-allow-unauthenticated \
    --port 8080
```

### **Custom Domain (Optional)**
```bash
# Map custom domain to service
gcloud run domain-mappings create \
    --service dom-tree-scraper \
    --domain [YOUR_DOMAIN] \
    --region us-central1
```

## 📚 **Step 10: Additional Resources**

### **Useful Commands**
```bash
# List all Cloud Run services
gcloud run services list --platform managed

# View service configuration
gcloud run services describe dom-tree-scraper --region us-central1

# Update service environment variables
gcloud run services update dom-tree-scraper \
    --set-env-vars "ENVIRONMENT=production" \
    --region us-central1

# View service logs
gcloud logs tail --service=dom-tree-scraper --region=us-central1
```

### **GCP Console Links**
- **Cloud Run**: https://console.cloud.google.com/run
- **Cloud Build**: https://console.cloud.google.com/cloud-build
- **Container Registry**: https://console.cloud.google.com/gcr
- **Logging**: https://console.cloud.google.com/logs
- **Monitoring**: https://console.cloud.google.com/monitoring

### **Documentation**
- **Cloud Run**: https://cloud.google.com/run/docs
- **Cloud Build**: https://cloud.google.com/cloud-build/docs
- **Container Registry**: https://cloud.google.com/container-registry/docs

## 🎯 **Deployment Checklist**

### **Pre-Deployment**
- [ ] Google Cloud SDK installed and authenticated
- [ ] GCP project created and selected
- [ ] Billing enabled for project
- [ ] Required APIs enabled
- [ ] Source code prepared and verified
- [ ] IAM permissions configured

### **Deployment**
- [ ] Docker image built successfully
- [ ] Image pushed to Container Registry
- [ ] Cloud Run service deployed
- [ ] Service accessible via HTTPS
- [ ] Health endpoint responding
- [ ] Tree extraction working

### **Post-Deployment**
- [ ] Service logs monitored
- [ ] Performance metrics reviewed
- [ ] Error handling verified
- [ ] Documentation updated
- [ ] Team access configured
- [ ] Monitoring alerts set up

## 🎉 **Success Indicators**

Your deployment is successful when:

1. **Service URL**: Returns a valid HTTPS URL
2. **Health Check**: `/health` endpoint returns `{"status": "healthy"}`
3. **Tree Extraction**: `/api/v1/div-tree` successfully extracts DOM trees
4. **Performance**: Response times within acceptable limits
5. **Logs**: No critical errors in service logs
6. **Monitoring**: Service metrics showing healthy operation

---

**Deployment Guide Version**: 1.0  
**Last Updated**: August 22, 2025  
**Status**: ✅ COMPLETE AND VERIFIED  
**Next Steps**: Test your deployed service and monitor performance 