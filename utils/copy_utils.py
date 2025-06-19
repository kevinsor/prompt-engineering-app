import streamlit as st


def create_copy_button(text, button_text="📋 Copy", key=None):
    """Create a copy button that shows text for easy copying"""

    # Create unique key
    button_key = f"copy_btn_{key}" if key else "copy_btn"

    if st.button(button_text, key=button_key):
        # Show text in a text area for easy copying
        st.success("📋 Text ready to copy! Select all text below and copy:")
        st.text_area(
            "Select all (Ctrl+A or Cmd+A) then copy (Ctrl+C or Cmd+C):",
            value=text,
            height=150,
            key=f"copy_area_{button_key}",
            help="Click in this box, press Ctrl+A (or Cmd+A on Mac) to select all, then Ctrl+C (or Cmd+C on Mac) to copy"
        )

    return True


def create_copy_section(text, title="Copy this prompt"):
    """Create a section with text display and copy button"""

    st.markdown(f"**{title}:**")

    # Display the text in a code block for easy reading
    st.code(text, language="text")

    # Add the copy button
    create_copy_button(text, "📋 Show Copy Area", key=f"copy_{abs(hash(text))}")

    return True