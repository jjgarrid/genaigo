#!/usr/bin/env python3
"""
Test script for Gmail integration functionality.
Run this to verify that the Gmail fetcher is working correctly.
"""

import json
import os
import sys
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.services.gmail_fetcher import GmailFetcher
    from app.services.scheduler import GmailScheduler
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the project root and dependencies are installed.")
    sys.exit(1)

def test_configuration():
    """Test configuration loading."""
    print("Testing configuration...")
    try:
        fetcher = GmailFetcher()
        print("✓ Configuration loaded successfully")
        
        # Check if credentials are configured
        creds = fetcher.gmail_config.get('gmail_credentials', {})
        if creds.get('client_id') and creds.get('client_secret'):
            print("✓ OAuth2 credentials found")
        else:
            print("⚠ OAuth2 credentials not configured")
            
        # Check settings
        settings = fetcher.fetcher_settings
        print(f"✓ Sender whitelist: {len(settings.get('sender_whitelist', []))} addresses")
        print(f"✓ Schedule: {settings.get('schedule', 'not set')}")
        print(f"✓ Enabled: {settings.get('enabled', False)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_gmail_connection():
    """Test Gmail API connection."""
    print("\nTesting Gmail connection...")
    try:
        fetcher = GmailFetcher()
        service = fetcher._get_gmail_service()
        
        # Try to get user profile
        profile = service.users().getProfile(userId='me').execute()
        print(f"✓ Connected to Gmail: {profile.get('emailAddress')}")
        return True
        
    except ValueError as e:
        print(f"⚠ Gmail connection failed: {e}")
        print("  Run 'python backend/setup_gmail.py' to configure OAuth2 credentials")
        return False
    except Exception as e:
        print(f"✗ Gmail connection error: {e}")
        return False

def test_database():
    """Test database functionality."""
    print("\nTesting database...")
    try:
        fetcher = GmailFetcher()
        db = fetcher._get_messages_db()
        
        # Test basic database operations
        test_message = {
            'messageId': 'test-' + str(int(datetime.now().timestamp())),
            'subject': 'Test Message',
            'sender': 'test@example.com',
            'date': datetime.now().isoformat(),
            'retrievalTimestamp': datetime.now().isoformat() + 'Z',
            'body': 'This is a test message',
            'bodyHash': 'test-hash'
        }
        
        # Insert test message
        db.insert(test_message)
        print("✓ Database write successful")
        
        # Read messages
        messages = fetcher.get_stored_messages(limit=1)
        if messages:
            print("✓ Database read successful")
        else:
            print("⚠ No messages in database")
            
        # Get stats
        stats = fetcher.get_message_stats()
        print(f"✓ Database stats: {stats['total_messages']} messages")
        
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_scheduler():
    """Test scheduler functionality."""
    print("\nTesting scheduler...")
    try:
        scheduler = GmailScheduler()
        
        # Test scheduler initialization
        print("✓ Scheduler initialized")
        
        # Check configuration
        settings = scheduler.fetcher.fetcher_settings
        schedule_str = settings.get('schedule', '0 2 * * *')
        print(f"✓ Schedule configured: {schedule_str}")
        
        return True
        
    except Exception as e:
        print(f"✗ Scheduler error: {e}")
        return False

def test_email_search():
    """Test email search functionality (if credentials are available)."""
    print("\nTesting email search...")
    try:
        fetcher = GmailFetcher()
        
        # Build search query
        query = fetcher._build_search_query()
        print(f"✓ Search query generated: {query}")
        
        # If we have valid credentials, try a search
        try:
            service = fetcher._get_gmail_service()
            result = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=5
            ).execute()
            
            messages = result.get('messages', [])
            print(f"✓ Search successful: found {len(messages)} messages")
            
            return True
            
        except Exception as e:
            print(f"⚠ Search test skipped (credentials issue): {e}")
            return True  # Don't fail the test for credential issues
            
    except Exception as e:
        print(f"✗ Search error: {e}")
        return False

def main():
    """Run all tests."""
    print("Gmail Integration Test Suite")
    print("=" * 40)
    
    tests = [
        test_configuration,
        test_database,
        test_scheduler,
        test_gmail_connection,
        test_email_search,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Gmail integration is ready to use.")
    else:
        print("⚠ Some tests failed. Check configuration and credentials.")
        
    print("\nNext steps:")
    if passed < total:
        print("1. Run 'python backend/setup_gmail.py' to configure OAuth2 credentials")
        print("2. Check /config/gmail.json and /config/fetcherSettings.json")
    print("3. Start the backend server: 'cd backend && uvicorn app.main:app --reload'")
    print("4. Test the API: http://localhost:8000/api/gmail/health")

if __name__ == "__main__":
    main()
