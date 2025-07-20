#!/usr/bin/env python3
"""
Debug cookie extraction from Chrome profile
"""
import sqlite3
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

def debug_sensortower_cookies():
    """Debug what cookies we're actually getting"""
    chrome_dir = Path.home() / "Library/Application Support/Google/Chrome"
    
    for profile_name in ["Profile 13", "Profile 15"]:
        profile_dir = chrome_dir / profile_name
        cookies_db = profile_dir / "Cookies"
        
        if not cookies_db.exists():
            continue
            
        print(f"\n{profile_name}:")
        print("=" * 50)
        
        temp_cookies = tempfile.mktemp(suffix=".db")
        try:
            shutil.copy2(cookies_db, temp_cookies)
            conn = sqlite3.connect(temp_cookies)
            cursor = conn.cursor()
            
            # Get all sensortower cookies with full details
            cursor.execute("""
                SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly, encrypted_value
                FROM cookies 
                WHERE host_key LIKE '%sensortower%'
                ORDER BY host_key, name
            """)
            
            cookies = cursor.fetchall()
            print(f"Found {len(cookies)} Sensor Tower cookies:")
            
            for cookie in cookies:
                host_key, name, value, path, expires_utc, is_secure, is_httponly, encrypted = cookie
                
                # Check if cookie is expired
                if expires_utc > 0:
                    # Convert Chrome timestamp to readable date
                    expire_date = datetime.fromtimestamp((expires_utc - 11644473600000000) / 1000000)
                    is_expired = expire_date < datetime.now()
                    expire_str = f"{expire_date} ({'EXPIRED' if is_expired else 'valid'})"
                else:
                    expire_str = "Session cookie"
                
                # Check if value is encrypted
                has_value = "Yes" if value else "No (encrypted)" if encrypted else "No value"
                
                print(f"\n  Cookie: {name}")
                print(f"    Host: {host_key}")
                print(f"    Path: {path}")
                print(f"    Secure: {bool(is_secure)}, HttpOnly: {bool(is_httponly)}")
                print(f"    Has Value: {has_value}")
                print(f"    Expires: {expire_str}")
            
            # Also check for authentication cookies
            print("\n\nChecking for common auth cookies:")
            auth_patterns = ['%session%', '%token%', '%auth%', '%jwt%']
            for pattern in auth_patterns:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM cookies 
                    WHERE host_key LIKE '%sensortower%' 
                    AND name LIKE ?
                """, (pattern,))
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"  Found {count} cookies matching '{pattern}'")
            
            conn.close()
            
        finally:
            if Path(temp_cookies).exists():
                Path(temp_cookies).unlink()

if __name__ == "__main__":
    debug_sensortower_cookies()