# analysis/gmail_analyzer.py

from typing import Any, Dict
from .base import BaseAnalyzer
from .report_schema import create_report
from .providers.openai_adapter import OpenAIAdapter
from .providers.claude_adapter import ClaudeAdapter
from .providers.deepseek_adapter import DeepSeekAdapter
from .providers.ollama_adapter import OllamaAdapter

class GmailAnalyzer(BaseAnalyzer):
    def __init__(self, provider: str, config: Dict[str, Any]):
        super().__init__(provider, config)
        self.adapter = self._init_adapter(provider, config)

    def _init_adapter(self, provider: str, config: Dict[str, Any]):
        if provider == "openai":
            return OpenAIAdapter(config["OPENAI_API_KEY"])
        elif provider == "claude":
            return ClaudeAdapter(config["CLAUDE_API_KEY"])
        elif provider == "deepseek":
            return DeepSeekAdapter(config["DEEPSEEK_API_KEY"])
        elif provider == "ollama":
            return OllamaAdapter(model=config.get("OLLAMA_MODEL", "llama2"))
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def analyze(self, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        prompt = self._build_prompt(content)
        result = self.adapter.analyze_text(prompt)
        # Here, parse result to extract entities (NER)
        entities = self._parse_entities(result)
        return create_report(entities, self.provider, self.config)

    def _build_prompt(self, content: str) -> str:
        return (
            "Extract the following from the email content: "
            "1. Key people\n2. Key locations\n3. Key events. "
            "Return as JSON with keys: people, locations, events.\n\n"
            f"Email content:\n{content}"
        )

    def _parse_entities(self, result: str) -> Dict[str, Any]:
        import json
        try:
            return json.loads(result)
        except Exception:
            return {"people": [], "locations": [], "events": [], "raw": result}

    def get_report(self, record_id: str) -> Dict[str, Any]:
        # Implement TinyDB lookup here
        from backend.services.gmail_fetcher import get_analysis_report_by_id
        return get_analysis_report_by_id(record_id)
