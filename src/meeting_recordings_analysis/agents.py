from crewai import Agent, LLM
from meeting_recordings_analysis.tools.gmail_custom_tool import GmailCustomTool
from meeting_recordings_analysis.tools.jira_custom_tool import JiraCustomTool
from meeting_recordings_analysis.tools.slack_custom_tool import SlackCustomTool
from crewai_tools import FileWriterTool
import os


file_writer_faq = FileWriterTool(file_name='faq.txt', directory='hackathon-2025')

class Agents():

    def __init__(self):
      self.groq_llm = LLM(model="groq/deepseek-r1-distill-llama-70b-specdec",
        api_key="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")
      self.google_llm = LLM( model=os.getenv("GEMINI_MODEL"),
        api_key=os.getenv("GEMINI_API_KEY"))
      self.deepseek_llm = LLM(base_url="https://openrouter.ai/api/v1", model="deepseek/deepseek-r1:free",
        api_key="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")
      self.azure_llm = LLM( model='azure/gpt-4o-mini',
                base_url='https://prasa-m6jgverq-eastus2.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview',
		api_key="4CAjxJRE4DzhhGdSTcDGj2inIkTFt3T9XqBrjVZiGDz6NaprvrUyJQQJ99BAACHYHv6XJ3w3AAAAACOGiLz5")
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
           llm=self.azure_llm
        )
    
    def summarizer_faq_agent(self):
            return Agent(
            role="CrewAI Meeting Minutes FAQ Writer",
            goal="""Create detailed and clear FAQ entries based on the questions, answers, and common concerns provided from various sources. Organize the information into a coherent and accessible FAQ format.""",
            backstory= """You are an expert writer with a knack for explaining complex topics in simple and understandable terms. 
    Your task is to take the questions asked and the answers provided to create an FAQ document that addresses the most common queries in a way that is clear, concise, and informative.""",
            llm=self.groq_llm,
            tools=[file_writer_faq]
            )
    
    def summarizer_jira_agent(self):
            return Agent(
            role="CrewAI Jira Story Creator",
            goal="""Transform FAQ content into a well-structured Jira story, breaking it down into actionable tasks and sub-tasks. Ensure each task is clear, achievable, and mapped to the context of the FAQ.""",
            backstory= """You are an experienced project manager with a deep understanding of agile workflows. Your task is to take the FAQ content provided and extract key tasks that align with the overall goals. You will then create a Jira story that reflects the broader project, detailing the necessary tasks with proper assignees, due dates, and priorities. Your work ensures that each task derived from the FAQ is actionable and serves as a step toward achieving the larger goal.""",
            llm=self.groq_llm,
            tools=[JiraCustomTool()]
            )
    
    def meeting_minutes_writer(self):
            return Agent(
            role="CrewAI Meeting Minutes Writer",
            goal="""Write the meeting minutes based on the summary, action items, and sentiment from the files using the file reader tools and put them together into a cohesive document""",
            backstory= """You are a skilled writer with a talent for crafting clear and concise meeting minutes. 
    Please use the summary provided and the action items extracted to write a comprehensive report that captures the main points of the discussion. 
    Ensure the minutes are well-organized, easy to read, and include all necessary details.""",
            llm=self.azure_llm
            )
    
    def gmail_draft_agent(self):
            return Agent(
            role="Gmail Draft Agent",
            goal="""Send an email to the client with the meeting minutes using the provided body""",
            backstory= """You're a seasoned gmail draft agent.""",
            tools=[GmailCustomTool()],
            llm=self.azure_llm
            )
    
    def slack_draft_agent(self):
            return Agent(
            role="Slack Draft Agent",
            goal="""Send an slack message to the client with the meeting minutes using the provided body""",
            backstory= """You're a seasoned slack draft agent.""",
            tools=[SlackCustomTool()],
            llm=self.azure_llm
            )
    
    def jira_ticket_agent(self):
           return Agent(
                role="Jira Ticket Agent",
                goal="""Take markdown input from another crew, send it to a tool as-is, and create a ticket.""",
                backstory="""You are an expert in handling markdown inputs and integrating with ticketing systems.""",
                tools=[JiraCustomTool()],  # Replace with the appropriate tool for interacting with Jira
                llm=self.azure_llm
            )
    
# Create an instance of the flow
agents = Agents()    