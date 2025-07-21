# API Specifications Directory

This directory contains the raw OpenAPI/Swagger specifications (YAML/JSON) organized by platform/game.

## Directory Structure

```
api_specs/
├── fortnite/         # Fortnite APIs
├── sensortower/      # Sensor Tower Analytics APIs
├── roblox/           # Roblox Platform APIs
├── minecraft/        # Minecraft APIs
├── steam/            # Steam Web APIs
├── epic_games/       # Epic Games Store APIs
├── unity/            # Unity Services APIs
└── playfab/          # PlayFab Backend APIs
```

## Adding New Specifications

1. **Single API per platform**: Place the YAML/JSON file directly in the platform folder
   ```
   api_specs/fortnite/ecosystem_api.yaml
   ```

2. **Multiple APIs per platform**: Use descriptive names for each API
   ```
   api_specs/sensortower/app_analysis.yml
   api_specs/sensortower/store_intelligence.yml
   api_specs/sensortower/usage_intelligence.yml
   ```

3. **Creating new platforms**: Simply create a new folder
   ```
   mkdir api_specs/my_new_platform
   ```

## Naming Conventions

- Use lowercase for folder names with underscores for spaces
- Keep original API spec filenames when possible
- Use descriptive names that indicate the API's purpose
- Both `.yaml` and `.yml` extensions are supported
- JSON files should use `.json` extension

## Extracting Specifications

Use the provided Chrome DevTools script:
```bash
# 1. Open API documentation page
# 2. Open Chrome DevTools (F12)
# 3. Paste contents of extract_swagger_yaml.js
# 4. Copy the extracted spec
# 5. Save to appropriate folder
```

Or manually from Network tab:
```bash
# 1. Open Network tab
# 2. Refresh the page
# 3. Look for .yaml, .yml, or .json files
# 4. Copy response content
# 5. Save to appropriate folder
```