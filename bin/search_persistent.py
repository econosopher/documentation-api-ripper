#!/usr/bin/env python3
"""
API Search with Persistent Chrome Profile
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.profile_manager import ChromeProfileManager
from src.api_doc_detector import APIDocDetector
from src.api_section_finder import APISectionFinder
from rich.console import Console
from rich.prompt import Prompt
import time

console = Console()

def main():
    """Main function with persistent profiles"""
    console.print("[bold cyan]API Documentation Search - Persistent Session[/bold cyan]")
    console.print()
    
    # Initialize profile manager
    profile_manager = ChromeProfileManager()
    
    # Select profile
    profile_path, profile_name = profile_manager.select_profile()
    
    try:
        # Create driver with selected profile
        console.print("\n[yellow]Starting Chrome...[/yellow]")
        driver = profile_manager.create_driver(profile_path, profile_name)
        
        # Get URL
        url = Prompt.ask(
            "\n[cyan]Enter API documentation URL[/cyan]",
            default="https://app.sensortower.com/api/v1/docs"
        )
        
        # Navigate
        console.print(f"[yellow]Navigating to {url}...[/yellow]")
        driver.get(url)
        time.sleep(2)
        
        # Check if we need to login
        current_url = driver.current_url.lower()
        if any(indicator in current_url for indicator in ['login', 'signin', 'sign_in', 'auth']):
            console.print("\n[yellow]⚠ Login required[/yellow]")
            console.print("[cyan]Please complete the login process in the browser[/cyan]")
            console.print("[dim]Your login will be saved for next time![/dim]")
            
            # Wait for login
            input("\nPress Enter when you've logged in...")
            
            # Refresh to ensure we're on the right page
            driver.get(url)
            time.sleep(2)
        else:
            console.print("[green]✓ Already authenticated! No login needed.[/green]")
        
        # Initialize tools
        detector = APIDocDetector(driver)
        finder = APISectionFinder(driver)
        
        # Detect format
        console.print("\n[yellow]Detecting API documentation format...[/yellow]")
        doc_format = detector.detect_format()
        
        # Main search loop
        while True:
            console.print("\n" + "="*50)
            console.print("\n[cyan]Options:[/cyan]")
            console.print("1. Search for text/section")
            console.print("2. List all endpoints")
            console.print("3. Search for specific endpoint")
            console.print("4. Navigate to new URL")
            console.print("5. Quit")
            
            choice = Prompt.ask("\n[cyan]Choose option[/cyan]", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                # Text search
                search_term = Prompt.ask("[cyan]Enter search term[/cyan]")
                
                # JavaScript search and highlight
                script = """
                function searchAndHighlight(term) {
                    // Remove old highlights
                    document.querySelectorAll('.api-highlight').forEach(el => {
                        el.classList.remove('api-highlight');
                        el.style.backgroundColor = '';
                        el.style.border = '';
                    });
                    
                    var found = 0;
                    var elements = document.querySelectorAll('*');
                    var regex = new RegExp(term, 'gi');
                    
                    for (var el of elements) {
                        if (el.children.length === 0 && el.textContent) {
                            if (regex.test(el.textContent)) {
                                el.classList.add('api-highlight');
                                el.style.backgroundColor = 'yellow';
                                el.style.border = '2px solid red';
                                el.style.padding = '2px';
                                found++;
                                
                                if (found === 1) {
                                    el.scrollIntoView({behavior: 'smooth', block: 'center'});
                                }
                            }
                        }
                    }
                    
                    return found;
                }
                return searchAndHighlight(arguments[0]);
                """
                
                count = driver.execute_script(script, search_term)
                if count > 0:
                    console.print(f"[green]✓ Found and highlighted {count} matches[/green]")
                else:
                    console.print(f"[red]No matches found for '{search_term}'[/red]")
                    
            elif choice == "2":
                # List endpoints
                endpoints = detector.get_endpoints()
                
                if endpoints:
                    console.print(f"\n[green]Found {len(endpoints)} endpoints:[/green]")
                    for i, ep in enumerate(endpoints[:10], 1):
                        console.print(f"{i}. [cyan]{ep['method']}[/cyan] {ep['path']}")
                    
                    if len(endpoints) > 10:
                        console.print(f"[dim]... and {len(endpoints) - 10} more[/dim]")
                else:
                    console.print("[yellow]No endpoints found[/yellow]")
                    
            elif choice == "3":
                # Search endpoint
                search = Prompt.ask("[cyan]Enter endpoint search term[/cyan]")
                matches = detector.search_endpoint(search)
                
                if matches:
                    for match in matches:
                        console.print(f"[cyan]{match['method']}[/cyan] {match['path']}")
                        detector.highlight_endpoint(match)
                else:
                    console.print("[red]No matching endpoints[/red]")
                    
            elif choice == "4":
                # New URL
                new_url = Prompt.ask("[cyan]Enter new URL[/cyan]")
                driver.get(new_url)
                time.sleep(2)
                
            elif choice == "5":
                break
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
    finally:
        if 'driver' in locals():
            driver.quit()
            console.print("\n[green]✓ Session saved. Your login will persist next time![/green]")
    
    console.print("\n[cyan]Goodbye![/cyan]")

if __name__ == "__main__":
    main()