# analysis/providers/deepseek_adapter.py

from typing import Any, Dict
import json
import requests

class DeepSeekAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        
    def analyze_text(self, prompt: str) -> str:
        if not self.api_key or self.api_key == "your_deepseek_api_key_here":
            # Return mock response for testing
            return json.dumps({
                "people": ["John Doe", "Jane Smith"],
                "locations": ["New York", "San Francisco"],
                "events": ["Meeting", "Conference Call", "Project Review"]
            })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return content
            
        except requests.exceptions.RequestException as e:
            print(f"DeepSeek API error: {e}")
            # Fallback to mock response on error
            return json.dumps({
                "people": ["Error: API call failed"],
                "locations": ["Error: API call failed"],
                "events": ["Error: API call failed"],
                "error": str(e)
            })
