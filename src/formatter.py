import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class OutputFormatter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def save_markdown(self, content: str, filename: str, subdirectory: Optional[str] = None) -> Path:
        """Save Markdown content to file"""
        if subdirectory:
            save_dir = self.output_dir / subdirectory
            save_dir.mkdir(exist_ok=True)
        else:
            save_dir = self.output_dir
        
        filepath = save_dir / f"{filename}.md"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        console.print(f"[green] Saved to: {filepath}[/green]")
        return filepath
    
    def save_json(self, data: Dict, filename: str, subdirectory: Optional[str] = None) -> Path:
        """Save JSON data to file"""
        if subdirectory:
            save_dir = self.output_dir / subdirectory
            save_dir.mkdir(exist_ok=True)
        else:
            save_dir = self.output_dir
        
        filepath = save_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green] Saved JSON to: {filepath}[/green]")
        return filepath
    
    def create_index(self, processed_docs: List[Dict[str, str]]) -> str:
        """Create an index file for all processed documentation"""
        index_content = ["# API Documentation Index\n"]
        index_content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        index_content.append("## Processed Documentation\n")
        
        for doc in processed_docs:
            title = doc.get('title', 'Untitled')
            url = doc.get('url', '')
            filename = doc.get('filename', '')
            endpoint_count = doc.get('endpoint_count', 0)
            
            index_content.append(f"### {title}")
            index_content.append(f"- **Source URL:** {url}")
            index_content.append(f"- **Output File:** [{filename}](./{filename})")
            index_content.append(f"- **Endpoints:** {endpoint_count}")
            index_content.append("")
        
        return '\n'.join(index_content)
    
    def create_claude_bundle(self, markdown_files: List[Path], bundle_name: str = "api_docs_bundle") -> Path:
        """Create a single bundled file optimized for Claude Code"""
        bundle_content = []
        
        # Header
        bundle_content.append("# Complete API Documentation Bundle\n")
        bundle_content.append("This file contains all extracted API documentation in a single file for easy Claude Code consumption.\n")
        bundle_content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        bundle_content.append("---\n")
        
        # Add table of contents
        bundle_content.append("## Table of Contents\n")
        for i, filepath in enumerate(markdown_files, 1):
            title = filepath.stem.replace('_', ' ').title()
            bundle_content.append(f"{i}. [{title}](#{filepath.stem})")
        
        bundle_content.append("\n---\n")
        
        # Add all documentation
        for filepath in markdown_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add anchor for TOC
            bundle_content.append(f"<a id='{filepath.stem}'></a>\n")
            bundle_content.append(content)
            bundle_content.append("\n\n---\n\n")
        
        # Save bundle
        bundle_path = self.output_dir / f"{bundle_name}.md"
        with open(bundle_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bundle_content))
        
        console.print(f"[green] Created bundle: {bundle_path}[/green]")
        return bundle_path
    
    def display_summary(self, results: List[Dict]) -> None:
        """Display a summary of processed documentation"""
        table = Table(title="Processing Summary", show_header=True, header_style="bold magenta")
        table.add_column("Source", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Endpoints", justify="right")
        table.add_column("Output File", style="yellow")
        
        total_endpoints = 0
        successful = 0
        
        for result in results:
            if 'error' in result:
                status = "[red]Failed[/red]"
                endpoints = "0"
                output = "-"
            else:
                status = "[green]Success[/green]"
                endpoints = str(len(result.get('endpoints', [])))
                output = result.get('output_file', '-')
                total_endpoints += len(result.get('endpoints', []))
                successful += 1
            
            url = result.get('url', 'Unknown')
            # Truncate URL for display
            if len(url) > 40:
                url = url[:37] + "..."
            
            table.add_row(url, status, endpoints, output)
        
        console.print(table)
        
        # Summary panel
        summary = Panel(
            f"[bold]Total Processed:[/bold] {len(results)}\n"
            f"[bold]Successful:[/bold] {successful}\n"
            f"[bold]Failed:[/bold] {len(results) - successful}\n"
            f"[bold]Total Endpoints:[/bold] {total_endpoints}",
            title="Summary",
            border_style="blue"
        )
        console.print(summary)
    
    def create_cli_friendly_format(self, markdown_content: str) -> str:
        """Create a CLI-friendly format for the documentation"""
        lines = markdown_content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Simplify headers
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                text = line.lstrip('#').strip()
                formatted_lines.append(f"{'  ' * (level - 1)}{text}")
                formatted_lines.append(f"{'  ' * (level - 1)}{'-' * len(text)}")
            # Format code blocks
            elif line.startswith('```'):
                if line == '```':
                    formatted_lines.append('---')
                else:
                    lang = line[3:]
                    formatted_lines.append(f"[CODE: {lang}]")
            # Keep other lines as-is
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def generate_metadata(self, api_docs: Dict) -> Dict:
        """Generate metadata for the processed documentation"""
        metadata = {
            'source_url': api_docs.get('url', ''),
            'title': api_docs.get('title', ''),
            'extraction_date': datetime.now().isoformat(),
            'endpoint_count': len(api_docs.get('endpoints', [])),
            'methods': list(set(ep.get('method', '') for ep in api_docs.get('endpoints', []) if ep.get('method'))),
            'has_code_samples': any(ep.get('code_samples') for ep in api_docs.get('endpoints', [])),
            'has_parameters': any(ep.get('parameters') for ep in api_docs.get('endpoints', []))
        }
        return metadata