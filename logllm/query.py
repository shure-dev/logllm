import google.generativeai as genai
import os
from dotenv import load_dotenv
import openai
from logllm.log_llm import log_llm

# Load environment variables
load_dotenv()

# Configure Google Generative AI API Key
genai.configure(api_key=os.getenv('API_KEY'))

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
def query_gemini(user_input: str):
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = """
        Convert the following query to a W&B API query:
    """.strip()

    user_prompt = f"""
    Here is a user's query: {user_input}
    """.strip()

    chat_session = model.start_chat(
        history=[
            {"role": "system", "parts": [system_prompt]},
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
notebook_path = "demos/svc-sample.ipynb" 

# Extract experimental conditions and results using log_llm
parsed_json = log_llm(notebook_path, project_name="Machine learning", is_logging=False, provider="gemini")

# Use the parsed_json as user_input for the query
response = query("what is the best model? :{parsed_json}", provider="gemini")

# Print the response from the query
print(response)
