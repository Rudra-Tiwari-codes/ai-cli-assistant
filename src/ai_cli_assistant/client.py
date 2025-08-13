"""OpenAI client wrapper with async support and function calling."""

import asyncio
import json
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI

from .config import Config
from .registry import registry


class OpenAIClient:
    """OpenAI client wrapper for the AI CLI Assistant."""
    
    def __init__(self, config: Config) -> None:
        """Initialize the OpenAI client."""
        self.config = config
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.conversation_history: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def add_function_call(self, name: str, arguments: Dict[str, Any], result: Any) -> None:
        """Add a function call and its result to the conversation history."""
        # Add the function call
        self.conversation_history.append({
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": json.dumps(arguments) if isinstance(arguments, dict) else str(arguments)
            }
        })
        
        # Add the function result
        self.conversation_history.append({
            "role": "function",
            "name": name,
            "content": str(result)
        })
    
    async def chat_completion(
        self, 
        message: str, 
        use_functions: bool = True
    ) -> Dict[str, Any]:
        """Get a chat completion from OpenAI."""
        # Add user message to history
        self.add_message("user", message)
        
        # Prepare messages for API call
        messages = self.conversation_history.copy()
        
        # Prepare function definitions if needed
        tools = None
        if use_functions:
            tools = registry.get_function_definitions()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if use_functions else None,
                temperature=self.config.openai_temperature,
            )
            
            return response.model_dump()
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")
    
    async def process_response(self, response: Dict[str, Any]) -> str:
        """Process the OpenAI response and handle function calls."""
        choices = response.get("choices", [])
        if not choices:
            raise ValueError("No choices in OpenAI response")
        
        choice = choices[0]
        message = choice.get("message", {})
        
        # Check if there's a function call
        if "tool_calls" in message and message["tool_calls"]:
            # Handle function calls
            results = []
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]
                
                # Parse arguments if they're a string
                if isinstance(arguments, str):
                    import json
                    try:
                        arguments = json.loads(arguments)
                    except json.JSONDecodeError:
                        arguments = {}
                
                # Execute the tool
                try:
                    result = await registry.execute_tool(function_name, **arguments)
                    results.append(f"{function_name}: {result}")
                    
                    # Add to conversation history
                    self.add_function_call(function_name, arguments, result)
                    
                except Exception as e:
                    results.append(f"{function_name}: Error - {e}")
            
            # Get a follow-up response
            follow_up = await self.chat_completion(
                f"Function calls completed: {', '.join(results)}"
            )
            return await self.process_response(follow_up)
        
        # Regular response
        content = message.get("content", "")
        if content:
            self.add_message("assistant", content)
        
        return content
    
    async def chat(self, message: str) -> str:
        """Complete chat interaction with function calling support."""
        try:
            response = await self.chat_completion(message)
            return await self.process_response(response)
        except Exception as e:
            return f"Error: {e}"
