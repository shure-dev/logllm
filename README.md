<div align="center">

# LogLLM

A package that automates the extraction of experimental conditions from your Python scripts with GPT4o-mini, and logs results using Weights & Biases (W&B).

[Project Website](https://logllm.tiiny.site/) | [Discord Community](https://discord.gg/3xvUV6xcKW)

</div>

## Features
- Automatically extracts code from Jupyter Notebook files with GPT4o.
- Logs responses to Weights & Biases (W&B) for easy tracking and analysis.
- Simplifies the ml development workflow for researchers and data scientists.

## Installation
To install the package, run the following command in your terminal:
```bash
pip install -e .
```
This command installs the package in editable mode, allowing you to modify the code and see changes without reinstalling.

## Usage
Here is a simplified example of how to use the package:
```python
from logllm import logllm

# Specify your parameters
notebook_path = 'your_notebook.ipynb'  # Path to your Jupyter Notebook
api_key = 'your_openai_api_key'  # Replace with your OpenAI API key
project_name = 'your_project_name'  # Name of your W&B project

# Process the notebook
logllm(notebook_path, api_key, project_name)
```

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to submit an issue or a pull request.

## License
This project is licensed under the MIT License.

Launched by https://github.com/shure-dev
