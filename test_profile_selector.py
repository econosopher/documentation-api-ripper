#!/usr/bin/env python3
"""Test Chrome profile selector integration"""

import sys
sys.path.insert(0, '.')

from src.chrome_profile_selector import ChromeProfileSelector
from src.parser import APIDocParser

def test_profile_selector():
    print("Testing Chrome Profile Selector...")
    
    # Test profile selector standalone
    selector = ChromeProfileSelector()
    profiles = selector.get_available_profiles()
    
    print(f"\nFound {len(profiles)} Chrome profiles:")
    for profile in profiles:
        print(f"  - {profile['name']}: {profile['email']}")
    
    # Test parser integration
    print("\nTesting parser integration...")
    parser = APIDocParser()
    
    # Test with a simple URL
    test_url = "https://www.google.com"
    print(f"\nTesting access check for: {test_url}")
    
    has_access, message = parser.check_access(test_url)
    print(f"Access check result: {has_access}")
    print(f"Message: {message}")
    
    # Clean up
    parser.close()
    print("\nTest completed!")

if __name__ == "__main__":
    test_profile_selector()