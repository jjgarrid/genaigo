#!/usr/bin/env python3
"""
Simple Mail Analysis Test
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

def test_simple_analysis():
    print("🧪 Testing Mail Analysis with LLM")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Test email content
    sample_email = """
    Subject: Marketing Meeting - Product Launch Discussion
    
    Hi team,
    
    We need to schedule a marketing meeting for next week to discuss our new product launch.
    
    Attendees:
    - Sarah Johnson (Marketing Director)
    - Mike Chen (Product Manager) 
    - Lisa Wang (Sales Lead)
    
    Location: San Francisco office, Conference Room A
    Date: Next Tuesday, 2 PM PST
    
    We'll be discussing:
    - Launch timeline for Q1 2025
    - Marketing budget allocation
    - Customer acquisition strategy
    - Partnership opportunities
    
    Please confirm your attendance by Friday.
    
    Best regards,
    John Smith
    CEO, TechCorp
    """
    
    # Test with DeepSeek adapter directly
    try:
        from analysis.providers.deepseek_adapter import DeepSeekAdapter
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        print(f"🔑 Using API key: {api_key[:15]}..." if api_key else "❌ No API key found")
        
        adapter = DeepSeekAdapter(api_key)
        
        prompt = f"""
        Extract key information from this email content and return as JSON with these keys:
        - people: list of people mentioned
        - locations: list of locations mentioned  
        - events: list of events/meetings mentioned
        - topics: list of main topics discussed
        
        Email content:
        {sample_email}
        """
        
        print("\n🚀 Sending request to DeepSeek...")
        result = adapter.analyze_text(prompt)
        
        print("\n📊 Analysis Result:")
        print("-" * 20)
        
        try:
            # Try to parse as JSON
            parsed_result = json.loads(result)
            print(json.dumps(parsed_result, indent=2))
        except json.JSONDecodeError:
            # If not JSON, print raw result
            print(result)
        
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False

def test_gmail_analyzer():
    print("\n🔬 Testing GmailAnalyzer Class")
    print("=" * 40)
    
    try:
        from analysis.gmail_analyzer import GmailAnalyzer
        
        config = {
            "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY", ""),
            "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama2"),
        }
        
        analyzer = GmailAnalyzer("deepseek", config)
        
        sample_content = """
        Important client meeting scheduled for tomorrow at 3 PM in New York office.
        Attendees: Robert Martinez (VP Sales), Jennifer Kim (Account Manager).
        Topics: Contract renewal, budget planning for 2025, expansion strategy.
        """
        
        print("📧 Analyzing sample email content...")
        result = analyzer.analyze(sample_content)
        
        print("\n📋 GmailAnalyzer Result:")
        print(json.dumps(result, indent=2))
        
        print("\n✅ GmailAnalyzer test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ GmailAnalyzer test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting simple mail analysis tests...\n")
    
    test1_success = test_simple_analysis()
    test2_success = test_gmail_analyzer()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"DeepSeek Adapter Test: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"GmailAnalyzer Test: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! Mail analysis is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
