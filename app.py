#!/usr/bin/env python3
"""
DOM Tree Extraction - FastAPI Application
Phase 5: FastAPI Application Development
"""

from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import os
import json

# Import our tree extractor
from src.tree_extractor import extract_tree_from_url, TreeExtractor
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="DOM Tree Extraction API",
    description="Extract hierarchical document trees from web pages using Playwright",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global configuration
DEFAULT_URL = "https://www.handelsregister.de/rp_web/welcome.xhtml"
MAX_TIMEOUT = 120  # seconds
DEFAULT_HEADLESS = True

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "DOM Tree Extraction API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tree_extraction": "/api/v1/div-tree",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "dom-tree-extractor",
        "version": "1.0.0"
    }

@app.get("/api/v1/div-tree")
async def get_div_tree(
    url: Optional[str] = Query(
        None, 
        description="Target URL to scrape (optional, uses default if not provided)"
    ),
    headless: bool = Query(
        DEFAULT_HEADLESS,
        description="Run browser in headless mode"
    )
):
    """
    Extract hierarchical tree structure from a web page
    
    Args:
        url: Target URL (optional, uses default if not provided)
        headless: Run browser in headless mode (default: True)
    
    Returns:
        JSON tree structure with labels, children, and optional hrefs
    """
    
    start_time = datetime.now()
    logger.info(f"Starting tree extraction at {start_time}")
    
    try:
        # Use default URL if none provided
        target_url = url or DEFAULT_URL
        logger.info(f"Extracting tree from URL: {target_url}")
        
        # Extract tree using our extractor
        tree_data = await extract_tree_async(target_url, headless)
        
        # Count nodes for metadata
        node_count = count_tree_nodes(tree_data)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Extraction completed in {duration:.2f}s, extracted {node_count} nodes")
        
        # Save to output directory with consistent format
        output_filename = f"output/tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("output", exist_ok=True)
        
        # Save with the same structure as API response
        output_data = {
            "data": tree_data,
            "metadata": {
                "url": target_url,
                "extracted_at": start_time.isoformat(),
                "duration_seconds": round(duration, 2),
                "node_count": node_count,
                "extraction_status": "success",
                "output_file": output_filename
            }
        }
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return {
            "data": tree_data,
            "metadata": {
                "url": target_url,
                "extracted_at": start_time.isoformat(),
                "duration_seconds": round(duration, 2),
                "node_count": node_count,
                "extraction_status": "success",
                "output_file": output_filename
            }
        }
        
    except asyncio.TimeoutError as e:
        logger.error(f"Timeout during extraction: {e}")
        raise HTTPException(
            status_code=408,
            detail={
                "error": "Timeout while expanding tree",
                "stage": "expand",
                "message": "Tree expansion took too long to complete",
                "extraction_status": "timeout"
            }
        )
    
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "stage": "extraction",
                "message": "Failed to extract tree structure",
                "extraction_status": "failed"
            }
        )

@app.post("/api/v1/div-tree")
async def post_div_tree(
    background_tasks: BackgroundTasks,
    url: str = Query(..., description="Target URL to scrape"),
    headless: bool = Query(DEFAULT_HEADLESS, description="Run browser in headless mode")
):
    """
    Extract tree structure via POST request (useful for longer URLs)
    """
    return await get_div_tree(url=url, headless=headless)

@app.get("/api/v1/status")
async def get_status():
    """Get current API status and statistics"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "version": "1.0.0",
        "features": [
            "DOM tree extraction",
            "Playwright automation",
            "JSON output",
            "File saving"
        ]
    }

async def extract_tree_async(url: str, headless: bool = True) -> Dict[str, Any]:
    """
    Async wrapper for tree extraction to avoid blocking the event loop
    """
    
    def sync_extract():
        """Synchronous tree extraction function"""
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--headless'
                ]
            )
            page = browser.new_page()
            
            try:
                # Navigate to the page with container-friendly settings
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                page.wait_for_load_state('domcontentloaded', timeout=30000)
                
                # Extract tree
                extractor = TreeExtractor(page)
                extractor.expand_all_nodes()
                tree_data = extractor.build_tree_structure()
                
                return tree_data
                
            finally:
                browser.close()
    
    # Run the synchronous extraction in a thread pool
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_extract)

def count_tree_nodes(tree_data: Dict[str, Any]) -> int:
    """Count total nodes in tree structure"""
    if not isinstance(tree_data, dict):
        return 0
    
    count = 1
    for child in tree_data.get('children', []):
        count += count_tree_nodes(child)
    return count

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with consistent error format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "Internal server error",
                "type": type(exc).__name__
            },
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
