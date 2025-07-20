#!/usr/bin/env python3
"""
Chrome Profile Selector for API Ripper
"""
from pathlib import Path
import json

def list_chrome_profiles():
    """List all Chrome profiles with their associated emails"""
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    profiles = {}
    
    print("Available Chrome Profiles:")
    print("=" * 50)
    
    for profile_dir in chrome_dir.glob("Profile*"):
        prefs_file = profile_dir / "Preferences"
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r') as f:
                    data = json.load(f)
                    # Look for account info
                    email = data.get('account_info', [{}])[0].get('email', 'No email found')
                    if email == 'No email found':
                        # Try another location
                        email = data.get('signin', {}).get('email', 'No email found')
                    
                    profiles[profile_dir.name] = email
                    print(f"{profile_dir.name}: {email}")
            except:
                profiles[profile_dir.name] = "Could not read profile"
                print(f"{profile_dir.name}: Could not read profile")
    
    print("\nYour deconstructoroffun.com profile is: Profile 13")
    print("\nTo use a different profile, run:")
    print("python simple_run.py <url> <function> --profile 'Profile X'")
    
    return profiles

if __name__ == "__main__":
    list_chrome_profiles()