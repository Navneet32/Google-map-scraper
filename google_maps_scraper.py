#!/usr/bin/env python3
"""
Clean Google Maps Scraper - No external dependencies conflicts
"""

import re
import time
import random
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from lxml import html
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class GoogleMapsBusinessScraper:
    def __init__(self, search_query, max_results=20, visit_websites=False):
        self.search_query = search_query
        self.max_results = max_results
        self.visit_websites = visit_websites
        self.extracted_count = 0
        self.contacts_found = 0
        
        # Email and phone patterns
        self.email_patterns = [
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            re.compile(r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'),
            re.compile(r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', re.IGNORECASE),
        ]
        
        self.phone_patterns = [
            re.compile(r'\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'),
            re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            re.compile(r'\(\d{3}\)\s?\d{3}[-.]?\d{4}'),
            re.compile(r'tel[:\s]*(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})', re.IGNORECASE),
        ]
        
        self.setup_browser()
    
    def setup_browser(self):
        """Setup Chrome browser with optimized configuration"""
        try:
            self.chrome_options = Options()
            
            # Essential headless options for Railway/cloud deployment - WORKING CONFIG
            self.chrome_options.add_argument("--headless=new")  # Use new headless mode
            self.chrome_options.add_argument("--no-sandbox")
            self.chrome_options.add_argument("--disable-dev-shm-usage")  # Critical for Docker
            self.chrome_options.add_argument("--disable-software-rasterizer")
            self.chrome_options.add_argument("--disable-gpu")
            self.chrome_options.add_argument("--disable-web-security")
            self.chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            self.chrome_options.add_argument("--disable-extensions")
            self.chrome_options.add_argument("--disable-plugins")
            self.chrome_options.add_argument("--disable-images")
            self.chrome_options.add_argument("--disable-background-timer-throttling")
            self.chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            self.chrome_options.add_argument("--disable-renderer-backgrounding")
            self.chrome_options.add_argument("--disable-ipc-flooding-protection")
            self.chrome_options.add_argument("--single-process")  # Important for Railway
            self.chrome_options.add_argument("--remote-debugging-port=9222")
            self.chrome_options.add_argument("--window-size=1920,1080")

            # Remove user data directory entirely - let Chrome handle it (CRITICAL FIX)
            self.chrome_options.add_argument("--disable-background-networking")
            self.chrome_options.add_argument("--disable-client-side-phishing-detection")
            self.chrome_options.add_argument("--disable-component-update")
            self.chrome_options.add_argument("--disable-hang-monitor")
            self.chrome_options.add_argument("--disable-popup-blocking")
            self.chrome_options.add_argument("--disable-prompt-on-repost")
            self.chrome_options.add_argument("--disable-sync")
            self.chrome_options.add_argument("--disable-web-resources")
            self.chrome_options.add_argument("--metrics-recording-only")
            self.chrome_options.add_argument("--no-crash-upload")
            self.chrome_options.add_argument("--safebrowsing-disable-auto-update")
            self.chrome_options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")

            # Anti-detection measures
            self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.chrome_options.add_experimental_option('useAutomationExtension', False)

            # Memory optimization for Railway
            self.chrome_options.add_argument("--memory-pressure-off")
            self.chrome_options.add_argument("--max_old_space_size=4096")

            # Try system Chrome first (for Nixpacks), fallback to ChromeDriverManager
            try:
                # Try with system chromedriver (Railway Nixpacks)
                self.driver = webdriver.Chrome(options=self.chrome_options)
                print("✅ Using system Chrome/Chromedriver")
            except Exception as e1:
                try:
                    # Fallback to ChromeDriverManager
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
                    print("✅ Using ChromeDriverManager")
                except Exception as e2:
                    print(f"❌ Both Chrome methods failed:")
                    print(f"   System Chrome error: {e1}")
                    print(f"   ChromeDriverManager error: {e2}")
                    raise Exception(f"Failed to initialize Chrome: {e2}")

            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)

            print("✅ Browser setup completed successfully")

        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            raise

    def search_google_maps(self):
        """Search Google Maps for the given query"""
        try:
            print(f"🔍 Searching Google Maps for: {self.search_query}")
            
            # Navigate to Google Maps
            self.driver.get("https://www.google.com/maps")
            time.sleep(2)
            
            # Find and fill search box
            search_box = self.wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
            search_box.clear()
            search_box.send_keys(self.search_query)
            
            # Click search button
            search_button = self.driver.find_element(By.ID, "searchbox-searchbutton")
            search_button.click()
            
            # Wait for results to load
            time.sleep(3)
            print("✅ Search completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return False

    def get_business_links(self):
        """Extract business links from Google Maps results"""
        try:
            print("📋 Extracting business links...")
            all_links = set()
            scroll_attempts = 0
            max_scrolls = 10
            no_new_content_count = 0
            
            while scroll_attempts < max_scrolls and len(all_links) < self.max_results:
                # Get current links
                page_source = self.driver.page_source
                tree = html.fromstring(page_source)
                current_links = tree.xpath('//a[contains(@href, "/maps/place/")]/@href')
                
                # Clean and add new links
                new_links_count = 0
                for link in current_links:
                    if link.startswith('/'):
                        link = 'https://www.google.com' + link
                    if link not in all_links:
                        all_links.add(link)
                        new_links_count += 1
                
                print(f"Scroll {scroll_attempts + 1}: Found {len(all_links)} total links (+{new_links_count} new)")
                
                # Check if we found new content
                if new_links_count == 0:
                    no_new_content_count += 1
                    if no_new_content_count >= 3:
                        print("No new content found after 3 attempts")
                        break
                else:
                    no_new_content_count = 0
                
                # Scroll down to load more results
                try:
                    results_panel = self.driver.find_element(By.CSS_SELECTOR, '[role="main"]')
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
                    time.sleep(2)
                except:
                    # Fallback scroll method
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                
                scroll_attempts += 1
            
            business_links = list(all_links)[:self.max_results]
            print(f"✅ Found {len(business_links)} business links")
            return business_links
            
        except Exception as e:
            print(f"❌ Link extraction failed: {e}")
            return []

    def extract_business_data(self, business_url):
        """Extract data from a single business page"""
        try:
            print(f"📊 Extracting data from: {business_url}")
            self.driver.get(business_url)
            time.sleep(3)
            
            data = {
                'name': '',
                'address': '',
                'rating': None,
                'review_count': None,
                'category': '',
                'website': None,
                'mobile': None,
                'email': None,
                'secondary_email': None,
                'google_maps_url': business_url,
                'search_query': self.search_query,
                'website_visited': False,
                'additional_contacts': ''
            }
            
            # Extract business name
            try:
                name_element = self.driver.find_element(By.CSS_SELECTOR, 'h1[data-attrid="title"]')
                data['name'] = name_element.text.strip()
            except:
                try:
                    name_element = self.driver.find_element(By.CSS_SELECTOR, 'h1')
                    data['name'] = name_element.text.strip()
                except:
                    data['name'] = 'Unknown Business'
            
            # Extract address
            try:
                address_element = self.driver.find_element(By.CSS_SELECTOR, '[data-item-id="address"]')
                data['address'] = address_element.text.strip()
            except:
                data['address'] = 'Address not found'
            
            # Extract rating and review count
            try:
                rating_element = self.driver.find_element(By.CSS_SELECTOR, '[jsaction*="pane.rating"]')
                rating_text = rating_element.text
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    data['rating'] = float(rating_match.group(1))
                
                review_match = re.search(r'\((\d+(?:,\d+)*)\)', rating_text)
                if review_match:
                    data['review_count'] = int(review_match.group(1).replace(',', ''))
            except:
                pass
            
            # Extract category
            try:
                category_element = self.driver.find_element(By.CSS_SELECTOR, '[jsaction*="pane.rating.category"]')
                data['category'] = category_element.text.strip()
            except:
                data['category'] = 'Category not found'
            
            # Extract website
            try:
                website_element = self.driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]')
                data['website'] = website_element.get_attribute('href')
            except:
                pass
            
            # Extract phone number
            try:
                phone_element = self.driver.find_element(By.CSS_SELECTOR, '[data-item-id*="phone"]')
                phone_text = phone_element.text.strip()
                for pattern in self.phone_patterns:
                    match = pattern.search(phone_text)
                    if match:
                        data['mobile'] = match.group(0)
                        break
            except:
                pass
            
            self.extracted_count += 1
            print(f"✅ Extracted data for: {data['name']}")
            return data
            
        except Exception as e:
            print(f"❌ Data extraction failed: {e}")
            return None

    def run_extraction(self):
        """Main extraction process"""
        start_time = datetime.now()
        results = []
        
        try:
            print(f"🚀 STARTING GOOGLE MAPS EXTRACTION")
            print(f"🔍 Search Query: {self.search_query}")
            print(f"🎯 Target: {self.max_results} businesses")
            print(f"🌐 Website visits: {'Enabled' if self.visit_websites else 'Disabled'}")
            print(f"⏰ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # Step 1: Search Google Maps
            if not self.search_google_maps():
                print("❌ Failed to search Google Maps")
                return []
            
            # Step 2: Extract business links
            business_links = self.get_business_links()
            if not business_links:
                print("❌ No business links found")
                return []
            
            # Step 3: Extract data from each business
            print(f"\n📊 EXTRACTING DATA FROM {len(business_links)} BUSINESSES")
            print("=" * 60)
            
            for i, link in enumerate(business_links, 1):
                print(f"\n[{i}/{len(business_links)}] Processing business...")
                
                business_data = self.extract_business_data(link)
                if business_data:
                    results.append(business_data)
                    if business_data.get('email') or business_data.get('mobile'):
                        self.contacts_found += 1
                
                # Add delay between requests
                time.sleep(random.uniform(1, 3))
            
            # Final summary
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"\n🎉 EXTRACTION COMPLETED!")
            print(f"⏱️ Duration: {duration}")
            print(f"📊 Businesses processed: {self.extracted_count}")
            print(f"📞 Total contacts found: {self.contacts_found}")
            print(f"✅ Results: {len(results)} businesses")
            
            return results
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return []
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            print("🧹 Cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")


def scrape_google_maps(query, max_results=20, visit_websites=False):
    """Convenience function to scrape Google Maps"""
    scraper = GoogleMapsBusinessScraper(
        search_query=query,
        max_results=max_results,
        visit_websites=visit_websites
    )
    return scraper.run_extraction()


if __name__ == "__main__":
    # Test the scraper
    results = scrape_google_maps("coffee shops in San Francisco", max_results=3)
    print(f"\nTest completed. Found {len(results)} results.")
    for result in results:
        print(f"- {result['name']}: {result['address']}")
