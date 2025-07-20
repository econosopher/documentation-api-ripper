#!/usr/bin/env python3
"""
Copy cookies from Chrome profile to use for authentication
"""
import sqlite3
import shutil
from pathlib import Path
import tempfile
import json

def check_all_profiles():
    """Check all Chrome profiles for Sensor Tower cookies"""
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    
    for profile_dir in chrome_dir.glob("Profile*"):
        cookies_db = profile_dir / "Cookies"
        if cookies_db.exists():
            # Copy cookies database to temp location
            temp_cookies = tempfile.mktemp(suffix=".db")
            try:
                shutil.copy2(cookies_db, temp_cookies)
                
                conn = sqlite3.connect(temp_cookies)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM cookies 
                    WHERE host_key LIKE '%sensortower.com%'
                """)
                
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"✓ {profile_dir.name}: Found {count} Sensor Tower cookies")
                    
                    # Get email for this profile
                    prefs_file = profile_dir / "Preferences"
                    email = "unknown"
                    if prefs_file.exists():
                        import json
                        try:
                            with open(prefs_file) as f:
                                data = json.load(f)
                                email = data.get('account_info', [{}])[0].get('email', 'unknown')
                        except:
                            pass
                    print(f"  Email: {email}")
                
                conn.close()
            except Exception as e:
                print(f"  Error reading {profile_dir.name}: {e}")
            finally:
                if Path(temp_cookies).exists():
                    Path(temp_cookies).unlink()

def copy_chrome_cookies(profile_name="Profile 13"):
    """Copy cookies from Chrome profile"""
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    profile_dir = chrome_dir / profile_name
    cookies_db = profile_dir / "Cookies"
    
    if not cookies_db.exists():
        print(f"Could not find cookies database at: {cookies_db}")
        return None
    
    # Copy cookies database to temp location (Chrome locks the original)
    temp_cookies = tempfile.mktemp(suffix=".db")
    shutil.copy2(cookies_db, temp_cookies)
    
    print(f"Copied cookies from {profile_name}")
    
    # Extract Sensor Tower cookies
    conn = sqlite3.connect(temp_cookies)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
            FROM cookies 
            WHERE host_key LIKE '%sensortower.com%'
        """)
        
        cookies = cursor.fetchall()
        print(f"Found {len(cookies)} Sensor Tower cookies")
        
        # Show some cookie names (not values for security)
        for cookie in cookies[:5]:
            print(f"  - {cookie[1]} from {cookie[0]}")
        
        return cookies
        
    finally:
        conn.close()
        Path(temp_cookies).unlink()

if __name__ == "__main__":
    print("Checking all Chrome profiles for Sensor Tower cookies...")
    print("=" * 50)
    check_all_profiles()
    print("\nChecking Profile 13 specifically...")
    copy_chrome_cookies()