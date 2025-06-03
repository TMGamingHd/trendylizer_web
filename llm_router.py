from dotenv import load_dotenv
load_dotenv()

import os
import random

# Example imports; in real use, conditionally import based on env availability
try:
    import openai
except ImportError:
    openai = None

# Simulated interfaces
def use_openai(prompt):
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Or your preferred model
        messages=[
            {"role": "system", "content": "You are a professional business consultant. Respond in clear, complete, markdown format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.85
    )
    return response.choices[0].message.content.strip()

def use_chatgpt_python(prompt):
    return f"[chatgpt-python] {prompt}"

def use_sora(prompt):
    return f"[Sora AI] {prompt}"

def use_groq(prompt):
    from groq import Groq
    import os
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",  # Or another supported model (like Mixtral-8x7b)
        messages=[
            {"role": "system", "content": "You are a business consultant. Respond in clear, markdown format."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=700
    )
    return chat_completion.choices[0].message.content.strip()
# Main router
def query_model(task_type, prompt):
    preferred = os.getenv("LLM_PROVIDER", "openai").lower()

    if preferred == "openai" and openai:
        try:
            return use_openai(prompt)
        except Exception:
            pass

    if preferred == "chatgpt-python":
        try:
            return use_chatgpt_python(prompt)
        except Exception:
            pass

    if preferred == "sora":
        try:
            return use_sora(prompt)
        except Exception:
            pass

    # Fallback: Groq or free tier
    return use_groq(prompt)
