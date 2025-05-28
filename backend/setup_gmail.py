#!/usr/bin/env python3
"""
Gmail OAuth2 Setup Script

This script helps you set up OAuth2 credentials for Gmail API access.
You need to:
1. Create a project in Google Cloud Console
2. Enable Gmail API
3. Create OAuth2 credentials (desktop application)
4. Run this script to get tokens

Prerequisites:
- Google Cloud project with Gmail API enabled
- OAuth2 client credentials (client_id and client_secret)
"""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Gmail API scope for read-only access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def setup_gmail_credentials():
    """Set up Gmail OAuth2 credentials."""
    
    config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
    gmail_config_path = os.path.join(config_dir, 'gmail.json')
    
    print("Gmail OAuth2 Setup")
    print("=" * 50)
    print()
    
    # Check if config file exists
    if not os.path.exists(gmail_config_path):
        print(f"Config file not found at {gmail_config_path}")
        print("Please create the config file first.")
        return
        
    # Load existing config
    with open(gmail_config_path, 'r') as f:
        config = json.load(f)
        
    credentials_data = config.get('gmail_credentials', {})
    
    # Get client credentials
    client_id = credentials_data.get('client_id')
    client_secret = credentials_data.get('client_secret')
    
    if not client_id or not client_secret:
        print("Missing client_id or client_secret in config file.")
        print()
        print("To get these credentials:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Create a new project or select an existing one")
        print("3. Enable the Gmail API")
        print("4. Go to 'Credentials' and create OAuth 2.0 Client IDs")
        print("5. Choose 'Desktop application' as the application type")
        print("6. Copy the client_id and client_secret to gmail.json")
        print()
        
        client_id = input("Enter your client_id: ").strip()
        client_secret = input("Enter your client_secret: ").strip()
        
        if not client_id or not client_secret:
            print("Invalid credentials provided.")
            return
            
        # Update config
        credentials_data['client_id'] = client_id
        credentials_data['client_secret'] = client_secret
        config['gmail_credentials'] = credentials_data
        
        with open(gmail_config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print("Credentials saved to config file.")
        print()
    
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
        scopes=SCOPES
    )
    
    flow.redirect_uri = "http://localhost:8080"
    
    # Get authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print("Authorization required:")
    print(f"1. Open this URL in your browser: {auth_url}")
    print("2. Complete the authorization process")
    print("3. Copy the authorization code from the redirect URL")
    print()
    
    auth_code = input("Enter the authorization code: ").strip()
    
    if not auth_code:
        print("No authorization code provided.")
        return
        
    try:
        # Exchange authorization code for tokens
        flow.fetch_token(code=auth_code)
        
        creds = flow.credentials
        
        # Test the credentials
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        print(f"Success! Connected to Gmail account: {profile.get('emailAddress')}")
        
        # Save tokens to config
        credentials_data.update({
            'access_token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_expiry': creds.expiry.isoformat() if creds.expiry else None
        })
        
        config['gmail_credentials'] = credentials_data
        
        with open(gmail_config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
        print("Tokens saved successfully!")
        print()
        print("Gmail integration is now configured and ready to use.")
        
    except Exception as e:
        print(f"Error during authorization: {e}")
        return

if __name__ == "__main__":
    setup_gmail_credentials()
