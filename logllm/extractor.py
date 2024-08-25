import json

def extract_notebook_code(notebook_path: str) -> str:
    """
    Extracts all code and output from a Jupyter Notebook file.

    Parameters:
        notebook_path (str): The path to the Jupyter Notebook file.

    Returns:
        str: A string containing all the code and output from the notebook, or an empty string if an error occurs.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = json.load(f)
    except Exception as e:
        print(f"Error loading notebook: {e}")
        return ""

    all_cells = []
    for cell in notebook_content.get('cells', []):
        # Extract the content of the cell
        source_content = ''.join(cell.get('source', []))
        all_cells.append(source_content)
        
        # Extract output cells if available
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'text' in output:
                    output_content = ''.join(output['text'])
                    all_cells.append(output_content)
                elif 'data' in output and 'text/plain' in output['data']:
                    output_content = ''.join(output['data']['text/plain'])
                    all_cells.append(output_content)
        
    full_content = "\n".join(all_cells)
    return full_content
