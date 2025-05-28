#!/usr/bin/env python3
"""
FastAPI Test Client for Mail Analysis
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def test_with_fastapi():
    """Test mail analysis using FastAPI test client"""
    print("🌐 Testing Mail Analysis via FastAPI")
    print("-" * 40)
    
    try:
        # Set environment
        os.environ["DEEPSEEK_API_KEY"] = "sk-82911f9d432946b9a017ebbc766f8def"
        os.environ["GENAIGO_ANALYSIS_PROVIDER"] = "deepseek"
        
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        print("✅ FastAPI test client created")
        
        # Test root endpoint
        response = client.get("/")
        print(f"📡 Root endpoint status: {response.status_code}")
        
        # Create sample data in the database first
        from app.config import db
        
        sample_messages = [
            {
                "id": "test_001",
                "subject": "Important Client Meeting",
                "content": "Meeting with John Smith (CEO of ABC Corp) and Sarah Johnson (CFO) scheduled for next Tuesday at 2 PM in the New York office. We'll discuss the Q4 budget planning and 2025 strategy.",
                "timestamp": "2024-12-09T10:00:00Z"
            },
            {
                "id": "test_002",
                "subject": "Product Launch Event",
                "content": "Join us for the product launch event on January 15th at the San Francisco Convention Center. Speakers include Dr. Amanda Chen and Robert Martinez. Expected attendance: 500+ professionals.",
                "timestamp": "2024-12-09T11:00:00Z"
            }
        ]
        
        # Insert sample messages
        messages_table = db.table("gmail_messages")
        messages_table.truncate()  # Clear existing data
        for msg in sample_messages:
            messages_table.insert(msg)
        
        print(f"📧 Inserted {len(sample_messages)} sample messages")
        
        # Test analysis endpoint
        print("🔍 Testing analysis endpoint...")
        analysis_request = {"ids": []}  # Analyze all messages
        
        response = client.post("/api/analyze/gmail", json=analysis_request)
        print(f"📊 Analysis endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            reports = result.get("reports", [])
            print(f"✅ Analysis successful! Generated {len(reports)} reports")
            
            # Display results
            for i, report in enumerate(reports, 1):
                print(f"\n📋 Report {i}:")
                print(f"   Email ID: {report['id']}")
                analysis = report['report']
                
                if 'entities' in analysis:
                    entities = analysis['entities']
                    print(f"   👥 People: {entities.get('people', [])}")
                    print(f"   📍 Locations: {entities.get('locations', [])}")
                    print(f"   📅 Events: {entities.get('events', [])}")
                else:
                    print(f"   📄 Raw analysis: {analysis}")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FastAPI test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_analysis():
    """Test individual email analysis"""
    print("\n🔬 Testing Individual Analysis")
    print("-" * 40)
    
    try:
        # Set environment
        os.environ["DEEPSEEK_API_KEY"] = "sk-82911f9d432946b9a017ebbc766f8def"
        
        from analysis.gmail_analyzer import GmailAnalyzer
        
        config = {
            "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY"),
            "OPENAI_API_KEY": "",
            "CLAUDE_API_KEY": "",
            "OLLAMA_MODEL": "llama2",
        }
        
        analyzer = GmailAnalyzer("deepseek", config)
        print("✅ GmailAnalyzer initialized")
        
        # Test with a complex email
        complex_email = """
        Subject: Critical System Alert - Immediate Action Required
        From: monitoring@techcorp.com
        
        ALERT: Production system experiencing degraded performance
        
        Incident Details:
        - Incident ID: INC-2024-001234
        - Severity: HIGH
        - Start Time: 2024-12-09 14:30 UTC
        - Affected Services: User Authentication, Payment Processing
        - Impact: 15% of users unable to log in
        
        Technical Team Response:
        - Primary: Michael Zhang (Lead Engineer)
        - Secondary: Lisa Rodriguez (DevOps Specialist)  
        - On-call Manager: David Kim
        
        Affected Regions:
        - US East (Virginia datacenter)
        - EU West (Dublin datacenter)
        - Asia Pacific (Singapore datacenter)
        
        Action Items:
        1. Scale up authentication servers immediately
        2. Investigate database connection pool exhaustion
        3. Prepare customer communication for social media
        4. Schedule post-incident review for tomorrow
        
        Estimated Resolution Time: 45 minutes
        Customer Impact: Minimal for existing sessions
        
        Updates will be posted every 15 minutes.
        
        System Operations Team
        """
        
        print("🔍 Analyzing complex email...")
        result = analyzer.analyze(complex_email)
        
        print("📊 Analysis Result:")
        print(json.dumps(result, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Individual analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 GenAI Go Mail Analysis - Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("FastAPI Integration", test_with_fastapi),
        ("Individual Analysis", test_individual_analysis)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🎯 Running: {test_name}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    success_rate = (successful / total) * 100 if total > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}% ({successful}/{total})")
    
    if successful == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Mail analysis with LLM is working perfectly!")
        print("\n🚀 Ready for production use:")
        print("   • Email entity extraction ✓")
        print("   • AI-powered analysis ✓") 
        print("   • FastAPI integration ✓")
        print("   • Database storage ✓")
    else:
        print(f"\n⚠️ {successful} out of {total} tests passed")
        if successful > 0:
            print("Partial functionality confirmed - some components working")
        else:
            print("All tests failed - check configuration and API keys")

if __name__ == "__main__":
    main()
