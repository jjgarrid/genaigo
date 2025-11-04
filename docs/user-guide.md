# User Guide

This guide explains how to set up and use the GenAI Go Email Integration Platform.

## 🚀 Getting Started

This guide assumes you are running the application from a pre-built package or have completed the steps in the [Development Guide](development.md).

### 1. Start the Application
Use the recommended startup script, which handles everything from dependency installation to server startup.

-   **Linux/Mac**:
    ```bash
    ./start.sh
    ```
-   **Windows**:
    ```cmd
    start.bat
    ```
-   **Using npm**:
    ```bash
    npm run start
    ```

### 2. Access the Web Interface
Once the application is running, open your web browser and navigate to:
`http://localhost:5173`

### 3. Configure Gmail (First-Time Setup)
If this is your first time running the application, you will need to authorize it to access your Gmail account.

1.  From the project's root directory, run the guided setup script:
    ```bash
    npm run setup:gmail
    ```
2.  Follow the on-screen prompts, which will open a browser window for you to sign in to your Google account and grant the necessary permissions.
3.  Once authorized, the application will be ready to fetch emails.

## 🖥️ Web Interface

The web interface provides a complete dashboard for managing the Gmail integration.

### Gmail Integration Page
This is the main control center for the application, with four key tabs:

#### Overview Tab
-   **Status Panels**: At-a-glance status of the Gmail connection, message database, and scheduler.
-   **Manual Actions**: Buttons to trigger an immediate email fetch or to start/stop the automated scheduler.

#### Configuration Tab
-   **Current Settings**: A read-only view of the current configuration, including the sender whitelist, cron schedule, and other parameters.
-   **Setup Instructions**: Reminders on how to run the setup script if credentials are not configured.

#### Messages Tab
-   **Message List**: A searchable and sortable list of all emails that have been fetched and stored.
-   **Message Details**: Click on a message to view its full body content, sender, subject, and date.

#### Logs Tab
-   **Execution History**: A log of every time the scheduler has run, showing the outcome (e.g., `success`, `failure`) and how many messages were processed.

## ⚙️ Configuration

All configuration is managed through files located in the `config/` directory.

### Sender Whitelist
This is the most important setting. It's a list of email addresses that the application is allowed to fetch emails from. Any email not from a sender in this list will be ignored.

1.  Open `config/fetcherSettings.json`.
2.  Add or remove email addresses from the `sender_whitelist` array:
    ```json
    "sender_whitelist": [
      "alerts@my-service.com",
      "newsletter@company.com"
    ]
    ```
3.  The application will automatically apply the changes on the next scheduled run.

### Fetch Schedule
This setting controls how often the application automatically checks for new emails. It uses a standard cron expression.

1.  Open `config/fetcherSettings.json`.
2.  Modify the `schedule` value.
    -   `"0 2 * * *"`: Daily at 2:00 AM (default).
    -   `"0 */6 * * *"`: Every 6 hours.
    -   `"*/30 * * * *"`: Every 30 minutes.

## 🔒 Security and Data Privacy

-   **Local First**: All your data, including emails and credentials, is stored locally on your machine in the `data/` and `config/` directories.
-   **Read-Only Access**: The application only requests permission to read your emails. It will never modify, send, or delete anything in your Gmail account.
-   **Secure Authentication**: The connection to Gmail is secured using the industry-standard OAuth2 protocol.

##  troubleshooting

### "Gmail credentials not configured"
This means the application hasn't been authorized yet. Run `npm run setup:gmail` from the project root and follow the prompts.

### "No messages found"
This is usually due to one of the following:
-   The `sender_whitelist` in `config/fetcherSettings.json` is empty or doesn't contain the correct sender emails.
-   There are no new emails from whitelisted senders within the `lookback_hours` window (default is 24 hours).
-   There's an issue with your Gmail API connection. Check the application logs in your terminal for any error messages.
