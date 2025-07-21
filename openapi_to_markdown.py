#!/usr/bin/env python3
"""
OpenAPI/Swagger to Markdown Converter

Converts OpenAPI/Swagger specifications (YAML or JSON) into well-organized Markdown documentation.
"""
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import argparse
from datetime import datetime


class OpenAPIToMarkdown:
    """Converts OpenAPI specifications to Markdown documentation"""
    
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.info = spec.get('info', {})
        self.servers = spec.get('servers', [])
        self.paths = spec.get('paths', {})
        self.components = spec.get('components', {})
        self.security = spec.get('security', [])
        self.tags = spec.get('tags', [])
    
    def generate_markdown(self) -> str:
        """Generate complete Markdown documentation"""
        sections = [
            self._generate_header(),
            self._generate_overview(),
            self._generate_authentication(),
            self._generate_servers(),
            self._generate_endpoints(),
            self._generate_schemas(),
            self._generate_footer()
        ]
        
        return '\n\n'.join(filter(None, sections))
    
    def _generate_header(self) -> str:
        """Generate documentation header"""
        title = self.info.get('title', 'API Documentation')
        version = self.info.get('version', '')
        
        header = f"# {title}"
        if version:
            header += f" v{version}"
        
        return header
    
    def _generate_overview(self) -> str:
        """Generate API overview section"""
        sections = []
        
        if description := self.info.get('description'):
            sections.append("## Overview\n")
            sections.append(description.strip())
        
        if contact := self.info.get('contact'):
            contact_info = []
            if name := contact.get('name'):
                contact_info.append(f"**Contact**: {name}")
            if email := contact.get('email'):
                contact_info.append(f"**Email**: {email}")
            if url := contact.get('url'):
                contact_info.append(f"**URL**: {url}")
            
            if contact_info:
                sections.append("### Contact Information")
                sections.extend(contact_info)
        
        if license_info := self.info.get('license'):
            sections.append(f"### License")
            sections.append(f"**{license_info.get('name', 'License')}**")
            if url := license_info.get('url'):
                sections.append(f"License URL: {url}")
        
        return '\n'.join(sections) if sections else None
    
    def _generate_authentication(self) -> str:
        """Generate authentication section"""
        if not self.components.get('securitySchemes'):
            return None
        
        sections = ["## Authentication\n"]
        
        for name, scheme in self.components['securitySchemes'].items():
            sections.append(f"### {name}")
            
            scheme_type = scheme.get('type', 'Unknown')
            sections.append(f"**Type**: {scheme_type}")
            
            if scheme_type == 'http':
                sections.append(f"**Scheme**: {scheme.get('scheme', 'Unknown')}")
                if bearer_format := scheme.get('bearerFormat'):
                    sections.append(f"**Bearer Format**: {bearer_format}")
            
            elif scheme_type == 'apiKey':
                sections.append(f"**In**: {scheme.get('in', 'Unknown')}")
                sections.append(f"**Name**: {scheme.get('name', 'Unknown')}")
            
            elif scheme_type == 'oauth2':
                sections.append("**OAuth2 Flows**:")
                for flow_type, flow_config in scheme.get('flows', {}).items():
                    sections.append(f"\n**{flow_type.title()} Flow**:")
                    if auth_url := flow_config.get('authorizationUrl'):
                        sections.append(f"- Authorization URL: `{auth_url}`")
                    if token_url := flow_config.get('tokenUrl'):
                        sections.append(f"- Token URL: `{token_url}`")
                    if scopes := flow_config.get('scopes'):
                        sections.append("- Scopes:")
                        for scope, desc in scopes.items():
                            sections.append(f"  - `{scope}`: {desc}")
            
            if description := scheme.get('description'):
                sections.append(f"\n{description}")
            
            sections.append("")
        
        return '\n'.join(sections)
    
    def _generate_servers(self) -> str:
        """Generate servers section"""
        if not self.servers:
            return None
        
        sections = ["## Servers\n"]
        
        for i, server in enumerate(self.servers, 1):
            url = server.get('url', 'Unknown')
            sections.append(f"### Server {i}")
            sections.append(f"**URL**: `{url}`")
            
            if description := server.get('description'):
                sections.append(f"**Description**: {description}")
            
            if variables := server.get('variables'):
                sections.append("\n**Variables**:")
                for var_name, var_config in variables.items():
                    sections.append(f"- `{var_name}`: {var_config.get('description', 'No description')}")
                    if default := var_config.get('default'):
                        sections.append(f"  - Default: `{default}`")
                    if enum := var_config.get('enum'):
                        sections.append(f"  - Options: {', '.join(f'`{e}`' for e in enum)}")
            
            sections.append("")
        
        return '\n'.join(sections)
    
    def _generate_endpoints(self) -> str:
        """Generate endpoints section"""
        if not self.paths:
            return None
        
        sections = ["## Endpoints\n"]
        
        # Group endpoints by tags
        tagged_endpoints = {}
        untagged_endpoints = []
        
        for path, path_item in self.paths.items():
            for method, operation in path_item.items():
                if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                    endpoint_info = {
                        'path': path,
                        'method': method.upper(),
                        'operation': operation
                    }
                    
                    if tags := operation.get('tags'):
                        for tag in tags:
                            if tag not in tagged_endpoints:
                                tagged_endpoints[tag] = []
                            tagged_endpoints[tag].append(endpoint_info)
                    else:
                        untagged_endpoints.append(endpoint_info)
        
        # Generate tagged endpoints
        for tag in self.tags:
            tag_name = tag.get('name', 'Unknown')
            if tag_name in tagged_endpoints:
                sections.append(f"### {tag_name}")
                if description := tag.get('description'):
                    sections.append(f"{description}\n")
                
                for endpoint in tagged_endpoints[tag_name]:
                    sections.append(self._format_endpoint(endpoint))
                
                sections.append("")
        
        # Generate untagged endpoints
        if untagged_endpoints:
            sections.append("### Other Endpoints\n")
            for endpoint in untagged_endpoints:
                sections.append(self._format_endpoint(endpoint))
        
        return '\n'.join(sections)
    
    def _format_endpoint(self, endpoint: Dict[str, Any]) -> str:
        """Format a single endpoint"""
        method = endpoint['method']
        path = endpoint['path']
        operation = endpoint['operation']
        
        lines = [f"#### `{method} {path}`"]
        
        if summary := operation.get('summary'):
            lines.append(f"\n{summary}")
        
        if description := operation.get('description'):
            lines.append(f"\n{description}")
        
        # Parameters
        if parameters := operation.get('parameters'):
            lines.append("\n**Parameters**:")
            for param in parameters:
                param_name = param.get('name', 'Unknown')
                param_in = param.get('in', 'Unknown')
                param_type = param.get('schema', {}).get('type', 'Unknown')
                required = param.get('required', False)
                
                param_line = f"- `{param_name}` ({param_in}, {param_type}"
                if required:
                    param_line += ", **required**"
                param_line += ")"
                
                if param_desc := param.get('description'):
                    param_line += f": {param_desc}"
                
                lines.append(param_line)
        
        # Request body
        if request_body := operation.get('requestBody'):
            lines.append("\n**Request Body**:")
            if rb_desc := request_body.get('description'):
                lines.append(f"{rb_desc}")
            
            if content := request_body.get('content'):
                for content_type, content_spec in content.items():
                    lines.append(f"- Content-Type: `{content_type}`")
                    if schema := content_spec.get('schema'):
                        lines.append(f"  - Schema: `{self._get_schema_ref(schema)}`")
        
        # Responses
        if responses := operation.get('responses'):
            lines.append("\n**Responses**:")
            for status_code, response in responses.items():
                response_line = f"- `{status_code}`"
                if resp_desc := response.get('description'):
                    response_line += f": {resp_desc}"
                lines.append(response_line)
                
                if content := response.get('content'):
                    for content_type, content_spec in content.items():
                        lines.append(f"  - Content-Type: `{content_type}`")
                        if schema := content_spec.get('schema'):
                            lines.append(f"    - Schema: `{self._get_schema_ref(schema)}`")
        
        lines.append("---")
        return '\n'.join(lines)
    
    def _get_schema_ref(self, schema: Dict[str, Any]) -> str:
        """Get schema reference or type"""
        if '$ref' in schema:
            ref_parts = schema['$ref'].split('/')
            return ref_parts[-1]
        elif 'type' in schema:
            return schema['type']
        return 'Unknown'
    
    def _generate_schemas(self) -> str:
        """Generate schemas section"""
        if not self.components.get('schemas'):
            return None
        
        sections = ["## Schemas\n"]
        
        for schema_name, schema in self.components['schemas'].items():
            sections.append(f"### {schema_name}")
            
            if description := schema.get('description'):
                sections.append(f"{description}\n")
            
            schema_type = schema.get('type', 'object')
            sections.append(f"**Type**: `{schema_type}`")
            
            if properties := schema.get('properties'):
                sections.append("\n**Properties**:")
                required_props = schema.get('required', [])
                
                for prop_name, prop_spec in properties.items():
                    prop_type = prop_spec.get('type', self._get_schema_ref(prop_spec))
                    prop_line = f"- `{prop_name}` ({prop_type}"
                    
                    if prop_name in required_props:
                        prop_line += ", **required**"
                    prop_line += ")"
                    
                    if prop_desc := prop_spec.get('description'):
                        prop_line += f": {prop_desc}"
                    
                    sections.append(prop_line)
            
            sections.append("")
        
        return '\n'.join(sections)
    
    def _generate_footer(self) -> str:
        """Generate documentation footer"""
        return f"\n---\n\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"


def load_spec_file(file_path: Path) -> Dict[str, Any]:
    """Load OpenAPI specification from YAML or JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif file_path.suffix == '.json':
            return json.load(f)
        else:
            # Try to parse as YAML first, then JSON
            content = f.read()
            try:
                return yaml.safe_load(content)
            except yaml.YAMLError:
                return json.loads(content)


def main():
    parser = argparse.ArgumentParser(
        description='Convert OpenAPI/Swagger specifications to Markdown documentation'
    )
    parser.add_argument(
        'spec_file',
        type=str,
        help='Path to OpenAPI/Swagger specification file (YAML or JSON)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path (default: prints to stdout)'
    )
    parser.add_argument(
        '--title',
        type=str,
        help='Override the API title'
    )
    
    args = parser.parse_args()
    
    # Load specification
    spec_path = Path(args.spec_file)
    if not spec_path.exists():
        print(f"Error: File '{spec_path}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        spec = load_spec_file(spec_path)
    except Exception as e:
        print(f"Error loading specification: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Override title if specified
    if args.title:
        if 'info' not in spec:
            spec['info'] = {}
        spec['info']['title'] = args.title
    
    # Convert to Markdown
    converter = OpenAPIToMarkdown(spec)
    markdown = converter.generate_markdown()
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(markdown, encoding='utf-8')
        print(f"Documentation written to: {output_path}")
    else:
        print(markdown)


if __name__ == '__main__':
    main()