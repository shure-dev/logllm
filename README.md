
# LLM-Powered W&B

A package that automates the extraction of experimental conditions from Jupyter Notebooks, sends them to OpenAI, and logs the results using Weights & Biases (W&B).

## Features

- Automatically extracts code from Jupyter Notebook files.
- Sends extracted code to OpenAI for processing.
- Logs responses to Weights & Biases (W&B) for easy tracking and analysis.
- Simplifies the workflow for researchers and data scientists.

## Installation

To install the package, run the following command in your terminal:

```bash
pip install -e .
```

This command installs the package in editable mode, allowing you to modify the code and see changes without reinstalling.

## Usage

Here is a basic example of how to use the package:

```python
from llm_powered_wandb import extract_notebook_code, send_code_to_openai, log_to_wandb, init_wandb

# Initialize W&B
init_wandb(project_name='your_project_name')

# Extract code from Jupyter Notebook
notebook_path = 'your_notebook.ipynb'  # Specify your notebook path
code_string = extract_notebook_code(notebook_path)

# Send code to OpenAI
api_key = 'your_openai_api_key'  # Replace with your OpenAI API key
response_text = send_code_to_openai(api_key, code_string)

# Log response to W&B
log_to_wandb(response_text)

print("Response from OpenAI logged to W&B.")
```

## Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to submit an issue or a pull request.

## License

This project is licensed under the MIT License.
