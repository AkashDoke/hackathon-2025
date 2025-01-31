from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from meeting_recordings_analysis.gmail.utils import authenticate_gmail, create_message, create_draft
import os

class GmailCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    body: str = Field(..., description="Description of the argument.")

class GmailCustomTool(BaseTool):
    name: str = "JiraTool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = GmailCustomToolInput

    def _run(self, body: str) -> str:
        try:
            service = authenticate_gmail()

            sender = os.getenv("GMAIL_SENDER")
            to = os.getenv("GMAIL_RECIPIENT")
            subject = "Meeting Minutes"
            message_text = body

            message = create_message(sender, to, subject, message_text)
            draft = create_draft(service, "me", message)

            return f"Email sent successfully! Draft id: {draft['id']}"
        except Exception as e:
            return f"Error sending email: {e}"
