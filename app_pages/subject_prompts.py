import streamlit as st
from datetime import datetime
from data.constants import SUBJECT_PROMPTS
from utils.copy_utils import create_copy_button


def show_subject_prompts():
    """Display subject-specific prompt templates"""
    st.markdown('<h2 class="section-header">📚 Subject-Specific Prompt Templates</h2>', unsafe_allow_html=True)

    # Subject selection
    selected_subject = st.selectbox("Choose your subject:", list(SUBJECT_PROMPTS.keys()))

    st.markdown(f"### {selected_subject} Prompts")

    for category, prompt in SUBJECT_PROMPTS[selected_subject].items():
        with st.expander(f"📋 {category}"):
            st.markdown(f"""
            <div class="prompt-example">
            <strong>Template:</strong><br>
            {prompt}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 1])
            with col1:
                # Create copy button
                create_copy_button(prompt, "📋 Copy", key=f"copy_{selected_subject}_{category}")
            with col2:
                if st.button(f"⭐ Save", key=f"save_{selected_subject}_{category}"):
                    # Check if this exact prompt is already in favorites
                    already_saved = any(
                        fav['prompt'] == prompt for fav in st.session_state.favorites
                    )
                    if not already_saved:
                        st.session_state.favorites.append({
                            'subject': selected_subject,
                            'category': category,
                            'prompt': prompt,
                            'date': datetime.now().strftime("%Y-%m-%d")
                        })
                        st.success("Added to favorites!")
                    else:
                        st.info("Already in favorites!")