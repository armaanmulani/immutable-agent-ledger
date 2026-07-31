from typing import Optional
from pydantic import BaseModel, Field


class ActionParameters(BaseModel):
  """Flexible parameters object covering arithmetic, code execution, and search."""

  query: Optional[str] = Field(
      default=None, description="Search query string or target input"
  )

  a: Optional[float] = Field(
      default=None, description="First number for calculations"
  )
  b: Optional[float] = Field(
      default=None, description="Second number for calculations"
  )
  operation: Optional[str] = Field(
      default=None,
      description="Operation type e.g., 'add', 'multiply', 'divide'",
  )

  # Added strict instruction for single-line / escaped string format!
  code: Optional[str] = Field(
      default=None,
      description=(
          "Raw Python code snippet to execute. MUST be a valid single-line or"
          " escaped string using '\\n' for line breaks."
      ),
  )


class AgentAction(BaseModel):
  """The strict schema that Gemini MUST follow when deciding its next move."""

  action_name: str = Field(
      description=(
          "The tool to execute: 'calculator', 'system_info',"
          " 'python_interpreter', or 'web_search'"
      )
  )
  parameters: ActionParameters = Field(
      description="The structured parameters needed for the tool"
  )
  reasoning: str = Field(
      description="A brief 1-sentence explanation of why the AI chose this action"
  )