import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import './GmailPage.css';

const GmailPage = () => {
  const [gmailHealth, setGmailHealth] = useState(null);
  const [gmailConfig, setGmailConfig] = useState(null);
  const [gmailStats, setGmailStats] = useState(null);
  const [schedulerInfo, setSchedulerInfo] = useState(null);
  const [messages, setMessages] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  const apiBase = 'http://localhost:8000/api/gmail';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [healthRes, configRes, statsRes, schedulerRes] = await Promise.all([
        fetch(`${apiBase}/health`),
        fetch(`${apiBase}/config`),
        fetch(`${apiBase}/stats`),
        fetch(`${apiBase}/scheduler`)
      ]);

      setGmailHealth(await healthRes.json());
      setGmailConfig(await configRes.json());
      setGmailStats(await statsRes.json());
      setSchedulerInfo(await schedulerRes.json());
    } catch (err) {
      setError(`Failed to fetch data: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async () => {
    try {
      const response = await fetch(`${apiBase}/messages?limit=50`);
      const data = await response.json();
      setMessages(data);
    } catch (err) {
      setError(`Failed to fetch messages: ${err.message}`);
    }
  };

  const fetchLogs = async () => {
    try {
      const response = await fetch(`${apiBase}/scheduler/logs?limit=20`);
      const data = await response.json();
      setLogs(data);
    } catch (err) {
      setError(`Failed to fetch logs: ${err.message}`);
    }
  };

  const handleFetchNow = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${apiBase}/fetch`, { method: 'POST' });
      const result = await response.json();
      
      if (result.status === 'success') {
        alert(`Successfully processed ${result.processed} new messages`);
        fetchData();
        if (activeTab === 'messages') fetchMessages();
      } else {
        alert(`Fetch failed: ${result.message || 'Unknown error'}`);
      }
    } catch (err) {
      alert(`Fetch failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSchedulerToggle = async (action) => {
    try {
      const response = await fetch(`${apiBase}/scheduler/${action}`, { method: 'POST' });
      const result = await response.json();
      alert(result.message);
      fetchData();
    } catch (err) {
      alert(`Scheduler ${action} failed: ${err.message}`);
    }
  };

  useEffect(() => {
    if (activeTab === 'messages') {
      fetchMessages();
    } else if (activeTab === 'logs') {
      fetchLogs();
    }
  }, [activeTab]);

  const renderOverview = () => (
    <div className="overview-grid">
      <div className="card health-card">
        <h3>Gmail Connection</h3>
        <div className={`status ${gmailHealth?.configured ? 'healthy' : 'unhealthy'}`}>
          {gmailHealth?.configured ? '✓ Connected' : '⚠ Not Configured'}
        </div>
        {gmailHealth?.error && (
          <p className="error-text">{gmailHealth.error}</p>
        )}
      </div>

      <div className="card stats-card">
        <h3>Message Statistics</h3>
        <div className="stats-grid">
          <div className="stat">
            <span className="stat-label">Total Messages</span>
            <span className="stat-value">{gmailStats?.total_messages || 0}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Unique Senders</span>
            <span className="stat-value">{gmailStats?.unique_senders || 0}</span>
          </div>
        </div>
      </div>

      <div className="card scheduler-card">
        <h3>Scheduler Status</h3>
        <div className={`status ${schedulerInfo?.running ? 'running' : 'stopped'}`}>
          {schedulerInfo?.running ? '⏰ Running' : '⏸ Stopped'}
        </div>
        <p>Schedule: {schedulerInfo?.schedule || 'Not set'}</p>
        {schedulerInfo?.next_run_time && (
          <p>Next run: {new Date(schedulerInfo.next_run_time).toLocaleString()}</p>
        )}
        <div className="scheduler-controls">
          <button 
            onClick={() => handleSchedulerToggle('start')}
            disabled={schedulerInfo?.running}
            className="btn btn-primary"
          >
            Start
          </button>
          <button 
            onClick={() => handleSchedulerToggle('stop')}
            disabled={!schedulerInfo?.running}
            className="btn btn-secondary"
          >
            Stop
          </button>
        </div>
      </div>

      <div className="card actions-card">
        <h3>Manual Actions</h3>
        <button 
          onClick={handleFetchNow}
          disabled={loading || !gmailHealth?.configured}
          className="btn btn-primary"
        >
          {loading ? 'Fetching...' : 'Fetch Now'}
        </button>
        <button 
          onClick={fetchData}
          className="btn btn-secondary"
        >
          Refresh Data
        </button>
      </div>
    </div>
  );

  const renderConfiguration = () => (
    <div className="config-section">
      <div className="card">
        <h3>Current Configuration</h3>
        <div className="config-item">
          <strong>Credentials Configured:</strong> 
          <span className={gmailConfig?.credentials_configured ? 'text-success' : 'text-error'}>
            {gmailConfig?.credentials_configured ? 'Yes' : 'No'}
          </span>
        </div>
        <div className="config-item">
          <strong>Enabled:</strong> 
          <span>{gmailConfig?.settings?.enabled ? 'Yes' : 'No'}</span>
        </div>
        <div className="config-item">
          <strong>Schedule:</strong> 
          <span>{gmailConfig?.settings?.schedule}</span>
        </div>
        <div className="config-item">
          <strong>Lookback Hours:</strong> 
          <span>{gmailConfig?.settings?.lookback_hours}</span>
        </div>
        <div className="config-item">
          <strong>Sender Whitelist:</strong>
          <ul>
            {gmailConfig?.settings?.sender_whitelist?.map((sender, index) => (
              <li key={index}>{sender}</li>
            ))}
          </ul>
        </div>
      </div>
      
      {!gmailConfig?.credentials_configured && (
        <div className="card setup-instructions">
          <h3>Setup Instructions</h3>
          <ol>
            <li>Run <code>python backend/setup_gmail.py</code> to configure OAuth2 credentials</li>
            <li>Follow the prompts to authorize your Gmail account</li>
            <li>Refresh this page to verify the connection</li>
          </ol>
        </div>
      )}
    </div>
  );

  const renderMessages = () => (
    <div className="messages-section">
      <div className="messages-header">
        <h3>Recent Messages ({messages.length})</h3>
        <button onClick={fetchMessages} className="btn btn-secondary">
          Refresh
        </button>
      </div>
      <div className="messages-list">
        {messages.map((message, index) => (
          <div key={message.messageId || index} className="message-card">
            <div className="message-header">
              <strong>{message.subject}</strong>
              <span className="message-date">
                {new Date(message.retrievalTimestamp).toLocaleString()}
              </span>
            </div>
            <div className="message-meta">
              <span className="sender">From: {message.sender}</span>
              <span className="date">Date: {message.date}</span>
            </div>
            <div className="message-body">
              {message.body.substring(0, 200)}
              {message.body.length > 200 && '...'}
            </div>
          </div>
        ))}
        {messages.length === 0 && (
          <p className="no-data">No messages found</p>
        )}
      </div>
    </div>
  );

  const renderLogs = () => (
    <div className="logs-section">
      <div className="logs-header">
        <h3>Execution Logs ({logs.length})</h3>
        <button onClick={fetchLogs} className="btn btn-secondary">
          Refresh
        </button>
      </div>
      <div className="logs-list">
        {logs.map((log, index) => (
          <div key={index} className="log-entry">
            <div className="log-header">
              <span className="log-timestamp">
                {new Date(log.timestamp).toLocaleString()}
              </span>
              <span className={`log-status status-${log.result.status}`}>
                {log.result.status}
              </span>
            </div>
            <div className="log-details">
              {log.result.processed !== undefined && (
                <span>Processed: {log.result.processed}</span>
              )}
              {log.result.skipped !== undefined && (
                <span>Skipped: {log.result.skipped}</span>
              )}
              {log.result.total_found !== undefined && (
                <span>Found: {log.result.total_found}</span>
              )}
              {log.result.message && (
                <span className="error-message">Error: {log.result.message}</span>
              )}
            </div>
          </div>
        ))}
        {logs.length === 0 && (
          <p className="no-data">No logs found</p>
        )}
      </div>
    </div>
  );

  return (
    <Layout>
      <div className="gmail-page">
        <div className="page-header">
          <h1>Gmail Integration</h1>
          <p>Manage automated email fetching and monitoring</p>
        </div>

        {error && (
          <div className="error-banner">
            {error}
            <button onClick={() => setError(null)} className="close-btn">×</button>
          </div>
        )}

        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button 
            className={`tab ${activeTab === 'config' ? 'active' : ''}`}
            onClick={() => setActiveTab('config')}
          >
            Configuration
          </button>
          <button 
            className={`tab ${activeTab === 'messages' ? 'active' : ''}`}
            onClick={() => setActiveTab('messages')}
          >
            Messages
          </button>
          <button 
            className={`tab ${activeTab === 'logs' ? 'active' : ''}`}
            onClick={() => setActiveTab('logs')}
          >
            Logs
          </button>
        </div>

        <div className="tab-content">
          {loading && <div className="loading">Loading...</div>}
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'config' && renderConfiguration()}
          {activeTab === 'messages' && renderMessages()}
          {activeTab === 'logs' && renderLogs()}
        </div>
      </div>
    </Layout>
  );
};

export default GmailPage;
