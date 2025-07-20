#!/usr/bin/env python3
"""
Test the main app by auto-selecting Profile 15 when prompted
"""
import sys
import os

# Monkey-patch input to auto-select Profile 15
original_input = __builtins__.input

def mock_input(prompt):
    print(prompt, end='')
    
    if "Select profile number" in prompt:
        print("2")  # Select Profile 15
        return "2"
    elif "Choose an option" in prompt:
        print("3")  # Cancel if asked to authenticate
        return "3"
    elif "Preview looks good?" in prompt:
        print("y")  # Confirm preview
        return "y"
    else:
        # For any other prompt, use default
        print("")
        return ""

__builtins__.input = mock_input

# Now import and run the main module
try:
    from src.main import main
    
    # Run with test arguments
    sys.argv = [
        'main.py',
        'https://app.sensortower.com/api/docs/app_analysis',
        'category_history'
    ]
    
    print("Running Documentation API Ripper with auto-selected Profile 15...")
    print("="*60)
    
    main()
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Restore original input
    __builtins__.input = original_input