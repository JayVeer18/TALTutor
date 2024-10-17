import requests
import streamlit as st
from chatbot import Chatbot
from dotenv import load_dotenv
import os

class App:
    def __init__(self, section_name, file_path, video_url, session_key):
        self.url = "http://127.0.0.1:8000/api/"
        self.section_name = section_name
        self.file_path = file_path
        self.video_url = video_url
        self.session_key = session_key

        # load environment variables from .env file
        load_dotenv()
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
        st.cache()

        if f"messages_{self.session_key}" not in st.session_state:
            st.session_state[f"messages_{self.session_key}"] = []
        self.load()

    def chat_with_document(self):
        # Display chat history before the input box
        self.display_chat_history()

        # Query input
        if query := st.chat_input("Ask questions about The video"):
            st.chat_message("user").markdown(query)
            
            # Add user message to chat history
            st.session_state[f"messages_{self.session_key}"].append({"role": "user", "content": query})

            with st.spinner("Querying... please wait..."), st.chat_message("assistant"):
                response = self.chatbot.invoke(query)
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state[f"messages_{self.session_key}"].append({"role": "assistant", "content": response})
            
     

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
            st.success("App instance and messages loaded successfully!")
        else:
            st.error(f"Failed to load data: {response.content}")

    def run(self):
        st.markdown('# School Name')
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
            st.markdown(self.section_name)
            st.video(self.video_url)

        # Display the chat history with scrollable container
        with chat_col:
            with st.container(height=600):
                st.markdown('### TALTutor chatBot')
                self.chat_with_document()
            st.button('save chat',on_click=self.save_chat)

# Example usage
# if __name__ == "__main__":
#   app = App("# Section_name ", r"path\to\file_name", "video_url")
#   app.run()