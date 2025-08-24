#!/usr/bin/env python3
"""
Deployment verification script for Google Maps Scraper
Run this after deployment to verify everything is working
"""

import requests
import json
import time

def test_endpoint(base_url, endpoint, method="GET", data=None, timeout=60):
    """Test a single endpoint"""
    url = f"{base_url}{endpoint}"
    print(f"\n🧪 Testing {method} {endpoint}")
    print(f"URL: {url}")
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        else:
            response = requests.get(url, timeout=timeout)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {json.dumps(result, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ Timeout after {timeout} seconds")
        return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def verify_deployment(base_url):
    """Verify the entire deployment"""
    print("🚀 Verifying Google Maps Scraper Deployment")
    print("=" * 60)
    print(f"Base URL: {base_url}")
    
    results = {}
    
    # Test 1: Health check (should be fast)
    results['health'] = test_endpoint(base_url, "/health", timeout=10)
    
    # Test 2: Dependencies check
    results['dependencies'] = test_endpoint(base_url, "/test-dependencies", timeout=30)
    
    # Test 3: Chrome functionality
    results['chrome'] = test_endpoint(base_url, "/test-chrome", timeout=60)
    
    # Test 4: Google Maps test (may take longer)
    results['google_maps'] = test_endpoint(base_url, "/test-google-maps", timeout=120)
    
    # Test 5: Full scraping (only if other tests pass)
    if all(results.values()):
        print("\n🎯 All basic tests passed! Testing full scraping...")
        scrape_data = {
            "query": "coffee shops in San Francisco",
            "max_results": 3,
            "visit_websites": False
        }
        results['scraping'] = test_endpoint(base_url, "/scrape", "POST", scrape_data, timeout=180)
    else:
        print("\n⚠️ Skipping scraping test due to failed basic tests")
        results['scraping'] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEPLOYMENT VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test.upper():15} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 DEPLOYMENT SUCCESSFUL! All systems operational.")
        return True
    else:
        print("⚠️ DEPLOYMENT ISSUES DETECTED. Check failed tests above.")
        return False

if __name__ == "__main__":
    # Replace with your Railway app URL
    BASE_URL = "https://google-map-scraper-production-702a.up.railway.app"
    
    print("🔍 Starting deployment verification...")
    print("This may take a few minutes...")
    
    success = verify_deployment(BASE_URL)
    
    if success:
        print("\n✅ Ready to use! Your Google Maps scraper is fully operational.")
    else:
        print("\n❌ Deployment needs attention. Check the logs above.")
    
    print("\n📚 Next steps:")
    print("- Use the /scrape endpoint for production scraping")
    print("- Monitor Railway logs for any issues")
    print("- Check DEPLOYMENT.md for troubleshooting tips")
