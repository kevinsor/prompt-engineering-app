import random
import time
from typing import Dict, List, Tuple


class MockAIService:
    """Mock AI service that provides educational responses based on prompt quality"""

    def __init__(self):
        self.response_templates = {
            "math": {
                "good": [
                    "I'll help you solve this step by step. First, let me identify what type of problem this is...",
                    "Great question! Let me break this down into manageable steps for you...",
                    "I can see you're working on [topic]. Here's how I'd approach this problem..."
                ],
                "poor": [
                    "This is a math problem. The answer depends on what you're trying to solve.",
                    "I need more specific information about what you want to learn.",
                    "Math can be tricky. What specific concept are you struggling with?"
                ]
            },
            "science": {
                "good": [
                    "Excellent question! This concept is fundamental to understanding [topic]. Let me explain...",
                    "I'll help you understand this by connecting it to what you already know...",
                    "This is a great way to think about [concept]. Here's how it works..."
                ],
                "poor": [
                    "Science is a broad field. Can you be more specific about what you want to know?",
                    "That's an interesting topic. What particular aspect interests you?",
                    "I'd be happy to help, but I need more details about your question."
                ]
            },
            "english": {
                "good": [
                    "I can help you analyze this text. Let me guide you through the key literary elements...",
                    "Great thesis statement! Here's how I'd structure your essay to support this argument...",
                    "This writing shows good understanding. Here are some suggestions to make it even stronger..."
                ],
                "poor": [
                    "Writing and literature analysis can be complex. What specific help do you need?",
                    "There are many aspects to consider in literature. Which one interests you most?",
                    "I'd like to help with your writing. Can you share more details about your assignment?"
                ]
            },
            "history": {
                "good": [
                    "This historical period is fascinating! Let me help you understand the key causes and effects...",
                    "You're asking great analytical questions. Here's how historians typically approach this topic...",
                    "I'll help you connect these historical events to their broader context..."
                ],
                "poor": [
                    "History is complex with many interconnected events. What specific period interests you?",
                    "That's a broad historical topic. Which aspect would you like to explore?",
                    "Historical analysis requires focus. What particular question are you investigating?"
                ]
            },
            "general": {
                "good": [
                    "I appreciate how clearly you've explained your learning goals. Here's how I can help...",
                    "Your question shows good critical thinking. Let me guide you through this step by step...",
                    "This is exactly the kind of question that leads to deep learning. Here's my approach..."
                ],
                "poor": [
                    "I'd be happy to help you learn! Could you provide more specific details about what you need?",
                    "Learning is most effective when we're specific about our goals. What would you like to focus on?",
                    "I want to give you the best help possible. Can you tell me more about your current understanding?"
                ]
            }
        }

        self.educational_feedback = {
            "good_prompt_indicators": [
                "specific subject mentioned",
                "clear learning objective",
                "context provided",
                "specific question asked",
                "learning level indicated",
                "examples requested",
                "step-by-step approach requested"
            ],
            "improvement_suggestions": [
                "Try being more specific about your learning level",
                "Consider adding context about what you already know",
                "Ask for specific examples to illustrate the concept",
                "Request step-by-step explanations for complex topics",
                "Specify the format you'd like for the response",
                "Mention which part of the topic confuses you most"
            ]
        }

    def analyze_prompt_quality(self, prompt: str) -> Dict:
        """Analyze prompt quality and provide educational feedback"""
        prompt_lower = prompt.lower()

        # Score different aspects of the prompt
        scores = {
            "specificity": self._score_specificity(prompt_lower),
            "context": self._score_context(prompt_lower),
            "clarity": self._score_clarity(prompt_lower),
            "educational_value": self._score_educational_value(prompt_lower)
        }

        overall_score = sum(scores.values()) / len(scores)

        # Determine prompt quality
        if overall_score >= 7:
            quality = "excellent"
        elif overall_score >= 5:
            quality = "good"
        elif overall_score >= 3:
            quality = "fair"
        else:
            quality = "needs_improvement"

        return {
            "overall_score": round(overall_score, 1),
            "quality": quality,
            "scores": scores,
            "suggestions": self._get_improvement_suggestions(scores, prompt_lower)
        }

    def _score_specificity(self, prompt: str) -> float:
        """Score how specific the prompt is"""
        specific_keywords = [
            "explain", "analyze", "compare", "solve", "step by step",
            "example", "specific", "particular", "exactly", "precisely"
        ]

        score = 0
        for keyword in specific_keywords:
            if keyword in prompt:
                score += 1

        # Check for specific subjects or topics
        subjects = ["math", "science", "history", "english", "biology", "chemistry", "physics"]
        for subject in subjects:
            if subject in prompt:
                score += 2
                break

        return min(score, 10)

    def _score_context(self, prompt: str) -> float:
        """Score how much context is provided"""
        context_indicators = [
            "i'm a", "grade", "level", "student", "learning", "studying",
            "understand", "know", "background", "currently", "previously"
        ]

        score = 0
        for indicator in context_indicators:
            if indicator in prompt:
                score += 1.5

        # Bonus for mentioning specific educational level
        levels = ["elementary", "middle school", "high school", "college", "graduate"]
        for level in levels:
            if level in prompt:
                score += 3
                break

        return min(score, 10)

    def _score_clarity(self, prompt: str) -> float:
        """Score how clear and well-structured the prompt is"""
        clarity_indicators = [
            "?", "help me", "can you", "please", "i need", "how do i",
            "what is", "why does", "when should", "where can"
        ]

        score = 5  # Base score for basic structure

        for indicator in clarity_indicators:
            if indicator in prompt:
                score += 1

        # Penalty for very short prompts
        if len(prompt.split()) < 5:
            score -= 3

        # Bonus for reasonable length
        if 10 <= len(prompt.split()) <= 50:
            score += 2

        return max(min(score, 10), 0)

    def _score_educational_value(self, prompt: str) -> float:
        """Score the educational potential of the prompt"""
        educational_keywords = [
            "learn", "understand", "practice", "study", "explain", "teach",
            "concept", "theory", "principle", "method", "process", "why",
            "how", "what if", "compare", "contrast", "analyze", "evaluate"
        ]

        score = 0
        for keyword in educational_keywords:
            if keyword in prompt:
                score += 1

        # Bonus for asking for explanations rather than just answers
        explanation_requests = ["explain", "teach me", "help me understand", "walk me through"]
        for request in explanation_requests:
            if request in prompt:
                score += 3
                break

        return min(score, 10)

    def _get_improvement_suggestions(self, scores: Dict, prompt: str) -> List[str]:
        """Generate specific improvement suggestions based on scores"""
        suggestions = []

        if scores["specificity"] < 5:
            suggestions.append("Be more specific about what you want to learn or accomplish")

        if scores["context"] < 5:
            suggestions.append("Provide context about your learning level or background knowledge")

        if scores["clarity"] < 5:
            suggestions.append("Try to structure your question more clearly with specific details")

        if scores["educational_value"] < 5:
            suggestions.append("Focus on learning and understanding rather than just getting answers")

        # Add general suggestions
        if len(prompt.split()) < 10:
            suggestions.append("Consider expanding your prompt with more details and context")

        if "?" not in prompt:
            suggestions.append("Frame your request as a clear question")

        return suggestions

    def generate_mock_response(self, prompt: str, subject_hint: str = None) -> Tuple[str, Dict]:
        """Generate a mock AI response based on prompt quality"""

        # Simulate response time
        time.sleep(random.uniform(1, 3))

        # Analyze prompt quality
        analysis = self.analyze_prompt_quality(prompt)

        # Determine subject from prompt or hint
        subject = self._detect_subject(prompt, subject_hint)

        # Select appropriate response template
        if analysis["quality"] in ["excellent", "good"]:
            template_quality = "good"
        else:
            template_quality = "poor"

        # Get response template
        templates = self.response_templates.get(subject, self.response_templates["general"])
        response_template = random.choice(templates[template_quality])

        # Customize response based on prompt
        response = self._customize_response(response_template, prompt, subject, analysis)

        return response, analysis

    def _detect_subject(self, prompt: str, hint: str = None) -> str:
        """Detect the subject area from the prompt"""
        if hint:
            return hint.lower()

        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ["math", "equation", "solve", "calculate", "algebra", "geometry"]):
            return "math"
        elif any(word in prompt_lower for word in ["science", "biology", "chemistry", "physics", "experiment"]):
            return "science"
        elif any(word in prompt_lower for word in ["essay", "writing", "literature", "analyze", "poem", "story"]):
            return "english"
        elif any(word in prompt_lower for word in ["history", "historical", "war", "revolution", "century"]):
            return "history"
        else:
            return "general"

    def _customize_response(self, template: str, prompt: str, subject: str, analysis: Dict) -> str:
        """Customize the response template based on the specific prompt"""

        # Extract key terms from prompt for personalization
        prompt_words = prompt.lower().split()

        # Replace placeholders in template
        customized = template

        if "[topic]" in customized:
            topic = self._extract_topic(prompt, subject)
            customized = customized.replace("[topic]", topic)

        if "[concept]" in customized:
            concept = self._extract_concept(prompt)
            customized = customized.replace("[concept]", concept)

        # Add educational content based on quality
        if analysis["quality"] in ["excellent", "good"]:
            customized += f"\n\n{self._add_educational_content(subject, prompt)}"
        else:
            customized += f"\n\n{self._add_improvement_guidance(analysis)}"

        return customized

    def _extract_topic(self, prompt: str, subject: str) -> str:
        """Extract the main topic from the prompt"""
        topic_mapping = {
            "math": "mathematical concepts",
            "science": "scientific principles",
            "english": "literary analysis",
            "history": "historical events",
            "general": "this topic"
        }
        return topic_mapping.get(subject, "this subject")

    def _extract_concept(self, prompt: str) -> str:
        """Extract the main concept from the prompt"""
        # Simple concept extraction - could be made more sophisticated
        key_concepts = ["photosynthesis", "algebra", "democracy", "evolution", "gravity", "metaphor"]
        prompt_lower = prompt.lower()

        for concept in key_concepts:
            if concept in prompt_lower:
                return concept

        return "the concept you're asking about"

    def _add_educational_content(self, subject: str, prompt: str) -> str:
        """Add subject-specific educational content"""
        educational_content = {
            "math": "Remember to always show your work step by step, and don't hesitate to ask if you need clarification on any part of the solution.",
            "science": "Science is all about understanding the 'why' behind phenomena. Try to connect this concept to real-world examples you've observed.",
            "english": "When analyzing literature, always support your interpretations with specific evidence from the text.",
            "history": "Consider the historical context and multiple perspectives when studying historical events.",
            "general": "Remember that learning is most effective when you actively engage with the material and ask follow-up questions."
        }

        return educational_content.get(subject, educational_content["general"])

    def _add_improvement_guidance(self, analysis: Dict) -> str:
        """Add guidance for improving the prompt"""
        guidance = "To get better responses in the future, try to:\n"
        for suggestion in analysis["suggestions"][:3]:  # Show top 3 suggestions
            guidance += f"• {suggestion}\n"

        return guidance.strip()