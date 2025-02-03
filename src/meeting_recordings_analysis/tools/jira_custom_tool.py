from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue, parse_markdown_v2


class JiraCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    ticket_details: str = Field(..., description="Description of the argument.")


class JiraCustomTool(BaseTool):
    name: str = "JiraTool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = JiraCustomToolInput

    def _run(self, ticket_details: str) -> str:

        trimmed_markdown = str(ticket_details).strip("```").strip()
        story = parse_markdown_v2(trimmed_markdown)
        print(story)
        create_jira_issue(story)
        print(ticket_details)

        # trimmed_markdown = self.meeting_minutes_jira_tasks.strip("```").strip()
        # print(ticket_details)
        # print(trimmed_markdown)
        # story = parse_markdown(trimmed_markdown)
        # create_jira_issue(story)
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
