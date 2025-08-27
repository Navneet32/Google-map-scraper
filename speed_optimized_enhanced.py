#!/usr/bin/env python3
"""
Speed-Optimized Enhanced Scraper - Uses the 11-lead logic but in 30-60 seconds
Based on enhanced_google_maps_scraper.py but with speed optimizations:
- Reduced delays from 1-3s to 0.1-0.3s
- Limited scrolling from 100 to 60 attempts
- Reduced patience from 15 to 8 attempts
- Faster browser setup
- Quick data extraction
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
from webdriver_manager.chrome import ChromeDriverManager


class SpeedOptimizedEnhancedScraper:
    def __init__(self, search_query, max_results=30, visit_websites=False):
        self.search_query = search_query
        self.max_results = max_results
        self.visit_websites = visit_websites
        self.extracted_count = 0
        self.contacts_found = 0
        
        # Enhanced email and phone patterns (same as working version)
        self.email_patterns = [
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            re.compile(r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'),
            re.compile(r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', re.IGNORECASE),
        ]
        
        self.phone_patterns = [
            re.compile(r'\+?1?[-.]\s?\(?([0-9]{3})\)?[-.]\s?([0-9]{3})[-.]\s?([0-9]{4})'),
            re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            re.compile(r'\(\d{3}\)\s?\d{3}[-.]?\d{4}'),
            re.compile(r'tel[:\s]*(\+?1?[-.]\s?\(?[0-9]{3}\)?[-.]\s?[0-9]{3}[-.]\s?[0-9]{4})', re.IGNORECASE),
            re.compile(r'\+?\d{1,3}[-.]\s?\(?\d{3}\)?[-.]\s?\d{3}[-.]\s?\d{4}'),
            re.compile(r'\d{10}'),
            re.compile(r'\+\d{1,3}\s?\d{3,4}\s?\d{3}\s?\d{4}'),
            re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'),
        ]
        
        self.setup_browser()
    
    def setup_browser(self):
        """Speed-optimized browser setup"""
        print("⚡ Setting up speed-optimized enhanced browser...")

        self.chrome_options = Options()
        
        # Speed-optimized options (same as enhanced but faster)
        browser_options = [
            "--headless=new",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",  # Critical for speed
            "--disable-javascript-harmony-shipping",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-ipc-flooding-protection",
            "--window-size=1920,1080",
            "--lang=en-US",
            "--accept-lang=en-US,en",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        for option in browser_options:
            self.chrome_options.add_argument(option)

        # Speed-optimized preferences
        self.chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'en-US,en',
            'intl.charset_default': 'UTF-8',
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'profile.managed_default_content_settings.images': 2  # Block images
        })

        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 15)  # Reduced timeout
            print("✅ Speed-optimized browser setup completed")
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            raise

    def search_google_maps(self):
        """Speed-optimized Google Maps search"""
        try:
            print(f"⚡ Speed search for: {self.search_query}")

            # Same URL strategy as working version
            search_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '+')}"
            print(f"🌐 Navigating to: {search_url}")

            self.driver.get(search_url)
            time.sleep(5)  # Reduced from 10s

            # Handle consent (same logic, faster)
            self._handle_consent_and_cookies()

            # Wait for results (same logic, faster)
            self._wait_for_search_results()

            print("✅ Speed search completed")
            return True

        except Exception as e:
            print(f"❌ Speed search failed: {e}")
            return False

    def _handle_consent_and_cookies(self):
        """Speed-optimized consent handling (same selectors as working version)"""
        try:
            print("⚡ Speed consent handling...")
            
            # Same consent selectors as working version
            consent_selectors = [
                "//button[contains(text(), 'Accept all')]",
                "//button[contains(text(), 'I agree')]",
                "//button[contains(text(), 'Accept')]",
                "//button[contains(text(), 'Alles accepteren')]",
                "//button[contains(text(), 'Accepteren')]",
                "//button[contains(text(), 'Tout accepter')]",
                "//button[contains(text(), 'Aceptar todo')]",
                "//div[contains(@class, 'VfPpkd-LgbsSe')]//parent::button",
                "//button[contains(@class, 'VfPpkd-LgbsSe')]",
                "//form//button[@type='submit']",
                "//button[not(@disabled)]"
            ]

            for selector in consent_selectors:
                try:
                    button = WebDriverWait(self.driver, 2).until(  # Reduced from 3s
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button.click()
                    print("✅ Consent handled")
                    time.sleep(1)  # Reduced from 3s
                    break
                except:
                    continue

        except Exception as e:
            print(f"⚠️ Consent handling: {e}")

    def _wait_for_search_results(self):
        """Speed-optimized waiting (same selectors as working version)"""
        print("⚡ Speed waiting for search results...")
        
        # Same result selectors as working version
        result_selectors = [
            "//div[contains(@class, 'Nv2PK')]",
            "//div[@role='article']",
            "//a[contains(@href, '/maps/place/')]",
            "//div[contains(@class, 'bfdHYd')]",
            "//div[contains(@class, 'lI9IFe')]",
            "//div[contains(@jsaction, 'mouseover')]",
            "//div[contains(@class, 'THOPZb')]",
            "//div[contains(@class, 'VkpGBb')]"
        ]

        max_wait = 20  # Reduced from 30
        wait_count = 0
        
        while wait_count < max_wait:
            for selector in result_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements and len(elements) > 0:
                        print(f"✅ Found {len(elements)} results")
                        return True
                except:
                    continue
            
            time.sleep(0.5)  # Reduced from 1s
            wait_count += 1
            
        print("⚠️ No clear results found, but continuing...")
        return True

    def get_business_links(self):
        """Speed-optimized business link extraction (same logic as working version but faster)"""
        try:
            print("⚡ Speed business link extraction...")
            all_links = set()
            scroll_attempts = 0
            max_scrolls = 60  # Reduced from 100 for speed
            no_new_content_count = 0
            max_patience = 8  # Reduced from 15 for speed

            # Same comprehensive link selectors as working version
            link_selectors = [
                '//a[contains(@href, "/maps/place/")]',
                '//div[@role="article"]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "Nv2PK")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "bfdHYd")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "lI9IFe")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@jsaction, "mouseover")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "THOPZb")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "VkpGBb")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "UaQhfb")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "section-result")]//a[contains(@href, "/maps/place/")]'
            ]

            while scroll_attempts < max_scrolls and len(all_links) < self.max_results:
                print(f"⚡ Speed scroll {scroll_attempts + 1}/{max_scrolls}")

                # Extract links (same logic as working version)
                new_links_count = 0
                for selector in link_selectors:
                    try:
                        link_elements = self.driver.find_elements(By.XPATH, selector)
                        for element in link_elements:
                            try:
                                href = element.get_attribute('href')
                                if href and '/maps/place/' in href and href not in all_links:
                                    all_links.add(href)
                                    new_links_count += 1
                            except:
                                continue
                    except:
                        continue

                current_count = len(all_links)
                progress = (current_count / self.max_results) * 100 if self.max_results > 0 else 0
                print(f"📊 Found {current_count} links (+{new_links_count} new) - {progress:.1f}% of target")

                # Early exit if target reached
                if current_count >= self.max_results:
                    print(f"🎯 Target reached: {current_count} links")
                    break

                # Speed-optimized patience logic
                if new_links_count == 0:
                    no_new_content_count += 1
                    # Try recovery strategies (same as working version but faster)
                    if no_new_content_count == 3:
                        print("⚡ Speed recovery: Alternative scroll...")
                        self._speed_alternative_scroll()
                    elif no_new_content_count == 6:
                        print("⚡ Speed recovery: Page refresh...")
                        self._speed_page_refresh()
                    
                    if no_new_content_count >= max_patience:
                        print(f"⏹️ No new content after {max_patience} attempts")
                        break
                else:
                    no_new_content_count = 0

                # Speed-optimized scrolling
                self._speed_enhanced_scroll()
                
                # Minimal delay for speed
                delay = 0.2 if new_links_count > 0 else 0.5  # Much faster than original
                time.sleep(delay)
                
                scroll_attempts += 1

            business_links = list(all_links)[:self.max_results]
            print(f"✅ Speed extraction complete: {len(business_links)} links")

            return business_links

        except Exception as e:
            print(f"❌ Speed link extraction failed: {e}")
            return []

    def _speed_enhanced_scroll(self):
        """Speed-optimized scrolling (same methods as working version but faster)"""
        try:
            # Same scrollable selectors as working version
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
                    # Faster scrolling - 2 actions instead of 3
                    for _ in range(2):
                        self.driver.execute_script("arguments[0].scrollTop += 800", panel)
                        time.sleep(0.1)  # Much faster
                    scrolled = True
                    break
                except:
                    continue

            # Fallback scrolling (same as working version but faster)
            if not scrolled:
                self.driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(0.1)
                self.driver.execute_script("document.body.scrollTop += 1000")

            # Keyboard scrolling (same as working version but faster)
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
            except:
                pass

        except Exception as e:
            print(f"⚠️ Speed scroll error: {e}")

    def _speed_alternative_scroll(self):
        """Speed-optimized alternative scrolling"""
        try:
            # Same show more selectors as working version
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
                    time.sleep(1)  # Reduced from 3s
                    return
                except:
                    continue
            
            # Keyboard navigation (faster)
            body = self.driver.find_element(By.TAG_NAME, "body")
            for _ in range(5):  # Reduced from 10
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)  # Much faster
            
        except Exception as e:
            print(f"⚠️ Speed alternative scroll failed: {e}")

    def _speed_page_refresh(self):
        """Speed-optimized page refresh"""
        try:
            print("⚡ Speed page refresh...")
            self.driver.refresh()
            time.sleep(3)  # Reduced from 5s
            
            # Faster immediate scrolling
            for _ in range(10):  # Reduced from 20
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(0.1)  # Much faster
            
        except Exception as e:
            print(f"⚠️ Speed page refresh failed: {e}")

    def extract_business_data(self, business_url):
        """Speed-optimized business data extraction (same extraction logic but faster)"""
        try:
            print(f"⚡ Speed extraction: {business_url[:60]}...")
            self.driver.get(business_url)
            time.sleep(2)  # Reduced from 4-7s

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

            # Same extraction methods as working version
            data['name'] = self._extract_business_name()
            data['address'] = self._extract_address()
            data['rating'], data['review_count'] = self._extract_rating_and_reviews()
            data['category'] = self._extract_category()
            data['website'] = self._extract_website()
            data['mobile'] = self._extract_phone_enhanced()

            self.extracted_count += 1

            # Same summary as working version
            summary = f"✅ {data['name']}"
            if data['rating']:
                summary += f" ({data['rating']}⭐)"
            if data['mobile']:
                summary += f" 📞{data['mobile']}"
            if data['website']:
                summary += f" 🌐"

            print(summary)
            return data

        except Exception as e:
            print(f"❌ Speed extraction failed: {e}")
            return None

    def _extract_business_name(self):
        """Same name extraction as working version"""
        name_selectors = [
            'h1[data-attrid="title"]',
            'h1.DUwDvf',
            'h1.x3AX1-LfntMc-header-title-title',
            'h1.fontHeadlineLarge',
            'h1',
            '.x3AX1-LfntMc-header-title-title',
            '.DUwDvf',
            '.fontHeadlineLarge',
            '[data-attrid="title"]'
        ]

        for selector in name_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                name = element.text.strip()
                if name and len(name) > 1:
                    return name
            except:
                continue
        return 'Unknown Business'

    def _extract_address(self):
        """Same address extraction as working version"""
        address_selectors = [
            '[data-item-id="address"]',
            '.Io6YTe.fontBodyMedium.kR99db.fdkmkc',
            '.rogA2c .Io6YTe',
            'button[data-item-id="address"]',
            '.fccl3c .Io6YTe',
            '[data-item-id*="address"]',
            '.fontBodyMedium[data-item-id*="address"]'
        ]

        for selector in address_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                address = element.text.strip()
                if address and len(address) > 5:
                    return address
            except:
                continue
        return 'Address not found'

    def _extract_rating_and_reviews(self):
        """Same rating extraction as working version"""
        rating = None
        review_count = None

        rating_selectors = [
            '.F7nice span[aria-hidden="true"]',
            '.ceNzKf[aria-label*="stars"]',
            'span.ceNzKf',
            '.MW4etd',
            '.fontDisplayLarge'
        ]

        for selector in rating_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                match = re.search(r'(\d+\.?\d*)', text)
                if match:
                    rating = float(match.group(1))
                    break
            except:
                continue

        review_selectors = [
            '.F7nice span:nth-child(2)',
            'button[aria-label*="reviews"]',
            '.UY7F9',
            '.fontBodyMedium[aria-label*="reviews"]'
        ]

        for selector in review_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                match = re.search(r'[\(]?(\d+(?:,\d+)*)[\)]?', text)
                if match:
                    review_count = int(match.group(1).replace(',', ''))
                    break
            except:
                continue

        return rating, review_count

    def _extract_category(self):
        """Same category extraction as working version"""
        category_selectors = [
            '.DkEaL',
            'button[jsaction*="category"]',
            '.YhemCb',
            '.fontBodyMedium[data-value*="category"]'
        ]

        for selector in category_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                category = element.text.strip()
                if category and len(category) > 2:
                    return category
            except:
                continue
        return 'Category not found'

    def _extract_website(self):
        """Same website extraction as working version"""
        website_selectors = [
            'a[data-item-id="authority"]',
            'a[href*="http"]:not([href*="google.com"]):not([href*="maps"])',
            '.CsEnBe a[href*="http"]',
            'a[data-item-id*="website"]'
        ]

        for selector in website_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                url = element.get_attribute('href')
                if url and 'google.com' not in url and 'maps' not in url:
                    return url
            except:
                continue
        return None

    def _extract_phone_enhanced(self):
        """Same phone extraction as working version"""
        try:
            phone_selectors = [
                "//button[@data-item-id='phone:tel:']",
                "//button[contains(@data-item-id,'phone')]",
                "//div[@data-item-id='phone:tel:']",
                "//div[contains(@data-item-id,'phone')]//div[contains(@class,'Io6YTe')]",
                "//a[starts-with(@href,'tel:')]",
                "//button[contains(@aria-label,'Phone')]",
                "//button[contains(@aria-label,'Call')]"
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
            print(f"❌ Phone extraction error: {e}")
            return None

    def _extract_phone_from_element(self, element):
        """Same phone extraction logic as working version"""
        try:
            text_sources = [
                element.get_attribute('aria-label') or '',
                element.get_attribute('href') or '',
                element.get_attribute('data-item-id') or '',
                element.text or ''
            ]
            
            for text in text_sources:
                if not text:
                    continue
                    
                text = text.replace('tel:', '').replace('Phone: ', '').replace('Call ', '')
                
                for pattern in self.phone_patterns:
                    match = pattern.search(text)
                    if match:
                        phone = match.group(0) if not isinstance(match.group(0), tuple) else ''.join(match.group(0))
                        digits = re.sub(r'\D', '', phone)
                        if len(digits) >= 10:
                            return phone
            
            return None
            
        except:
            return None

    def run_extraction(self):
        """Speed-optimized main extraction process"""
        start_time = datetime.now()
        results = []

        try:
            print(f"⚡ SPEED-OPTIMIZED ENHANCED EXTRACTION")
            print(f"🔍 Query: '{self.search_query}'")
            print(f"🎯 Target: {self.max_results} businesses in 30-60 seconds")
            print(f"⏰ Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 70)

            # Speed-optimized search
            if not self.search_google_maps():
                print("❌ Speed search failed")
                return []

            # Speed-optimized link extraction
            business_links = self.get_business_links()
            if not business_links:
                print("❌ No business links found")
                return []

            print(f"✅ Found {len(business_links)} business links")

            # Speed-optimized data extraction
            print(f"\n⚡ SPEED DATA EXTRACTION")
            print("=" * 70)

            successful = 0
            failed = 0

            for i, link in enumerate(business_links, 1):
                print(f"\n[{i:2d}/{len(business_links)}] Processing...")

                try:
                    business_data = self.extract_business_data(link)
                    if business_data and business_data.get('name') != 'Unknown Business':
                        results.append(business_data)
                        successful += 1
                        
                        if business_data.get('email') or business_data.get('mobile'):
                            self.contacts_found += 1
                    else:
                        failed += 1

                except Exception as e:
                    failed += 1
                    print(f"❌ Error: {e}")

                # Speed-optimized delay
                delay = random.uniform(0.3, 0.8)  # Much faster than original
                time.sleep(delay)

            # Final summary
            end_time = datetime.now()
            duration = end_time - start_time
            total_seconds = duration.total_seconds()

            print(f"\n" + "=" * 70)
            print(f"⚡ SPEED-OPTIMIZED EXTRACTION COMPLETED!")
            print(f"⏱️ Duration: {duration}")
            print(f"📊 Links processed: {len(business_links)}")
            print(f"✅ Successful: {successful}")
            print(f"❌ Failed: {failed}")
            print(f"📞 Contacts found: {self.contacts_found}")
            print(f"📋 Final results: {len(results)} businesses")
            print(f"📈 Success rate: {(successful/len(business_links)*100):.1f}%")
            
            # Speed check
            if total_seconds <= 60:
                print(f"🎉 SPEED SUCCESS! Completed in {total_seconds:.1f}s (target: 30-60s)")
            else:
                print(f"⚠️ Took {total_seconds:.1f}s (target: 30-60s)")

            return results

        except Exception as e:
            print(f"❌ Critical error: {e}")
            return []
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            print("🧹 Speed cleanup completed")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")


def speed_optimized_enhanced_scrape(query, max_results=30, visit_websites=False):
    """Speed-optimized enhanced scraping function"""
    scraper = SpeedOptimizedEnhancedScraper(
        search_query=query,
        max_results=max_results,
        visit_websites=visit_websites
    )
    return scraper.run_extraction()


if __name__ == "__main__":
    # Test with same query that got 11 results
    start_test = time.time()
    results = speed_optimized_enhanced_scrape("restaurants in New York", max_results=25)
    test_duration = time.time() - start_test
    
    print(f"\n⚡ SPEED TEST RESULTS")
    print(f"📊 Found: {len(results)} businesses")
    print(f"⏱️ Time: {test_duration:.1f} seconds")
    print(f"🎯 Target met: {'✅' if test_duration <= 60 and len(results) >= 10 else '❌'}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"speed_enhanced_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    
    # Show sample results
    for i, result in enumerate(results[:10], 1):
        phone = f" 📞 {result['mobile']}" if result.get('mobile') else ""
        rating = f" ({result['rating']}⭐)" if result.get('rating') else ""
        print(f"{i}. {result['name']}{rating}{phone}")
