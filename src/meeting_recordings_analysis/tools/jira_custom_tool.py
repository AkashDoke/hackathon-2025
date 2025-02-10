from crewai.tools import BaseTool, tool
from typing import Type
from pydantic import BaseModel, Field
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue, create_jira_task, get_active_sprint_id, add_to_sprint
import json
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

        print("body inside tool", body)
        story = parse_markdown(body)
        print("story inside tool", story)
               # Parse the JSON string
        # data = json.loads(body)
        # print("data inside tool", data)
        # Process the data as needed
        # For example, extract the description
        # description = data.get('body', {}).get('description', {})
        # print("description inside tool", description)
        # print("body inside tool 2", body.description)
        # story = parse_markdown(body)
        # print("story inside tool", story)
        # story = body

        sprint_id = get_active_sprint_id()     

        if sprint_id:
            print(sprint_id)
            story_id = create_jira_issue(story) 
            print(story_id)

            task_ids = []

            for task in story['tasks']:
                task_id = create_jira_task(task)
                task_ids.append(task_id)

                add_to_sprint(sprint_id, [story_id] + task_ids)
                return "successfully creted jira stories"

        else:
            return "Kickoff did not complete successfully. Skipping subsequent steps."