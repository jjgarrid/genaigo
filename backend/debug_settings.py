#!/usr/bin/env python3

import os
import json
import sys

# Add the backend directory to the Python path
sys.path.append('/workspaces/genaigo/backend')

def test_settings_path():
    """Test the settings path calculation."""
    
    # Simulate the path calculation from email_processor.py
    current_file = '/workspaces/genaigo/backend/app/services/email_processor.py'
    settings_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file)))),
        'config',
        'processingSettings.json'
    )
    
    print(f"Current file: {current_file}")
    print(f"Calculated settings path: {settings_path}")
    print(f"Path exists: {os.path.exists(settings_path)}")
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r') as f:
                content = f.read()
                print(f"File content length: {len(content)}")
                print(f"First 100 chars: {content[:100]}")
                
                # Try to parse JSON
                f.seek(0)
                data = json.load(f)
                print(f"JSON parsed successfully: {data}")
        except Exception as e:
            print(f"Error reading file: {e}")
    
    # Try the direct path
    direct_path = '/workspaces/genaigo/config/processingSettings.json'
    print(f"\nDirect path: {direct_path}")
    print(f"Direct path exists: {os.path.exists(direct_path)}")
    
    if os.path.exists(direct_path):
        try:
            with open(direct_path, 'r') as f:
                content = f.read()
                print(f"Direct file content length: {len(content)}")
                print(f"Direct first 100 chars: {content[:100]}")
                
                # Try to parse JSON
                f.seek(0)
                data = json.load(f)
                print(f"Direct JSON parsed successfully: {data}")
        except Exception as e:
            print(f"Error reading direct file: {e}")

if __name__ == "__main__":
    test_settings_path()
