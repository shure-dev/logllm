import json

def extract_notebook_code(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = json.load(f)
    except Exception as e:
        print(f"Error loading notebook: {e}")
        return

    all_cells = []
    for cell in notebook_content.get('cells', []):
        # セルの内容を取得
        source_content = ''.join(cell.get('source', []))
        all_cells.append(source_content)
        
        # 出力セル（output）を取得
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