#!/usr/bin/env python3
"""
Test Mail Analysis with LLM
Comprehensive test for GenAI Go email analysis functionality
"""

import os
import sys
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

print("🧪 GenAI Go Mail Analysis Test")
print("=" * 50)

# Load environment variables
load_dotenv()

def create_sample_emails() -> List[Dict[str, Any]]:
    """Create sample email data for testing"""
    return [
        {
            "id": "test_001",
            "subject": "Q4 Business Review Meeting",
            "from": "john.smith@company.com",
            "content": """
            Hi Sarah,
            
            I hope this email finds you well. I wanted to schedule our Q4 business review meeting for next week.
            The meeting will be held at our New York office on December 15th at 2:00 PM.
            
            Attendees will include:
            - John Smith (CEO)
            - Sarah Johnson (CFO) 
            - Mike Wilson (CTO)
            - Lisa Brown (VP Sales)
            
            We'll be reviewing our quarterly performance, discussing the budget for 2024, and planning our expansion into the European market.
            
            Please confirm your attendance by December 10th.
            
            Best regards,
            John Smith
            """,
            "timestamp": "2024-12-08T10:30:00Z"
        },
        {
            "id": "test_002", 
            "subject": "Product Launch Event - San Francisco",
            "from": "events@techcorp.com",
            "content": """
            Dear Team,
            
            We're excited to announce our product launch event for the new AI-powered analytics platform.
            
            Event Details:
            - Date: January 20, 2025
            - Time: 6:00 PM - 9:00 PM PST
            - Location: Moscone Center, San Francisco, CA
            - Expected Attendees: 500+ industry professionals
            
            Key speakers include:
            - Dr. Amanda Chen (Chief Data Scientist)
            - Robert Martinez (Product Manager)
            - Jennifer Kim (Head of Engineering)
            
            The event will feature live demos, networking sessions, and a keynote presentation about the future of AI in business analytics.
            
            Please RSVP by January 15th.
            
            Best,
            Events Team
            """,
            "timestamp": "2024-12-09T14:22:00Z"
        },
        {
            "id": "test_003",
            "subject": "Customer Support Issue - Urgent",
            "from": "support@clientcompany.com", 
            "content": """
            Hello Support Team,
            
            We're experiencing critical issues with our payment processing system since yesterday morning.
            
            Issue Details:
            - Error Code: PAY_500_TIMEOUT
            - Affected Services: Credit card processing, PayPal integration
            - Impact: Unable to process customer orders
            - Estimated Revenue Loss: $25,000 per hour
            
            Technical contacts:
            - James Wilson (DevOps Lead)
            - Maria Garcia (Backend Engineer)
            - David Lee (QA Manager)
            
            We need immediate assistance to resolve this issue. Our customers in New York, Los Angeles, and Chicago are particularly affected.
            
            Priority: CRITICAL
            Expected Resolution: Within 2 hours
            
            Please escalate to senior engineering team immediately.
            
            Thanks,
            Customer Support
            """,
            "timestamp": "2024-12-09T09:15:00Z"
        }
    ]

def test_provider_connectivity():
    """Test connectivity to different AI providers"""
    print("\n🔌 Testing AI Provider Connectivity")
    print("-" * 40)
    
    providers = {
        "deepseek": os.getenv("DEEPSEEK_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"), 
        "claude": os.getenv("CLAUDE_API_KEY")
    }
    
    available_providers = []
    
    for provider, api_key in providers.items():
        if api_key and api_key != f"your_{provider}_api_key_here":
            print(f"✅ {provider.upper()}: API key configured")
            available_providers.append(provider)
        else:
            print(f"❌ {provider.upper()}: No API key found")
    
    # Test Ollama separately (local model)
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ OLLAMA: Local service available")
            available_providers.append("ollama")
        else:
            print("❌ OLLAMA: Service not responding")
    except:
        print("❌ OLLAMA: Service not available")
    
    return available_providers

def test_analysis_with_provider(provider: str, sample_emails: List[Dict[str, Any]]):
    """Test email analysis with a specific provider"""
    print(f"\n🤖 Testing Analysis with {provider.upper()}")
    print("-" * 40)
    
    try:
        from analysis.gmail_analyzer import GmailAnalyzer
        
        config = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "CLAUDE_API_KEY": os.getenv("CLAUDE_API_KEY", ""),
            "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY", ""),
            "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL", "llama2"),
        }
        
        analyzer = GmailAnalyzer(provider, config)
        
        results = []
        for email in sample_emails:
            print(f"\n📧 Analyzing: {email['subject']}")
            try:
                analysis = analyzer.analyze(email["content"], metadata=email)
                results.append({
                    "email_id": email["id"],
                    "subject": email["subject"],
                    "analysis": analysis,
                    "status": "success"
                })
                
                # Display results
                if "entities" in analysis:
                    entities = analysis["entities"]
                    print(f"   👥 People: {', '.join(entities.get('people', []))}")
                    print(f"   📍 Locations: {', '.join(entities.get('locations', []))}")
                    print(f"   📅 Events: {', '.join(entities.get('events', []))}")
                else:
                    print(f"   📊 Analysis: {json.dumps(analysis, indent=2)}")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                results.append({
                    "email_id": email["id"],
                    "subject": email["subject"], 
                    "error": str(e),
                    "status": "failed"
                })
        
        return results
        
    except Exception as e:
        print(f"❌ Failed to initialize {provider} analyzer: {str(e)}")
        return []

def test_api_endpoints():
    """Test the FastAPI analysis endpoints"""
    print("\n🌐 Testing API Endpoints")
    print("-" * 40)
    
    try:
        import requests
        base_url = "http://localhost:8000"
        
        # Test health check
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server is running")
            else:
                print(f"⚠️ Backend server responding with status {response.status_code}")
        except requests.exceptions.RequestException:
            print("❌ Backend server is not running")
            print("   💡 Start with: npm run backend")
            return False
        
        # Test analysis endpoint
        try:
            payload = {"ids": []}  # Analyze all messages
            response = requests.post(f"{base_url}/api/analyze/gmail", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis endpoint working - {len(result.get('reports', []))} reports generated")
                return True
            else:
                print(f"❌ Analysis endpoint error: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {str(e)}")
            return False
            
    except ImportError:
        print("❌ requests library not available")
        return False

def generate_test_report(all_results: Dict[str, List]):
    """Generate a comprehensive test report"""
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    total_tests = 0
    successful_tests = 0
    
    for provider, results in all_results.items():
        if not results:
            continue
            
        print(f"\n{provider.upper()} Provider:")
        provider_success = 0
        for result in results:
            total_tests += 1
            if result.get("status") == "success":
                successful_tests += 1
                provider_success += 1
                print(f"  ✅ {result['subject']}")
            else:
                print(f"  ❌ {result['subject']} - {result.get('error', 'Unknown error')}")
        
        success_rate = (provider_success / len(results)) * 100 if results else 0
        print(f"  📈 Success Rate: {success_rate:.1f}% ({provider_success}/{len(results)})")
    
    overall_success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"\n🎯 Overall Success Rate: {overall_success_rate:.1f}% ({successful_tests}/{total_tests})")
    
    return {
        "total_tests": total_tests,
        "successful_tests": successful_tests, 
        "success_rate": overall_success_rate,
        "provider_results": all_results
    }

def main():
    """Main test function"""
    print("Starting comprehensive mail analysis test...\n")
    
    # Step 1: Check provider connectivity
    available_providers = test_provider_connectivity()
    
    if not available_providers:
        print("\n❌ No AI providers available!")
        print("💡 Set up at least one provider:")
        print("   - Copy .env.example to .env")
        print("   - Add your API keys")
        print("   - Or start Ollama locally")
        return
    
    # Step 2: Create sample data
    sample_emails = create_sample_emails()
    print(f"\n📧 Created {len(sample_emails)} sample emails for testing")
    
    # Step 3: Test analysis with each available provider
    all_results = {}
    for provider in available_providers:
        results = test_analysis_with_provider(provider, sample_emails)
        all_results[provider] = results
    
    # Step 4: Test API endpoints (optional)
    print("\n🔍 Checking if backend is running for API tests...")
    api_working = test_api_endpoints()
    
    # Step 5: Generate report
    report = generate_test_report(all_results)
    
    # Step 6: Recommendations
    print("\n💡 Recommendations:")
    if report["success_rate"] >= 80:
        print("✅ Mail analysis system is working well!")
    elif report["success_rate"] >= 50:
        print("⚠️ Mail analysis system has some issues - check provider configurations")
    else:
        print("❌ Mail analysis system needs attention - check API keys and connections")
    
    if not api_working:
        print("🚀 Start the backend server to test API endpoints: npm run backend")
    
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        sys.exit(1)
