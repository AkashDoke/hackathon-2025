from crewai import Task
from meeting_recordings_analysis.tools.jira_custom_tool import JiraCustomTool


class Tasks(): 
    def summarizer_agent_task(self, agent, transcript):
        return Task(
            description=(f"""
                Summarize the meeting transcript into a summary with the following transcript:
    {transcript}

    Write the summary to a file called "summary.txt" in the "meeting_minutes" directory.  This is provided by the tool.

    Write the action items to a file called "action_items.txt" in the "meeting_minutes" directory.  This is provided by the tool.

    I would like you to return the action items from the meeting transcript in the following format:
    - Action item 1
    - Action item 2
    - ...

    I would also like you to analyze the sentiment of the meeting transcript and write it to a file called "sentiment.txt" in the "meeting_minutes" directory.  This is provided by the tool.
            """),
            expected_output=("""A summary of the meeting transcript and a list of action items."""),
            agent=agent,
        )
    
    def summarizer_meeting_minutes_writer_task(self, agent):
        return Task(
            description=("""
                Write the meeting minutes based on the summary, action items and sentiment.  This should give everything needed to know based on summary and action items.
    Put them into a nice markdown document.

    - Use Todays Date for the meeting date
    - Use the company name TylerAI for the company name
    - User Tyler for the name of the organizer
    - Create a list of attendees from the transcript (make up some if needed)
    - The location was on Zoom
            """),
            expected_output=("""A meeting minutes document"""),
            agent=agent,
        )
    
    def summarizer_faq_agent_task(self, agent, transcript):
        return Task(
            description=(f"""
                Create an FAQ based on the given transcript with the following content:
    {transcript}

    Write the FAQ to a file called "faq.txt" in the "faq" directory. This is provided by the tool.

    The FAQ should be formatted as follows:
    - **Question**: [Insert question here]
      **Answer**: [Insert answer here]
    - **Question**: [Insert next question here]
      **Answer**: [Insert answer here]
    - ...

    I would also like you to analyze the sentiment of the transcript and save it to a file called "sentiment_analysis.txt" in the "faq" directory. The sentiment can be categorized as Positive, Neutral, or Negative.
            """),
            expected_output=("""A well-organized FAQ based on the provided transcript, and a sentiment analysis file indicating the tone of the content."""),
            agent=agent,
        )
    
    def summarizer_jira_agent_task(self, agent, transcript):
        return Task(
            description=(f"""
                Based on the provided faq content, generate a Jira story with associated tasks. The faq content is provided in the following format:
    {transcript}

    Write the Jira story with associated tasks to a file called "jira.txt" in the "jira" directory. This is provided by the tool.

    Review each FAQ entry and create relevant Jira tasks based on the questions and answers. These tasks should be clear, actionable, and broken down as sub-tasks in the Jira story. The story should encapsulate the broader theme of the FAQ content.

    The Jira story should be written in the following format:
    **Story Title**: [Insert story title here]
    **Story Description**: [Insert brief description of the story here]

    **Tasks**:
    - Task 1: [Description of the task]
    - Task 2: [Description of the task]
    - ...

    For each task, assign the following:
    - **Priority**: [Set priority, e.g., Low, Medium, High]
    - **Assignee**: [Insert appropriate assignee name]
    - **Due Date**: [Insert due date if relevant]

    Additionally, ensure that the story and tasks are logically connected to the content of the FAQ.
            """),
            tools=[JiraCustomTool()],
            expected_output=("""A well-structured Jira story with detailed tasks and sub-tasks based on the FAQ content. The story should provide a clear overview and actionable steps for implementation."""),
            agent=agent,
        )
    
    def meeting_minutes_writing_task(self, agent):
        return Task(
            description=("""
                Write the meeting minutes based on the summary, action items and sentiment.  This should give everything needed to know based on summary and action items.
    Put them into a nice markdown document.

    - Use Todays Date for the meeting date
    - Use the company name TylerAI for the company name
    - User Tyler for the name of the organizer
    - Create a list of attendees from the transcript (make up some if needed)
    - The location was on Zoom
            """),
            expected_output=("""A meeting minutes document"""),
            agent=agent,
        )
    
    def gmail_draft_task(self, agent, body):
        return Task(
            description=(f"""
                Send an email to the client with the meeting minutes using the provided body: {body}
            """),
            expected_output=("""To return whether the email was sent successfully or not"""),
            agent=agent,
        )
    
    def jira_draft_task(self, agent, body):
        return Task(
            description=(f"""
                Based on the provided faq content, generate a Jira story with associated tasks. The faq content is provided in the following format:
    {body}

    Write the Jira story with associated tasks to a file called "jira.txt" in the "jira" directory. This is provided by the tool.

    Review each FAQ entry and create relevant Jira tasks based on the questions and answers. These tasks should be clear, actionable, and broken down as sub-tasks in the Jira story. The story should encapsulate the broader theme of the FAQ content.

    The Jira story should be written in the following format:
    **Story Title**: [Insert story title here]
    **Story Description**: [Insert brief description of the story here]

    **Tasks**:
    - Task 1: [Description of the task]
    - Task 2: [Description of the task]
    - ...

    For each task, assign the following:
    - **Priority**: [Set priority, e.g., Low, Medium, High]
    - **Assignee**: [Insert appropriate assignee name]
    - **Due Date**: [Insert due date if relevant]

    Additionally, ensure that the story and tasks are logically connected to the content of the FAQ.
            """),
            expected_output=("""A well-structured Jira story with detailed tasks and sub-tasks based on the FAQ content. The story should provide a clear overview and actionable steps for implementation."""),
            agent=agent,
        )
    
    