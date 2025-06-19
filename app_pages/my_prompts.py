import streamlit as st
from utils.copy_utils import create_copy_button


def show_my_prompts():
    """Display saved prompts and favorites"""
    st.markdown('<h2 class="section-header">📝 My Saved Prompts</h2>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💾 My Custom Prompts", "⭐ Favorites"])

    with tab1:
        if st.session_state.user_prompts:
            for i, prompt_data in enumerate(st.session_state.user_prompts):
                with st.expander(f"{prompt_data['subject']} - {prompt_data['topic']} ({prompt_data['date']})"):
                    st.write(prompt_data['prompt'])

                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        # Create copy button
                        create_copy_button(prompt_data['prompt'], "📋 Copy", key=f"copy_custom_{i}")
                    with col2:
                        if st.button(f"🗑️ Delete", key=f"delete_custom_{i}"):
                            st.session_state.user_prompts.pop(i)
                            st.rerun()
                    with col3:
                        if st.button(f"🧪 Test", key=f"test_custom_{i}"):
                            st.session_state.prompt_to_test = prompt_data['prompt']
                            st.session_state.test_prompt_source = f"My Prompts - {prompt_data['topic']}"
                            st.success("Prompt loaded for testing! Go to Test Prompts page.")
        else:
            st.info("No custom prompts saved yet. Use the Prompt Builder to create some!")

    with tab2:
        if st.session_state.favorites:
            for i, fav in enumerate(st.session_state.favorites):
                with st.expander(f"{fav['subject']} - {fav['category']} ({fav['date']})"):
                    st.write(fav['prompt'])

                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        # Create copy button
                        create_copy_button(fav['prompt'], "📋 Copy", key=f"copy_fav_{i}")
                    with col2:
                        if st.button(f"🗑️ Remove", key=f"delete_fav_{i}"):
                            st.session_state.favorites.pop(i)
                            st.rerun()
                    with col3:
                        if st.button(f"🧪 Test", key=f"test_fav_{i}"):
                            st.session_state.prompt_to_test = fav['prompt']
                            st.session_state.test_prompt_source = f"Favorites - {fav['category']}"
                            st.success("Prompt loaded for testing! Go to Test Prompts page.")
        else:
            st.info("No favorites saved yet. Browse the subject-specific prompts to add some!")