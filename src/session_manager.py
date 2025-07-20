"""
Session manager for maintaining authenticated browser sessions
"""
import pickle
import os
from pathlib import Path
from typing import Optional
from selenium import webdriver
from rich.console import Console

console = Console()

class SessionManager:
    """Manages persistent browser sessions to maintain authentication"""
    
    def __init__(self, session_dir: str = "./sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        
    def save_session(self, driver: webdriver.Chrome, site_name: str):
        """Save browser session cookies and local storage"""
        session_file = self.session_dir / f"{site_name}_session.pkl"
        
        try:
            session_data = {
                'cookies': driver.get_cookies(),
                'url': driver.current_url,
                # Note: localStorage can't be easily saved/restored across sessions
            }
            
            with open(session_file, 'wb') as f:
                pickle.dump(session_data, f)
                
            console.print(f"[green]✓ Session saved for {site_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[yellow]Could not save session: {e}[/yellow]")
            return False
    
    def load_session(self, driver: webdriver.Chrome, site_name: str) -> bool:
        """Load saved session into browser"""
        session_file = self.session_dir / f"{site_name}_session.pkl"
        
        if not session_file.exists():
            return False
            
        try:
            with open(session_file, 'rb') as f:
                session_data = pickle.load(f)
            
            # Navigate to the domain first (required for setting cookies)
            driver.get(session_data['url'])
            
            # Clear existing cookies
            driver.delete_all_cookies()
            
            # Add saved cookies
            for cookie in session_data['cookies']:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    # Some cookies might fail, that's ok
                    pass
            
            # Refresh to use new cookies
            driver.refresh()
            
            console.print(f"[green]✓ Session restored for {site_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[yellow]Could not restore session: {e}[/yellow]")
            return False
    
    def has_session(self, site_name: str) -> bool:
        """Check if we have a saved session for this site"""
        session_file = self.session_dir / f"{site_name}_session.pkl"
        return session_file.exists()
    
    def clear_session(self, site_name: str):
        """Clear saved session for a site"""
        session_file = self.session_dir / f"{site_name}_session.pkl"
        if session_file.exists():
            session_file.unlink()
            console.print(f"[yellow]Cleared session for {site_name}[/yellow]")