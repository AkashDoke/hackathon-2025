import requests
import re
import json
import base64
import os


# Define Jira URL and credentials
JIRA_URL =  os.getenv('JIRA_URL')
API_TOKEN = os.getenv('API_TOKEN')
EMAIL = os.getenv('EMAIL')
PROJECT_KEY = os.getenv('PROJECT_KEY')

auth_header = base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()
# Define headers for Jira API authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Basic {auth_header}",
    'Accept': 'application/json'
}


def parse_markdown_v2(markdown_text):
    """
    Parses markdown text to extract story title, description, and tasks.
    """
    parsed_data = {}
    lines = markdown_text.split("\n")

    # Extract Story Title
    story_title_match = re.search(r"\*\*Story Title\*\*: (.+)", markdown_text)
    if story_title_match:
        parsed_data["story_title"] = story_title_match.group(1).strip()

    # Extract Story Description
    story_description_match = re.search(r"\*\*Story Description\*\*: (.+)", markdown_text)
    if story_description_match:
        parsed_data["story_description"] = story_description_match.group(1).strip()

    # Extract Tasks and Sub-tasks
    tasks = []
    task_pattern = re.compile(r"- \*\*Task (\d+): (.+)\*\*")
    sub_task_pattern = re.compile(r"\s*\* \*\*Sub-task (\d+\.\d+): (.+)\*\*")

    current_task = None
    for line in lines:
        task_match = task_pattern.match(line)
        if task_match:
            if current_task:
                tasks.append(current_task)
            current_task = {"title": task_match.group(2).strip(), "sub_tasks": []}
        else:
            sub_task_match = sub_task_pattern.match(line)
            if sub_task_match and current_task:
                current_task["sub_tasks"].append(sub_task_match.group(2).strip())

    if current_task:
        tasks.append(current_task)

    parsed_data["tasks"] = tasks
    return parsed_data

# Function to parse markdown into structured data
def parse_markdown(markdown):
    # Initialize a dictionary to hold story and tasks
    story = {}

     # Extract Story Title
    title_match = re.search(r'\*\*Story Title\*\*: (.*)', markdown)
    if title_match:
        story['title'] = title_match.group(1)

    # Extract Story Description
    desc_match = re.search(r'\*\*Story Description\*\*: (.*)', markdown)
    if desc_match:
        story['description'] = desc_match.group(1)

    # Extract tasks
    tasks = []
    task_matches = re.findall(r'- \*\*(.*?): (.*?)\*\*\s*- \*\*Priority\*\*: (.*?)\s*- \*\*Assignee\*\*: (.*?)\s*- \*\*Due Date\*\*: (.*?)\s*- \*\*Sub-tasks\*\*:\s*([\s\S]*?)(?=- \*\*Task \d)', markdown)
    for task_match in task_matches:
        task = {
            'title': task_match[1],
            'priority': task_match[2],
            'assignee': task_match[3],
            'due_date': task_match[4],
            'subtasks': [subtask.strip() for subtask in task_match[5].strip().split('\n')]
        }
        tasks.append(task)

    story['tasks'] = tasks
    return story

# Function to create Jira issue (story)
def create_jira_issue(story):
    # Define the payload for creating a Jira story
    adf_description = {
    "version": 1,
    "type": "doc",
    "content": [
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": story['story_description']
                }
            ]
        }
        ]
    }

    
    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY  # Replace with your Jira project key
            },
            "summary": story['story_title'],
            "description": adf_description,
            "issuetype": {
                "name": "Story"
            }
        }
    }

    # Send request to Jira API to create the story
    try :
        response = requests.post(f'{JIRA_URL}/rest/api/3/issue', headers=headers, json=payload)
        print(response.status_code, response.text) 
    except Exception as e:
        print("failed")
        print(e)
    
    # if response.status_code == 201:
    #     story_id = response.json()['id']
    #     print(f"Story created successfully with ID: {story_id}")
        
    #     # Create tasks and subtasks under the story
    #     for task in story['tasks']:
    #         create_jira_task(story_id, task)
    # else:
    #     print(f"Error creating story: {response.content}")

# Function to create Jira task (sub-task)
def create_jira_task(parent_issue_id, task):

    
    adf_description = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": task['title']
                    }
                ]
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": subtask
                                    }
                                ]
                            }
                        ]
                    } for subtask in task['subtasks']
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY  # Replace with your Jira project key
            },
            "summary": task['title'],
            "description": adf_description,
            "issuetype": {
                "name": "Task"
            },
            "assignee": {
                "name": task['assignee']
            }
        }
    }

    response = requests.post(f'{JIRA_URL}/rest/api/3/issue', headers=headers, json=payload)
    print(response.status_code, response.text)

    if response.status_code == 200:
        print(f"Task created successfully: {task['title']}")
    else:
        print(f"Error creating task: {response.content}")
