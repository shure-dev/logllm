from openai import OpenAI
import wandb
from .extractor import extract_notebook_code
import json
# import logging

# wandb.logger.setLevel(logging.ERROR)

def init_wandb(project_name):
    wandb.init(project=project_name, settings=wandb.Settings(_disable_stats=True))

def extract_experimental_conditions(code):
    client = OpenAI()
    
    prompt = f"""
        # Please extract all experimental conditions and results for logging via wandb api. 
        # Extract all informaiton you can find the given script
        # Output JSON schema:
        {{
            "param_name_1":"",
            "param_name_2":"",
            "condition":"here is condition as natural language description"
        }}
        # Here is a Jupyter Notebook script:{code}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        response_format = { "type": "json_object" }
    )
    
    # print(response.choices[0].message.content)
    
    return response.choices[0].message.content

def log_to_wandb(response_text):
    print(response_text)
    wandb.log(json.loads(response_text))

def logllm(notebook_path, project_name):
    
    # import psutil

    # def get_notebook_name():
    #     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    #         if proc.info['name'] == 'python' and 'jupyter-notebook' in proc.info['cmdline']:
    #             for cmd in proc.info['cmdline']:
    #                 if cmd.endswith('.ipynb'):
    #                     return cmd
    #     return None

    # notebook_name = get_notebook_name()
    # print(f"Notebook Name: {notebook_name}")
    
    # Initialize W&B
    init_wandb(project_name)
    
    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

    # Send code to OpenAI
    response_text = extract_experimental_conditions(code_string)

    # Log response to W&B
    log_to_wandb(response_text)

    print("Response from OpenAI logged to W&B.")