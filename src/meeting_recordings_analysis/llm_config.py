# llm_config.py
from crewai import LLM
import os

# Initialize LLM models with environment variables
google_llm = LLM(
    model=os.getenv("GEMINI_MODEL"),
    api_key=os.getenv("GEMINI_API_KEY")
)

azure_llm = LLM(
    model=os.getenv("AZURE_OPENAI_MODEL"),
    base_url=os.getenv("AZURE_OPENAI_BASEURL"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)

deepseak_llm = LLM(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0.7,
    model=os.getenv("OLLAMA_MODEL")
)
