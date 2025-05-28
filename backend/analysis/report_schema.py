# analysis/report_schema.py

from typing import Dict, Any
from datetime import datetime

def create_report(entities: Dict[str, Any], provider: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "entities": entities,
        "metadata": {
            "date_of_analysis": datetime.utcnow().isoformat(),
            "provider": provider,
            "parameters": parameters
        }
    }
