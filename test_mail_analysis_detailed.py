#!/usr/bin/env python3
"""
Mail Analysis Test with Detailed Output
"""

import os
import sys
import json
import traceback
from datetime import datetime

def log_message(level, message):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def test_environment_setup():
    """Test environment configuration"""
    log_message("INFO", "Testing environment setup...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        log_message("SUCCESS", "Environment variables loaded")
        
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if deepseek_key and deepseek_key != "your_deepseek_api_key_here":
            log_message("SUCCESS", f"DeepSeek API key found: {deepseek_key[:15]}...")
            return True
        else:
            log_message("ERROR", "DeepSeek API key not found or invalid")
            return False
            
    except Exception as e:
        log_message("ERROR", f"Environment setup failed: {str(e)}")
        return False

def test_deepseek_direct():
    """Test DeepSeek API directly with requests"""
    log_message("INFO", "Testing DeepSeek API directly...")
    
    try:
        import requests
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            log_message("ERROR", "No API key available")
            return False
        
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
                    "content": "Extract entities from this email: 'Meeting with John Smith and Sarah Johnson in New York office about Q4 budget planning.' Return JSON with keys: people, locations, events."
                }
            ],
            "max_tokens": 500,
            "temperature": 0.3
        }
        
        log_message("INFO", "Sending request to DeepSeek API...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        log_message("INFO", f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            log_message("SUCCESS", "DeepSeek API call successful")
            log_message("INFO", f"Response content: {content}")
            return True
        else:
            log_message("ERROR", f"API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        log_message("ERROR", f"DeepSeek direct test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_adapter_classes():
    """Test the adapter classes"""
    log_message("INFO", "Testing adapter classes...")
    
    try:
        # Add backend to path
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)
        
        from analysis.providers.deepseek_adapter import DeepSeekAdapter
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        adapter = DeepSeekAdapter(api_key)
        
        log_message("INFO", "DeepSeekAdapter created successfully")
        
        test_prompt = "Extract entities from: 'Conference call with Mike Wilson and Lisa Brown about product launch in San Francisco.' Return JSON with people, locations, events."
        
        log_message("INFO", "Testing analysis...")
        result = adapter.analyze_text(test_prompt)
        
        log_message("SUCCESS", "Adapter analysis completed")
        log_message("INFO", f"Result: {result}")
        
        return True
        
    except Exception as e:
        log_message("ERROR", f"Adapter test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_gmail_analyzer_full():
    """Test the complete GmailAnalyzer"""
    log_message("INFO", "Testing GmailAnalyzer...")
    
    try:
        # Add backend to path
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)
        
        from analysis.gmail_analyzer import GmailAnalyzer
        from dotenv import load_dotenv
        load_dotenv()
        
        config = {
            "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY", ""),
            "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama2"),
        }
        
        analyzer = GmailAnalyzer("deepseek", config)
        log_message("SUCCESS", "GmailAnalyzer created successfully")
        
        sample_email = """
        Subject: Quarterly Business Review
        From: ceo@company.com
        
        Team,
        
        Please join us for the Q4 business review meeting next week.
        
        Details:
        - Date: December 15, 2024
        - Time: 2:00 PM EST
        - Location: New York headquarters, Executive Conference Room
        - Duration: 2 hours
        
        Attendees:
        - Robert Chen (CEO)
        - Sarah Martinez (CFO)
        - David Kim (CTO)
        - Jennifer Wilson (VP Marketing)
        - Michael Brown (VP Sales)
        
        Agenda:
        1. Q4 financial performance review
        2. 2025 budget planning
        3. Market expansion strategy
        4. Technology roadmap discussion
        5. Team growth plans
        
        Please prepare your departmental reports and send them to my assistant by December 10th.
        
        Looking forward to seeing everyone there.
        
        Best regards,
        Robert Chen
        """
        
        log_message("INFO", "Analyzing sample email...")
        result = analyzer.analyze(sample_email)
        
        log_message("SUCCESS", "GmailAnalyzer analysis completed")
        log_message("INFO", f"Analysis result: {json.dumps(result, indent=2)}")
        
        return True
        
    except Exception as e:
        log_message("ERROR", f"GmailAnalyzer test failed: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Mail Analysis Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("DeepSeek Direct API", test_deepseek_direct),
        ("Adapter Classes", test_adapter_classes),
        ("GmailAnalyzer Full", test_gmail_analyzer_full)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            log_message("ERROR", f"Test {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Mail analysis with LLM is working correctly!")
    elif passed > 0:
        print("\n⚠️ Some tests passed. The system is partially functional.")
    else:
        print("\n❌ All tests failed. Please check your configuration.")

if __name__ == "__main__":
    main()
