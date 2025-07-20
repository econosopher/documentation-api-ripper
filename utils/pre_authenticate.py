#!/usr/bin/env python3
"""
Pre-authenticate with Google to save session for future use
"""
from src.parser import APIDocParser
from rich.console import Console
import time

console = Console()

def pre_authenticate():
    """Pre-authenticate and save session"""
    console.print("[bold blue]Pre-Authentication Setup[/bold blue]")
    console.print("=" * 50)
    console.print("\nThis will save your Google authentication for future use.")
    console.print("You only need to do this once.\n")
    
    parser = APIDocParser()
    
    try:
        # Navigate to Google accounts
        console.print("[cyan]Opening Google sign-in page...[/cyan]")
        parser.driver = parser._init_driver(headless=False)
        parser.driver.get("https://accounts.google.com")
        
        console.print("\n[yellow]Please sign in to your Google account.[/yellow]")
        console.print("[yellow]After signing in, press Enter here...[/yellow]")
        input()
        
        # Test the authentication by visiting a few common sites
        test_sites = [
            "https://app.sensortower.com",
            "https://github.com",
            "https://docs.google.com"
        ]
        
        console.print("\n[cyan]Testing authentication on common sites...[/cyan]")
        for site in test_sites:
            try:
                parser.driver.get(site)
                time.sleep(2)
                console.print(f"[green]✓ {site}[/green]")
            except:
                console.print(f"[yellow]? {site}[/yellow]")
        
        console.print("\n[green]✓ Pre-authentication complete![/green]")
        console.print("[cyan]Your session has been saved in ./chrome_profile[/cyan]")
        console.print("\nYou can now run the API ripper without signing in each time:")
        console.print("[bold]python src/main.py <url> <function>[/bold]")
        
    except Exception as e:
        console.print(f"[red]Error during pre-authentication: {e}[/red]")
    finally:
        if parser.driver:
            parser.driver.quit()

if __name__ == "__main__":
    pre_authenticate()