<div align="center">

# LogLLM

A package that automates the extraction of experimental conditions from your Python scripts with GPT4o-mini, and logs results using Weights & Biases (W&B).

[Project Website](https://logllm.tiiny.site/) | [Discord Community](https://discord.gg/3xvUV6xcKW) | [Google Colab](https://colab.research.google.com/drive/1s4VMa4iaD85uZEcuhQmiosQ6Wkk5pj-c?usp=sharing) 


</div>

## Feature
Automatically extracts code from Jupyter Notebook files with GPT4o then save extracted logs to Weights & Biases (W&B) for easy tracking and analysis.

## Installation
To install the package, run the following command in your terminal:
```bash
git clone https://github.com/shure-dev/logllm.git
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

from logllm import log_llm

notebook_path = "sample-script.ipynb" # Here is target file to log
project_name = "sample-project" # project name for wandb

log_llm(notebook_path,project_name)
```


# How it works: very simple, and powerful!

LLM(`Our prompt` + `Your ML script`) = `Extracted experimental conditions`

Our prompt
```
You are advanced machine learning experiment designer.
Extract all experimental conditions and results for logging via wandb api. 
Add your original params in your JSON responce if you want to log other params.
Extract all informaiton you can find the given script as int, bool or float value.
If you can not describe conditions with int, bool or float value, use list of natural language.
Give advice to improve the acc.
If you use natural language, answer should be very short.
Do not include information already provided in param_name_1 for `condition_as_natural_langauge`.
Output JSON schema example:
This is just a example, make it change as you want.
{{
    "method":"str",
    "dataset":"str",
    "task":"str",
    "is_advanced_method":bool,
    "is_latest_method":"",
    "accuracy":"",
    "other_param_here":"",
    "other_param_here":"",
    ...
    "condition_as_natural_langauge":["Small dataset."],
    "advice_to_improve_acc":["Use bigger dataset.","Use more simple model."]
}}
```

Your ML script: `svc-sample.ipynb`

```Python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()

X = iris.data[iris.target != 2] 
y = iris.target[iris.target != 2]  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = SVC(kernel='linear')
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
```

Extracted experimental conditions

```Python
{
    "method": "SVC",
    "dataset": "Iris",
    "task": "classification",
    "is_advanced_method": false,
    "is_latest_method": "",
    "accuracy": 1.00,
    "kernel": "linear",
    "test_size": 0.2,
    "random_state": 42,
    "condition_as_natural_langauge": ["Using linear kernel on SVC model.", "Excluding class 2 from Iris dataset.", "Splitting data into 80% training and 20% testing."],
    "advice_to_improve_acc": ["Confirm dataset consistency.", "Consider cross-validation for validation."]
}

```


Check the demo code:  
https://github.com/shure-dev/logllm/blob/main/demos/svc-sample.ipynb

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to submit an issue or a pull request.

## License
This project is licensed under the MIT License.