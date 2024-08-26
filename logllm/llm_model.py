import google.generativeai as genai
import wandb
from extractor import extract_notebook_code
import json
import os

genai.configure(api_key=os.environ['API_KEY'])

def init_wandb(project_name):
    wandb.init(project=project_name, settings=wandb.Settings(_disable_stats=True))


def extract_experimental_conditions(code):
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
         {{
             "method": "str",
             "dataset": "str",
             "task": "str",
             "accuracy": float,
             "other_param_here": {{
                "param1": int,
             "param2": int
            }},
           "condition_as_natural_language": ["Small dataset."],
        "advice_to_improve_acc": ["Use a bigger dataset.", "Use a simpler model."]
        Here is a user's Jupyter Notebook script:{code}

    Your answers should return a dictionary like this: 
    "method": "SVC",
    "dataset": "Iris",
    "task": "classification",
    "accuracy": 1.0,
    "C": 1.0,
    "degree": 3,
    "tol": 0.001,
    "cache_size": 200,
    "max_iter": -1,
    "test_size": 0.2,
    "random_state": 42,
    "kernel": "linear",
    "condition_as_natural_langauge": [
        "Using linear kernel on SVC model.",
        "Excluding class 2 from Iris dataset.",
        "Splitting data into 80% training and 20% testing."
    ],
    "advice_to_improve_acc": [
        "Consider using cross-validation for better performance evaluation.",
        "Experiment with different kernels to optimize results.",
        "Increase the dataset size to improve generalization."
    ]
}
    Remeber this is just an example how the data shuold be returned.

    """

    model = genai.GenerativeModel("gemini-1.5-pro", 
                                  generation_config={"response_mime_type": "application/json"},
                                  system_instruction="You are an advanced machine learning expert that is responsible for making realistic prdedictions and recommendations on machine learning patterns")
    response = model.generate_content(system_prompt)

    
    # Print for debugging
    print(f"Response content: {response}")

    # Return the extracted JSON content
    return response

def log_to_wandb(response_text):
    try:
        # Parse the response text into a dictionary
        response_dict = json.loads(response_text)
        # Log the dictionary to W&B
        wandb.log(response_dict)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error logging to W&B: {e}")

def log_llm(notebook_path, project_name=None, is_logging=False):
    if project_name is None:
        project_name = notebook_path.replace(".ipynb", "")

    # Initialize W&B
    if is_logging:
        init_wandb(project_name)

    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

    # Send code to Generative AI
    response_text = extract_experimental_conditions(code_string)

    # Log response to W&B
    if is_logging:
        log_to_wandb(response_text)

    print("Response from Google Generative AI processed and logged to W&B.")
    

    

def log_to_wandb(parsed_json):
    if parsed_json:
        try:
            # Log the parsed JSON to W&B
            wandb.log(parsed_json)
        except Exception as e:
            print(f"Error logging to W&B: {e}")
    else:
        print("No data to log. Parsed JSON is empty or None.")


def log_llm(notebook_path, project_name=None, is_logging=False):
    if project_name is None:
        project_name = os.path.basename(notebook_path).replace(".ipynb", "")
    
    # Initialize W&B
    if is_logging:
        init_wandb(project_name)

    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

     # Send code to Google Generative AI for processing
    parsed_json = extract_experimental_conditions(code_string)
   
    # Log the response to W&B
    if is_logging and parsed_json:
        log_to_wandb(parsed_json)

    print("Response from Google Generative AI processed and logged to W&B.")

    print("Dictionary: ", parsed_json)  # Inspect the response to ensure it's valid JSON


