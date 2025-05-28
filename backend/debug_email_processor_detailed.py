#!/usr/bin/env python3

import os
import sys
import json

# Add the backend directory to the Python path
sys.path.append('/workspaces/genaigo/backend')

def debug_email_processor():
    """Debug EmailProcessor step by step."""
    
    print("1. Testing imports...")
    try:
        from app.services.email_processor import EmailProcessor
        print("✓ EmailProcessor imported successfully")
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return
    
    print("\n2. Testing EmailProcessor initialization...")
    try:
        processor = EmailProcessor()
        print("✓ EmailProcessor created successfully")
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n3. Testing get_analysis_stats...")
    try:
        stats = processor.get_analysis_stats()
        print(f"✓ Stats retrieved: {stats}")
    except Exception as e:
        print(f"✗ get_analysis_stats failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n4. Testing process_unanalyzed_emails...")
    try:
        result = processor.process_unanalyzed_emails()
        print(f"✓ Process result: {result}")
    except Exception as e:
        print(f"✗ process_unanalyzed_emails failed: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    debug_email_processor()
