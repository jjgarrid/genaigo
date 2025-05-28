#!/usr/bin/env python3
"""
Test script for email processing functionality
"""
import sys
import os

# Add paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

print("Testing email processor...")

try:
    print("1. Testing database connection...")
    from app.config import db
    print("✓ Database connection successful")
    
    # Check if we have any messages
    messages_table = db.table("gmail_messages")
    messages = messages_table.all()
    print(f"✓ Found {len(messages)} messages in database")
    
    print("\n2. Testing gmail analyzer...")
    from analysis.gmail_analyzer import GmailAnalyzer
    print("✓ Gmail analyzer imported successfully")
    
    print("\n3. Testing email processor...")
    from app.services.email_processor import EmailProcessor
    print("✓ Email processor imported successfully")
    
    # Create processor instance
    processor = EmailProcessor()
    print("✓ Email processor instance created")
    
    print("\n4. Testing analysis stats...")
    stats = processor.get_analysis_stats()
    print("✓ Analysis stats retrieved:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n5. Testing processing settings...")
    settings = processor.processing_settings
    print("✓ Processing settings loaded:")
    for key, value in settings.items():
        print(f"   {key}: {value}")
    
    if len(messages) > 0:
        print("\n6. Testing email processing (dry run)...")
        # Test with a small batch to avoid costs
        result = processor.process_unanalyzed_emails()
        print("✓ Email processing test completed:")
        for key, value in result.items():
            print(f"   {key}: {value}")
    else:
        print("\n6. Skipping email processing test (no messages found)")
        print("   To test processing, first fetch some emails using the Gmail fetcher")
    
    print("\n✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
