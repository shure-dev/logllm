import google.generativeai as genai
import wandb
from logllm import extract_notebook_code
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

def init_wandb(project_name):
    wandb.init(project=project_name, settings=wandb.Settings(_disable_stats=True))

# Load environment variables from a .env file
load_dotenv()

# Function to configure Google Generative AI only when needed
def configure_google_genai():
    # Set up Google Generative AI with API key and model configuration
    genai.configure(api_key=os.getenv('API_KEY'))

    # Define generation settings for the model
    generation_config = {
        "temperature": 0,  # Controls the randomness of the output
        "top_p": 0.95,     # Nucleus sampling parameter
        "top_k": 64,       # Limits the pool of candidates to the top-k
        "max_output_tokens": 8192,  # Maximum number of tokens in the output
        "response_mime_type": "application/json",  # Expected response format
    }

    # Initialize and return the GenerativeModel instance
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

# System prompt for guiding the AI model to extract experiment details
system_prompt = """
    You are an advanced machine learning experiment designer.
    Extract all experimental conditions and results for logging via wandb API. 
    Add your original parameters in your JSON response if you want to log other parameters.
    Extract all information you can find in the given script as int, bool, or float values.
    If you cannot describe conditions with int, bool, or float values, use a list of natural language.
    Give advice to improve the accuracy.
    If you use natural language, the answers should be very short.
    Do not include information already provided in param_name_1 for `condition_as_natural_language`.
    Output JSON schema example:
    This is just an example, make changes as necessary. Use nested dictionaries if necessary.
    {{
        "method":"str",
        "dataset":"str",
        "task":"str",
        "accuracy":"",
        "other_param_here":{
            "other_param_here":"",
            "other_param_here":"",
        },
        "other_param_here":"",
        ...
        "condition_as_natural_language":["Small dataset."],
        "advice_to_improve_acc":["Use a bigger dataset.","Use a simpler model."]
    }}
""".replace("    ", "")

# Function to extract experimental conditions using the specified provider (Google or OpenAI)
def extract_experimental_conditions(provider, code):
    # Combine system prompt with user's code input
    user_input = f"{system_prompt}\n\nHere is a user's Jupyter Notebook script: {code}"

    if provider == "gemini":
        # Configure and use Google Generative AI if specified
        model = configure_google_genai()
        chat_session = model.start_chat(
            history=[{"role": "user", "parts": ["Hello! help me analyze data in JSON format only and return only json object nothing else"]}]
        )
        response = chat_session.send_message(user_input)
        result = response.candidates[0].content.parts[0].text

    elif provider == "openai":
        # Use OpenAI's API to get the response
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": user_input},
            ],
            response_format={"type": "json_object"},
        )
        result = response.choices[0].message.content

    else:
        # Raise an error if an invalid provider is specified
        raise ValueError("Invalid provider specified. Use 'gemini' or 'openai'.")

    # Parse the result from JSON string to Python dictionary
    parsed_json = json.loads(result)
    # Format the JSON output for better readability
    return json.dumps(parsed_json, indent=4, ensure_ascii=False)

# Function to log the extracted information to Weights & Biases (W&B)
def log_to_wandb(response_text):
    try:
        # Parse the JSON response and log it to W&B
        response_dict = json.loads(response_text)
        wandb.log(response_dict)
    except (json.JSONDecodeError, Exception) as e:
        # Handle errors in JSON parsing or W&B logging
        print(f"Error logging to W&B: {e}")

# Main function to extract and log experimental conditions from a Jupyter Notebook
def log_llm(notebook_path, project_name=None, is_logging=False, provider=None):
    # Use the notebook file name as the project name if not specified
    project_name = project_name or os.path.basename(notebook_path).replace(".ipynb", "")
    if is_logging:
        # Initialize a new W&B run if logging is enabled
        init_wandb(project_name)

    # Extract the code from the notebook
    code_string = extract_notebook_code(notebook_path)
    # Extract the experimental conditions using the specified AI provider
    parsed_json = extract_experimental_conditions(provider, code_string)

    if is_logging and parsed_json:
        # Log the extracted information to W&B
        log_to_wandb(parsed_json)

    # Inform the user that the process is complete
    print("Response from the provider processed and logged to W&B.")