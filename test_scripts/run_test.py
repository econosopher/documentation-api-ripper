#!/usr/bin/env python3
import subprocess
import sys

# Run the main script
subprocess.run([
    sys.executable, 
    "src/main.py", 
    "https://app.sensortower.com/api/docs/app_analysis",
    "category_history"
])