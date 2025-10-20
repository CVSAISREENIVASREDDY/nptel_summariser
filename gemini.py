import google.generativeai as genai
from google.generativeai import types
from google.api_core import exceptions
import json
import os

script_dir = os.path.dirname(__file__)

GEMINI_MODEL = "gemini-pro-latest"

def is_api_key_valid(api_key):
    """Validate the Gemini API key by making a lightweight call to the API."""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        return any('generateContent' in model.supported_generation_methods for model in models)
    except exceptions.PermissionDenied as e:
        print(f"Permission Denied Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during API key validation: {e}")
        return False


output_prompt = r"""
If there is an error fetching the transcript, just give one line describing the error.

Output structure:
Your output will be placed directly inside an HTML <div> tag and should only use standard HTML tags for all formatting (e.g., <p>, <b>, <i>, <br>).
Do not use Markdown.
All mathematical notation must be formatted for MathJax. Use \\( and \\) for all inline LaTeX, and use \\[ and \\] for all block LaTeX.
Do not wrap the entire response in an HTML or code block. Start the response content immediately."""

assignment_prompt = r"""
Explain the questions and answers in the following assignment. Provide a clear and concise explanation for each question.
"""

extra_questions_prompt = r"""
Based on the following weekly summary and original assignment questions, generate 10 additional assignment questions and options but not answers for them. The questions should be relevant to the topics covered in the summary and should be in a similar style to the original assignment questions.
"""


def call_gemini_api(api_key, system_prompt, model_ack_prompt, user_data):
    """
    A generalized function to call the Gemini API with a specific structure.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GEMINI_MODEL)

    full_prompt = (
        f"{system_prompt}\n\n{output_prompt}\n\n{model_ack_prompt}\n\n{user_data}"
    )

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"    ERROR generating content with Gemini: {e}")
        raise # Re-raise the exception to be caught by the main loop


def generate_ai_response(api_key, prompt, transcript):
    return call_gemini_api(
        api_key,
        system_prompt=prompt,
        model_ack_prompt="Here is the transcript:",
        user_data=transcript,
    )


def generate_assignment_explanation(api_key, assignment_text):
    return call_gemini_api(
        api_key,
        system_prompt=assignment_prompt,
        model_ack_prompt="Here is the assignment text:",
        user_data=assignment_text,
    )


def generate_extra_questions(api_key, weekly_summary, original_assignment):
    user_data = f"Weekly Summary:\n{weekly_summary}\n\nOriginal Assignment:\n{original_assignment}"
    return call_gemini_api(
        api_key,
        system_prompt=extra_questions_prompt,
        model_ack_prompt="Here is the weekly summary and original assignment:",
        user_data=user_data,
    ) 