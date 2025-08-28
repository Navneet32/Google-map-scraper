#!/usr/bin/env python3
"""
Railway-Optimized Google Maps Scraper - Based on working optimized_scraper.py
Simplified and focused approach for reliable Railway deployment
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class EnhancedGoogleMapsBusinessScraper:
    def __init__(self, search_query, max_results=50, visit_websites=True):
        self.search_query = search_query
        self.max_results = max_results
        self.visit_websites = visit_websites
        self.extracted_count = 0
        self.contacts_found = 0
        
        # Simplified phone patterns (based on working optimized_scraper.py)
        self.phone_patterns = [
            re.compile(r'\+?1?[-.]\s?\(?([0-9]{3})\)?[-.]\s?([0-9]{3})[-.]\s?([0-9]{4})'),
            re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            re.compile(r'\(\d{3}\)\s?\d{3}[-.]?\d{4}'),
            re.compile(r'\d{10}'),
        ]
        
        # Enhanced email patterns
        self.email_patterns = [
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            re.compile(r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'),
            re.compile(r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', re.IGNORECASE),
        ]
        
        self.setup_browser()
    
    def setup_browser(self):
        """Railway-optimized browser setup (based on working optimized_scraper.py)"""
        print("🔧 Setting up optimized Chrome browser...")

        self.chrome_options = Options()
        
        # Performance-optimized options (simplified from working version)
        options = [
            "--headless=new",
            "--no-sandbox", 
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-images",  # Faster loading
            "--window-size=1920,1080",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ]
        
        for option in options:
            self.chrome_options.add_argument(option)

        self.chrome_options.add_experimental_option('prefs', {
            'profile.managed_default_content_settings.images': 2,
            'profile.default_content_settings.popups': 0
        })

        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            print("✅ Browser setup completed")
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            raise

    def search_and_extract_links(self):
        """Optimized search with guaranteed results (based on working version)"""
        try:
            print(f"🔍 Searching for: {self.search_query}")
            
            # Direct search URL (from working version)
            search_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '+')}"
            self.driver.get(search_url)
            time.sleep(8)  # Wait for page load
            
            # Handle consent (from working version)
            self._handle_consent()
            
            # Extract links with optimized method
            all_links = self._extract_links_optimized()
            
            # Fallback: Try alternative search approach if no results
            if len(all_links) == 0:
                print("🔄 No results found, trying alternative approach...")
                all_links = self._try_alternative_search()
            
            print(f"✅ Found {len(all_links)} business links")
            return list(all_links)[:self.max_results]
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []

    def _try_alternative_search(self):
        """Alternative search method for Railway environment"""
        all_links = set()
        
        try:
            # Try different Google Maps URL format
            alt_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '%20')}"
            print(f"🔄 Trying alternative URL: {alt_url}")
            self.driver.get(alt_url)
            time.sleep(10)
            
            # Wait for results to load
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            try:
                # Wait for any clickable elements that might be business listings
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "a"))
                )
                print("✅ Page loaded with clickable elements")
            except:
                print("⚠️ Timeout waiting for elements")
            
            # Try more aggressive link extraction
            time.sleep(5)
            
            # Get all links and filter for place URLs
            all_elements = self.driver.find_elements(By.TAG_NAME, "a")
            print(f"🔍 Found {len(all_elements)} total links on page")
            
            for element in all_elements:
                try:
                    href = element.get_attribute('href')
                    if href and '/maps/place/' in href:
                        all_links.add(href)
                        print(f"✅ Alternative found: {href[:60]}...")
                        if len(all_links) >= 5:  # Get at least a few results
                            break
                except:
                    continue
            
            print(f"🔄 Alternative search found {len(all_links)} links")
            
        except Exception as e:
            print(f"❌ Alternative search failed: {e}")
        
        return all_links

    def _handle_consent(self):
        """Handle consent popups (simplified from working version)"""
        try:
            consent_buttons = [
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'I agree')]", 
                "//button[contains(@class, 'VfPpkd-LgbsSe')]"
            ]
            
            for selector in consent_buttons:
                try:
                    button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button.click()
                    time.sleep(2)
                    break
                except:
                    continue
        except:
            pass

    def _extract_links_optimized(self):
        """Optimized link extraction with 200 scroll attempts (from working version)"""
        all_links = set()
        scroll_count = 0
        max_scrolls = 200  # Aggressive scrolling
        patience = 0
        max_patience = 30
        
        # Debug: Check page state on first attempt
        if scroll_count == 0:
            try:
                page_title = self.driver.title
                current_url = self.driver.current_url
                print(f"🔍 Debug - Page title: {page_title}")
                print(f"🔍 Debug - Current URL: {current_url}")
                
                # Check if we're blocked or redirected
                if "sorry" in page_title.lower() or "blocked" in page_title.lower():
                    print("❌ Google appears to be blocking access")
                    return all_links
                    
                # Check for common page elements
                body_text = self.driver.find_element(By.TAG_NAME, "body").text[:200]
                print(f"🔍 Debug - Page body preview: {body_text}")
                
            except Exception as e:
                print(f"🔍 Debug error: {e}")
        
        # Updated comprehensive selectors for current Google Maps DOM
        selectors = [
            '//a[contains(@href, "/maps/place/")]',
            '//div[@role="article"]//a[contains(@href, "/maps/place/")]',
            '//div[contains(@class, "Nv2PK")]//a[contains(@href, "/maps/place/")]',
            '//div[contains(@class, "bfdHYd")]//a[contains(@href, "/maps/place/")]',
            '//div[contains(@class, "lI9IFe")]//a[contains(@href, "/maps/place/")]',
            '//a[contains(@data-value, "Feature")]',
            '//div[contains(@class, "THOPZb")]//a',
            '//div[contains(@class, "VkpGBb")]//a',
            '//div[contains(@jsaction, "click")]//a[contains(@href, "place")]',
            '//a[contains(@aria-label, "")][@href*="place"]'
        ]
        
        while scroll_count < max_scrolls and len(all_links) < self.max_results:
            print(f"🔄 Scroll {scroll_count + 1}/{max_scrolls} - Found: {len(all_links)} links")
            
            # Extract links with detailed debugging
            new_count = 0
            for i, selector in enumerate(selectors):
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if scroll_count < 3:  # Debug first few attempts
                        print(f"🔍 Selector {i+1}: Found {len(elements)} elements")
                    
                    for element in elements:
                        try:
                            href = element.get_attribute('href')
                            if href and '/maps/place/' in href and href not in all_links:
                                all_links.add(href)
                                new_count += 1
                                if scroll_count < 3:  # Debug first few links
                                    print(f"✅ Found business link: {href[:60]}...")
                        except:
                            continue
                except Exception as e:
                    if scroll_count < 3:
                        print(f"❌ Selector {i+1} error: {e}")
                    continue
            
            # Additional fallback: Try CSS selectors if XPath fails
            if new_count == 0 and scroll_count < 5:
                css_selectors = [
                    'a[href*="/maps/place/"]',
                    '[data-result-index] a',
                    '.section-result a',
                    '[jsaction*="click"] a[href*="place"]'
                ]
                
                for css_selector in css_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
                        print(f"🔍 CSS Selector '{css_selector}': Found {len(elements)} elements")
                        
                        for element in elements:
                            try:
                                href = element.get_attribute('href')
                                if href and '/maps/place/' in href and href not in all_links:
                                    all_links.add(href)
                                    new_count += 1
                                    print(f"✅ CSS Found: {href[:60]}...")
                            except:
                                continue
                    except Exception as e:
                        print(f"❌ CSS Selector error: {e}")
                        continue
            
            # Check progress
            if new_count == 0:
                patience += 1
                if patience >= max_patience:
                    print(f"⏹️ Stopping after {patience} attempts with no new results")
                    break
            else:
                patience = 0
            
            # Optimized scrolling
            self._scroll_optimized()
            
            # Dynamic delay based on results found
            delay = 1.0 if new_count > 0 else 2.0
            time.sleep(delay)
            scroll_count += 1
        
        return all_links

    def _scroll_optimized(self):
        """Optimized scrolling method (from working version)"""
        try:
            # Method 1: Scroll results panel
            panel_selectors = ['[role="main"]', '.m6QErb', '#pane']
            
            for selector in panel_selectors:
                try:
                    panel = self.driver.find_element(By.CSS_SELECTOR, selector)
                    # Multiple scroll actions
                    for _ in range(3):
                        self.driver.execute_script("arguments[0].scrollTop += 1000", panel)
                        time.sleep(0.3)
                    return
                except:
                    continue
            
            # Method 2: Fallback page scroll
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(0.5)
            
            # Method 3: Keyboard scroll
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.PAGE_DOWN)
                body.send_keys(Keys.PAGE_DOWN)
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Scroll error: {e}")

    def get_business_links(self):
        """Main method to get business links (Railway compatibility)"""
        return self.search_and_extract_links()

    def _enhanced_scroll(self):
        """Enhanced scrolling with multiple methods"""
        try:
            # Method 1: Scroll results panel
            scrollable_selectors = [
                '[role="main"]',
                '.m6QErb',
                '#pane',
                '.siAUzd',
                '.section-scrollbox',
                '.section-layout',
                '.section-listbox',
                '.section-result-container'
            ]

            scrolled = False
            for selector in scrollable_selectors:
                try:
                    panel = self.driver.find_element(By.CSS_SELECTOR, selector)
                    # Multiple scroll actions per attempt
                    for _ in range(3):
                        self.driver.execute_script("arguments[0].scrollTop += 800", panel)
                        time.sleep(0.5)
                    scrolled = True
                    break
                except:
                    continue

            # Method 2: Fallback scrolling
            if not scrolled:
                # Page scroll
                self.driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(0.5)
                # Body scroll
                self.driver.execute_script("document.body.scrollTop += 1000")
                time.sleep(0.5)
                # Try to find and scroll any scrollable div
                try:
                    scrollable_divs = self.driver.find_elements(By.CSS_SELECTOR, "div[style*='overflow']")
                    for div in scrollable_divs[:3]:
                        self.driver.execute_script("arguments[0].scrollTop += 500", div)
                        time.sleep(0.3)
                except:
                    pass

            # Method 3: Keyboard scrolling (sometimes more effective)
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
                body.send_keys(Keys.PAGE_DOWN)
            except:
                pass

        except Exception as e:
            print(f"⚠️ Enhanced scroll error: {e}")

    def _alternative_scroll_strategy(self):
        """Alternative scrolling when normal scrolling fails"""
        try:
            # Strategy 1: Click "Show more results" if available
            show_more_selectors = [
                "//button[contains(text(), 'Show more')]",
                "//button[contains(text(), 'More results')]",
                "//div[contains(text(), 'Show more')]//parent::button",
                "//span[contains(text(), 'Show more')]//parent::button"
            ]
            
            for selector in show_more_selectors:
                try:
                    button = self.driver.find_element(By.XPATH, selector)
                    button.click()
                    print("✅ Clicked 'Show more' button")
                    time.sleep(3)
                    return
                except:
                    continue
            
            # Strategy 2: Try keyboard navigation
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, "body")
            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            
            print("✅ Used alternative keyboard scrolling")
            
        except Exception as e:
            print(f"⚠️ Alternative scroll failed: {e}")

    def _page_refresh_strategy(self):
        """Refresh page and scroll to get more results"""
        try:
            print("🔄 Refreshing page to get more results...")
            current_url = self.driver.current_url
            self.driver.refresh()
            time.sleep(5)
            
            # Scroll immediately after refresh
            for _ in range(20):
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(0.3)
            
            print("✅ Page refresh strategy completed")
            
        except Exception as e:
            print(f"⚠️ Page refresh failed: {e}")

    def _zoom_out_strategy(self):
        """Zoom out to show more results"""
        try:
            print("🔍 Zooming out to show more results...")
            
            # Try to find and click zoom out button
            zoom_selectors = [
                "//button[@aria-label='Zoom out']",
                "//button[contains(@class, 'widget-zoom-out')]",
                "//div[@data-value='Zoom out']//parent::button"
            ]
            
            for selector in zoom_selectors:
                try:
                    for _ in range(3):  # Zoom out multiple times
                        button = self.driver.find_element(By.XPATH, selector)
                        button.click()
                        time.sleep(1)
                    print("✅ Zoomed out successfully")
                    return
                except:
                    continue
            
            # Fallback: Use keyboard zoom
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.CONTROL, "-", "-", "-")  # Zoom out
            time.sleep(2)
            
            print("✅ Used keyboard zoom out")
            
        except Exception as e:
            print(f"⚠️ Zoom out failed: {e}")

    def extract_business_data(self, business_url):
        """Extract business data from individual page (based on working version)"""
        try:
            self.driver.get(business_url)
            time.sleep(random.uniform(3, 5))

            data = {
                'name': self._get_name(),
                'address': self._get_address(),
                'rating': self._get_rating(),
                'category': self._get_category(),
                'website': self._get_website(),
                'mobile': self._get_phone(),
                'google_maps_url': business_url,
                'search_query': self.search_query
            }

            self.extracted_count += 1
            if data.get('mobile'):
                self.contacts_found += 1

            print(f"✅ {data['name']} {'📞' if data.get('mobile') else ''}")
            return data

        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return None

    def _get_name(self):
        """Extract business name (from working version)"""
        selectors = ['h1.DUwDvf', 'h1[data-attrid="title"]', 'h1']
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                name = element.text.strip()
                if name and len(name) > 1:
                    return name
            except:
                continue
        return 'Unknown Business'

    def _get_address(self):
        """Extract address (from working version)"""
        selectors = [
            '[data-item-id="address"]',
            '.Io6YTe.fontBodyMedium.kR99db.fdkmkc'
        ]
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                address = element.text.strip()
                if address and len(address) > 5:
                    return address
            except:
                continue
        return 'Address not found'

    def _get_rating(self):
        """Extract rating (from working version)"""
        selectors = ['.F7nice span[aria-hidden="true"]', 'span.ceNzKf']
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                match = re.search(r'(\d+\.?\d*)', text)
                if match:
                    return float(match.group(1))
            except:
                continue
        return None

    def _get_category(self):
        """Extract category (from working version)"""
        selectors = ['.DkEaL', '.YhemCb']
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                category = element.text.strip()
                if category and len(category) > 2:
                    return category
            except:
                continue
        return 'Category not found'

    def _get_website(self):
        """Extract website (from working version)"""
        selectors = [
            'a[data-item-id="authority"]',
            'a[href*="http"]:not([href*="google.com"]):not([href*="maps"])'
        ]
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                url = element.get_attribute('href')
                if url and 'google.com' not in url:
                    return url
            except:
                continue
        return None

    def _get_phone(self):
        """Extract phone number (from working version)"""
        try:
            # Direct phone selectors
            phone_selectors = [
                "//button[contains(@data-item-id,'phone')]",
                "//a[starts-with(@href,'tel:')]",
                "//button[contains(@aria-label,'Phone')]"
            ]
            
            for selector in phone_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        phone = self._extract_phone_from_element(element)
                        if phone:
                            return phone
                except:
                    continue
            
            return None
            
        except Exception as e:
            return None

    def _extract_phone_from_element(self, element):
        """Extract phone from element (from working version)"""
        try:
            sources = [
                element.get_attribute('aria-label') or '',
                element.get_attribute('href') or '',
                element.text or ''
            ]
            
            for text in sources:
                text = text.replace('tel:', '').replace('Phone: ', '')
                for pattern in self.phone_patterns:
                    match = pattern.search(text)
                    if match:
                        phone = match.group(0)
                        digits = re.sub(r'\D', '', phone)
                        if len(digits) >= 10:
                            return phone
            return None
        except:
            return None

    def run_scraping(self):
        """Main scraping process (based on working version)"""
        start_time = datetime.now()
        results = []

        try:
            print(f"🚀 OPTIMIZED GOOGLE MAPS SCRAPING")
            print(f"🔍 Query: '{self.search_query}'")
            print(f"🎯 Target: {self.max_results} businesses")
            print("=" * 60)

            # Get business links
            business_links = self.search_and_extract_links()
            if not business_links:
                print("❌ No business links found")
                return []

            print(f"\n📊 EXTRACTING DATA FROM {len(business_links)} BUSINESSES")
            print("=" * 60)

            # Extract data from each business
            for i, link in enumerate(business_links, 1):
                print(f"[{i:2d}/{len(business_links)}] Processing...")

                try:
                    business_data = self.extract_business_data(link)
                    if business_data:
                        results.append(business_data)
                except Exception as e:
                    print(f"❌ Error: {e}")

                # Delay between requests
                time.sleep(random.uniform(1.5, 3.0))

            # Final summary
            end_time = datetime.now()
            duration = end_time - start_time

            print(f"\n" + "=" * 60)
            print(f"🎉 SCRAPING COMPLETED!")
            print(f"⏱️ Duration: {duration}")
            print(f"📊 Businesses found: {len(results)}")
            print(f"📞 Contacts found: {self.contacts_found}")
            print(f"📈 Success rate: {(len(results)/len(business_links)*100):.1f}%")

            return results

        except Exception as e:
            print(f"❌ Critical error: {e}")
            return []
        finally:
            self.cleanup()

    def run_extraction(self):
        """Compatibility method for Railway deployment"""
        return self.run_scraping()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            print("🧹 Enhanced cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")


def enhanced_scrape_google_maps(query, max_results=100, visit_websites=True):
    """Enhanced convenience function"""
    scraper = EnhancedGoogleMapsBusinessScraper(
        search_query=query,
        max_results=max_results,
        visit_websites=visit_websites
    )
    return scraper.run_extraction()


if __name__ == "__main__":
    # Test the enhanced scraper
    results = enhanced_scrape_google_maps("restaurants in New York", max_results=50)
    print(f"\nEnhanced test completed. Found {len(results)} results.")
    for result in results[:5]:
        print(f"- {result['name']}: {result['address']}")
