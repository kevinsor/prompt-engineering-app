"""Data constants for the prompt engineering app - Optimized for performance"""
import streamlit as st

@st.cache_data
def get_subject_prompts():
    """Cache the subject prompts dictionary for better performance"""
    return {
        "Mathematics": {
            "Concept Learning": "Act as my patient math tutor. I'm a [GRADE LEVEL] student learning [SPECIFIC CONCEPT]. First, explain this concept using simple language and real-world examples I can relate to. Then, show me one worked example step-by-step. Finally, give me a similar practice problem to try on my own. Check my understanding by asking me to explain back one key part of the concept.",
            "Problem Solving": "I'm working on this math problem: [YOUR PROBLEM]. I'm a [GRADE LEVEL] student. Please don't solve it for me - instead, guide me through it by: 1) Helping me identify what type of problem this is, 2) Asking me what information I have and what I need to find, 3) Suggesting the first step I should take, 4) Letting me try each step and giving feedback. If I get stuck, give me a hint rather than the answer.",
            "Error Analysis": "I solved this math problem but got the wrong answer: [SHOW YOUR WORK]. I'm a [GRADE LEVEL] student. Please: 1) Identify exactly where my thinking went wrong, 2) Explain why that step is incorrect, 3) Help me understand the correct reasoning for that step, 4) Guide me through fixing my work, 5) Give me a similar problem to check if I understand the correction.",
            "Real-World Applications": "I'm learning [MATH CONCEPT] in my [GRADE LEVEL] class, but I don't understand why it's useful. Please: 1) Give me 3 real-world examples of careers or situations where this math is actually used, 2) Show me a specific, concrete problem from one of these examples, 3) Walk me through how the math concept solves this real problem, 4) Help me think of a situation in my own life where I might use this math.",
            "Test Preparation": "I have a [GRADE LEVEL] math test coming up on [TOPICS]. I learn best through [LEARNING STYLE]. Please: 1) Help me create a study plan for the next [TIME PERIOD], 2) Generate practice problems that start easy and get harder, 3) Create memory aids or tricks for the concepts I find most difficult, 4) Quiz me on the material and give me immediate feedback on my explanations, not just my answers.",
            "Concept Connections": "I'm learning [MATH CONCEPT A] and [MATH CONCEPT B] in my [GRADE LEVEL] math class. I understand each concept separately, but I'm struggling to see how they connect. Please: 1) Explain the relationship between these concepts in simple terms, 2) Give me a real-world example that uses both concepts together, 3) Show me a problem that requires both concepts to solve, 4) Help me create a visual or mental map of how they fit together."
        },
        "Science": {
            "Concept Exploration": "Act as my science teacher. I'm a [GRADE LEVEL] student trying to understand [SCIENTIFIC CONCEPT]. Please: 1) Start by asking me what I already think I know about this topic, 2) Build on my existing knowledge to explain the concept, 3) Use an analogy that relates to something I experience daily, 4) Show me how this concept connects to at least 2 other science ideas I've learned, 5) Help me predict what would happen in a new situation using this concept.",
            "Scientific Method": "I need to design an experiment to investigate [RESEARCH QUESTION] for my [GRADE LEVEL] science class. Please guide me through the scientific method by: 1) Helping me refine my research question to be testable, 2) Asking me what I predict will happen and why, 3) Helping me identify variables (independent, dependent, control), 4) Suggesting practical ways to measure results, 5) Discussing what results would support or disprove my hypothesis.",
            "Lab Report Help": "I completed a lab experiment about [EXPERIMENT TOPIC] and need help organizing my lab report. I'm a [GRADE LEVEL] student. Please: 1) Help me write a clear purpose statement, 2) Guide me in organizing my observations and data, 3) Help me analyze what my results mean and why they happened, 4) Assist me in identifying possible sources of error, 5) Help me connect my results to the scientific concepts we're studying.",
            "Misconception Fixing": "I'm confused about [SCIENTIFIC CONCEPT] because I thought [YOUR MISCONCEPTION]. I'm a [GRADE LEVEL] student. Please: 1) Explain why my thinking makes sense and where it comes from, 2) Gently correct my misconception with clear evidence, 3) Give me a simple experiment or observation I can do to see the correct concept in action, 4) Help me understand why the correct explanation is better, 5) Give me a memory trick to remember the right concept.",
            "Current Events": "I read/heard about [CURRENT SCIENCE NEWS/EVENT] and want to understand the science behind it. I'm a [GRADE LEVEL] student. Please: 1) Explain the basic scientific principles involved in terms I can understand, 2) Help me identify what's new or surprising about this discovery/event, 3) Connect this to science concepts I've learned in class, 4) Help me evaluate: is this good science? How do we know? 5) Discuss why this matters for society or my daily life.",
            "Career Exploration": "I'm interested in [SCIENCE FIELD/CAREER] but don't really know what scientists in this field actually do. I'm a [GRADE LEVEL] student. Please: 1) Describe a typical day for someone in this career, 2) Explain what kind of problems they solve and how, 3) Tell me what education and skills I'd need, 4) Give me a hands-on activity or project I could do now to explore this field, 5) Help me identify science classes and experiences that would prepare me for this path."
        },
        "English/Literature": {
            "Text Analysis": "I'm analyzing [BOOK/POEM/STORY] for my [GRADE LEVEL] English class, focusing on [THEME/LITERARY DEVICE/CHARACTER]. Please be my literary analysis coach: 1) Ask me what I notice about [FOCUS AREA] when I first read it, 2) Help me find specific textual evidence that supports my observations, 3) Guide me to make connections between different parts of the text, 4) Help me articulate why the author made these choices and their effect on readers, 5) Challenge me to consider alternative interpretations.",
            "Essay Writing": "I need to write a [ESSAY TYPE] essay about [TOPIC] for my [GRADE LEVEL] English class. My thesis is: [YOUR THESIS]. Please be my writing coach: 1) Help me evaluate if my thesis is arguable and specific enough, 2) Guide me in organizing my main points logically, 3) Help me brainstorm strong evidence for each point, 4) Teach me how to write transitions that connect my ideas, 5) Review my introduction and conclusion to make them compelling.",
            "Creative Writing": "I'm working on a [CREATIVE WRITING PROJECT] for my [GRADE LEVEL] class. My idea so far: [YOUR IDEA]. Please help me develop this by: 1) Asking me questions that help me clarify my vision, 2) Helping me develop my characters/setting/conflict more deeply, 3) Suggesting techniques to make my writing more vivid and engaging, 4) Giving me specific writing exercises to improve weak areas, 5) Helping me understand how published authors handle similar challenges.",
            "Reading Comprehension": "I'm reading [TEXT] for my [GRADE LEVEL] class and I'm struggling to understand [SPECIFIC DIFFICULTY - plot, characters, themes, language, etc.]. Please help me by: 1) Breaking down the confusing parts into smaller pieces, 2) Providing context that helps me understand (historical, cultural, etc.), 3) Helping me use context clues and other strategies to figure out meaning, 4) Connecting this text to simpler examples or modern equivalents, 5) Giving me questions to ask myself as I continue reading.",
            "Discussion Prep": "We're having a class discussion about [TOPIC/TEXT] in my [GRADE LEVEL] English class. Please help me prepare by: 1) Helping me form my own opinion with solid reasoning, 2) Anticipating what different viewpoints my classmates might have, 3) Finding strong textual evidence to support my points, 4) Preparing thoughtful questions I can ask others, 5) Teaching me how to respectfully disagree and build on others' ideas during discussion.",
            "Grammar & Style": "I'm working on improving [SPECIFIC WRITING ISSUE - sentence variety, word choice, grammar, etc.] in my writing for [GRADE LEVEL] English. Please: 1) Explain this writing element in simple terms with clear examples, 2) Show me how good writers use this technique effectively, 3) Give me specific exercises to practice this skill, 4) Help me edit a sample of my writing to improve this area, 5) Teach me how to self-edit for this issue in future writing."
        },
        "History": {
            "Historical Thinking": "I'm studying [HISTORICAL TOPIC/PERIOD] in my [GRADE LEVEL] history class. Instead of just telling me facts, please develop my historical thinking by: 1) Asking me what I think I already know and where that knowledge comes from, 2) Helping me analyze primary sources from this period - what do they reveal and what are their limitations? 3) Guiding me to consider multiple perspectives on these events, 4) Helping me understand cause and effect relationships, 5) Connecting this historical period to current events or issues.",
            "Primary Sources": "I need to analyze this primary source: [DESCRIBE SOURCE] from [TIME PERIOD/EVENT] for my [GRADE LEVEL] history class. Please guide me through historical analysis: 1) Help me identify what type of source this is and who created it, 2) Guide me to understand the historical context surrounding this source, 3) Help me determine what we can learn from this source and what questions it raises, 4) Discuss the limitations and potential bias of this source, 5) Connect this source to broader historical patterns or themes.",
            "Building Arguments": "I need to argue [YOUR POSITION] about [HISTORICAL TOPIC] for my [GRADE LEVEL] history class. Please help me think like a historian: 1) Help me refine my argument to be historically specific and defensible, 2) Guide me in finding and evaluating evidence from multiple types of sources, 3) Help me anticipate and address counterarguments, 4) Teach me to distinguish between correlation and causation in historical events, 5) Help me write with appropriate historical context and vocabulary.",
            "Historical Empathy": "I'm trying to understand why [HISTORICAL FIGURE/GROUP] acted the way they did during [HISTORICAL EVENT/PERIOD]. I'm a [GRADE LEVEL] student. Please help me develop historical empathy by: 1) Helping me understand the world as they experienced it (beliefs, knowledge, constraints), 2) Guiding me to see multiple factors that influenced their decisions, 3) Helping me avoid presentism (judging the past by today's standards), 4) Discussing how different groups experienced the same events differently, 5) Connecting their choices to human motivations I can understand.",
            "Patterns & Connections": "I'm studying [HISTORICAL TOPIC A] and [HISTORICAL TOPIC B] and want to understand how they connect. I'm a [GRADE LEVEL] student. Please help me see historical patterns by: 1) Guiding me to identify similarities and differences between these topics, 2) Helping me understand how one influenced the other, 3) Discussing what broader historical trends or patterns they represent, 4) Connecting these historical patterns to other examples from different time periods, 5) Helping me predict or understand later historical developments based on these patterns.",
            "Research Projects": "I'm doing a history research project on [RESEARCH TOPIC] for my [GRADE LEVEL] class. Please guide my research process: 1) Help me develop focused, answerable research questions, 2) Suggest types of sources I should look for and how to evaluate them, 3) Guide me in organizing my research and taking effective notes, 4) Help me identify gaps in my research and potential bias in my sources, 5) Assist me in drawing conclusions that are supported by evidence and historically significant."
        },
        "Study Skills": {
            "Study Plans": "I need to study for [SUBJECT/TEST] covering [TOPICS] in [TIME AVAILABLE]. I'm a [GRADE LEVEL] student and I learn best through [LEARNING STYLE]. Please create a personalized study plan by: 1) Helping me assess what I already know vs. what I need to learn, 2) Prioritizing topics based on importance and my current understanding, 3) Suggesting study methods that match my learning style for each type of content, 4) Creating a realistic schedule that includes breaks and review time, 5) Building in self-testing and progress checks.",
            "Active Techniques": "I've been studying [SUBJECT/TOPIC] by re-reading my notes, but I'm not retaining the information well. I'm a [GRADE LEVEL] student. Please teach me active study methods by: 1) Explaining why passive reading isn't effective for learning, 2) Teaching me 3-4 active study techniques appropriate for this subject, 3) Guiding me through trying each technique with my actual study material, 4) Helping me create a study schedule that incorporates these active methods, 5) Teaching me how to test my understanding and identify gaps.",
            "Note-Taking": "I'm struggling to take good notes in my [SUBJECT] class. I'm a [GRADE LEVEL] student. Please help me develop better note-taking by: 1) Teaching me a note-taking system that works well for this subject, 2) Showing me how to identify and capture key information during class, 3) Helping me organize my notes for easy review and study, 4) Teaching me how to review and improve my notes after class, 5) Giving me strategies for taking notes from textbooks and other reading materials.",
            "Memory & Retention": "I understand [SUBJECT/TOPIC] when I study it, but I forget it quickly. I'm a [GRADE LEVEL] student. Please help me improve my memory by: 1) Teaching me why forgetting happens and how memory works, 2) Showing me specific memory techniques (mnemonics, visualization, etc.) for this type of content, 3) Helping me create memory aids for the material I'm currently studying, 4) Teaching me about spaced repetition and how to schedule review sessions, 5) Helping me connect new information to things I already know well.",
            "Test-Taking": "I get nervous during tests and don't perform as well as I could, especially on [TEST TYPE]. I'm a [GRADE LEVEL] student. Please help me improve my test performance by: 1) Teaching me specific strategies for this type of test (multiple choice, essay, etc.), 2) Helping me manage test anxiety through preparation and mindset techniques, 3) Showing me how to read questions carefully and avoid common mistakes, 4) Teaching me time management strategies for different test formats, 5) Helping me learn from my mistakes on past tests.",
            "Organization": "I'm struggling to keep up with assignments and study time for [SUBJECTS/CLASSES]. I'm a [GRADE LEVEL] student. Please help me get organized by: 1) Teaching me how to track assignments and due dates effectively, 2) Helping me break large projects into manageable steps, 3) Showing me how to prioritize tasks when I have multiple deadlines, 4) Teaching me to estimate how long tasks will take and plan accordingly, 5) Helping me create sustainable daily and weekly routines for academic success."
        }
    }

@st.cache_data
def get_prompt_techniques():
    """Cache the prompt techniques dictionary for better performance"""
    return {
        "Role Assignment": {
            "description": "Ask the AI to take on a specific educational role (tutor, teacher, coach) for personalized guidance.",
            "good_example": "Act as my patient biology tutor. I'm a high school student struggling with cellular respiration. Guide me through the process step-by-step, checking my understanding along the way.",
            "bad_example": "Explain cellular respiration."
        },
        "Learning Level Context": {
            "description": "Always specify your grade level and current understanding to get appropriately tailored responses.",
            "good_example": "I'm a 9th grade student who understands basic algebra but is new to quadratic equations. Can you explain how to solve x² + 5x + 6 = 0?",
            "bad_example": "How do you solve quadratic equations?"
        },
        "Guided Discovery": {
            "description": "Ask the AI to guide you to discover answers rather than just providing them directly.",
            "good_example": "I'm trying to understand why the American Civil War started. Instead of telling me the causes, ask me guiding questions that help me think through the factors and come to my own understanding.",
            "bad_example": "What caused the American Civil War?"
        },
        "Step-by-Step Scaffolding": {
            "description": "Request that complex topics be broken down into manageable, sequential steps.",
            "good_example": "I need to write a persuasive essay about climate change. Please guide me through the process: first help me develop a strong thesis, then organize my arguments, then work on evidence for each point.",
            "bad_example": "Help me write an essay about climate change."
        },
        "Error Analysis Learning": {
            "description": "Share your mistakes and ask for analysis of your thinking process, not just the correct answer.",
            "good_example": "I solved this physics problem but got the wrong answer: [show your work]. Help me identify where my reasoning went wrong and understand the correct thinking process.",
            "bad_example": "I got this wrong. What's the right answer?"
        },
        "Connection Building": {
            "description": "Ask the AI to help you connect new information to what you already know.",
            "good_example": "I just learned about photosynthesis. Help me understand how this connects to the water cycle and ecosystem concepts I learned last month.",
            "bad_example": "Tell me about photosynthesis."
        },
        "Real-World Application": {
            "description": "Request concrete examples of how concepts apply to real life or future careers.",
            "good_example": "I'm learning about statistics in math class. Show me 3 specific examples of how professionals in different careers actually use these statistical concepts in their daily work.",
            "bad_example": "Why is statistics important?"
        },
        "Socratic Questioning": {
            "description": "Ask the AI to use questions to develop your critical thinking rather than giving direct explanations.",
            "good_example": "I need to analyze this poem for English class. Instead of telling me what it means, ask me questions that help me discover the themes and literary devices myself.",
            "bad_example": "What does this poem mean?"
        },
        "Knowledge Gap Assessment": {
            "description": "Share your current understanding and ask the AI to identify and fill specific gaps.",
            "good_example": "Here's what I understand about the Revolutionary War: [your explanation]. What important aspects am I missing or misunderstanding?",
            "bad_example": "Teach me about the Revolutionary War."
        },
        "Multiple Perspectives": {
            "description": "Ask the AI to help you consider different viewpoints or approaches to complex topics.",
            "good_example": "Help me understand the debate about renewable energy by explaining the main arguments from environmental, economic, and technological perspectives.",
            "bad_example": "Is renewable energy good?"
        },
        "Practice Generation": {
            "description": "Request customized practice problems that match your current skill level and learning needs.",
            "good_example": "Create 3 algebra problems that start easy and get progressively harder, focusing on solving equations with variables on both sides. After I try each one, give me feedback.",
            "bad_example": "Give me some math problems to practice."
        },
        "Study Customization": {
            "description": "Ask for study methods tailored to your specific learning style and the subject matter.",
            "good_example": "I'm a visual learner preparing for a biology test on cell organelles. What study techniques would work best for me, and can you help me create visual study aids?",
            "bad_example": "How should I study for my biology test?"
        },
        "Explanation Check": {
            "description": "Test your understanding by explaining concepts back to the AI and asking for feedback.",
            "good_example": "Let me explain photosynthesis as I understand it: [your explanation]. Please tell me what I got right, what I missed, and help me correct any misconceptions.",
            "bad_example": "Do I understand photosynthesis correctly?"
        },
        "Progressive Difficulty": {
            "description": "Request that learning materials increase in complexity as your understanding grows.",
            "good_example": "Start with a simple explanation of fractions, then give me practice problems that gradually become more challenging as I master each level.",
            "bad_example": "Teach me about fractions."
        },
        "Metacognitive Reflection": {
            "description": "Ask the AI to help you think about your own learning process and strategies.",
            "good_example": "I notice I always struggle with word problems in math. Help me identify what makes them difficult for me and develop strategies to approach them more effectively.",
            "bad_example": "I'm bad at word problems."
        }
    }

# For backward compatibility, provide the original constants
SUBJECT_PROMPTS = get_subject_prompts()
PROMPT_TECHNIQUES = get_prompt_techniques()