#!/usr/bin/env python3
"""
Test script for Google Maps scraper
"""

import requests
import json
import time

# Test the scraper endpoints
BASE_URL = "https://google-map-scraper-production-702a.up.railway.app"

def test_local_scraper():
    """Test the local scraper directly"""
    try:
        print("\n🧪 Testing local scraper directly...")
        from google_maps_scraper import GoogleMapsBusinessScraper

        scraper = GoogleMapsBusinessScraper(
            search_query="pizza restaurants in New York",
            max_results=2,
            visit_websites=False
        )

        results = scraper.run_extraction()

        if results:
            print(f"✅ Local scraper works! Found {len(results)} results")
            for result in results[:1]:  # Show first result
                print(f"- {result['name']}: {result['address']}")
            return True
        else:
            print("❌ Local scraper returned no results")
            return False

    except Exception as e:
        print(f"❌ Local scraper failed: {str(e)}")
        return False

def test_endpoint(endpoint, method="GET", data=None):
    """Test an endpoint and return the response"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🧪 Testing {method} {endpoint}")
        print(f"URL: {url}")
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=60)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"❌ Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def main():
    print("🚀 Testing Google Maps Scraper API")
    print("=" * 50)

    # Test 0: Local scraper test (to verify it works)
    local_works = test_local_scraper()

    # Test 1: Health check
    test_endpoint("/health")

    # Test 2: Chrome test
    test_endpoint("/test-chrome")

    # Test 3: Google Maps test (small sample)
    test_endpoint("/test-google-maps")

    # Test 4: Full scraping test (only if local works)
    if local_works:
        scrape_data = {
            "query": "pizza restaurants in New York",
            "max_results": 5,
            "visit_websites": False
        }

        print(f"\n🍕 Testing full scraping with: {scrape_data}")
        result = test_endpoint("/scrape", method="POST", data=scrape_data)
    else:
        print("\n⚠️ Skipping API scraping test since local scraper failed")
    
    if result and result.get("success"):
        print(f"\n🎉 Scraping successful!")
        print(f"Found {result.get('total_results')} businesses")
        
        # Show sample results
        if result.get("data"):
            print("\n📋 Sample results:")
            for i, business in enumerate(result["data"][:2]):  # Show first 2
                print(f"\n{i+1}. {business.get('name', 'Unknown')}")
                print(f"   Address: {business.get('address', 'N/A')}")
                print(f"   Rating: {business.get('rating', 'N/A')}")
                print(f"   Category: {business.get('category', 'N/A')}")
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    main()
