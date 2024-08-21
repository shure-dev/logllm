<div align="center">

# LogLLM

A package that automates the extraction of experimental conditions from your Python scripts with GPT4o-mini, and logs results using Weights & Biases (W&B).

[Project Website](https://logllm.tiiny.site/) | [Discord Community](https://discord.gg/3xvUV6xcKW)

</div>

## Features
- Automatically extracts code from Jupyter Notebook files with GPT4o then save extracted logs to Weights & Biases (W&B) for easy tracking and analysis.

## Installation
To install the package, run the following command in your terminal:
```bash
pip install -e .
```

This command installs the package in editable mode, allowing you to modify the code and see changes without reinstalling.

## Usage
Here is a simplified example of how to use the package:


```bash
export OPENAI_API_KEY="your-openai-api-key"
wandb login
```

`sample-script.ipynb`
```python

###
# Your machine learning script is here.
###

from logllm import logllm

notebook_path = "sample-script.ipynb" # Here is target file to log
project_name = "sample-project" # project name for wandb

logllm(notebook_path,project_name)
```

Check the demo code:  
https://github.com/shure-dev/logllm/blob/main/demos/svc-sample.ipynb

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to submit an issue or a pull request.

## License
This project is licensed under the MIT License.

Launched by https://github.com/shure-dev
