import os

import agentops
import streamlit as st
import io

from openai import OpenAI
from pydantic import BaseModel
from agents import agents
from tasks import tasks
from crewai import Crew , LLM
from pydub import AudioSegment
from pydub.utils import make_chunks

#import msal
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue, parse_markdown_v2
from dotenv import load_dotenv

#agentops.init(api_key="8eba4d8b-0246-42f8-adb4-0b16f7f5fd61")

# MSAL Authentication Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]

# State Management Class
class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""
    meeting_minutes_faq: str = ""
    meeting_minutes_jira_tasks: str = ""

# openai_api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_api_key)

# Flow Class
class MeetingMinutesFlow:
    def __init__(self):
        self.state = MeetingMinutesState()

    def transcribe_meeting(self, file_content: str) -> str:
        print("Generating Transcription")

        # # Working codebase
        # audio_file = io.BytesIO(file_content)
        # audio = AudioSegment.from_file(audio_file, format="wav")

        # # # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        # chunk_length_ms = 60000
        # chunks = make_chunks(audio, chunk_length_ms)

        # print(chunks)

        # # Transcribe each chunk
        # full_transcription = ""
        # for i, chunk in enumerate(chunks):
        #     print(f"Transcribing chunk {i+1}/{len(chunks)}")
        #     chunk_path = f"chunk_{i}.wav"
        #     chunk.export(chunk_path, format="wav")
            
        #     with open(chunk_path, "rb") as audio_file:
        #         transcription = client.audio.transcriptions.create(
        #             model="whisper-1", 
        #             file=audio_file
        #         )
        #         full_transcription += transcription.text + " "

        # print(full_transcription)

        full_transcription = """Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much.
Transcription: Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much."""

        self.state.transcript = full_transcription
        return full_transcription

    # def generate_summary(self):
    #     summarize_agent = agents.summarizer_agent()     
    #     summarize_agent_task = tasks.summarizer_agent_task(summarize_agent, self.state.transcript)

    #     meeting_minutes_writer = agents.meeting_minutes_writer()
    #     meeting_minutes_writer_task = tasks.meeting_minutes_writing_task(meeting_minutes_writer)

    #     crew = Crew(agents=[summarize_agent, meeting_minutes_writer],
    #                     tasks=[summarize_agent_task, meeting_minutes_writer_task],
    #                     verbose=False)
    #     result = crew.kickoff()
    #     self.meeting_minutes = result

        
    #     gmail_draft_agent = agent.gmail_draft_agent()
    #     gmail_draft_task = Tasks().gmail_draft_task(gmail_draft_agent, result)

    #     gmailcrew = Crew(agents=[gmail_draft_agent],
    #                     tasks=[gmail_draft_task],
    #                     verbose=False)
    #     gmailcrew.kickoff()

    #     return result

    # def generate_meeting_minutes_faq(self):
    #     summarize_faq_agent = Agents().summarizer_faq_agent()
    #     summarize_faq_agent_task = Tasks().summarizer_faq_agent_task(summarize_faq_agent, self.state.transcript)

    #     crew = Crew(agents=[summarize_faq_agent],
    #                     tasks=[summarize_faq_agent_task],
    #                     verbose=False)
        
    #     result = crew.kickoff()
    #     self.meeting_minutes_faq = result

    #     slack_draft_agent = Agents().slack_draft_agent()
    #     slack_draft_task = Tasks().slack_draft_task(slack_draft_agent, result)
    #     slackcrew = Crew(agents=[slack_draft_agent],
    #                     tasks=[slack_draft_task],
    #                     verbose=False)
        
    #     slackcrew.kickoff()

    #     return result
    
    # def generate_meeting_minutes_jira_tasks(self):
    #     try:
    #         summarizer_jira_agent = Agents().summarizer_jira_agent()
    #         summarizer_jira_agent_task = Tasks().summarizer_jira_agent_task(summarizer_jira_agent, self.state.transcript)

    #         crew = Crew(agents=[summarizer_jira_agent],
    #                     tasks=[summarizer_jira_agent_task],
    #                     verbose=False)

    #         # Wait for kickoff to complete successfully
    #         result = crew.kickoff()

    #         # Check if result is valid or success before continuing
    #         if result is not None and result != "":  # Customize this based on how you determine success
    #             trimmed_markdown = str(result).strip("```").strip()
    #             story = parse_markdown(trimmed_markdown)
    #             print(story)
    #             create_jira_issue(story)
    #         else:
    #             print("Kickoff did not complete successfully. Skipping subsequent steps.")
    #         return result
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return None

# Create an instance of the flow
meeting_minutes_flow = MeetingMinutesFlow()