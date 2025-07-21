#!/usr/bin/env python3
"""
Batch converter for API specifications to Markdown

Processes all YAML/JSON files in api_specs/ folders and converts them to 
organized Markdown documentation in api_docs/ folders.
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json
import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()


class BatchAPIConverter:
    def __init__(self):
        self.api_specs_dir = Path("api_specs")
        self.api_docs_dir = Path("api_docs")
        self.converter_script = Path("openapi_to_markdown.py")
        self.stats = {
            'total_files': 0,
            'converted': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def ensure_directories(self):
        """Ensure api_specs and api_docs directories exist"""
        self.api_specs_dir.mkdir(exist_ok=True)
        self.api_docs_dir.mkdir(exist_ok=True)
    
    def find_spec_files(self):
        """Find all YAML and JSON files in api_specs directory"""
        spec_files = []
        
        for platform_dir in self.api_specs_dir.iterdir():
            if platform_dir.is_dir():
                # Find all YAML and JSON files in each platform directory
                yaml_files = list(platform_dir.glob("*.yaml")) + list(platform_dir.glob("*.yml"))
                json_files = list(platform_dir.glob("*.json"))
                
                for spec_file in yaml_files + json_files:
                    spec_files.append({
                        'platform': platform_dir.name,
                        'file': spec_file,
                        'relative_path': spec_file.relative_to(self.api_specs_dir)
                    })
        
        return spec_files
    
    def get_output_path(self, spec_info):
        """Generate output path for converted Markdown"""
        platform = spec_info['platform']
        spec_name = spec_info['file'].stem  # filename without extension
        
        # Create platform directory in api_docs if it doesn't exist
        platform_docs_dir = self.api_docs_dir / platform
        platform_docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filename (same name as input, just .md extension)
        output_file = platform_docs_dir / f"{spec_name}.md"
        return output_file
    
    def get_spec_title(self, spec_file):
        """Extract title from API specification"""
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                if spec_file.suffix in ['.yaml', '.yml']:
                    spec = yaml.safe_load(f)
                else:
                    spec = json.load(f)
                
                title = spec.get('info', {}).get('title', spec_file.stem.replace('_', ' ').title())
                version = spec.get('info', {}).get('version', '')
                
                if version:
                    return f"{title} v{version}"
                return title
        except:
            return spec_file.stem.replace('_', ' ').title()
    
    def convert_file(self, spec_info):
        """Convert a single spec file to Markdown"""
        input_file = spec_info['file']
        output_file = self.get_output_path(spec_info)
        
        # Check if output already exists and is newer than input
        if output_file.exists() and output_file.stat().st_mtime > input_file.stat().st_mtime:
            return 'skipped', f"Up to date: {output_file.name}"
        
        # Run the converter
        cmd = [
            sys.executable,
            str(self.converter_script),
            str(input_file),
            '-o', str(output_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                return 'success', f"Converted: {output_file.name}"
            else:
                return 'error', f"Error: {result.stderr.strip()}"
        except Exception as e:
            return 'error', f"Exception: {str(e)}"
    
    def generate_summary(self):
        """Generate a simple summary of converted files"""
        summary = []
        
        for platform_dir in sorted(self.api_docs_dir.iterdir()):
            if platform_dir.is_dir():
                md_files = sorted(platform_dir.glob("*.md"))
                if md_files:
                    summary.append(f"\n{platform_dir.name}:")
                    for md_file in md_files:
                        summary.append(f"  - {md_file.name}")
        
        return '\n'.join(summary) if summary else "No documentation files found."
    
    def run(self, platform_filter=None):
        """Run the batch conversion process"""
        self.ensure_directories()
        
        console.print(Panel.fit(
            "[bold cyan]API Documentation Batch Converter[/bold cyan]",
            border_style="cyan"
        ))
        
        # Find all spec files
        spec_files = self.find_spec_files()
        
        # Filter by platform if specified
        if platform_filter:
            spec_files = [s for s in spec_files if s['platform'] == platform_filter]
        
        if not spec_files:
            console.print("[yellow]No specification files found![/yellow]")
            console.print("\nPlace your YAML/JSON files in:")
            for platform_dir in ['fortnite', 'sensortower', 'roblox', 'minecraft', 'steam', 'epic_games', 'unity', 'playfab']:
                console.print(f"  - api_specs/{platform_dir}/")
            return
        
        # Display found files
        table = Table(title="Found API Specifications")
        table.add_column("Platform", style="cyan")
        table.add_column("File", style="green")
        table.add_column("Title", style="yellow")
        
        for spec in spec_files:
            title = self.get_spec_title(spec['file'])
            table.add_row(
                spec['platform'],
                spec['file'].name,
                title
            )
        
        console.print(table)
        console.print(f"\n[bold]Total files found: {len(spec_files)}[/bold]\n")
        
        # Convert files with progress
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Converting specifications...", total=len(spec_files))
            
            for spec in spec_files:
                self.stats['total_files'] += 1
                progress.update(task, description=f"Converting {spec['file'].name}...")
                
                status, message = self.convert_file(spec)
                
                if status == 'success':
                    self.stats['converted'] += 1
                    console.print(f"[green]✓[/green] {message}")
                elif status == 'skipped':
                    self.stats['skipped'] += 1
                    console.print(f"[yellow]○[/yellow] {message}")
                else:
                    self.stats['errors'] += 1
                    console.print(f"[red]✗[/red] {message}")
                
                progress.advance(task)
        
        # Show summary of files
        summary = self.generate_summary()
        if summary:
            console.print("\n[cyan]Documentation files:[/cyan]")
            console.print(summary)
        
        # Print summary
        console.print("\n[bold]Conversion Summary:[/bold]")
        console.print(f"  Total files: {self.stats['total_files']}")
        console.print(f"  [green]Converted: {self.stats['converted']}[/green]")
        console.print(f"  [yellow]Skipped: {self.stats['skipped']}[/yellow]")
        console.print(f"  [red]Errors: {self.stats['errors']}[/red]")
        
        # Show where docs are located
        if self.stats['converted'] > 0 or self.stats['skipped'] > 0:
            console.print(f"\n[bold cyan]Documentation available in:[/bold cyan]")
            console.print(f"  {self.api_docs_dir}/")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Batch convert API specifications to Markdown documentation'
    )
    parser.add_argument(
        '-p', '--platform',
        type=str,
        help='Convert only specs for a specific platform (e.g., fortnite, sensortower)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force reconversion of all files (ignore timestamps)'
    )
    
    args = parser.parse_args()
    
    converter = BatchAPIConverter()
    
    # Modify converter if force flag is set
    if args.force:
        original_convert = converter.convert_file
        def force_convert(spec_info):
            # Remove the timestamp check by always converting
            input_file = spec_info['file']
            output_file = converter.get_output_path(spec_info)
            
            cmd = [
                sys.executable,
                str(converter.converter_script),
                str(input_file),
                '-o', str(output_file)
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return 'success', f"Converted: {output_file.name}"
                else:
                    return 'error', f"Error: {result.stderr.strip()}"
            except Exception as e:
                return 'error', f"Exception: {str(e)}"
        
        converter.convert_file = force_convert
    
    converter.run(platform_filter=args.platform)


if __name__ == '__main__':
    main()