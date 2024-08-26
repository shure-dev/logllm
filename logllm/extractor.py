import json

def extract_notebook_code(notebook_path: str) -> dict:
    """
    Extracts all code and output from a Jupyter Notebook file and returns it as a dictionary.

    Parameters:
        notebook_path (str): The path to the Jupyter Notebook file.

    Returns:
        dict: A dictionary containing all the code and output from the notebook.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = json.load(f)
    except Exception as e:
        print(f"Error loading notebook: {e}")
        return {}

    result_dict = {
        "Method": None,
        "Dataset": None,
        "Task": None,
        "Accuracy": None,
        "C": None,
        "Degree": None,
        "Tolerance (Tol)": None,
        "Cache Size": None,
        "Max Iterations": None,
        "Test Size": None,
        "Random State": None,
        "Kernel": None,
        "Condition as Natural Language": None,
        "Advice to Improve Accuracy": None
    }

    # Populate the dictionary with relevant data
    # This assumes the structure of your JSON follows the example you provided
    for cell in notebook_content.get('cells', []):
        source_content = ''.join(cell.get('source', []))
        # Extract specific attributes from the JSON content
        try:
            data = json.loads(source_content)
            if isinstance(data, dict):
                result_dict.update({
                    "Method": data.get("method"),
                    "Dataset": data.get("dataset"),
                    "Task": data.get("task"),
                    "Accuracy": data.get("accuracy"),
                    "C": data.get("C"),
                    "Degree": data.get("degree"),
                    "Tolerance (Tol)": data.get("tol"),
                    "Cache Size": data.get("cache_size"),
                    "Max Iterations": data.get("max_iter"),
                    "Test Size": data.get("test_size"),
                    "Random State": data.get("random_state"),
                    "Kernel": data.get("kernel"),
                    "Condition as Natural Language": "\n".join(data.get("condition_as_natural_langauge", [])),
                    "Advice to Improve Accuracy": "\n".join(data.get("advice_to_improve_acc", []))
                })
        except json.JSONDecodeError:
            continue
    
    return result_dict
