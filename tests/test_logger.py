import pytest
import json  # jsonモジュールをインポート

from logllm.extractor import extract_notebook_code
from logllm.logllm import extract_experimental_conditions, logllm

# サンプルのJupyter Notebookの内容を含むJSONを定義
sample_notebook_content = {
    "cells": [
        {
            "cell_type": "code",
            "source": ["print('Hello, World!')\n"]
        },
        {
            "cell_type": "markdown",
            "source": ["This is a markdown cell."]
        },
        {
            "cell_type": "code",
            "source": ["a = 10\n", "b = 20\n", "c = a + b\n", "print(c)\n"]
        }
    ]
}

def test_extract_notebook_code(tmp_path):
    # テスト用の一時ファイルを作成して、サンプルNotebook JSONを書き込む
    notebook_file = tmp_path / "sample_notebook.ipynb"
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(sample_notebook_content, f)

    # コード抽出関数をテスト
    extracted_code = extract_notebook_code(notebook_file)
    expected_code = "print('Hello, World!')\n\na = 10\nb = 20\nc = a + b\nprint(c)\n"
    assert extracted_code == expected_code

def test_extract_experimental_conditions(monkeypatch):
    # モックを使用してOpenAIのAPIレスポンスをシミュレート
    def mock_chat_completion_create(*args, **kwargs):
        return {
            'choices': [
                {'message': {'content': 'Extracted conditions from the code.'}}
            ]
        }

    monkeypatch.setattr("openai.ChatCompletion.create", mock_chat_completion_create)

    # APIキーとコードを仮定してテスト
    api_key = "fake-api-key"
    code = "print('Hello, World!')\n"
    response = extract_experimental_conditions(api_key, code)
    assert response == 'Extracted conditions from the code.'

def test_logllm(monkeypatch, tmp_path):
    # モックのW&Bの初期化とログ関数
    def mock_init(*args, **kwargs):
        pass

    def mock_log(data):
        assert "openai_response" in data
        assert data["openai_response"] == 'Extracted conditions from the code.'

    monkeypatch.setattr("wandb.init", mock_init)
    monkeypatch.setattr("wandb.log", mock_log)

    # モックのOpenAIレスポンス
    def mock_chat_completion_create(*args, **kwargs):
        return {
            'choices': [
                {'message': {'content': 'Extracted conditions from the code.'}}
            ]
        }

    monkeypatch.setattr("openai.ChatCompletion.create", mock_chat_completion_create)

    # テスト用の一時ファイルを作成して、サンプルNotebook JSONを書き込む
    notebook_file = tmp_path / "sample_notebook.ipynb"
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(sample_notebook_content, f)

    # logllm関数をテスト
    logllm(str(notebook_file), "fake-api-key", "test-project")