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


def build_advanced_prompt(prompt_data):
    """Build an advanced educational prompt based on comprehensive user inputs"""

    prompt_parts = []

    # 1. Role Assignment - This is crucial for educational prompts
    role_mapping = {
        "Patient tutor - guide me step by step": "Act as my patient and supportive tutor",
        "Socratic teacher - ask me questions to help me discover answers": "Act as my Socratic teacher who guides learning through thoughtful questions",
        "Study coach - help me develop learning strategies": "Act as my study coach and learning strategist",
        "Writing mentor - provide feedback and suggestions": "Act as my writing mentor and editor",
        "Research assistant - help me find and organize information": "Act as my research assistant and information organizer",
        "Practice partner - quiz me and give feedback": "Act as my practice partner and learning assessor"
    }

    role_instruction = role_mapping.get(prompt_data.get('ai_role', ''), "Act as my educational assistant")
    prompt_parts.append(f"{role_instruction}.")

    # 2. Student Context - Critical for appropriate responses
    grade_context = {
        "Elementary (K-5)": "elementary school student",
        "Middle School (6-8)": "middle school student",
        "High School (9-12)": "high school student",
        "College/University": "college student",
        "Graduate School": "graduate student"
    }

    student_level = grade_context.get(prompt_data.get('grade_level', ''), "student")
    subject_area = prompt_data.get('subject_area', 'general studies')
    prompt_parts.append(f"I'm a {student_level} studying {subject_area.lower()}.")

    # 3. Current Understanding Level - Helps AI calibrate response
    understanding_context = {
        "Complete beginner - never studied this before": "I'm completely new to this topic and have never studied it before",
        "Basic understanding - know a little but confused": "I have basic understanding but I'm confused about key parts",
        "Moderate understanding - get the basics but struggle with applications": "I understand the basics but struggle with applying the concepts",
        "Good understanding - just need help with specific parts": "I have good overall understanding but need help with specific aspects",
        "Advanced - want to deepen or extend my knowledge": "I have advanced understanding and want to deepen my knowledge further"
    }

    current_understanding = prompt_data.get('current_understanding', '')
    if current_understanding in understanding_context:
        prompt_parts.append(understanding_context[current_understanding] + ".")

    # 4. Background Context - User's specific situation
    background_context = prompt_data.get('background_context', '').strip()
    if background_context:
        prompt_parts.append(f"Background: {background_context}")

    # 5. Specific Learning Request
    learning_goal_context = {
        "Understand a concept I'm confused about": "Please help me understand this concept by breaking it down clearly",
        "Get help solving problems step-by-step": "Please guide me through solving this step-by-step, letting me try each step",
        "Prepare for a test or assignment": "Please help me prepare for assessment by focusing on key concepts and likely questions",
        "Connect ideas to real-world applications": "Please help me see how this connects to real-world situations and applications",
        "Improve my study techniques": "Please help me develop better study strategies for this material",
        "Analyze and interpret information": "Please guide me through analyzing and interpreting this information",
        "Get feedback on my work": "Please review my work and provide constructive feedback for improvement"
    }

    learning_goal = prompt_data.get('learning_goal', '')
    goal_instruction = learning_goal_context.get(learning_goal, "Please help me with")
    topic_or_question = prompt_data.get('topic_or_question', 'this topic')
    prompt_parts.append(f"{goal_instruction}: {topic_or_question}")

    # 6. Interaction Style Preferences
    style_instructions = {
        "Guide me to discover answers myself": "Instead of giving me direct answers, guide me to discover the solutions through questions and hints",
        "Explain clearly then let me practice": "First explain the concept clearly, then give me practice opportunities to apply it",
        "Show examples then help me try similar problems": "Show me examples first, then help me work through similar problems on my own",
        "Break complex topics into simple steps": "Break this complex topic into simple, manageable steps I can follow",
        "Connect new ideas to what I already know": "Help me connect these new ideas to concepts I already understand",
        "Help me see real-world applications": "Show me concrete examples of how this applies to real-world situations"
    }

    interaction_style = prompt_data.get('interaction_style', '')
    if interaction_style in style_instructions:
        prompt_parts.append(style_instructions[interaction_style] + ".")

    # 7. Response Format Preferences
    response_format = prompt_data.get('response_format', [])
    if response_format:
        format_request = "Please structure your response to include: " + ", ".join(response_format[:3]).lower()
        prompt_parts.append(format_request + ".")

    # 8. Learning Style Adaptations
    learning_styles = prompt_data.get('learning_styles', [])
    if learning_styles:
        style_adaptations = {
            "Visual (diagrams, charts, visual examples)": "use visual descriptions and examples I can picture",
            "Auditory (explanations I can 'hear' in my head)": "explain things in a conversational way I can hear in my mind",
            "Kinesthetic (hands-on examples, real-world applications)": "include hands-on examples and real-world applications",
            "Reading/Writing (text-based explanations, note-taking)": "provide clear text explanations that are good for note-taking",
            "Social (discussion-style explanations)": "explain things in a discussion-style format",
            "Logical (step-by-step reasoning, cause-and-effect)": "use step-by-step logical reasoning and show cause-and-effect relationships"
        }

        matched_styles = [style_adaptations.get(style) for style in learning_styles if style in style_adaptations]
        if matched_styles:
            prompt_parts.append(f"Please adapt your teaching to {', '.join(matched_styles[:2])}.")

    # 9. Feedback and Assessment Preferences
    feedback_preference = prompt_data.get('feedback_preference', [])
    if feedback_preference:
        feedback_requests = []
        feedback_mapping = {
            "Check my understanding along the way": "check my understanding at key points",
            "Point out common mistakes to avoid": "warn me about common mistakes students make",
            "Suggest study strategies that match my learning style": "suggest study strategies that work for my learning style",
            "Provide memory tricks and mnemonics": "include memory tricks and mnemonics",
            "Give me practice problems at different difficulty levels": "provide practice problems at different difficulty levels",
            "Help me make connections between topics": "help me see connections to other topics I've learned"
        }

        for pref in feedback_preference[:3]:  # Limit to avoid overly long prompts
            if pref in feedback_mapping:
                feedback_requests.append(feedback_mapping[pref])

        if feedback_requests:
            prompt_parts.append(f"Please also {', and '.join(feedback_requests)}.")

    # 10. Follow-up and Engagement
    followup_support = prompt_data.get('followup_support', True)
    if followup_support:
        prompt_parts.append("Ask me follow-up questions to ensure I truly understand the material.")

    # 11. Special Considerations
    special_requests = []
    if prompt_data.get('common_mistakes', False):
        special_requests.append("highlight common mistakes students make with this topic")
    if prompt_data.get('exam_focus', False):
        special_requests.append("focus on aspects most likely to appear on tests")
    if prompt_data.get('career_connections', False):
        special_requests.append("explain how this connects to future careers")
    if prompt_data.get('prerequisite_check', False):
        special_requests.append("check if I have the prerequisite knowledge needed")

    if special_requests:
        prompt_parts.append(f"Additionally, please {', and '.join(special_requests)}.")

    # 12. Detail Level Instruction
    detail_instructions = {
        "Brief overview": "Keep your explanation concise and focused on the most important points",
        "Moderate detail": "Provide a moderately detailed explanation with key examples",
        "Comprehensive explanation": "Give a comprehensive explanation with multiple examples and detailed reasoning",
        "In-depth analysis": "Provide an in-depth analysis with extensive examples, connections, and implications"
    }

    detail_level = prompt_data.get('detail_level', '')
    if detail_level in detail_instructions:
        prompt_parts.append(detail_instructions[detail_level] + ".")

    # Combine all parts into a coherent prompt
    return " ".join(prompt_parts)