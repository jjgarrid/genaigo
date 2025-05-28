# analysis/providers/ollama_adapter.py

from typing import Any, Dict
from langchain_community.llms import Ollama

class OllamaAdapter:
    def __init__(self, model: str = "llama2"):
        self.llm = Ollama(model=model)

    def analyze_text(self, prompt: str) -> str:
        return self.llm(prompt)
