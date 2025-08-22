from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
import json
import os

app = FastAPI(
    title="DOM Tree Extractor - Simple Version",
    description="A simplified version for testing deployment",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "DOM Tree Extractor API",
        "status": "running",
        "version": "1.0.0",
        "note": "This is a simplified version for testing deployment"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "dom-tree-extractor",
        "version": "1.0.0"
    }

@app.get("/api/v1/div-tree")
async def get_div_tree(url: str = Query(None, description="Target URL to extract DOM tree from")):
    start_time = datetime.now()
    
    if not url:
        url = "https://example.com"
    
    import time
    time.sleep(1)
    
    tree_data = {
        "label": "html",
        "tag": "html",
        "attributes": {"lang": "en"},
        "children": [
            {
                "label": "head",
                "tag": "head",
                "attributes": {},
                "children": [
                    {
                        "label": "title",
                        "tag": "title",
                        "attributes": {},
                        "children": [],
                        "text": "Example Domain"
                    }
                ]
            },
            {
                "label": "body",
                "tag": "body",
                "attributes": {},
                "children": [
                    {
                        "label": "h1",
                        "tag": "h1",
                        "attributes": {},
                        "children": [],
                        "text": "Example Domain"
                    }
                ]
            }
        ]
    }
    
    duration = (datetime.now() - start_time).total_seconds()
    node_count = 5
    
    output_data = {
        "data": tree_data,
        "metadata": {
            "url": url,
            "extracted_at": start_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "node_count": node_count,
            "extraction_status": "success",
            "note": "Mock data - Playwright integration pending"
        }
    }
    
    return output_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
