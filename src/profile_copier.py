"""
Chrome profile copier to avoid conflicts
"""
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, Optional
from rich.console import Console

console = Console()

class ChromeProfileCopier:
    """Creates a copy of Chrome profile to avoid conflicts"""
    
    def __init__(self):
        self.temp_dir = None
    
    def create_profile_copy(self, source_profile_path: str) -> str:
        """
        Create a copy of Chrome profile in a temporary directory
        
        Args:
            source_profile_path: Path to the source Chrome profile
            
        Returns:
            Path to the copied profile directory
        """
        try:
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix="chrome_profile_copy_")
            console.print(f"[dim]Creating profile copy in: {self.temp_dir}[/dim]")
            
            # Define what to copy (important files/dirs for authentication)
            important_items = [
                'Cookies',
                'Cookies-journal',
                'Local Storage',
                'Session Storage',
                'IndexedDB',
                'Preferences',
                'Secure Preferences',
                'Login Data',
                'Login Data-journal',
                'Web Data',
                'Web Data-journal'
            ]
            
            source_path = Path(source_profile_path)
            dest_path = Path(self.temp_dir)
            
            # Copy important files
            copied_count = 0
            for item in important_items:
                source_item = source_path / item
                if source_item.exists():
                    dest_item = dest_path / item
                    try:
                        if source_item.is_dir():
                            shutil.copytree(source_item, dest_item)
                        else:
                            shutil.copy2(source_item, dest_item)
                        copied_count += 1
                    except Exception as e:
                        console.print(f"[dim]Could not copy {item}: {e}[/dim]")
            
            console.print(f"[green]✓ Copied {copied_count} profile items[/green]")
            return self.temp_dir
            
        except Exception as e:
            console.print(f"[red]Error creating profile copy: {e}[/red]")
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            raise
    
    def cleanup(self):
        """Remove the temporary profile copy"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                console.print("[dim]Cleaned up temporary profile copy[/dim]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not clean up temp profile: {e}[/yellow]")