import os
import time
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from .site_config import SiteRegistry, AuthType
from .auth_manager import AuthenticationManager
from .chrome_profile_selector import ChromeProfileSelector
from .chrome_manager import ChromeManager

console = Console()


class APIDocParser:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.driver = None
        self.authenticated = False
        self.profile_with_cookies = None
        self.site_registry = SiteRegistry()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            console.print(f"[yellow]Config file {config_path} not found. Using defaults.[/yellow]")
            return {}
    
    def _init_driver(self, headless: bool = False, profile_name: Optional[str] = None) -> webdriver.Chrome:
        """Initialize Chrome webdriver with profile selection"""
        
        # Use ChromeManager for better profile handling
        self.chrome_manager = ChromeManager()
        
        # Use profile selector to choose profile
        profile_selector = ChromeProfileSelector()
        selected_profile = profile_selector.select_profile(auto_select=profile_name)
        
        if not selected_profile:
            raise Exception("No profile selected. Cancelling browser launch.")
        
        # Store selected profile for reference
        self._selected_profile = selected_profile
        
        console.print("[cyan]Starting Chrome browser...[/cyan]")
        
        try:
            # Determine base profile path if not temporary
            base_profile = None
            if selected_profile['name'] != 'Temporary':
                if selected_profile['name'] == 'Default':
                    base_profile = profile_selector.chrome_dir
                else:
                    base_profile = os.path.join(profile_selector.chrome_dir, selected_profile['name'])
            
            # Create driver with ChromeManager
            driver = self.chrome_manager.create_driver(
                base_profile=base_profile,
                headless=headless
            )
            
            return driver
        except Exception as e:
            error_msg = str(e)
            
            # Check for common Chrome profile in use error
            if "user data directory is already in use" in error_msg:
                console.print(f"[red]Failed to start browser: Chrome profile is already in use![/red]")
                console.print("\n[yellow]⚠️  This error typically means:[/yellow]")
                console.print("1. [cyan]Chrome is already running with the selected profile[/cyan]")
                console.print("2. [cyan]A previous Chrome process didn't shut down properly[/cyan]")
                console.print("\n[yellow]Solutions:[/yellow]")
                console.print("1. [green]Try again - we'll use a unique temporary directory[/green]")
                console.print("2. [cyan]Select profile '0' (Temporary) for a clean profile[/cyan]")
                console.print("3. [cyan]Close all Chrome windows and try again[/cyan]")
                
                # Check if Chrome is running
                import subprocess
                try:
                    result = subprocess.run(['pgrep', '-x', 'Google Chrome'], capture_output=True, text=True)
                    if result.returncode == 0:
                        console.print("\n[red]✗ Chrome is currently running![/red]")
                        console.print(f"[dim]Process IDs: {result.stdout.strip()}[/dim]")
                except:
                    pass
            else:
                console.print(f"[red]Failed to start browser: {e}[/red]")
                console.print("[yellow]Troubleshooting tips:[/yellow]")
                console.print("1. Make sure Chrome is up to date")
                console.print("2. Try: brew upgrade google-chrome")
                console.print("3. Or download from: https://www.google.com/chrome/")
            raise
    
    def _copy_cookies_to_driver(self, driver: webdriver.Chrome, profile_path: str):
        """Copy cookies from Chrome profile to the webdriver"""
        import sqlite3
        import shutil
        import tempfile
        from pathlib import Path
        from urllib.parse import urlparse
        
        console.print("[cyan]Copying cookies from Chrome profile...[/cyan]")
        
        # We'll get domain from the target URL passed to extract_function
        # For now, just copy all relevant cookies
        
        # Copy cookies database
        cookies_db = Path(profile_path) / "Cookies"
        temp_cookies = tempfile.mktemp(suffix=".db")
        
        try:
            shutil.copy2(cookies_db, temp_cookies)
            conn = sqlite3.connect(temp_cookies)
            cursor = conn.cursor()
            
            # Get all cookies
            cursor.execute("""
                SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, samesite
                FROM cookies
            """)
            
            cookies = cursor.fetchall()
            cookie_count = 0
            
            # Get current domain from driver URL
            current_url = driver.current_url
            if current_url and current_url != 'data:,':
                current_domain = urlparse(current_url).netloc
            else:
                current_domain = None
            
            for cookie in cookies:
                host_key, name, value, path, expires_utc, is_secure, is_httponly, samesite = cookie
                
                # For sensortower cookies, be more permissive
                if current_domain and 'sensortower' in current_domain:
                    if 'sensortower' not in host_key:
                        continue
                elif current_domain:
                    # Check if cookie is relevant to current domain
                    domain_parts = current_domain.split('.')
                    if len(domain_parts) >= 2:
                        base_domain = f"{domain_parts[-2]}.{domain_parts[-1]}"
                        if base_domain not in host_key:
                            continue
                
                try:
                    # Convert Chrome cookie to Selenium format
                    selenium_cookie = {
                        'name': name,
                        'value': value,
                        'path': path,
                        'secure': bool(is_secure),
                        'httpOnly': bool(is_httponly)
                    }
                    
                    # Set domain - handle both .domain.com and domain.com formats
                    if host_key.startswith('.'):
                        selenium_cookie['domain'] = host_key  # Keep the dot for wildcard cookies
                    else:
                        selenium_cookie['domain'] = host_key
                    
                    # Add expiry if not session cookie
                    if expires_utc > 0:
                        # Chrome stores in microseconds since 1601, convert to seconds since 1970
                        selenium_cookie['expiry'] = int((expires_utc - 11644473600000000) / 1000000)
                    
                    driver.add_cookie(selenium_cookie)
                    cookie_count += 1
                    
                except Exception as e:
                    # Some cookies might fail due to domain restrictions, that's ok
                    if "invalid cookie domain" not in str(e).lower():
                        console.print(f"[dim]Skipped cookie {name}: {str(e)[:50]}...[/dim]")
            
            console.print(f"[green]✓ Copied {cookie_count} cookies[/green]")
            conn.close()
            
        except Exception as e:
            console.print(f"[yellow]Warning: Could not copy all cookies: {e}[/yellow]")
        finally:
            if Path(temp_cookies).exists():
                Path(temp_cookies).unlink()
    
    def check_access(self, url: str) -> Tuple[bool, str]:
        """Check if we have access to the URL via Chrome profiles"""
        try:
            # First check for existing cookies
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            
            # Check if we have site-specific configuration
            site_config = self.site_registry.get_config(url)
            
            if site_config:
                # For all authentication types, check Chrome profiles
                console.print(f"[yellow]Checking Chrome profiles for {domain}...[/yellow]")
                
                # Check which Chrome profiles might have access
                profile_selector = ChromeProfileSelector()
                profiles = profile_selector.get_available_profiles()
                
                # Filter out temporary profile for reporting
                real_profiles = [p for p in profiles if p['path'] != 'temp']
                
                if real_profiles:
                    console.print(f"[cyan]Found {len(real_profiles)} Chrome profiles:[/cyan]")
                    for profile in real_profiles[:3]:  # Show first 3
                        console.print(f"  - {profile['name']}: {profile['email']}")
                    if len(real_profiles) > 3:
                        console.print(f"  ... and {len(real_profiles) - 3} more")
                    
                    return False, f"Chrome profiles found - select one when browser launches"
                else:
                    return False, "No Chrome profiles found - will use temporary profile"
            
            # For unknown sites, we can't check authentication
            console.print(f"[yellow]No configuration for {domain}[/yellow]")
            return False, "Unknown site - authentication may be required"
            
        except Exception as e:
            return False, f"Error checking Chrome profiles: {str(e)}"
    
    def _check_for_cookies(self, domain: str) -> bool:
        """Check if we have cookies for the given domain"""
        import sqlite3
        import shutil
        import tempfile
        import json
        from pathlib import Path
        
        profiles_with_cookies = []
        
        try:
            # Check all Chrome profiles
            chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
            
            for profile_dir in chrome_dir.glob("Profile*"):
                cookies_db = profile_dir / "Cookies"
                if cookies_db.exists():
                    # Copy cookies database to temp location
                    temp_cookies = tempfile.mktemp(suffix=".db")
                    try:
                        shutil.copy2(cookies_db, temp_cookies)
                        
                        conn = sqlite3.connect(temp_cookies)
                        cursor = conn.cursor()
                        
                        # Look for cookies from this domain
                        # Handle both exact domain and subdomain cookies (e.g., .domain.com)
                        # Also check parent domain cookies that should work for subdomains
                        
                        # Get parent domain(s) if this is a subdomain
                        domain_parts = domain.split('.')
                        parent_domains = []
                        if len(domain_parts) > 2:
                            # For app.sensortower.com, also check sensortower.com and .sensortower.com
                            for i in range(1, len(domain_parts) - 1):
                                parent = '.'.join(domain_parts[i:])
                                parent_domains.append(parent)
                                parent_domains.append(f'.{parent}')
                        
                        # Build query to check all relevant domains
                        query_parts = ["host_key = ?", "host_key = ?"]  # exact domain and .domain
                        params = [domain, f'.{domain}']
                        
                        # Add parent domains
                        for parent in parent_domains:
                            query_parts.append("host_key = ?")
                            params.append(parent)
                        
                        query = f"""
                            SELECT COUNT(*) 
                            FROM cookies 
                            WHERE {' OR '.join(query_parts)}
                        """
                        
                        cursor.execute(query, params)
                        
                        count = cursor.fetchone()[0]
                        conn.close()
                        
                        if count > 0:
                            # Get profile email if available
                            email = "Unknown"
                            prefs_file = profile_dir / "Preferences"
                            if prefs_file.exists():
                                try:
                                    with open(prefs_file) as f:
                                        data = json.load(f)
                                        email = data.get('account_info', [{}])[0].get('email', 'Unknown')
                                except:
                                    pass
                            
                            profiles_with_cookies.append({
                                'path': str(profile_dir),
                                'name': profile_dir.name,
                                'email': email,
                                'cookie_count': count
                            })
                            
                    except Exception as e:
                        console.print(f"[yellow]Error checking {profile_dir.name}: {e}[/yellow]")
                    finally:
                        if Path(temp_cookies).exists():
                            Path(temp_cookies).unlink()
            
            # Handle results
            if not profiles_with_cookies:
                # Show which domains were checked
                domain_parts = domain.split('.')
                checked_domains = [domain, f'.{domain}']
                if len(domain_parts) > 2:
                    for i in range(1, len(domain_parts) - 1):
                        parent = '.'.join(domain_parts[i:])
                        checked_domains.extend([parent, f'.{parent}'])
                
                console.print(f"[yellow]No cookies found for {domain} (also checked: {', '.join(set(checked_domains))}) in any Chrome profile[/yellow]")
                return False
            
            elif len(profiles_with_cookies) == 1:
                # Only one profile has cookies, use it
                profile = profiles_with_cookies[0]
                console.print(f"[green]Found {profile['cookie_count']} cookies in {profile['name']} ({profile['email']})[/green]")
                self.profile_with_cookies = profile['path']
                return True
            
            else:
                # Multiple profiles have cookies, let user choose
                console.print(f"[cyan]Found cookies for {domain} in multiple profiles:[/cyan]")
                for i, profile in enumerate(profiles_with_cookies):
                    console.print(f"  {i+1}. {profile['name']} - {profile['email']} ({profile['cookie_count']} cookies)")
                
                while True:
                    choice = input("\nSelect profile number (or 'skip' to continue without cookies): ").strip()
                    
                    if choice.lower() == 'skip':
                        return False
                    
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(profiles_with_cookies):
                            selected = profiles_with_cookies[idx]
                            console.print(f"[green]Using {selected['name']} ({selected['email']})[/green]")
                            self.profile_with_cookies = selected['path']
                            return True
                        else:
                            console.print("[red]Invalid selection. Please try again.[/red]")
                    except ValueError:
                        console.print("[red]Please enter a number or 'skip'[/red]")
            
        except Exception as e:
            console.print(f"[yellow]Could not check for cookies: {e}[/yellow]")
            return False
    
    def authenticate_google(self, return_to_url: Optional[str] = None) -> bool:
        """Improved authentication with better timeout handling"""
        console.print("[cyan]Starting authentication process...[/cyan]")
        
        # Ensure browser is initialized
        if not self.driver:
            try:
                self.driver = self._init_driver(headless=False)
            except Exception as e:
                console.print(f"[red]Could not start browser: {e}[/red]")
                return False
        
        # Create authentication manager
        auth_manager = AuthenticationManager(self.driver)
        
        # Get site config
        site_config = None
        if return_to_url:
            site_config = self.site_registry.get_config(return_to_url)
        
        # Define success check function
        def is_authenticated():
            try:
                current_url = self.driver.current_url
                
                # Generic check - not on a login page
                if any(indicator in current_url.lower() for indicator in ['login', 'signin', 'auth', 'sso']):
                    return False
                
                # Site-specific check
                if site_config:
                    return self.site_registry.is_authenticated(current_url, site_config)
                
                # If we're on the target URL, assume success
                if return_to_url and return_to_url in current_url:
                    return True
                    
                return True  # Assume authenticated if not on login page
                
            except:
                return False
        
        # First check if already authenticated
        if return_to_url:
            console.print(f"[cyan]Checking current authentication status...[/cyan]")
            self.driver.get(return_to_url)
            time.sleep(3)
            
            if is_authenticated():
                console.print("[green]✓ Already authenticated![/green]")
                self.authenticated = True
                
                # Authentication successful
                
                return True
        
        # Need to authenticate
        login_url = "https://accounts.google.com"
        if return_to_url and "sensortower.com" in return_to_url:
            login_url = "https://app.sensortower.com/users/sign_in"
        
        # Use the improved authentication manager
        success = auth_manager.interactive_authentication(
            login_url=login_url,
            success_check_fn=is_authenticated,
            timeout_seconds=300  # 5 minutes
        )
        
        if success:
            self.authenticated = True
            
            # Navigate back to target URL
            if return_to_url:
                console.print(f"[cyan]Returning to: {return_to_url}[/cyan]")
                self.driver.get(return_to_url)
                time.sleep(3)
            
            # Authentication successful
        
        return success
    
    def authenticate_google_old(self, return_to_url: Optional[str] = None) -> bool:
        """Handle Google OAuth authentication"""
        console.print("[cyan]Starting authentication process...[/cyan]")
        
        if not self.driver:
            try:
                self.driver = self._init_driver(headless=False)
            except Exception as e:
                console.print(f"[red]Could not start browser: {e}[/red]")
                console.print("[yellow]Please check that Chrome is installed and try again.[/yellow]")
                return False
        
        max_attempts = 3
        attempt = 1
        
        while attempt <= max_attempts:
            try:
                console.print(f"\n[cyan]Authentication attempt {attempt}/{max_attempts}[/cyan]")
                
                # Navigate to the target URL first to see if we're already authenticated
                if return_to_url:
                    console.print(f"[cyan]Checking authentication status...[/cyan]")
                    self.driver.get(return_to_url)
                    time.sleep(3)
                    
                    # Check if we're already authenticated
                    current_url = self.driver.current_url
                    if not any(auth_indicator in current_url.lower() for auth_indicator in ['login', 'signin', 'auth', 'sso']):
                        console.print("[green]✓ Already authenticated![/green]")
                        self.authenticated = True
                        return True
                
                # If not authenticated, go to Google sign-in
                console.print("[yellow]Authentication required. Opening sign-in page...[/yellow]")
                self.driver.get("https://accounts.google.com")
                
                # Give user options
                console.print("\n[yellow]Please sign in to your Google account in the browser.[/yellow]")
                console.print("[cyan]Options:[/cyan]")
                console.print("  - Press [green]Enter[/green] when you've successfully signed in")
                console.print("  - Type [yellow]'skip'[/yellow] and press Enter to skip authentication")
                console.print("  - Type [red]'quit'[/red] and press Enter to exit")
                
                user_input = input("\nYour choice: ").strip().lower()
                
                if user_input == 'quit':
                    console.print("[red]Exiting...[/red]")
                    return False
                elif user_input == 'skip':
                    console.print("[yellow]Skipping authentication. Some features may not work.[/yellow]")
                    return False
                else:
                    # User pressed Enter, check if authentication worked
                    if return_to_url:
                        console.print(f"[cyan]Returning to: {return_to_url}[/cyan]")
                        self.driver.get(return_to_url)
                        time.sleep(5)
                        
                        # Verify authentication
                        current_url = self.driver.current_url
                        if any(auth_indicator in current_url.lower() for auth_indicator in ['login', 'signin', 'auth', 'sso']):
                            console.print("[yellow]Still seeing login page. Authentication may have failed.[/yellow]")
                            if attempt < max_attempts:
                                retry = input("Try again? (y/n): ").strip().lower()
                                if retry != 'y':
                                    console.print("[yellow]Authentication skipped.[/yellow]")
                                    return False
                            attempt += 1
                            continue
                    
                    console.print("[green]✓ Authentication process completed[/green]")
                    self.authenticated = True
                    
                    # Authentication successful
                    
                    return True
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Authentication interrupted by user.[/yellow]")
                return False
            except Exception as e:
                console.print(f"[red]Error during authentication: {e}[/red]")
                if attempt < max_attempts:
                    retry = input("Try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        return False
                attempt += 1
        
        console.print("[red]Authentication failed after multiple attempts.[/red]")
        console.print("[yellow]You can still try to proceed, but some features may not work.[/yellow]")
        return False
    
    def parse_documentation(self, url: str, selectors: Optional[Dict[str, str]] = None) -> Dict:
        """Parse API documentation from a given URL"""
        if not self.driver:
            self.driver = self._init_driver()
        
        console.print(f"[cyan]Parsing documentation from: {url}[/cyan]")
        
        try:
            self.driver.get(url)
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, 10)
            
            # Use custom selectors if provided, otherwise use defaults
            if not selectors:
                selectors = self.config.get('selectors', {
                    'api_endpoint': '[data-testid="api-endpoint"], .api-endpoint, .endpoint',
                    'method': '[data-testid="http-method"], .http-method, .method',
                    'description': '[data-testid="api-description"], .api-description, .description',
                    'parameters': '[data-testid="parameters"], .parameters, .params',
                    'response': '[data-testid="response"], .response, .api-response',
                    'code_sample': 'pre, code, .code-sample'
                })
            
            # Wait for content to load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)  # Additional wait for dynamic content
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Extract API documentation
            api_docs = {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'endpoints': []
            }
            
            # Find all API endpoints
            for selector in selectors['api_endpoint'].split(', '):
                endpoints = soup.select(selector)
                if endpoints:
                    console.print(f"[green]Found {len(endpoints)} endpoints using selector: {selector}[/green]")
                    break
            else:
                console.print("[yellow]No endpoints found with default selectors[/yellow]")
                endpoints = []
            
            # Parse each endpoint
            for endpoint in endpoints:
                endpoint_data = self._parse_endpoint(endpoint, selectors)
                if endpoint_data:
                    api_docs['endpoints'].append(endpoint_data)
            
            return api_docs
            
        except Exception as e:
            console.print(f"[red]Error parsing documentation: {e}[/red]")
            return {'error': str(e)}
    
    def _parse_endpoint(self, element, selectors: Dict[str, str]) -> Optional[Dict]:
        """Parse individual API endpoint"""
        try:
            endpoint_data = {
                'endpoint': element.get_text(strip=True),
                'method': '',
                'description': '',
                'parameters': [],
                'response': '',
                'code_samples': []
            }
            
            # Get parent container for related elements
            parent = element.parent
            
            # Extract method
            for selector in selectors.get('method', '').split(', '):
                method = parent.select_one(selector)
                if method:
                    endpoint_data['method'] = method.get_text(strip=True)
                    break
            
            # Extract description
            for selector in selectors.get('description', '').split(', '):
                desc = parent.select_one(selector)
                if desc:
                    endpoint_data['description'] = desc.get_text(strip=True)
                    break
            
            # Extract parameters
            for selector in selectors.get('parameters', '').split(', '):
                params = parent.select(selector)
                if params:
                    endpoint_data['parameters'] = [p.get_text(strip=True) for p in params]
                    break
            
            # Extract code samples
            for selector in selectors.get('code_sample', '').split(', '):
                code_samples = parent.select(selector)
                if code_samples:
                    endpoint_data['code_samples'] = [c.get_text(strip=True) for c in code_samples]
                    break
            
            return endpoint_data
            
        except Exception as e:
            console.print(f"[yellow]Error parsing endpoint: {e}[/yellow]")
            return None
    
    def parse_multiple_pages(self, urls: List[str]) -> List[Dict]:
        """Parse multiple documentation pages"""
        results = []
        
        for url in urls:
            result = self.parse_documentation(url)
            results.append(result)
            time.sleep(2)  # Be respectful with requests
        
        return results
    
    def extract_function(self, url: str, function_name: str) -> Dict:
        """Extract a specific function/endpoint from documentation"""
        console.print(f"[cyan]Looking for function: {function_name}[/cyan]")
        
        if not self.driver:
            self.driver = self._init_driver()
        
        try:
            # Navigate to the URL
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            site_config = self.site_registry.get_config(url)
            
            # Normal navigation
            if self.driver.current_url != url:
                self.driver.get(url)
                
                # Copy cookies after navigating to the domain
                if hasattr(self, '_cookies_to_copy') and self._cookies_to_copy:
                    self._copy_cookies_to_driver(self.driver, self._cookies_to_copy)
                    # Refresh the page to use the new cookies
                    self.driver.refresh()
                    console.print("[cyan]Page refreshed with copied cookies[/cyan]")
                
                time.sleep(2)
            
            # Wait for page to load
            time.sleep(2)
            
            # Get page source
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Search for the function using multiple strategies
            function_data = None
            
            # Strategy 1: Look for exact text matches
            for element in soup.find_all(text=lambda text: function_name in text if text else False):
                parent = element.parent
                # Look for surrounding context
                container = parent
                for _ in range(5):  # Look up to 5 levels up
                    if container and self._looks_like_api_container(container):
                        function_data = self._extract_from_container(container, function_name)
                        if function_data:
                            break
                    container = container.parent if container else None
                if function_data:
                    break
            
            # Strategy 2: Look for common patterns
            if not function_data:
                # Common selectors for functions/methods
                function_selectors = [
                    f'[id*="{function_name}"]',
                    f'[data-name="{function_name}"]',
                    f'[class*="function"][class*="{function_name}"]',
                    f'[class*="method"][class*="{function_name}"]',
                    f'h2:contains("{function_name}")',
                    f'h3:contains("{function_name}")',
                    f'code:contains("{function_name}")'
                ]
                
                for selector in function_selectors:
                    try:
                        elements = soup.select(selector)
                        if elements:
                            for elem in elements:
                                container = elem.parent
                                function_data = self._extract_from_container(container, function_name)
                                if function_data:
                                    break
                            if function_data:
                                break
                    except:
                        continue
            
            if not function_data:
                console.print(f"[yellow]Could not find function '{function_name}' in documentation[/yellow]")
                return {'error': f'Function {function_name} not found'}
            
            return function_data
            
        except Exception as e:
            console.print(f"[red]Error extracting function: {e}[/red]")
            return {'error': str(e)}
    
    def _looks_like_api_container(self, element) -> bool:
        """Check if an element looks like it contains API documentation"""
        if not element:
            return False
        
        # Check class names
        if element.get('class'):
            classes = ' '.join(element.get('class')).lower()
            if any(keyword in classes for keyword in ['api', 'endpoint', 'method', 'function', 'operation']):
                return True
        
        # Check for common API documentation patterns
        text = element.get_text().lower()
        api_keywords = ['parameters', 'response', 'request', 'returns', 'arguments', 'example']
        keyword_count = sum(1 for keyword in api_keywords if keyword in text)
        
        return keyword_count >= 2
    
    def _extract_from_container(self, container, function_name: str) -> Dict:
        """Extract API documentation from a container element"""
        try:
            data = {
                'function': function_name,
                'description': '',
                'parameters': [],
                'returns': '',
                'examples': [],
                'raw_html': str(container)
            }
            
            # Extract description
            desc_patterns = ['summary', 'description', 'overview']
            for pattern in desc_patterns:
                desc_elem = container.find(class_=lambda c: c and pattern in c.lower() if c else False)
                if desc_elem:
                    data['description'] = desc_elem.get_text(strip=True)
                    break
            
            # If no description found, try first paragraph
            if not data['description']:
                p = container.find('p')
                if p:
                    data['description'] = p.get_text(strip=True)
            
            # Extract parameters
            param_section = container.find(['div', 'section', 'table'], class_=lambda c: c and 'param' in c.lower() if c else False)
            if param_section:
                params = param_section.find_all(['tr', 'li', 'div'])
                for param in params:
                    param_text = param.get_text(strip=True)
                    if param_text and param_text != 'Parameters':
                        data['parameters'].append(param_text)
            
            # Extract return value
            return_section = container.find(text=lambda t: t and 'return' in t.lower())
            if return_section:
                return_container = return_section.parent
                data['returns'] = return_container.get_text(strip=True)
            
            # Extract code examples
            code_blocks = container.find_all(['pre', 'code'])
            for code in code_blocks:
                code_text = code.get_text(strip=True)
                if code_text and len(code_text) > 10:  # Skip small snippets
                    data['examples'].append(code_text)
            
            return data
            
        except Exception as e:
            console.print(f"[yellow]Error extracting from container: {e}[/yellow]")
            return None
    
    def get_preview(self, function_data: Dict) -> str:
        """Generate a preview of the extracted function"""
        if 'error' in function_data:
            return f"Error: {function_data['error']}"
        
        preview = []
        preview.append(f"# {function_data.get('function', 'Unknown Function')}")
        
        if function_data.get('description'):
            preview.append(f"\n## Description\n{function_data['description']}")
        
        if function_data.get('parameters'):
            preview.append("\n## Parameters")
            for param in function_data['parameters'][:3]:  # Show first 3 params
                preview.append(f"- {param}")
            if len(function_data['parameters']) > 3:
                preview.append(f"... and {len(function_data['parameters']) - 3} more")
        
        if function_data.get('returns'):
            preview.append(f"\n## Returns\n{function_data['returns'][:200]}...")
        
        if function_data.get('examples'):
            preview.append(f"\n## Example")
            preview.append("```")
            preview.append(function_data['examples'][0][:300] + "..." if len(function_data['examples'][0]) > 300 else function_data['examples'][0])
            preview.append("```")
        
        return '\n'.join(preview)
    
    def close(self):
        """Close the webdriver and clean up"""
        if hasattr(self, 'chrome_manager') and self.chrome_manager:
            self.chrome_manager.quit()
        elif self.driver:
            self.driver.quit()
            self.driver = None
        
        # Clean up any profile copies
        if hasattr(self, '_selected_profile') and self._selected_profile:
            if '_copier' in self._selected_profile:
                self._selected_profile['_copier'].cleanup()