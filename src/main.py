#!/usr/bin/env python3
"""
DOM Tree Extraction - Starter Code
Phase 1: Project Setup & Environment
"""

import asyncio
import time
from playwright.sync_api import sync_playwright
import os

def navigate_to_target_page(page, url="https://www.handelsregister.de/rp_web/welcome.xhtml"):
    """Navigate to the target page and wait for it to load"""
    print(f"Navigating to: {url}")
    
    try:
        # Navigate to the page
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Wait for the page to be fully loaded
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_load_state('networkidle')
        
        print(f"Successfully navigated to: {page.title()}")
        print(f"Current URL: {page.url}")
        
        # Take a screenshot for verification
        screenshot_path = "assets/page_loaded.png"
        os.makedirs("assets", exist_ok=True)
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")
        
        return True
        
    except Exception as e:
        print(f"Error navigating to page: {e}")
        return False

def analyze_page_structure(page):
    """Analyze the DOM to understand tree structure"""
    
    print("\n=== Page Structure Analysis ===")
    
    # Print page title and URL for verification
    print(f"Page Title: {page.title()}")
    print(f"Current URL: {page.url}")
    
    # Look for common tree indicators
    tree_containers = page.query_selector_all('[class*="tree"], [class*="expand"], [role="tree"]')
    print(f"Found {len(tree_containers)} potential tree containers")
    
    # Look for expandable elements
    expandable = page.query_selector_all('[aria-expanded], [class*="chevron"], [class*="collapse"]')
    print(f"Found {len(expandable)} potentially expandable elements")
    
    # Look for nested lists or hierarchical structures
    nested_lists = page.query_selector_all('ul ul, ol ol, div div[class*="level"]')
    print(f"Found {len(nested_lists)} nested structures")
    
    # Look for document-related elements
    document_links = page.query_selector_all('a[href*="document"], a[href*="file"]')
    print(f"Found {len(document_links)} document links")
    
    # Analyze the first few potential tree containers
    if tree_containers:
        print("\n--- Tree Container Analysis ---")
        for i, container in enumerate(tree_containers[:3]):
            print(f"Container {i+1}:")
            print(f"  Tag: {container.evaluate('el => el.tagName')}")
            print(f"  Classes: {container.get_attribute('class')}")
            print(f"  Role: {container.get_attribute('role')}")
            print(f"  Children count: {len(container.query_selector_all('*'))}")
    
    # Analyze expandable elements
    if expandable:
        print("\n--- Expandable Elements Analysis ---")
        for i, elem in enumerate(expandable[:3]):
            print(f"Element {i+1}:")
            print(f"  Tag: {elem.evaluate('el => el.tagName')}")
            print(f"  Classes: {elem.get_attribute('class')}")
            print(f"  Aria-expanded: {elem.get_attribute('aria-expanded')}")
            print(f"  Text: {elem.text_content()[:100]}...")

def main():
    """Main function to test the starter code"""
    print("🚀 DOM Tree Extraction - Starter Code Test")
    print("=" * 50)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(
            headless=False,  # Set to True for production
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        page = browser.new_page()
        
        try:
            # Navigate to target page
            if navigate_to_target_page(page):
                # Analyze page structure
                analyze_page_structure(page)
                
                # Take additional screenshots for analysis
                page.screenshot(path="assets/full_page.png", full_page=True)
                print("Full page screenshot saved to: assets/full_page.png")
                
                print("\n✅ Starter code executed successfully!")
                print("Check the assets/ folder for screenshots")
                
            else:
                print("❌ Failed to navigate to target page")
                
        except Exception as e:
            print(f"❌ Error during execution: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    main()
