#!/usr/bin/env python3
"""
Demo: Profile Selection When Multiple Profiles Have Cookies

This demonstrates what happens when multiple Chrome profiles
have cookies for the target domain.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_profile_selection_demo():
    """Show how profile selection works"""
    console.print("[bold blue]Documentation API Ripper - Profile Selection Demo[/bold blue]")
    console.print("=" * 60)
    
    console.print("\n[cyan]Scenario:[/cyan] Extracting from a site where multiple Chrome profiles have cookies")
    console.print("\nWhen the tool detects cookies in multiple profiles, it will:")
    
    console.print("\n1. [green]List all profiles with cookies for the domain[/green]")
    console.print("2. [green]Show email addresses associated with each profile[/green]")
    console.print("3. [green]Display cookie count for each profile[/green]")
    console.print("4. [yellow]Let you choose which profile to use[/yellow]")
    
    # Create example table
    table = Table(title="\nExample: Multiple profiles with google.com cookies")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Profile", style="green")
    table.add_column("Email", style="yellow")
    table.add_column("Cookies", style="magenta", justify="right")
    
    table.add_row("1", "Profile 10", "pblack@sipher.xyz", "33")
    table.add_row("2", "Profile 7", "ilovbleach@gmail.com", "93")
    table.add_row("3", "Profile 14", "phillip@experimentation.group", "59")
    table.add_row("4", "Profile 15", "phil@deconstructoroffun.com", "23")
    
    console.print(table)
    
    console.print("\n[cyan]You would then enter:[/cyan]")
    console.print("- A number (1-4) to select that profile")
    console.print("- 'skip' to continue without cookies")
    
    console.print("\n[bold]Benefits:[/bold]")
    console.print("✓ No need to log in manually if you already have a session")
    console.print("✓ Can use different accounts for different APIs")
    console.print("✓ Preserves your existing Chrome sessions")
    
    console.print("\n[bold]Note:[/bold] Make sure Chrome is completely closed before running!")

if __name__ == "__main__":
    show_profile_selection_demo()