import google.generativeai as genai
import os
from dotenv import load_dotenv
import openai
from logllm.log_llm import log_llm

# Load environment variables
load_dotenv()

# Configure Google Generative AI API Key
genai.configure(api_key=os.getenv('API_KEY'))
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Function to query OpenAI
def query_openai(user_input: str):

    system_prompt = """
        Convert the following query to a W&B API query:
    """.strip()

    user_prompt = f"""
    Here is a user's query: {user_input}
    """.strip()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    
    return response['choices'][0]['message']['content']

# Function to query Google Gemini
def query_gemini(user_input: str, code):
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
    user_input = f"{code}"

    system_prompt = """
        Please provide the data you want me to convert to a W&B API query:
    """.strip()

    user_prompt = f"""
    Here is a user's query: {user_input}
    """

    chat_session = model.start_chat(
        history=[
            {"role": "model", "parts": [system_prompt]},
            {"role": "user", "parts": [user_prompt]},
        ]
    )

    response = chat_session.send_message(user_prompt)
    return response.candidates[0].content.parts[0].text

# General query function that calls the appropriate provider

def query(user_input: str, provider: str):
    if provider == 'openai':
        return query_openai(user_input)
    elif provider == 'gemini':
        return query_gemini(user_input)
    else:
        raise ValueError("Invalid provider specified. Use 'openai' or 'gemini'.")
        

# Usage Example:

