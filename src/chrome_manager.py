"""
Chrome instance manager with unique user-data-dir and proper cleanup
"""
import os
import tempfile
import shutil
import atexit
import signal
import time
from typing import Optional, Dict, Set
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console

console = Console()

class ChromeManager:
    """Manages Chrome instances with unique directories and cleanup"""
    
    # Class variable to track all temporary directories
    _temp_dirs: Set[str] = set()
    _cleanup_registered = False
    
    def __init__(self):
        self.temp_dir: Optional[str] = None
        self.driver: Optional[webdriver.Chrome] = None
        self._register_cleanup()
    
    @classmethod
    def _register_cleanup(cls):
        """Register cleanup handlers once"""
        if not cls._cleanup_registered:
            atexit.register(cls._cleanup_all)
            signal.signal(signal.SIGINT, cls._signal_handler)
            signal.signal(signal.SIGTERM, cls._signal_handler)
            cls._cleanup_registered = True
    
    @classmethod
    def _signal_handler(cls, signum, frame):
        """Handle termination signals"""
        console.print("\n[yellow]Received termination signal. Cleaning up...[/yellow]")
        cls._cleanup_all()
        exit(0)
    
    @classmethod
    def _cleanup_all(cls):
        """Clean up all temporary directories"""
        for temp_dir in list(cls._temp_dirs):
            cls._cleanup_dir(temp_dir)
    
    @classmethod
    def _cleanup_dir(cls, temp_dir: str):
        """Clean up a specific temporary directory"""
        if temp_dir and os.path.exists(temp_dir):
            try:
                # Give Chrome time to release files
                time.sleep(0.5)
                shutil.rmtree(temp_dir, ignore_errors=True)
                cls._temp_dirs.discard(temp_dir)
                console.print(f"[dim]Cleaned up: {temp_dir}[/dim]")
            except Exception as e:
                console.print(f"[red]Failed to clean up {temp_dir}: {e}[/red]")
    
    def create_unique_profile(self, base_profile: Optional[str] = None) -> str:
        """Create a unique temporary profile directory"""
        # Create unique temp directory with timestamp
        timestamp = int(time.time() * 1000)
        temp_dir = tempfile.mkdtemp(prefix=f"chrome_profile_{timestamp}_")
        
        # Track for cleanup
        self._temp_dirs.add(temp_dir)
        self.temp_dir = temp_dir
        
        # If base profile provided, copy it
        if base_profile and os.path.exists(base_profile):
            try:
                # Copy only essential files
                essential_dirs = ['Default', 'Local State']
                for item in essential_dirs:
                    src = os.path.join(base_profile, item)
                    if os.path.exists(src):
                        dst = os.path.join(temp_dir, item)
                        if os.path.isdir(src):
                            shutil.copytree(src, dst, ignore_errors=True)
                        else:
                            shutil.copy2(src, dst)
                
                console.print(f"[green]Created profile copy at: {temp_dir}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not copy profile: {e}[/yellow]")
        else:
            console.print(f"[green]Created fresh profile at: {temp_dir}[/green]")
        
        return temp_dir
    
    def get_chrome_options(self, profile_dir: str, headless: bool = False) -> webdriver.ChromeOptions:
        """Get Chrome options with unique user-data-dir"""
        options = webdriver.ChromeOptions()
        
        # Use the unique profile directory
        options.add_argument(f'--user-data-dir={profile_dir}')
        
        # Standard options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Prevent Chrome from checking if it's default browser
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        
        # Disable crash reporter
        options.add_argument('--disable-crash-reporter')
        options.add_argument('--disable-background-timer-throttling')
        
        if headless:
            options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
        
        return options
    
    def create_driver(self, base_profile: Optional[str] = None, headless: bool = False) -> webdriver.Chrome:
        """Create a Chrome driver with unique profile"""
        # Create unique profile
        profile_dir = self.create_unique_profile(base_profile)
        
        # Get options
        options = self.get_chrome_options(profile_dir, headless)
        
        try:
            # Create driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Disable webdriver detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return self.driver
            
        except Exception as e:
            # Clean up on failure
            self._cleanup_dir(profile_dir)
            raise Exception(f"Failed to create Chrome driver: {e}")
    
    def quit(self):
        """Quit driver and clean up"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        if self.temp_dir:
            self._cleanup_dir(self.temp_dir)
            self.temp_dir = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.quit()
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.quit()