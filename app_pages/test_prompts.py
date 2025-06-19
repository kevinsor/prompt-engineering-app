import streamlit as st
import time
from datetime import datetime
from services.mock_ai_service import MockAIService

# Initialize services
mock_ai = MockAIService()


def show_test_prompts():
    """Display prompt testing interface focused on educational simulation"""
    st.markdown('<h2 class="section-header">🧪 Test Your Prompts</h2>', unsafe_allow_html=True)

    st.write(
        "Practice and refine your prompts with our educational AI simulator. Get instant feedback on prompt quality and see how well your prompts work!")

    # Educational notice
    st.info(
        "🎓 **Educational Focus**: This simulator helps you learn prompt engineering techniques and see how different prompt styles affect AI responses. Perfect for practicing before using real AI systems!")

    # Testing mode selection
    col1, col2 = st.columns([1, 1])
    with col1:
        test_mode = st.selectbox(
            "Choose testing mode:",
            [
                "📚 Full Educational Simulation",
                "🔧 Prompt Quality Analysis Only",
                "🎯 Quick Prompt Check"
            ],
            help="Full Simulation: Complete AI response with quality analysis\nQuality Analysis: Detailed prompt improvement feedback\nQuick Check: Fast quality score and tips"
        )

    with col2:
        subject_hint = st.selectbox(
            "Subject (optional):",
            ["Auto-detect", "Mathematics", "Science", "English/Literature", "History", "Study Skills"]
        )

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
            placeholder="Enter your prompt here or load one from other sections...\n\nExample: 'Act as my math tutor. I'm a 10th grader who understands basic algebra but struggles with quadratic equations. Please guide me step-by-step through solving x² + 5x + 6 = 0, checking my understanding at each step.'"
        )

    # Quick tips based on current prompt
    if prompt_text.strip():
        quick_analysis = mock_ai.analyze_prompt_quality(prompt_text)
        if quick_analysis['overall_score'] < 6:
            st.warning(
                "💡 **Quick Tip**: Your prompt could be improved! Try adding your grade level, what you already know, and asking AI to take a teaching role.")
        elif quick_analysis['overall_score'] >= 8:
            st.success("✨ **Great start!** This looks like a well-structured educational prompt.")

    # Test button and results
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🚀 Test Prompt", disabled=not prompt_text.strip(), type="primary"):
            if prompt_text.strip():
                subject_for_analysis = None if subject_hint == "Auto-detect" else subject_hint

                with st.spinner("Analyzing your prompt and generating educational response..."):
                    start_time = time.time()

                    # Initialize variables
                    response = None
                    analysis = None

                    if test_mode == "🔧 Prompt Quality Analysis Only":
                        # Just analyze the prompt quality
                        analysis = mock_ai.analyze_prompt_quality(prompt_text)
                        response = None
                    elif test_mode == "🎯 Quick Prompt Check":
                        # Quick analysis with basic feedback
                        analysis = mock_ai.analyze_prompt_quality(prompt_text)
                        response = f"Quick Assessment: Your prompt scored {analysis['overall_score']}/10. " + (
                            "This is excellent for educational use!" if analysis['overall_score'] >= 8
                            else "This is good but could be improved." if analysis['overall_score'] >= 6
                            else "This needs improvement for better AI responses."
                        )
                    else:
                        # Full simulation with response and analysis
                        response, analysis = mock_ai.generate_mock_response(prompt_text, subject_for_analysis)

                    end_time = time.time()

                    # Store test result
                    test_result = {
                        'prompt': prompt_text,
                        'response': response,
                        'analysis': analysis,
                        'provider': 'Educational Simulator',
                        'model': test_mode,
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
            st.write(f"**Mode:** {latest_result['model']}")
        with col2:
            st.write(f"**Response Time:** {latest_result['response_time']}s")
        with col3:
            st.write(f"**Time:** {latest_result['timestamp']}")

        # Display prompt quality analysis
        if 'analysis' in latest_result and latest_result['analysis']:
            analysis = latest_result['analysis']

            st.markdown("### 📈 Prompt Quality Analysis")

            # Overall score with color coding
            col1, col2 = st.columns([1, 2])
            with col1:
                score_color = "🟢" if analysis['overall_score'] >= 8 else "🟡" if analysis[
                                                                                    'overall_score'] >= 6 else "🟠" if \
                analysis['overall_score'] >= 4 else "🔴"
                st.metric("Overall Score", f"{score_color} {analysis['overall_score']}/10")

            with col2:
                quality_descriptions = {
                    "excellent": "🌟 Excellent! This prompt should get great AI responses.",
                    "good": "👍 Good prompt! Minor improvements could make it even better.",
                    "fair": "⚡ Fair prompt. Some key improvements would help significantly.",
                    "needs_improvement": "🔧 Needs work. Focus on the suggestions below for better results."
                }
                st.write(quality_descriptions.get(analysis['quality'], ""))

            # Detailed scores in a more visual way
            st.markdown("**Detailed Breakdown:**")

            score_data = analysis['scores']
            col1, col2, col3, col4 = st.columns(4)

            def score_emoji(score):
                if score >= 8:
                    return "🟢"
                elif score >= 6:
                    return "🟡"
                elif score >= 4:
                    return "🟠"
                else:
                    return "🔴"

            with col1:
                st.metric("Specificity", f"{score_emoji(score_data['specificity'])} {score_data['specificity']}/10")
            with col2:
                st.metric("Context", f"{score_emoji(score_data['context'])} {score_data['context']}/10")
            with col3:
                st.metric("Clarity", f"{score_emoji(score_data['clarity'])} {score_data['clarity']}/10")
            with col4:
                st.metric("Educational Value",
                          f"{score_emoji(score_data['educational_value'])} {score_data['educational_value']}/10")

            # Improvement suggestions
            if analysis.get('suggestions'):
                st.markdown("**💡 Suggestions for Improvement:**")
                for i, suggestion in enumerate(analysis['suggestions'][:4], 1):
                    st.write(f"{i}. {suggestion}")

                # Quick improvement template
                if analysis['overall_score'] < 7:
                    with st.expander("🚀 Quick Improvement Template"):
                        st.markdown("""
                        **Try this structure for better prompts:**

                        ```
                        Act as my [ROLE: tutor/teacher/coach] for [SUBJECT].
                        I'm a [GRADE LEVEL] student who [CURRENT UNDERSTANDING].
                        Please [SPECIFIC REQUEST] by [HOW YOU WANT TO LEARN].
                        [ADDITIONAL PREFERENCES: examples, step-by-step, etc.]
                        ```

                        **Example:**
                        "Act as my patient math tutor. I'm a 9th grader who understands basic equations but gets confused with quadratic equations. Please guide me through solving x² + 5x + 6 = 0 step-by-step, checking my understanding at each step."
                        """)

        # Display AI response if available
        if latest_result['response']:
            st.markdown("### 🤖 AI Response Preview")
            st.markdown("**Your Prompt:**")
            st.markdown(f"""
            <div class="prompt-example">
            {latest_result['prompt']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Simulated AI Response:**")
            st.markdown(f"""
            <div class="tip-box">
            {latest_result['response']}
            </div>
            """, unsafe_allow_html=True)

        # Rating and feedback
        st.markdown("### 📈 Rate This Test")
        col1, col2 = st.columns([1, 2])
        with col1:
            rating = st.select_slider(
                "How helpful was this analysis?",
                options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
                key=f"rating_{len(st.session_state.test_results)}"
            )
        with col2:
            feedback = st.text_area(
                "What did you learn about prompt engineering?",
                placeholder="Reflect on what you learned about writing better prompts...",
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
                    f"Test {len(st.session_state.test_results) - i - 1}: Score {result['analysis']['overall_score']}/10 - {result['timestamp']}"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write(f"**Mode:** {result['model']}")
                    st.write(f"**Response Time:** {result['response_time']}s")
                    if 'rating' in result:
                        st.write(f"**Your Rating:** {result['rating']}")
                with col2:
                    if result['analysis']:
                        st.write(f"**Quality:** {result['analysis']['quality'].title()}")
                        st.write(
                            f"**Best Area:** {max(result['analysis']['scores'], key=result['analysis']['scores'].get).title()}")

                st.markdown("**Prompt:**")
                st.code(result['prompt'], language="text")

                if result['response']:
                    st.markdown("**Response Preview:**")
                    st.write(result['response'][:200] + "..." if len(result['response']) > 200 else result['response'])

                if 'feedback' in result and result['feedback']:
                    st.markdown("**Your Reflection:**")
                    st.write(result['feedback'])

        # Clear history button
        if st.button("🗑️ Clear Test History"):
            st.session_state.test_results = []
            st.success("Test history cleared!")
            st.rerun()

    # Educational guidance
    st.markdown("### 💡 Mastering Educational Prompts")

    tab1, tab2, tab3 = st.tabs(["🎯 Quality Indicators", "📚 Learning Strategies", "🔄 Improvement Process"])

    with tab1:
        st.markdown("""
        <div class="tip-box">
        <strong>What Makes Educational Prompts Excellent:</strong><br><br>

        <strong>🎭 Role Assignment (9-10 points):</strong><br>
        • "Act as my tutor/teacher/coach"<br>
        • Gives AI clear educational context<br><br>

        <strong>📍 Learning Context (8-10 points):</strong><br>
        • Your grade level and current understanding<br>
        • What you already know vs. what confuses you<br><br>

        <strong>🎯 Specific Request (8-10 points):</strong><br>
        • Exactly what you want to learn or accomplish<br>
        • Clear, focused learning objective<br><br>

        <strong>🤝 Interaction Style (7-10 points):</strong><br>
        • How you want AI to teach you<br>
        • Request for guidance vs. direct answers
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="prompt-example">
        <strong>Effective Learning Strategies with AI:</strong><br><br>

        <strong>🧠 For Understanding:</strong> "Explain X in simple terms, then give me an analogy"<br>
        <strong>🔍 For Problem Solving:</strong> "Guide me step-by-step, let me try each step"<br>
        <strong>📝 For Writing:</strong> "Act as my writing coach, give feedback on this draft"<br>
        <strong>🎯 For Test Prep:</strong> "Quiz me on X, then explain what I got wrong"<br>
        <strong>🔗 For Connections:</strong> "Help me see how X relates to Y"<br><br>

        <strong>💡 Pro Tip:</strong> Always ask AI to check your understanding rather than just giving you information!
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="warning-box">
        <strong>Your Prompt Improvement Process:</strong><br><br>

        <strong>1. Start Simple</strong> → Test your basic prompt<br>
        <strong>2. Analyze Results</strong> → Look at quality scores and suggestions<br>
        <strong>3. Add Context</strong> → Include grade level, current understanding<br>
        <strong>4. Specify Role</strong> → Ask AI to be your tutor/teacher/coach<br>
        <strong>5. Clarify Interaction</strong> → Say how you want to learn<br>
        <strong>6. Test Again</strong> → See improvement in quality scores<br><br>

        <strong>🎓 Goal:</strong> Consistently create prompts that score 8+/10 for excellent AI responses!
        </div>
        """, unsafe_allow_html=True)