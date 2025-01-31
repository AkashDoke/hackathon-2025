from crewai import Agent, LLM
from meeting_recordings_analysis.tools.gmail_custom_tool import GmailCustomTool
from meeting_recordings_analysis.tools.jira_custom_tool import JiraCustomTool
import os

class Agents():

    def __init__(self):
      self.llm = LLM( model=os.getenv("GEMINI_MODEL"),
        api_key=os.getenv("GEMINI_API_KEY"))
    #model="llama3-8b-8192")
    #anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    #self.llm = ChatAnthropic(anthropic_api_key=anthropic_api_key,
    #                         model_name="claude-3-haiku-20240307")

    def summarizer_agent(self):
        return Agent(
           role="CrewAI Meeting Minutes Summarizer",
           goal="""Summarize the meeting transcript into a summary and write it to a file.
    Extract the action items from the meeting transcript and write them to a file.
    As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. 
    Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible.  And write to a file.""",
           backstory= """You are a highly skilled AI trained in language comprehension and summarization. 
    I would like you to read the following text and summarize it into a concise abstract paragraph. 
    Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. 
    Please avoid unnecessary details or tangential points.""",
           llm=self.llm
        )
    
    def summarizer_faq_agent(self):
            return Agent(
            role="CrewAI Meeting Minutes FAQ Writer",
            goal="""Create detailed and clear FAQ entries based on the questions, answers, and common concerns provided from various sources. Organize the information into a coherent and accessible FAQ format.""",
            backstory= """You are an expert writer with a knack for explaining complex topics in simple and understandable terms. 
    Your task is to take the questions asked and the answers provided to create an FAQ document that addresses the most common queries in a way that is clear, concise, and informative.""",
            llm=self.llm
            )
    
    def summarizer_jira_agent(self):
            return Agent(
            role="CrewAI Jira Story Creator",
            goal="""Transform FAQ content into a well-structured Jira story, breaking it down into actionable tasks and sub-tasks. Ensure each task is clear, achievable, and mapped to the context of the FAQ.""",
            backstory= """You are an experienced project manager with a deep understanding of agile workflows. Your task is to take the FAQ content provided and extract key tasks that align with the overall goals. You will then create a Jira story that reflects the broader project, detailing the necessary tasks with proper assignees, due dates, and priorities. Your work ensures that each task derived from the FAQ is actionable and serves as a step toward achieving the larger goal.""",
            llm=self.llm
            )
    
    def meeting_minutes_writer(self):
            return Agent(
            role="CrewAI Meeting Minutes Writer",
            goal="""Write the meeting minutes based on the summary, action items, and sentiment from the files using the file reader tools and put them together into a cohesive document""",
            backstory= """You are a skilled writer with a talent for crafting clear and concise meeting minutes. 
    Please use the summary provided and the action items extracted to write a comprehensive report that captures the main points of the discussion. 
    Ensure the minutes are well-organized, easy to read, and include all necessary details.""",
            llm=self.llm
            )
    
    def gmail_draft_agent(self):
            return Agent(
            role="Gmail Draft Agent",
            goal="""Send an email to the client with the meeting minutes using the provided body""",
            backstory= """You're a seasoned gmail draft agent.""",
            tools=[GmailCustomTool()],
            llm=self.llm
            )
    
    def jira_draft_agent(self):
            return Agent(
            role="CrewAI Jira Story Creator",
            goal="""Transform meeting transcripts into a well-structured Jira story, breaking down the discussions into actionable tasks and sub-tasks. Ensure each task is clear, achievable, and aligned with the overall goals and outcomes discussed in the meeting.""",
            backstory= """You are an experienced project manager with a deep understanding of agile workflows. Your task is to take the provided meeting transcript and extract key points, decisions, and action items. From these, you'll create a Jira story that reflects the larger project or initiative discussed, detailing the necessary tasks with proper assignees, due dates, and priorities. Your goal is to ensure each task derived from the meeting is actionable and aligned with the team's overall objectives.""",
            tools=[JiraCustomTool()],
            llm=self.llm
            )