#!/usr/bin/env python3
"""
Use existing Chrome profile for authentication
"""
import os
import sys
from pathlib import Path

def find_chrome_profile():
    """Find default Chrome profile path"""
    home = Path.home()
    
    # macOS Chrome profile location
    chrome_profile = home / "Library/Application Support/Google/Chrome"
    
    if chrome_profile.exists():
        print(f"Found Chrome profile at: {chrome_profile}")
        print("\nTo use your existing Chrome profile, run:")
        print(f"CHROME_PROFILE='{chrome_profile}' python src/main.py <url> <function>")
        print("\nNote: Make sure Chrome is closed before running this.")
        return str(chrome_profile)
    else:
        print("Chrome profile not found at default location.")
        print("You may need to locate it manually.")
        return None

if __name__ == "__main__":
    find_chrome_profile()