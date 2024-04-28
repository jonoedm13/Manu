import streamlit as st
import os
import subprocess 
import logging
from gtts import gTTS 
from langchain.chains import ConversationChain 
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from crewai import Crew, Process
from agents import CrewOne
from tasks import MlcTask
# Configuring logging
logging.basicConfig(level=logging.ERROR)

def initialize_crew(topic=None, query=None):
    agents = [CrewOne()]
    tasks = [MlcTask()]
    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential)
    inputs = {'topic': topic} if topic else {'query': query}
    return crew, inputs

def speak_response(text):
    """Speak the provided text using a text-to-speech engine."""
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        subprocess.run(["start", "response.mp3"])  # Using 'start' to play the sound file on Windows
        print('Speech function has been called')
    except Exception as e:
        logging.error(f"Failed to generate speech: {e}")

def init_conversation(memory_length, crew):
    """Initializes and returns a conversation chain with memory and model setup."""
    memory = ConversationBufferWindowMemory(k=memory_length)
    groq_api_key = os.getenv('GROQ_API_KEY', 'your-default-api-key')
    if groq_api_key == 'your-default-api-key':
        logging.error("GROQ API Key is missing. Please set it in your environment variables.")
        raise ValueError("API Key is missing")
    groq_chat = ChatGroq(api_key=groq_api_key, model_name=crew)
    return ConversationChain(llm=groq_chat, verbose=True, memory=memory)

def chat_interface(role, action):
    """Handle the chat interface and interactions for the specified role."""
    model = st.sidebar.selectbox(
        'Choose a model',
        ['llama3-8b-8192', 'llama3-70b-8192', 'gemma-7b-lt', 'mixtral-8x7b-32768', 'llama2-70b-4096'],
        index=0
    )
    memory_length = st.sidebar.slider('Conversational memory length:', 50000, 200000, value=100000)

    if 'conversation' not in st.session_state or st.session_state.get('reset', False):
        try:
            st.session_state.conversation = init_conversation(memory_length, model)
            st.session_state.reset = False
        except ValueError:
            st.error("Failed to initialize conversation due to missing API key.")
            return

    user_question = st.text_area("He Aha To Patai?:", value="", height=50)
    if len(user_question) > 10024:
        st.error("Question is very long. Please keep it under 10024 characters.")
        return

    if st.button('Submit') and user_question:
        st.session_state.last_question = user_question  # Store last question
        with st.spinner(f"Loading Up For a {role}!!..."):
            response_data = st.session_state.conversation(user_question)
            response_text = response_data.get('response', "No response received.")  # Extracting the response text
            if response_text:
                st.session_state.last_response = response_text  # Store last response
                st.success(f"{role} ({action}):")
                st.write(response_text)  # Displaying the response text directly
            else:
                st.error("No response received. Please try again.")

        st.session_state.reset = False  # Signal to reset on next run

        if st.button('Hear Response'):
            speak_response(st.session_state.last_response)

    if st.button('Clear Conversation'):
        st.session_state.last_question = ""
        st.session_state.last_response = ""
        st.session_state.reset = True

def Manu(delegation):
    chat_interface("Manu", delegation)

def Lawyer(kings_counsil):
    chat_interface("Lawyer", kings_counsil)

def Genealogist():
    chat_interface("Genealogist", "Whakapapa")

def Historian(research_agent):
    chat_interface("Historian", research_agent)
