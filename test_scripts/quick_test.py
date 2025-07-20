#!/usr/bin/env python3
"""
Quick test - make sure Chrome is COMPLETELY CLOSED before running!
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import time

print("Quick Chrome Profile Test")
print("=" * 40)
print("IMPORTANT: Close Chrome completely first!")
print("Press Ctrl+C to cancel if Chrome is open")
print()

# Setup
options = webdriver.ChromeOptions()
chrome_profile = Path.home() / "Library/Application Support/Google/Chrome"

# Use Profile 11 (has Sensor Tower cookies)
profile = "Profile 11"
print(f"Using Chrome profile: {profile} (with Sensor Tower access)")

options.add_argument(f'user-data-dir={chrome_profile}')
options.add_argument(f'profile-directory={profile}')
options.add_argument('--no-sandbox')

# Start driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Test navigation
print("\nTesting navigation to Sensor Tower...")
driver.get("https://app.sensortower.com/api/docs/app_analysis")
time.sleep(5)

# Check what we got
current_url = driver.current_url
print(f"Current URL: {current_url}")

if "login" in current_url or "auth" in current_url:
    print("❌ Redirected to login - not authenticated")
else:
    print("✅ Loaded successfully - already authenticated!")
    
    # Try to find content
    page_text = driver.find_element("tag name", "body").text
    if "category_history" in page_text:
        print("✅ Found 'category_history' on the page!")
    else:
        print("❓ Could not find 'category_history' - might need to navigate")

print("\nClosing in 5 seconds...")
time.sleep(5)
driver.quit()
print("Done!")