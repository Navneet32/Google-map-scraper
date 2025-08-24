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
        "endpoints": ["/", "/health", "/test-dependencies", "/install-selenium", "/test-chrome"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "port": os.environ.get('PORT', 'NOT SET')
    }

@app.get("/test-dependencies")
async def test_dependencies():
    """Test if all Python dependencies are installed"""
    try:
        dependencies = {}

        # Test FastAPI
        try:
            import fastapi
            dependencies["fastapi"] = fastapi.__version__
        except ImportError as e:
            dependencies["fastapi"] = f"ERROR: {str(e)}"

        # Test Selenium
        try:
            import selenium
            dependencies["selenium"] = selenium.__version__
        except ImportError as e:
            dependencies["selenium"] = f"ERROR: {str(e)}"

        # Test other dependencies
        try:
            import uvicorn
            dependencies["uvicorn"] = uvicorn.__version__
        except ImportError as e:
            dependencies["uvicorn"] = f"ERROR: {str(e)}"

        try:
            import pydantic
            dependencies["pydantic"] = pydantic.__version__
        except ImportError as e:
            dependencies["pydantic"] = f"ERROR: {str(e)}"

        return {
            "status": "success",
            "dependencies": dependencies,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Dependency test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/install-selenium")
async def install_selenium():
    """Try to install selenium manually"""
    try:
        import subprocess
        import sys

        # Try to install selenium
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "selenium==4.15.2"
        ], capture_output=True, text=True, timeout=60)

        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Manual selenium install failed: {str(e)}",
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

        # Enhanced Chrome options for Railway deployment
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--no-zygote")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-login-animations")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor,VizHitTestSurfaceLayer")
        chrome_options.add_argument("--disable-ipc-flooding-protection")

        # Set Chrome binary location for Docker - try multiple paths
        import os
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser"
        ]

        chrome_binary = None
        for path in chrome_paths:
            if os.path.exists(path):
                chrome_binary = path
                break

        if chrome_binary:
            chrome_options.binary_location = chrome_binary
            print(f"✅ Found Chrome binary at: {chrome_binary}")
        else:
            print("⚠️ No Chrome binary found, using system default")

        # Fix user data directory issue
        import tempfile
        import uuid
        temp_dir = tempfile.mkdtemp()
        unique_user_data_dir = f"{temp_dir}/chrome_user_data_{uuid.uuid4().hex[:8]}"
        chrome_options.add_argument(f"--user-data-dir={unique_user_data_dir}")

        print("✅ Chrome options configured with unique user data directory")

        # Try to create driver with system Chrome only (avoid WebDriver Manager issues)
        try:
            # Use system Chrome directly
            driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome driver created successfully")

            # Simple test - just get the title without navigation
            driver.get("data:text/html,<html><head><title>Test Page</title></head><body>Test</body></html>")
            title = driver.title
            print(f"✅ Test page loaded: {title}")

            driver.quit()
            print("✅ Chrome driver closed successfully")

            # Clean up temp directory
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

            return {
                "status": "success",
                "message": "Chrome browser working correctly on Railway",
                "method": "system-chrome",
                "test_page_title": title,
                "user_data_dir": unique_user_data_dir,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Chrome test failed: {str(e)}")

            # Clean up temp directory on error
            import shutil
            try:
                shutil.rmtree(temp_dir)
            except:
                pass

            return {
                "status": "error",
                "message": f"Chrome failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    except Exception as e:
        print(f"❌ General error: {str(e)}")
        return {
            "status": "error",
            "message": f"Chrome test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Get port from environment, default to 8000
    port = int(os.environ.get("PORT", 8000))

    print(f"🔍 Environment PORT: {os.environ.get('PORT', 'NOT SET')}")
    print(f"🌐 Starting server on 0.0.0.0:{port}")

    # Start the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
