"""
Chrome profile selector for browser initialization
"""
from pathlib import Path
from typing import List, Optional, Dict
import json
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class ChromeProfileSelector:
    """Handles Chrome profile selection for browser launch"""
    
    def __init__(self):
        self.chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
        
    def get_available_profiles(self) -> List[Dict[str, str]]:
        """Get list of available Chrome profiles with their info"""
        profiles = []
        
        # Always add option for temporary profile
        profiles.append({
            'name': 'Temporary',
            'path': 'temp',
            'email': 'Clean temporary profile',
            'number': '0'
        })
        
        # Check Default profile
        default_dir = self.chrome_dir / "Default"
        if default_dir.exists():
            email = self._get_profile_email(default_dir)
            profiles.append({
                'name': 'Default',
                'path': str(default_dir),
                'email': email,
                'number': '1'
            })
        
        # Check numbered profiles
        profile_num = 2
        for profile_dir in sorted(self.chrome_dir.glob("Profile *")):
            if profile_dir.is_dir():
                email = self._get_profile_email(profile_dir)
                profiles.append({
                    'name': profile_dir.name,
                    'path': str(profile_dir),
                    'email': email,
                    'number': str(profile_num)
                })
                profile_num += 1
                
        return profiles
    
    def _get_profile_email(self, profile_dir: Path) -> str:
        """Extract email from Chrome profile preferences"""
        prefs_file = profile_dir / "Preferences"
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r') as f:
                    data = json.load(f)
                    accounts = data.get('account_info', [])
                    if accounts:
                        return accounts[0].get('email', 'No email')
            except:
                pass
        return 'No email'
    
    def select_profile(self, auto_select: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        Let user select a Chrome profile
        
        Args:
            auto_select: Profile name to auto-select (e.g., "Profile 15")
            
        Returns:
            Selected profile info or None if cancelled
        """
        profiles = self.get_available_profiles()
        
        if not profiles:
            console.print("[red]No Chrome profiles found![/red]")
            return None
        
        # Auto-select if specified
        if auto_select:
            for profile in profiles:
                if profile['name'].lower() == auto_select.lower():
                    console.print(f"[green]Auto-selected: {profile['name']} ({profile['email']})[/green]")
                    return profile
        
        # Display available profiles
        console.print("\n[bold cyan]Available Chrome Profiles:[/bold cyan]")
        
        table = Table(show_header=True)
        table.add_column("#", style="cyan", width=3)
        table.add_column("Profile", style="green")
        table.add_column("Email/Description", style="yellow")
        
        for profile in profiles:
            table.add_row(
                profile['number'],
                profile['name'],
                profile['email']
            )
        
        console.print(table)
        
        # Get user selection
        console.print("\n[yellow]Note: Using an existing profile requires Chrome to be closed![/yellow]")
        
        while True:
            choice = Prompt.ask(
                "\n[cyan]Select profile number (or 'q' to quit)[/cyan]",
                default="0"
            )
            
            if choice.lower() == 'q':
                return None
                
            # Find selected profile
            for profile in profiles:
                if profile['number'] == choice:
                    console.print(f"\n[green]Selected: {profile['name']} ({profile['email']})[/green]")
                    
                    if profile['path'] != 'temp' and profile['name'] != 'Temporary':
                        # Check if Chrome is running
                        import subprocess
                        chrome_running = False
                        try:
                            result = subprocess.run(['pgrep', '-x', 'Google Chrome'], capture_output=True, text=True)
                            chrome_running = result.returncode == 0
                        except:
                            pass
                        
                        if chrome_running:
                            console.print("\n[red]⚠️  Chrome is currently running![/red]")
                            console.print("[yellow]This can cause conflicts when using an existing profile.[/yellow]")
                            console.print("\n[cyan]Options:[/cyan]")
                            console.print("1. [green]Use Safe Mode[/green] (recommended) - Creates a copy of the profile")
                            console.print("2. [yellow]Continue anyway[/yellow] - May fail if profile is in use")
                            console.print("3. [red]Go back[/red] - Choose a different profile")
                            
                            mode_choice = Prompt.ask("\n[cyan]Select option (1-3)[/cyan]", default="1")
                            
                            if mode_choice == "1":
                                # Enable safe mode
                                profile['safe_mode'] = True
                                console.print("\n[green]✓ Safe mode enabled - will use a copy of the profile[/green]")
                            elif mode_choice == "2":
                                # Continue without safe mode
                                console.print("\n[yellow]⚠️  Continuing without safe mode...[/yellow]")
                            else:
                                # Go back
                                continue
                        else:
                            console.print("\n[green]✓ Chrome appears to be closed[/green]")
                            console.print("[cyan]Using profile directly (recommended when Chrome is closed)[/cyan]")
                            
                    return profile
            
            console.print("[red]Invalid selection. Please try again.[/red]")
    
    def get_chrome_options(self, profile: Dict[str, str]):
        """Get Chrome options for the selected profile"""
        from selenium import webdriver
        
        options = webdriver.ChromeOptions()
        
        # Common options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable some features that might trigger profile verification
        options.add_argument('--disable-features=ChromeWhatsNewUI')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-popup-blocking')
        
        # Profile-specific options
        if profile['path'] == 'temp':
            # Use temporary profile
            import os
            temp_dir = os.path.abspath('./chrome_temp_profile')
            options.add_argument(f'user-data-dir={temp_dir}')
            console.print("[cyan]Using temporary Chrome profile[/cyan]")
        elif profile.get('safe_mode', False):
            # Use safe mode - copy profile to avoid conflicts
            from .profile_copier import ChromeProfileCopier
            copier = ChromeProfileCopier()
            copied_profile_path = copier.create_profile_copy(profile['path'])
            options.add_argument(f'user-data-dir={copied_profile_path}')
            console.print(f"[cyan]Using safe copy of Chrome {profile['name']}[/cyan]")
            console.print("[dim]This avoids conflicts with running Chrome instances[/dim]")
            # Store copier for cleanup
            profile['_copier'] = copier
        else:
            # Use existing profile directly (may conflict if Chrome is running)
            profile_path = Path(profile['path'])
            if profile['name'] == 'Default':
                # For default profile, use the Chrome directory as user-data-dir
                options.add_argument(f'user-data-dir={self.chrome_dir}')
                # No need to specify profile-directory for Default
            else:
                # For numbered profiles
                options.add_argument(f'user-data-dir={self.chrome_dir}')
                options.add_argument(f'profile-directory={profile["name"]}')
            
            console.print(f"[cyan]Using Chrome {profile['name']} directly[/cyan]")
        
        return options