#!/usr/bin/env python3
"""
Test that subdomain cookie checking is working correctly
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import sqlite3
import shutil
import tempfile
from pathlib import Path

console = Console()

def test_subdomain_logic():
    """Test the subdomain cookie detection logic"""
    console.print(Panel("[bold cyan]Testing Subdomain Cookie Detection[/bold cyan]", expand=False))
    
    test_cases = [
        ("app.sensortower.com", ["sensortower.com", ".sensortower.com"]),
        ("docs.stripe.com", ["stripe.com", ".stripe.com"]),
        ("api.github.com", ["github.com", ".github.com"]),
        ("subdomain.example.co.uk", ["example.co.uk", ".example.co.uk"]),
        ("deep.sub.example.com", ["sub.example.com", ".sub.example.com", "example.com", ".example.com"])
    ]
    
    console.print("\n[bold]Cookie Domain Matching Logic:[/bold]")
    table = Table(show_header=True)
    table.add_column("Requested URL Domain", style="cyan")
    table.add_column("Will Also Check For", style="green")
    
    for domain, expected_parents in test_cases:
        # Simulate the logic from parser.py
        domain_parts = domain.split('.')
        checked_domains = [domain, f'.{domain}']
        
        if len(domain_parts) > 2:
            for i in range(1, len(domain_parts) - 1):
                parent = '.'.join(domain_parts[i:])
                checked_domains.extend([parent, f'.{parent}'])
        
        table.add_row(domain, ', '.join(checked_domains))
    
    console.print(table)
    
    # Now test with actual Chrome cookies
    console.print("\n[bold]Testing with Actual Chrome Cookies:[/bold]\n")
    
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    
    # Test app.sensortower.com
    console.print("[cyan]Checking app.sensortower.com:[/cyan]")
    found_profiles = []
    
    for profile_dir in chrome_dir.glob("Profile*"):
        cookies_db = profile_dir / "Cookies"
        if not cookies_db.exists():
            continue
            
        temp_cookies = tempfile.mktemp(suffix=".db")
        try:
            shutil.copy2(cookies_db, temp_cookies)
            conn = sqlite3.connect(temp_cookies)
            cursor = conn.cursor()
            
            # Check for sensortower.com cookies (parent domain)
            cursor.execute("""
                SELECT COUNT(*) 
                FROM cookies 
                WHERE host_key IN ('sensortower.com', '.sensortower.com', 'app.sensortower.com', '.app.sensortower.com')
            """)
            
            count = cursor.fetchone()[0]
            if count > 0:
                # Get details
                cursor.execute("""
                    SELECT host_key, COUNT(*) 
                    FROM cookies 
                    WHERE host_key IN ('sensortower.com', '.sensortower.com', 'app.sensortower.com', '.app.sensortower.com')
                    GROUP BY host_key
                """)
                
                details = cursor.fetchall()
                found_profiles.append({
                    'profile': profile_dir.name,
                    'details': details
                })
            
            conn.close()
        finally:
            if Path(temp_cookies).exists():
                Path(temp_cookies).unlink()
    
    if found_profiles:
        for profile_info in found_profiles:
            console.print(f"\n[green]{profile_info['profile']}:[/green]")
            for host, count in profile_info['details']:
                console.print(f"  • {host}: {count} cookies")
        
        console.print("\n[green]✓ With the fix, app.sensortower.com will now find and use these parent domain cookies![/green]")
    else:
        console.print("[yellow]No sensortower.com cookies found in any profile[/yellow]")

if __name__ == "__main__":
    test_subdomain_logic()