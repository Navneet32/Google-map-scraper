#!/usr/bin/env python3
"""
Ultra-simple Google Maps Scraper API for Railway deployment
Minimal dependencies, guaranteed to start
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uvicorn
import os
import sys

# Print startup info
print("🚀 Starting Google Maps Scraper API...")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"PORT: {os.environ.get('PORT', 'Not set')}")

# FastAPI app initialization
app = FastAPI(title="Google Maps Scraper API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    visit_websites: Optional[bool] = False

class BusinessResult(BaseModel):
    name: str
    address: str
    mobile: Optional[str]
    website: Optional[str]
    google_maps_url: str

class SearchResponse(BaseModel):
    success: bool
    data: List[BusinessResult]
    total_results: int
    message: str

# Basic endpoints
@app.get("/")
async def root():
    return {
        "message": "Google Maps Scraper API", 
        "version": "1.0.0", 
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version,
        "port": os.environ.get('PORT', 'Not set')
    }

@app.get("/test-simple")
async def test_simple():
    """Simple test endpoint"""
    try:
        return {
            "status": "success",
            "message": "Simple test passed",
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "python_version": sys.version,
                "port": os.environ.get('PORT'),
                "cwd": os.getcwd()
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Simple test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/test-chrome")
async def test_chrome():
    """Test if Chrome browser can be initialized"""
    try:
        print("🧪 Testing Chrome browser initialization...")
        
        # Try to import selenium
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            print("✅ Selenium imported successfully")
        except ImportError as e:
            return {
                "status": "error",
                "message": f"Selenium import failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        
        # Try to setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        print("✅ Chrome options configured")
        
        # Try to create driver (but don't actually start it yet)
        try:
            # Just test if we can create the driver object
            driver = webdriver.Chrome(options=chrome_options)
            driver.quit()
            method = "system-chrome"
        except Exception as e1:
            try:
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.quit()
                method = "chromedriver-manager"
            except Exception as e2:
                return {
                    "status": "error",
                    "message": f"Chrome initialization failed. System: {str(e1)}, Manager: {str(e2)}",
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "status": "success",
            "message": "Chrome browser test passed",
            "method": method,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Chrome test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.post("/scrape", response_model=SearchResponse)
async def scrape_google_maps(request: SearchRequest):
    """
    Scrape Google Maps for business information
    """
    try:
        print(f"🔍 Received scraping request: {request.query}")
        
        # For now, return a mock response to test the API structure
        mock_results = [
            BusinessResult(
                name="Test Coffee Shop",
                address="123 Test Street, Test City",
                mobile="+1 555-123-4567",
                website="https://testcoffee.com",
                google_maps_url="https://maps.google.com/test"
            )
        ]
        
        return SearchResponse(
            success=True,
            data=mock_results,
            total_results=len(mock_results),
            message=f"Mock response for query: {request.query}"
        )
            
    except Exception as e:
        print(f"Scraping error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
