#!/usr/bin/env python3
"""
Test script to debug the response structure
"""

import json
from datetime import datetime

# Simulate the exact response structure from app.py
def test_response():
    tree_data = {"label": "test", "children": []}
    start_time = datetime.now()
    target_url = "https://example.com"
    node_count = 1
    duration = 1.5
    output_filename = "test.json"
    
    response = {
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
    
    print("Response structure:")
    print(json.dumps(response, indent=2))
    
    print("\nMetadata keys:", list(response['metadata'].keys()))
    print("extraction_status present:", 'extraction_status' in response['metadata'])
    print("extraction_status value:", response['metadata'].get('extraction_status'))

if __name__ == "__main__":
    test_response() 