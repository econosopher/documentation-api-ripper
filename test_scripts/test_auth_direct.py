#!/usr/bin/env python3
"""
Direct test of authentication - no input required
"""
from src.parser import APIDocParser
from rich.console import Console
from pathlib import Path
import sys

console = Console()

# Test URL
test_url = "https://app.sensortower.com/api/docs/app_analysis"

console.print("[bold cyan]Google Authentication & Session Storage Test[/bold cyan]")
console.print("="*60)

parser = APIDocParser()

try:
    # Check current status
    console.print("\n[cyan]Checking authentication status...[/cyan]")
    has_access, message = parser.check_access(test_url)
    console.print(f"Status: {message}\n")
    
    # Check for stored sessions
    token_dir = Path("./oauth_tokens")
    if token_dir.exists():
        sessions = list(token_dir.glob("*_session.json"))
        if sessions:
            console.print(f"[green]Found {len(sessions)} stored session(s):[/green]")
            for session in sessions:
                console.print(f"  • {session.name}")
    
    if not parser.session_manager.has_stored_session("sensortower.com"):
        console.print("\n[yellow]No stored session found.[/yellow]")
        console.print("\n[cyan]To authenticate and store a session:[/cyan]")
        console.print("1. Run the main tool:")
        console.print("   python -m src.main https://app.sensortower.com/api/docs/app_analysis category_history")
        console.print("2. Choose option 1 to authenticate")
        console.print("3. Sign in with Google")
        console.print("4. The session will be automatically saved\n")
    else:
        console.print("\n[green]✓ Stored session found![/green]")
        console.print("The app will use this session automatically.")
        
except Exception as e:
    console.print(f"\n[red]Error: {e}[/red]")
finally:
    if parser.driver:
        parser.close()

console.print("\n[dim]Session storage location: ./oauth_tokens/[/dim]")