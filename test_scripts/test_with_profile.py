#!/usr/bin/env python3
"""
Test the app by pre-selecting a Chrome profile with cookies
"""
import sys
import os
from pathlib import Path

# Set environment variable to use Profile 15 (which has more cookies)
os.environ['CHROME_PROFILE'] = 'Profile 15'

# Import after setting env var
from src.parser import APIDocParser
from rich.console import Console

console = Console()

def test_with_profile():
    """Test extraction using a specific profile"""
    url = "https://app.sensortower.com/api/docs/app_analysis"
    function = "category_history"
    
    console.print("[bold cyan]Testing with Pre-selected Profile[/bold cyan]")
    console.print(f"URL: {url}")
    console.print(f"Function: {function}\n")
    
    parser = APIDocParser()
    
    # Manually set the profile to avoid interactive prompt
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    parser.profile_with_cookies = str(chrome_dir / "Profile 15")
    
    console.print(f"[green]Using Chrome Profile 15 (phil@deconstructoroffun.com)[/green]")
    console.print("[yellow]Make sure Chrome is completely closed before proceeding![/yellow]")
    
    try:
        # Skip the check_access since we know we have cookies
        console.print("\n[cyan]Extracting function documentation...[/cyan]")
        result = parser.extract_function(url, function)
        
        if 'error' not in result:
            console.print("[green]✓ Extraction successful![/green]\n")
            
            # Show preview
            preview = parser.get_preview(result)
            console.print("[bold]Preview:[/bold]")
            console.print(preview)
            
            # Ask if user wants to save
            console.print("\n[cyan]The extraction was successful! Use the main tool to save:[/cyan]")
            console.print(f"python src/main.py {url} {function}")
        else:
            console.print(f"[red]✗ Extraction failed: {result.get('error', 'Unknown error')}[/red]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\n[yellow]Make sure:[/yellow]")
        console.print("1. Chrome is completely closed")
        console.print("2. You're logged into Sensor Tower in Chrome Profile 15")
    finally:
        if parser.driver:
            parser.close()

if __name__ == "__main__":
    console.print("[yellow]IMPORTANT: This will launch Chrome with Profile 15[/yellow]")
    console.print("[yellow]Make sure Chrome is COMPLETELY CLOSED first![/yellow]")
    console.print("\nPress Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
        test_with_profile()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user[/yellow]")
        sys.exit(0)