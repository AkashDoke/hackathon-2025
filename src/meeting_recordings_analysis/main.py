import os
from pydantic import BaseModel
from meeting_recordings_analysis.agents import Agents
from meeting_recordings_analysis.tasks import Tasks
from crewai import Crew
import agentops
import streamlit as st
import msal
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue

#agentops.init(api_key="8eba4d8b-0246-42f8-adb4-0b16f7f5fd61")

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
    
    def generate_jira_task(self):

        jira_story_value = """```
**Story Title**: Q2 2023 Earnings Call - Actionable Insights and Next Steps

**Story Description**: This story outlines tasks derived from the Q2 2023 FinTech Plus Sync earnings call, focusing on key performance indicators, strategic initiatives, and upcoming plans.  The goal is to translate the call's highlights into actionable items and ensure follow-through on key strategies.


**Tasks**:

- **Task 1: Analyze Q2 Performance & Identify Key Trends**
    - **Priority**: High
    - **Assignee**: Data Analytics Team
    - **Due Date**: 2023-10-27
    - **Sub-tasks**:
        - Analyze revenue growth (25% YoY) and identify contributing factors.
        - Investigate gross profit margin (58%) and identify areas for further improvement.
        - Analyze EBITDA margin (30%) and pinpoint key drivers.
        - Examine net income increase and explore future growth potential.
        - Analyze the impact of high-yield savings and RoboAdvisor platform expansion on the total addressable market.
        - Assess the diversification strategy for the asset-backed securities portfolio.
        - Evaluate the effectiveness of the $25 million investment in AAA-rated corporate bonds.
        - Analyze customer acquisition cost (CAC) reduction (15%) and lifetime value (LTV) growth (25%).  Assess the LTV/CAC ratio (3.5x).
        - Review the Value-at-Risk (VaR) model and its implications for risk management.

- **Task 2: Develop Q3 Strategic Plan Based on Q2 Performance**
    - **Priority**: High
    - **Assignee**: Strategy Team
    - **Due Date**: 2023-10-31
    - **Sub-tasks**:
        - Develop a detailed plan to achieve the projected Q3 revenue of $135 million (8% QoQ growth).
        - Outline specific strategies to leverage blockchain solutions and AI-driven predictive analytics for growth.
        - Create a detailed action plan to support the upcoming IPO of Pay Plus and manage the anticipated $200 million funding.
        - Analyze the debt-to-equity ratio (1.5) and propose strategies for maintaining financial health during expansion.

- **Task 3: Prepare and Distribute Q2 Earnings Report**
    - **Priority**: High
    - **Assignee**: Marketing & Communications Team
    - **Due Date**: 2023-10-20
    - **Sub-tasks**:
        - Create a comprehensive report summarizing Q2 performance.
        - Prepare a presentation for shareholders and investors.
        - Disseminate the report and presentation through appropriate channels.

- **Task 4: Monitor Key Performance Indicators (KPIs) in Q3**
    - **Priority**: High
    - **Assignee**: Operations Team
    - **Due Date**: Ongoing
    - **Sub-tasks**:
        - Track revenue, gross profit margin, EBITDA, net income, and other relevant KPIs.
        - Monitor customer acquisition costs and lifetime value.
        - Continuously assess risk using the VaR model and Tier 1 capital ratio.
        - Regularly report on progress towards Q3 goals.


- **Task 5:  Prepare for Pay Plus IPO**
    - **Priority**: High
    - **Assignee**: Finance Team & Pay Plus Team
    - **Due Date**: Ongoing (leading up to IPO)
    - **Sub-tasks**:
        - Finalize IPO documentation.
        - Secure necessary regulatory approvals.
        - Manage investor relations activities.
        - Plan for post-IPO integration and growth strategies.

```"""

        trimmed_markdown = jira_story_value.strip("```").strip()
        story = parse_markdown(trimmed_markdown)
        create_jira_issue(story)


        print(story)

        return story
# Create an instance of the flow
meeting_minutes_flow = MeetingMinutesFlow()
