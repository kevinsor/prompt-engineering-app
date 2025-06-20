import streamlit as st


def render_sidebar():
    """Render the sidebar navigation and prompt engineering information"""

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "📚 Subject-Specific Prompts", "🎯 Prompt Techniques",
         "🔧 Prompt Builder", "💡 Tips & Best Practices", "📝 My Prompts"]
    )

    # Prompt Engineering Information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎓 Prompt Engineering")

    st.sidebar.markdown("**📚 Learn to Create:**")
    st.sidebar.markdown("• Effective educational prompts")
    st.sidebar.markdown("• Clear learning objectives")
    st.sidebar.markdown("• Better AI conversations")

    st.sidebar.markdown("**🎯 Key Benefits:**")
    st.sidebar.markdown("• Get better AI responses")
    st.sidebar.markdown("• Learn more effectively")
    st.sidebar.markdown("• Build transferable skills")

    # Quick tips section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Quick Tips")

    st.sidebar.success("✅ Always specify your grade level")
    st.sidebar.success("✅ Ask AI to be your tutor")
    st.sidebar.success("✅ Be specific about what you need")
    st.sidebar.success("✅ Request step-by-step guidance")

    st.sidebar.markdown("""
    <div style="font-size: 0.8em; color: #666;">
    <strong>Goal:</strong> Create prompts that work with any AI system - ChatGPT, Claude, Gemini, and more!
    </div>
    """, unsafe_allow_html=True)

    # Help section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ❓ Need Help?")

    if st.sidebar.button("📖 Quick Start Guide"):
        st.sidebar.markdown("""
        **Getting Started:**
        1. 📚 Browse subject templates
        2. 🎯 Learn prompt techniques  
        3. 🔧 Build custom prompts
        4. 📋 Copy and use with AI
        5. 💾 Save your best prompts
        """)

    st.sidebar.markdown("""
    <div style="font-size: 0.8em; color: #666; margin-top: 20px;">
    💡 <strong>Focus:</strong> Master prompt engineering to enhance your learning with any AI system!
    </div>
    """, unsafe_allow_html=True)

    return page