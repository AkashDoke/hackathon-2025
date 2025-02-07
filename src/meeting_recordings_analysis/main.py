from crewai import Crew, LLM
from dotenv import load_dotenv
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue, create_jira_task, get_active_sprint_id, add_to_sprint
from pydub.utils import make_chunks
from pydub import AudioSegment
from meeting_recordings_analysis.tasks import Tasks
from meeting_recordings_analysis.agents import Agents
from pydantic import BaseModel
from openai import OpenAI
import os

import agentops
import streamlit as st
import io

os.environ["OTEL_SDK_DISABLED"] = "true"


# import msal

load_dotenv()

# agentops.init(api_key=os.getenv("AGENT_OPS_KEY"), skip_auto_end_session=True)

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


class MeetingMinutesFlow:
    def __init__(self):
        self.state = MeetingMinutesState()
        self.agents = Agents()
        self.tasks = Tasks()

    def transcribe_meeting(self, file_content: str) -> str:
        print("Generating Transcription")

        # Working codebase
        # audio_file = io.BytesIO(file_content)
        # audio = AudioSegment.from_file(audio_file, format="wav")

        # # # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        # chunk_length_ms = 60000
        # chunks = make_chunks(audio, chunk_length_ms)

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

        # Simulated full transcription
        full_transcription = """Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much.
Transcription: Good afternoon, everyone, and welcome to FinTech Plus Sync's 2nd quarter 2023 earnings call. I'm John Doe, CEO of FinTech Plus. We've had a stellar Q2 with a revenue of $125 million, a 25% increase year over year. Our gross profit margin stands at a solid 58%, due in part to cost efficiencies gained from our scalable business model. Our EBITDA has surged to $37.5 million, translating to a remarkable 30% EBITDA margin. Our net income for the quarter rose to $16 million, which is a noteworthy increase from $10 million in Q2 2022. Our total addressable market has grown substantially, thanks to the expansion of our high-yield savings product line and the new RoboAdvisor platform. We've been diversifying our asset-backed securities portfolio, investing heavily in collateralized debt obligations and residential mortgage-backed securities. We've also invested $25 million in AAA-rated corporate bonds, enhancing our risk-adjusted returns. As for our balance sheet, total assets reached $1.5 billion with total liabilities at $900 million, leaving us with a solid equity base of $600 million. Our debt to equity ratio stands at 1.5, a healthy figure considering our expansionary phase. We continue to see substantial organic user growth, with customer acquisition cost dropping by 15% and lifetime value growing by 25%. Our LTVCAC ratio is at an impressive 3.5x. In terms of risk management, we have a value-at-risk model in place with a 99% confidence level indicating that our maximum loss will not exceed 5 million in the next trading day. We've adopted a conservative approach to managing our leverage and have a healthy tier one capital ratio of 12.5%. Our forecast for the coming quarter is positive. We expect revenue to be around 135 million and 8% quarter over quarter growth driven primarily by our cutting edge blockchain solutions and AI driven predictive analytics. We're also excited about the upcoming IPO of our FinTech subsidiary Pay Plus, which we expect to raise 200 million. Significantly bolstering our liquidity and paving the way for aggressive growth strategies. We thank our shareholders for their continued faith in us and we look forward to an even more successful Q3. Thank you so much."""
        self.state.transcript = full_transcription
        return full_transcription

    def generate_summary(self):
        summarize_agent = self.agents.summarizer_agent()
        meeting_minutes_writer = self.agents.meeting_minutes_writer()

        summarize_task = self.tasks.summarizer_agent_task(
            summarize_agent, self.state.transcript)
        meeting_minutes_task = self.tasks.meeting_minutes_writing_task(
            meeting_minutes_writer)

        crew = Crew(agents=[summarize_agent, meeting_minutes_writer], tasks=[
                    summarize_task, meeting_minutes_task])
        result = crew.kickoff()

        gmail_agent = self.agents.gmail_draft_agent()
        gmail_task = self.tasks.gmail_draft_task(gmail_agent, result)

        gmail_crew = Crew(agents=[gmail_agent], tasks=[gmail_task])
        gmail_crew.kickoff()

        return result

    def generate_meeting_minutes_faq(self):
        summarize_faq_agent = self.agents.summarizer_faq_agent()
        summarize_faq_task = self.tasks.summarizer_faq_agent_task(
            summarize_faq_agent, self.state.transcript)

        crew = Crew(agents=[summarize_faq_agent], tasks=[summarize_faq_task])
        result = crew.kickoff()

        slack_agent = self.agents.slack_draft_agent()
        slack_task = self.tasks.slack_draft_task(slack_agent, result)

        slack_crew = Crew(agents=[slack_agent], tasks=[slack_task])
        slack_crew.kickoff()

        return result

    def generate_meeting_minutes_jira_tasks(self):
        try:
            # jira_agent = self.agents.summarizer_jira_agent()
            # jira_task = self.tasks.summarizer_jira_agent_task(jira_agent, self.state.transcript)

            # crew = Crew(agents=[jira_agent], tasks=[jira_task])
            # result = crew.kickoff()

            # print("jira_agent_result", result)

            result = """```
**Story Title**: Q2 2023 Financial Performance Review and Strategy Implementation

**Story Description**: This story outlines the necessary tasks to review Q2 2023 financial performance and implement strategies for continued growth following the earnings call. We aim to capitalize on the positive results and prepare for upcoming quarter forecasts and the IPO.

**Tasks**:
- Task 1: Review Q2 2023 financial performance metrics.
  - **Priority**: High
  - **Assignee**: Finance Team Lead
  - **Due Date**: 2023-08-01
- Task 2: Analyze customer acquisition strategies and outline improvements based on a 15% drop in costs.
  - **Priority**: Medium
  - **Assignee**: Marketing Manager
  - **Due Date**: 2023-08-15
- Task 3: Develop risk management framework based on the value-at-risk model and current financial data.
  - **Priority**: High
  - **Assignee**: Risk Management Officer
  - **Due Date**: 2023-08-10
- Task 4: Create strategic plan for upcoming IPO of Pay Plus, including investment requirements and expected outcomes.
  - **Priority**: High
  - **Assignee**: Strategy Director
  - **Due Date**: 2023-08-30
- Task 5: Assess opportunities in blockchain solutions and AI predictive analytics to drive growth for Q3.
  - **Priority**: Medium
  - **Assignee**: Head of Innovation
  - **Due Date**: 2023-08-20
- Task 6: Prepare presentation summarizing Q2 results and Q3 forecasts for stakeholders.
  - **Priority**: High
  - **Assignee**: Executive Assistant to the CEO
  - **Due Date**: 2023-08-25
```"""

            if result:
                trimmed_markdown = str(result).strip("```").strip()
                story = parse_markdown(trimmed_markdown)

                sprint_id = get_active_sprint_id()

                if sprint_id:
                    print(sprint_id)
                    story_id = create_jira_issue(story)
                    print(story_id)

                    task_ids = []

                    for task in story['tasks']:
                        task_id = create_jira_task(task)
                        task_ids.append(task_id)

                    add_to_sprint(sprint_id, [story_id] + task_ids)
                    print("successfully creted jira stories")

            else:
                print(
                    "Kickoff did not complete successfully. Skipping subsequent steps.")

            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


# Create an instance of the flow
meeting_minutes_flow = MeetingMinutesFlow()
