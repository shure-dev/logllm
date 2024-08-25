---
name: Bug report
about: Create a report to help us improve
title: "[BUG] <function displacements>"
labels: bug
assignees: 'Archilles'

---

## Bug Description
- Provide a clear and concise description of what the bug is.
1) The dependencies are declining due to the specified versions when installing from the `requirements.txt`. I suggest removing them to prevent unseen errors, that would install the latest version for each dependencies.

2) File "/Users/jake/vscode/logllm-1/logllm/log_llm.py", line 3, in <module>
    from .extractor import extract_notebook_code
ImportError: attempted relative import with no known parent package
solution: remove the dot --> `from extractor import extract_notebook_code`

3) "logllm" is not defined [Ln 85, Col 5] on `test_logger.py` file 
solution: refactor to `    test_logllm(str(notebook_file), "api_key", "sample_notebook.ipynb")` 

4) ![alt text](<Screenshot 2024-08-24 at 11.35.33 PM.png>) 
solution: I havent figured it out has something to do with `_init_.py` Question: What does the `_init_.py` does?

## Steps to Reproduce
- List the steps to reproduce the behavior:
  1. Go to '...'
  2. Click on '...'
  3. Scroll down to '...'
  4. See error
The GPT generative had to be changed for unavialablity usage.
Go to to the log_llm.py for change of codes.

## Expected Behavior
- Describe what you expected to happen.

## Screenshots
- If applicable, add screenshots to help explain the issue.

## Environment Information
- OS: [e.g. Windows, macOS, Linux]
- Python version: [e.g. 3.8.5]
- Package version: [e.g. v1.2.3]

## Additional Context
- Add any other context about the problem here.
I do not have a paid token for the GPT4o so had to compromise by using a different generative model -Gemini.