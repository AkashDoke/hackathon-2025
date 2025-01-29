import requests
import re
import json
import base64


# Define Jira URL and credentials
JIRA_URL = 'https://akashdoke4.atlassian.net'
API_TOKEN = 'ATATT3xFfGF0Un8kGpsSZCDS_hIJHFQ3hNeWPZMM-tWSalBBPkmMA9jSFt-fJ1j0ZTM37TpT-_ICB2cPS4vnoWtht_B0LNQh6CHakCU9z6eSe9FNQ33EEVdiOZ-UJiPp2WYzMRr1Q-1qVg0Fxnzvs_1m61uKtI-soUSotqLjZxiQrxGjzhTi0sk=4DDB8ECB'
EMAIL = 'akashdoke4@gmail.com'
PROJECT_KEY = 'SCRUM'

auth_header = base64.b64encode(f"{EMAIL}:{API_TOKEN}".encode()).decode()
# Define headers for Jira API authentication
headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Basic {auth_header}",
    'Accept': 'application/json'
}

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
                    "text": story['description']
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
            "summary": story['title'],
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
    
    if response.status_code == 201:
        story_id = response.json()['id']
        print(f"Story created successfully with ID: {story_id}")
        
        # Create tasks and subtasks under the story
        for task in story['tasks']:
            create_jira_task(story_id, task)
    else:
        print(f"Error creating story: {response.content}")

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
