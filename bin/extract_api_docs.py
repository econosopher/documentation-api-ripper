#!/usr/bin/env python3
"""
Interactive API documentation search tool
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import APIDocParser
from src.api_section_finder import APISectionFinder
from rich.console import Console
from rich.prompt import Prompt
import json

console = Console()

def main():
    """Main interactive search function"""
    console.print("[bold cyan]API Documentation Search Tool[/bold cyan]")
    console.print()
    
    # Initialize parser
    parser = APIDocParser()
    
    try:
        # Get the API docs URL
        url = Prompt.ask(
            "[cyan]Enter the API documentation URL[/cyan]",
            default="https://app.sensortower.com/api/v1/docs"
        )
        
        # Navigate to the page
        console.print(f"\n[yellow]Navigating to {url}...[/yellow]")
        
        # Use the parser to handle authentication and navigation
        content = parser.parse_url(url)
        
        if not content:
            console.print("[red]Failed to load the page[/red]")
            return
        
        console.print("[green]✓ Page loaded successfully[/green]")
        
        # Initialize the section finder
        finder = APISectionFinder(parser.driver)
        
        # Interactive search loop
        while True:
            console.print("\n" + "="*50)
            search_term = Prompt.ask(
                "\n[cyan]Enter search term (or 'quit' to exit)[/cyan]"
            )
            
            if search_term.lower() in ['quit', 'exit', 'q']:
                break
            
            # Search and extract
            results = finder.search_and_extract(search_term)
            
            if not results:
                console.print("[yellow]No results found. Try a different search term.[/yellow]")
                continue
            
            # Ask if user wants to save results
            if Prompt.ask("\n[cyan]Save results to file? (y/n)[/cyan]", default="n").lower() == 'y':
                filename = Prompt.ask("[cyan]Enter filename[/cyan]", default=f"{search_term.replace(' ', '_')}_api.json")
                
                # Prepare data for saving
                save_data = []
                for result in results:
                    save_data.append({
                        'search_term': search_term,
                        'match_text': result['match']['text'],
                        'api_info': result['api_info']
                    })
                
                with open(filename, 'w') as f:
                    json.dump(save_data, f, indent=2)
                
                console.print(f"[green]✓ Results saved to {filename}[/green]")
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Search interrupted[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    finally:
        if parser:
            parser.close()
        console.print("\n[cyan]Goodbye![/cyan]")

if __name__ == "__main__":
    main()