#!/usr/bin/env python3
"""
Test script that ONLY checks for cookies and displays them
Does NOT launch any browser
"""
import sqlite3
import shutil
import tempfile
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def check_all_cookies():
    """Check all Chrome profiles for cookies from various API doc sites"""
    
    # Common API documentation domains
    domains_to_check = [
        "sensortower.com",
        "app.sensortower.com", 
        "stripe.com",
        "docs.stripe.com",
        "github.com",
        "api.github.com",
        "openai.com",
        "platform.openai.com",
        "aws.amazon.com",
        "docs.aws.amazon.com"
    ]
    
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    results = {}
    
    console.print(Panel("[bold cyan]Cookie Scanner - Checking Chrome Profiles[/bold cyan]", expand=False))
    console.print("\n[yellow]Note: This only reads cookies, it does NOT launch any browser.[/yellow]\n")
    
    # Check each profile
    for profile_dir in sorted(chrome_dir.glob("Profile*")):
        cookies_db = profile_dir / "Cookies"
        if not cookies_db.exists():
            continue
            
        profile_name = profile_dir.name
        profile_info = {
            'email': 'Unknown',
            'cookies': {}
        }
        
        # Get email from preferences
        prefs_file = profile_dir / "Preferences"
        if prefs_file.exists():
            try:
                with open(prefs_file) as f:
                    data = json.load(f)
                    accounts = data.get('account_info', [])
                    if accounts:
                        profile_info['email'] = accounts[0].get('email', 'Unknown')
            except:
                pass
        
        # Copy cookies database to temp location
        temp_cookies = tempfile.mktemp(suffix=".db")
        try:
            shutil.copy2(cookies_db, temp_cookies)
            
            conn = sqlite3.connect(temp_cookies)
            cursor = conn.cursor()
            
            # Check each domain
            for domain in domains_to_check:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM cookies 
                    WHERE host_key = ? 
                       OR host_key = ?
                       OR host_key LIKE ?
                """, (domain, f'.{domain}', f'%.{domain}'))
                
                count = cursor.fetchone()[0]
                if count > 0:
                    profile_info['cookies'][domain] = count
            
            conn.close()
            
            # Only include profiles that have relevant cookies
            if profile_info['cookies']:
                results[profile_name] = profile_info
                
        except Exception as e:
            console.print(f"[red]Error reading {profile_name}: {e}[/red]")
        finally:
            if Path(temp_cookies).exists():
                Path(temp_cookies).unlink()
    
    # Display results
    if results:
        console.print("[bold green]Found cookies in the following Chrome profiles:[/bold green]\n")
        
        for profile_name, info in results.items():
            table = Table(title=f"{profile_name} ({info['email']})", show_header=True)
            table.add_column("Domain", style="cyan")
            table.add_column("Cookie Count", style="green")
            
            for domain, count in sorted(info['cookies'].items()):
                table.add_row(domain, str(count))
            
            console.print(table)
            console.print()
    else:
        console.print("[yellow]No cookies found for API documentation sites in any Chrome profile.[/yellow]")
    
    # Show instructions
    console.print(Panel(
        "[bold]To use these cookies:[/bold]\n\n"
        "1. The app will automatically detect and use cookies when you run:\n"
        "   [cyan]python src/main.py <url> <function>[/cyan]\n\n"
        "2. If multiple profiles have cookies, you'll be prompted to choose\n\n"
        "3. If no cookies exist, you'll be asked if you want to authenticate\n\n"
        "[yellow]The browser will ONLY launch if:[/yellow]\n"
        "- No cookies are found AND\n" 
        "- You explicitly choose to authenticate",
        title="[bold]How Cookie Authentication Works[/bold]",
        expand=False
    ))

def test_specific_url(url: str):
    """Test if we have cookies for a specific URL"""
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    
    console.print(f"\n[cyan]Checking cookies for: {domain}[/cyan]")
    
    from src.parser import APIDocParser
    parser = APIDocParser()
    
    has_access, message = parser.check_access(url)
    
    if has_access:
        console.print(f"[green]✓ {message}[/green]")
        console.print("[green]Ready to extract documentation without browser launch![/green]")
    else:
        console.print(f"[yellow]✗ {message}[/yellow]")
        console.print("[yellow]Browser would need to be launched for authentication[/yellow]")

if __name__ == "__main__":
    # Check all cookies
    check_all_cookies()
    
    # Test a specific URL
    console.print("\n" + "="*60 + "\n")
    test_url = "https://app.sensortower.com/api/docs/app_analysis"
    console.print(f"[bold]Testing specific URL:[/bold] {test_url}")
    test_specific_url(test_url)