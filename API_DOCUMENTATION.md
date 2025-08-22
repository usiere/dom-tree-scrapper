# API Documentation - DOM Tree Extraction Service

## 🌐 **Service Overview**

**Base URL**: https://dom-tree-scraper-326385607594.us-central1.run.app  
**API Version**: v1  
**Status**: ✅ Production Ready  

The DOM Tree Extraction Service provides a RESTful API for extracting hierarchical DOM tree structures from web pages using Playwright automation.

## 📡 **API Endpoints**

### **1. Health Check**
**Endpoint**: `GET /health`  
**Description**: Service health status and uptime information  
**Authentication**: None required  

#### **Request**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/health"
```

#### **Response**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-22T14:38:06.037741",
  "service": "dom-tree-extractor",
  "version": "1.0.0"
}
```

#### **Response Fields**
- `status`: Service health status (`healthy` | `unhealthy`)
- `timestamp`: ISO 8601 timestamp of health check
- `service`: Service identifier
- `version`: API version number

---

### **2. Quick Test Endpoint**
**Endpoint**: `GET /api/v1/div-tree/quick`  
**Description**: Immediate response endpoint for testing connectivity  
**Authentication**: None required  

#### **Request**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree/quick"
```

#### **Response**
```json
{
  "data": {
    "label": "Quick Test Response",
    "children": [
      {
        "label": "Service is working",
        "children": [],
        "href": null
      },
      {
        "label": "Ready for full extraction",
        "children": [],
        "href": null
      }
    ],
    "href": null
  },
  "metadata": {
    "url": "quick_test",
    "extracted_at": "2025-08-22T17:45:19.621747",
    "duration_seconds": 0.0,
    "node_count": 3,
    "extraction_status": "quick_test"
  }
}
```

#### **Response Fields**
- `data`: Sample tree structure for testing
- `metadata`: Test metadata with quick_test status
- `duration_seconds`: Always 0.0 for immediate response

---

### **3. Root Endpoint**
**Endpoint**: `GET /`  
**Description**: API information and available endpoints  
**Authentication**: None required  

#### **Request**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/"
```

#### **Response**
```json
{
  "message": "DOM Tree Extraction API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "root": "/",
    "extract_tree": "/api/v1/div-tree",
    "status": "/api/v1/status",
    "docs": "/docs"
  },
  "status": "operational"
}
```

---

### **4. DOM Tree Extraction (GET)**
**Endpoint**: `GET /api/v1/div-tree`  
**Description**: Extract DOM tree structure from a web page  
**Authentication**: None required  

#### **Query Parameters**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | No | German business register | Target URL to extract tree from |
| `headless` | boolean | No | true | Run browser in headless mode |

#### **Request Examples**

**Extract from example.com:**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree?url=https://example.com"
```

**Extract from default target:**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree"
```

**Extract with visible browser (for debugging):**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree?url=https://example.com&headless=false"
```

#### **Success Response**
```json
{
  "data": {
    "label": "Example Domain\n    This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.\n    More information...",
    "href": "https://www.iana.org/domains/example",
    "expandable": false,
    "children": [
      {
        "label": "Example Domain\n    This domain is for use in illustrative examples in documents. You may use this\n  ",
        "href": "https://www.iana.org/domains/example",
        "expandable": false,
        "children": [
          {
            "label": "Example Domain",
            "expandable": false,
            "children": []
          },
          {
            "label": "This domain is for use in illustrative examples in documents. You may use this\n    domain in literat",
            "expandable": false,
            "children": []
          },
          {
            "label": "More information...",
            "href": "https://www.iana.org/domains/example",
            "expandable": false,
            "children": [
              {
                "label": "More information...",
                "expandable": false,
                "children": []
              }
            ]
          }
        ]
      }
    ]
  },
  "metadata": {
    "url": "https://example.com",
    "extracted_at": "2025-08-22T14:45:06.270134",
    "duration_seconds": 7.71,
    "node_count": 6,
    "extraction_status": "success",
    "output_file": "output/tree_20250822_144513.json"
  }
}
```

#### **Response Structure**

**Data Section (`data`):**
- `label`: Text content of the node
- `href`: Link URL (if applicable)
- `expandable`: Whether the node can be expanded
- `children`: Array of child nodes (recursive structure)

**Metadata Section (`metadata`):**
- `url`: Source URL that was processed
- `extracted_at`: ISO 8601 timestamp of extraction
- `duration_seconds`: Total processing time in seconds
- `node_count`: Total number of nodes in the tree
- `extraction_status`: Status of extraction (`success` | `failed` | `timeout`)
- `output_file`: Local file path where tree was saved

---

### **5. DOM Tree Extraction (POST)**
**Endpoint**: `POST /api/v1/div-tree`  
**Description**: Extract DOM tree structure via POST (useful for long URLs)  
**Authentication**: None required  

#### **Request Body**
```json
{
  "url": "https://example.com",
  "headless": true
}
```

#### **Request Example**
```bash
curl -X POST "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "headless": true}'
```

#### **Response**
Same format as GET endpoint.

---

### **6. API Status**
**Endpoint**: `GET /api/v1/status`  
**Description**: Get current API status and feature list  
**Authentication**: None required  

#### **Request**
```bash
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/status"
```

#### **Response**
```json
{
  "status": "operational",
  "timestamp": "2025-08-22T14:38:06.037741",
  "uptime": "running",
  "version": "1.0.0",
  "features": [
    "DOM tree extraction",
    "Playwright automation",
    "JSON output",
    "File saving"
  ]
}
```

---

### **7. API Documentation (Swagger UI)**
**Endpoint**: `GET /docs`  
**Description**: Interactive API documentation using Swagger UI  
**Authentication**: None required  

**Access**: https://dom-tree-scraper-326385607594.us-central1.run.app/docs

---

### **8. API Documentation (ReDoc)**
**Endpoint**: `GET /redoc`  
**Description**: Alternative API documentation using ReDoc  
**Authentication**: None required  

**Access**: https://dom-tree-scraper-326385607594.us-central1.run.app/redoc

---

### **9. OpenAPI Schema**
**Endpoint**: `GET /openapi.json`  
**Description**: OpenAPI 3.0 specification in JSON format  
**Authentication**: None required  

**Access**: https://dom-tree-scraper-326385607594.us-central1.run.app/openapi.json

## 🚨 **Error Handling**

### **Error Response Format**
All error responses follow a consistent format:

```json
{
  "error": {
    "error": "Detailed error message",
    "stage": "extraction|navigation|expansion",
    "message": "User-friendly description",
    "extraction_status": "failed|timeout|error"
  },
  "timestamp": "2025-08-22T14:38:49.748978",
  "path": "http://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree"
}
```

### **Common Error Scenarios**

#### **1. Navigation Timeout**
```json
{
  "error": {
    "error": "Page.goto: Timeout 60000ms exceeded.\nCall log:\n  - navigating to \"https://example.com/\", waiting until \"domcontentloaded\"",
    "stage": "extraction",
    "message": "Failed to extract tree structure",
    "extraction_status": "failed"
  },
  "timestamp": "2025-08-22T14:38:49.748978",
  "path": "http://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree"
}
```

#### **2. Tree Expansion Timeout**
```json
{
  "error": {
    "error": "Tree expansion timed out after 60 seconds",
    "stage": "expand",
    "message": "Failed to expand all nodes within time limit",
    "extraction_status": "timeout"
  },
  "timestamp": "2025-08-22T14:38:49.748978",
  "path": "http://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree"
}
```

#### **3. Invalid URL**
```json
{
  "error": {
    "error": "Invalid URL format: not-a-url",
    "stage": "validation",
    "message": "URL validation failed",
    "extraction_status": "failed"
  },
  "timestamp": "2025-08-22T14:38:49.748978",
  "path": "http://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree"
}
```

### **HTTP Status Codes**
| Status Code | Description | Use Case |
|-------------|-------------|----------|
| `200` | Success | Tree extraction completed successfully |
| `400` | Bad Request | Invalid URL or parameters |
| `408` | Request Timeout | Tree expansion exceeded time limit |
| `500` | Internal Server Error | Server-side processing error |
| `503` | Service Unavailable | Service temporarily unavailable |

## 📊 **Performance Characteristics**

### **Response Times**
- **Health Check**: < 100ms
- **Simple Tree**: 5-15 seconds
- **Complex Tree**: 15-60 seconds
- **Timeout Limit**: 60 seconds (well within 120s requirement)

### **Resource Usage**
- **Memory**: Optimized for Cloud Run constraints
- **CPU**: Single-threaded processing
- **Network**: Efficient browser automation
- **Storage**: Temporary file storage for results

### **Scalability**
- **Concurrent Requests**: Supports multiple simultaneous extractions
- **Auto-scaling**: Cloud Run automatic scaling
- **Load Distribution**: Stateless design for horizontal scaling

## 🔒 **Security & Rate Limiting**

### **Current Implementation**
- **Authentication**: None required (public API)
- **Rate Limiting**: Not implemented (can be added)
- **Input Validation**: URL format and content validation
- **Resource Protection**: Timeout and memory limits

### **Security Considerations**
- **URL Validation**: Prevents malicious URL injection
- **Timeout Protection**: Prevents resource exhaustion
- **Container Isolation**: Docker-based security
- **Cloud Run Security**: Google Cloud security features

## 📱 **Client Libraries & SDKs**

### **Python Example**
```python
import requests

def extract_dom_tree(url):
    """Extract DOM tree from URL"""
    api_url = "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree"
    params = {"url": url}
    
    response = requests.get(api_url, params=params, timeout=120)
    response.raise_for_status()
    
    return response.json()

# Usage
try:
    result = extract_dom_tree("https://example.com")
    print(f"Extracted {result['metadata']['node_count']} nodes")
    print(f"Status: {result['metadata']['extraction_status']}")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

### **JavaScript Example**
```javascript
async function extractDomTree(url) {
    const apiUrl = 'https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree';
    const params = new URLSearchParams({ url });
    
    try {
        const response = await fetch(`${apiUrl}?${params}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log(`Extracted ${result.metadata.node_count} nodes`);
        console.log(`Status: ${result.metadata.extraction_status}`);
        
        return result;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Usage
extractDomTree('https://example.com')
    .then(result => console.log('Success:', result))
    .catch(error => console.error('Failed:', error));
```

### **cURL Examples**
```bash
# Basic extraction
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree?url=https://example.com"

# With custom timeout
curl --max-time 120 "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree?url=https://example.com"

# Save to file
curl "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree?url=https://example.com" > tree_result.json

# POST request
curl -X POST "https://dom-tree-scraper-326385607594.us-central1.run.app/api/v1/div-tree" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  -o tree_result.json
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. Timeout Errors**
- **Cause**: Page takes too long to load or tree is very complex
- **Solution**: Use shorter timeout or simpler pages
- **Prevention**: Check page complexity before extraction

#### **2. Memory Errors**
- **Cause**: Very large DOM trees
- **Solution**: Process smaller sections or use pagination
- **Prevention**: Implement tree size limits

#### **3. Network Errors**
- **Cause**: Target site is down or blocking requests
- **Solution**: Check site availability and try again
- **Prevention**: Implement retry logic

### **Debug Information**
- **Logs**: Check Cloud Run logs for detailed error information
- **Health**: Use `/health` endpoint to verify service status
- **Metrics**: Monitor response times and success rates
- **Screenshots**: Local testing can generate debug screenshots

## 📈 **Monitoring & Analytics**

### **Available Metrics**
- **Response Times**: Per-request timing information
- **Success Rates**: Extraction success/failure ratios
- **Resource Usage**: Memory and CPU utilization
- **Error Rates**: Error frequency and types

### **Health Monitoring**
- **Uptime**: Service availability monitoring
- **Performance**: Response time tracking
- **Errors**: Error rate and type monitoring
- **Resources**: Container health and resource usage

---

**API Version**: 1.0  
**Last Updated**: August 22, 2025  
**Status**: ✅ PRODUCTION READY  
**Documentation**: Interactive docs available at `/docs` 