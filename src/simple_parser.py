import time
from typing import Dict, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from rich.console import Console
from pathlib import Path

console = Console()


class SimpleAPIParser:
    def __init__(self, profile_name: str = "Profile 11"):
        self.driver = None
        self.profile_name = profile_name
        
    def _init_driver(self) -> webdriver.Chrome:
        """Initialize Chrome with your actual profile"""
        options = webdriver.ChromeOptions()
        
        # Use your actual Chrome profile
        chrome_profile = Path.home() / "Library/Application Support/Google/Chrome"
        
        console.print(f"[cyan]Using Chrome profile: {self.profile_name}[/cyan]")
        console.print("[yellow]Important: Close Chrome completely before running![/yellow]")
        
        # Use specified profile
        options.add_argument(f'user-data-dir={chrome_profile}')
        options.add_argument(f'profile-directory={self.profile_name}')
        
        # Minimal options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def extract_function(self, url: str, function_name: str) -> Dict:
        """Simple extraction without authentication checks"""
        console.print(f"[cyan]Opening {url}...[/cyan]")
        
        if not self.driver:
            self.driver = self._init_driver()
        
        self.driver.get(url)
        time.sleep(5)  # Wait for page to load
        
        # Get page source
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        
        # Look for the function
        console.print(f"[cyan]Searching for '{function_name}'...[/cyan]")
        
        # Simple search for the function text
        function_data = {
            'function': function_name,
            'url': url,
            'content': '',
            'found': False
        }
        
        # Find all elements containing the function name
        for element in soup.find_all(text=lambda text: function_name in text if text else False):
            # Get parent container
            container = element.parent
            for _ in range(5):  # Look up to 5 levels
                if container and container.name in ['div', 'section', 'article']:
                    content = container.get_text(separator='\n', strip=True)
                    if len(content) > 100:  # Meaningful content
                        function_data['content'] = content
                        function_data['found'] = True
                        function_data['html'] = str(container)
                        break
                container = container.parent if container else None
            if function_data['found']:
                break
        
        # Also try finding by ID or class
        if not function_data['found']:
            for selector in [f'#{function_name}', f'.{function_name}', f'[data-name="{function_name}"]']:
                try:
                    element = soup.select_one(selector)
                    if element:
                        function_data['content'] = element.get_text(separator='\n', strip=True)
                        function_data['found'] = True
                        function_data['html'] = str(element)
                        break
                except:
                    continue
        
        return function_data
    
    def close(self):
        if self.driver:
            self.driver.quit()