from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue, parse_markdown_v2, parse_llm_response, extract_story_and_tasks


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

        trimmed_markdown = body.strip("```").strip()
        print("trimmed_markdown", trimmed_markdown)
        story = parse_markdown(trimmed_markdown)
        print("story", story)
        create_jira_issue(story)
        print("success createing stroy")
        return "this is an example of a tool output, ignore it and move along."