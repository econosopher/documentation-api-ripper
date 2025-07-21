#!/usr/bin/env python3
"""
API Documentation Ripper - Convert API Specs to Markdown
"""
import sys
from pathlib import Path

def main():
    """Display usage information"""
    print("API Documentation Ripper")
    print("========================")
    print("\nConvert OpenAPI/Swagger specifications to well-organized Markdown documentation.")
    print("\nUsage:")
    print("  python openapi_to_markdown.py <spec-file> [options]")
    print("\nExamples:")
    print("  # Convert YAML spec to markdown (output to console)")
    print("  python openapi_to_markdown.py api-spec.yaml")
    print("\n  # Convert JSON spec to markdown file")
    print("  python openapi_to_markdown.py api-spec.json -o api-docs.md")
    print("\n  # Convert with custom title")
    print("  python openapi_to_markdown.py spec.yaml --title 'My API v2.0' -o docs.md")
    print("\nOrganized workflow:")
    print("  1. Save YAML/JSON files to api_specs/{platform}/")
    print("  2. Run: python3 batch_convert.py")
    print("  3. Find docs in api_docs/{platform}/")
    print("\nCurrent platforms:")
    print("  - api_specs/fortnite/")
    print("  - api_specs/sensortower/")
    print("\nFor more details, see README.md")

if __name__ == "__main__":
    main()