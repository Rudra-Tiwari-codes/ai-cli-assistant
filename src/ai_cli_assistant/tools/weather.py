"""Weather tool for AI CLI Assistant."""

from ..base import Tool
from typing import Any, Dict


class WeatherTool(Tool):
    """Weather information tool."""
    
    @property
    def name(self) -> str:
        return "weather"
    
    @property
    def description(self) -> str:
        return "Get weather information for a location"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City or location name"
                }
            },
            "required": ["location"]
        }
    
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        location = kwargs.get("location", "")
        
        # Generate different weather based on location
        import random
        
        # Create location-based weather patterns
        weather_patterns = {
            "london": {"temp": "15°C", "condition": "Rainy", "humidity": "80%"},
            "new york": {"temp": "22°C", "condition": "Partly Cloudy", "humidity": "65%"},
            "tokyo": {"temp": "28°C", "condition": "Sunny", "humidity": "70%"},
            "mumbai": {"temp": "32°C", "condition": "Hot", "humidity": "85%"},
            "paris": {"temp": "18°C", "condition": "Cloudy", "humidity": "75%"},
            "sydney": {"temp": "24°C", "condition": "Clear", "humidity": "60%"},
        }
        
        # Get weather for location (case insensitive)
        location_lower = location.lower()
        if location_lower in weather_patterns:
            weather = weather_patterns[location_lower]
        else:
            # Generate random weather for unknown locations
            conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Clear"]
            temps = [f"{random.randint(10, 35)}°C"]
            weather = {
                "temp": temps[0],
                "condition": random.choice(conditions),
                "humidity": f"{random.randint(50, 90)}%"
            }
        
        return {
            "location": location,
            "temperature": weather["temp"],
            "condition": weather["condition"],
            "humidity": weather["humidity"],
            "description": f"Weather for {location}: {weather['condition']} with {weather['temp']} temperature, {weather['humidity']} humidity"
        }
