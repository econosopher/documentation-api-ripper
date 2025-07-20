#!/usr/bin/env python3
import click
import yaml
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.syntax import Syntax

from .parser import APIDocParser
from .converter import HTMLToMarkdownConverter
from .formatter import OutputFormatter

console = Console()


@click.command()
@click.argument('url')
@click.argument('function')
@click.option('--output-dir', '-o', default='output', help='Output directory (default: output)')
@click.option('--config', '-c', default='config.yaml', help='Configuration file (default: config.yaml)')
@click.option('--skip-preview', '-s', is_flag=True, help='Skip preview and confirmation')
@click.option('--format', type=click.Choice(['markdown', 'json', 'both']), default='markdown', help='Output format (default: markdown)')
def main(url: str, function: str, output_dir: str, config: str, skip_preview: bool, format: str):
    """
    Documentation API Ripper - Extract specific functions from API documentation
    
    URL: The documentation URL to extract from
    FUNCTION: The function/method name to extract
    
    Example:
        python src/main.py https://api.example.com/docs getUserProfile
    """
    console.print("[bold blue]Documentation API Ripper[/bold blue]")
    console.print("=" * 50)
    
    # Initialize components
    parser = APIDocParser(config)
    converter = HTMLToMarkdownConverter()
    formatter = OutputFormatter(output_dir)
    
    # Step 1: Check access
    console.print(f"\n[cyan]URL:[/cyan] {url}")
    console.print(f"[cyan]Function:[/cyan] {function}\n")
    
    has_access, message = parser.check_access(url)
    console.print(f"[{'green' if has_access else 'yellow'}]{message}[/{'green' if has_access else 'yellow'}]")
    
    # Step 2: Authenticate if needed
    if not has_access:
        console.print("\n[yellow]Authentication required to access this URL.[/yellow]")
        console.print("\n[cyan]Options:[/cyan]")
        console.print("1. Launch browser for authentication")
        console.print("2. Try anyway (may fail)")
        console.print("3. Cancel")
        
        choice = console.input("\n[cyan]Choose an option (1-3):[/cyan] ").strip()
        
        if choice == "1":
            console.print("\n[cyan]Launching browser for authentication...[/cyan]")
            auth_result = parser.authenticate_google(return_to_url=url)
            
            if auth_result:
                console.print("[green]✓ Authentication process completed[/green]")
                
                # Re-check access
                has_access, message = parser.check_access(url)
                if not has_access:
                    console.print(f"[yellow]Warning: {message}[/yellow]")
                    console.print("[cyan]Attempting to continue anyway...[/cyan]")
            else:
                console.print("[red]Authentication failed or was cancelled[/red]")
                parser.close()
                return
                
        elif choice == "2":
            console.print("[yellow]Proceeding without authentication...[/yellow]")
            console.print("[cyan]Note: Some content may not be accessible.[/cyan]")
            
        else:
            console.print("[yellow]Extraction cancelled[/yellow]")
            parser.close()
            return
    
    # Step 3: Extract the function
    console.print(f"\n[cyan]Extracting function '{function}'...[/cyan]")
    
    # Clarify that browser is needed for extraction even with cookies
    if has_access and parser.profile_with_cookies:
        console.print("[dim]Note: Browser will launch to extract documentation (using saved cookies)[/dim]")
    else:
        console.print("[dim]Note: Browser will launch to extract documentation[/dim]")
    
    function_data = parser.extract_function(url, function)
    
    if 'error' in function_data:
        console.print(f"[red]Error: {function_data['error']}[/red]")
        parser.close()
        return
    
    # Step 4: Show preview
    if not skip_preview:
        preview = parser.get_preview(function_data)
        console.print("\n[bold]Preview of extracted content:[/bold]")
        console.print(Panel(preview, title=f"Function: {function}", border_style="green"))
        
        if not Confirm.ask("\nDoes this look correct? Proceed with extraction?"):
            console.print("[yellow]Extraction cancelled[/yellow]")
            parser.close()
            return
    
    # Step 5: Convert and save
    console.print(f"\n[cyan]Processing and saving documentation...[/cyan]")
    
    try:
        # Create output subdirectory for this API
        api_name = Path(url).netloc.replace('.', '_') or 'api'
        
        # Convert function data to API docs format
        api_docs = {
            'url': url,
            'title': f"{api_name} - {function}",
            'endpoints': [{
                'endpoint': function,
                'method': '',
                'description': function_data.get('description', ''),
                'parameters': function_data.get('parameters', []),
                'response': function_data.get('returns', ''),
                'code_samples': function_data.get('examples', [])
            }]
        }
        
        # Convert to markdown
        markdown_content = converter.convert_api_docs(api_docs)
        claude_formatted = converter.convert_to_claude_format(markdown_content)
        
        # Add integration guide
        integration_guide = f"""

## Integration with Claude Code

This function can be integrated into your Python/R projects:

### Python Example
```python
# Import required libraries
import requests

# Use the {function} function
# {function_data.get('description', 'Function description here')[:100]}...

# Example implementation based on the documentation above
```

### R Example
```r
# Load required libraries
library(httr)

# Use the {function} function
# {function_data.get('description', 'Function description here')[:100]}...

# Example implementation based on the documentation above
```
"""
        claude_formatted += integration_guide
        
        # Save outputs
        filename = f"{api_name}_{function.replace('/', '_').replace('.', '_')}"
        
        if format in ['markdown', 'both']:
            md_path = formatter.save_markdown(claude_formatted, filename, subdirectory=api_name)
            console.print(f"[green]✓ Markdown saved to: {md_path}[/green]")
        
        if format in ['json', 'both']:
            formatter.save_json(function_data, filename + '_raw', subdirectory=api_name)
            metadata = formatter.generate_metadata(api_docs)
            metadata['function_name'] = function
            formatter.save_json(metadata, filename + '_metadata', subdirectory=api_name)
            console.print(f"[green]✓ JSON data saved[/green]")
        
        # Save raw HTML for reference
        html_path = formatter.output_dir / api_name / f"{filename}_raw.html"
        html_path.parent.mkdir(exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(function_data.get('raw_html', ''))
        
        console.print(f"\n[green]✓ Extraction complete![/green]")
        console.print(f"[cyan]Output directory: {formatter.output_dir / api_name}[/cyan]")
        
        # Show quick usage tip
        console.print("\n[bold]Quick tip:[/bold]")
        console.print(f"To use this in Claude Code, open the file: [yellow]{md_path}[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error saving documentation: {e}[/red]")
    
    finally:
        parser.close()


if __name__ == "__main__":
    main()