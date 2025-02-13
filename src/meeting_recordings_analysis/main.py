from crewai import Crew, LLM
from dotenv import load_dotenv
from meeting_recordings_analysis.jira.utils import parse_markdown, create_jira_issue, create_jira_task, get_active_sprint_id, add_to_sprint, chunk_text
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

session = agentops.init(api_key=os.getenv(
    "AGENT_OPS_KEY"), skip_auto_end_session=True)

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


openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


class MeetingMinutesFlow:
    def __init__(self):
        self.state = MeetingMinutesState()
        self.agents = Agents()
        self.tasks = Tasks()

    def transcribe_meeting(self, file_content: str) -> str:
        print("Generating Transcription")

        # Working codebase
        audio_file = io.BytesIO(file_content)
        audio = AudioSegment.from_file(audio_file, format="wav")

        # # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        # Transcribe each chunk
        full_transcription = ""
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")

            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        # Simulated full transcription
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

    def generate_mp3_using_transcript(self, output_path="output-marathi.wav"):
        print("Generating MP3")
        file_path = "transcript-marathi.txt"
        file_content = ""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        chunks = chunk_text(file_content)
        with open(output_path, "wb") as f:
            for chunk in chunks:
                response = client.audio.speech.create(
                    model="tts-1",  # OpenAI's TTS model
                    input=chunk,
                    voice="alloy"  # You can change the voice to "nova" or "echo"
                )
                f.write(response.content)
        print(f"Audio saved to {output_path}") 

    def generate_meeting_minutes_jira_tasks(self):
        try:
            jira_agent = self.agents.summarizer_jira_agent()
            jira_task = self.tasks.summarizer_jira_agent_task(
                jira_agent, self.state.transcript)

            crew = Crew(agents=[jira_agent], tasks=[jira_task])
            result = crew.kickoff()
            session.end_session("success")
            # print("jira_agent_result", result)

            if result:
                trimmed_markdown = str(result).strip("```").strip()
                story = parse_markdown(trimmed_markdown)

                sprint_id = get_active_sprint_id()
                print(sprint_id)

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
