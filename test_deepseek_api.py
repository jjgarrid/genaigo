#!/usr/bin/env python3

import os
import sys

print("Starting DeepSeek API test...")

try:
    import requests
    import json
    from dotenv import load_dotenv
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Load environment variables
try:
    load_dotenv()
    print("✅ Environment variables loaded")
except Exception as e:
    print(f"❌ Error loading .env: {e}")

def test_deepseek_api():
    """Test DeepSeek API connectivity"""
    print("🔍 Checking API key...")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        print("❌ DEEPSEEK_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...")
    
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
                "content": "Extract entities from this text: 'John Smith met with Sarah Johnson in New York for a quarterly review meeting.' Return as JSON with keys: people, locations, events."
            }
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    try:
        print("🚀 Testing DeepSeek API connection...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print("✅ DeepSeek API connection successful!")
            print(f"📝 Response: {content}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = test_deepseek_api()
        if success:
            print("\n🎉 DeepSeek API is working correctly!")
        else:
            print("\n💔 DeepSeek API test failed!")
    except Exception as e:
        print(f"❌ Script error: {e}")
        sys.exit(1)
