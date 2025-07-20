#!/usr/bin/env python3
"""
Test what content we're actually getting from the page
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from rich.console import Console

console = Console()

def test_page_content():
    """See what we're actually getting from the Sensor Tower page"""
    
    console.print("[cyan]Testing page content extraction...[/cyan]")
    
    # Set up Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Use temp profile
    import os
    profile_dir = os.path.abspath('./chrome_profile_test')
    options.add_argument(f'user-data-dir={profile_dir}')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to the page
        url = "https://app.sensortower.com/api/docs/app_analysis"
        console.print(f"\n[cyan]Navigating to: {url}[/cyan]")
        driver.get(url)
        
        # Wait a bit
        time.sleep(5)
        
        # Check current URL (might redirect to login)
        console.print(f"\n[yellow]Current URL: {driver.current_url}[/yellow]")
        
        # Get page title
        console.print(f"[yellow]Page Title: {driver.title}[/yellow]")
        
        # Get page source and analyze
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Look for common indicators
        console.print("\n[cyan]Page Analysis:[/cyan]")
        
        # Check for login forms
        login_forms = soup.find_all(['form', 'button'], text=lambda t: t and ('sign' in t.lower() or 'login' in t.lower()))
        if login_forms:
            console.print("[red]✗ Login page detected[/red]")
        
        # Check for API documentation elements
        api_elements = soup.find_all(text=lambda t: t and 'category_history' in t if t else False)
        if api_elements:
            console.print(f"[green]✓ Found 'category_history' mentioned {len(api_elements)} times[/green]")
        else:
            console.print("[red]✗ 'category_history' not found on page[/red]")
        
        # Look for any text containing "api" or "endpoint"
        api_content = soup.find_all(text=lambda t: t and ('api' in t.lower() or 'endpoint' in t.lower()) if t else False)
        console.print(f"\n[cyan]Found {len(api_content)} elements with 'api' or 'endpoint'[/cyan]")
        
        # Save page source for inspection
        with open("page_source.html", "w") as f:
            f.write(driver.page_source)
        console.print("\n[green]Page source saved to page_source.html[/green]")
        
        # Take screenshot
        driver.save_screenshot("page_screenshot.png")
        console.print("[green]Screenshot saved to page_screenshot.png[/green]")
        
        console.print("\n[bold]Summary:[/bold]")
        if "accounts.google.com" in driver.current_url or "login" in driver.current_url.lower():
            console.print("[red]You're on a login page - authentication is required[/red]")
        elif not api_elements:
            console.print("[yellow]Page loaded but 'category_history' not found - might be wrong page or need to navigate[/yellow]")
        else:
            console.print("[green]Documentation page loaded successfully[/green]")
            
    finally:
        driver.quit()
        console.print("\n[dim]Browser closed[/dim]")

if __name__ == "__main__":
    test_page_content()