#!/usr/bin/env python3
"""
Detect API documentation format and extract endpoints
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.chrome_manager import ChromeManager
from src.api_doc_detector import APIDocDetector
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import json
import time

console = Console()

def display_endpoints(endpoints: list):
    """Display endpoints in a nice table"""
    if not endpoints:
        console.print("[yellow]No endpoints found[/yellow]")
        return
        
    table = Table(title="API Endpoints", show_header=True)
    table.add_column("Method", style="cyan", width=10)
    table.add_column("Path", style="green")
    table.add_column("Description", style="dim")
    
    for ep in endpoints[:20]:  # Show first 20
        table.add_row(
            ep['method'],
            ep['path'],
            ep['description'][:50] + '...' if len(ep['description']) > 50 else ep['description']
        )
    
    console.print(table)
    
    if len(endpoints) > 20:
        console.print(f"[dim]... and {len(endpoints) - 20} more endpoints[/dim]")

def main():
    """Main function"""
    console.print("[bold cyan]API Documentation Format Detector & Extractor[/bold cyan]")
    console.print()
    
    with ChromeManager() as manager:
        try:
            # Create driver
            console.print("[yellow]Starting browser...[/yellow]")
            driver = manager.create_driver()
            
            # Get URL
            url = Prompt.ask(
                "[cyan]Enter the API documentation URL[/cyan]",
                default="https://app.sensortower.com/api/v1/docs"
            )
            
            # Navigate
            console.print(f"[yellow]Navigating to {url}...[/yellow]")
            driver.get(url)
            
            # Wait for page load
            console.print("[yellow]Waiting for page to load...[/yellow]")
            time.sleep(3)
            
            # Check if we need to login
            if "sign_in" in driver.current_url or "login" in driver.current_url.lower():
                console.print("[yellow]Login required. Please complete the login process.[/yellow]")
                Prompt.ask("[cyan]Press Enter when you've logged in[/cyan]")
            
            # Initialize detector
            detector = APIDocDetector(driver)
            
            # Detect format
            console.print("\n[yellow]Detecting API documentation format...[/yellow]")
            doc_format = detector.detect_format()
            
            # Main loop
            while True:
                console.print("\n" + "="*50)
                console.print("\n[cyan]Options:[/cyan]")
                console.print("1. List all endpoints")
                console.print("2. Search for endpoint")
                console.print("3. Export endpoints to JSON")
                console.print("4. Detect format again")
                console.print("5. Navigate to new URL")
                console.print("6. Quit")
                
                choice = Prompt.ask("\n[cyan]Choose an option[/cyan]", choices=["1", "2", "3", "4", "5", "6"])
                
                if choice == "1":
                    # List all endpoints
                    console.print("\n[yellow]Extracting endpoints...[/yellow]")
                    endpoints = detector.get_endpoints()
                    display_endpoints(endpoints)
                    
                elif choice == "2":
                    # Search for endpoint
                    search_term = Prompt.ask("[cyan]Enter search term[/cyan]")
                    matches = detector.search_endpoint(search_term)
                    
                    if matches:
                        console.print(f"\n[green]Found {len(matches)} matching endpoints:[/green]")
                        for i, match in enumerate(matches):
                            console.print(f"\n[yellow]{i+1}.[/yellow] {match['method']} {match['path']}")
                            
                        # Highlight option
                        if Prompt.ask("\n[cyan]Highlight an endpoint? (y/n)[/cyan]", default="n").lower() == 'y':
                            idx = int(Prompt.ask("[cyan]Enter number[/cyan]", default="1")) - 1
                            if 0 <= idx < len(matches):
                                detector.highlight_endpoint(matches[idx])
                                console.print("[green]✓ Endpoint highlighted on page[/green]")
                    else:
                        console.print("[red]No matching endpoints found[/red]")
                    
                elif choice == "3":
                    # Export to JSON
                    console.print("\n[yellow]Extracting all endpoints...[/yellow]")
                    endpoints = detector.get_endpoints()
                    
                    filename = Prompt.ask("[cyan]Enter filename[/cyan]", default="api_endpoints.json")
                    
                    # Prepare data for export
                    export_data = {
                        'url': driver.current_url,
                        'format': doc_format,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'endpoints': [
                            {
                                'method': ep['method'],
                                'path': ep['path'],
                                'description': ep['description']
                            }
                            for ep in endpoints
                        ]
                    }
                    
                    with open(filename, 'w') as f:
                        json.dump(export_data, f, indent=2)
                    
                    console.print(f"[green]✓ Exported {len(endpoints)} endpoints to {filename}[/green]")
                    
                elif choice == "4":
                    # Detect format again
                    console.print("\n[yellow]Re-detecting format...[/yellow]")
                    doc_format = detector.detect_format()
                    
                elif choice == "5":
                    # Navigate to new URL
                    new_url = Prompt.ask("[cyan]Enter new URL[/cyan]")
                    console.print(f"[yellow]Navigating to {new_url}...[/yellow]")
                    driver.get(new_url)
                    time.sleep(3)
                    
                    # Re-detect format
                    doc_format = detector.detect_format()
                    
                elif choice == "6":
                    break
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            import traceback
            traceback.print_exc()
    
    console.print("\n[cyan]Goodbye![/cyan]")

if __name__ == "__main__":
    main()