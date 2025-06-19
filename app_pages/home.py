import streamlit as st
from data.constants import SUBJECT_PROMPTS, PROMPT_TECHNIQUES


def show_home_page():
    """Display the home page with app overview"""
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Welcome to Your AI Learning Companion! 🚀")
        st.write("""
        This app is designed to help you harness the power of AI language models for your education. 
        Learn how to craft effective prompts that will help you:

        - **Understand complex concepts** with clear explanations
        - **Solve problems step-by-step** with guided assistance  
        - **Improve your writing** with constructive feedback
        - **Create study materials** tailored to your needs
        - **Prepare for exams** with personalized practice
        """)

        st.markdown("### Quick Start Guide")
        st.info("""
        1. **Browse Subject-Specific Prompts** - Find ready-to-use prompts for your subjects
        2. **Learn Prompt Techniques** - Master the art of effective AI communication  
        3. **Use the Prompt Builder** - Create custom prompts with guided assistance
        4. **Test Your Prompts** - See how they perform with real AI models
        5. **Save Your Favorites** - Keep track of prompts that work well for you
        """)

    with col2:
        st.markdown("### 📊 Quick Stats")
        st.metric("Available Prompt Templates", len([p for subject in SUBJECT_PROMPTS.values() for p in subject]))
        st.metric("Technique Categories", len(PROMPT_TECHNIQUES))
        st.metric("Your Saved Prompts", len(st.session_state.user_prompts))

        st.markdown("### 🎯 Featured Tip")
        st.markdown("""
        <div class="tip-box">
        <strong>💡 Pro Tip:</strong> Always specify your academic level and context when asking for help. 
        This helps the AI tailor its response to your understanding level!
        </div>
        """, unsafe_allow_html=True)

    # How to Better Use AI for Learning section
    st.markdown("---")
    st.markdown("## 🎓 How to Better Use AI for Learning")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🧠 The Feynman Technique with AI")
        st.markdown("""
        <div class="tip-box">
        <strong>Master any concept in 4 steps:</strong><br><br>
        1. <strong>Explain</strong> a concept to the AI in your own words<br>
        2. <strong>Ask</strong> the AI to identify gaps or errors in your explanation<br>
        3. <strong>Simplify</strong> complex parts with AI's help<br>
        4. <strong>Practice</strong> teaching the concept back until it's crystal clear
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⚡ Power Prompts for Learning")
        st.markdown("""
        <div class="warning-box">
        <strong>Copy these proven prompts:</strong><br><br>
        • "I think I understand X, but I'm not sure. Quiz me and point out what I'm missing."<br><br>
        • "Act as my study partner. Let's discuss the pros and cons of [theory/event/concept]."<br><br>
        • "I made this mistake: [show error]. Help me understand the thinking error so I don't repeat it."<br><br>
        • "Create an analogy that helps me understand [complex concept] using [familiar topic]."
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📚 From Lecture Notes to Deep Understanding")
        st.markdown("""
        <div class="tip-box">
        <strong>Transform passive notes into active learning:</strong><br><br>
        • <strong>Upload or paste your lecture notes</strong> and ask: "Create thought-provoking questions about this material"<br><br>
        • <strong>Request connections:</strong> "What are the key concepts here and how do they connect?"<br><br>
        • <strong>Find applications:</strong> "What real-world applications demonstrate these principles?"<br><br>
        • <strong>Prepare for exams:</strong> "What would be challenging exam questions based on this content?"
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🎯 Smart Learning Strategies")
        st.markdown("""
        <div class="prompt-example">
        <strong>Instead of asking:</strong> "What is photosynthesis?"<br>
        <strong>Try this:</strong> "Act as my biology tutor. I understand that plants make food from sunlight, but I'm confused about the chemical process. Can you guide me through it step by step?"
        </div>
        """, unsafe_allow_html=True)