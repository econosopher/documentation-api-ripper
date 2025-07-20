#!/usr/bin/env python3
"""
Simplified API documentation extractor - uses your existing Chrome profile
"""
import sys
from src.simple_parser import SimpleAPIParser
from src.converter import HTMLToMarkdownConverter
from src.formatter import OutputFormatter
from rich.console import Console

console = Console()

def main():
    if len(sys.argv) != 3:
        console.print("[red]Usage: python simple_run.py <url> <function_name>[/red]")
        console.print("Example: python simple_run.py https://app.sensortower.com/api/docs/app_analysis category_history")
        sys.exit(1)
    
    url = sys.argv[1]
    function_name = sys.argv[2]
    
    console.print("[bold blue]Simple API Documentation Extractor[/bold blue]")
    console.print("=" * 50)
    console.print(f"URL: {url}")
    console.print(f"Function: {function_name}\n")
    
    parser = SimpleAPIParser()
    converter = HTMLToMarkdownConverter()
    formatter = OutputFormatter()
    
    try:
        # Extract function
        result = parser.extract_function(url, function_name)
        
        if result['found']:
            console.print(f"[green]✓ Found content for '{function_name}'[/green]")
            
            # Save content
            filename = f"{function_name}_simple"
            
            # Save raw text
            with open(f"output/{filename}.txt", 'w') as f:
                f.write(result['content'])
            
            # Save HTML if available
            if 'html' in result:
                with open(f"output/{filename}.html", 'w') as f:
                    f.write(result['html'])
                
                # Try to convert to markdown
                try:
                    markdown = converter.convert_html_to_markdown(result['html'])
                    formatter.save_markdown(markdown, filename)
                except:
                    pass
            
            console.print(f"\n[green]✓ Saved to output/{filename}.*[/green]")
            console.print("\n[cyan]Preview:[/cyan]")
            console.print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
            
        else:
            console.print(f"[red]Could not find '{function_name}' on the page[/red]")
            console.print("[yellow]Try checking if you're on the right page or if the function name is correct[/yellow]")
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
    
    finally:
        parser.close()

if __name__ == "__main__":
    main()