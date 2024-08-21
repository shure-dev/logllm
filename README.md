<h1 style="text-align: center;">LLM-Powered W&B</h1>

<p style="text-align: center;">
  A tool that automates the extraction of experimental conditions from your machine learning scripts and saves them using the Weights & Biases (W&B) API.
</p>

<p style="text-align: center;">
  Better than MLflow's Autolog, this tool automates everything for seamless experiment tracking.
</p>

<h2 style="text-align: center;">Features</h2>
<ul style="text-align: center;">
  <li>Automated extraction and logging of experimental conditions</li>
  <li>Streamlined workflows for data scientists</li>
  <li>Enhanced documentation and reproducibility</li>
  <li>Comprehensive automation for seamless integration</li>
</ul>

<h2 style="text-align: center;">Installation</h2>
<pre style="text-align: center;">
pip install llm-powered-wandb
</pre>

<h2 style="text-align: center;">Usage</h2>
<pre style="text-align: center;">
import wandb
from llm_powered_wandb import LLMLogger

# Initialize W&B
wandb.init(project="your_project_name")

# Log with LLM
logger = LLMLogger()
logger.log_experiment(params)
</pre>

<h2 style="text-align: center;">Contributing</h2>
<p style="text-align: center;">
  Contributions are welcome! Please open an issue or submit a pull request.
</p>

<h2 style="text-align: center;">License</h2>
<p style="text-align: center;">
  This project is licensed under the MIT License.
</p>
