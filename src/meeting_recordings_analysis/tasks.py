from crewai import Task
from meeting_recordings_analysis.tools.jira_custom_tool import JiraCustomTool
from datetime import date

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
    - Use the company name ArieoAI for the company name
    - User ArieoAI for the name of the organizer
    - Create a list of attendees from the transcript
            """),
            expected_output=("""A meeting minutes document"""),
            agent=agent,
        )
    
    # def summarizer_faq_agent_task(self, agent, transcript):
    #     return Task(
    #         description=(f"""
    #         **Task Title**: FAQ Creation and Sentiment Analysis  
    #         **Date**: {date.today().strftime('%B %d, %Y')}  

    #         **Objective**:  
    #         Based on the provided transcript, create a well-organized Frequently Asked Questions (FAQ) document. The FAQ should include professionally formatted questions and answers, clearly categorized and easy to navigate.

    #         **Transcript**:
    #         {transcript}

    #         **Instructions**:  
    #         1. **FAQ Creation**:  
    #             - Review the transcript and extract key points to form relevant and precise questions and answers.
    #             - Each FAQ entry should be professionally formatted as follows:

    #                 - **Question**: [Insert question here]  
    #                   **Answer**: [Insert detailed answer here]  

    #             - Please ensure that the questions are phrased clearly and concisely, and that the answers provide informative and accurate explanations.
    #             - Each FAQ entry should be logically ordered and easy to follow.

    #         2. **Sentiment Analysis**:  
    #             - After creating the FAQ, analyze the sentiment of the transcript.
    #             - The sentiment should be categorized as one of the following: Positive, Neutral, or Negative.
    #             - Save the sentiment analysis result to a file called "sentiment_analysis.txt" in the "faq" directory.
            
    #         **Expected Output**:  
    #         - A well-organized FAQ file that follows the format outlined above.
    #         - A sentiment analysis file named "sentiment_analysis.txt" containing the sentiment categorization.

    #         **File Locations**:  
    #         - The FAQ file will be saved as "faq.txt" in the "faq" directory.  
    #         - The sentiment analysis file will be saved as "sentiment_analysis.txt" in the same "faq" directory.
    #     """),
    #         expected_output=("""A well-organized FAQ based on the provided transcript, and a sentiment analysis file indicating the tone of the content."""),
    #         agent=agent,
    #     )
    
    def summarizer_faq_agent_task(self, agent, transcript):
        return Task(
            description=(f"""
            *FAQ Creation and Sentiment Analysis Task*  
            
            *Date:* {date.today().strftime('%B %d, %Y')}  

            *Objective:*  
            Based on the provided transcript, create a well-organized Frequently Asked Questions (FAQ) document in Slack’s Markdown format. The FAQ should include professionally formatted questions and answers, clearly categorized and easy to navigate.

            *Transcript:*  
            ``` 
            {transcript}
            ```

            *Instructions:*  

            *1. FAQ Creation:*  
            - Review the transcript and extract key points to form relevant and precise questions and answers.
            - Each FAQ entry should be formatted as follows:

            ```
            *Question:* [Insert question here]  
            *Answer:*  
            [Insert detailed answer here]  
            ```

            - Ensure the questions are clear and concise, while the answers provide informative and accurate explanations.
            - Maintain logical ordering and ease of navigation.

            *2. Sentiment Analysis:*  
            - After creating the FAQ, analyze the sentiment of the transcript.
            - Categorize the sentiment as one of the following: *Positive*, *Neutral*, or *Negative*.
            - Save the sentiment analysis result in a file named `sentiment_analysis.txt` inside the `faq` directory.

            *Expected Output:*  
            - A well-organized FAQ file (`faq.txt`) formatted in Slack’s Markdown style.  
            - A sentiment analysis file (`sentiment_analysis.txt`) containing the sentiment categorization.

            *File Locations:*  
            - *FAQ File:* `faq/faq.txt`  
            - *Sentiment Analysis File:* `faq/sentiment_analysis.txt`
            """),
            expected_output=("""A properly formatted FAQ document in Slack's Markdown style and a sentiment analysis file indicating the tone of the content."""), 
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
    - Use the company name ArieoAi for the company name
    - User ArieoAi for the name of the organizer
    - Create a list of attendees from the transcript 
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
    
    def slack_draft_task(self, agent, body):
        return Task(
            description=(f"""
                Send an slack message to the client with the FAQ using the provided body: {body}
            """),
            expected_output=("""To return whether the slack message was sent successfully or not"""),
            agent=agent,
        )
    
    def jira_draft_task(self, agent, body):
        return Task(
            description=(f"""Take the markdown input from another crew, send it to the tool as-is  using the provided body: {body}"""),
            expected_output=("""A ticket created successfully with the provided markdown content."""),
            agent=agent,
        )