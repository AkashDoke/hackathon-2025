import requests
import re
import json
import base64
import os


# Define Jira URL and credentials
JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
JIRA_URL = os.getenv('JIRA_URL')
API_TOKEN = os.getenv('API_TOKEN')
EMAIL = os.getenv('EMAIL')
PROJECT_KEY = os.getenv('PROJECT_KEY')
SPRINT_ID = 1
BOARD_ID = 1
EPIC_KEY = "10029"
JIRA_API_BASE_URL = f'https://{JIRA_DOMAIN}/rest/agile/1.0'

auth_header = base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()
# Define headers for Jira API authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Basic {auth_header}",
    'Accept': 'application/json'
}


def extract_story_and_tasks(llm_response):
    """Extracts story title, description, and tasks from various formats."""
    # Remove markdown code blocks if present
    llm_response = re.sub(r'```[a-zA-Z]*\n|```', '', llm_response).strip()

    # Extract Story Title
    title_match = re.search(r'\*\*Story Title\*\*:\s*(.+)', llm_response)
    story_title = title_match.group(
        1).strip() if title_match else "Untitled Story"

    # Extract Story Description
    desc_match = re.search(
        r'\*\*Story Description\*\*:\s*(.+)', llm_response, re.DOTALL)
    story_description = desc_match.group(1).strip(
    ) if desc_match else "No Description Provided"

    # Extract Tasks
    tasks = []
    task_pattern = re.compile(
        r'- Task \d+:\s*(.*?)\n'  # Task Name
        r'\s*- Priority:\s*(.*?)\n'  # Priority
        r'\s*- Assignee:\s*(.*?)\n'  # Assignee
        r'\s*- Due Date:\s*(.*?)\n',  # Due Date
        re.MULTILINE
    )

    for match in task_pattern.finditer(llm_response):
        task = {
            "summary": match.group(1).strip(),
            "priority": match.group(2).strip(),
            "assignee": match.group(3).strip(),
            "due_date": match.group(4).strip()
        }
        tasks.append(task)

    return story_title, story_description, tasks

# Generic function to extract title and description


def extract_title_and_description(response):
    # Use regex to find the title and description
    title_match = re.search(r"**Story Title:**\s*(.*)", response)
    description_match = re.search(r"**Story Description:**\s*(.*)", response)

    # Extract the title and description if matches are found
    title = title_match.group(1).strip() if title_match else None
    description = description_match.group(
        1).strip() if description_match else None

    return title, description


def parse_llm_response(response):
    lines = response.strip().split('\n')
    story_title = lines[0].replace("Story Title: ", "").strip()
    story_description = lines[2].replace("Story Description: ", "").strip()

    tasks = []
    current_task = {}

    for line in lines[4:]:
        if line.strip().startswith("- Task"):
            if current_task:
                tasks.append(current_task)
            current_task = {
                "summary": line.split(": ")[1].strip(),
                "priority": None,
                "assignee": None,
                "due_date": None
            }
        elif "Priority:" in line:
            current_task["priority"] = line.split(": ")[1].strip()
        elif "Assignee:" in line:
            current_task["assignee"] = line.split(": ")[1].strip()
        elif "Due Date:" in line:
            current_task["due_date"] = line.split(": ")[1].strip()

    if current_task:
        tasks.append(current_task)

    return story_title, story_description, tasks


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
    story_description_match = re.search(
        r"\*\*Story Description\*\*: (.+)", markdown_text)
    if story_description_match:
        parsed_data["story_description"] = story_description_match.group(
            1).strip()

    # Extract Tasks and Sub-tasks
    tasks = []
    task_pattern = re.compile(r"- \*\*Tasks (\d+): (.+)\*\*")
    sub_task_pattern = re.compile(r"\s*\* \*\*Sub-task (\d+\.\d+): (.+)\*\*")

    current_task = None
    for line in lines:
        task_match = task_pattern.match(line)
        if task_match:
            if current_task:
                tasks.append(current_task)
            current_task = {"title": task_match.group(
                2).strip(), "sub_tasks": []}
        else:
            sub_task_match = sub_task_pattern.match(line)
            if sub_task_match and current_task:
                current_task["sub_tasks"].append(
                    sub_task_match.group(2).strip())

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
    task_matches = re.findall(
        r'- Task (\d+): (.*?)\n\s*- \*\*Priority\*\*: (.*?)\n\s*- \*\*Assignee\*\*: (.*?)\n\s*- \*\*Due Date\*\*: (.*?)\n', markdown)

    for task_match in task_matches:
        task = {
            'task_number': task_match[0],
            'title': task_match[1],
            'priority': task_match[2],
            'assignee': task_match[3],
            'due_date': task_match[4],
            'subtasks': []  # Since no sub-tasks were mentioned, keeping it empty for now
        }
        tasks.append(task)

    story['tasks'] = tasks
    return story


def send_jira_request(payload):
    """Helper function to send a request to the Jira API."""
    try:
        response = requests.post(
            f'{JIRA_URL}/rest/api/3/issue', headers=headers, json=payload)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def add_to_sprint(sprint_id, issue_id):
    """Helper function to add an issue (story or task) to a sprint."""
    add_to_sprint_data = {
        "issues": issue_id
    }
    sprint_url = f"{JIRA_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    try:
        sprint_response = requests.post(
            sprint_url, headers=headers, data=json.dumps(add_to_sprint_data))
        print(f"Added {issue_id} for sprint {sprint_id}")
        sprint_response.raise_for_status()
        return sprint_response
    except requests.exceptions.RequestException as e:
        print(f"Failed to add issue to sprint: {e}")
        return None


def create_adf_description(text):
    """Helper function to create ADF description."""
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }


def get_active_sprint_id():
    # Fetch active sprints for the board
    url = f'{JIRA_API_BASE_URL}/board/{BOARD_ID}/sprint?state=active'
    try:
        response = requests.get(url, headers=headers)
        print(response)
        response.raise_for_status()  # Raise an exception for HTTP errors
        sprints = response.json().get('values', [])
        print(sprints)
        if sprints:
            # Assuming the first active sprint is the current one
            return sprints[0]['id']
        else:
            print('No active sprints found.')
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # HTTP error
    except Exception as err:
        print(f'Other error occurred: {err}')  # Other errors
    return None


def create_jira_issue(story):
    """Function to create a Jira issue (story)."""
    adf_description = create_adf_description(story['description'])

    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": story['title'],
            "description": adf_description,
            "issuetype": {"name": "Story"}
        }
    }

    response = send_jira_request(payload)
    if response and response.status_code == 201:
        return response.json()['id']
    else:
        print(
            f"Error creating story: {response.content if response else 'No response'}")
        return None


def create_jira_task(task):
    """Function to create a Jira task (sub-task)."""
    adf_description = create_adf_description(task['title'])

    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": task['title'],
            "description": adf_description,
            "issuetype": {"name": "Task"}
        }
    }

    response = send_jira_request(payload)
    if response and response.status_code == 201:
        task_id = response.json()['id']
        print(f"Task created successfully: {task['title']} (ID: {task_id})")
        return task_id
    else:
        print(f"Error creating task: {response.content}")
        return None

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]