import openai
import wandb

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
    wandb.finish()