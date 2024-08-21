from setuptools import setup, find_packages

setup(
    name='llm-powered-wandb',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'wandb',
    ],
    description='A package to extract code from Jupyter Notebooks, send to OpenAI, and log results to W&B.',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/your_username/llm-powered-wandb',  # Replace with your GitHub URL
)