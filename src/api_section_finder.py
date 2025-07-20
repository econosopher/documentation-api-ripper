"""
API Section Finder - Search and highlight API documentation sections
"""
from typing import Optional, Dict, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
import time
import re

console = Console()

class APISectionFinder:
    """Find and extract API documentation sections"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        
    def search_text_on_page(self, search_term: str) -> List[Dict]:
        """
        Search for text on the current page and return all matches with context
        """
        console.print(f"\n[cyan]Searching for: '{search_term}'[/cyan]")
        
        # Get page source
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find all text nodes containing the search term (case insensitive)
        matches = []
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        
        # Search in all text elements
        for element in soup.find_all(text=pattern):
            parent = element.parent
            
            # Skip script and style tags
            if parent.name in ['script', 'style']:
                continue
                
            # Get the parent element that might be a section
            section = self._find_parent_section(parent)
            
            matches.append({
                'text': str(element).strip(),
                'parent_tag': parent.name,
                'parent_class': parent.get('class', []),
                'parent_id': parent.get('id', ''),
                'section': section,
                'xpath': self._get_xpath(parent)
            })
        
        console.print(f"[green]Found {len(matches)} matches[/green]")
        return matches
    
    def _find_parent_section(self, element):
        """Find the parent section/container of an element"""
        # Common API doc section indicators
        section_tags = ['section', 'article', 'div']
        section_classes = ['endpoint', 'method', 'api-method', 'api-endpoint', 
                          'api-section', 'doc-section', 'content-section']
        
        current = element
        for _ in range(10):  # Limit traversal depth
            if not current:
                break
                
            # Check if this is likely a section container
            if current.name in section_tags:
                classes = current.get('class', [])
                if any(cls in ' '.join(classes).lower() for cls in section_classes):
                    return current
                    
                # Also check for data attributes
                if any(attr.startswith('data-') and 'api' in attr 
                      for attr in current.attrs):
                    return current
            
            current = current.parent
            
        return element.parent
    
    def _get_xpath(self, element):
        """Generate XPath for an element"""
        components = []
        child = element
        
        while child and child.name:
            siblings = child.parent.find_all(child.name, recursive=False) if child.parent else []
            if len(siblings) > 1:
                index = siblings.index(child) + 1
                components.append(f"{child.name}[{index}]")
            else:
                components.append(child.name)
            child = child.parent
            
        components.reverse()
        return '/' + '/'.join(components)
    
    def highlight_section(self, xpath: str):
        """Highlight a section on the page using JavaScript"""
        try:
            # Scroll to element
            script = f"""
            var element = document.evaluate('{xpath}', document, null, 
                XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {{
                element.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                
                // Highlight with border and background
                element.style.border = '3px solid red';
                element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
                element.style.transition = 'all 0.3s ease';
                
                // Remove highlight after 3 seconds
                setTimeout(function() {{
                    element.style.border = '';
                    element.style.backgroundColor = '';
                }}, 3000);
                
                return true;
            }}
            return false;
            """
            
            result = self.driver.execute_script(script)
            if result:
                console.print("[green]✓ Section highlighted[/green]")
            else:
                console.print("[yellow]Could not highlight section[/yellow]")
                
        except Exception as e:
            console.print(f"[red]Error highlighting: {e}[/red]")
    
    def extract_api_section(self, section_element) -> Dict:
        """Extract API information from a section"""
        api_info = {
            'endpoint': '',
            'method': '',
            'description': '',
            'parameters': [],
            'responses': [],
            'examples': []
        }
        
        # Try to extract endpoint URL
        endpoint_elements = section_element.find_all(['code', 'pre'], 
            text=re.compile(r'(/api/|https?://)', re.IGNORECASE))
        if endpoint_elements:
            api_info['endpoint'] = endpoint_elements[0].get_text(strip=True)
        
        # Try to extract HTTP method
        method_pattern = re.compile(r'\b(GET|POST|PUT|DELETE|PATCH)\b', re.IGNORECASE)
        method_elements = section_element.find_all(text=method_pattern)
        if method_elements:
            match = method_pattern.search(method_elements[0])
            if match:
                api_info['method'] = match.group(1).upper()
        
        # Extract description (usually in <p> tags)
        desc_elements = section_element.find_all('p', limit=3)
        if desc_elements:
            api_info['description'] = ' '.join(p.get_text(strip=True) for p in desc_elements)
        
        # Look for parameter tables or lists
        param_headers = ['parameter', 'param', 'field', 'attribute']
        tables = section_element.find_all('table')
        for table in tables:
            headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
            if any(param in ' '.join(headers) for param in param_headers):
                # Extract parameter info
                for row in table.find_all('tr')[1:]:  # Skip header row
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        api_info['parameters'].append({
                            'name': cells[0].get_text(strip=True),
                            'description': cells[1].get_text(strip=True) if len(cells) > 1 else '',
                            'type': cells[2].get_text(strip=True) if len(cells) > 2 else ''
                        })
        
        # Look for code examples
        code_blocks = section_element.find_all(['pre', 'code'])
        for block in code_blocks:
            code_text = block.get_text(strip=True)
            if len(code_text) > 50:  # Likely an example, not inline code
                api_info['examples'].append(code_text)
        
        return api_info
    
    def search_and_extract(self, search_term: str) -> List[Dict]:
        """Main method to search and extract API information"""
        matches = self.search_text_on_page(search_term)
        
        results = []
        for i, match in enumerate(matches):
            console.print(f"\n[yellow]Match {i+1}:[/yellow]")
            console.print(f"Text: {match['text'][:100]}...")
            console.print(f"Parent: <{match['parent_tag']}> {match['parent_class']}")
            
            # Highlight the section
            if match['xpath']:
                self.highlight_section(match['xpath'])
                time.sleep(1)  # Give user time to see highlight
            
            # Extract API info if we have a section
            if match['section']:
                api_info = self.extract_api_section(match['section'])
                results.append({
                    'match': match,
                    'api_info': api_info
                })
                
                # Display extracted info
                if api_info['endpoint'] or api_info['method']:
                    console.print(Panel(
                        f"[bold]Endpoint:[/bold] {api_info['endpoint']}\n"
                        f"[bold]Method:[/bold] {api_info['method']}\n"
                        f"[bold]Description:[/bold] {api_info['description'][:200]}...\n"
                        f"[bold]Parameters:[/bold] {len(api_info['parameters'])}\n"
                        f"[bold]Examples:[/bold] {len(api_info['examples'])}",
                        title="Extracted API Info"
                    ))
        
        return results