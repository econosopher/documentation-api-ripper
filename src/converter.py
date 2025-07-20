import re
from typing import Dict, List, Optional
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()


class HTMLToMarkdownConverter:
    def __init__(self):
        self.conversion_options = {
            'heading_style': 'ATX',
            'bullets': '-',
            'code_language': '',
            'strip': ['a', 'img'],
            'convert': ['pre', 'code', 'table', 'ul', 'ol', 'li']
        }
    
    def convert_api_docs(self, api_docs: Dict) -> str:
        """Convert parsed API documentation to Markdown format"""
        markdown_content = []
        
        # Add title
        title = api_docs.get('title', 'API Documentation')
        markdown_content.append(f"# {title}\n")
        
        # Add source URL
        if api_docs.get('url'):
            markdown_content.append(f"**Source:** {api_docs['url']}\n")
        
        # Convert endpoints
        endpoints = api_docs.get('endpoints', [])
        if endpoints:
            markdown_content.append("## Endpoints\n")
            
            for endpoint in endpoints:
                endpoint_md = self._convert_endpoint(endpoint)
                markdown_content.append(endpoint_md)
        
        return '\n'.join(markdown_content)
    
    def _convert_endpoint(self, endpoint: Dict) -> str:
        """Convert individual endpoint to Markdown"""
        sections = []
        
        # Endpoint header
        method = endpoint.get('method', '').upper()
        path = endpoint.get('endpoint', '')
        
        if method and path:
            sections.append(f"### {method} {path}")
        elif path:
            sections.append(f"### {path}")
        
        # Description
        if endpoint.get('description'):
            sections.append(f"\n{endpoint['description']}")
        
        # Parameters
        if endpoint.get('parameters'):
            sections.append("\n#### Parameters")
            for param in endpoint['parameters']:
                sections.append(f"- {param}")
        
        # Response
        if endpoint.get('response'):
            sections.append("\n#### Response")
            sections.append(f"```json\n{endpoint['response']}\n```")
        
        # Code samples
        if endpoint.get('code_samples'):
            sections.append("\n#### Code Examples")
            for i, sample in enumerate(endpoint['code_samples']):
                language = self._detect_language(sample)
                sections.append(f"\n```{language}\n{sample}\n```")
        
        sections.append("\n---\n")
        return '\n'.join(sections)
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language from code sample"""
        patterns = {
            'python': [r'import\s+\w+', r'def\s+\w+', r'print\(', r'^\s*#'],
            'javascript': [r'const\s+\w+', r'let\s+\w+', r'var\s+\w+', r'function\s+\w+', r'=>'],
            'java': [r'public\s+class', r'private\s+\w+', r'System\.out\.println'],
            'curl': [r'curl\s+-', r'-H\s+"', r'--header'],
            'bash': [r'^\$', r'echo\s+', r'export\s+'],
        }
        
        for language, patterns_list in patterns.items():
            for pattern in patterns_list:
                if re.search(pattern, code, re.MULTILINE):
                    return language
        
        return ''
    
    def convert_html_to_markdown(self, html_content: str, preserve_code_blocks: bool = True) -> str:
        """Convert raw HTML to Markdown"""
        if preserve_code_blocks:
            # Preserve code blocks before conversion
            soup = BeautifulSoup(html_content, 'lxml')
            code_blocks = soup.find_all(['pre', 'code'])
            
            # Replace code blocks with placeholders
            placeholders = {}
            for i, block in enumerate(code_blocks):
                placeholder = f"CODE_BLOCK_PLACEHOLDER_{i}"
                placeholders[placeholder] = block.get_text()
                block.string = placeholder
            
            # Convert to markdown
            html_content = str(soup)
            markdown = md(html_content, **self.conversion_options)
            
            # Restore code blocks
            for placeholder, code in placeholders.items():
                language = self._detect_language(code)
                markdown = markdown.replace(
                    placeholder, 
                    f"```{language}\n{code}\n```"
                )
            
            return markdown
        else:
            return md(html_content, **self.conversion_options)
    
    def clean_markdown(self, markdown: str) -> str:
        """Clean up converted Markdown"""
        # Remove excessive newlines
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        
        # Fix header spacing
        markdown = re.sub(r'(#+\s+[^\n]+)\n(?!\n)', r'\1\n\n', markdown)
        
        # Clean up list formatting
        markdown = re.sub(r'\n-\s+', '\n- ', markdown)
        
        # Remove trailing spaces
        markdown = re.sub(r' +$', '', markdown, flags=re.MULTILINE)
        
        return markdown.strip()
    
    def convert_to_claude_format(self, markdown: str) -> str:
        """Format Markdown specifically for Claude Code consumption"""
        sections = []
        
        # Add header for Claude
        sections.append("# API Documentation\n")
        sections.append("This documentation has been extracted and formatted for Claude Code.\n")
        
        # Process the markdown content
        lines = markdown.split('\n')
        current_section = []
        
        for line in lines:
            # Group related content
            if line.startswith('###'):
                if current_section:
                    sections.append('\n'.join(current_section))
                    sections.append('')
                current_section = [line]
            else:
                current_section.append(line)
        
        # Add the last section
        if current_section:
            sections.append('\n'.join(current_section))
        
        # Join all sections
        formatted_content = '\n'.join(sections)
        
        # Add metadata
        formatted_content += "\n\n---\n"
        formatted_content += "**Note:** This documentation was automatically extracted. "
        formatted_content += "Some formatting may have been adjusted for clarity.\n"
        
        return self.clean_markdown(formatted_content)