#!/usr/bin/env python3
"""
Interactive authentication script for storing Google OAuth sessions
Run this directly in your terminal
"""
import sys
from pathlib import Path

print("""
==============================================================
Google Authentication Setup for Documentation API Ripper
==============================================================

This script will help you authenticate and store your session.

To run this authentication:

1. Open a terminal
2. Navigate to the project directory:
   cd /Users/phillip/Documents/vibe_coding_projects/documentation-api-ripper

3. Activate the virtual environment:
   source venv/bin/activate

4. Run the authentication:
   python -m src.main https://app.sensortower.com/api/docs/app_analysis category_history

5. When prompted:
   - Choose option 1 to launch browser
   - The new authentication system will show a progress indicator
   - You'll have 5 minutes to complete the login
   - Sign in with your Google account
   - The session will be automatically saved

Once authenticated, future runs will use the stored session!

The session will be saved in: ./oauth_tokens/sensortower.com_session.json

==============================================================
""")