import requests
import json
import time
from typing import Optional, Dict, List
import streamlit as st


class HuggingFaceService:
    """Service for interacting with Hugging Face's free Inference API"""

    def __init__(self):
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Content-Type": "application/json"
        }

        # Available free models for different use cases
        self.models = {
            "general": {
                "microsoft/DialoGPT-medium": "Conversational AI - Good for general questions",
                "google/flan-t5-large": "Text-to-Text - Excellent for educational content",
                "microsoft/DialoGPT-large": "Conversational AI - More sophisticated responses"
            },
            "text_generation": {
                "gpt2": "GPT-2 - Classic text generation model",
                "distilgpt2": "DistilGPT-2 - Faster, lighter version of GPT-2",
                "microsoft/DialoGPT-medium": "Dialogue-focused generation"
            },
            "question_answering": {
                "deepset/roberta-base-squad2": "Question Answering - Good for factual queries",
                "distilbert-base-cased-distilled-squad": "Question Answering - Fast responses"
            },
            "text2text": {
                "google/flan-t5-base": "Text-to-Text - Good for instructions and explanations",
                "google/flan-t5-large": "Text-to-Text - Better quality responses",
                "t5-base": "T5 - Versatile text-to-text model"
            }
        }

        # Default model for educational use
        self.default_model = "google/flan-t5-large"

    def get_available_models(self) -> Dict[str, Dict[str, str]]:
        """Get list of available models organized by category"""
        return self.models

    def query_model(self, prompt: str, model_name: str = None, max_retries: int = 3) -> Dict:
        """Query a Hugging Face model with the given prompt"""
        if not model_name:
            model_name = self.default_model

        url = f"{self.base_url}/{model_name}"

        # Prepare the payload based on model type
        payload = self._prepare_payload(prompt, model_name)

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "response": self._extract_response(result, model_name),
                        "model": model_name,
                        "raw_response": result
                    }
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    if attempt < max_retries - 1:
                        wait_time = 10 + (attempt * 5)  # Progressive backoff
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "error": f"Model is loading. Please try again in a few minutes.",
                            "status_code": response.status_code
                        }
                elif response.status_code == 429:
                    # Rate limited
                    return {
                        "success": False,
                        "error": "Rate limit exceeded. Please wait a moment before trying again.",
                        "status_code": response.status_code
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API Error: {response.status_code} - {response.text}",
                        "status_code": response.status_code
                    }

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return {
                    "success": False,
                    "error": "Request timed out. The model might be busy."
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Unexpected error: {str(e)}"
                }

        return {
            "success": False,
            "error": "Failed after multiple retries"
        }

    def _prepare_payload(self, prompt: str, model_name: str) -> Dict:
        """Prepare the API payload based on the model type"""

        # For text-to-text models (T5, FLAN-T5)
        if any(model in model_name.lower() for model in ["t5", "flan"]):
            return {
                "inputs": prompt,
                "parameters": {
                    "max_length": 512,
                    "temperature": 0.7,
                    "do_sample": True,
                    "top_p": 0.9
                }
            }

        # For conversational models (DialoGPT)
        elif "dialogo" in model_name.lower():
            return {
                "inputs": {
                    "past_user_inputs": [],
                    "generated_responses": [],
                    "text": prompt
                },
                "parameters": {
                    "max_length": 300,
                    "temperature": 0.7,
                    "repetition_penalty": 1.2
                }
            }

        # For question-answering models
        elif any(model in model_name.lower() for model in ["squad", "roberta", "distilbert"]):
            # For QA models, we need to provide context and question
            # We'll treat the prompt as the question and provide general context
            return {
                "inputs": {
                    "question": prompt,
                    "context": "This is an educational context where a student is asking for help with learning."
                }
            }

        # For general text generation models (GPT-2, etc.)
        else:
            return {
                "inputs": prompt,
                "parameters": {
                    "max_length": 400,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            }

    def _extract_response(self, result: Dict, model_name: str) -> str:
        """Extract the actual response text from the API result"""

        try:
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                item = result[0]

                # Text generation models
                if "generated_text" in item:
                    return item["generated_text"].strip()

                # Question answering models
                elif "answer" in item:
                    return item["answer"].strip()

                # Conversational models
                elif "generated_text" in item:
                    return item["generated_text"].strip()

            # For conversational models (DialoGPT)
            elif isinstance(result, dict):
                if "generated_text" in result:
                    return result["generated_text"].strip()
                elif "conversation" in result:
                    return result["conversation"]["generated_responses"][-1] if result["conversation"][
                        "generated_responses"] else "No response generated"

            # Fallback
            return str(result)

        except Exception as e:
            return f"Error parsing response: {str(e)}"

    def enhance_prompt_for_education(self, prompt: str, subject: str = None) -> str:
        """Enhance the user prompt for better educational responses"""

        educational_prefix = "You are a helpful educational assistant. "

        if subject:
            educational_prefix += f"The student is asking about {subject}. "

        educational_prefix += "Please provide a clear, educational response that helps the student learn. "

        # Add educational framing
        enhanced_prompt = f"{educational_prefix}Student question: {prompt}"

        return enhanced_prompt

    def get_model_recommendation(self, prompt: str, subject: str = None) -> str:
        """Recommend the best model based on the prompt and subject"""

        prompt_lower = prompt.lower()

        # For question-answering style prompts
        if any(word in prompt_lower for word in ["what", "why", "how", "when", "where", "who"]):
            return "google/flan-t5-large"  # Best for educational Q&A

        # For conversational/explanatory prompts
        elif any(word in prompt_lower for word in ["explain", "tell me", "help me understand", "discuss"]):
            return "microsoft/DialoGPT-medium"  # Good for explanations

        # For step-by-step or procedural prompts
        elif any(word in prompt_lower for word in ["step", "process", "how to", "guide", "walk me through"]):
            return "google/flan-t5-large"  # Excellent for structured responses

        # Default to the most versatile educational model
        else:
            return "google/flan-t5-large"

    def test_model_availability(self, model_name: str) -> Dict:
        """Test if a model is currently available and responsive"""
        test_prompt = "Hello, this is a test."
        result = self.query_model(test_prompt, model_name, max_retries=1)

        return {
            "available": result["success"],
            "model": model_name,
            "error": result.get("error") if not result["success"] else None
        }


# Utility functions for integration
def get_huggingface_service() -> HuggingFaceService:
    """Get or create HuggingFace service instance"""
    if 'hf_service' not in st.session_state:
        st.session_state.hf_service = HuggingFaceService()
    return st.session_state.hf_service


def format_educational_response(response: str, prompt: str) -> str:
    """Format the HuggingFace response for educational purposes"""

    # Clean up the response
    cleaned_response = response.strip()

    # Remove any repetition of the original prompt
    if prompt.lower() in cleaned_response.lower():
        # Find where the actual response starts
        lines = cleaned_response.split('\n')
        response_lines = []
        for line in lines:
            if line.strip() and not any(part.lower() in line.lower() for part in prompt.split()[:3]):
                response_lines.append(line)
        if response_lines:
            cleaned_response = '\n'.join(response_lines)

    # Add educational context if the response is too short
    if len(cleaned_response.split()) < 10:
        educational_note = "\n\n💡 Note: For more detailed responses, try being more specific in your prompt or ask follow-up questions!"
        cleaned_response += educational_note

    return cleaned_response