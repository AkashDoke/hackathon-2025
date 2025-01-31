import streamlit as st
from streamlit.components.v1 import html

# Import the main processing logic
from meeting_recordings_analysis.main import meeting_minutes_flow

# Set up the page
st.set_page_config(page_title="Meeting Minutes Generator", layout="wide")

# Title
st.title("📋 Meeting Minutes Generator")
st.subheader("AI-powered Meeting Transcriptions, Summarization, and More")

# Add a carousel using HTML and CSS
carousel_css = """
<style>
.carousel-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    overflow: hidden;
    position: relative;
}

.carousel-slide {
    display: flex;
    width: 300%;
    animation: slide-animation 10s infinite;
}

.carousel-slide img {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
}

@keyframes slide-animation {
    0% { transform: translateX(0); }
    33% { transform: translateX(-100%); }
    66% { transform: translateX(-200%); }
    100% { transform: translateX(0); }
}

.carousel-caption {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    text-align: center;
}
</style>
"""

carousel_html = """
<div class="carousel-container">
    <div class="carousel-slide">
        <div style="position: relative;">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd-M_r7bEyuBQzUODeKwobumjZ2bnoB_uelw&s" alt="OpenAI API">
            <div class="carousel-caption">Explore OpenAI APIs</div>
        </div>
        <div style="position: relative;">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd-M_r7bEyuBQzUODeKwobumjZ2bnoB_uelw&s" alt="Innovation">
            <div class="carousel-caption">Empowering Innovation</div>
        </div>
        <div style="position: relative;">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRd-M_r7bEyuBQzUODeKwobumjZ2bnoB_uelw&s" alt="AI Future">
            <div class="carousel-caption">Shaping the Future with AI</div>
        </div>
    </div>
</div>
"""

st.markdown(carousel_css, unsafe_allow_html=True)
st.markdown(carousel_html, unsafe_allow_html=True)

# File Upload Section
st.write("---")
st.header("Upload Your Meeting Audio File")

uploaded_file = st.file_uploader("Choose a file", type=["mp3", "wav"])
if uploaded_file:
    st.info("File uploaded successfully!")
    
    # Process the file with transcribe_meeting
    with st.spinner("Processing your file..."):
        transcription = meeting_minutes_flow.transcribe_meeting(uploaded_file.read())
        st.success("Transcription Complete!")
        st.text_area("Meeting Transcript", transcription, height=200)

    # Generate Summary
    st.write("### Generate Additional Insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = meeting_minutes_flow.generate_summary()
                st.success("Summary Generated!")
                st.text_area("Summary", summary, height=200)

    with col2:
        if st.button("Generate FAQ"):
            with st.spinner("Generating FAQ..."):
                faq = meeting_minutes_flow.generate_meeting_minutes_faq()
                st.success("FAQ Generated!")
                st.text_area("FAQ", faq, height=200)

    with col3:
        if st.button("Generate Tasks"):
            with st.spinner("Generating tasks..."):
                tasks = meeting_minutes_flow.generate_meeting_minutes_jira_tasks()
                st.success("Tasks Generated!")
                st.text_area("Tasks", tasks, height=200)

    # Email and JIRA Buttons
    st.write("---")
    st.header("Take Action")
    col4, col5 = st.columns(2)

    with col4:
        if st.button("Send Email"):
            st.info("Email functionality triggered. Integrate your email service logic here.")

    with col5:
        if st.button("Create JIRA Tasks"):
            with st.spinner("Creating JIRA tasks..."):
                tasks = meeting_minutes_flow.generate_jira_task()
                st.success("JIRA task creation triggered. Integrate your JIRA service logic here.")

# Footer
st.write("---")
st.caption("Powered by OpenAI | Built with ❤️ using Streamlit")
