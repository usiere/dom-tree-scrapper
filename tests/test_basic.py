#!/usr/bin/env python3
"""
Basic tests for DOM Tree Extraction project
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from tree_extractor import TreeExtractor
        print("✅ TreeExtractor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TreeExtractor: {e}")
        return False
    
    try:
        from main import navigate_to_target_page, analyze_page_structure
        print("✅ Main module functions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import main module functions: {e}")
        return False
    
    return True

def test_fastapi_imports():
    """Test FastAPI application imports"""
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from app import app
        print("✅ FastAPI app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FastAPI app: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Running basic tests...")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("FastAPI Imports", test_fastapi_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Project setup is correct.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    exit(main()) 