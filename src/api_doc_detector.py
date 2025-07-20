"""
Detect and parse common API documentation formats
"""
from typing import Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from rich.console import Console
import re

console = Console()

class APIDocDetector:
    """Detect and parse common API documentation formats"""
    
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.format = None
        self.soup = None
        
    def detect_format(self) -> str:
        """Detect which API documentation format is being used"""
        page_source = self.driver.page_source
        self.soup = BeautifulSoup(page_source, 'html.parser')
        
        # Check for Swagger UI
        if self._is_swagger():
            self.format = "swagger"
            console.print("[green]✓ Detected: Swagger UI[/green]")
            return "swagger"
            
        # Check for Redoc
        if self._is_redoc():
            self.format = "redoc"
            console.print("[green]✓ Detected: Redoc[/green]")
            return "redoc"
            
        # Check for Slate
        if self._is_slate():
            self.format = "slate"
            console.print("[green]✓ Detected: Slate[/green]")
            return "slate"
            
        # Check for Postman
        if self._is_postman():
            self.format = "postman"
            console.print("[green]✓ Detected: Postman Documentation[/green]")
            return "postman"
            
        # Check for ReadMe.io
        if self._is_readme():
            self.format = "readme"
            console.print("[green]✓ Detected: ReadMe.io[/green]")
            return "readme"
            
        # Check for Stoplight
        if self._is_stoplight():
            self.format = "stoplight"
            console.print("[green]✓ Detected: Stoplight[/green]")
            return "stoplight"
            
        console.print("[yellow]⚠ Unknown API documentation format[/yellow]")
        return "unknown"
    
    def _is_swagger(self) -> bool:
        """Check if this is Swagger UI"""
        indicators = [
            self.soup.find('div', {'id': 'swagger-ui'}),
            self.soup.find('div', {'class': 'swagger-ui'}),
            self.soup.find(text=re.compile('swagger', re.I)),
            self.soup.find('meta', {'name': 'generator', 'content': re.compile('swagger', re.I)})
        ]
        return any(indicators)
    
    def _is_redoc(self) -> bool:
        """Check if this is Redoc"""
        indicators = [
            self.soup.find('redoc'),
            self.soup.find('div', {'id': 'redoc'}),
            self.soup.find('div', {'class': 'redoc-wrap'}),
            bool(re.search(r'redoc\.standalone', str(self.soup)))
        ]
        return any(indicators)
    
    def _is_slate(self) -> bool:
        """Check if this is Slate"""
        indicators = [
            self.soup.find('div', {'class': 'tocify-wrapper'}),
            self.soup.find('div', {'class': 'page-wrapper'}),
            all([
                self.soup.find('div', {'class': 'dark-box'}),
                self.soup.find('div', {'class': 'content'})
            ])
        ]
        return any(indicators)
    
    def _is_postman(self) -> bool:
        """Check if this is Postman documentation"""
        indicators = [
            'postman' in self.driver.current_url,
            self.soup.find('div', {'class': re.compile('postman', re.I)}),
            self.soup.find(text=re.compile('postman', re.I))
        ]
        return any(indicators)
    
    def _is_readme(self) -> bool:
        """Check if this is ReadMe.io"""
        indicators = [
            'readme.io' in self.driver.current_url,
            self.soup.find('div', {'id': 'hub-reference'}),
            self.soup.find('div', {'class': re.compile('rm-', re.I)})
        ]
        return any(indicators)
    
    def _is_stoplight(self) -> bool:
        """Check if this is Stoplight"""
        indicators = [
            self.soup.find('div', {'class': re.compile('sl-', re.I)}),
            'stoplight.io' in self.driver.current_url,
            self.soup.find('elements-api')
        ]
        return any(indicators)
    
    def get_endpoints(self) -> List[Dict]:
        """Extract all API endpoints based on detected format"""
        if not self.format:
            self.detect_format()
            
        endpoints = []
        
        if self.format == "swagger":
            endpoints = self._get_swagger_endpoints()
        elif self.format == "redoc":
            endpoints = self._get_redoc_endpoints()
        elif self.format == "slate":
            endpoints = self._get_slate_endpoints()
        elif self.format == "postman":
            endpoints = self._get_postman_endpoints()
        elif self.format == "readme":
            endpoints = self._get_readme_endpoints()
        elif self.format == "stoplight":
            endpoints = self._get_stoplight_endpoints()
        else:
            endpoints = self._get_generic_endpoints()
            
        console.print(f"[green]Found {len(endpoints)} endpoints[/green]")
        return endpoints
    
    def _get_swagger_endpoints(self) -> List[Dict]:
        """Extract endpoints from Swagger UI"""
        endpoints = []
        
        # Swagger UI specific selectors
        operations = self.soup.find_all('div', {'class': re.compile('opblock')})
        
        for op in operations:
            method_elem = op.find('span', {'class': re.compile('opblock-summary-method')})
            path_elem = op.find('span', {'class': re.compile('opblock-summary-path')})
            desc_elem = op.find('div', {'class': re.compile('opblock-summary-description')})
            
            if method_elem and path_elem:
                endpoints.append({
                    'method': method_elem.get_text(strip=True).upper(),
                    'path': path_elem.get_text(strip=True),
                    'description': desc_elem.get_text(strip=True) if desc_elem else '',
                    'element': op
                })
                
        return endpoints
    
    def _get_redoc_endpoints(self) -> List[Dict]:
        """Extract endpoints from Redoc"""
        endpoints = []
        
        # Redoc specific selectors
        operations = self.soup.find_all(['div', 'section'], {'class': re.compile('operation')})
        
        for op in operations:
            # Redoc shows method and path together
            header = op.find(['h2', 'h3', 'h4'])
            if header:
                text = header.get_text(strip=True)
                # Extract method and path from header
                match = re.match(r'(GET|POST|PUT|DELETE|PATCH)\s+(.+)', text, re.I)
                if match:
                    endpoints.append({
                        'method': match.group(1).upper(),
                        'path': match.group(2),
                        'description': '',
                        'element': op
                    })
                    
        return endpoints
    
    def _get_slate_endpoints(self) -> List[Dict]:
        """Extract endpoints from Slate docs"""
        endpoints = []
        
        # Slate typically uses headers with HTTP methods
        headers = self.soup.find_all(['h1', 'h2', 'h3'])
        
        for header in headers:
            text = header.get_text(strip=True)
            # Look for HTTP method patterns
            match = re.match(r'(GET|POST|PUT|DELETE|PATCH)\s+(.+)', text, re.I)
            if match:
                # Get the content section after this header
                content = []
                sibling = header.find_next_sibling()
                while sibling and sibling.name not in ['h1', 'h2', 'h3']:
                    content.append(sibling)
                    sibling = sibling.find_next_sibling()
                    
                endpoints.append({
                    'method': match.group(1).upper(),
                    'path': match.group(2),
                    'description': '',
                    'element': header.parent if header.parent else header
                })
                
        return endpoints
    
    def _get_generic_endpoints(self) -> List[Dict]:
        """Generic endpoint extraction for unknown formats"""
        endpoints = []
        
        # Look for common patterns
        # Pattern 1: HTTP method followed by path
        method_pattern = re.compile(r'\b(GET|POST|PUT|DELETE|PATCH)\b', re.I)
        path_pattern = re.compile(r'(/api/[^\s<>"]+|/v\d+/[^\s<>"]+)', re.I)
        
        # Find all elements containing HTTP methods
        for elem in self.soup.find_all(text=method_pattern):
            parent = elem.parent
            if parent:
                method_match = method_pattern.search(elem)
                if method_match:
                    # Look for path in same element or nearby
                    path_text = parent.get_text()
                    path_match = path_pattern.search(path_text)
                    
                    if path_match:
                        endpoints.append({
                            'method': method_match.group(1).upper(),
                            'path': path_match.group(1),
                            'description': '',
                            'element': parent
                        })
                        
        return endpoints
    
    def _get_postman_endpoints(self) -> List[Dict]:
        """Extract endpoints from Postman documentation"""
        # Implementation would depend on Postman's specific HTML structure
        return self._get_generic_endpoints()
    
    def _get_readme_endpoints(self) -> List[Dict]:
        """Extract endpoints from ReadMe.io"""
        # Implementation would depend on ReadMe's specific HTML structure
        return self._get_generic_endpoints()
    
    def _get_stoplight_endpoints(self) -> List[Dict]:
        """Extract endpoints from Stoplight"""
        # Implementation would depend on Stoplight's specific HTML structure
        return self._get_generic_endpoints()
    
    def search_endpoint(self, search_term: str) -> List[Dict]:
        """Search for specific endpoints"""
        endpoints = self.get_endpoints()
        
        # Filter endpoints matching search term
        matches = []
        search_lower = search_term.lower()
        
        for endpoint in endpoints:
            if (search_lower in endpoint['path'].lower() or 
                search_lower in endpoint['description'].lower()):
                matches.append(endpoint)
                
        return matches
    
    def highlight_endpoint(self, endpoint: Dict):
        """Highlight an endpoint in the browser"""
        if 'element' not in endpoint:
            return
            
        # Try to find element by text content
        script = """
        function highlightEndpoint(method, path) {
            // Find element containing both method and path
            var elements = document.querySelectorAll('*');
            var found = false;
            
            for (var i = 0; i < elements.length; i++) {
                var elem = elements[i];
                var text = elem.textContent || '';
                
                if (text.includes(method) && text.includes(path)) {
                    // Highlight the element
                    elem.style.backgroundColor = 'yellow';
                    elem.style.border = '3px solid red';
                    elem.scrollIntoView({behavior: 'smooth', block: 'center'});
                    
                    // Remove highlight after 3 seconds
                    setTimeout(function() {
                        elem.style.backgroundColor = '';
                        elem.style.border = '';
                    }, 3000);
                    
                    found = true;
                    break;
                }
            }
            
            return found;
        }
        
        return highlightEndpoint(arguments[0], arguments[1]);
        """
        
        self.driver.execute_script(script, endpoint['method'], endpoint['path'])