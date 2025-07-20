#!/usr/bin/env python3
"""
Profile Helper - Manage and use existing authenticated profiles
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.profile_manager import ChromeProfileManager
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import shutil
import time

console = Console()

def show_profile_info():
    """Show information about existing profiles"""
    console.print("[bold cyan]Chrome Profile Helper[/bold cyan]")
    console.print("\n[yellow]⚠️  Important: Sensor Tower limits to 3 new browsers per 24 hours[/yellow]")
    console.print("[dim]To avoid lockouts, always use the same profile![/dim]\n")
    
    manager = ChromeProfileManager()
    
    # Show app profiles
    app_profiles = manager.list_app_profiles()
    if app_profiles:
        console.print("[bold green]Your Persistent API Ripper Profiles:[/bold green]")
        console.print("[dim]These profiles maintain your login sessions[/dim]\n")
        
        table = Table(show_header=True)
        table.add_column("Profile Name", style="cyan")
        table.add_column("Path", style="dim")
        table.add_column("Size", justify="right")
        
        for name, path, _ in app_profiles:
            # Calculate size
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
            
            size_mb = total_size / (1024 * 1024)
            profile_name = name.replace("API Ripper: ", "")
            table.add_row(profile_name, path, f"{size_mb:.1f} MB")
        
        console.print(table)
    else:
        console.print("[yellow]No persistent profiles found yet.[/yellow]")
        console.print("[dim]Create one to avoid repeated logins![/dim]")
    
    console.print("\n[bold]Quick Actions:[/bold]")
    console.print("1. Use existing profile (no new device registration)")
    console.print("2. Create ONE persistent profile (use this same one always)")
    console.print("3. Check which Chrome profiles exist")
    console.print("4. Clean up temporary profiles")
    console.print("5. Exit")
    
    return Prompt.ask("\n[cyan]Choose action[/cyan]", choices=["1", "2", "3", "4", "5"])

def use_existing_profile():
    """Launch browser with existing profile"""
    manager = ChromeProfileManager()
    app_profiles = manager.list_app_profiles()
    
    if not app_profiles:
        console.print("[red]No existing profiles found![/red]")
        console.print("[yellow]You need to create one persistent profile first.[/yellow]")
        return
    
    console.print("\n[cyan]Select profile to use:[/cyan]")
    for i, (name, path, _) in enumerate(app_profiles, 1):
        profile_name = name.replace("API Ripper: ", "")
        console.print(f"{i}. {profile_name}")
    
    choice = Prompt.ask("[cyan]Select profile number[/cyan]")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(app_profiles):
            _, profile_path, _ = app_profiles[idx]
            
            console.print(f"\n[green]Using profile: {profile_path}[/green]")
            console.print("[dim]This won't count as a new device![/dim]")
            
            # Launch with profile
            driver = manager.create_driver(profile_path)
            
            console.print("\n[green]✓ Browser launched with existing profile[/green]")
            console.print("[yellow]Press Ctrl+C to close when done[/yellow]")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                driver.quit()
                console.print("\n[green]✓ Browser closed[/green]")
    except:
        console.print("[red]Invalid selection[/red]")

def create_single_profile():
    """Create ONE persistent profile to use always"""
    manager = ChromeProfileManager()
    
    console.print("\n[yellow]Creating ONE persistent profile[/yellow]")
    console.print("[dim]Use this same profile every time to avoid device limits![/dim]\n")
    
    name = Prompt.ask(
        "[cyan]Enter profile name[/cyan]",
        default="sensortower_main"
    )
    
    profile_path = manager.create_app_profile(name)
    
    console.print(f"\n[green]✓ Created profile: {name}[/green]")
    console.print(f"[dim]Location: {profile_path}[/dim]")
    console.print("\n[bold yellow]⚠️  IMPORTANT:[/bold yellow]")
    console.print("1. Always use this same profile")
    console.print("2. Don't create new profiles unnecessarily")
    console.print("3. This profile will maintain your login session")
    
    if Prompt.ask("\n[cyan]Launch browser with this profile now? (y/n)[/cyan]", default="y") == "y":
        driver = manager.create_driver(profile_path)
        console.print("\n[green]✓ Browser launched[/green]")
        console.print("[yellow]Login once, and it will be saved for future use[/yellow]")
        console.print("[dim]Press Ctrl+C to close when done[/dim]")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            driver.quit()
            console.print("\n[green]✓ Profile saved with your login![/green]")

def check_chrome_profiles():
    """Show all Chrome profiles on system"""
    console.print("\n[cyan]Checking Chrome profiles...[/cyan]")
    
    chrome_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    if os.path.exists(chrome_dir):
        profiles = []
        for item in os.listdir(chrome_dir):
            item_path = os.path.join(chrome_dir, item)
            if os.path.isdir(item_path) and (item == "Default" or item.startswith("Profile")):
                profiles.append(item)
        
        if profiles:
            console.print(f"\n[green]Found {len(profiles)} Chrome profiles:[/green]")
            for profile in profiles:
                console.print(f"  - {profile}")
            console.print("\n[dim]Note: Using your actual Chrome profiles may interfere with your browsing[/dim]")
        else:
            console.print("[yellow]No Chrome profiles found[/yellow]")
    else:
        console.print("[yellow]Chrome directory not found[/yellow]")

def cleanup_temp_profiles():
    """Remove temporary profile directories"""
    console.print("\n[yellow]Cleaning up temporary profiles...[/yellow]")
    
    temp_dirs = ["/tmp", "/var/folders", os.path.expanduser("~/Library/Caches")]
    cleaned = 0
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir):
                for d in dirs:
                    if d.startswith("api_ripper_temp_") or d.startswith("chrome_profile_"):
                        try:
                            dir_path = os.path.join(root, d)
                            shutil.rmtree(dir_path)
                            cleaned += 1
                            console.print(f"[dim]Removed: {dir_path}[/dim]")
                        except:
                            pass
    
    console.print(f"\n[green]✓ Cleaned up {cleaned} temporary profiles[/green]")

def main():
    """Main function"""
    while True:
        try:
            choice = show_profile_info()
            
            if choice == "1":
                use_existing_profile()
            elif choice == "2":
                create_single_profile()
            elif choice == "3":
                check_chrome_profiles()
            elif choice == "4":
                cleanup_temp_profiles()
            elif choice == "5":
                break
            
            console.print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    console.print("\n[cyan]Remember: Always use the same profile to avoid device limits![/cyan]")

if __name__ == "__main__":
    main()