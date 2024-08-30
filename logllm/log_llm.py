import google.generativeai as genai
import wandb
from logllm import extract_notebook_code
import json
import os
from dotenv import load_dotenv
import markdown as md
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv('API_KEY'))

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def init_wandb(project_name):
    wandb.init(project=project_name, settings=wandb.Settings(_disable_stats=True))

def extract_experimental_conditions_gemini(code):
    user_input = f"""
         You are an advanced machine learning experiment designer.
         Extract all experimental conditions and results for logging via wandb API. 
         Add your original parameters in your JSON response if you want to log other parameters.
         Extract all information you can find in the given script as int, bool, or float values.
         If you cannot describe conditions with int, bool, or float values, use a list of natural language.
         Give advice to improve the accuracy.
         If you use natural language, the answers should be short.
         Do not include information already provided in param_name_1 for `condition_as_natural_language`.
         
         Here is a user's Jupyter Notebook script: {code}
    """.replace("    ","")

    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": ["Hello! help me analyse data in json format only"]},
            {"role": "model", "parts": ["Sure I can do that, provide me with data"]},
        ]
    )

    response = chat_session.send_message(user_input)
    result = response.candidates[0].content.parts[0].text
    
    parsed_json = json.loads(result)
    formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
    print("response: ", formatted_json)
    return formatted_json

def extract_experimental_conditions_openai(code):
    client = OpenAI()

    system_prompt = """
        You are an advanced machine learning experiment designer.
        Extract all experimental conditions and results for logging via wandb API.
        Add your original parameters in your JSON response if you want to log other parameters.
        Extract all information you can find in the given script as int, bool, or float values.
        If you cannot describe conditions with int, bool, or float values, use a list of natural language.
        Give advice to improve the accuracy.
        If you use natural language, the answers should be very short.
        Do not include information already provided in param_name_1 for `condition_as_natural_language`.
    """.replace("    ", "")

    user_prompt = f"""
    Here is a user's Jupyter Notebook script:{code}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    parsed_json = json.loads(response.choices[0].message.content)
    formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)
    print(formatted_json)

    return response.choices[0].message.content

def log_to_wandb(response_text):
    try:
        response_dict = json.loads(response_text)
        wandb.log(response_dict)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error logging to W&B: {e}")

def log_llm(notebook_path, project_name=None, is_logging=False, provider=None):
    if project_name is None:
        project_name = os.path.basename(notebook_path).replace(".ipynb", "")
    
    if is_logging:
        init_wandb(project_name)

    code_string = extract_notebook_code(notebook_path)

    if provider == "gemini":
        parsed_json = extract_experimental_conditions_gemini(code_string)
    elif provider == "openai":
        parsed_json = extract_experimental_conditions_openai(code_string)
    else:
        raise ValueError("Invalid provider specified. Use 'gemini' or 'openai'.")

    if is_logging and parsed_json:
        log_to_wandb(parsed_json)

    print("Response from the provider processed and logged to W&B.")
    return parsed_json
