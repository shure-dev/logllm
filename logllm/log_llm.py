from openai import OpenAI
import wandb
from .extractor import extract_notebook_code
import json


def init_wandb(project_name):
    wandb.init(project=project_name, settings=wandb.Settings(_disable_stats=True))


def extract_experimental_conditions(code):
    client = OpenAI()

    system_prompt = """
        # You are advanced machine learning experiment designer.
        # Extract all experimental conditions and results for logging via wandb api. 
        # Add your original params in your JSON responce if you want to log other params.
        # Extract all informaiton you can find the given script as int, bool or float value.
        # If you can not describe conditions with int, bool or float value, use list of natural language.
        # Give advice to improve the acc.
        # If you use natural language, answer should be very short.
        # Do not include information already provided in param_name_1 for `condition_as_natural_langauge`.
        # Output JSON schema example:
        This is just a example, make it change as you want. Use nested dictionally if nessasary.
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
            "condition_as_natural_langauge":["Small dataset."],
            "advice_to_improve_acc":["Use bigger dataset.","Use more simple model."]
        }}
    """.replace("    ","")

    user_prompt = f"""
    # Here is a user's Jupyter Notebook script:{code}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    # Parse the JSON string from `response.choices[0].message.content` into a dictionary
    parsed_json = json.loads(response.choices[0].message.content)

    # Format the dictionary to make it more readable (4-space indentation, non-ASCII characters displayed as is)
    formatted_json = json.dumps(parsed_json, indent=4, ensure_ascii=False)

    # Print the formatted JSON data
    print(formatted_json)
    
    return response.choices[0].message.content


def log_to_wandb(response_text):
    wandb.log(json.loads(response_text))


def log_llm(notebook_path, project_name = None, is_logging = False):

    
    if project_name is None:
        project_name = notebook_path.replace(".ipynb","")
        
    # Initialize W&B
    if is_logging:
        init_wandb(project_name)

    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

    # Send code to OpenAI
    response_text = extract_experimental_conditions(code_string)

    # Log response to W&B
    if is_logging:
        log_to_wandb(response_text)

    print("Response from OpenAI logged to W&B.")
