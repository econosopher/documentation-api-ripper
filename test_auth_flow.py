#!/usr/bin/env python3
"""Test authentication flow with Safe Mode"""

import sys
import time
sys.path.insert(0, '.')

from src.parser import APIDocParser

def test_authentication_flow():
    """Test the complete authentication flow with SensorTower"""
    
    print("\n=== Testing Authentication Flow with Safe Mode ===\n")
    
    # Test configuration
    test_url = "https://app.sensortower.com/api/docs"
    test_function = "getUserInfo"
    
    parser = APIDocParser()
    
    try:
        # Step 1: Check available profiles
        print("Step 1: Checking available Chrome profiles...")
        has_access, message = parser.check_access(test_url)
        print(f"Result: {message}\n")
        
        # Step 2: Launch browser with profile selection
        print("Step 2: Launching browser with profile selection...")
        print("Note: If Chrome is running, you'll be offered Safe Mode\n")
        
        # Initialize the browser (this will trigger profile selection)
        if not parser.driver:
            parser.driver = parser._init_driver()
            print("\n✓ Browser launched successfully!")
        
        # Step 3: Navigate to SensorTower
        print("\nStep 3: Navigating to SensorTower...")
        parser.driver.get(test_url)
        time.sleep(3)
        
        # Check if we're redirected to login
        current_url = parser.driver.current_url
        print(f"Current URL: {current_url}")
        
        if "sign_in" in current_url or "login" in current_url:
            print("\n⚠️  Redirected to login page - authentication required")
            print("\nStep 4: Starting authentication process...")
            
            # Use the authentication manager
            success = parser.authenticate_google(return_to_url=test_url)
            
            if success:
                print("\n✅ Authentication successful!")
                
                # Try to extract the function
                print(f"\nStep 5: Attempting to extract function '{test_function}'...")
                result = parser.extract_function(test_url, test_function)
                
                if 'error' in result:
                    print(f"Function extraction error: {result['error']}")
                else:
                    print("✅ Function extracted successfully!")
                    print("\nPreview:")
                    print(parser.get_preview(result))
            else:
                print("\n❌ Authentication failed or was cancelled")
        else:
            print("\n✅ Already authenticated! No login required.")
            
            # Try to extract the function
            print(f"\nStep 5: Attempting to extract function '{test_function}'...")
            result = parser.extract_function(test_url, test_function)
            
            if 'error' in result:
                print(f"Function extraction error: {result['error']}")
            else:
                print("✅ Function extracted successfully!")
                print("\nPreview:")
                print(parser.get_preview(result))
        
        # Keep browser open for inspection
        input("\n\nPress Enter to close the browser and exit...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        parser.close()
        print("\n✓ Browser closed and cleanup completed")

if __name__ == "__main__":
    print("This script will test the authentication flow with SensorTower.")
    print("It will:")
    print("1. Let you select a Chrome profile (with Safe Mode if Chrome is running)")
    print("2. Navigate to SensorTower API docs")
    print("3. Handle authentication if needed")
    print("4. Attempt to extract a function from the docs")
    print("\nWhen Google's 2FA/verification triggers, please complete it in the browser.")
    
    confirm = input("\nReady to start? (y/n): ")
    if confirm.lower() == 'y':
        test_authentication_flow()
    else:
        print("Test cancelled.")