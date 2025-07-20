#!/usr/bin/env python3
"""Test SensorTower authentication with profile selection"""

import sys
sys.path.insert(0, '.')

from src.parser import APIDocParser

def test_sensortower():
    print("Testing SensorTower authentication with Chrome profile selection...")
    
    parser = APIDocParser()
    
    # Test URL
    test_url = "https://app.sensortower.com/api/docs"
    print(f"\nTesting URL: {test_url}")
    
    # Check access
    print("\nChecking access...")
    has_access, message = parser.check_access(test_url)
    print(f"Access check result: {has_access}")
    print(f"Message: {message}")
    
    if not has_access:
        print("\nAttempting to extract function (will trigger authentication)...")
        # This will trigger the browser launch with profile selection
        result = parser.extract_function(test_url, "test_function")
        
        if 'error' in result:
            print(f"\nError: {result['error']}")
        else:
            print("\nSuccessfully accessed the page!")
            print(f"Function data: {result}")
    else:
        print("\nAlready have access! Extracting function...")
        result = parser.extract_function(test_url, "test_function")
        print(f"Result: {result}")
    
    # Clean up
    parser.close()
    print("\nTest completed!")

if __name__ == "__main__":
    test_sensortower()