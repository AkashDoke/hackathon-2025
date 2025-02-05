from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from meeting_recordings_analysis.teams.utils import convert_markdown_to_slack_format, send_to_slack
import os

class SlackCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    body: str = Field(..., description="Description of the argument.")

class SlackCustomTool(BaseTool):
    name: str = "TeamsTool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = SlackCustomToolInput

    def _run(self, body: str) -> str:
        try:
            slack_formatted_message = convert_markdown_to_slack_format(body)

            # Slack webhook URL (you can replace this with your actual webhook URL)
            webhook_url = os.getenv("SLACK_WEBHOOK_URL")

            print("slack_formatted_message", slack_formatted_message)
            
            # Send formatted message to Slack
            send_to_slack(body, webhook_url)

            return "Slack messsage sent successfully!"
        except Exception as e:
            return f"Error sending email: {e}"