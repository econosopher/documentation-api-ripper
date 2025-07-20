#!/usr/bin/env python3
"""
Interactive wrapper for the Documentation API Ripper
Handles user input properly
"""
import subprocess
import sys

def main():
    print("="*60)
    print("Documentation API Ripper - Interactive Mode")
    print("="*60)
    
    # Default values
    default_url = "https://app.sensortower.com/api/docs/app_analysis"
    default_function = "category_history"
    
    # Get URL
    url = input(f"\nEnter URL (default: {default_url}): ").strip()
    if not url:
        url = default_url
    
    # Get function name
    function = input(f"Enter function name (default: {default_function}): ").strip()
    if not function:
        function = default_function
    
    print(f"\nRunning: python src/main.py {url} {function}")
    print("="*60)
    
    # Run the main script
    subprocess.call([
        sys.executable, 
        "src/main.py", 
        url, 
        function
    ])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user")
        sys.exit(0)