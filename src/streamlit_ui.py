from meeting_recordings_analysis.main import meeting_minutes_flow
import streamlit as st
from streamlit.components.v1 import html
from streamlit_carousel import carousel
import streamlit.components.v1 as components
import base64
import os
import sys
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add the src/ directory to the Python path


# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page

# Read query parameters to set the page
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

# Set up the page
st.set_page_config(page_title="Meeting Minutes Generator", layout="wide")

# Custom logo path

# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This is "src/demo/"
# This is "src/demo/assets/"
ASSETS_DIR = os.path.join(BASE_DIR, "meeting_recordings_analysis/assets")

image_paths = {
    "one": os.path.join(ASSETS_DIR, "one.png"),
    "two": os.path.join(ASSETS_DIR, "two.png"),
    "LOGO_PATH": os.path.join(ASSETS_DIR, "logo.png"),
    "Abhi": os.path.join(ASSETS_DIR, "Abhi.png"),
    "akash": os.path.join(ASSETS_DIR, "akash.png"),
    "ankita": os.path.join(ASSETS_DIR, "ankita.png"),
    "dharmik": os.path.join(ASSETS_DIR, "dharmik.png"),
    "Linkedin": os.path.join(ASSETS_DIR, "Linkedin.png"),
    "Github": os.path.join(ASSETS_DIR, "Github.png"),
    "email": os.path.join(ASSETS_DIR, "email.png"),
    "three": os.path.join(ASSETS_DIR, "3.png"),
    "four": os.path.join(ASSETS_DIR, "4.png"),
    "five": os.path.join(ASSETS_DIR, "5.png"),
}
# Function to encode images to base64


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Encode images
encoded_images = {name: image_to_base64(path)
                  for name, path in image_paths.items()}

print("LOGO_PATH", image_paths['LOGO_PATH'])

# Custom Header with Logo
header_html = f"""
<style>
    .header {{
        display: flex;
        align-items: center;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }}

    .nav-container {{
        display: flex;
        gap: 20px;
        margin-left: auto;
    }}

    .logo {{
        height: 30px;
        margin-right: 15px;
    }}

    .nav-link {{
        font-size: 18px;
        font-weight: bold;
        color: #007bff;
        cursor: pointer;
        text-decoration: none;
    }}

    .nav-link:hover {{
        text-decoration: underline;
    }}

    footer {{
        background-color: #007bff;
        color: #fff;
        padding: 10px;
        width: 100%;
        height: 40px;
        position: fixed;
        bottom: 0;
        left: 0;
        text-align: center;
        z-index: 10;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .st-emotion-cache-1ibsh2c {{
        padding: 0 0 10px 0;
    }}

    .stHeading {{
        padding: 0 20px;
    }}

    .stHorizontalBlock.st-emotion-cache-ocqkz7.eiemyj0 {{
        padding: 0 40px;
    }}

    #actions {{
        padding: 0 40px;
        font-size: 22px !important;
        margin-bottom: 10px;
        margin-top: 20px;
    }}

    #take-action {{
        padding: 0 20px;
        font-size: 22px;
        margin: 20px 0 30px;
    }}

    #upload-your-meeting-audio-file {{
        font-size: 22px;
        padding: 0 20px;
    }}

    .st-emotion-cache-1gulkj5 {{
        display: block;
        height:300px;
    }}

    .st-emotion-cache-1104ytp p {{
        margin: 0 0 10px 0;
        font-size: 16px;
    }}

    .stFileUploader.st-emotion-cache-1dnm2d2.es2srfl15 {{
        padding: 20px;
        height: 310px;
        margin-top: 28px;
        background-color: rgb(240, 242, 246);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }}

    .stElementContainer.element-container.st-emotion-cache-ihqqol.eiemyj1 
    .st-emotion-cache-ocsh0s.e1obcldf2 {{
        top: 50%;
        right: 43%;
        position: absolute;
        background-color: #009cdb;
        color: #fff !important;
        border-color: #009cdb !important;
    }}
    .st-emotion-cache-ocsh0s{{
        top: 50%;
        right: 43%;
        position: absolute;
        background-color: #5BA8FF;
        color: #fff !important;
        border-color: #5BA8FF !important;
    }}

    .stColumn.st-emotion-cache-1h3k0y3.eiemyj2 {{
        position: relative;
    }}

    .st-emotion-cache-u8hs99 {{
        margin-right: auto;
        align-items: center;
        display: flex;
        justify-content: center;
        margin-top:50px
    }}

    .title {{
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }}

    .st-emotion-cache-12fmjuu {{
        display: none;
    }}

    .st-emotion-cache-1lvxfs7 h2 {{
        padding: 40px;
        font-weight: 400;
        font-size: 24px;
    }}
    .st-emotion-cache-t1wise{{
        padding:0px;
    }}
    .st-emotion-cache-1gulkj5.es2srfl0 .st-emotion-cache-ocsh0s{{
        top: 50%;
        right: 43%;
        position: absolute;
        background-color: #5BA8FF;
        color: #fff !important;
        border-color: #5BA8FF !important;
    }}
    .st-emotion-cache-fis6aj.e1blfcsg5{{
        position: absolute;
        bottom: 19%;
        background-color:#fff;
        width:80%;
        margin:auto;
    }}
    .stHorizontalBlock.st-emotion-cache-ocqkz7.e6rk8up0{{
        padding:30px;
    }}
 
    @media screen and (min-width: 1024px) {{
        .stElementContainer.element-container.st-emotion-cache-ihqqol.eiemyj1 
        .st-emotion-cache-ocsh0s.e1obcldf2 {{
            top: 50%;
            right: 43%;
            position: absolute;
            background-color: #009cdb;
            color: #fff !important;
            border-color: #009cdb !important;
        }}
    }}
</style>



<div class="header">
    <img src="data:image/png;base64,{encoded_images['LOGO_PATH']}" class="logo" alt="Arieotech">
    <div class="nav-container">
        <a class="nav-link" href="?page=home">Home</a>
        <a class="nav-link" href="?page=ourteam">Our Team</a>
    </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)


st.markdown("""
   <style>
    .meeting-minutes {
        margin: 0px 40px;
    }

    h1#meeting-minutes-generator {
        text-align: left;
        font-size: 34px;
        font-weight: 700;
        color: #5BA8FF;
        margin: 0px;
    }

    .st-emotion-cache-1i2xbq7 {
        gap: 0px;
    }

    .stColumn.st-emotion-cache-1vj2wxa.eiemyj2 {
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
        border-radius: 20px;
        height: 310px;
        padding: 20px;
    }

    .st-emotion-cache-fis6aj.es2srfl5 {
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
        margin-top: 80px;
        border-radius: 10px;
        padding: 10px;
    }

    #text_area_1 {
        height: 300px;
    }

    .st-emotion-cache-1104ytp p,
    .st-emotion-cache-1104ytp ol,
    .st-emotion-cache-1104ytp ul,
    .st-emotion-cache-1104ytp dl,
    .st-emotion-cache-1104ytp li {
        text-align: left;
        font-size: 25px;
        color: #333;
        margin: 0px;
    }

    .stCustomComponentV1.st-emotion-cache-1tvzk6f.e9msf260 {
        margin-top: 30px;
    }

    .st-emotion-cache-1104ytp hr:not([size]) {
        display: none;
    }

    .st-emotion-cache-1h9usn1 {
        background: rgb(240, 242, 246);
    }

    .st-emotion-cache-1104ytp p {
        text-align: left;
        font-size: 20px;
        color: #333;
        margin: 0px;
    }

    .st-emotion-cache-1104ytp.e121c1cl0 {
        margin-bottom: -5px;
    }
    .st-emotion-cache-1104ytp a {
        text-decoration: none; 
        color:#5BA8FF;       
    }

    .nav-link:hover {
      text-decoration: none;
    }
         .st-emotion-cache-1104ytp h2{
            font-size:24px;
            }   
.ai-info {
            background-color: #f0f2f6; /* Light gray background */
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-family: Arial, sans-serif;
            margin-top:30px;
            font-size:16px !important;
            height:300px
        }
            .ai-info p{
            font-size:16px !important;
        }
           .ai-info img{
            height:168px
            }
            .stCustomComponentV1.st-emotion-cache-1tvzk6f.e1begtbc0{
            margin-top:20px
            }
            .st-emotion-cache-1104ytp{
            margin-bottom:0px;
            font-size:16px;
            padding-left:20px
            }
                .st-emotion-cache-1104ytp p{
            font-size:16px;
            }
            .stAlertContainer{
            padding:10px;
            }
</style>

""", unsafe_allow_html=True)


# Conditional Page Rendering
if st.session_state.page == "home":
    st.markdown("""
    <div class='meeting-minutes'>
        <h1>Meeting Minutes Generator</h1>
        <p>AI-powered Meeting Transcriptions, Summarization, and more</p>
    </div>
    """, unsafe_allow_html=True)

    carousel_items = [
        {"title": "Ollama: llm model", "text": "AI-powered solutions for meeting minutes and transcription.",
            "img": f"data:image/png;base64,{encoded_images['one']}"},
        {"title": "Real-time Transcription", "text": "Get accurate transcriptions instantly.",
            "img": f"data:image/png;base64,{encoded_images['two']}"},
        {"title": "Summarization", "text": "Generate concise summaries with AI.",
            "img": f"data:image/png;base64,{encoded_images['three']}"},
        {"title": "Collaboration", "text": "Share and collaborate on meeting notes effortlessly.",
            "img": f"data:image/png;base64,{encoded_images['four']}"},
        {"title": "Collaboration", "text": "Share and collaborate on meeting notes effortlessly.",
            "img": f"data:image/png;base64,{encoded_images['five']}"}
    ]
    carousel(items=carousel_items)

    st.write("---")
    st.header("Upload Your Meeting Audio File")

    col1, col2 = st.columns([4, 8])

    uploaded_file = None
    transcription = ""

    with col1:
        uploaded_file = st.file_uploader("Choose a file", type=["mp3", "wav"])

        if uploaded_file:
            st.info("File uploaded successfully!")

            with col2:
                st.spinner("Processing your file...")
                # Simulating transcription process
                transcription = meeting_minutes_flow.transcribe_meeting(
                    uploaded_file.read())
                st.text_area("Meeting Transcript", transcription, height=200)
                st.success("Transcription Complete!")
        else:
            # AI-related content when no file is uploaded
            with col2:
                st.markdown(
                    """
                    <div class="ai-info">
                        <p>🤖 <strong>Did you know?</strong></br> AI-powered transcription tools use Natural Language Processing (NLP) and Speech Recognition to convert speech into text accurately.</p>
                        <p>🎙️ Upload an audio file to see AI in action!</p>
                        <img src="https://t3.ftcdn.net/jpg/05/59/87/12/360_F_559871209_pbXlOVArUal3mk6Ce60JuP13kmuIRCth.jpg" width="300" >
                    </div>
                    """, unsafe_allow_html=True
                )

    # Show Actions section only if a file is uploaded
    if uploaded_file:
        st.write("Actions")
        col1, col2, col3 = st.columns(3)
        if 'summary_open' not in st.session_state:
            st.session_state.summary_open = False

        if 'faq_open' not in st.session_state:
            st.session_state.faq_open = False

        if 'task_open' not in st.session_state:
            st.session_state.task_open = False

        with col1:
            st.spinner("Generating summary...")
            with st.expander("📄 Summary", expanded=st.session_state.summary_open):
                # summary = meeting_minutes_flow.generate_summary()
                st.success("Summary Generated!")
                st.session_state.summary_open = True
                # st.text_area("Summary", summary, height=200)

        with col2:
            if st.session_state.summary_open:
                with st.expander("📚 FAQ", expanded=st.session_state.faq_open):
                    st.spinner("Generating FAQ...")
                    # faq = meeting_minutes_flow.generate_meeting_minutes_faq()
                    st.success("FAQ Generated!")
                    st.session_state.faq_open = True
                    # st.text_area("FAQ", faq, height=200)
            else:
                # FAQ section is disabled if Summary isn't open
                with st.expander("📚 FAQ", expanded=False):
                    st.write("Please generate the summary first.")

        with col3:
            with st.expander("📝 Create Task"):
                st.spinner("Generating tasks...")
                # tasks = meeting_minutes_flow.generate_meeting_minutes_jira_tasks()
                st.success("Tasks Generated!")
                # st.text_area("Tasks", tasks, height=200)


elif st.session_state.page == "ourteam":
    st.markdown("<h2>Meet our awesome team at Arieotech!</h2>",
                unsafe_allow_html=True)

    team_members = [
        {"name": "Akash Doke",
         "image": encoded_images["akash"],
         "linkedin": "https://www.linkedin.com/in/akashdoke/",
         "github": "https://github.com/akashdoke",
         "email": "akashdoke@example.com"},

        {"name": "Abhishek Kulkarni",
         "image": encoded_images["Abhi"],
         "linkedin": "https://www.linkedin.com/in/abhishek-kulkarni-5a31b3112/",
         "github": "https://github.com/abhikulkarni",
         "email": "abhikulkarni@example.com"},

        {"name": "Ankita Chavan",
         "image": encoded_images["ankita"],
         "linkedin": "https://www.linkedin.com/in/ankita-chavan-92a16b160/",
         "github": "https://github.com/ankitachavan",
         "email": "ankitachavan@example.com"},

        {"name": "Dharmik Desai",
         "image": encoded_images["dharmik"],
         "linkedin": "https://www.linkedin.com/in/dharmikdesai/",
         "github": "https://github.com/dharmikdesai",
         "email": "dharmikdesai@example.com"}
    ]

    team_html = '<div class="team-container">'
    for member in team_members:
        team_html += f"""
          <style>
.team-container {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 40px;
    margin-top: 20px;
}}

.team-card {{
    background: #ffffff;
    border-radius: 15px;
    padding: 25px;
    width: 280px;  
    height: 380px; /* Adjusted height */
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.team-card:hover {{
    transform: scale(1.05);
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15);
}}

.team-card img {{
    border-radius: 50%;
    width: 140px; 
    height: 140px; 
    object-fit: cover;
    border: 5px solid #0077b5;
    margin-bottom: 15px;
}}

.team-card h3 {{
    margin: 10px 0 5px;
    font-size: 22px;
    color: #333;
    font-weight: 600;
}}

/* Social Icons Container */
.social-icons {{
    display: flex;
    justify-content: center;
    gap: 15px;  /* Adjusts spacing between icons */
    margin-top: 15px;
}}

/* Individual Icon Styling */
.icon {{
    width: 45px;  /* Increased size for better visibility */
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    overflow: hidden;
}}

/* Hover Effect */
.icon:hover {{
    transform: scale(1.1);
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.25);
}}


.icon img {{
    width: 80%;  /* Adjust image size within the circle */
    height: 80%;
    object-fit: cover;
}}
</style>

<div class="team-card">
    <img src="data:image/png;base64,{member['image']}" alt="{member['name']}">
    <h3>{member['name']}</h3>
    <div class="social-icons">
        <a href="{member['linkedin']}" target="_blank" class="icon">
            <img src="https://img.freepik.com/free-psd/social-media-logo-design_23-2151296991.jpg" alt="LinkedIn">
        </a>
        <a href="{member['github']}" target="_blank" class="icon">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKfpcT9pukR3OGAg5MzGXR0aopy7CRbEGjQYeprsv57ecKJlo4eRiZYuou9e_RAtuseHE&usqp=CAU" alt="GitHub">
        </a>
        <a href="mailto:{member['email']}" class="icon">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrIlnK2H1OUyHmvnq0pG1d2Vt5YJOFxnnW4g&s" alt="Email">
        </a>
    </div>
</div>

        """
    team_html += '</div>'

    components.html(team_html, height=600)

st.markdown("""
    <style>
        @keyframes slides {
            from {
                transform: translateX(0);
            }
            to {
                transform: translateX(-100%);
            }
        }

        .logos {
            overflow: hidden;
           padding: 7% 0px 46px 60px;
            white-space: nowrap;
            position: relative;
            background: #fff;
 
        }

        .logos:before, .logos:after {
            position: absolute;
            top: 0;
            content: '';
            width: 250px;
            height: 100%;
            z-index: 2;
        }

        .logos:before {
            left: 0;
            background: linear-gradient(to left, rgba(255,255,255,0), rgb(255, 255, 255));
        }

        .logos:after {
            right: 0;
            background: linear-gradient(to right, rgba(255,255,255,0), rgb(255, 255, 255));
        }

        .logo_items {
            display: inline-block;
            animation: 35s slides infinite linear;
        }

        .logos:hover .logo_items {
            animation-play-state: paused;
        }

        .logo_items img {
            height: 100px;
            margin: 0 10px;
        }
    </style>

    <div class="logos">
        <div class="logo_items">
            <img src="https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/6/slack-logo-slide.png">
            <img src="https://miro.medium.com/v2/resize:fit:1400/1*Ulg1BjUIxIdmOw63J5gF1Q.png">
            <img src="https://miro.medium.com/v2/resize:fit:1200/1*srQdUu5yPUu6msmYr_-eQw.jpeg">
            <img src="https://i0.wp.com/junilearning.com/wp-content/uploads/2020/06/python-programming-language.webp?fit=800%2C800&ssl=1">
            <img src="https://media.licdn.com/dms/image/C5612AQEQc4mBtUSbUw/article-cover_image-shrink_600_2000/0/1606280532648?e=2147483647&v=beta&t=6r9dBiRXoaMRIEKZWZfG49NbKR_MiUYcYFijqNB8sSw">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo8uxvp_oaMdkstYS9gbtGfFIA34zTosaaAhUjPTpBdc0P_wd6m94ozZY0hBOkmg91lg&usqp=CAU">
            <img src="https://store-images.s-microsoft.com/image/apps.64314.14423064005243201.ff003f01-b27e-4e67-9aa6-33c671187261.c7133ceb-d688-4f51-b158-23818ec236ff">
            <img src="https://www.uscloud.com/wp-content/uploads/Azure-Open-AI.webp?v=5a">
            <img src="https://pbs.twimg.com/profile_images/1837604284344807424/B7KYrv04_400x400.jpg">
            <img src="https://bsmedia.business-standard.com/_media/bs/img/article/2025-01/27/full/1737959259-7169.png?im=FeatureCrop,size=(826,465)">
        </div>
        <div class="logo_items">
             <img src="https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/6/slack-logo-slide.png">
            <img src="https://miro.medium.com/v2/resize:fit:1400/1*Ulg1BjUIxIdmOw63J5gF1Q.png">
            <img src="https://miro.medium.com/v2/resize:fit:1200/1*srQdUu5yPUu6msmYr_-eQw.jpeg">
            <img src="https://i0.wp.com/junilearning.com/wp-content/uploads/2020/06/python-programming-language.webp?fit=800%2C800&ssl=1">
            <img src="https://media.licdn.com/dms/image/C5612AQEQc4mBtUSbUw/article-cover_image-shrink_600_2000/0/1606280532648?e=2147483647&v=beta&t=6r9dBiRXoaMRIEKZWZfG49NbKR_MiUYcYFijqNB8sSw">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSo8uxvp_oaMdkstYS9gbtGfFIA34zTosaaAhUjPTpBdc0P_wd6m94ozZY0hBOkmg91lg&usqp=CAU">
            <img src="https://store-images.s-microsoft.com/image/apps.64314.14423064005243201.ff003f01-b27e-4e67-9aa6-33c671187261.c7133ceb-d688-4f51-b158-23818ec236ff">
            <img src="https://www.uscloud.com/wp-content/uploads/Azure-Open-AI.webp?v=5a">
            <img src="https://pbs.twimg.com/profile_images/1837604284344807424/B7KYrv04_400x400.jpg">
            <img src="https://bsmedia.business-standard.com/_media/bs/img/article/2025-01/27/full/1737959259-7169.png?im=FeatureCrop,size=(826,465)">
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""<footer>Made with ❤️ by Arieotech</footer>""",
            unsafe_allow_html=True)
