import streamlit as st
from data.constants import PROMPT_TECHNIQUES


def show_prompt_techniques():
    """Display prompt engineering techniques and examples"""
    st.markdown('<h2 class="section-header">🎯 Effective Prompt Techniques</h2>', unsafe_allow_html=True)

    st.write("Master these techniques to get better responses from AI language models:")

    for technique, details in PROMPT_TECHNIQUES.items():
        with st.expander(f"🎪 {technique}"):
            st.write(f"**Description:** {details['description']}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Good Example:**")
                st.markdown(f"""
                <div class="prompt-example">
                {details['good_example']}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("**❌ Poor Example:**")
                st.markdown(f"""
                <div class="warning-box">
                {details['bad_example']}
                </div>
                """, unsafe_allow_html=True)