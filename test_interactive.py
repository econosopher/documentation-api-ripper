#!/usr/bin/env python3
"""Interactive test for Chrome profile selection and authentication"""

import sys
sys.path.insert(0, '.')

from src.parser import APIDocParser

def main():
    print("\n=== Documentation API Ripper - Interactive Test ===\n")
    
    # Test URL
    test_url = "https://app.sensortower.com/api/docs"
    function_name = "getUserInfo"  # Example function to search for
    
    # Create parser
    parser = APIDocParser()
    
    try:
        # Check access
        print(f"Testing URL: {test_url}")
        print("\nChecking for available Chrome profiles...\n")
        
        has_access, message = parser.check_access(test_url)
        print(f"\nAccess status: {message}\n")
        
        # Try to extract a function (this will trigger browser launch with profile selection)
        print(f"Attempting to extract function '{function_name}'...")
        print("This will launch Chrome with profile selection.\n")
        
        result = parser.extract_function(test_url, function_name)
        
        if 'error' in result:
            print(f"\nError: {result['error']}")
        else:
            print("\nSuccess! Here's what was found:")
            print(parser.get_preview(result))
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Clean up
        if parser.driver:
            parser.close()
            print("\nBrowser closed.")
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()