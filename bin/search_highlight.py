#!/usr/bin/env python3
"""
Simple text search and highlight tool for API docs
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.chrome_manager import ChromeManager
from selenium.webdriver.common.by import By
from rich.console import Console
from rich.prompt import Prompt
import time

console = Console()

def search_and_highlight(driver, search_term):
    """Search for text and highlight it on the page"""
    
    # JavaScript to search and highlight text
    script = """
    function highlightText(searchTerm) {
        // Remove previous highlights
        var existingHighlights = document.querySelectorAll('.api-search-highlight');
        existingHighlights.forEach(el => {
            el.outerHTML = el.innerHTML;
        });
        
        var found = false;
        var walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(node) {
                    if (node.parentElement.tagName === 'SCRIPT' || 
                        node.parentElement.tagName === 'STYLE') {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );
        
        var textNodes = [];
        var node;
        while (node = walker.nextNode()) {
            if (node.nodeValue.toLowerCase().includes(searchTerm.toLowerCase())) {
                textNodes.push(node);
            }
        }
        
        textNodes.forEach(function(node) {
            var parent = node.parentElement;
            var text = node.nodeValue;
            var regex = new RegExp('(' + searchTerm + ')', 'gi');
            var parts = text.split(regex);
            
            var fragment = document.createDocumentFragment();
            parts.forEach(function(part) {
                if (part.toLowerCase() === searchTerm.toLowerCase()) {
                    var span = document.createElement('span');
                    span.className = 'api-search-highlight';
                    span.style.backgroundColor = 'yellow';
                    span.style.color = 'black';
                    span.style.padding = '2px 4px';
                    span.style.borderRadius = '3px';
                    span.style.fontWeight = 'bold';
                    span.textContent = part;
                    fragment.appendChild(span);
                    found = true;
                } else {
                    fragment.appendChild(document.createTextNode(part));
                }
            });
            
            parent.replaceChild(fragment, node);
        });
        
        // Scroll to first match
        if (found) {
            var firstMatch = document.querySelector('.api-search-highlight');
            if (firstMatch) {
                firstMatch.scrollIntoView({behavior: 'smooth', block: 'center'});
                
                // Add pulsing animation
                firstMatch.style.animation = 'pulse 1s ease-in-out 3';
                var style = document.createElement('style');
                style.textContent = '@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }';
                document.head.appendChild(style);
            }
        }
        
        return {found: found, count: textNodes.length};
    }
    
    return highlightText(arguments[0]);
    """
    
    result = driver.execute_script(script, search_term)
    return result

def main():
    """Main function"""
    console.print("[bold cyan]Simple API Documentation Search[/bold cyan]")
    console.print()
    
    with ChromeManager() as manager:
        try:
            # Create driver
            console.print("[yellow]Starting browser...[/yellow]")
            driver = manager.create_driver()
            
            # Get URL
            url = Prompt.ask(
                "[cyan]Enter the API documentation URL[/cyan]",
                default="https://app.sensortower.com/api/v1/docs"
            )
            
            # Navigate
            console.print(f"[yellow]Navigating to {url}...[/yellow]")
            driver.get(url)
            
            # Wait for page load
            console.print("[yellow]Waiting for page to load...[/yellow]")
            time.sleep(3)
            
            # Check if we need to login
            if "sign_in" in driver.current_url or "login" in driver.current_url.lower():
                console.print("[yellow]Login required. Please complete the login process.[/yellow]")
                Prompt.ask("[cyan]Press Enter when you've logged in[/cyan]")
            
            console.print("[green]✓ Ready to search![/green]")
            
            # Search loop
            while True:
                console.print("\n" + "="*50)
                search_term = Prompt.ask(
                    "\n[cyan]Enter text to search for (or 'quit' to exit)[/cyan]"
                )
                
                if search_term.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Search and highlight
                result = search_and_highlight(driver, search_term)
                
                if result['found']:
                    console.print(f"[green]✓ Found {result['count']} matches for '{search_term}'[/green]")
                    console.print("[dim]The matches are highlighted in yellow on the page[/dim]")
                    
                    # Let user interact with the page
                    action = Prompt.ask(
                        "\n[cyan]Press Enter to continue searching, or type 'inspect' to pause[/cyan]",
                        default=""
                    )
                    
                    if action.lower() == 'inspect':
                        console.print("[yellow]Browser paused. Inspect the page as needed.[/yellow]")
                        Prompt.ask("[cyan]Press Enter when ready to continue[/cyan]")
                else:
                    console.print(f"[red]✗ No matches found for '{search_term}'[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Search interrupted[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            import traceback
            traceback.print_exc()
    
    console.print("\n[cyan]Goodbye![/cyan]")

if __name__ == "__main__":
    main()