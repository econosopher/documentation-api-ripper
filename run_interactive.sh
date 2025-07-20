#!/bin/bash
# Interactive script for Documentation API Ripper

echo "Starting Documentation API Ripper..."
echo "=================================="
echo ""
echo "This script will:"
echo "1. Open Chrome browser"
echo "2. Navigate to Sensor Tower API docs"
echo "3. Wait for you to sign in"
echo "4. Extract the category_history function"
echo ""
echo "Press Enter to start..."
read

# Activate virtual environment and run
source venv/bin/activate
python src/main.py https://app.sensortower.com/api/docs/app_analysis "category_history"