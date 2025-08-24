#!/usr/bin/env python3
"""
Simplified Google Maps Scraper API for Railway deployment
This version initializes Chrome only when needed to avoid startup issues
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import uvicorn
import os

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
    max_results: Optional[int] = 100
    visit_websites: Optional[bool] = True

class BusinessResult(BaseModel):
    name: str
    address: str
    rating: Optional[float]
    review_count: Optional[int]
    category: str
    website: Optional[str]
    mobile: Optional[str]
    email: Optional[str]
    secondary_email: Optional[str]
    google_maps_url: str
    search_query: str
    website_visited: bool
    additional_contacts: str

class SearchResponse(BaseModel):
    success: bool
    data: List[BusinessResult]
    total_results: int
    message: str

# Basic endpoints
@app.get("/")
async def root():
    return {"message": "Google Maps Scraper API", "version": "1.0.0", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/test-chrome")
async def test_chrome():
    """Test if Chrome browser can be initialized"""
    try:
        print("🧪 Testing Chrome browser initialization...")
        
        # Import here to avoid startup issues
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Test Chrome setup
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Try system Chrome first
        try:
            driver = webdriver.Chrome(options=chrome_options)
            method = "system"
        except:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            method = "chromedriver-manager"
        
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
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
            "message": f"Chrome browser test failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.post("/scrape", response_model=SearchResponse)
async def scrape_google_maps(request: SearchRequest):
    """
    Scrape Google Maps for business information
    """
    try:
        print(f"🔍 Received scraping request: {request.query}")
        print(f"📊 Max results: {request.max_results}, Visit websites: {request.visit_websites}")
        
        # Import the scraper class here to avoid startup issues
        from main import AdvancedContactExtractor
        
        # Create extractor instance
        print("🚀 Initializing Google Maps extractor...")
        extractor = AdvancedContactExtractor(
            search_query=request.query,
            max_results=request.max_results,
            visit_websites=request.visit_websites
        )
        
        # Run extraction
        print("Starting extraction process...")
        results = extractor.run_extraction()
        print(f"Extraction completed. Results type: {type(results)}")
        
        if results and isinstance(results, list):
            # Convert results to BusinessResult objects
            business_results = []
            for result in results:
                if result:  # Skip None results
                    business_result = BusinessResult(
                        name=result.get('name', 'Unknown Business'),
                        address=result.get('address', 'Address not found'),
                        rating=result.get('rating'),
                        review_count=result.get('review_count'),
                        category=result.get('category', 'Unknown Category'),
                        website=result.get('website'),
                        mobile=result.get('mobile'),
                        email=result.get('email'),
                        secondary_email=result.get('secondary_email'),
                        google_maps_url=result.get('google_maps_url', ''),
                        search_query=result.get('search_query', request.query),
                        website_visited=result.get('website_visited', False),
                        additional_contacts=result.get('additional_contacts', '')
                    )
                    business_results.append(business_result)
            
            return SearchResponse(
                success=True,
                data=business_results,
                total_results=len(business_results),
                message=f"Successfully scraped {len(business_results)} businesses"
            )
        else:
            return SearchResponse(
                success=False,
                data=[],
                total_results=0,
                message="No results found or extraction failed"
            )
            
    except Exception as e:
        print(f"Scraping error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
