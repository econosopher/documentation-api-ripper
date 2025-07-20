# Project Structure

```
documentation-api-ripper/
│
├── src/                    # Core application code
│   ├── main.py            # Main entry point
│   ├── parser.py          # API documentation parser
│   ├── converter.py       # HTML to Markdown converter
│   ├── formatter.py       # Output formatter
│   ├── oauth_manager.py   # OAuth session management
│   ├── auth_manager.py    # Authentication flow manager
│   ├── site_config.py     # Site-specific configurations
│   └── session_manager.py # Browser session management
│
├── test_scripts/          # Test scripts for development
│   └── test_*.py         # Various test files
│
├── utils/                 # Utility scripts
│   ├── check_auth.py     # Check authentication status
│   ├── force_auth.py     # Force authentication flow
│   └── debug_cookies.py  # Debug cookie issues
│
├── examples/              # Example usage scripts
│   └── *.py              # Various examples
│
├── tests/                 # Unit tests (future)
│
├── oauth_tokens/          # Stored OAuth sessions (git-ignored)
├── output/                # Extracted documentation output
│
├── config.yaml           # Main configuration
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── run_interactive.sh   # Interactive run script
```
