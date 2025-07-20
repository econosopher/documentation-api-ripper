"""
Persistent session management for avoiding repeated logins
"""
import os
import json
import pickle
import shutil
from pathlib import Path
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rich.console import Console
from rich.prompt import Prompt
import time

console = Console()

class PersistentSessionManager:
    """Manage persistent Chrome sessions to avoid repeated logins"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.path.expanduser("~/.api_ripper_sessions")
        self.sessions_dir = os.path.join(self.base_dir, "chrome_sessions")
        self.cookies_dir = os.path.join(self.base_dir, "cookies")
        
        # Create directories if they don't exist
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.cookies_dir, exist_ok=True)
        
    def list_sessions(self) -> List[str]:
        """List all saved sessions"""
        sessions = []
        if os.path.exists(self.sessions_dir):
            sessions = [d for d in os.listdir(self.sessions_dir) 
                       if os.path.isdir(os.path.join(self.sessions_dir, d))]
        return sessions
    
    def create_persistent_profile(self, name: str) -> str:
        """Create a persistent Chrome profile"""
        profile_path = os.path.join(self.sessions_dir, name)
        os.makedirs(profile_path, exist_ok=True)
        console.print(f"[green]Created persistent profile: {name}[/green]")
        return profile_path
    
    def get_chrome_options(self, session_name: str) -> Options:
        """Get Chrome options for a persistent session"""
        profile_path = os.path.join(self.sessions_dir, session_name)
        
        options = Options()
        options.add_argument(f'--user-data-dir={profile_path}')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        return options
    
    def save_cookies(self, driver: webdriver.Chrome, session_name: str):
        """Save cookies from current session"""
        cookies_file = os.path.join(self.cookies_dir, f"{session_name}.pkl")
        cookies = driver.get_cookies()
        
        with open(cookies_file, 'wb') as f:
            pickle.dump(cookies, f)
        
        console.print(f"[green]✓ Saved {len(cookies)} cookies for session '{session_name}'[/green]")
    
    def load_cookies(self, driver: webdriver.Chrome, session_name: str) -> bool:
        """Load cookies into current session"""
        cookies_file = os.path.join(self.cookies_dir, f"{session_name}.pkl")
        
        if not os.path.exists(cookies_file):
            return False
        
        try:
            with open(cookies_file, 'rb') as f:
                cookies = pickle.load(f)
            
            for cookie in cookies:
                # Handle domain mismatch
                if 'domain' in cookie:
                    current_domain = driver.current_url.split('/')[2]
                    cookie_domain = cookie['domain'].lstrip('.')
                    
                    # Only add cookie if domains match
                    if cookie_domain in current_domain or current_domain in cookie_domain:
                        try:
                            driver.add_cookie(cookie)
                        except Exception as e:
                            console.print(f"[dim]Skipped cookie: {cookie.get('name', 'unknown')}[/dim]")
            
            console.print(f"[green]✓ Loaded cookies for session '{session_name}'[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Failed to load cookies: {e}[/red]")
            return False
    
    def delete_session(self, session_name: str):
        """Delete a saved session"""
        profile_path = os.path.join(self.sessions_dir, session_name)
        cookies_file = os.path.join(self.cookies_dir, f"{session_name}.pkl")
        
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path)
        if os.path.exists(cookies_file):
            os.remove(cookies_file)
        
        console.print(f"[yellow]Deleted session: {session_name}[/yellow]")
    
    def interactive_session_selector(self) -> Optional[str]:
        """Interactive session selection"""
        sessions = self.list_sessions()
        
        console.print("\n[cyan]Available Sessions:[/cyan]")
        console.print("0. Create new session")
        
        for i, session in enumerate(sessions, 1):
            profile_path = os.path.join(self.sessions_dir, session)
            size = sum(os.path.getsize(os.path.join(dirpath, filename))
                      for dirpath, dirnames, filenames in os.walk(profile_path)
                      for filename in filenames) / (1024 * 1024)  # MB
            
            console.print(f"{i}. {session} [dim]({size:.1f} MB)[/dim]")
        
        choice = Prompt.ask("\n[cyan]Select session (0 to create new)[/cyan]", 
                           choices=[str(i) for i in range(len(sessions) + 1)])
        
        if choice == "0":
            name = Prompt.ask("[cyan]Enter name for new session[/cyan]")
            self.create_persistent_profile(name)
            return name
        else:
            return sessions[int(choice) - 1]


class PersistentChromeDriver:
    """Wrapper for Chrome driver with persistent session"""
    
    def __init__(self, session_manager: PersistentSessionManager):
        self.session_manager = session_manager
        self.driver = None
        self.session_name = None
        
    def start(self, session_name: Optional[str] = None) -> webdriver.Chrome:
        """Start Chrome with persistent session"""
        if not session_name:
            session_name = self.session_manager.interactive_session_selector()
        
        self.session_name = session_name
        
        console.print(f"\n[yellow]Starting Chrome with session: {session_name}[/yellow]")
        
        # Get options for persistent session
        options = self.session_manager.get_chrome_options(session_name)
        
        # Create driver
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Disable webdriver detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        console.print("[green]✓ Chrome started with persistent session[/green]")
        return self.driver
    
    def navigate_and_check_auth(self, url: str) -> bool:
        """Navigate to URL and check if we're already authenticated"""
        console.print(f"[yellow]Navigating to {url}...[/yellow]")
        self.driver.get(url)
        time.sleep(2)
        
        # Check if we're on a login page
        current_url = self.driver.current_url.lower()
        login_indicators = ['login', 'signin', 'sign_in', 'auth', 'sso']
        
        is_login_page = any(indicator in current_url for indicator in login_indicators)
        
        if is_login_page:
            console.print("[yellow]⚠ Not authenticated - login required[/yellow]")
            return False
        else:
            console.print("[green]✓ Already authenticated![/green]")
            return True
    
    def save_session(self):
        """Save current session cookies"""
        if self.driver and self.session_name:
            self.session_manager.save_cookies(self.driver, self.session_name)
    
    def quit(self):
        """Quit driver and save session"""
        if self.driver:
            self.save_session()
            self.driver.quit()
            console.print(f"[green]✓ Session '{self.session_name}' saved[/green]")