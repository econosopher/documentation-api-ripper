#!/usr/bin/env python3
"""
Test the Documentation API Ripper without automatically launching browser
"""
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from src.parser import APIDocParser

console = Console()

def test_cookie_based_auth():
    """Test the cookie-based authentication flow"""
    console.print(Panel("[bold cyan]Documentation API Ripper - Cookie Test[/bold cyan]", expand=False))
    
    # Get URL from user or use default
    url = Prompt.ask(
        "Enter documentation URL to test", 
        default="https://app.sensortower.com/api/docs/app_analysis"
    )
    
    function = Prompt.ask(
        "Enter function name to extract", 
        default="category_history"
    )
    
    console.print(f"\n[cyan]Testing access to:[/cyan] {url}")
    console.print(f"[cyan]Looking for function:[/cyan] {function}\n")
    
    # Create parser but don't let it auto-launch browser
    parser = APIDocParser()
    
    try:
        # Check for existing cookies first
        has_access, message = parser.check_access(url)
        
        if has_access:
            console.print(f"[green]✓ {message}[/green]")
            
            # Ask if user wants to proceed with extraction
            if Confirm.ask("\nProceed with extraction?", default=True):
                console.print("\n[cyan]Extracting documentation...[/cyan]")
                # Note: This will still launch browser but with existing cookies
                result = parser.extract_function(url, function)
                
                if 'error' not in result:
                    console.print("[green]✓ Extraction successful![/green]")
                    
                    # Show preview
                    preview = parser.get_preview(result)
                    console.print("\n[bold]Preview:[/bold]")
                    console.print(Panel(preview, expand=False))
                else:
                    console.print(f"[red]✗ Extraction failed: {result['error']}[/red]")
        else:
            console.print(f"[yellow]✗ {message}[/yellow]")
            console.print("\n[bold]Options:[/bold]")
            console.print("1. Run 'python copy_cookies.py' to check which Chrome profiles have cookies")
            console.print("2. Manually sign in to the site in Chrome, then try again")
            console.print("3. Use the main tool with authentication: python src/main.py <url> <function>")
            
            if Confirm.ask("\nWould you like to launch browser for authentication?", default=False):
                console.print("\n[cyan]Please use the main tool for authentication:[/cyan]")
                console.print(f"python src/main.py {url} {function}")
            else:
                console.print("\n[yellow]Exiting without authentication.[/yellow]")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
    finally:
        if parser.driver:
            parser.close()

def check_available_cookies():
    """Check which domains have cookies available"""
    console.print("\n[cyan]Checking for available cookies...[/cyan]")
    
    # Common API documentation domains to check
    domains = [
        "sensortower.com",
        "app.sensortower.com",
        "stripe.com",
        "docs.stripe.com",
        "github.com",
        "api.github.com",
        "openai.com",
        "platform.openai.com"
    ]
    
    parser = APIDocParser()
    found_any = False
    
    for domain in domains:
        # Use the parser's internal method to check for cookies
        if parser._check_for_cookies(domain):
            console.print(f"[green]✓ Found cookies for {domain}[/green]")
            found_any = True
    
    if not found_any:
        console.print("[yellow]No cookies found for common API documentation sites[/yellow]")
    
    return found_any

if __name__ == "__main__":
    try:
        # First check what cookies are available
        console.print("[bold]Checking available cookies...[/bold]")
        check_available_cookies()
        
        # Then run the main test
        console.print("\n" + "="*50 + "\n")
        test_cookie_based_auth()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)