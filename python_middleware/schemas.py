from typing import Optional
from pydantic import BaseModel, Field


class ActionParameters(BaseModel):
  """Explicit parameters object so Gemini doesn't inject illegal additionalProperties."""

  query: Optional[str] = Field(
      default=None, description="Search query or input string"
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


class AgentAction(BaseModel):
  """The strict schema that Gemini MUST follow when deciding its next move."""

  action_name: str = Field(
      description=(
          "The name of the tool to execute (e.g., 'calculator', 'web_search')"
      )
  )
  parameters: ActionParameters = Field(
      description="The structured parameters needed for the tool"
  )
  reasoning: str = Field(
      description=(
          "A brief 1-sentence explanation of why the AI chose this action"
      )
  )