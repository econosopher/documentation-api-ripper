"""
Improved authentication manager with better timeout handling
"""
import time
from typing import Optional, Callable
from selenium import webdriver
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class AuthenticationManager:
    """Manages authentication with proper timeout handling"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        
    def wait_for_authentication(
        self, 
        check_fn: Callable[[], bool],
        timeout_seconds: int = 300,  # 5 minutes default
        check_interval: int = 5
    ) -> bool:
        """
        Wait for user to complete authentication with visual feedback
        
        Args:
            check_fn: Function that returns True when authenticated
            timeout_seconds: Maximum time to wait (default 5 minutes)
            check_interval: How often to check (seconds)
        
        Returns:
            True if authenticated, False if timeout
        """
        console.print("\n[yellow]Waiting for authentication...[/yellow]")
        console.print(f"[dim]Timeout: {timeout_seconds} seconds ({timeout_seconds//60} minutes)[/dim]")
        console.print("[dim]Press Ctrl+C to cancel at any time[/dim]\n")
        
        start_time = time.time()
        last_url = None
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            task = progress.add_task(
                "[cyan]Waiting for login completion...", 
                total=timeout_seconds
            )
            
            while (time.time() - start_time) < timeout_seconds:
                try:
                    # Update progress
                    elapsed = int(time.time() - start_time)
                    progress.update(task, completed=elapsed)
                    
                    # Check current URL to provide feedback
                    try:
                        current_url = self.driver.current_url
                        if current_url != last_url:
                            last_url = current_url
                            # Show URL changes (helps user understand what's happening)
                            if "accounts.google.com" in current_url:
                                progress.update(task, description="[cyan]On Google login page...")
                            elif "consent" in current_url:
                                progress.update(task, description="[cyan]On consent page...")
                            elif "sensortower.com" in current_url and "sign_in" not in current_url:
                                progress.update(task, description="[green]Redirecting to app...")
                    except:
                        pass  # Browser might be in transition
                    
                    # Check if authenticated
                    if check_fn():
                        progress.update(task, description="[green]Authentication successful!")
                        return True
                    
                    time.sleep(check_interval)
                    
                except KeyboardInterrupt:
                    console.print("\n[yellow]Authentication cancelled by user[/yellow]")
                    return False
                except Exception as e:
                    console.print(f"\n[red]Error during authentication: {e}[/red]")
                    return False
            
            # Timeout reached
            console.print(f"\n[red]Authentication timeout after {timeout_seconds} seconds[/red]")
            console.print("[yellow]Tips:[/yellow]")
            console.print("- Try running the command again")
            console.print("- Make sure you complete the login process")
            console.print("- Check if pop-ups are blocked")
            
            return False
    
    def interactive_authentication(
        self,
        login_url: str,
        success_check_fn: Callable[[], bool],
        timeout_seconds: int = 300
    ) -> bool:
        """
        Handle interactive authentication with better user experience
        """
        console.print(f"\n[cyan]Opening login page: {login_url}[/cyan]")
        
        try:
            self.driver.get(login_url)
            time.sleep(2)  # Give page time to load
            
            # Show options to user
            console.print("\n[yellow]Authentication Options:[/yellow]")
            console.print("1. [green]Auto-wait[/green] - Wait for you to complete login (recommended)")
            console.print("2. [yellow]Manual[/yellow] - Press Enter when done")
            console.print("3. [red]Cancel[/red] - Skip authentication")
            
            choice = console.input("\n[cyan]Choose option (1-3) [[1]]:[/cyan] ").strip() or "1"
            
            if choice == "1":
                # Auto-wait with timeout
                return self.wait_for_authentication(success_check_fn, timeout_seconds)
                
            elif choice == "2":
                # Manual confirmation
                console.print("\n[yellow]Please complete the login process in the browser[/yellow]")
                console.input("[cyan]Press Enter when done...[/cyan]")
                
                # Verify authentication worked
                if success_check_fn():
                    console.print("[green]✓ Authentication successful![/green]")
                    return True
                else:
                    console.print("[red]✗ Authentication verification failed[/red]")
                    retry = console.input("[yellow]Try again? (y/n):[/yellow] ").lower()
                    return retry == 'y'
                    
            else:
                console.print("[yellow]Authentication cancelled[/yellow]")
                return False
                
        except Exception as e:
            console.print(f"[red]Authentication error: {e}[/red]")
            return False