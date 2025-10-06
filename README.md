# AI CLI Assistant

A modular command-line AI assistant that integrates with OpenAI's GPT-4o-mini model, featuring an extensible tool system for function calling.


## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-cli-assistant
   ```

2. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

3. **Set up environment**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your OpenAI API key
   # Get your key from: https://platform.openai.com/api-keys
   ```

4. **Run the assistant**
   ```bash
   python main.py
   ```

## Usage

### Available Commands
- `help` - Show help information
- `tools` - List available tools
- `exit` or `quit` - Exit the application
- `clear` - Clear conversation history

### Tool Examples
- **Calculator**: "Calculate 2 + 2" or "What is 10 * 5?"
- **Weather**: "What's the weather in London?" or "Weather in Tokyo"
- **Web Search**: "Search for Python tutorials" or "Find machine learning resources"

## Project Structure

```
ai-cli-assistant/
├── src/ai_cli_assistant/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── base.py              # Abstract tool classes
│   ├── registry.py          # Tool registry system
│   ├── client.py            # OpenAI client wrapper
│   ├── cli.py               # CLI interface
│   └── tools/               # Tool implementations
│       ├── __init__.py
│       ├── calculator.py    # Mathematical expressions
│       ├── weather.py       # Weather information
│       └── web_search.py    # Web search functionality
├── main.py                  # Entry point
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Development

### Adding New Tools

1. Create a new tool file in `src/ai_cli_assistant/tools/`
2. Inherit from the `Tool` base class
3. Implement required methods: `name`, `description`, `parameters`, `execute`
4. Register the tool in `cli.py`

### Example Tool Structure
```python
from ..base import Tool

class MyTool(Tool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    @property
    def description(self) -> str:
        return "Description of what this tool does"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param_name"]
        }
    
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        # Tool implementation
        return {"result": "tool output"}
```

## Requirements

- Python 3.11+
- OpenAI API key
- Dependencies: openai, python-dotenv, rich, pydantic

## License

MIT License
