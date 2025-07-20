#!/bin/bash
# Script to run the Documentation API Ripper

# Activate virtual environment
source venv/bin/activate

# Run the tool
python src/main.py https://app.sensortower.com/api/docs/app_analysis "category_history"