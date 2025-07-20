#!/usr/bin/env python3
"""
Test to identify why browser quits during authentication
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from rich.console import Console

console = Console()

def test_browser_lifecycle():
    """Test browser lifecycle and identify timeout issues"""
    
    console.print("[cyan]Testing Browser Lifecycle[/cyan]")
    console.print("="*50)
    
    # Set up Chrome with same options as parser
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Use temporary profile
    import os
    profile_dir = os.path.abspath('./chrome_profile_test')
    options.add_argument(f'user-data-dir={profile_dir}')
    
    console.print("[cyan]Starting Chrome...[/cyan]")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to Google login
        console.print("\n[cyan]Navigating to Google login...[/cyan]")
        driver.get("https://accounts.google.com")
        
        console.print("\n[yellow]Browser is now open. Testing different scenarios:[/yellow]")
        console.print("1. The browser should stay open indefinitely")
        console.print("2. Try signing in - see if it affects browser stability")
        console.print("3. Press Ctrl+C when done testing\n")
        
        # Keep browser open with periodic status updates
        start_time = time.time()
        while True:
            elapsed = int(time.time() - start_time)
            
            # Check if browser is still responsive
            try:
                current_url = driver.current_url
                title = driver.title
                console.print(f"\r[dim]Browser alive for {elapsed}s - URL: {current_url[:50]}... Title: {title[:30]}...[/dim]", end="")
                
                # Check for any JavaScript errors
                logs = driver.get_log('browser')
                if logs:
                    console.print(f"\n[yellow]Browser console logs:[/yellow]")
                    for log in logs[-5:]:  # Last 5 logs
                        console.print(f"  {log['level']}: {log['message'][:100]}...")
                        
            except Exception as e:
                console.print(f"\n[red]Browser became unresponsive: {e}[/red]")
                break
                
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Test interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Browser crashed or closed: {e}[/red]")
        console.print("[red]This might be the issue![/red]")
    finally:
        console.print("\n[cyan]Closing browser...[/cyan]")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    test_browser_lifecycle()