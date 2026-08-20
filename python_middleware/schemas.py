from pydantic import BaseModel, Field

class ActionParameters(BaseModel):
    query: str = Field(description="Search query string or task query")

class AgentAction(BaseModel):
    action_name: str = Field(
        default="SEARCH",
        description="Allowed action type: 'SEARCH'"
    )
    parameters: ActionParameters = Field(
        description="The structured parameters containing 'query'"
    )
    reasoning: str = Field(
        description="Brief 1-sentence reasoning for selecting this action"
    )