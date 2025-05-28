#!/usr/bin/env python3
"""
Quick DeepSeek Test
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_deepseek():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("ERROR: No DeepSeek API key found")
        return
    
    print(f"Testing with key: {api_key[:15]}...")
    
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": "Extract people, locations, and events from: 'John Smith met with Sarah Johnson in New York for a quarterly review.' Return as JSON."
            }
        ],
        "max_tokens": 300,
        "temperature": 0.1
    }
    
    try:
        print("Sending request...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print("SUCCESS!")
            print("Response:")
            print(content)
        else:
            print("ERROR!")
            print(response.text)
    
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_deepseek()
