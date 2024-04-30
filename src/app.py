import streamlit as st
import os

# This Defines the functions for each chat assistant 
from manage_chat import Manu, Lawyer, Genealogist, Historian

def check_environment_vars():
    """Check if necessary environment variables are set."""
    if "GROQ_API_KEY" not in os.environ:
        st.error("GROQ_API_KEY environment variable not set.")
        st.stop()

def load_css():
    """Load and apply CSS styles from a local file to the UI."""
    if 'css_style' not in st.session_state:
        try:
            with open("style.css", "r") as f:
                st.session_state.css_style = f"<style>{f.read()}</style>"
        except FileNotFoundError:
            st.warning("No style.css file found.")
    st.markdown(st.session_state.css_style, unsafe_allow_html=True)

def init_ui():
    """Initialize the UI components, especially the sidebar for navigation."""
    load_css()
    st.sidebar.title("Navigation")
    return st.sidebar.radio("Choose a page", ["Manu", "Lawyer", "Genealogist", "Historian"])

def main():
    """Define the structure and flow of the application."""
    check_environment_vars()
    page = init_ui()
    # Display the selected page
    if page == "Manu":
        st.title("Chat with Manu!")
        st.write("Kia Ora! I'm Manu, Your friendly assistant.")
        Manu(delegation=0)
    elif page == "Lawyer":
        st.title("Chat with Ture!")
        st.write("Kia Ora! I'm Ture, Your Friendly Law Assistant.")
        Lawyer(kings_counsil=1)
    elif page == "Genealogist":
        st.title("Chat with Whakapapa!")
        st.write("Kia Ora! I'm Whakapapa, Your Friendly Maori Genealogy Assistant.")
        Genealogist()
    elif page == "Historian":
        st.title("Chat with Tumu!")
        st.write("Kia Ora! I'm Tumu Korero, Your Friendly Maori History Assistant.")
        Historian(research_agent=2)
    else:
        st.write("Please select a page.")

if __name__ == "__main__":
    main()
