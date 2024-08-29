import google.generativeai as genai
import wandb
from logllm import extract_notebook_code
import json
import os
from dotenv import load_dotenv
import markdown as md

load_dotenv()

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


def extract_experimental_conditions(code):
    user_input = f"""
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
        "advice_to_improve_acc": ["Use a bigger dataset.", "Use a simpler model."].

         f""Here is a user's Jupyter Notebook script: {code}"".
    """

    chat_session = model.start_chat(
    history=[
    {
      "role": "user",
      "parts": [
          "Hello! help me analyse data in json format only",
      ],
    },
    {
      "role": "model",
      "parts": [
          "Sure I can do that provide me with data",
      ],
    },
    ]
    )

    response = chat_session.send_message(user_input)
    result =  response.candidates[0].content.parts[0].text
    model_response = md.markdown(result)
    print("result: ", result)
    return model_response
    

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
        project_name = os.path.basename(notebook_path).replace(".ipynb", "")
    
    # Initialize W&B
    if is_logging:
        init_wandb(project_name)

    # Extract code from Jupyter Notebook
    code_string = extract_notebook_code(notebook_path)

     # Send code to Google Generative AI for processing
    parsed_json = extract_experimental_conditions(code_string)

    # parsed_json = json.dumps(parsed_json)
    # print(parsed_json)
   
    # Log the response to W&B
    if is_logging and parsed_json:
        log_to_wandb(parsed_json)

    print("Response from Google Generative AI processed and logged to W&B.")
    print("response: ", parsed_json)

    # print("Dictionary: ", parsed_json)  # Inspect the response to ensure it's valid JSON