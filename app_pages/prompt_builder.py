import streamlit as st
from datetime import datetime
from utils.prompt_utils import build_advanced_prompt


def show_prompt_builder():
    """Advanced prompt builder tool with educational focus"""
    st.markdown('<h2 class="section-header">🔧 Advanced Prompt Builder</h2>', unsafe_allow_html=True)

    st.write("Create powerful, educational prompts that get better AI responses and enhance your learning!")


    with st.form("advanced_prompt_builder"):
        # Educational Context Section
        st.markdown("### 🎓 Educational Context")
        col1, col2 = st.columns(2)

        with col1:
            grade_level = st.selectbox(
                "Your Grade Level:",
                ["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/University",
                 "Graduate School"],
                help="This helps AI adjust language and examples to your level"
            )

            subject_area = st.selectbox(
                "Subject Area:",
                ["Mathematics", "Science (Biology/Chemistry/Physics)", "English/Literature", "History/Social Studies",
                 "Study Skills & Test Prep", "Other"],
                help="Choose the main subject for your prompt"
            )

        with col2:
            learning_goal = st.selectbox(
                "What's your main learning goal?",
                [
                    "Understand a concept I'm confused about",
                    "Get help solving problems step-by-step",
                    "Prepare for a test or assignment",
                    "Connect ideas to real-world applications",
                    "Improve my study techniques",
                    "Analyze and interpret information",
                    "Get feedback on my work"
                ],
                help="This determines the type of educational support you need"
            )

            current_understanding = st.selectbox(
                "Your current understanding level:",
                [
                    "Complete beginner - never studied this before",
                    "Basic understanding - know a little but confused",
                    "Moderate understanding - get the basics but struggle with applications",
                    "Good understanding - just need help with specific parts",
                    "Advanced - want to deepen or extend my knowledge"
                ],
                help="Helps AI know where to start and how much detail to provide"
            )

        # AI Role & Approach Section
        st.markdown("### 👨‍🏫 AI Teaching Role & Approach")
        col1, col2 = st.columns(2)

        with col1:
            ai_role = st.selectbox(
                "How should the AI help you?",
                [
                    "Patient tutor - guide me step by step",
                    "Socratic teacher - ask me questions to help me discover answers",
                    "Study coach - help me develop learning strategies",
                    "Writing mentor - provide feedback and suggestions",
                    "Research assistant - help me find and organize information",
                    "Practice partner - quiz me and give feedback"
                ],
                help="Different roles provide different types of educational support"
            )

            interaction_style = st.selectbox(
                "Preferred interaction style:",
                [
                    "Guide me to discover answers myself",
                    "Explain clearly then let me practice",
                    "Show examples then help me try similar problems",
                    "Break complex topics into simple steps",
                    "Connect new ideas to what I already know",
                    "Help me see real-world applications"
                ],
                help="How you learn best determines how AI should teach you"
            )

        with col2:
            feedback_preference = st.multiselect(
                "What kind of feedback do you want?",
                [
                    "Check my understanding along the way",
                    "Point out common mistakes to avoid",
                    "Suggest study strategies that match my learning style",
                    "Provide memory tricks and mnemonics",
                    "Give me practice problems at different difficulty levels",
                    "Help me make connections between topics"
                ],
                help="Select all types of feedback that would help your learning"
            )

        # Specific Learning Request
        st.markdown("### 📝 Your Specific Learning Request")

        topic_or_question = st.text_area(
            "What specific topic, question, or problem do you need help with?",
            height=100,
            placeholder="Be as specific as possible. For example: 'solving quadratic equations with the quadratic formula' rather than just 'algebra'",
            help="The more specific you are, the better help you'll get"
        )

        background_context = st.text_area(
            "Additional context (what you already know, what you've tried, what's confusing you):",
            height=80,
            placeholder="Example: 'I understand regular equations like 2x + 5 = 11, but when there's an x² term I get lost...'",
            help="This helps AI build on your existing knowledge and address your specific confusion"
        )

        # Output Preferences
        st.markdown("### 📊 How You Want the Response Structured")
        col1, col2 = st.columns(2)

        with col1:
            response_format = st.multiselect(
                "Response format preferences:",
                [
                    "Step-by-step explanations",
                    "Real-world examples and analogies",
                    "Practice problems with solutions",
                    "Visual descriptions or diagrams",
                    "Memory aids and mnemonics",
                    "Summary of key points",
                    "Questions to test my understanding"
                ],
                default=["Step-by-step explanations", "Real-world examples and analogies"],
                help="Choose formats that help you learn best"
            )

        with col2:
            detail_level = st.select_slider(
                "Level of detail:",
                options=["Brief overview", "Moderate detail", "Comprehensive explanation", "In-depth analysis"],
                value="Moderate detail",
                help="How much detail do you need to understand the topic?"
            )

            followup_support = st.checkbox(
                "Ask me follow-up questions to check my understanding",
                value=True,
                help="AI will ask questions to make sure you really understand"
            )

        # Advanced Options
        with st.expander("🔬 Advanced Options"):
            st.markdown("**Learning Style Preferences:**")
            learning_styles = st.multiselect(
                "How do you learn best?",
                [
                    "Visual (diagrams, charts, visual examples)",
                    "Auditory (explanations I can 'hear' in my head)",
                    "Kinesthetic (hands-on examples, real-world applications)",
                    "Reading/Writing (text-based explanations, note-taking)",
                    "Social (discussion-style explanations)",
                    "Logical (step-by-step reasoning, cause-and-effect)"
                ],
                help="AI can adapt explanations to match your learning preferences"
            )

            st.markdown("**Special Considerations:**")
            col1, col2 = st.columns(2)
            with col1:
                common_mistakes = st.checkbox("Warn me about common mistakes students make")
                exam_focus = st.checkbox("Focus on what's likely to be on tests")
            with col2:
                career_connections = st.checkbox("Show how this connects to careers/real life")
                prerequisite_check = st.checkbox("Check if I'm missing prerequisite knowledge")

        # Generate Prompt Button
        submitted = st.form_submit_button("🚀 Generate Educational Prompt", type="primary")

    # Handle form submission
    if submitted:
        if topic_or_question.strip():
            # Collect all form data
            prompt_data = {
                'grade_level': grade_level,
                'subject_area': subject_area,
                'learning_goal': learning_goal,
                'current_understanding': current_understanding,
                'ai_role': ai_role,
                'interaction_style': interaction_style,
                'feedback_preference': feedback_preference,
                'topic_or_question': topic_or_question,
                'background_context': background_context,
                'response_format': response_format,
                'detail_level': detail_level,
                'followup_support': followup_support,
                'learning_styles': learning_styles if 'learning_styles' in locals() else [],
                'common_mistakes': common_mistakes if 'common_mistakes' in locals() else False,
                'exam_focus': exam_focus if 'exam_focus' in locals() else False,
                'career_connections': career_connections if 'career_connections' in locals() else False,
                'prerequisite_check': prerequisite_check if 'prerequisite_check' in locals() else False
            }

            # Generate the advanced prompt
            generated_prompt = build_advanced_prompt(prompt_data)

            # Store in session state
            st.session_state.current_generated_prompt = {
                'prompt': generated_prompt,
                'subject': subject_area,
                'topic': topic_or_question[:50] + "..." if len(topic_or_question) > 50 else topic_or_question,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'prompt_data': prompt_data
            }

            # Display the generated prompt
            st.markdown("### 🎉 Your Educational Prompt")
            st.markdown("**Ready to copy and use with any AI system:**")

            st.markdown(f"""
            <div class="prompt-example">
            {generated_prompt}
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("💾 Save This Prompt"):
                    st.session_state.user_prompts.append(st.session_state.current_generated_prompt)
                    st.success("Prompt saved!")
            with col2:
                if st.button("🧪 Test This Prompt"):
                    st.session_state.prompt_to_test = generated_prompt
                    st.session_state.test_prompt_source = f"Advanced Builder - {topic_or_question[:30]}..."
                    st.success("Prompt loaded for testing! Go to Test Prompts page.")

            # Explanation of prompt components
            with st.expander("🔍 Understanding Your Generated Prompt"):
                st.markdown("**Your prompt includes these educational elements:**")

                components = []
                if prompt_data['ai_role']:
                    components.append(f"**Role Assignment**: AI acts as {prompt_data['ai_role'].lower()}")
                if prompt_data['grade_level']:
                    components.append(f"**Learning Level**: Tailored for {prompt_data['grade_level'].lower()}")
                if prompt_data['current_understanding']:
                    components.append(
                        f"**Understanding Context**: Acknowledges you have {prompt_data['current_understanding'].lower()}")
                if prompt_data['interaction_style']:
                    components.append(f"**Teaching Style**: Uses {prompt_data['interaction_style'].lower()} approach")
                if prompt_data['response_format']:
                    components.append(
                        f"**Format Preferences**: Includes {', '.join(prompt_data['response_format'][:2]).lower()}")

                for component in components:
                    st.write(f"• {component}")

                st.markdown(
                    "**💡 Pro Tip**: This prompt structure works with any AI system - ChatGPT, Claude, Gemini, etc.!")

        else:
            st.warning("Please enter a specific topic or question to generate your prompt.")

    # Display previously generated prompt if exists
    elif 'current_generated_prompt' in st.session_state:
        st.markdown("### 🎉 Your Educational Prompt")
        st.markdown("**Ready to copy and use:**")

        st.markdown(f"""
        <div class="prompt-example">
        {st.session_state.current_generated_prompt['prompt']}
        </div>
        """, unsafe_allow_html=True)

        # Action buttons for existing prompt
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 Save This Prompt"):
                if st.session_state.current_generated_prompt not in st.session_state.user_prompts:
                    st.session_state.user_prompts.append(st.session_state.current_generated_prompt)
                    st.success("Prompt saved!")
                else:
                    st.info("This prompt is already saved!")
