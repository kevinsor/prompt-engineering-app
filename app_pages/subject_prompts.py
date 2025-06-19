import streamlit as st
from datetime import datetime
from data.constants import SUBJECT_PROMPTS


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

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                if st.button(f"📋 Copy", key=f"copy_{selected_subject}_{category}"):
                    # Show copy instructions
                    st.info("""
                    **To copy this prompt:**
                    1. Highlight the text in the blue box above
                    2. Right-click and select "Copy" or press Ctrl+C
                    3. Paste into any AI system
                    """)
            with col2:
                # Create a text area for easy copying of this specific prompt
                copy_key = f"copy_area_{selected_subject}_{category}"
                if st.button(f"📝 Select Text", key=f"select_{selected_subject}_{category}"):
                    st.text_area(
                        f"Copy this {category} prompt:",
                        value=prompt,
                        height=100,
                        key=copy_key,
                        help="Click in this box, press Ctrl+A to select all, then Ctrl+C to copy"
                    )
            with col3:
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
            with col4:
                if st.button(f"🧪 Test", key=f"test_{selected_subject}_{category}"):
                    st.session_state.prompt_to_test = prompt
                    st.session_state.test_prompt_source = f"{selected_subject} - {category}"
                    st.success("Prompt loaded for testing! Go to Test Prompts page.")