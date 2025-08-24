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
        """Setup Chrome browser with progressive stability testing"""
        print("🔧 Starting progressive Chrome setup for Railway...")

        # Try multiple Chrome configurations in order of stability
        configs = [
            {
                "name": "Ultra-Minimal",
                "options": [
                    "--headless",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ]
            },
            {
                "name": "Basic-Stable",
                "options": [
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process"
                ]
            },
            {
                "name": "Railway-Optimized",
                "options": [
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process",
                    "--disable-extensions",
                    "--disable-plugins",
                    "--window-size=800,600",
                    "--lang=en-US",
                    "--accept-lang=en-US,en"
                ]
            }
        ]

        for config in configs:
            try:
                print(f"🧪 Trying {config['name']} configuration...")

                self.chrome_options = Options()
                for option in config['options']:
                    self.chrome_options.add_argument(option)

                # Add language preferences to avoid non-English consent pages
                self.chrome_options.add_experimental_option('prefs', {
                    'intl.accept_languages': 'en-US,en',
                    'intl.charset_default': 'UTF-8'
                })

                # Test Chrome creation
                print(f"   Creating Chrome driver...")
                self.driver = webdriver.Chrome(options=self.chrome_options)

                # Test basic functionality
                print(f"   Testing basic functionality...")
                self.driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")

                # Test if we can get the title
                title = self.driver.title
                print(f"   ✅ {config['name']} successful! Page title: '{title}'")

                self.wait = WebDriverWait(self.driver, 15)
                print(f"✅ Browser setup completed with {config['name']} configuration")
                return  # Success!

            except Exception as config_error:
                print(f"   ❌ {config['name']} failed: {config_error}")
                try:
                    if hasattr(self, 'driver'):
                        self.driver.quit()
                except:
                    pass
                continue

        # If all configs failed, raise error
        raise Exception("All Chrome configurations failed on Railway")




    def search_google_maps(self):
        """Search Google Maps for the given query with multiple fallback methods"""
        try:
            print(f"🔍 Searching Google Maps for: {self.search_query}")

            # Method 1: Direct search URL (primary method)
            search_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '+')}"
            print(f"🌐 Method 1: Navigating to: {search_url}")

            try:
                self.driver.get(search_url)
                time.sleep(8)  # Increased wait time for Railway

                # Check if we're on Google Maps
                current_url = self.driver.current_url
                page_title = self.driver.title

                print(f"📄 Page title: {page_title}")
                print(f"🌐 Current URL: {current_url[:100]}...")

                # Check for common blocking indicators
                if "sorry" in page_title.lower() or "blocked" in page_title.lower():
                    print("🚫 Method 1 blocked by Google, trying Method 2...")
                    raise Exception("Blocked by Google")

                if "maps" not in current_url.lower():
                    print("🔄 Method 1 redirected, trying Method 2...")
                    raise Exception("Redirected away from Maps")

            except Exception as method1_error:
                print(f"⚠️ Method 1 failed: {method1_error}")

                # Method 2: Go to Google Maps first, then search
                print("🔄 Method 2: Going to Google Maps homepage first...")
                try:
                    self.driver.get("https://www.google.com/maps")
                    time.sleep(5)

                    # Find and use search box
                    search_box_selectors = [
                        "#searchboxinput",
                        'input[placeholder*="Search"]',
                        'input[aria-label*="Search"]'
                    ]

                    search_box = None
                    for selector in search_box_selectors:
                        try:
                            search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                            break
                        except:
                            continue

                    if search_box:
                        search_box.clear()
                        search_box.send_keys(self.search_query)

                        # Find and click search button
                        search_button_selectors = [
                            "#searchbox-searchbutton",
                            'button[aria-label*="Search"]',
                            'button[data-value="Search"]'
                        ]

                        for selector in search_button_selectors:
                            try:
                                search_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                                search_button.click()
                                break
                            except:
                                continue

                        time.sleep(5)
                        print("✅ Method 2: Search submitted successfully")
                    else:
                        raise Exception("Could not find search box")

                except Exception as method2_error:
                    print(f"❌ Method 2 also failed: {method2_error}")
                    return False

            # Handle cookie consent if it appears (for both methods)
            print("🍪 Checking for cookie consent...")
            try:
                # Check if we're on a consent page
                current_url = self.driver.current_url
                page_title = self.driver.title

                if "consent.google.com" in current_url or "consent" in page_title.lower() or "voordat je verdergaat" in page_title.lower():
                    print(f"🍪 Detected consent page: {page_title}")
                    print(f"🌐 Consent URL: {current_url}")

                    # Extended list of consent button selectors (multiple languages)
                    cookie_buttons = [
                        # English
                        "//button[contains(text(), 'Accept all')]",
                        "//button[contains(text(), 'I agree')]",
                        "//button[contains(text(), 'Accept')]",
                        "//div[contains(text(), 'Accept all')]//parent::button",
                        "//button[@aria-label='Accept all']",

                        # Dutch (specific to the detected consent page)
                        "//button[contains(text(), 'Alles accepteren')]",
                        "//button[contains(text(), 'Accepteren')]",
                        "//button[contains(text(), 'Akkoord')]",
                        "//button[contains(text(), 'Ga door naar Google Maps')]",  # Continue to Google Maps
                        "//button[contains(text(), 'Doorgaan')]",  # Continue

                        # More specific Dutch selectors
                        "//div[contains(text(), 'Alles accepteren')]//parent::button",
                        "//div[contains(text(), 'Accepteren')]//parent::button",

                        # Generic Google consent selectors (very specific)
                        "//button[contains(@class, 'VfPpkd-LgbsSe') and contains(@class, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ')]",
                        "//button[contains(@class, 'VfPpkd-LgbsSe')]",
                        "//div[@role='button'][contains(@class, 'VfPpkd')]",
                        "//button[@jsname]",
                        "//div[@role='button']",

                        # Form submission
                        "//form//button[@type='submit']",
                        "//input[@type='submit']",
                        "//button[not(@disabled)]",  # Any enabled button
                        "//div[@role='button'][not(@disabled)]"  # Any enabled div button
                    ]

                    consent_handled = False
                    for button_xpath in cookie_buttons:
                        try:
                            print(f"   Trying selector: {button_xpath}")
                            accept_button = WebDriverWait(self.driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, button_xpath))
                            )
                            accept_button.click()
                            print("✅ Clicked consent button")
                            time.sleep(5)  # Wait for redirect

                            # Check if we were redirected away from consent page
                            new_url = self.driver.current_url
                            if "consent.google.com" not in new_url:
                                print("✅ Successfully handled consent and redirected")
                                consent_handled = True
                                break
                            else:
                                print("⚠️ Still on consent page, trying next selector...")

                        except Exception as button_error:
                            print(f"   ❌ Selector failed: {button_error}")
                            continue

                    if not consent_handled:
                        print("⚠️ Could not handle consent page automatically")
                        print("🔄 Trying alternative approach: direct navigation...")

                        # Try to bypass consent by going directly to search results
                        try:
                            bypass_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '+')}"
                            print(f"🌐 Attempting bypass: {bypass_url}")
                            self.driver.get(bypass_url)
                            time.sleep(5)

                            # Check if we're still on consent page
                            final_url = self.driver.current_url
                            if "consent.google.com" not in final_url:
                                print("✅ Successfully bypassed consent page")
                                consent_handled = True
                            else:
                                print("❌ Still on consent page after bypass attempt")

                        except Exception as bypass_error:
                            print(f"❌ Bypass attempt failed: {bypass_error}")

                        # If still not handled, continue anyway
                        if not consent_handled:
                            print("⚠️ Continuing despite consent page issues...")
                else:
                    print("ℹ️ No consent page detected")

            except Exception as e:
                print(f"⚠️ Error handling consent: {e}")

            # Wait for results to load with longer timeout
            print("⏳ Waiting for search results to load...")
            time.sleep(5)

            # Check if we have results by looking for business listings
            try:
                # Look for any business result indicators with more selectors
                result_indicators = [
                    "//div[contains(@class, 'Nv2PK')]",  # Business listing container
                    "//div[@role='article']",  # Article role elements
                    "//a[contains(@href, '/maps/place/')]",  # Direct place links
                    "//div[contains(@class, 'bfdHYd')]",  # Another common container
                    "//div[contains(@class, 'lI9IFe')]",  # Search result container
                    "//div[contains(@jsaction, 'mouseover')]"  # Interactive elements
                ]

                found_results = False
                total_elements = 0

                for indicator in result_indicators:
                    try:
                        elements = self.driver.find_elements(By.XPATH, indicator)
                        if elements:
                            print(f"✅ Found {len(elements)} potential results with selector: {indicator}")
                            total_elements += len(elements)
                            found_results = True
                            break
                    except Exception as indicator_error:
                        print(f"⚠️ Selector {indicator} failed: {indicator_error}")
                        continue

                if found_results:
                    print(f"🎯 Total potential results found: {total_elements}")
                else:
                    print("⚠️ No obvious results found, but continuing...")
                    # Still return True to attempt link extraction

            except Exception as e:
                print(f"⚠️ Error checking for results: {e}")

            print("✅ Search completed successfully")
            return True

        except Exception as e:
            print(f"❌ Search failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_business_links(self):
        """Extract business links from Google Maps results with improved selectors"""
        try:
            print("📋 Extracting business links...")
            all_links = set()
            scroll_attempts = 0
            max_scrolls = 8
            no_new_content_count = 0

            # Multiple strategies to find business links
            link_selectors = [
                '//a[contains(@href, "/maps/place/")]',
                '//div[@role="article"]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "Nv2PK")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "bfdHYd")]//a[contains(@href, "/maps/place/")]'
            ]

            while scroll_attempts < max_scrolls and len(all_links) < self.max_results:
                print(f"🔄 Scroll attempt {scroll_attempts + 1}/{max_scrolls}")

                # Try multiple selectors to find links
                new_links_count = 0
                for selector in link_selectors:
                    try:
                        link_elements = self.driver.find_elements(By.XPATH, selector)
                        for element in link_elements:
                            try:
                                href = element.get_attribute('href')
                                if href and '/maps/place/' in href:
                                    if href not in all_links:
                                        all_links.add(href)
                                        new_links_count += 1
                            except:
                                continue
                    except Exception as e:
                        print(f"⚠️ Selector {selector} failed: {e}")
                        continue

                print(f"📊 Found {len(all_links)} total links (+{new_links_count} new)")

                # If we have enough links, break early
                if len(all_links) >= self.max_results:
                    print(f"🎯 Reached target of {self.max_results} links")
                    break

                # Check if we found new content
                if new_links_count == 0:
                    no_new_content_count += 1
                    if no_new_content_count >= 3:
                        print("⏹️ No new content found after 3 attempts, stopping")
                        break
                else:
                    no_new_content_count = 0

                # Scroll down to load more results - try multiple scroll methods
                try:
                    # Method 1: Find and scroll the results panel
                    scrollable_selectors = [
                        '[role="main"]',
                        '.m6QErb',
                        '#pane',
                        '.siAUzd'
                    ]

                    scrolled = False
                    for selector in scrollable_selectors:
                        try:
                            results_panel = self.driver.find_element(By.CSS_SELECTOR, selector)
                            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
                            scrolled = True
                            print(f"✅ Scrolled using selector: {selector}")
                            break
                        except:
                            continue

                    if not scrolled:
                        # Fallback: scroll the entire page
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        print("✅ Used fallback page scroll")

                    time.sleep(random.uniform(2, 4))  # Random delay to avoid detection

                except Exception as e:
                    print(f"⚠️ Scroll error: {e}")
                    time.sleep(2)

                scroll_attempts += 1

            business_links = list(all_links)[:self.max_results]
            print(f"✅ Final result: {len(business_links)} business links extracted")

            # Debug: print first few links
            if business_links:
                print("🔗 Sample links:")
                for i, link in enumerate(business_links[:3]):
                    print(f"  {i+1}. {link[:80]}...")
            else:
                print("❌ No business links found!")

            return business_links

        except Exception as e:
            print(f"❌ Link extraction failed: {e}")
            import traceback
            traceback.print_exc()
            return []

    def extract_business_data(self, business_url):
        """Extract data from a single business page with improved selectors"""
        try:
            print(f"📊 Extracting data from: {business_url[:60]}...")
            self.driver.get(business_url)
            time.sleep(random.uniform(3, 5))  # Random delay

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

            # Extract business name with multiple selectors
            name_selectors = [
                'h1[data-attrid="title"]',
                'h1.DUwDvf',
                'h1.x3AX1-LfntMc-header-title-title',
                'h1',
                '.x3AX1-LfntMc-header-title-title',
                '.DUwDvf'
            ]

            for selector in name_selectors:
                try:
                    name_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    name_text = name_element.text.strip()
                    if name_text and len(name_text) > 1:
                        data['name'] = name_text
                        break
                except:
                    continue

            if not data['name']:
                data['name'] = 'Unknown Business'

            # Extract address with multiple selectors
            address_selectors = [
                '[data-item-id="address"]',
                '.Io6YTe.fontBodyMedium.kR99db.fdkmkc',
                '.rogA2c .Io6YTe',
                'button[data-item-id="address"]',
                '.fccl3c .Io6YTe'
            ]

            for selector in address_selectors:
                try:
                    address_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    address_text = address_element.text.strip()
                    if address_text and len(address_text) > 5:
                        data['address'] = address_text
                        break
                except:
                    continue

            if not data['address']:
                data['address'] = 'Address not found'

            # Extract rating and review count with multiple approaches
            rating_selectors = [
                '.F7nice span[aria-hidden="true"]',
                '.ceNzKf[aria-label*="stars"]',
                'span.ceNzKf',
                '.MW4etd'
            ]

            for selector in rating_selectors:
                try:
                    rating_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    rating_text = rating_element.text.strip()

                    # Try to extract rating number
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        data['rating'] = float(rating_match.group(1))
                        break
                except:
                    continue

            # Extract review count
            review_selectors = [
                '.F7nice span:nth-child(2)',
                'button[aria-label*="reviews"]',
                '.UY7F9'
            ]

            for selector in review_selectors:
                try:
                    review_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    review_text = review_element.text.strip()

                    # Extract number from text like "(1,234)" or "1,234 reviews"
                    review_match = re.search(r'[\(]?(\d+(?:,\d+)*)[\)]?', review_text)
                    if review_match:
                        data['review_count'] = int(review_match.group(1).replace(',', ''))
                        break
                except:
                    continue

            # Extract category
            category_selectors = [
                '.DkEaL',
                'button[jsaction*="category"]',
                '.YhemCb'
            ]

            for selector in category_selectors:
                try:
                    category_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    category_text = category_element.text.strip()
                    if category_text and len(category_text) > 2:
                        data['category'] = category_text
                        break
                except:
                    continue

            if not data['category']:
                data['category'] = 'Category not found'

            # Extract website
            website_selectors = [
                'a[data-item-id="authority"]',
                'a[href*="http"]:not([href*="google.com"]):not([href*="maps"])',
                '.CsEnBe a[href*="http"]'
            ]

            for selector in website_selectors:
                try:
                    website_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    website_url = website_element.get_attribute('href')
                    if website_url and 'google.com' not in website_url and 'maps' not in website_url:
                        data['website'] = website_url
                        break
                except:
                    continue

            # Extract phone number
            phone_selectors = [
                'button[data-item-id*="phone"]',
                '.rogA2c button[aria-label*="phone"]',
                'button[aria-label*="Call"]',
                '.Io6YTe.fontBodyMedium.kR99db.fdkmkc[aria-label*="phone"]'
            ]

            for selector in phone_selectors:
                try:
                    phone_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    phone_text = phone_element.get_attribute('aria-label') or phone_element.text

                    # Try to extract phone number using patterns
                    for pattern in self.phone_patterns:
                        match = pattern.search(phone_text)
                        if match:
                            data['mobile'] = match.group(0)
                            break

                    if data['mobile']:
                        break

                except:
                    continue

            self.extracted_count += 1

            # Create a summary for logging
            summary = f"✅ {data['name']}"
            if data['rating']:
                summary += f" ({data['rating']}⭐)"
            if data['mobile']:
                summary += f" 📞"
            if data['website']:
                summary += f" 🌐"

            print(summary)
            return data

        except Exception as e:
            print(f"❌ Data extraction failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    def run_extraction(self):
        """Main extraction process with improved error handling and debugging"""
        start_time = datetime.now()
        results = []

        try:
            print(f"🚀 STARTING GOOGLE MAPS EXTRACTION")
            print(f"🔍 Search Query: '{self.search_query}'")
            print(f"🎯 Target: {self.max_results} businesses")
            print(f"🌐 Website visits: {'Enabled' if self.visit_websites else 'Disabled'}")
            print(f"⏰ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 70)

            # Step 1: Search Google Maps
            print("\n🔍 STEP 1: Searching Google Maps...")
            if not self.search_google_maps():
                print("❌ Failed to search Google Maps")
                return []
            print("✅ Google Maps search completed")

            # Step 2: Extract business links
            print("\n📋 STEP 2: Extracting business links...")
            business_links = self.get_business_links()
            if not business_links:
                print("❌ No business links found")
                print("🔍 Debug: Checking page source for clues...")

                # Debug information
                try:
                    page_title = self.driver.title
                    current_url = self.driver.current_url
                    print(f"📄 Page title: {page_title}")
                    print(f"🌐 Current URL: {current_url}")

                    # Check if we're blocked or redirected
                    if "sorry" in page_title.lower() or "blocked" in page_title.lower():
                        print("🚫 Appears to be blocked by Google")
                    elif "maps" not in current_url:
                        print("🔄 Redirected away from Google Maps")
                    else:
                        print("🤔 On Google Maps but no results found")

                except Exception as debug_e:
                    print(f"⚠️ Debug info error: {debug_e}")

                return []

            print(f"✅ Found {len(business_links)} business links")

            # Step 3: Extract data from each business
            print(f"\n📊 STEP 3: Extracting data from businesses...")
            print("=" * 70)

            successful_extractions = 0
            failed_extractions = 0

            for i, link in enumerate(business_links, 1):
                print(f"\n[{i:2d}/{len(business_links)}] Processing business {i}...")

                try:
                    business_data = self.extract_business_data(link)
                    if business_data and business_data.get('name') != 'Unknown Business':
                        results.append(business_data)
                        successful_extractions += 1

                        # Count contacts
                        if business_data.get('email') or business_data.get('mobile'):
                            self.contacts_found += 1
                    else:
                        failed_extractions += 1
                        print(f"⚠️ Failed to extract meaningful data from business {i}")

                except Exception as extract_e:
                    failed_extractions += 1
                    print(f"❌ Error extracting business {i}: {extract_e}")

                # Progress update every 5 businesses
                if i % 5 == 0:
                    elapsed = datetime.now() - start_time
                    rate = i / elapsed.total_seconds() * 60 if elapsed.total_seconds() > 0 else 0
                    print(f"📈 Progress: {successful_extractions} successful, {failed_extractions} failed, {rate:.1f} businesses/min")

                # Add delay between requests to avoid being blocked
                delay = random.uniform(2, 4)
                time.sleep(delay)

            # Final summary
            end_time = datetime.now()
            duration = end_time - start_time

            print(f"\n" + "=" * 70)
            print(f"🎉 EXTRACTION COMPLETED!")
            print(f"⏱️ Duration: {duration}")
            print(f"📊 Businesses processed: {len(business_links)}")
            print(f"✅ Successful extractions: {successful_extractions}")
            print(f"❌ Failed extractions: {failed_extractions}")
            print(f"📞 Contacts found: {self.contacts_found}")
            print(f"📋 Final results: {len(results)} businesses")

            if results:
                print(f"\n📝 Sample results:")
                for i, result in enumerate(results[:3], 1):
                    print(f"  {i}. {result['name']} - {result['address'][:50]}...")

            return results

        except Exception as e:
            print(f"❌ Critical extraction error: {e}")
            import traceback
            traceback.print_exc()
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
