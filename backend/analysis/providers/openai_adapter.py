# analysis/providers/openai_adapter.py

from typing import Any, Dict
from langchain_community.llms import OpenAI

class OpenAIAdapter:
    def __init__(self, api_key: str):
        self.llm = OpenAI(openai_api_key=api_key)

    def analyze_text(self, prompt: str) -> str:
        return self.llm(prompt)
