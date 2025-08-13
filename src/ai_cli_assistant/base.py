"""Base classes for the extensible tool system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol, TypeAlias

# Type aliases for better readability
ToolResult = TypeAlias = Dict[str, Any]
ToolParameters = TypeAlias = Dict[str, Any]


class Tool(ABC):
    """Abstract base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Tool parameters schema for OpenAI function calling."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool with given parameters."""
        pass


class ToolRegistry(Protocol):
    """Protocol for tool registry."""
    
    def register(self, tool: Tool) -> None:
        """Register a tool."""
        ...
    
    def get_tool(self, name: str) -> Tool | None:
        """Get a tool by name."""
        ...
    
    def list_tools(self) -> List[Tool]:
        """List all registered tools."""
        ...
    
    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get function definitions for OpenAI API."""
        ...
