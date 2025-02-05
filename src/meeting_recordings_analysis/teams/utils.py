import re
import requests

def convert_markdown_to_slack_format(markdown_text):
    # Convert markdown to Slack's formatting
    # Bold: *text* -> *text*
    markdown_text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', markdown_text)
    
    # Italic: *text* or _text_ -> _text_
    markdown_text = re.sub(r'\*(.*?)\*', r'_\1_', markdown_text)
    markdown_text = re.sub(r'_(.*?)_', r'_\1_', markdown_text)
    
    # Strikethrough: ~~text~~ -> ~text~
    markdown_text = re.sub(r'~~(.*?)~~', r'~\1~', markdown_text)
    
    # Code block (inline): `code` -> `code`
    markdown_text = re.sub(r'`([^`]+)`', r'`\1`', markdown_text)
    
    # Code block (multi-line): ```code``` -> ```code```
    markdown_text = re.sub(r'```(.*?)```', r'```\1```', markdown_text, flags=re.DOTALL)
    
    # Links: [text](url) -> <url|text>
    markdown_text = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<\2|\1>', markdown_text)
    
    # Lists: "-" or "*" -> •
    markdown_text = re.sub(r'^\s*[-\*]\s+', '• ', markdown_text, flags=re.MULTILINE)
    
    # Blockquotes: > text -> > text
    markdown_text = re.sub(r'^\s*>\s+', '> ', markdown_text, flags=re.MULTILINE)
    
    return markdown_text

def send_to_slack(message, webhook_url):

    slack_payload = {
    "type": "markdown",
    "text": message,
    }

    response = requests.post(webhook_url, json=slack_payload)
    if response.status_code == 200:
        print("Message successfully sent to Slack.")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")