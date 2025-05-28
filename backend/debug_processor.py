#!/usr/bin/env python3

import os
import sys

# Add the backend directory to the Python path
sys.path.append('/workspaces/genaigo/backend')

def test_email_processor():
    """Test EmailProcessor initialization."""
    try:
        from app.services.email_processor import EmailProcessor
        
        print("Attempting to create EmailProcessor...")
        processor = EmailProcessor()
        print("EmailProcessor created successfully!")
        print(f"Processing settings: {processor.processing_settings}")
        
    except Exception as e:
        print(f"Error creating EmailProcessor: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email_processor()
