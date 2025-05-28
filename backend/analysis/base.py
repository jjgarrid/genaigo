# analysis/base.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAnalyzer(ABC):
    """
    Abstract base class for analyzers. Each source type (e.g., Gmail, RSS) should implement this.
    """
    def __init__(self, provider: str, config: Dict[str, Any]):
        self.provider = provider
        self.config = config

    @abstractmethod
    def analyze(self, content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze the given content and return a structured report.
        """
        pass

    @abstractmethod
    def get_report(self, record_id: str) -> Dict[str, Any]:
        """
        Retrieve the analysis report for a given record.
        """
        pass
