# analysis/providers/claude_adapter.py

from typing import Any, Dict
from langchain_community.llms import Anthropic

class ClaudeAdapter:
    def __init__(self, api_key: str):
        self.llm = Anthropic(anthropic_api_key=api_key)

    def analyze_text(self, prompt: str) -> str:
        return self.llm(prompt)
