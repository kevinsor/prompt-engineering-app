import streamlit as st
from config.app_config import configure_page, load_custom_css
from utils.session_state import initialize_session_state
from components.sidebar import render_sidebar
from app_pages.home import show_home_page
from app_pages.subject_prompts import show_subject_prompts
from app_pages.prompt_techniques import show_prompt_techniques
from app_pages.prompt_builder import show_prompt_builder
from app_pages.tips_practices import show_tips_and_practices
from app_pages.my_prompts import show_my_prompts


def main():
    """Main application entry point"""
    # Configure page
    configure_page()

    # Load custom CSS
    load_custom_css()

    # Initialize session state
    initialize_session_state()

    # Main header
    st.markdown('<h1 class="main-header">🎓 Student AI Prompt Engineering Hub</h1>', unsafe_allow_html=True)

    # Render sidebar and get selected page
    page = render_sidebar()

    # Route to appropriate page
    if page == "🏠 Home":
        show_home_page()
    elif page == "📚 Subject-Specific Prompts":
        show_subject_prompts()
    elif page == "🎯 Prompt Techniques":
        show_prompt_techniques()
    elif page == "🔧 Prompt Builder":
        show_prompt_builder()
    elif page == "💡 Tips & Best Practices":
        show_tips_and_practices()
    elif page == "📝 My Prompts":
        show_my_prompts()


if __name__ == "__main__":
    main()