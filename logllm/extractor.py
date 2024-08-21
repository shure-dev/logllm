import json

def extract_notebook_code(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    
    code_cells = []
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code':
            code_cells.append(''.join(cell['source']))
    
    full_code = "\n".join(code_cells)
    print("Extracted script",full_code)
    return full_code