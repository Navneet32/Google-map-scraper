from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os
import sys

print("🚀 Starting Google Maps Scraper API...")
print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")

app = FastAPI(title="Google Maps Scraper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Google Maps Scraper API", 
        "version": "1.0.0", 
        "status": "active",
        "port": os.environ.get('PORT', 'NOT SET'),
        "endpoints": ["/", "/health", "/test-chrome"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "port": os.environ.get('PORT', 'NOT SET')
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
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--remote-debugging-port=9222")
        print("✅ Chrome options configured")
        
        # Try to create driver
        try:
            # Test system Chrome first
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://www.google.com")
            title = driver.title
            driver.quit()
            method = "system-chrome"
        except Exception as e1:
            try:
                # Try with ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.get("https://www.google.com")
                title = driver.title
                driver.quit()
                method = "chromedriver-manager"
            except Exception as e2:
                return {
                    "status": "error",
                    "message": f"Chrome failed. System: {str(e1)}, Manager: {str(e2)}",
                    "timestamp": datetime.now().isoformat()
                }
        
        return {
            "status": "success",
            "message": "Chrome browser working correctly",
            "method": method,
            "test_page_title": title,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Chrome test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
