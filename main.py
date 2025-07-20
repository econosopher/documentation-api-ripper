#!/usr/bin/env python3
"""
API Documentation Ripper - Main Entry Point
"""
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    """Display available tools and usage"""
    console.print(Panel.fit(
        "[bold cyan]API Documentation Ripper[/bold cyan]\n"
        "Extract and parse API documentation from various formats",
        border_style="cyan"
    ))
    
    console.print("\n[bold yellow]Available Tools:[/bold yellow]\n")
    
    tools = [
        ("manage_profiles", "Manage persistent Chrome profiles to avoid repeated logins"),
        ("search_highlight", "Simple text search and highlighting in API docs"),
        ("search_persistent", "Search with persistent session (stays logged in)"),
        ("detect_api_format", "Detect API format (Swagger, Redoc, etc.) and extract endpoints"),
        ("extract_api_docs", "Interactive API documentation extraction tool")
    ]
    
    for tool, description in tools:
        console.print(f"  [cyan]./bin/{tool}.py[/cyan]")
        console.print(f"    {description}\n")
    
    console.print("[bold yellow]Quick Start:[/bold yellow]")
    console.print("1. First, create a persistent profile to avoid repeated logins:")
    console.print("   [cyan]python bin/manage_profiles.py[/cyan]\n")
    
    console.print("2. Then use any of the search tools:")
    console.print("   [cyan]python bin/search_persistent.py[/cyan]")
    console.print("   [cyan]python bin/detect_api_format.py[/cyan]\n")
    
    console.print("[dim]For more information, see README.md[/dim]")

if __name__ == "__main__":
    main()