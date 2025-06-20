import streamlit as st

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_prompts' not in st.session_state:
        st.session_state.user_prompts = []
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []