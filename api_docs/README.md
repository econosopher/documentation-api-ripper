# API Documentation Directory

This directory contains the converted Markdown documentation generated from the API specifications.

## Directory Structure

```
api_docs/
├── index.md          # Master index of all documentation
├── fortnite/         # Fortnite API documentation
│   └── index.md      # Platform-specific index
├── sensortower/      # Sensor Tower API documentation
│   └── index.md      # Platform-specific index
├── roblox/           # Roblox API documentation
│   └── index.md      # Platform-specific index
└── ...               # Other platforms
```

## Generated Files

Each API specification is converted to a Markdown file with:
- Comprehensive API overview
- Authentication methods
- All endpoints with parameters
- Request/response schemas
- Data models and types

## Viewing Documentation

1. **Master Index**: Start with `api_docs/index.md` for an overview of all APIs
2. **Platform Index**: Each platform has its own `index.md` listing all APIs
3. **Individual APIs**: Each `.md` file contains complete documentation for one API

## Automatic Features

- **Smart Titles**: Extracted from API specification or filename
- **Version Info**: Included when available in the spec
- **Organized Structure**: Endpoints grouped by tags/categories
- **Cross-References**: Links between related documentation
- **Timestamps**: Generation date for tracking updates

## Regenerating Documentation

Use the batch converter to update documentation:
```bash
# Convert all new/updated specs
python3 batch_convert.py

# Convert only one platform
python3 batch_convert.py -p sensortower

# Force regenerate all docs
python3 batch_convert.py --force
```