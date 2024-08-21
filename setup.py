from setuptools import setup, find_packages

setup(
    name='logllm',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'wandb',
    ],
    description='Automatically extract experimental conditions from your Python scripts with GPT4, and logs results with WandB.',
    author='Yusuke',
    author_email='yusuke.mikami.contact@gmail.com',
    url='https://github.com/shure-dev/logllm',  # Replace with your GitHub URL
)