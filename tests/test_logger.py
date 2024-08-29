import pytest
import json
from logllm.log_llm import log_llm
from logllm.extractor import extract_notebook_code




# Define a sample notebook path and project name for testing
notebook_path = "sample_notebook.ipynb"
project_name = "test_project"

# Mock notebook content for testing
sample_notebook_content = {
    "cells": [
        {
            "cell_type": "code",
            "source": ["print('Hello, World!')\n"]
        },
        {
            "cell_type": "markdown",
            "source": ["This is a markdown cell."]
        },
        {
            "cell_type": "code",
            "source": ["a = 10\n", "b = 20\n", "c = a + b\n", "print(c)\n"]
        }
    ]
}

# Function to create a sample notebook file for testing
def create_sample_notebook(notebook_file):
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(sample_notebook_content, f)

def test_log_llm(monkeypatch, tmp_path):
    # Create a temporary notebook file
    notebook_file = tmp_path / notebook_path
    create_sample_notebook(notebook_file)

    # Mock the W&B init and log functions
    def mock_init(*args, **kwargs):
        pass

    def mock_log(data):
        assert "method" in data
        assert data["method"] == "example_method"

    monkeypatch.setattr("wandb.init", mock_init)
    monkeypatch.setattr("wandb.log", mock_log)

    # Mock the Google Generative AI response
    def mock_generate_content(*args, **kwargs):
        class MockResponse:
            choices = [type('obj', (object,), {
                "message": type('msg', (object,), {
                    "content": json.dumps({
                        "method": "example_method",
                        "dataset": "example_dataset",
                        "task": "example_task",
                        "accuracy": 0.95,
                        "other_param_here": {
                            "param1": 10,
                            "param2": 20
                        },
                        "condition_as_natural_language": ["Small dataset."],
                        "advice_to_improve_acc": ["Use a bigger dataset.", "Use a simpler model."]
                    })
                })
            })]

        return MockResponse()

    monkeypatch.setattr("google.generativeai.GenerativeModel.start_chat", mock_generate_content)

    # Call the log_llm function to test
    log_llm(str(notebook_file), project_name, is_logging=True)
    
    print("Test completed successfully.")

if __name__ == "__main__":
    pytest.main([__file__])