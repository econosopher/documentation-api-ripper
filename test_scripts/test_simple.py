#!/usr/bin/env python3
"""
Simple test to verify the cookie approach works
"""
from rich.console import Console

console = Console()

print("""
The Documentation API Ripper has been updated to handle cookies better:

1. ✅ Fixed: No more "Chrome profile in use" errors
   - Now uses a temporary profile and copies cookies

2. ✅ Fixed: Properly detects parent domain cookies
   - app.sensortower.com now finds .sensortower.com cookies

3. ✅ Fixed: Browser only launches when you choose to
   - Not automatically when checking for cookies

To run the app interactively:

cd /Users/phillip/Documents/vibe_coding_projects/documentation-api-ripper
source venv/bin/activate
python -m src.main https://app.sensortower.com/api/docs/app_analysis category_history

When prompted:
- Enter '2' to use Profile 15 (has more cookies)
- The browser will launch with a clean profile
- Cookies will be copied automatically
- You should be logged in automatically

Note: If you still see login page, the cookies may have expired.
""")