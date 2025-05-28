#!/usr/bin/env python3
"""
Manual Mail Analysis Demo
This script demonstrates mail analysis functionality without relying on terminal execution.
"""

import os
import sys
import json
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def setup_environment():
    """Setup environment variables manually"""
    os.environ["DEEPSEEK_API_KEY"] = "sk-82911f9d432946b9a017ebbc766f8def"
    os.environ["GENAIGO_ANALYSIS_PROVIDER"] = "deepseek"
    print("✅ Environment variables set")

def demo_deepseek_adapter():
    """Demonstrate DeepSeek adapter functionality"""
    print("\n🤖 DeepSeek Adapter Demo")
    print("-" * 30)
    
    try:
        from analysis.providers.deepseek_adapter import DeepSeekAdapter
        
        # Initialize adapter
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        adapter = DeepSeekAdapter(api_key)
        print(f"✅ DeepSeek adapter initialized with key: {api_key[:15]}...")
        
        # Test prompt
        prompt = """
        Extract entities from this email content:
        
        "Meeting with John Smith (CEO) and Sarah Johnson (CFO) scheduled for next Tuesday at 2 PM in the New York office. We'll discuss Q4 budget planning, revenue projections, and the upcoming product launch."
        
        Return JSON with keys: people, locations, events, topics
        """
        
        print("🚀 Analyzing email content...")
        result = adapter.analyze_text(prompt)
        
        print("📊 Analysis Result:")
        try:
            # Try to parse and pretty print JSON
            parsed = json.loads(result)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def demo_gmail_analyzer():
    """Demonstrate full GmailAnalyzer functionality"""
    print("\n📧 Gmail Analyzer Demo")
    print("-" * 30)
    
    try:
        from analysis.gmail_analyzer import GmailAnalyzer
        
        # Configuration
        config = {
            "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY"),
            "OPENAI_API_KEY": "",
            "CLAUDE_API_KEY": "",
            "OLLAMA_MODEL": "llama2",
        }
        
        # Initialize analyzer
        analyzer = GmailAnalyzer("deepseek", config)
        print("✅ GmailAnalyzer initialized")
        
        # Sample email content
        email_content = """
        Subject: Urgent: Server Downtime Resolution Meeting
        From: devops@techcorp.com
        To: engineering-team@techcorp.com
        
        Dear Engineering Team,
        
        We're experiencing critical server issues affecting our production environment. 
        
        Emergency meeting details:
        - Date: Today, 3:00 PM EST
        - Location: Engineering Lab, Building C, Floor 5
        - Expected duration: 1 hour
        
        Attendees required:
        - Michael Chen (DevOps Lead)
        - Lisa Rodriguez (Backend Engineer)
        - David Park (Infrastructure Manager)
        - Amanda Kim (Security Specialist)
        
        Agenda:
        1. Root cause analysis of server failures
        2. Immediate mitigation strategies
        3. Long-term infrastructure improvements
        4. Customer communication plan
        
        Current impact:
        - API response times increased by 300%
        - Customer login failures in US West region
        - Database connection timeouts
        - Estimated revenue impact: $15K/hour
        
        Please drop everything and attend. This is our highest priority.
        
        Best regards,
        Operations Team
        """
        
        print("🔍 Analyzing sample email...")
        analysis_result = analyzer.analyze(email_content, metadata={
            "id": "sample_001",
            "timestamp": "2024-12-09T15:30:00Z",
            "from": "devops@techcorp.com"
        })
        
        print("📋 Analysis Complete!")
        print(json.dumps(analysis_result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def demo_multiple_emails():
    """Demonstrate analysis of multiple emails"""
    print("\n📬 Multiple Email Analysis Demo")
    print("-" * 40)
    
    emails = [
        {
            "id": "email_001",
            "subject": "Marketing Campaign Results",
            "content": "Great news! Our Q4 marketing campaign exceeded expectations. Sarah Martinez and Tom Wilson will present results at the San Francisco office next week. ROI improved by 35%."
        },
        {
            "id": "email_002", 
            "subject": "Customer Support Escalation",
            "content": "Priority ticket from Enterprise client ABC Corp. Issue affects their payment processing. Contact: Jennifer Lee (their CTO). Estimated impact: $50K. Need immediate response."
        },
        {
            "id": "email_003",
            "subject": "Team Building Event",
            "content": "Annual team building event scheduled for December 20th at Golden Gate Park in San Francisco. Activities include team challenges and networking lunch. RSVP to HR by December 15th."
        }
    ]
    
    try:
        from analysis.gmail_analyzer import GmailAnalyzer
        
        config = {
            "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY"),
            "OPENAI_API_KEY": "",
            "CLAUDE_API_KEY": "",
            "OLLAMA_MODEL": "llama2",
        }
        
        analyzer = GmailAnalyzer("deepseek", config)
        
        results = []
        for email in emails:
            print(f"\n📧 Analyzing: {email['subject']}")
            analysis = analyzer.analyze(email["content"])
            results.append({
                "email": email,
                "analysis": analysis
            })
            
            # Show quick summary
            if "entities" in analysis and isinstance(analysis["entities"], dict):
                entities = analysis["entities"]
                print(f"   👥 People: {len(entities.get('people', []))} found")
                print(f"   📍 Locations: {len(entities.get('locations', []))} found")
                print(f"   📅 Events: {len(entities.get('events', []))} found")
        
        print(f"\n✅ Successfully analyzed {len(results)} emails")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main demo function"""
    print("🧪 GenAI Go - Mail Analysis with LLM Demo")
    print("=" * 50)
    
    # Setup
    setup_environment()
    
    # Run demos
    demos = [
        ("DeepSeek Adapter", demo_deepseek_adapter),
        ("Gmail Analyzer", demo_gmail_analyzer),
        ("Multiple Emails", demo_multiple_emails)
    ]
    
    results = {}
    for demo_name, demo_func in demos:
        print(f"\n🎯 Running: {demo_name}")
        try:
            results[demo_name] = demo_func()
        except Exception as e:
            print(f"❌ Demo {demo_name} failed: {str(e)}")
            results[demo_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DEMO SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    for demo_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{demo_name}: {status}")
    
    print(f"\nOverall: {successful}/{total} demos successful")
    
    if successful == total:
        print("\n🎉 All demos successful! Mail analysis with LLM is working perfectly!")
        print("\n💡 Next steps:")
        print("   - Start the backend server: cd backend && python -m uvicorn app.main:app --reload")
        print("   - Test API endpoints at http://localhost:8000/docs")
        print("   - Start frontend: cd frontend && npm run dev")
    elif successful > 0:
        print(f"\n⚠️ {successful} out of {total} demos worked. Partial functionality confirmed.")
    else:
        print("\n❌ All demos failed. Check your API key configuration.")

if __name__ == "__main__":
    main()
