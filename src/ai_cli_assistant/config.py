"""Configuration management for AI CLI Assistant."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration class for AI CLI Assistant."""
    
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        
        return cls(
            openai_api_key=api_key,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        if not (0.0 <= self.openai_temperature <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        
        if not self.openai_model:
            raise ValueError("OpenAI model is required")
