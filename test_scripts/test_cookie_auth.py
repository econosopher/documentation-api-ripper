#!/usr/bin/env python3
"""
Test the cookie-based authentication flow
"""
from src.parser import APIDocParser
from rich.console import Console

console = Console()

def test_sensor_tower():
    """Test extracting from Sensor Tower API docs"""
    url = "https://app.sensortower.com/api/docs/app_analysis"
    function = "category_history"
    
    console.print("[bold blue]Testing Cookie-Based Authentication[/bold blue]")
    console.print("=" * 50)
    console.print(f"URL: {url}")
    console.print(f"Function: {function}\n")
    
    parser = APIDocParser()
    
    try:
        # Check access - this will now check for cookies first
        has_access, message = parser.check_access(url)
        console.print(f"[{'green' if has_access else 'yellow'}]{message}[/{'green' if has_access else 'yellow'}]")
        
        if not has_access and not parser.profile_with_cookies:
            console.print("\n[yellow]No cookies found. Would normally prompt for authentication.[/yellow]")
            console.print("[cyan]Run the full tool to handle authentication:[/cyan]")
            console.print("python src/main.py https://app.sensortower.com/api/docs/app_analysis category_history")
        else:
            console.print("\n[green]Ready to extract documentation![/green]")
            
            # Try extraction
            console.print(f"\n[cyan]Attempting to extract '{function}'...[/cyan]")
            result = parser.extract_function(url, function)
            
            if 'error' not in result:
                console.print("[green]✓ Extraction successful![/green]")
                preview = parser.get_preview(result)
                console.print("\n[bold]Preview:[/bold]")
                console.print(preview)
            else:
                console.print(f"[red]Extraction failed: {result['error']}[/red]")
    
    finally:
        parser.close()

if __name__ == "__main__":
    test_sensor_tower()