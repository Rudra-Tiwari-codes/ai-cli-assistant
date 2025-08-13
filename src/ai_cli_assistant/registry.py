"""Tool registry system for dynamic tool discovery and registration."""

from typing import Any, Dict, List

from .base import Tool


class ToolRegistry:
    """Registry for managing tools."""
    
    def __init__(self) -> None:
        """Initialize the tool registry."""
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Tool | None:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[Tool]:
        """List all registered tools."""
        return list(self._tools.values())
    
    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get function definitions for OpenAI API."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                }
            }
            for tool in self._tools.values()
        ]
    
    async def execute_tool(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        
        return await tool.execute(**kwargs)


# Global registry instance
registry = ToolRegistry()
