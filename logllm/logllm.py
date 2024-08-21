from openai import OpenAI
import wandb
from .extractor import extract_notebook_code
import os

def init_wandb(project_name):
    wandb.init(project=project_name)

def extract_experimental_conditions(code):
    client = OpenAI()
    
    prompt = f"Here is a Jupyter Notebook code:\n\n{code}\n\nPlease extract the experimental conditions and log them using the W&B API."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message['content']

def log_to_wandb(response_text):
    wandb.log({"openai_response": response_text})

def logllm(notebook_path, project_name):
    # Initialize W&B
    init_wandb(project_name)
    
    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

    # Send code to OpenAI
    response_text = extract_experimental_conditions(code_string)

    # Log response to W&B
    log_to_wandb(response_text)

    print("Response from OpenAI logged to W&B.")