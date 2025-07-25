# API Documentation Ripper

Convert OpenAPI/Swagger specifications to clean, organized Markdown documentation.

## Features

- 🔄 Convert OpenAPI 3.x and Swagger 2.0 specifications
- 📝 Generate well-structured Markdown documentation
- 🎯 Support for YAML and JSON formats
- 🔍 Extract API specs from Swagger UI pages
- 📚 Organize endpoints by tags/categories
- 🔐 Document authentication methods
- 📊 Include request/response schemas

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/documentation-api-ripper.git
cd documentation-api-ripper

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Conversion

```bash
# Convert YAML spec to markdown (outputs to console)
python openapi_to_markdown.py api-spec.yaml

# Convert JSON spec to markdown file
python openapi_to_markdown.py api-spec.json -o api-documentation.md

# Convert with custom title
python openapi_to_markdown.py spec.yaml --title "My API v2.0" -o docs.md
```

### Extract API Specs from Swagger UI Pages

Many APIs only provide their documentation through Swagger UI web pages. Here's how to extract the raw OpenAPI/Swagger specification:

#### Method 1: Using Chrome DevTools (Recommended)

1. **Open the Swagger UI page** in Chrome
2. **Open Developer Tools** (F12 or Cmd+Option+I on Mac)
3. **Go to the Console tab**
4. **Copy and paste** the entire contents of `extract_swagger_yaml.js`
5. **Press Enter** to run the script
6. **Copy the extracted specification** from the console output
7. **Save to a file** (e.g., `api-spec.yaml` or `api-spec.json`)
8. **Convert to Markdown** using this tool

The extraction script automatically:
- Detects the API specification location
- Handles both YAML and JSON formats
- Tries multiple methods to find the spec
- Provides the raw specification without UI elements

#### Method 2: Quick Bookmarklet

For frequent use, create a bookmarklet:

1. **Create a new bookmark** in your browser
2. **Set the URL** to the contents of `swagger_extractor_bookmarklet.js`
3. **Click the bookmarklet** when viewing any Swagger UI page
4. **Check the console** for the extracted specification

#### Method 3: Manual Extraction

If the automated methods don't work:

1. **Open Developer Tools** → **Network tab**
2. **Refresh the page**
3. **Look for requests** to files like:
   - `openapi.yaml`
   - `openapi.json`
   - `swagger.json`
   - `api-docs`
4. **Click on the file** to view its contents
5. **Copy and save** the specification

### Example Workflow

```bash
# 1. Extract spec from Swagger UI (see above)
# 2. Save to file
echo "paste-your-spec-here" > fortnite-api.yaml

# 3. Convert to Markdown
python openapi_to_markdown.py fortnite-api.yaml -o fortnite-api-docs.md

# 4. View the result
cat fortnite-api-docs.md
```

## Output Format

The generated Markdown includes:

- **API Overview**: Title, version, description
- **Authentication**: Security schemes and requirements
- **Servers**: Base URLs and environments
- **Endpoints**: Grouped by tags with:
  - HTTP method and path
  - Description
  - Parameters
  - Request/response details
  - Status codes
- **Schemas**: Data models and structures

## Examples

See the `fortnite_api_documentation.md` file for an example of the generated documentation.

## Project Structure

```
documentation-api-ripper/
├── openapi_to_markdown.py    # Main conversion script
├── batch_convert.py          # Batch conversion for multiple APIs
├── extract_swagger_yaml.js   # Chrome DevTools extraction script
├── swagger_extractor_bookmarklet.js  # Bookmarklet version
├── requirements.txt          # Python dependencies
├── api_specs/               # Raw API specifications (YAML/JSON)
│   ├── fortnite/           # Fortnite APIs
│   ├── sensortower/        # Sensor Tower APIs (multiple files)
│   ├── roblox/             # Roblox APIs
│   └── ...                 # Other platforms
└── api_docs/               # Converted Markdown documentation
    ├── index.md            # Master documentation index
    ├── fortnite/           # Fortnite API docs
    ├── sensortower/        # Sensor Tower API docs
    └── ...                 # Other platforms
```

## Organized Workflow

### 1. Store API Specifications

Place your YAML/JSON files in the appropriate platform folder:
```bash
# For Sensor Tower (multiple APIs)
api_specs/sensortower/app_analysis.yml
api_specs/sensortower/store_intelligence.yml
api_specs/sensortower/usage_intelligence.yml

# For Fortnite (single API)
api_specs/fortnite/ecosystem_api.yaml
```

### 2. Batch Convert All APIs

```bash
# Convert all new/updated specifications
python3 batch_convert.py

# Convert only Sensor Tower APIs
python3 batch_convert.py -p sensortower

# Force regenerate all documentation
python3 batch_convert.py --force
```

### 3. Access Documentation

- **Master Index**: `api_docs/index.md` - Overview of all APIs
- **Platform Index**: `api_docs/{platform}/index.md` - List of APIs per platform
- **Individual Docs**: `api_docs/{platform}/{api_name}.md` - Full API documentation

## Requirements

- Python 3.7+
- PyYAML for YAML parsing
- Rich for console output
- Requests for HTTP operations

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License