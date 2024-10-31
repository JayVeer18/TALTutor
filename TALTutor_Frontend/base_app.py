import requests
import streamlit as st
from chatbot import Chatbot
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

# Get the directory of the current script (where this Python file is located)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the path of the README.md file
env_path = os.path.normpath(os.path.join(script_dir,".env"))

# load environment variables from .env file
load_dotenv(dotenv_path=env_path, verbose=True, override=True)

class App:
    def __init__(self, section_name, file_path, video_url, session_key):
        self.url = "http://127.0.0.1:8000/api/"
        self.section_name = section_name
        self.file_path = file_path
        self.video_url = video_url
        self.session_key = session_key
        self.api_key = os.environ.get("OPENAI_API_KEY")

        # Initialize chatbot
        self.chatbot = Chatbot(
            model_name="gpt-4o-mini",
            api_key=self.api_key,
            file_path=self.file_path,
            chain_type='RAG'
        )

        # Initialize session state
        self.init_session_state()

    def init_session_state(self):
        # Streamlit page configuration
        st.set_page_config(layout="wide")
        # st.cache()

        if f"messages_{self.session_key}" not in st.session_state:
            st.session_state[f"messages_{self.session_key}"] = []
            self.load()

    def display_chat_history(self):
        for message in st.session_state[f"messages_{self.session_key}"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def save_chat(self):
        data = {
            "section_name": self.section_name,
            "file_path": self.file_path,
            "video_url": self.video_url,
            "session_key": self.session_key,
            "messages": st.session_state.get(f"messages_{self.session_key}", [])
        }
        url = self.url+"save/"
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success("App instance and messages saved successfully!")
        else:
            st.error(f"Failed to save data: {response.content}")

    def load(self):
        url = self.url+f"load/{self.session_key}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # self.section_name = data['section_name']
            # self.file_path = data['file_path']
            # self.video_url = data['video_url']
            st.session_state[f"messages_{self.session_key}"] = data['messages']
            print("App instance and messages loaded successfully!")
            # st.success("App instance and messages loaded successfully!")
        # else:
        #     st.error(f"Failed to load data: {response.content}")

    def run(self):
        # Display the logo and title
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://www.kindpng.com/picc/m/72-726998_north-south-foundation-logo-hd-png-download.png" width="50" style="margin-right: 10px;">
                <h3 style="color: #4169E1;">North South Foundation Presents</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.sidebar.markdown("# Welcome to Drona, the TALTutor App")
        st.sidebar.markdown(self.section_name)
        # Add multiple empty strings to create space above the footer
        st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

        # Footer with an image and text
        image_url = 'https://play-lh.googleusercontent.com/TJ5FL4km1GSK_MvO8Yy9Ad0GezFLYhSk4eUFGCWhaj_07iKjhW6Zp2hS33Rtb3TokVTU=s64-rw'
        st.sidebar.markdown(
            f"""
            <div style='text-align: center; padding-top: 20px;'>
                <img src="{image_url}" alt="Logo" style="width: 50px;">
                <p>Powered by <b>TOUCH-A-LIFE Foundation</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Layout for video, summary, and chatbox
        video_col, chat_col = st.columns([0.45, 0.55])
        # Display the video
        with video_col:
            st.markdown('<h4 style="color: #008080;">&emsp;{}</h4>'.format(self.section_name), unsafe_allow_html=True)

            parsed_url = urlparse(self.video_url)
            if 'baps.app.box.com' == parsed_url.netloc:
                st.components.v1.html(
                    f""" <iframe src="{self.video_url}" width="600" height="700" allow="autoplay"></iframe>""",
                    height=700,
                )
            else:
                st.video(self.video_url)

        # Display the chat history with scrollable container
        with chat_col:
            # Create two columns
            col1, col2 = st.columns([1, 0.2])  # Adjust the column widths as needed

            with col1:
                st.markdown('<h4 style="color: #008080;">&emsp;{}</h4>'.format('TALTutor chatBot'),
                            unsafe_allow_html=True)

            with col2:
                st.button('💾 Save Chat', on_click=self.save_chat)

            query = st.chat_input("Ask questions about The video")

            # Inject JavaScript to set the scroll position to the top of the container on load
            scroll_js = """
                <script>
                // Wait until the DOM is fully loaded
                document.addEventListener("DOMContentLoaded", function() {
                    // Get the chat history container by class name
                    var chatContainer = document.querySelector('.st-key-chat_history');

                    if (chatContainer) {
                        // Set the scroll position to the top
                        chatContainer.scrollTop = 0;
                    }
                });
                </script>
            """
            st.markdown(scroll_js, unsafe_allow_html=True)

            with st.container(height=650, key='chat_history'):
                # # Display chat history after loading existing messages
                self.display_chat_history()

                # Query input
                if query:
                    st.chat_message("user").markdown(query)

                    # Add user message to chat history
                    st.session_state[f"messages_{self.session_key}"].append({"role": "user", "content": query})

                    with st.spinner("Querying... please wait..."):
                        response = self.chatbot.invoke(query)
                        st.markdown(response)

                    # Add assistant response to chat history
                    st.session_state[f"messages_{self.session_key}"].append({"role": "assistant", "content": response})






# Example usage
# if __name__ == "__main__":
#   app = App("# Section_name ", r"path\to\file_name", "video_url")
#   app.run()