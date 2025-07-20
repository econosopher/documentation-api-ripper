#!/usr/bin/env python3
"""
Test Google authentication and session storage
"""
from src.parser import APIDocParser
from rich.console import Console
from pathlib import Path

console = Console()

def test_auth_and_storage():
    """Test authentication and verify session storage"""
    
    console.print("[bold cyan]Google Authentication & Session Storage Test[/bold cyan]")
    console.print("="*60)
    
    # Test URL - Sensor Tower API docs
    test_url = "https://app.sensortower.com/api/docs/app_analysis"
    
    parser = APIDocParser()
    
    try:
        # Step 1: Check current status
        console.print("\n[cyan]Step 1: Checking current authentication status[/cyan]")
        has_access, message = parser.check_access(test_url)
        console.print(f"Status: {message}\n")
        
        # Step 2: Authenticate if needed
        if not parser.session_manager.has_stored_session("sensortower.com"):
            console.print("[yellow]No stored session found. Let's create one![/yellow]")
            console.print("\n[cyan]Launching browser for authentication...[/cyan]")
            
            # This will launch the browser and wait for you to sign in
            auth_result = parser.authenticate_google(return_to_url=test_url)
            
            if auth_result:
                console.print("\n[green]✓ Authentication successful![/green]")
                
                # Check if session was saved
                session_file = Path("./oauth_tokens/sensortower.com_session.json")
                if session_file.exists():
                    console.print(f"[green]✓ Session saved to: {session_file}[/green]")
                    
                    # Show session file size
                    size = session_file.stat().st_size
                    console.print(f"[dim]Session file size: {size} bytes[/dim]")
                else:
                    console.print("[red]✗ Session file not found![/red]")
            else:
                console.print("[red]✗ Authentication failed or was cancelled[/red]")
        else:
            console.print("[green]✓ Found existing stored session![/green]")
            console.print("Session will be restored automatically when needed.")
            
        # Step 3: Show what's stored
        console.print("\n[cyan]Step 3: Checking stored sessions[/cyan]")
        token_dir = Path("./oauth_tokens")
        if token_dir.exists():
            sessions = list(token_dir.glob("*_session.json"))
            if sessions:
                console.print(f"Found {len(sessions)} stored session(s):")
                for session in sessions:
                    console.print(f"  • {session.name}")
                    # Show when it was created
                    created = session.stat().st_mtime
                    from datetime import datetime
                    created_date = datetime.fromtimestamp(created).strftime("%Y-%m-%d %H:%M:%S")
                    console.print(f"    Created: {created_date}")
        else:
            console.print("No sessions directory found yet.")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Test cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
    finally:
        if parser.driver:
            console.print("\n[cyan]Closing browser...[/cyan]")
            parser.close()

if __name__ == "__main__":
    console.print("[yellow]This test will:[/yellow]")
    console.print("1. Check for existing authentication sessions")
    console.print("2. Launch browser for Google sign-in if needed")
    console.print("3. Save the session for future use")
    console.print("4. Show stored sessions\n")
    
    console.input("[cyan]Press Enter to start...[/cyan]")
    
    test_auth_and_storage()