from setuptools import setup, find_packages

setup(
    name='logllm',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Gemini',
        'wandb',
    ],
    description='Automatically extract experimental conditions from your Python scripts with GPT4, and logs results with WandB.',
    author='Archilles',
    author_email='jakingsarchly@gmail.com',
    url='https://github.com/Archly2022/logllm.git',  # Replace with your GitHub URL
)