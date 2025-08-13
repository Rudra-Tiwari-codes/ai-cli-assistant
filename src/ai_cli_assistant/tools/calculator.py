"""Calculator tool for AI CLI Assistant."""

from ..base import Tool
from typing import Any, Dict


class CalculatorTool(Tool):
    """Calculator tool for mathematical expressions."""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Evaluate mathematical expressions safely. Return the result in plain text format without LaTeX notation."
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    
    async def execute(self, **kwargs: Any) -> Dict[str, Any]:
        expression = kwargs.get("expression", "")
        try:
            # Simple safe evaluation for basic math
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return {"error": "Invalid characters in expression"}
            
            result = eval(expression)
            return {
                "result": result, 
                "expression": expression,
                "formatted_result": f"{expression} = {result}",
                "plain_result": str(result),
                "clean_result": f"The result of {expression} is {result}.",
                "answer": f"{expression} equals {result}",
                "calculation": f"{expression} = {result}",
                "final_answer": f"Answer: {result}"
            }
        except Exception as e:
            return {"error": f"Calculation error: {e}"}
