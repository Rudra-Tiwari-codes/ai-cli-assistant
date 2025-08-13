"""CLI interface for AI CLI Assistant."""

import asyncio
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from .client import OpenAIClient
from .config import Config
from .registry import registry
from .tools import CalculatorTool, WeatherTool, WebSearchTool

console = Console()


def setup_tools() -> None:
    """Register all available tools."""
    tools = [
        CalculatorTool(),
        WeatherTool(),
        WebSearchTool(),
    ]
    
    for tool in tools:
        registry.register(tool)


def show_help() -> None:
    """Display help information."""
    help_text = """
[bold blue]AI CLI Assistant[/bold blue]

Available commands:
• [green]help[/green] - Show this help message
• [green]tools[/green] - List available tools
• [green]exit[/green] or [green]quit[/green] - Exit the application
• [green]clear[/green] - Clear conversation history

Just type your message to chat with the AI assistant!
    """
    console.print(Panel(help_text, title="Help", border_style="blue"))


def list_tools() -> None:
    """List all available tools."""
    tools = registry.list_tools()
    
    if not tools:
        console.print("[yellow]No tools available[/yellow]")
        return
    
    tool_list = "\n".join([
        f"• [green]{tool.name}[/green] - {tool.description}"
        for tool in tools
    ])
    
    console.print(Panel(tool_list, title="Available Tools", border_style="green"))


async def chat_loop(client: OpenAIClient) -> None:
    """Main chat loop."""
    console.print(Panel(
        "[bold blue]AI CLI Assistant[/bold blue]\nType 'help' for commands, 'exit' to quit",
        border_style="blue"
    ))
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            # Handle special commands
            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif user_input.lower() == "help":
                show_help()
                continue
            elif user_input.lower() == "tools":
                list_tools()
                continue
            elif user_input.lower() == "clear":
                client.conversation_history.clear()
                console.print("[green]Conversation history cleared[/green]")
                continue
            
            # Show typing indicator
            with console.status("[bold green]AI is thinking..."):
                response = await client.chat(user_input)
            
            # Display response
            console.print(Panel(
                response,
                title="[bold green]Assistant[/bold green]",
                border_style="green"
            ))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def main() -> None:
    """Main entry point for the CLI."""
    try:
        # Load configuration
        config = Config.from_env()
        config.validate()
        
        # Setup tools
        setup_tools()
        
        # Create client
        client = OpenAIClient(config)
        
        # Run chat loop
        asyncio.run(chat_loop(client))
        
    except ValueError as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
