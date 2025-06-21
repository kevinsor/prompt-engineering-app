import streamlit as st
from datetime import datetime
from utils.prompt_utils import build_advanced_prompt


def show_prompt_builder():
    """Advanced prompt builder tool with educational focus"""
    st.markdown('<h2 class="section-header">🔧 Advanced Prompt Builder</h2>', unsafe_allow_html=True)

    st.write("Create powerful, educational prompts that get better AI responses and enhance your learning!")
    
    # Progress indicator
    progress_placeholder = st.empty()
    progress_placeholder.progress(0, "Getting started...")


    with st.form("advanced_prompt_builder"):
        # Update progress
        progress_placeholder.progress(0.1, "Setting up form...")
        
        # Educational Context Section
        st.markdown("### 🎓 Educational Context")
        st.markdown("*Tell us about your learning situation*")
        col1, col2 = st.columns(2)

        with col1:
            grade_level = st.selectbox(
                "Your Grade Level:",
                ["Elementary (K-5)", "Middle School (6-8)", "High School (9-12)", "College/University",
                 "Graduate School"],
                index=2,  # Default to High School
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
                index=1,  # Default to Basic understanding
                help="Helps AI know where to start and how much detail to provide"
            )

        # AI Role & Approach Section
        st.markdown("### 👨‍🏫 AI Teaching Role & Approach")
        st.markdown("*Choose how you want the AI to help you learn*")
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
                index=0,  # Default to Patient tutor
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
            # Smart defaults for feedback based on learning goal
            default_feedback = ["Check my understanding along the way"]
            if learning_goal == "Prepare for a test or assignment":
                default_feedback.extend(["Point out common mistakes to avoid", "Give me practice problems at different difficulty levels"])
            elif learning_goal == "Understand a concept I'm confused about":
                default_feedback.append("Help me make connections between topics")
            
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
                default=default_feedback,
                help="Select all types of feedback that would help your learning (smart defaults applied)"
            )

        # Specific Learning Request
        st.markdown("### 📝 Your Specific Learning Request")
        st.markdown("*The most important part - be specific!*")

        topic_or_question = st.text_area(
            "What specific topic, question, or problem do you need help with? *",
            height=100,
            placeholder="Be as specific as possible. For example: 'solving quadratic equations with the quadratic formula' rather than just 'algebra'",
            help="The more specific you are, the better help you'll get"
        )
        
        # Character counter and validation hints
        if topic_or_question:
            char_count = len(topic_or_question)
            if char_count < 10:
                st.warning("⚠️ Consider adding more detail for better results (current: {} characters)".format(char_count))
            elif char_count > 20:
                st.success("✅ Good detail level (current: {} characters)".format(char_count))

        background_context = st.text_area(
            "Additional context (what you already know, what you've tried, what's confusing you):",
            height=80,
            placeholder="Example: 'I understand regular equations like 2x + 5 = 11, but when there's an x² term I get lost...'",
            help="This helps AI build on your existing knowledge and address your specific confusion"
        )

        # Output Preferences
        st.markdown("### 📊 How You Want the Response Structured")
        st.markdown("*Control the format and detail level*")
        col1, col2 = st.columns(2)

        with col1:
            # Smart defaults based on grade level and subject
            default_formats = ["Step-by-step explanations", "Real-world examples and analogies"]
            if grade_level in ["Elementary (K-5)", "Middle School (6-8)"]:
                default_formats.append("Visual descriptions or diagrams")
            if subject_area == "Mathematics":
                if "Practice problems with solutions" not in default_formats:
                    default_formats.append("Practice problems with solutions")
            
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
                default=default_formats,
                help="Choose formats that help you learn best (smart defaults applied based on your selections)"
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
        with st.expander("🔬 Advanced Options (Optional)"):
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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🚀 Generate Educational Prompt", type="primary", use_container_width=True)

    # Handle form submission
    if submitted:
        # Update progress
        progress_placeholder.progress(0.3, "Validating form...")
        
        # Enhanced validation
        errors = []
        if not topic_or_question.strip():
            errors.append("Please enter a specific topic or question")
        elif len(topic_or_question.strip()) < 5:
            errors.append("Please provide more detail about your topic (at least 5 characters)")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            st.info("💡 Tip: The more specific you are, the better your AI tutor can help you!")
        else:
            progress_placeholder.progress(0.5, "Building your personalized prompt...")
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
            progress_placeholder.progress(0.7, "Generating prompt...")
            generated_prompt = build_advanced_prompt(prompt_data)
            progress_placeholder.progress(1.0, "Complete! ✨")

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
            
            # Enhanced prompt display with copy button
            col_prompt, col_copy = st.columns([4, 1])
            with col_prompt:
                st.markdown(f"""
                <div class="prompt-example">
                {generated_prompt}
                </div>
                """, unsafe_allow_html=True)
            
            with col_copy:
                st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
                if st.button("📋 Copy", help="Copy prompt to clipboard", use_container_width=True):
                    st.code(generated_prompt, language=None)
                    st.success("✅ Prompt copied! Paste it into your AI chat.")

            # Enhanced action buttons
            st.markdown("---")
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if st.button("💾 Save Prompt", use_container_width=True):
                    if st.session_state.current_generated_prompt not in st.session_state.get('user_prompts', []):
                        if 'user_prompts' not in st.session_state:
                            st.session_state.user_prompts = []
                        st.session_state.user_prompts.append(st.session_state.current_generated_prompt)
                        st.success("✅ Prompt saved!")
                    else:
                        st.info("💾 Already saved!")
            
            with col2:
                if st.button("🧪 Test Prompt", use_container_width=True):
                    st.session_state.prompt_to_test = generated_prompt
                    st.session_state.test_prompt_source = f"Advanced Builder - {topic_or_question[:30]}..."
                    st.success("✅ Ready to test! Go to Test Prompts page.")
            
            with col3:
                if st.button("✏️ Edit Prompt", use_container_width=True, help="Customize the generated prompt"):
                    st.session_state.show_prompt_editor = True
            
            with col4:
                # Export options
                prompt_text = f"""# Educational Prompt Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Topic:** {topic_or_question}
**Subject:** {subject_area}
**Grade Level:** {grade_level}

## Generated Prompt:
{generated_prompt}

---
Generated using Advanced Prompt Builder"""
                
                st.download_button(
                    "📎 Export",
                    prompt_text,
                    file_name=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    help="Download as text file"
                )
            
            # Prompt Editor
            if st.session_state.get('show_prompt_editor', False):
                st.markdown("---")
                st.markdown("### ✏️ Edit Your Prompt")
                
                edited_prompt = st.text_area(
                    "Customize your prompt:",
                    value=generated_prompt,
                    height=200,
                    help="Make any changes you want to the generated prompt"
                )
                
                col_save, col_cancel = st.columns([1, 1])
                with col_save:
                    if st.button("✅ Save Changes", type="primary", use_container_width=True):
                        # Update the generated prompt
                        st.session_state.current_generated_prompt['prompt'] = edited_prompt
                        st.session_state.show_prompt_editor = False
                        st.success("Prompt updated!")
                        st.rerun()
                
                with col_cancel:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.show_prompt_editor = False
                        st.rerun()

            # Quick Preview Section
            with st.expander("🔎 Quick Preview - How This Prompt Works"):
                st.markdown("**This is what your AI assistant will understand:**")
                preview_parts = []
                
                if prompt_data['ai_role']:
                    preview_parts.append(f"• **Role**: Acts as your {prompt_data['ai_role'].split(' - ')[0].lower()}")
                if prompt_data['grade_level']:
                    preview_parts.append(f"• **Level**: Explains things for {prompt_data['grade_level'].lower()} level")
                if prompt_data['current_understanding']:
                    understanding = prompt_data['current_understanding'].split(' - ')[0]
                    preview_parts.append(f"• **Starting Point**: Knows you have {understanding.lower()}")
                if prompt_data['interaction_style']:
                    style = prompt_data['interaction_style'].lower()
                    preview_parts.append(f"• **Teaching Style**: Will {style}")
                
                for part in preview_parts[:4]:  # Show top 4 most important parts
                    st.markdown(part)
                
                if len(preview_parts) > 4:
                    st.markdown(f"*...and {len(preview_parts) - 4} more customizations*")
            
            # Detailed explanation
            with st.expander("🔍 Full Prompt Analysis"):
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

            # Clear progress indicator after brief delay
            import time
            time.sleep(0.5)
            progress_placeholder.empty()

    # Display previously generated prompt if exists
    elif 'current_generated_prompt' in st.session_state:
        st.markdown("### 🎉 Your Educational Prompt")
        st.markdown("**Ready to copy and use:**")

        st.markdown(f"""
        <div class="prompt-example">
        {st.session_state.current_generated_prompt['prompt']}
        </div>
        """, unsafe_allow_html=True)

        # Enhanced action buttons for existing prompt
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.button("💾 Save Prompt", key="save_existing", use_container_width=True):
                if 'user_prompts' not in st.session_state:
                    st.session_state.user_prompts = []
                if st.session_state.current_generated_prompt not in st.session_state.user_prompts:
                    st.session_state.user_prompts.append(st.session_state.current_generated_prompt)
                    st.success("✅ Prompt saved!")
                else:
                    st.info("💾 Already saved!")
        
        with col2:
            if st.button("🧪 Test Prompt", key="test_existing", use_container_width=True):
                st.session_state.prompt_to_test = st.session_state.current_generated_prompt['prompt']
                st.session_state.test_prompt_source = f"Saved Prompt - {st.session_state.current_generated_prompt['topic']}"
                st.success("✅ Ready to test!")
        
        with col3:
            if st.button("✏️ Edit", key="edit_existing", use_container_width=True):
                st.session_state.show_existing_editor = True
        
        # Editor for existing prompt
        if st.session_state.get('show_existing_editor', False):
            st.markdown("---")
            st.markdown("### ✏️ Edit Saved Prompt")
            
            edited_existing = st.text_area(
                "Customize your saved prompt:",
                value=st.session_state.current_generated_prompt['prompt'],
                height=200,
                key="edit_existing_text"
            )
            
            col_save, col_cancel = st.columns([1, 1])
            with col_save:
                if st.button("✅ Save Changes", key="save_existing_changes", type="primary", use_container_width=True):
                    st.session_state.current_generated_prompt['prompt'] = edited_existing
                    st.session_state.show_existing_editor = False
                    st.success("Prompt updated!")
                    st.rerun()
            
            with col_cancel:
                if st.button("❌ Cancel", key="cancel_existing_edit", use_container_width=True):
                    st.session_state.show_existing_editor = False
                    st.rerun()
        
        with col4:
            prompt_text = f"""# Educational Prompt

**Topic:** {st.session_state.current_generated_prompt['topic']}
**Subject:** {st.session_state.current_generated_prompt['subject']}
**Date:** {st.session_state.current_generated_prompt['date']}

## Generated Prompt:
{st.session_state.current_generated_prompt['prompt']}

---
Generated using Advanced Prompt Builder"""
            
            st.download_button(
                "📎 Export",
                prompt_text,
                file_name=f"prompt_{st.session_state.current_generated_prompt['date'].replace(' ', '_').replace(':', '')}.txt",
                mime="text/plain",
                key="export_existing",
                use_container_width=True
            )
