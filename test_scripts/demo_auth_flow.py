#!/usr/bin/env python3
"""
Demo: Documentation API Ripper Authentication Flow

This demonstrates the proper authentication workflow:
1. First checks for existing Chrome profile cookies
2. If multiple profiles have cookies, lets user choose
3. Falls back to manual login only if no cookies found
"""
import sys
import time
from src.parser import APIDocParser
from rich.console import Console
from rich.panel import Panel

console = Console()

def demo_authentication_flow():
    """Demonstrate the authentication flow"""
    console.print("[bold blue]Documentation API Ripper - Authentication Demo[/bold blue]")
    console.print("=" * 60)
    
    # Example URL
    url = "https://app.sensortower.com/api/docs/app_analysis"
    function = "category_history"
    
    console.print(f"\n[cyan]Target URL:[/cyan] {url}")
    console.print(f"[cyan]Function to extract:[/cyan] {function}\n")
    
    # Initialize parser
    parser = APIDocParser()
    
    # Step 1: Check access (this will check for cookies)
    console.print("[yellow]Step 1: Checking for existing authentication...[/yellow]")
    has_access, message = parser.check_access(url)
    
    if has_access:
        console.print(f"[green]✓ {message}[/green]")
        console.print("[green]No additional authentication needed![/green]")
        
        # Try to extract the function
        console.print(f"\n[yellow]Step 2: Extracting function '{function}'...[/yellow]")
        result = parser.extract_function(url, function)
        
        if 'error' not in result:
            console.print("[green]✓ Function extracted successfully![/green]")
            # Show preview
            preview = parser.get_preview(result)
            console.print(Panel(preview[:500] + "...", title="Preview", border_style="green"))
        else:
            console.print(f"[red]✗ {result['error']}[/red]")
    else:
        console.print(f"[yellow]✗ {message}[/yellow]")
        console.print("\n[yellow]Step 2: Manual authentication required[/yellow]")
        console.print("The tool will now:")
        console.print("1. Open a browser window")
        console.print("2. Navigate to the login page")
        console.print("3. Wait for you to sign in")
        console.print("4. Continue once authenticated")
        
        # Demonstrate authentication
        console.print("\n[cyan]Starting authentication process...[/cyan]")
        auth_result = parser.authenticate_google(return_to_url=url)
        
        if auth_result:
            console.print("[green]✓ Authentication successful![/green]")
            console.print("\n[yellow]Step 3: Retrying function extraction...[/yellow]")
            
            result = parser.extract_function(url, function)
            if 'error' not in result:
                console.print("[green]✓ Function extracted successfully![/green]")
            else:
                console.print(f"[red]✗ {result['error']}[/red]")
        else:
            console.print("[red]✗ Authentication failed or was cancelled[/red]")
    
    # Cleanup
    parser.close()
    console.print("\n[green]Demo completed![/green]")

def show_authentication_info():
    """Show information about authentication"""
    console.print("\n[bold]Authentication Methods:[/bold]")
    console.print("1. [green]Existing Chrome Profile Cookies (Preferred)[/green]")
    console.print("   - Automatically detects cookies from your Chrome profiles")
    console.print("   - No manual login required if valid cookies exist")
    console.print("   - Supports multiple profiles with selection prompt")
    
    console.print("\n2. [yellow]Manual Browser Login (Fallback)[/yellow]")
    console.print("   - Opens browser for manual authentication")
    console.print("   - Supports Google OAuth and other login methods")
    console.print("   - Saves session for future use")
    
    console.print("\n[bold]To Pre-authenticate:[/bold]")
    console.print("1. Open Chrome and navigate to your API documentation site")
    console.print("2. Log in with your credentials")
    console.print("3. Make sure 'Remember me' is checked")
    console.print("4. The tool will automatically use those cookies")

if __name__ == "__main__":
    try:
        show_authentication_info()
        console.print("\n" + "="*60 + "\n")
        
        if len(sys.argv) > 1 and sys.argv[1] == "--skip-demo":
            console.print("[yellow]Skipping demo (--skip-demo flag)[/yellow]")
        else:
            demo_authentication_flow()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")