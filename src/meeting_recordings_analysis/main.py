import os
from pydantic import BaseModel
from meeting_recordings_analysis.agents import Agents
from meeting_recordings_analysis.tasks import Tasks
from crewai import Crew
import agentops
import streamlit as st
import msal

agentops.init(api_key="8eba4d8b-0246-42f8-adb4-0b16f7f5fd61")

# MSAL Authentication Configuration
CLIENT_ID = "c2a66d44-0827-420a-af20-91fab30ea419"
TENANT_ID = "b3d2bfa8-536e-4864-8ada-5f93cc8faea3"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read"]

# State Management Class
class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""
    meeting_minutes_faq: str = ""
    meeting_minutes_jira_tasks: str = ""


# Flow Class
class MeetingMinutesFlow:
    def __init__(self):
        self.state = MeetingMinutesState()

    def transcribe_meeting(self, file_content: str) -> str:
        print("Generating Transcription")
        # Mock transcription logic
        full_transcription = """Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much.
Transcription: Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much."""
        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")
        return full_transcription

    def generate_summary(self):
        summarize_agent = Agents().summarizer_agent()
        summarize_agent_task = Tasks().summarizer_agent_task(summarize_agent, self.state.transcript)

        crew = Crew(agents=[summarize_agent],
                        tasks=[summarize_agent_task],
                        verbose=False)
        
        result = crew.kickoff()
        self.meeting_minutes = result
        return result

    def generate_meeting_minutes_faq(self):
        summarize_faq_agent = Agents().summarizer_faq_agent()
        summarize_faq_agent_task = Tasks().summarizer_faq_agent_task(summarize_faq_agent, self.state.transcript)

        crew = Crew(agents=[summarize_faq_agent],
                        tasks=[summarize_faq_agent_task],
                        verbose=False)
        
        result = crew.kickoff()
        self.meeting_minutes_faq = result
        return result
    
    def generate_meeting_minutes_jira_tasks(self):
        summarize_faq_agent = Agents().summarizer_jira_agent()
        summarize_faq_agent_task = Tasks().summarizer_jira_agent_task(summarize_faq_agent, self.state.transcript)

        crew = Crew(agents=[summarize_faq_agent],
                        tasks=[summarize_faq_agent_task],
                        verbose=False)
        
        result = crew.kickoff()
        self.meeting_minutes_jira_tasks = result
        return result
    
    # def generate_jira_task(self):
    #     print("here", self.state.transcript)

    #     summarize_agent = Agents().summarizer_agent()
    #     summarize_agent_task = Tasks().summarizer_agent_task(summarize_agent, self.state.transcript)

    #     crew = Crew(agents=[summarize_agent],
    #                     tasks=[summarize_agent_task],
    #                     verbose=False)
        
    #     result = crew.kickoff()
    #     return result
# Create an instance of the flow
meeting_minutes_flow = MeetingMinutesFlow()
