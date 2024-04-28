import streamlit as st
import os
import logging
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Configuring logging
logging.basicConfig(level=logging.ERROR)

def init_conversation(memory_length, model):
    """Initializes and returns a conversation chain with memory and model setup."""
    memory = ConversationBufferWindowMemory(k=memory_length)
    groq_api_key = os.getenv('GROQ_API_KEY', 'your-default-api-key')
    if groq_api_key == 'your-default-api-key':
        logging.error("GROQ API Key is missing. Please set it in your environment variables.")
        raise ValueError("API Key is missing")
    groq_chat = ChatGroq(api_key=groq_api_key, model_name=model)
    return ConversationChain(llm=groq_chat, verbose=True, memory=memory)

def chat_interface(role):
    """Handle the chat interface and interactions based on the role."""
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
        with st.spinner(f"Loading Up For {role}!!..."):
            response_data = st.session_state.conversation(user_question)
            response_text = response_data.get('response', "No response received.")  # Extracting the response text
            if response_text:
                st.session_state.last_response = response_text  # Store last response
                st.success(role + ":")
                st.write(response_text)  # Displaying the response text directly
            else:
                st.error("No response received. Please try again.")

        st.session_state.reset = False  # Signal to reset on next run

    if st.button('Clear Conversation'):
        st.session_state.last_question = ""
        st.session_state.last_response = ""
        st.session_state.reset = True

def Manu():
    chat_interface("Manu")

def Lawyer():
    chat_interface("Ture")

def Genealogist():
    chat_interface("Whakapapa")

def Historian():
    chat_interface("Tumu")
