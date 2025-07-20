#!/usr/bin/env python3
"""
Standalone test - creates a fresh Chrome instance
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Standalone Chrome Test")
print("=" * 40)

# Simple options without profile
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')

# Create a new temporary profile
import tempfile
temp_dir = tempfile.mkdtemp()
options.add_argument(f'user-data-dir={temp_dir}')

print(f"Using temporary profile at: {temp_dir}")

# Start driver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    print("\nNavigating to Sensor Tower API docs...")
    driver.get("https://app.sensortower.com/api/docs/app_analysis")
    
    # Wait a bit
    time.sleep(5)
    
    # Check where we ended up
    current_url = driver.current_url
    print(f"\nCurrent URL: {current_url}")
    
    if "login" in current_url or "auth" in current_url:
        print("\n❌ Redirected to login page")
        print("This is expected - you'll need to sign in")
        print("\nNext steps:")
        print("1. Sign in manually in the browser that opened")
        print("2. Navigate to the API docs")
        print("3. Then we can extract the documentation")
    else:
        print("\n✅ Loaded API docs successfully!")
    
    print("\nBrowser will stay open for 30 seconds...")
    print("You can sign in during this time if needed")
    time.sleep(30)
    
finally:
    driver.quit()
    print("\nDone!")