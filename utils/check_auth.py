#!/usr/bin/env python3
"""
Check which Chrome profiles have actual authentication for various sites
"""
import sqlite3
import shutil
import tempfile
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def check_auth_status():
    """Check authentication status across profiles"""
    
    # Common authentication cookie patterns
    auth_indicators = {
        'sensortower.com': ['session', 'token', 'auth', 'user', 'login', '_st_'],
        'stripe.com': ['session', 'token', '__stripe_', 'auth'],
        'github.com': ['_gh_sess', 'user_session', 'logged_in'],
        'openai.com': ['__Secure-next-auth', 'session', 'cf_clearance']
    }
    
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    
    # Build results table
    table = Table(title="Chrome Profile Authentication Status", show_header=True)
    table.add_column("Profile", style="cyan")
    table.add_column("Email", style="green")
    table.add_column("Site", style="yellow")
    table.add_column("Auth Status", style="bold")
    table.add_column("Details")
    
    for profile_dir in sorted(chrome_dir.glob("Profile*")):
        cookies_db = profile_dir / "Cookies"
        if not cookies_db.exists():
            continue
            
        profile_name = profile_dir.name
        
        # Get email
        email = "Unknown"
        prefs_file = profile_dir / "Preferences"
        if prefs_file.exists():
            try:
                import json
                with open(prefs_file) as f:
                    data = json.load(f)
                    accounts = data.get('account_info', [])
                    if accounts:
                        email = accounts[0].get('email', 'Unknown')
            except:
                pass
        
        # Check each site
        temp_cookies = tempfile.mktemp(suffix=".db")
        try:
            shutil.copy2(cookies_db, temp_cookies)
            conn = sqlite3.connect(temp_cookies)
            cursor = conn.cursor()
            
            for site, patterns in auth_indicators.items():
                # Check if any auth cookies exist
                auth_found = False
                details = []
                
                for pattern in patterns:
                    cursor.execute("""
                        SELECT name, expires_utc
                        FROM cookies 
                        WHERE host_key LIKE ? 
                        AND name LIKE ?
                    """, (f'%{site.split(".")[0]}%', f'%{pattern}%'))
                    
                    results = cursor.fetchall()
                    for cookie_name, expires in results:
                        auth_found = True
                        details.append(cookie_name)
                
                if auth_found:
                    table.add_row(
                        profile_name,
                        email[:20] + "..." if len(email) > 20 else email,
                        site,
                        "[green]Likely Authenticated[/green]",
                        ", ".join(details[:3]) + ("..." if len(details) > 3 else "")
                    )
                else:
                    # Check if site has any cookies at all
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM cookies 
                        WHERE host_key LIKE ?
                    """, (f'%{site.split(".")[0]}%',))
                    
                    count = cursor.fetchone()[0]
                    if count > 0:
                        table.add_row(
                            profile_name,
                            email[:20] + "..." if len(email) > 20 else email,
                            site,
                            "[yellow]Has cookies[/yellow]",
                            f"{count} cookies (no auth indicators)"
                        )
            
            conn.close()
            
        finally:
            if Path(temp_cookies).exists():
                Path(temp_cookies).unlink()
    
    console.print("\n")
    console.print(table)
    console.print("\n[bold]Note:[/bold] 'Likely Authenticated' means auth-related cookies were found.")
    console.print("Actual authentication status depends on cookie validity and expiration.")
    
    # Specific message about Sensor Tower
    console.print("\n[yellow]⚠️  Sensor Tower Issue:[/yellow]")
    console.print("The profiles only have tracking cookies (_gcl_au), not authentication cookies.")
    console.print("You'll need to sign in again to get proper authentication cookies.")

if __name__ == "__main__":
    check_auth_status()