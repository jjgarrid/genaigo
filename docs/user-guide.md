# User Guide

## Getting Started

### Prerequisites
- Gmail account
- Web browser (Chrome, Firefox, Safari, or Edge)

### Initial Setup

1. **Start the Application**
   - Run the startup script:
     - Linux/Mac: `./start.sh`
     - Windows: `start.bat`
   - Or use npm: `npm run start`

2. **Configure Gmail Integration**
   - Open the web interface at http://localhost:5173
   - Navigate to the Gmail page
   - If credentials are not configured, follow the setup instructions:
     - Run `python backend/setup_gmail.py` from the project root
     - Follow the OAuth2 authorization process
     - The application will automatically fetch emails based on your configuration

## Web Interface

### Dashboard
The main dashboard shows:
- Current system time
- Quick access to different sections

### Gmail Integration Page
This page provides comprehensive Gmail integration management:

#### Overview Tab
- **Gmail Connection Status**: Shows if the Gmail API is properly connected
- **Message Statistics**: Displays total messages and unique senders
- **Scheduler Status**: Shows if the automated scheduler is running
- **Manual Actions**: Allows you to manually fetch emails or refresh data

#### Configuration Tab
- **Current Configuration**: Displays your current settings
- **Sender Whitelist**: Shows which email addresses are being monitored
- **Schedule**: Displays the current fetch schedule (cron format)
- **Setup Instructions**: If credentials aren't configured, shows how to set them up

#### Messages Tab
- **Recent Messages**: Displays the most recently fetched emails
- **Message Details**: Shows subject, sender, date, and a preview of the body

#### Logs Tab
- **Execution Logs**: Shows the history of email fetch operations
- **Status Information**: Displays success/failure status and processing statistics

### Settings Page
- Configure application settings
- Manage API connections
- Adjust fetch parameters

## Configuration

### Sender Whitelist
The sender whitelist determines which emails are fetched from your Gmail account. Only emails from addresses in this list will be processed.

To modify the whitelist:
1. Edit `config/fetcherSettings.json`
2. Add or remove email addresses from the `sender_whitelist` array
3. Restart the application or refresh the configuration via the web interface

### Fetch Schedule
The fetch schedule determines how often the application checks for new emails. It uses cron format:

- `0 2 * * *` - Daily at 2:00 AM (default)
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 0` - Weekly on Sunday at midnight

To modify the schedule:
1. Edit `config/fetcherSettings.json`
2. Change the `schedule` value to your desired cron expression
3. Restart the application or refresh the configuration via the web interface

### Lookback Period
The lookback period determines how far back in time the application will search for emails.

To modify the lookback period:
1. Edit `config/fetcherSettings.json`
2. Change the `lookback_hours` value (default: 24)
3. Restart the application or refresh the configuration via the web interface

## Manual Operations

### Manual Fetch
To manually fetch emails:
1. Navigate to the Gmail page
2. Go to the Overview tab
3. Click the "Fetch Now" button
4. The application will immediately check for new emails

### Scheduler Control
To start or stop the automated scheduler:
1. Navigate to the Gmail page
2. Go to the Overview tab
3. Use the Start/Stop buttons in the Scheduler Status section

## Troubleshooting

### Common Issues

#### "Gmail credentials not configured"
- Run `python backend/setup_gmail.py` to configure OAuth2 credentials
- Follow the authorization process in your web browser

#### "No messages found"
- Check that your sender whitelist includes addresses that have sent you emails
- Verify that emails exist in the specified time range
- Check Gmail API quota limits if this is a recurring issue

#### "Port already in use"
- The startup script should automatically kill existing processes
- If issues persist, manually kill processes using ports 8000 and 5173:
  - Linux/Mac: `pkill -f "uvicorn|vite"`
  - Windows: Use Task Manager to end processes

### Checking Logs
- **Application Logs**: Visible in the terminal where you started the application
- **Execution Logs**: Available in the Logs tab of the Gmail page
- **Data Storage**: Check `data/messages.json` for stored email data

## Data Management

### Stored Data
Email data is stored in `data/messages.json` in JSON format. Each email includes:
- Message ID
- Subject
- Sender
- Date
- Retrieval timestamp
- Body content
- Body hash (for deduplication)

### Data Privacy
- All data is stored locally on your machine
- No data is transmitted to external servers
- Gmail access is read-only
- Emails remain unchanged in your Gmail account

## Security

### OAuth2 Authentication
The application uses secure OAuth2 authentication with Google:
- Minimal permissions (read-only access to Gmail)
- Tokens are stored locally
- Automatic token refresh when needed

### Data Protection
- All data remains on your local machine
- Configuration files contain sensitive information and should be protected
- The application does not modify your Gmail messages