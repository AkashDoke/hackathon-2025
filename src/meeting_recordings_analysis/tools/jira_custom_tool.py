from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class JiraCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    body: str = Field(..., description="Description of the argument.")

class JiraCustomTool(BaseTool):
    name: str = "JiraTool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = JiraCustomToolInput

    def _run(self, body: str) -> str:
        print(body)
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
