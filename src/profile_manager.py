"""
Chrome Profile Manager - Use persistent profiles to maintain login sessions
"""
import os
import shutil
from pathlib import Path
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class ChromeProfileManager:
    """Manage Chrome profiles for persistent authentication"""
    
    def __init__(self):
        # Default Chrome profile locations
        self.chrome_user_data = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        
        # Our app's persistent profile directory
        self.app_profiles_dir = os.path.expanduser("~/.api_ripper/chrome_profiles")
        os.makedirs(self.app_profiles_dir, exist_ok=True)
        
    def list_chrome_profiles(self):
        """List available Chrome profiles"""
        profiles = []
        
        # Check default profile
        if os.path.exists(os.path.join(self.chrome_user_data, "Default")):
            profiles.append(("Default Chrome Profile", self.chrome_user_data, "Default"))
        
        # Check other Chrome profiles
        if os.path.exists(self.chrome_user_data):
            for item in os.listdir(self.chrome_user_data):
                if item.startswith("Profile ") and os.path.isdir(os.path.join(self.chrome_user_data, item)):
                    profiles.append((f"Chrome {item}", self.chrome_user_data, item))
        
        return profiles
    
    def list_app_profiles(self):
        """List our app's persistent profiles"""
        profiles = []
        
        if os.path.exists(self.app_profiles_dir):
            for item in os.listdir(self.app_profiles_dir):
                profile_path = os.path.join(self.app_profiles_dir, item)
                if os.path.isdir(profile_path):
                    profiles.append((f"API Ripper: {item}", profile_path, None))
        
        return profiles
    
    def create_app_profile(self, name: str) -> str:
        """Create a new persistent profile for our app"""
        profile_path = os.path.join(self.app_profiles_dir, name)
        os.makedirs(profile_path, exist_ok=True)
        console.print(f"[green]✓ Created persistent profile: {name}[/green]")
        return profile_path
    
    def select_profile(self):
        """Interactive profile selection"""
        console.print("\n[bold cyan]Chrome Profile Selection[/bold cyan]")
        console.print("[dim]Using a persistent profile will maintain your login sessions[/dim]\n")
        
        all_profiles = []
        
        # Add option to create new persistent profile
        console.print("[yellow]0.[/yellow] Create new persistent profile (Recommended)")
        
        # List app profiles
        app_profiles = self.list_app_profiles()
        for i, (name, path, _) in enumerate(app_profiles, 1):
            all_profiles.append((name, path, None))
            console.print(f"[green]{i}.[/green] {name}")
        
        # List Chrome profiles
        chrome_profiles = self.list_chrome_profiles()
        start_idx = len(app_profiles) + 1
        for i, (name, base_path, profile_name) in enumerate(chrome_profiles, start_idx):
            all_profiles.append((name, base_path, profile_name))
            console.print(f"[blue]{i}.[/blue] {name} [dim](uses your actual Chrome profile)[/dim]")
        
        # Add temporary option
        temp_idx = len(all_profiles) + 1
        console.print(f"[red]{temp_idx}.[/red] Temporary session (will need to login each time)")
        
        choice = Prompt.ask(
            f"\n[cyan]Select profile (0-{temp_idx})[/cyan]",
            default="0"
        )
        
        try:
            choice_int = int(choice)
            
            if choice_int == 0:
                # Create new persistent profile
                name = Prompt.ask("[cyan]Enter profile name[/cyan]", default="sensortower")
                profile_path = self.create_app_profile(name)
                return profile_path, None
                
            elif 1 <= choice_int <= len(all_profiles):
                # Use existing profile
                name, base_path, profile_name = all_profiles[choice_int - 1]
                return base_path, profile_name
                
            elif choice_int == temp_idx:
                # Temporary session
                return None, None
                
        except ValueError:
            pass
        
        console.print("[yellow]Invalid choice, using temporary session[/yellow]")
        return None, None
    
    def create_driver(self, profile_path: Optional[str] = None, 
                     profile_name: Optional[str] = None) -> webdriver.Chrome:
        """Create Chrome driver with specified profile"""
        options = Options()
        
        if profile_path:
            # Use persistent profile
            options.add_argument(f'--user-data-dir={profile_path}')
            
            if profile_name:
                # Specific Chrome profile within user data dir
                options.add_argument(f'--profile-directory={profile_name}')
            
            console.print(f"[green]Using persistent profile: {profile_path}[/green]")
        else:
            # Temporary profile
            import tempfile
            temp_dir = tempfile.mkdtemp(prefix="api_ripper_temp_")
            options.add_argument(f'--user-data-dir={temp_dir}')
            console.print("[yellow]Using temporary profile (login required)[/yellow]")
        
        # Standard options
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Create driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Disable webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver


def create_persistent_driver():
    """Helper function to create a driver with persistent profile"""
    manager = ChromeProfileManager()
    profile_path, profile_name = manager.select_profile()
    return manager.create_driver(profile_path, profile_name)