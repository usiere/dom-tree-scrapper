# 🚀 DOM Tree Extraction - Quick Start Guide

## ⚡ **Get Running in 5 Minutes**

This guide will get you up and running with the DOM Tree Extraction project immediately.

---

## 🎯 **What You'll Get**

- ✅ **Working DOM tree extractor** that can scrape any web page
- ✅ **FastAPI REST API** with full documentation
- ✅ **Local development environment** ready to use
- ✅ **Complete tree expansion algorithm** with intelligent node detection

---

## 🚀 **Step 1: Quick Test (2 minutes)**

```bash
# Navigate to project
cd dom-tree-scraper

# Activate environment
source venv/bin/activate

# Test the starter code
python src/main.py
```

**Expected Output:**
- ✅ Navigates to German business register page
- ✅ Analyzes DOM structure
- ✅ Takes screenshots
- ✅ Shows tree containers and expandable elements

---

## 🌐 **Step 2: Start the API (1 minute)**

```bash
# In the same terminal (keep venv activated)
python app.py
```

**Expected Output:**
- ✅ FastAPI server starts on http://localhost:8080
- ✅ API documentation available at http://localhost:8080/docs

---

## 🧪 **Step 3: Test API Endpoints (2 minutes)**

Open a new terminal and run:

```bash
# Health check
curl http://localhost:8080/health

# Extract tree from default URL
curl "http://localhost:8080/api/v1/div-tree"

# Extract tree from custom URL
curl "http://localhost:8080/api/v1/div-tree?url=https://example.com"
```

**Expected Output:**
- ✅ Health endpoint returns status
- ✅ Tree extraction returns JSON structure
- ✅ Metadata includes timing and node count

---

## 🎉 **You're Done!**

**Your DOM Tree Extraction project is now fully operational!**

---

## 🔍 **What You Can Do Now**

### **1. Extract Trees from Any Website**
```python
from src.tree_extractor import extract_tree_from_url

# Extract from any URL
tree = extract_tree_from_url("https://your-website.com")
print(f"Found {len(tree.get('children', []))} root children")
```

### **2. Use the REST API**
- **Local**: http://localhost:8080
- **Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

### **3. Customize Extraction**
```python
from src.tree_extractor import TreeExtractor
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate and extract
    page.goto("https://your-site.com")
    extractor = TreeExtractor(page)
    extractor.expand_all_nodes()
    tree = extractor.build_tree_structure()
    
    browser.close()
```

---

## 🚨 **Troubleshooting**

### **If starter code fails:**
```bash
# Reinstall Playwright
pip install --upgrade playwright
playwright install chromium
```

### **If API won't start:**
```bash
# Check dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :8080
```

### **If tree extraction is slow:**
- Increase timeout in `src/tree_extractor.py`
- Use `headless=False` for debugging
- Check network connectivity

---

## 📚 **Next Steps**

1. **Explore the API**: Visit http://localhost:8080/docs
2. **Test with your own URLs**: Modify the test scripts
3. **Customize selectors**: Edit `src/tree_extractor.py`
4. **Deploy to cloud**: Use `./deploy.sh` (requires GCP setup)

---

## 🎯 **Success Indicators**

✅ **Starter code runs without errors**
✅ **API starts on port 8080**
✅ **Health endpoint returns 200 OK**
✅ **Tree extraction returns JSON**
✅ **Screenshots saved to assets/ folder**

---

## 🆘 **Need Help?**

- **Check logs**: Look for error messages in terminal
- **Review documentation**: README.md has detailed information
- **Test step by step**: Run each component individually
- **Check dependencies**: Ensure all packages are installed

---

**🎉 Congratulations! You now have a fully functional DOM Tree Extraction system!** 