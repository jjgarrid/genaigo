import React, { useState } from 'react';
import { useApiConfig } from '../contexts/ApiConfigContext';
import Layout from '../components/Layout';

const SettingsPage = () => {
  const { apiBaseUrl, setApiBaseUrl } = useApiConfig();
  const [value, setValue] = useState(apiBaseUrl);
  const [saved, setSaved] = useState(false);

  // Helper function to sanitize URL (same as in context)
  const sanitizeApiUrl = (url) => {
    if (!url || typeof url !== 'string') {
      return '';
    }
    
    // Remove trailing slashes
    let sanitized = url.trim().replace(/\/+$/, '');
    
    // Ensure it starts with http:// or https://
    if (sanitized && !sanitized.match(/^https?:\/\//)) {
      // If it doesn't start with a protocol, assume https
      sanitized = `https://${sanitized}`;
    }
    
    return sanitized;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setApiBaseUrl(value);
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  const previewUrl = sanitizeApiUrl(value);
  const fullExampleUrl = previewUrl ? `${previewUrl}/api/time` : '';

  return (
    <Layout title="Settings">
      <div style={{ maxWidth: 500, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px #0001' }}>
        <form onSubmit={handleSubmit}>
          <label htmlFor="api-url" style={{ fontWeight: 'bold' }}>Backend API Base URL:</label>
          <input
            id="api-url"
            type="text"
            value={value}
            onChange={e => setValue(e.target.value)}
            style={{ width: '100%', margin: '12px 0', padding: 8, fontSize: 16 }}
            placeholder="https://your-backend-url.app.github.dev"
          />
          
          {/* URL Preview */}
          {previewUrl && (
            <div style={{ margin: '8px 0', padding: '8px', background: '#f5f5f5', borderRadius: 4, fontSize: 14 }}>
              <strong>Sanitized URL:</strong> <code style={{ color: '#0066cc' }}>{previewUrl}</code>
              <br />
              <strong>Time endpoint:</strong> <code style={{ color: '#666' }}>{fullExampleUrl}</code>
            </div>
          )}
          
          <button type="submit" style={{ padding: '8px 20px', fontSize: 16 }}>Save</button>
          {saved && <span style={{ color: 'green', marginLeft: 16 }}>Saved!</span>}
        </form>
        
        <div style={{ marginTop: 20, padding: 12, background: '#fff3cd', borderRadius: 4, fontSize: 13 }}>
          <strong>💡 Tips:</strong>
          <ul style={{ margin: '8px 0', paddingLeft: 20 }}>
            <li>Don't include trailing slashes (/) - they will be automatically removed</li>
            <li>Don't include the endpoint path (/api/time) - it's added automatically</li>
            <li>Protocol (https://) will be added if missing</li>
          </ul>
        </div>
        
        <p style={{ fontSize: 13, color: '#666', marginTop: 16 }}>
          Example: <code>https://automatic-chainsaw-9qwrgpw654xcpxjg-8001.app.github.dev</code>
        </p>
      </div>
    </Layout>
  );
};

export default SettingsPage;
