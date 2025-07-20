#!/usr/bin/env python3
"""
Demo script showing how to use the Documentation API Ripper
"""
from src.parser import APIDocParser
from src.converter import HTMLToMarkdownConverter
from src.formatter import OutputFormatter
from rich.console import Console

console = Console()

def main():
    """Demo of the API ripper workflow"""
    console.print("[bold blue]Documentation API Ripper - Demo[/bold blue]")
    console.print("=" * 50)
    
    # Configuration
    url = "https://app.sensortower.com/api/docs/app_analysis"
    function_name = "category_history"
    
    console.print(f"\n[cyan]Target URL:[/cyan] {url}")
    console.print(f"[cyan]Function to extract:[/cyan] {function_name}")
    
    # Initialize components
    parser = APIDocParser()
    
    console.print("\n[yellow]Note: This demo shows the workflow.[/yellow]")
    console.print("[yellow]When you run the actual tool, it will:[/yellow]")
    console.print("1. Check if authentication is needed")
    console.print("2. Open Chrome browser for Google sign-in if required")
    console.print("3. Extract the function documentation")
    console.print("4. Show a preview for verification")
    console.print("5. Save formatted output for Claude Code")
    
    console.print("\n[green]To run the actual tool:[/green]")
    console.print("[bold]python src/main.py https://app.sensortower.com/api/docs/app_analysis category_history[/bold]")
    
    console.print("\n[cyan]The tool will handle authentication automatically.[/cyan]")
    console.print("[cyan]Just complete the Google sign-in when the browser opens.[/cyan]")

if __name__ == "__main__":
    main()