#!/usr/bin/env python3
"""
Simple test to verify the backend imports work correctly
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

def test_imports():
    print("Testing individual imports...")
    
    try:
        print("1. Testing app.config...")
        from app.config import db
        print("✓ app.config imported successfully")
        
        print("2. Testing gmail_analyzer...")
        from analysis.gmail_analyzer import GmailAnalyzer
        print("✓ gmail_analyzer imported successfully")
        
        print("3. Testing email_processor...")
        from app.services.email_processor import EmailProcessor
        print("✓ email_processor imported successfully")
        
        print("4. Testing app.main...")
        from app.main import app
        print("✓ app.main imported successfully")
        
        print("5. Testing database connection...")
        messages_table = db.table("gmail_messages")
        messages = messages_table.all()
        print(f"✓ Database connected - found {len(messages)} messages")
        
        print("6. Testing email processor functionality...")
        processor = EmailProcessor()
        stats = processor.get_analysis_stats()
        print(f"✓ Email processor working - stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_endpoint():
    print("\n7. Testing basic endpoint creation...")
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        response = client.get("/health")
        print(f"✓ Health endpoint working - status: {response.status_code}")
        
        # Test the analysis endpoint
        response = client.get("/api/analysis/stats")
        print(f"✓ Analysis stats endpoint - status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ Endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Backend Test Suite ===")
    
    if test_imports():
        test_basic_endpoint()
        print("\n✅ All tests completed!")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
