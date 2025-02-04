from setuptools import setup, find_packages

setup(
    name="meeting_recordings_analysis",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your dependencies here, e.g.,
        "streamlit",
        "pydantic",
        "crewai",
        "crewai_tools",
        "agentops",
        "requests",
        "carousel",
        "streamlit_carousel",
        "msal"
    ],
)