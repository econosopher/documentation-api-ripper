"""
Google OAuth authentication manager with token storage
"""
import os
import json
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from rich.console import Console

console = Console()

class OAuthManager:
    """Manages Google OAuth authentication and token storage"""
    
    def __init__(self, token_dir: str = "./oauth_tokens"):
        self.token_dir = Path(token_dir)
        self.token_dir.mkdir(exist_ok=True)
        
    def get_stored_credentials(self, site: str) -> Optional[Credentials]:
        """Get stored OAuth credentials for a site"""
        token_file = self.token_dir / f"{site}_token.json"
        
        if not token_file.exists():
            return None
            
        try:
            creds = Credentials.from_authorized_user_file(str(token_file))
            
            # Check if token is expired
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.save_credentials(site, creds)
                    console.print(f"[green]✓ Refreshed expired token for {site}[/green]")
                except RefreshError:
                    console.print(f"[yellow]Token refresh failed for {site}[/yellow]")
                    return None
                    
            return creds
            
        except Exception as e:
            console.print(f"[yellow]Could not load credentials: {e}[/yellow]")
            return None
    
    def save_credentials(self, site: str, creds: Credentials):
        """Save OAuth credentials for a site"""
        token_file = self.token_dir / f"{site}_token.json"
        
        # Convert credentials to JSON format
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes,
            'expiry': creds.expiry.isoformat() if creds.expiry else None
        }
        
        with open(token_file, 'w') as f:
            json.dump(token_data, f, indent=2)
            
        console.print(f"[green]✓ Saved authentication for {site}[/green]")
    
    def has_valid_token(self, site: str) -> bool:
        """Check if we have a valid token for a site"""
        creds = self.get_stored_credentials(site)
        return creds is not None and creds.valid
    
    def clear_token(self, site: str):
        """Clear stored token for a site"""
        token_file = self.token_dir / f"{site}_token.json"
        if token_file.exists():
            token_file.unlink()
            console.print(f"[yellow]Cleared token for {site}[/yellow]")


class BrowserSessionManager:
    """
    Generic handler for capturing and restoring browser sessions
    Works for any site that uses OAuth or other browser-based authentication
    """
    
    def __init__(self, oauth_manager: OAuthManager):
        self.oauth_manager = oauth_manager
        
    def capture_session_from_browser(self, driver, site_name: str):
        """
        Capture authentication state from browser after successful login
        This includes cookies, localStorage, and sessionStorage
        """
        session_file = self.oauth_manager.token_dir / f"{site_name}_session.json"
        
        try:
            # Get all cookies
            cookies = driver.get_cookies()
            
            # Try to get localStorage (might fail on some sites)
            try:
                local_storage = driver.execute_script(
                    "return Object.entries(localStorage).reduce((acc, [k, v]) => ({...acc, [k]: v}), {})"
                )
            except:
                local_storage = {}
            
            # Try to get sessionStorage
            try:
                session_storage = driver.execute_script(
                    "return Object.entries(sessionStorage).reduce((acc, [k, v]) => ({...acc, [k]: v}), {})"
                )
            except:
                session_storage = {}
            
            session_data = {
                'url': driver.current_url,
                'cookies': cookies,
                'local_storage': local_storage,
                'session_storage': session_storage,
                'captured_at': datetime.now().isoformat()
            }
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            console.print(f"[green]✓ Captured session for {site_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Failed to capture session: {e}[/red]")
            return False
    
    def restore_session_to_browser(self, driver, site_name: str) -> bool:
        """Restore captured session to browser"""
        session_file = self.oauth_manager.token_dir / f"{site_name}_session.json"
        
        if not session_file.exists():
            return False
            
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is recent (within 7 days)
            captured_at = datetime.fromisoformat(session_data['captured_at'])
            if datetime.now() - captured_at > timedelta(days=7):
                console.print("[yellow]Session is older than 7 days, may be expired[/yellow]")
            
            # Navigate to the site first
            driver.get(session_data['url'])
            
            # Clear and set cookies
            driver.delete_all_cookies()
            for cookie in session_data['cookies']:
                try:
                    # Remove expiry if it's in the past
                    if 'expiry' in cookie:
                        if cookie['expiry'] < datetime.now().timestamp():
                            del cookie['expiry']
                    driver.add_cookie(cookie)
                except Exception as e:
                    pass  # Some cookies might fail
            
            # Restore localStorage
            if session_data.get('local_storage'):
                for key, value in session_data['local_storage'].items():
                    try:
                        driver.execute_script(f"localStorage.setItem('{key}', '{value}')")
                    except:
                        pass
            
            # Restore sessionStorage
            if session_data.get('session_storage'):
                for key, value in session_data['session_storage'].items():
                    try:
                        driver.execute_script(f"sessionStorage.setItem('{key}', '{value}')")
                    except:
                        pass
            
            # Refresh the page to use the restored session
            driver.refresh()
            
            console.print(f"[green]✓ Restored session for {site_name}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Failed to restore session: {e}[/red]")
            return False
    
    def has_stored_session(self, site_name: str) -> bool:
        """Check if we have a stored session"""
        session_file = self.oauth_manager.token_dir / f"{site_name}_session.json"
        if not session_file.exists():
            return False
            
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Check if session is recent
            captured_at = datetime.fromisoformat(session_data['captured_at'])
            is_recent = datetime.now() - captured_at < timedelta(days=7)
            
            return is_recent
            
        except:
            return False