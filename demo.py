#!/usr/bin/env python3
"""
DOM Tree Extraction - Demo Script
Demonstrates the key functionality of the project
"""

import asyncio
import json
from src.tree_extractor import TreeExtractor, extract_tree_from_url
from playwright.sync_api import sync_playwright

def demo_local_extraction():
    """Demo local tree extraction"""
    print("🌳 Demo: Local Tree Extraction")
    print("=" * 50)
    
    try:
        # Extract tree from a simple test page
        test_url = "https://example.com"
        print(f"Testing with: {test_url}")
        
        tree_data = extract_tree_from_url(test_url, headless=True)
        
        print(f"✅ Successfully extracted tree with {len(tree_data.get('children', []))} root children")
        print(f"Root label: {tree_data.get('label', 'N/A')}")
        
        # Save to file
        with open("output/demo_tree.json", "w") as f:
            json.dump(tree_data, f, indent=2)
        print("💾 Tree saved to: output/demo_tree.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def demo_page_analysis():
    """Demo page structure analysis"""
    print("\n🔍 Demo: Page Structure Analysis")
    print("=" * 50)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu'
                ]
            )
            page = browser.new_page()
            
            # Navigate to a test page
            page.goto("https://example.com", wait_until='networkidle')
            
            # Create extractor and analyze
            extractor = TreeExtractor(page)
            
            # Find expandable nodes
            expandable = extractor.find_expandable_nodes()
            print(f"Found {len(expandable)} expandable nodes")
            
            # Take screenshot
            page.screenshot(path="assets/demo_page.png")
            print("📸 Screenshot saved to: assets/demo_page.png")
            
            browser.close()
            return True
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def demo_api_endpoints():
    """Demo API endpoints"""
    print("\n🚀 Demo: API Endpoints")
    print("=" * 50)
    
    try:
        # Import and test FastAPI app
        from app import app
        
        # Check available routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(f"{route.methods} {route.path}")
        
        print("Available endpoints:")
        for route in routes:
            print(f"  {route}")
        
        print("\n✅ FastAPI app is ready to run")
        print("Run with: python app.py")
        print("Access docs at: http://localhost:8080/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def main():
    """Run all demos"""
    print("🎯 DOM Tree Extraction - Complete Demo")
    print("=" * 60)
    
    demos = [
        ("Local Extraction", demo_local_extraction),
        ("Page Analysis", demo_page_analysis),
        ("API Endpoints", demo_api_endpoints),
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        try:
            if demo_func():
                passed += 1
                print(f"✅ {demo_name} completed successfully")
            else:
                print(f"❌ {demo_name} failed")
        except Exception as e:
            print(f"❌ {demo_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Demo Results: {passed}/{total} demos completed")
    
    if passed == total:
        print("🎉 All demos completed successfully!")
        print("\n🚀 Your DOM Tree Extraction project is ready!")
        print("\nNext steps:")
        print("1. Run the API: python app.py")
        print("2. Test endpoints: curl http://localhost:8080/health")
        print("3. Build Docker: docker build -t dom-tree-scraper .")
        print("4. Deploy to GCP: ./deploy.sh YOUR-PROJECT-ID")
    else:
        print("⚠️  Some demos failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    exit(0 if main() else 1) 