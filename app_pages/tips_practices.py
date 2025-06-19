import streamlit as st


def show_tips_and_practices():
    """Display tips and best practices"""
    st.markdown('<h2 class="section-header">💡 Tips & Best Practices</h2>', unsafe_allow_html=True)

    # Academic integrity section
    st.markdown("### 🎓 Academic Integrity")
    st.markdown("""
    <div class="warning-box">
    <strong>⚠️ Important:</strong> Always use AI as a learning tool, not a replacement for your own thinking. 
    Check your school's AI policy and always cite AI assistance when required.
    </div>
    """, unsafe_allow_html=True)

    # Effective strategies
    strategies = {
        "🎯 Be Specific and Clear": [
            "Instead of 'help with math,' try 'explain how to solve quadratic equations using the quadratic formula'",
            "Provide your current understanding level",
            "Specify what type of help you need (explanation, examples, practice problems)"
        ],
        "👨‍🏫 Use AI as a Tutor": [
            "Ask AI to take the role of a patient tutor: 'Act as my biology tutor and guide me through photosynthesis'",
            "Request Socratic questioning: 'Instead of telling me, ask questions that help me figure out the causes of WWI'",
            "Have AI check your explanations: 'Let me explain this concept, then tell me what I got wrong'"
        ],
        "🧠 Active Learning Techniques": [
            "Share your understanding and ask for gap analysis: 'Here's what I know about X, what am I missing?'",
            "Request practice questions from your notes: 'Create quiz questions based on these lecture notes'",
            "Ask for error analysis: 'I got this problem wrong, help me understand where my thinking went off track'"
        ],
        "🔄 Iterate and Refine": [
            "If the first response isn't helpful, ask follow-up questions",
            "Request different explanations or approaches",
            "Ask for clarification on confusing parts"
        ],
        "📚 Use AI for Learning, Not Cheating": [
            "Ask for explanations and teaching, not just answers",
            "Use AI to check your work and understand mistakes",
            "Generate practice problems to test your understanding"
        ],
        "🎨 Get Creative with Applications": [
            "Ask for analogies and real-world examples",
            "Request different perspectives on topics",
            "Use AI to create mnemonics and memory aids"
        ],
        "🤝 Interactive Learning": [
            "Practice presentations by explaining concepts to AI",
            "Have mock discussions about complex topics",
            "Use AI to debate different viewpoints on historical events or literature"
        ],
        "📖 Study Material Enhancement": [
            "Turn passive notes into active study materials",
            "Create flashcards and quizzes from textbook content",
            "Generate practice exams based on your syllabus"
        ]
    }

    for strategy, tips in strategies.items():
        with st.expander(strategy):
            for tip in tips:
                st.write(f"• {tip}")

    # Common mistakes
    st.markdown("### ❌ Common Mistakes to Avoid")
    mistakes = [
        "Being too vague in your requests",
        "Not providing context about your level or background",
        "Accepting the first answer without verification",
        "Using AI to do your work instead of helping you learn",
        "Not asking follow-up questions when confused",
        "Asking for answers instead of understanding",
        "Not sharing your current knowledge level",
        "Avoiding mistakes instead of learning from them"
    ]

    for mistake in mistakes:
        st.write(f"• {mistake}")

    # Additional practical tips
    st.markdown("### 🔧 Practical Implementation Tips")
    st.markdown("""
    <div class="tip-box">
    <strong>🚀 Getting Started:</strong><br>
    • Start with simple prompts and gradually make them more sophisticated<br>
    • Keep a collection of prompts that work well for your subjects<br>
    • Experiment with different approaches for the same question<br>
    • Use the testing feature to see how different models respond
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="prompt-example">
    <strong>💬 Building Better Conversations with AI:</strong><br>
    • Treat AI like a knowledgeable study partner, not a search engine<br>
    • Don't hesitate to ask for clarification: "Can you explain that differently?"<br>
    • Build on previous responses: "Now that I understand X, how does Y relate to it?"<br>
    • Ask for alternative explanations: "Can you give me another way to think about this?"
    </div>
    """, unsafe_allow_html=True)