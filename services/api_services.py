import requests
import streamlit as st
from typing import Optional


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