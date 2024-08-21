import openai
import wandb
from .extractor import extract_notebook_code

def init_wandb(project_name):
    wandb.init(project=project_name)

def send_code_to_openai(api_key, code):
    openai.api_key = api_key
    prompt = f"Here is a Jupyter Notebook code:\n\n{code}\n\nPlease extract the experimental conditions and log them using the W&B API."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message['content']

def log_to_wandb(response_text):
    wandb.log({"openai_response": response_text})

def process_notebook(notebook_path, api_key, project_name):
    # Initialize W&B
    init_wandb(project_name)
    
    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

    # Send code to OpenAI
    response_text = send_code_to_openai(api_key, code_string)

    # Log response to W&B
    log_to_wandb(response_text)

    print("Response from OpenAI logged to W&B.")