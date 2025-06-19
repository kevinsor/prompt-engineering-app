import streamlit as st


def render_sidebar():
    """Render the sidebar navigation and testing information"""

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "📚 Subject-Specific Prompts", "🎯 Prompt Techniques",
         "🔧 Prompt Builder", "🧪 Test Prompts", "💡 Tips & Best Practices", "📝 My Prompts"]
    )

    # Testing Information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧪 Prompt Testing")

    st.sidebar.markdown("**📚 Educational Simulator**")
    st.sidebar.markdown("• Instant quality analysis")
    st.sidebar.markdown("• Learning-focused responses")
    st.sidebar.markdown("• Always available")

    st.sidebar.markdown("**🎯 Quick Benefits:**")
    st.sidebar.markdown("• Practice prompt engineering")
    st.sidebar.markdown("• Get improvement suggestions")
    st.sidebar.markdown("• See quality scores instantly")

    # Prompt quality tips
    if page == "🧪 Test Prompts":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💡 Quick Tips")

        st.sidebar.success("✅ Include your grade level")
        st.sidebar.success("✅ Ask AI to be your tutor")
        st.sidebar.success("✅ Be specific about what you need")
        st.sidebar.success("✅ Request step-by-step guidance")

        st.sidebar.markdown("""
        <div style="font-size: 0.8em; color: #666;">
        <strong>Goal:</strong> Create prompts that consistently score 8+/10 for excellent AI responses!
        </div>
        """, unsafe_allow_html=True)

    # Help section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ❓ Need Help?")

    if st.sidebar.button("📖 Quick Start Guide"):
        st.sidebar.markdown("""
        **Getting Started:**
        1. 📚 Browse subject templates
        2. 🔧 Build custom prompts  
        3. 🧪 Test and get feedback
        4. 📈 Improve based on scores
        5. 💾 Save your best prompts
        """)

    st.sidebar.markdown("""
    <div style="font-size: 0.8em; color: #666; margin-top: 20px;">
    💡 <strong>Focus:</strong> This app teaches you to create prompts that work with any AI system - ChatGPT, Claude, Gemini, and more!
    </div>
    """, unsafe_allow_html=True)

    return page