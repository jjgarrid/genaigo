#!/usr/bin/env python3
"""
Complete OAuth2 setup with authorization code
"""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

def complete_oauth_setup(auth_code):
    """Complete OAuth2 setup with the provided authorization code."""
    
    # Load config
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
    gmail_config_path = os.path.join(config_dir, 'gmail.json')
    
    with open(gmail_config_path, 'r') as f:
        config = json.load(f)
        
    credentials_data = config.get('gmail_credentials', {})
    client_id = credentials_data.get('client_id')
    client_secret = credentials_data.get('client_secret')
    
    # Create OAuth2 flow
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8080"]
            }
        },
        scopes=['https://www.googleapis.com/auth/gmail.readonly']
    )
    
    flow.redirect_uri = "http://localhost:8080"
    
    try:
        # Exchange authorization code for tokens
        flow.fetch_token(code=auth_code)
        
        creds = flow.credentials
        
        # Test the credentials
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        print(f"✓ Success! Connected to Gmail account: {profile.get('emailAddress')}")
        
        # Save tokens to config
        credentials_data.update({
            'access_token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_expiry': creds.expiry.isoformat() if creds.expiry else None
        })
        
        config['gmail_credentials'] = credentials_data
        
        with open(gmail_config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print("✓ Tokens saved successfully!")
        print("✓ Gmail integration is now configured and ready to use.")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during authorization: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    print("Gmail OAuth2 Completion")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        auth_code = sys.argv[1]
    else:
        auth_code = input("Enter your authorization code: ").strip()
    
    if not auth_code:
        print("No authorization code provided.")
        sys.exit(1)
        
    success = complete_oauth_setup(auth_code)
    sys.exit(0 if success else 1)
