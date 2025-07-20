#!/usr/bin/env python3
"""
Force authentication flow to create a stored session
"""
from src.parser import APIDocParser
from rich.console import Console

console = Console()

def force_authentication():
    """Force the authentication flow regardless of cookies"""
    
    url = "https://app.sensortower.com/api/docs/app_analysis"
    
    console.print("[bold cyan]Forcing Authentication Flow[/bold cyan]")
    console.print("="*50)
    console.print("\nThis will:")
    console.print("1. Launch browser")
    console.print("2. Navigate to Sensor Tower login")
    console.print("3. Wait for you to sign in with Google")
    console.print("4. Save your session for future use\n")
    
    parser = APIDocParser()
    
    try:
        # Skip cookie check and go straight to authentication
        console.print("[cyan]Launching browser for authentication...[/cyan]")
        
        # Call authenticate_google directly
        success = parser.authenticate_google(return_to_url=url)
        
        if success:
            console.print("\n[green]✓ Authentication successful![/green]")
            console.print("[green]✓ Session has been saved[/green]")
            console.print("\nYou can now run the main tool and it will use the saved session:")
            console.print("python -m src.main https://app.sensortower.com/api/docs/app_analysis category_history")
        else:
            console.print("\n[red]Authentication failed or was cancelled[/red]")
            
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
    finally:
        if parser.driver:
            parser.close()

if __name__ == "__main__":
    # Run it directly
    force_authentication()