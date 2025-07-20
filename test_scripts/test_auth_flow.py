#!/usr/bin/env python3
"""
Test the authentication flow step by step
"""
from src.parser import APIDocParser
from rich.console import Console
import time

console = Console()

def test_auth_flow():
    """Test authentication and session storage"""
    
    url = "https://app.sensortower.com/api/docs/app_analysis"
    function = "category_history"
    
    console.print("[bold cyan]Testing Authentication Flow[/bold cyan]")
    console.print("="*50)
    
    parser = APIDocParser()
    
    # Step 1: Check current status
    console.print("\n[cyan]Step 1: Checking authentication status[/cyan]")
    has_access, message = parser.check_access(url)
    console.print(f"Status: {message}")
    
    if not parser.session_manager.has_stored_session("sensortower.com"):
        console.print("\n[yellow]No stored session found.[/yellow]")
        console.print("To create a stored session:")
        console.print("1. Run: python -m src.main <url> <function>")
        console.print("2. Sign in when prompted") 
        console.print("3. The session will be automatically saved")
        console.print("4. Future runs will use the saved session")
    else:
        console.print("\n[green]Found stored session![/green]")
        console.print("The app should automatically restore your session.")
    
    # Show where sessions are stored
    console.print(f"\n[dim]Sessions are stored in: ./oauth_tokens/[/dim]")
    
    # Check what's in the oauth_tokens directory
    from pathlib import Path
    token_dir = Path("./oauth_tokens")
    if token_dir.exists():
        sessions = list(token_dir.glob("*_session.json"))
        if sessions:
            console.print(f"[dim]Found {len(sessions)} stored session(s):[/dim]")
            for session in sessions:
                console.print(f"[dim]  - {session.name}[/dim]")

if __name__ == "__main__":
    test_auth_flow()