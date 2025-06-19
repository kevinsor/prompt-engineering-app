import streamlit as st
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import time

# Page configuration
st.set_page_config(
    page_title="Student AI Prompt Engineering Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff7f0e;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .prompt-example {
        background-color: #e8f4fd;
        color: #1a1a1a;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        border: 1px solid #d1ecf1;
    }
    .tip-box {
        background-color: #e8f5e8;
        color: #1a1a1a;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ca02c;
        margin: 1rem 0;
        border: 1px solid #c3e6cb;
    }
    .warning-box {
        background-color: #fff8e1;
        color: #1a1a1a;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        border: 1px solid #f5c6cb;
    }

    /* Ensure form elements have proper contrast */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }

    /* Fix expander content visibility */
    .streamlit-expanderContent {
        background-color: #ffffff;
        color: #000000;
    }

    /* Ensure button text is visible */
    .stButton > button {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #cccccc;
    }

    .stButton > button:hover {
        background-color: #f0f0f0;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# Sample data for prompts and templates
SUBJECT_PROMPTS = {
    "Mathematics": {
        "Problem Solving": "I need help solving this math problem step by step: [YOUR PROBLEM]. Please explain each step clearly and show your work.",
        "Concept Explanation": "Can you explain the concept of [MATH CONCEPT] in simple terms with examples? I'm a [GRADE LEVEL] student.",
        "Practice Problems": "Generate 3 practice problems about [TOPIC] with varying difficulty levels. Include solutions.",
        "Tutor Role": "Act as my math tutor. I'm struggling with [SPECIFIC TOPIC]. Guide me through understanding it by asking questions and letting me work through examples.",
        "Error Analysis": "I solved this problem but got the wrong answer: [SHOW YOUR WORK]. Help me identify where I went wrong and understand the correct approach.",
        "Gap Assessment": "Here's what I understand about [MATH CONCEPT]: [YOUR UNDERSTANDING]. What important details am I missing?"
    },
    "Science": {
        "Lab Report Help": "Help me structure a lab report for an experiment about [EXPERIMENT TOPIC]. What sections should I include?",
        "Concept Connection": "Explain how [CONCEPT A] relates to [CONCEPT B] in [SUBJECT AREA]. Use real-world examples.",
        "Study Guide": "Create a study guide for [SCIENCE TOPIC] covering the main concepts, key terms, and important formulas.",
        "Misconception Check": "What are common misconceptions students have about [SCIENCE TOPIC]? Help me avoid these errors.",
        "Question Generation": "Based on my notes about [TOPIC], create quiz questions that test deep understanding, not just memorization.",
        "Teaching Back": "Let me explain [SCIENTIFIC PROCESS] as I understand it: [YOUR EXPLANATION]. Correct any errors and fill gaps."
    },
    "English/Literature": {
        "Essay Structure": "Help me create an outline for a [TYPE] essay about [TOPIC]. My thesis is: [YOUR THESIS]",
        "Text Analysis": "Analyze the theme of [THEME] in [BOOK/POEM]. Provide specific examples from the text.",
        "Writing Improvement": "Review this paragraph and suggest improvements for clarity and flow: [YOUR PARAGRAPH]",
        "Critical Thinking": "Help me analyze the arguments in [TEXT/ARTICLE]. What evidence supports the claims? What are potential counterarguments?",
        "Discussion Prep": "I need to discuss [LITERARY WORK] in class. Ask me Socratic questions to help me think deeply about themes and meanings.",
        "Writing Coach": "Act as my writing coach. I'll share my draft paragraph, and you help me improve it through guided questions."
    },
    "History": {
        "Timeline Creation": "Create a timeline of key events related to [HISTORICAL TOPIC] with brief explanations.",
        "Cause and Effect": "Explain the causes and effects of [HISTORICAL EVENT]. How did it impact society?",
        "Comparative Analysis": "Compare and contrast [EVENT/PERSON A] and [EVENT/PERSON B] in terms of [SPECIFIC ASPECT].",
        "Primary Source Analysis": "Help me analyze this primary source document: [DOCUMENT]. What does it reveal about the time period?",
        "Historical Thinking": "Instead of telling me about [HISTORICAL EVENT], ask me guiding questions that help me analyze the causes myself.",
        "Connection Making": "Help me connect [HISTORICAL PERIOD] to current events. What patterns or lessons can we identify?"
    },
    "General Study": {
        "Note Taking": "Help me organize my notes on [TOPIC]. What are the main points I should focus on?",
        "Exam Preparation": "Create a study plan for my upcoming [SUBJECT] exam covering [TOPICS]. I have [TIME PERIOD] to prepare.",
        "Research Starting Point": "I need to research [TOPIC] for a project. What are the key questions I should investigate?",
        "Study Strategy": "I'm a [LEARNING STYLE] learner studying [SUBJECT]. What study techniques would work best for me?",
        "Recall Practice": "Quiz me on [TOPIC] using active recall. After each answer, tell me what I got right and what needs improvement.",
        "Presentation Practice": "I need to present [TOPIC] to my class. Let me practice explaining it to you and give me feedback on clarity."
    },
    "Test Preparation": {
        "Question Generation": "Based on these lecture notes/textbook chapters: [CONTENT], create practice exam questions with varying difficulty levels.",
        "Weak Spot Analysis": "I'm preparing for a [SUBJECT] test. Here are the topics I struggle with: [LIST]. Help me create a focused study plan.",
        "Mock Interview": "Act as my teacher and conduct a mock oral exam on [TOPIC]. Ask me questions and provide feedback.",
        "Memory Techniques": "Help me create mnemonics, acronyms, or memory devices for remembering [SPECIFIC INFORMATION].",
        "Study Schedule": "I have [TIME PERIOD] to prepare for [NUMBER] exams in [SUBJECTS]. Help me create an effective study schedule.",
        "Review Session": "Let's have a review session on [TOPIC]. Ask me questions, and when I get something wrong, guide me to the right answer."
    }
}

PROMPT_TECHNIQUES = {
    "Be Specific": {
        "description": "Provide clear, detailed instructions rather than vague requests.",
        "good_example": "Explain photosynthesis for a 10th-grade biology student, including the chemical equation and the role of chloroplasts.",
        "bad_example": "Tell me about photosynthesis."
    },
    "Set Context": {
        "description": "Give background information about your level, subject, and specific needs.",
        "good_example": "I'm a college freshman taking introductory psychology. Can you explain classical conditioning with examples I can relate to in everyday life?",
        "bad_example": "What is classical conditioning?"
    },
    "Ask for Examples": {
        "description": "Request concrete examples to better understand abstract concepts.",
        "good_example": "Explain supply and demand in economics with three real-world examples from different industries.",
        "bad_example": "Explain supply and demand."
    },
    "Request Step-by-Step": {
        "description": "Ask for processes to be broken down into manageable steps.",
        "good_example": "Walk me through solving quadratic equations step by step, starting with the simplest form.",
        "bad_example": "How do you solve quadratic equations?"
    },
    "Specify Format": {
        "description": "Tell the AI how you want the information presented.",
        "good_example": "Create a bullet-point summary of the causes of World War I, organized by category (political, economic, social).",
        "bad_example": "What caused World War I?"
    },
    "Role-Based Learning": {
        "description": "Ask the AI to take on the role of a tutor, teacher, or learning assistant for personalized guidance.",
        "good_example": "Act as my calculus tutor. I'm struggling with integration by parts. Guide me through the process with a practice problem, asking me questions along the way to check my understanding.",
        "bad_example": "Help me with calculus."
    },
    "Socratic Method": {
        "description": "Have the AI ask you questions to guide your thinking rather than giving direct answers.",
        "good_example": "I need to understand why the American Civil War started. Instead of telling me directly, ask me guiding questions that help me think through the causes and come to my own conclusions.",
        "bad_example": "What caused the American Civil War?"
    },
    "Knowledge Gap Analysis": {
        "description": "Share your current understanding and ask the AI to identify and fill in gaps.",
        "good_example": "Here's what I understand about mitosis: cells divide to make two identical cells, and DNA gets copied. What important details am I missing? Where are the gaps in my understanding?",
        "bad_example": "Explain cell division."
    },
    "Teaching by Explanation": {
        "description": "Explain a concept to the AI and ask for feedback on your understanding.",
        "good_example": "Let me explain photosynthesis as I understand it: [your explanation]. Please point out any errors in my explanation and help me correct my misconceptions.",
        "bad_example": "Is my understanding of photosynthesis correct?"
    },
    "Interactive Problem Solving": {
        "description": "Work through problems collaboratively with the AI, step by step.",
        "good_example": "I'm solving this physics problem about projectile motion. Let me show you my work so far: [your work]. Can you check my approach and guide me through the next steps?",
        "bad_example": "Solve this physics problem for me."
    },
    "Question Generation": {
        "description": "Ask the AI to create questions based on your study materials to test your understanding.",
        "good_example": "Based on these lecture notes about the Revolutionary War [attach notes], create 5 thought-provoking questions that would test my deep understanding, not just memorization.",
        "bad_example": "Make some questions about history."
    },
    "Misconception Identification": {
        "description": "Ask the AI to help identify and correct common misconceptions in your field of study.",
        "good_example": "I'm studying basic chemistry. What are the most common misconceptions students have about atomic structure, and how can I avoid them?",
        "bad_example": "Tell me about atoms."
    },
    "Active Recall Practice": {
        "description": "Use the AI to create recall exercises and test your memory of key concepts.",
        "good_example": "Quiz me on the major battles of World War II. After I answer each one, tell me what I got right, what I missed, and provide the correct information for what I got wrong.",
        "bad_example": "Tell me about World War II battles."
    },
    "Analogy and Metaphor": {
        "description": "Request analogies and metaphors to understand complex concepts through familiar comparisons.",
        "good_example": "I'm struggling to understand how neural networks work. Can you explain it using analogies to things I'm familiar with as a high school student?",
        "bad_example": "Explain neural networks."
    },
    "Elaborative Learning": {
        "description": "Ask the AI to help you connect new information to what you already know.",
        "good_example": "I just learned about supply and demand. Help me connect this concept to my previous knowledge of basic economics and real-world examples I've observed.",
        "bad_example": "I learned about supply and demand."
    },
    "Error Analysis": {
        "description": "Share your mistakes and ask the AI to help you understand why they happened and how to avoid them.",
        "good_example": "I got this math problem wrong: [show your work]. Can you analyze where my thinking went off track and help me understand the correct reasoning process?",
        "bad_example": "I got this wrong, what's the right answer?"
    },
    "Study Strategy Guidance": {
        "description": "Ask for personalized study strategies based on your learning style and subject matter.",
        "good_example": "I'm a visual learner preparing for a biology exam on cellular processes. What study techniques would work best for me, and can you help me create visual study aids?",
        "bad_example": "How should I study for my exam?"
    },
    "Presentation Preparation": {
        "description": "Use AI to help practice presentations and get feedback on your explanations.",
        "good_example": "I need to present on climate change to my class. Let me practice explaining the greenhouse effect to you, and then give me feedback on clarity and suggest improvements.",
        "bad_example": "Help me with my presentation."
    },
    "Critical Thinking Development": {
        "description": "Ask the AI to help you analyze arguments, evaluate evidence, and think critically about topics.",
        "good_example": "I'm reading this article about renewable energy. Help me identify the main arguments, evaluate the evidence presented, and think critically about potential counterarguments.",
        "bad_example": "What do you think about this article?"
    },
    "Synthesis and Integration": {
        "description": "Ask the AI to help you combine information from multiple sources or subjects.",
        "good_example": "I'm studying both history and literature. Help me understand how the social movements of the 1960s influenced the literature of that period, connecting specific historical events to literary works.",
        "bad_example": "How are history and literature related?"
    }
}


def initialize_session_state():
    """Initialize session state variables"""
    if 'user_prompts' not in st.session_state:
        st.session_state.user_prompts = []
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    if 'api_provider' not in st.session_state:
        st.session_state.api_provider = 'OpenAI'


def main():
    initialize_session_state()

    # Main header
    st.markdown('<h1 class="main-header">🎓 Student AI Prompt Engineering Hub</h1>', unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "📚 Subject-Specific Prompts", "🎯 Prompt Techniques", "🔧 Prompt Builder", "🧪 Test Prompts",
         "💡 Tips & Best Practices", "📝 My Prompts"]
    )

    # API Configuration in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 API Configuration")

    api_provider = st.sidebar.selectbox(
        "Choose LLM Provider:",
        ["OpenAI", "Anthropic", "Groq", "Ollama (Local)"],
        index=["OpenAI", "Anthropic", "Groq", "Ollama (Local)"].index(st.session_state.api_provider)
    )
    st.session_state.api_provider = api_provider

    # API Key input
    if api_provider != "Ollama (Local)":
        api_key = st.sidebar.text_input(
            f"{api_provider} API Key:",
            type="password",
            help=f"Enter your {api_provider} API key to test prompts"
        )
        if api_key:
            st.session_state[f"{api_provider.lower()}_api_key"] = api_key
    else:
        ollama_url = st.sidebar.text_input(
            "Ollama Server URL:",
            value="http://localhost:11434",
            help="URL of your local Ollama server"
        )
        st.session_state.ollama_url = ollama_url

    if page == "🏠 Home":
        show_home_page()
    elif page == "📚 Subject-Specific Prompts":
        show_subject_prompts()
    elif page == "🎯 Prompt Techniques":
        show_prompt_techniques()
    elif page == "🔧 Prompt Builder":
        show_prompt_builder()
    elif page == "🧪 Test Prompts":
        show_test_prompts()
    elif page == "💡 Tips & Best Practices":
        show_tips_and_practices()
    elif page == "📝 My Prompts":
        show_my_prompts()


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

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"Copy", key=f"copy_{selected_subject}_{category}"):
                    st.success("Copied to clipboard! (Feature to be implemented)")
            with col2:
                if st.button(f"⭐ Save", key=f"save_{selected_subject}_{category}"):
                    if prompt not in st.session_state.favorites:
                        st.session_state.favorites.append({
                            'subject': selected_subject,
                            'category': category,
                            'prompt': prompt,
                            'date': datetime.now().strftime("%Y-%m-%d")
                        })
                        st.success("Added to favorites!")
                    else:
                        st.info("Already in favorites!")
            with col3:
                if st.button(f"🧪 Test", key=f"test_{selected_subject}_{category}"):
                    st.session_state.prompt_to_test = prompt
                    st.session_state.test_prompt_source = f"{selected_subject} - {category}"
                    st.switch_page = "🧪 Test Prompts"
                    st.success("Prompt loaded for testing! Go to Test Prompts page.")


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


def show_prompt_builder():
    """Interactive prompt builder tool"""
    st.markdown('<h2 class="section-header">🔧 Interactive Prompt Builder</h2>', unsafe_allow_html=True)

    st.write("Build a custom prompt by filling out the sections below:")

    with st.form("prompt_builder"):
        # Basic information
        st.markdown("### 📋 Basic Information")
        subject = st.selectbox("Subject Area:", ["Mathematics", "Science", "English/Literature", "History", "Other"])
        grade_level = st.selectbox("Your Grade Level:",
                                   ["Elementary", "Middle School", "High School", "College", "Graduate"])

        # Task type
        st.markdown("### 🎯 Task Type")
        task_type = st.selectbox("What do you need help with?", [
            "Explain a concept", "Solve a problem", "Review my work", "Create study materials",
            "Generate practice questions", "Analyze text", "Other"
        ])

        # Specific request
        st.markdown("### 📝 Your Specific Request")
        topic = st.text_input("Topic or specific question:")
        context = st.text_area("Additional context or background information:")

        # Output preferences
        st.markdown("### 📊 Output Preferences")
        col1, col2 = st.columns(2)
        with col1:
            format_pref = st.multiselect("Preferred format:", [
                "Step-by-step explanation", "Bullet points", "Examples",
                "Diagrams/Visual aids", "Practice problems", "Summary"
            ])
        with col2:
            detail_level = st.select_slider("Detail level:", ["Basic", "Moderate", "Detailed", "Comprehensive"])

        # Generate prompt
        submitted = st.form_submit_button("🚀 Generate Prompt")

    # Handle form submission outside the form
    if submitted:
        if topic:
            generated_prompt = build_custom_prompt(subject, grade_level, task_type, topic, context, format_pref,
                                                   detail_level)

            # Store the generated prompt in session state for saving
            st.session_state.current_generated_prompt = {
                'prompt': generated_prompt,
                'subject': subject,
                'topic': topic,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            }

            st.markdown("### 🎉 Your Generated Prompt:")
            st.markdown(f"""
            <div class="prompt-example">
            {generated_prompt}
            </div>
            """, unsafe_allow_html=True)

            # Save option - now outside the form
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("💾 Save This Prompt"):
                    st.session_state.user_prompts.append(st.session_state.current_generated_prompt)
                    st.success("Prompt saved!")
            with col2:
                if st.button("🧪 Test This Prompt"):
                    st.session_state.prompt_to_test = generated_prompt
                    st.session_state.test_prompt_source = f"Custom - {topic}"
                    st.success("Prompt loaded for testing! Go to Test Prompts page.")
        else:
            st.warning("Please enter a topic or question to generate a prompt.")

    # Display previously generated prompt if it exists
    elif 'current_generated_prompt' in st.session_state:
        st.markdown("### 🎉 Your Generated Prompt:")
        st.markdown(f"""
        <div class="prompt-example">
        {st.session_state.current_generated_prompt['prompt']}
        </div>
        """, unsafe_allow_html=True)

        # Save option for existing prompt
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 Save This Prompt"):
                if st.session_state.current_generated_prompt not in st.session_state.user_prompts:
                    st.session_state.user_prompts.append(st.session_state.current_generated_prompt)
                    st.success("Prompt saved!")
                else:
                    st.info("This prompt is already saved!")
        with col2:
            if st.button("🧪 Test This Prompt"):
                st.session_state.prompt_to_test = st.session_state.current_generated_prompt['prompt']
                st.session_state.test_prompt_source = f"Custom - {st.session_state.current_generated_prompt['topic']}"
                st.success("Prompt loaded for testing! Go to Test Prompts page.")


def build_custom_prompt(subject, grade_level, task_type, topic, context, format_pref, detail_level):
    """Build a custom prompt based on user inputs"""
    prompt_parts = []

    # Context setting
    prompt_parts.append(f"I'm a {grade_level.lower()} student studying {subject.lower()}.")

    if context:
        prompt_parts.append(f"Context: {context}")

    # Main request
    if task_type == "Explain a concept":
        prompt_parts.append(f"Please explain {topic} in a way that's appropriate for my level.")
    elif task_type == "Solve a problem":
        prompt_parts.append(f"Help me solve this problem step by step: {topic}")
    elif task_type == "Review my work":
        prompt_parts.append(f"Please review my work on {topic} and provide constructive feedback.")
    elif task_type == "Create study materials":
        prompt_parts.append(f"Create study materials for {topic} that will help me learn effectively.")
    elif task_type == "Generate practice questions":
        prompt_parts.append(f"Generate practice questions about {topic} with varying difficulty levels.")
    elif task_type == "Analyze text":
        prompt_parts.append(f"Help me analyze {topic} by identifying key themes, concepts, or arguments.")
    else:
        prompt_parts.append(f"Help me with {topic}.")

    # Format preferences
    if format_pref:
        format_text = ", ".join(format_pref).lower()
        prompt_parts.append(f"Please include {format_text} in your response.")

    # Detail level
    if detail_level == "Basic":
        prompt_parts.append("Keep the explanation simple and concise.")
    elif detail_level == "Comprehensive":
        prompt_parts.append("Provide a thorough, detailed explanation with multiple examples.")

    return " ".join(prompt_parts)


def call_openai_api(prompt: str, api_key: str, model: str = "gpt-3.5-turbo") -> Optional[str]:
    """Call OpenAI API with the given prompt"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"


def call_anthropic_api(prompt: str, api_key: str, model: str = "claude-3-haiku-20240307") -> Optional[str]:
    """Call Anthropic API with the given prompt"""
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": model,
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error calling Anthropic API: {str(e)}"


def call_groq_api(prompt: str, api_key: str, model: str = "llama3-8b-8192") -> Optional[str]:
    """Call Groq API with the given prompt"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error calling Groq API: {str(e)}"


def call_ollama_api(prompt: str, server_url: str, model: str = "llama2") -> Optional[str]:
    """Call local Ollama API with the given prompt"""
    try:
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{server_url}/api/generate",
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error calling Ollama API: {str(e)}"


def test_prompt_with_llm(prompt: str, provider: str) -> Optional[str]:
    """Test a prompt with the selected LLM provider"""

    if provider == "OpenAI":
        api_key = st.session_state.get("openai_api_key")
        if not api_key:
            return "Error: OpenAI API key not provided"
        return call_openai_api(prompt, api_key)

    elif provider == "Anthropic":
        api_key = st.session_state.get("anthropic_api_key")
        if not api_key:
            return "Error: Anthropic API key not provided"
        return call_anthropic_api(prompt, api_key)

    elif provider == "Groq":
        api_key = st.session_state.get("groq_api_key")
        if not api_key:
            return "Error: Groq API key not provided"
        return call_groq_api(prompt, api_key)

    elif provider == "Ollama (Local)":
        server_url = st.session_state.get("ollama_url", "http://localhost:11434")
        return call_ollama_api(prompt, server_url)

    else:
        return "Error: Unknown provider"


def show_test_prompts():
    """Display prompt testing interface"""
    st.markdown('<h2 class="section-header">🧪 Test Your Prompts</h2>', unsafe_allow_html=True)

    st.write("Test your prompts with real LLM APIs to see how they perform and iterate for better results.")

    # Check if API is configured
    provider = st.session_state.api_provider
    api_configured = False

    if provider == "OpenAI" and st.session_state.get("openai_api_key"):
        api_configured = True
    elif provider == "Anthropic" and st.session_state.get("anthropic_api_key"):
        api_configured = True
    elif provider == "Groq" and st.session_state.get("groq_api_key"):
        api_configured = True
    elif provider == "Ollama (Local)":
        api_configured = True  # Assume local server is available

    if not api_configured and provider != "Ollama (Local)":
        st.warning(f"⚠️ Please configure your {provider} API key in the sidebar to test prompts.")
        return

    # Model selection
    col1, col2 = st.columns([1, 1])
    with col1:
        if provider == "OpenAI":
            model = st.selectbox("Model:", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"])
        elif provider == "Anthropic":
            model = st.selectbox("Model:",
                                 ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"])
        elif provider == "Groq":
            model = st.selectbox("Model:", ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"])
        elif provider == "Ollama (Local)":
            model = st.text_input("Model:", value="llama2", help="Enter the name of your local Ollama model")

    with col2:
        st.info(f"Using: {provider}")

    # Prompt input
    st.markdown("### 📝 Enter Your Prompt")

    # Check if there's a prompt loaded for testing
    if 'prompt_to_test' in st.session_state:
        st.info(f"📋 Loaded prompt from: {st.session_state.get('test_prompt_source', 'Unknown')}")
        prompt_text = st.text_area(
            "Prompt to test:",
            value=st.session_state.prompt_to_test,
            height=150,
            help="Edit the prompt if needed before testing"
        )
        # Clear the loaded prompt after displaying
        if st.button("🗑️ Clear Loaded Prompt"):
            if 'prompt_to_test' in st.session_state:
                del st.session_state.prompt_to_test
            if 'test_prompt_source' in st.session_state:
                del st.session_state.test_prompt_source
            st.rerun()
    else:
        prompt_text = st.text_area(
            "Prompt to test:",
            height=150,
            placeholder="Enter your prompt here or load one from the Subject-Specific Prompts or Prompt Builder sections..."
        )

    # Test button and results
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🚀 Test Prompt", disabled=not prompt_text.strip()):
            if prompt_text.strip():
                with st.spinner(f"Testing with {provider}..."):
                    start_time = time.time()
                    response = test_prompt_with_llm(prompt_text, provider)
                    end_time = time.time()

                    # Store test result
                    test_result = {
                        'prompt': prompt_text,
                        'response': response,
                        'provider': provider,
                        'model': model,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'response_time': round(end_time - start_time, 2)
                    }
                    st.session_state.test_results.append(test_result)

    # Display current test results
    if st.session_state.test_results:
        st.markdown("### 📊 Test Results")

        # Show most recent result first
        latest_result = st.session_state.test_results[-1]

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**Provider:** {latest_result['provider']} ({latest_result['model']})")
        with col2:
            st.write(f"**Response Time:** {latest_result['response_time']}s")
        with col3:
            st.write(f"**Time:** {latest_result['timestamp']}")

        st.markdown("**Prompt:**")
        st.markdown(f"""
        <div class="prompt-example">
        {latest_result['prompt']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Response:**")
        if latest_result['response'].startswith("Error:"):
            st.error(latest_result['response'])
        else:
            st.markdown(f"""
            <div class="tip-box">
            {latest_result['response']}
            </div>
            """, unsafe_allow_html=True)

        # Rating and feedback
        st.markdown("### 📈 Rate This Response")
        col1, col2 = st.columns([1, 2])
        with col1:
            rating = st.select_slider(
                "How helpful was this response?",
                options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
                key=f"rating_{len(st.session_state.test_results)}"
            )
        with col2:
            feedback = st.text_area(
                "What could be improved?",
                placeholder="Optional feedback about the response quality...",
                key=f"feedback_{len(st.session_state.test_results)}"
            )

        if st.button("💾 Save Feedback"):
            st.session_state.test_results[-1]['rating'] = rating
            st.session_state.test_results[-1]['feedback'] = feedback
            st.success("Feedback saved!")

    # Test history
    if len(st.session_state.test_results) > 1:
        st.markdown("### 📚 Previous Test Results")

        for i, result in enumerate(reversed(st.session_state.test_results[:-1])):
            with st.expander(
                    f"Test {len(st.session_state.test_results) - i - 1}: {result['provider']} - {result['timestamp']}"):
                st.write(f"**Model:** {result['model']}")
                st.write(f"**Response Time:** {result['response_time']}s")
                if 'rating' in result:
                    st.write(f"**Rating:** {result['rating']}")

                st.markdown("**Prompt:**")
                st.code(result['prompt'], language="text")

                st.markdown("**Response:**")
                if result['response'].startswith("Error:"):
                    st.error(result['response'])
                else:
                    st.write(result['response'])

                if 'feedback' in result and result['feedback']:
                    st.markdown("**Feedback:**")
                    st.write(result['feedback'])

        # Clear history button
        if st.button("🗑️ Clear Test History"):
            st.session_state.test_results = []
            st.success("Test history cleared!")
            st.rerun()

    # Tips for testing
    st.markdown("### 💡 Testing Tips")
    st.markdown("""
    <div class="tip-box">
    <strong>🎯 Effective Testing Strategies:</strong><br>
    • Test the same prompt with different models to compare responses<br>
    • Try variations of your prompt to see which works best<br>
    • Rate responses to track what prompting techniques work for you<br>
    • Use the feedback to refine your prompts iteratively<br>
    • Pay attention to response time vs. quality trade-offs
    </div>
    """, unsafe_allow_html=True)


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


def show_my_prompts():
    """Display saved prompts and favorites"""
    st.markdown('<h2 class="section-header">📝 My Saved Prompts</h2>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💾 My Custom Prompts", "⭐ Favorites"])

    with tab1:
        if st.session_state.user_prompts:
            for i, prompt_data in enumerate(st.session_state.user_prompts):
                with st.expander(f"{prompt_data['subject']} - {prompt_data['topic']} ({prompt_data['date']})"):
                    st.write(prompt_data['prompt'])
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        if st.button(f"🗑️ Delete", key=f"delete_custom_{i}"):
                            st.session_state.user_prompts.pop(i)
                            st.rerun()
                    with col2:
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
                    col1, col2, col3 = st.columns([1, 1, 2])
                    with col1:
                        if st.button(f"🗑️ Remove", key=f"delete_fav_{i}"):
                            st.session_state.favorites.pop(i)
                            st.rerun()
                    with col2:
                        if st.button(f"🧪 Test", key=f"test_fav_{i}"):
                            st.session_state.prompt_to_test = fav['prompt']
                            st.session_state.test_prompt_source = f"Favorites - {fav['category']}"
                            st.success("Prompt loaded for testing! Go to Test Prompts page.")
        else:
            st.info("No favorites saved yet. Browse the subject-specific prompts to add some!")


if __name__ == "__main__":
    main()