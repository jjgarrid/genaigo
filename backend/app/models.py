from pydantic import BaseModel
from typing import Any, Dict

class SourceConfig(BaseModel):
    name: str
    type: str
    endpoint: str
    method: str
    headers: Dict[str, Any]
    params: Dict[str, Any]
    parser: str
