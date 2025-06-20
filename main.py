import streamlit as st


# Lazy imports for better performance
def get_config():
    from config.app_config import configure_page, load_custom_css
    return configure_page, load_custom_css


def get_session_utils():
    from utils.session_state import initialize_session_state
    return initialize_session_state


def get_sidebar():
    from components.sidebar import render_sidebar
    return render_sidebar


def load_home_page():
    """Lazy load home page"""
    from app_pages.home import show_home_page
    show_home_page()


def load_subject_prompts():
    """Lazy load subject prompts page"""
    from app_pages.subject_prompts import show_subject_prompts
    show_subject_prompts()


def load_prompt_techniques():
    """Lazy load prompt techniques page"""
    from app_pages.prompt_techniques import show_prompt_techniques
    show_prompt_techniques()


def load_prompt_builder():
    """Lazy load prompt builder page"""
    from app_pages.prompt_builder import show_prompt_builder
    show_prompt_builder()


def load_tips_practices():
    """Lazy load tips and practices page"""
    from app_pages.tips_practices import show_tips_and_practices
    show_tips_and_practices()


def load_my_prompts():
    """Lazy load my prompts page"""
    from app_pages.my_prompts import show_my_prompts
    show_my_prompts()


def main():
    """Main application entry point - optimized for speed"""

    # Initialize core functions
    configure_page, load_custom_css = get_config()
    initialize_session_state = get_session_utils()
    render_sidebar = get_sidebar()

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

    # Lazy load pages to reduce initial load time
    if page == "🏠 Home":
        load_home_page()
    elif page == "📚 Subject-Specific Prompts":
        load_subject_prompts()
    elif page == "🎯 Prompt Techniques":
        load_prompt_techniques()
    elif page == "🔧 Prompt Builder":
        load_prompt_builder()
    elif page == "💡 Tips & Best Practices":
        load_tips_practices()
    elif page == "📝 My Prompts":
        load_my_prompts()


if __name__ == "__main__":
    main()