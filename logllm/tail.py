from llm_model import log_llm
import os

notebook_path = "demos/svc-sample.ipynb" # Here is target file to log

log_llm(notebook_path, project_name = None, is_logging=True)