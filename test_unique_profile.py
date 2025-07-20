#!/usr/bin/env python3
"""
Test script to verify unique Chrome profile solution
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.chrome_manager import ChromeManager
from rich.console import Console
import time

console = Console()

def test_unique_profiles():
    """Test creating multiple Chrome instances with unique profiles"""
    console.print("[bold cyan]Testing Unique Chrome Profile Solution[/bold cyan]")
    console.print()
    
    # Test 1: Create single instance
    console.print("[yellow]Test 1: Creating single Chrome instance...[/yellow]")
    try:
        with ChromeManager() as manager:
            driver = manager.create_driver()
            console.print("[green]✓ Successfully created Chrome instance[/green]")
            driver.get("https://www.google.com")
            console.print(f"[dim]Current URL: {driver.current_url}[/dim]")
            time.sleep(2)
        console.print("[green]✓ Chrome instance closed and cleaned up[/green]")
        console.print()
    except Exception as e:
        console.print(f"[red]✗ Test 1 failed: {e}[/red]")
        console.print()
        return False
    
    # Test 2: Create multiple instances sequentially
    console.print("[yellow]Test 2: Creating multiple instances sequentially...[/yellow]")
    for i in range(3):
        try:
            with ChromeManager() as manager:
                driver = manager.create_driver()
                console.print(f"[green]✓ Instance {i+1} created successfully[/green]")
                driver.get(f"https://www.example.com/?test={i+1}")
                time.sleep(1)
        except Exception as e:
            console.print(f"[red]✗ Failed to create instance {i+1}: {e}[/red]")
            return False
    console.print("[green]✓ All sequential instances created successfully[/green]")
    console.print()
    
    # Test 3: Test with existing Chrome profile
    console.print("[yellow]Test 3: Testing with existing Chrome profile...[/yellow]")
    try:
        chrome_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        if os.path.exists(chrome_dir):
            with ChromeManager() as manager:
                driver = manager.create_driver(base_profile=chrome_dir)
                console.print("[green]✓ Created instance with profile copy[/green]")
                driver.get("https://app.sensortower.com")
                console.print(f"[dim]Current URL: {driver.current_url}[/dim]")
                time.sleep(2)
        else:
            console.print("[yellow]Chrome profile directory not found, skipping...[/yellow]")
    except Exception as e:
        console.print(f"[red]✗ Test 3 failed: {e}[/red]")
    
    console.print()
    console.print("[bold green]All tests completed![/bold green]")
    return True

if __name__ == "__main__":
    try:
        test_unique_profiles()
    except KeyboardInterrupt:
        console.print("\n[yellow]Tests interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")