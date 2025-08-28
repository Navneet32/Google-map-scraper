#!/usr/bin/env python3
"""
Enhanced Google Maps Scraper - Optimized for maximum lead extraction
Addresses issues with limited results (4-5 leads) by implementing:
- More aggressive scrolling strategies
- Better selector coverage
- Improved wait times and retry logic
- Enhanced result extraction methods
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
    def __init__(self, search_query, max_results=100, visit_websites=True):
        self.search_query = search_query
        self.max_results = max_results
        self.visit_websites = visit_websites
        self.extracted_count = 0
        self.contacts_found = 0
        
        # Enhanced email and phone patterns
        self.email_patterns = [
            re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            re.compile(r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'),
            re.compile(r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', re.IGNORECASE),
        ]
        
        # Enhanced phone patterns with better support for Indian numbers
        self.phone_patterns = [
            # Indian numbers with country code (e.g., +91 98765 43210, 91-98765-43210)
            re.compile(r'(?:\+?(91)|(0)|(\+?\d{1,3}))?[\s.-]?\b(\d{5})\s?-?\s?(\d{5})\b'),
            # Standard 10-digit numbers
            re.compile(r'(?:\+?(\d{1,3})[\s.-]?)?\(?(\d{3})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})\b'),
            # Numbers with special characters
            re.compile(r'(?:\+?(\d{1,3})[\s.-]?)?\(?\s*(\d{2,})\s*\)?[\s.-]?\s*(\d+)[\s.-]?\s*(\d+)\b'),
            # Simple 10+ digit numbers
            re.compile(r'\b(?:\+?\d{1,3}[\s.-]?)?(\d[\s.-]?){9,}\d\b'),
            # Phone numbers in href attributes
            re.compile(r'tel:(\+?[\d\s.-]{10,})\b'),
            # Common phone number formats
            re.compile(r'\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'),
            # Indian mobile numbers
            re.compile(r'\b(?:0|\+?91[\s-]?)?[6-9]\d{9}\b')
        ]
        
        self.setup_browser()
    
    def setup_browser(self):
        """Enhanced browser setup with Railway-specific optimizations"""
        print("🔧 Setting up enhanced Chrome browser for Railway...")

        self.chrome_options = Options()
        
        # Railway-optimized browser options
        browser_options = [
            "--headless=new",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-plugins",
            "--disable-images",  # Faster loading
            "--disable-javascript-harmony-shipping",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--disable-ipc-flooding-protection",
            "--window-size=1920,1080",  # Larger window for more content
            "--lang=en-US",
            "--accept-lang=en-US,en",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Railway-specific optimizations
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--disable-default-apps",
            "--disable-sync",
            "--disable-translate",
            "--hide-scrollbars",
            "--metrics-recording-only",
            "--mute-audio",
            "--no-default-browser-check",
            "--no-pings",
            "--password-store=basic",
            "--use-mock-keychain",
            "--disable-component-extensions-with-background-pages",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-client-side-phishing-detection",
            "--disable-hang-monitor",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-domain-reliability",
            "--disable-features=TranslateUI",
            "--disable-ipc-flooding-protection",
            "--enable-features=NetworkService,NetworkServiceLogging",
            "--force-color-profile=srgb",
            "--memory-pressure-off",
            "--max_old_space_size=4096"
        ]
        
        for option in browser_options:
            self.chrome_options.add_argument(option)

        # Railway-optimized preferences
        self.chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': 'en-US,en',
            'intl.charset_default': 'UTF-8',
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'profile.managed_default_content_settings.images': 2,  # Block images for faster loading
            'profile.default_content_setting_values.media_stream_mic': 2,
            'profile.default_content_setting_values.media_stream_camera': 2,
            'profile.default_content_setting_values.geolocation': 2,
            'profile.default_content_setting_values.desktop_notifications': 2,
            'profile.password_manager_enabled': False,
            'credentials_enable_service': False,
            'profile.default_content_settings.popups': 0
        })
        
        # Railway-specific experimental options
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 30)  # Longer timeout for Railway
            
            # Railway-specific: Remove automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Railway-optimized browser setup completed")
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            raise

    def search_google_maps(self):
        """Enhanced Google Maps search with Railway-specific optimizations"""
        try:
            print(f"🔍 Enhanced search for: {self.search_query}")

            # Strategy 1: Direct search with enhanced URL
            search_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '+')}"
            print(f"🌐 Navigating to: {search_url}")

            self.driver.get(search_url)
            time.sleep(15)  # Longer wait for Railway environment

            # Handle consent/cookies more aggressively
            self._handle_consent_and_cookies()

            # Railway-specific: Additional wait and page check
            self._railway_page_verification()

            # Wait for results with multiple indicators
            self._wait_for_search_results()

            print("✅ Enhanced search completed")
            return True

        except Exception as e:
            print(f"❌ Enhanced search failed: {e}")
            # Railway fallback: Try alternative search method
            return self._fallback_search_strategy()
    
    def _railway_page_verification(self):
        """Railway-specific page verification and debugging"""
        try:
            print("🔍 Railway environment verification...")
            
            # Check if page loaded properly
            page_title = self.driver.title
            current_url = self.driver.current_url
            
            print(f"  Page title: {page_title[:50]}...")
            print(f"  Current URL: {current_url[:80]}...")
            
            # Check for common Railway/headless issues
            if "blocked" in page_title.lower() or "captcha" in page_title.lower():
                print("⚠️ Detected potential blocking - trying refresh")
                self.driver.refresh()
                time.sleep(10)
            
            # Verify page has loaded content
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if len(body_text) < 100:
                print("⚠️ Page seems empty - waiting longer")
                time.sleep(10)
                
        except Exception as e:
            print(f"⚠️ Railway verification error: {e}")
    
    def _fallback_search_strategy(self):
        """Fallback search strategy for Railway environment"""
        try:
            print("🔄 Trying fallback search strategy...")
            
            # Try different URL format
            fallback_url = f"https://www.google.com/maps/search/{self.search_query.replace(' ', '%20')}"
            print(f"🌐 Fallback URL: {fallback_url}")
            
            self.driver.get(fallback_url)
            time.sleep(20)  # Even longer wait
            
            # Try to interact with page to trigger loading
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.click()
                time.sleep(5)
            except:
                pass
            
            self._handle_consent_and_cookies()
            self._wait_for_search_results()
            
            print("✅ Fallback search completed")
            return True
            
        except Exception as e:
            print(f"❌ Fallback search failed: {e}")
            return False

    def _handle_consent_and_cookies(self):
        """Enhanced consent and cookie handling"""
        try:
            print("🍪 Handling consent and cookies...")
            
            # Extended consent selectors (multiple languages)
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
                    button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button.click()
                    print("✅ Consent handled")
                    time.sleep(3)
                    break
                except:
                    continue

        except Exception as e:
            print(f"⚠️ Consent handling: {e}")

    def _wait_for_search_results(self):
        """Enhanced waiting for search results"""
        print("⏳ Waiting for search results...")
        
        # Multiple result indicators
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

        max_wait = 30
        wait_count = 0
        
        while wait_count < max_wait:
            for selector in result_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements and len(elements) > 0:
                        print(f"✅ Found {len(elements)} results with selector")
                        return True
                except:
                    continue
            
            time.sleep(1)
            wait_count += 1
            
        print("⚠️ No clear results found, but continuing...")
        return True

    def get_business_links(self):
        """Enhanced business link extraction with aggressive scrolling"""
        try:
            print("📋 Enhanced business link extraction...")
            all_links = set()
            scroll_attempts = 0
            max_scrolls = 200  # Increased from 100 to 200 for more thorough scraping
            no_new_content_count = 0
            max_patience = 25  # Increased from 15 to 25 for more patience

            # Comprehensive link selectors - updated with more recent Google Maps selectors
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
                '//div[contains(@class, "section-result")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "Nv2PK")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "qBF1Pd")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "hfpxzc")]',  # New Google Maps card selector
                '//div[contains(@class, "lI9IFe")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "m6QErb")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "Nv2PK")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "bfdHYd")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "VkpGBb")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "qBF1Pd")]//a[contains(@href, "/maps/place/")]',
                '//div[contains(@class, "hfpxzc")]'  # New Google Maps card selector
            ]

            # Railway-specific: Initial element detection
            if scroll_attempts == 0:
                print("🔍 Railway environment - checking initial page state...")
                self._debug_page_elements()
            
            while scroll_attempts < max_scrolls and len(all_links) < self.max_results:
                print(f"🔄 Enhanced scroll {scroll_attempts + 1}/{max_scrolls}")

                # Extract links with all selectors
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
                                    
                                    # Railway debug: Show first few found links
                                    if len(all_links) <= 5:
                                        print(f"  ✅ Railway found: {href[:60]}...")
                                        
                            except:
                                continue
                    except:
                        continue
                
                # Railway-specific: Extra debugging when no links found
                if new_links_count == 0 and scroll_attempts < 5:
                    print(f"  ⚠️ No links found on attempt {scroll_attempts + 1} - debugging...")
                    self._debug_no_links_found()

                current_count = len(all_links)
                progress = (current_count / self.max_results) * 100 if self.max_results > 0 else 0
                print(f"📊 Found {current_count} links (+{new_links_count} new) - {progress:.1f}% of target")

                # Early exit if target reached
                if current_count >= self.max_results:
                    print(f"🎯 Target reached: {current_count} links")
                    break

                # Railway-optimized patience logic
                if new_links_count == 0:
                    no_new_content_count += 1
                    # Try different strategies more aggressively for Railway
                    if no_new_content_count == 2:  # Earlier intervention
                        print("🔄 Railway: Trying alternative scroll strategy...")
                        self._alternative_scroll_strategy()
                    elif no_new_content_count == 4:  # Earlier refresh
                        print("🔄 Railway: Trying page refresh strategy...")
                        self._page_refresh_strategy()
                    elif no_new_content_count == 7:  # Earlier zoom
                        print("🔄 Railway: Trying zoom out strategy...")
                        self._zoom_out_strategy()
                    elif no_new_content_count == 12:  # Railway-specific strategy
                        print("🔄 Railway: Trying complete page reload...")
                        self._railway_complete_reload()
                    
                    if no_new_content_count >= max_patience:
                        print(f"⏹️ Railway: No new content after {max_patience} attempts")
                        # Final Railway attempt
                        final_links = self._railway_final_attempt()
                        if final_links:
                            all_links.update(final_links)
                        break
                else:
                    no_new_content_count = 0

                # Railway-optimized scrolling strategy
                self._enhanced_scroll()
                
                # Railway-specific delay strategy (longer delays for stability)
                if new_links_count > 0:
                    delay = random.uniform(2, 4)  # Slower even when finding results
                else:
                    delay = random.uniform(5, 8)  # Much slower when stuck
                time.sleep(delay)
                
                scroll_attempts += 1

            business_links = list(all_links)[:self.max_results]
            print(f"✅ Enhanced extraction complete: {len(business_links)} links")

            # Show sample links for debugging
            if business_links:
                print("🔗 Sample links:")
                for i, link in enumerate(business_links[:5]):
                    print(f"  {i+1}. {link[:80]}...")

            return business_links

        except Exception as e:
            print(f"❌ Enhanced link extraction failed: {e}")
            return []

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
    
    def _debug_page_elements(self):
        """Debug page elements for Railway environment"""
        try:
            print("🔍 Railway debugging - checking page elements...")
            
            # Check basic page structure
            debug_selectors = [
                ('//div', 'All divs'),
                ('//a', 'All links'),
                ('//div[contains(@class, "hfpxzc")]', 'hfpxzc divs'),
                ('//div[contains(@class, "Nv2PK")]', 'Nv2PK divs'),
                ('//a[contains(@href, "maps")]', 'Maps links'),
                ('//div[@role="article"]', 'Article divs'),
                ('//div[contains(@class, "THOPZb")]', 'THOPZb divs')
            ]
            
            for selector, description in debug_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    print(f"  {description}: {len(elements)} found")
                    
                    # Show sample text for first few elements
                    if len(elements) > 0 and 'links' in description.lower():
                        for i, elem in enumerate(elements[:3]):
                            try:
                                href = elem.get_attribute('href') or 'No href'
                                text = elem.text[:30] or 'No text'
                                print(f"    [{i+1}] {text}... -> {href[:50]}...")
                            except:
                                pass
                                
                except Exception as e:
                    print(f"  {description}: Error - {e}")
            
            # Check page source for debugging
            page_source_length = len(self.driver.page_source)
            print(f"  Page source length: {page_source_length} characters")
            
            if page_source_length < 10000:
                print("⚠️ Page source seems small - potential loading issue")
                
        except Exception as e:
            print(f"⚠️ Debug page elements error: {e}")
    
    def _debug_no_links_found(self):
        """Debug when no links are found"""
        try:
            print("🔍 Debugging why no links were found...")
            
            # Check if we're on the right page
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            print(f"  Current URL: {current_url[:80]}...")
            print(f"  Page title: {page_title[:50]}...")
            
            # Check for error messages or blocks
            error_indicators = [
                '//div[contains(text(), "blocked")]',
                '//div[contains(text(), "error")]',
                '//div[contains(text(), "captcha")]',
                '//div[contains(text(), "robot")]'
            ]
            
            for indicator in error_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    if elements:
                        print(f"⚠️ Found potential issue: {elements[0].text[:50]}...")
                except:
                    pass
            
            # Try to take a screenshot for debugging (if possible)
            try:
                screenshot_path = f"/tmp/debug_screenshot_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"  Screenshot saved: {screenshot_path}")
            except:
                print("  Could not save screenshot")
                
        except Exception as e:
            print(f"⚠️ Debug no links error: {e}")
    
    def _railway_complete_reload(self):
        """Complete page reload strategy for Railway"""
        try:
            print("🔄 Railway: Complete page reload...")
            
            current_url = self.driver.current_url
            self.driver.get(current_url)
            time.sleep(20)  # Long wait after reload
            
            # Re-handle consent
            self._handle_consent_and_cookies()
            
            # Wait for page to stabilize
            time.sleep(10)
            
            print("✅ Railway: Complete reload finished")
            
        except Exception as e:
            print(f"⚠️ Railway reload error: {e}")
    
    def _railway_final_attempt(self):
        """Final attempt to find links using alternative methods"""
        try:
            print("🔄 Railway: Final attempt using alternative methods...")
            
            final_links = set()
            
            # Method 1: Search page source directly
            page_source = self.driver.page_source
            import re
            
            # Find all Google Maps place URLs in page source
            place_pattern = r'https://www\.google\.com/maps/place/[^"\s]+'
            matches = re.findall(place_pattern, page_source)
            
            for match in matches:
                if '/maps/place/' in match:
                    final_links.add(match)
                    print(f"  ✅ Source found: {match[:60]}...")
            
            # Method 2: Try JavaScript execution
            try:
                js_links = self.driver.execute_script("""
                    var links = [];
                    var elements = document.querySelectorAll('a[href*="/maps/place/"]');
                    for (var i = 0; i < elements.length; i++) {
                        if (elements[i].href) {
                            links.push(elements[i].href);
                        }
                    }
                    return links;
                """)
                
                for link in js_links:
                    final_links.add(link)
                    print(f"  ✅ JS found: {link[:60]}...")
                    
            except Exception as e:
                print(f"  ⚠️ JS method failed: {e}")
            
            print(f"  Railway final attempt found {len(final_links)} links")
            return final_links
            
        except Exception as e:
            print(f"⚠️ Railway final attempt error: {e}")
            return set()

    def extract_business_data(self, business_url):
        """Enhanced business data extraction"""
        try:
            print(f"📊 Enhanced extraction: {business_url[:60]}...")
            self.driver.get(business_url)
            time.sleep(random.uniform(4, 7))  # Longer wait for full page load

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

            # Enhanced name extraction
            data['name'] = self._extract_business_name()
            
            # Enhanced address extraction
            data['address'] = self._extract_address()
            
            # Enhanced rating and reviews
            data['rating'], data['review_count'] = self._extract_rating_and_reviews()
            
            # Enhanced category extraction
            data['category'] = self._extract_category()
            
            # Enhanced website extraction
            data['website'] = self._extract_website()
            
            # Enhanced phone extraction
            data['mobile'] = self._extract_phone_enhanced()

            self.extracted_count += 1

            # Enhanced summary
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
            print(f"❌ Enhanced extraction failed: {e}")
            return None

    def _extract_business_name(self):
        """Enhanced business name extraction"""
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
        """Enhanced address extraction"""
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
        """Enhanced rating and review extraction"""
        rating = None
        review_count = None

        # Rating selectors
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

        # Review count selectors
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
        """Enhanced category extraction"""
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
        """Enhanced website extraction"""
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
        """Enhanced phone number extraction with multiple strategies"""
        try:
            # Strategy 1: Direct phone button/link selectors
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
            
            # Strategy 2: Text-based search in visible elements
            text_selectors = [
                "//span[contains(text(),'(') and contains(text(),')')]",
                "//div[contains(text(),'(') and contains(text(),')')]",
                "//div[contains(@class,'fontBodyMedium')]"
            ]
            
            for selector in text_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        phone = self._extract_phone_from_element(element)
                        if phone:
                            return phone
                except:
                    continue
            
            # Strategy 3: Page source search (last resort)
            page_source = self.driver.page_source
            for pattern in self.phone_patterns:
                matches = pattern.findall(page_source)
                for match in matches:
                    if isinstance(match, tuple):
                        match = ''.join(match)
                    digits = re.sub(r'\D', '', str(match))
                    if len(digits) >= 10:
                        return str(match)
            
            return None
            
        except Exception as e:
            print(f"❌ Enhanced phone extraction error: {e}")
            return None

    def _extract_phone_from_element(self, element):
        """Extract phone from element with enhanced patterns"""
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
                    
                # Clean the text
                text = text.replace('tel:', '').replace('Phone: ', '').replace('Call ', '')
                
                # Try each pattern
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
        """Enhanced main extraction process"""
        start_time = datetime.now()
        results = []

        try:
            print(f"🚀 ENHANCED GOOGLE MAPS EXTRACTION")
            print(f"🔍 Query: '{self.search_query}'")
            print(f"🎯 Target: {self.max_results} businesses")
            print(f"⏰ Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 70)

            # Enhanced search
            if not self.search_google_maps():
                print("❌ Enhanced search failed")
                return []

            # Enhanced link extraction
            business_links = self.get_business_links()
            if not business_links:
                print("❌ No business links found")
                return []

            print(f"✅ Found {len(business_links)} business links")

            # Enhanced data extraction
            print(f"\n📊 ENHANCED DATA EXTRACTION")
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

                # Progress updates
                if i % 10 == 0:
                    elapsed = datetime.now() - start_time
                    rate = i / elapsed.total_seconds() * 60 if elapsed.total_seconds() > 0 else 0
                    print(f"📈 Progress: {successful} successful, {rate:.1f}/min")

                # Adaptive delay
                delay = random.uniform(1.5, 3.5)
                time.sleep(delay)

            # Enhanced final summary
            end_time = datetime.now()
            duration = end_time - start_time

            print(f"\n" + "=" * 70)
            print(f"🎉 ENHANCED EXTRACTION COMPLETED!")
            print(f"⏱️ Duration: {duration}")
            print(f"📊 Links processed: {len(business_links)}")
            print(f"✅ Successful: {successful}")
            print(f"❌ Failed: {failed}")
            print(f"📞 Contacts found: {self.contacts_found}")
            print(f"📋 Final results: {len(results)} businesses")
            print(f"📈 Success rate: {(successful/len(business_links)*100):.1f}%")

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
