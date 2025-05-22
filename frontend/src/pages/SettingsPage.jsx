import React, { useState } from 'react';
import { useApiConfig } from '../contexts/ApiConfigContext';

const SettingsPage = () => {
  const { apiBaseUrl, setApiBaseUrl } = useApiConfig();
  const [value, setValue] = useState(apiBaseUrl);
  const [saved, setSaved] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setApiBaseUrl(value);
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', padding: 24, background: '#fff', borderRadius: 8, boxShadow: '0 2px 8px #0001' }}>
      <h2>Settings</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="api-url" style={{ fontWeight: 'bold' }}>Backend API Base URL:</label>
        <input
          id="api-url"
          type="text"
          value={value}
          onChange={e => setValue(e.target.value)}
          style={{ width: '100%', margin: '12px 0', padding: 8, fontSize: 16 }}
        />
        <button type="submit" style={{ padding: '8px 20px', fontSize: 16 }}>Save</button>
        {saved && <span style={{ color: 'green', marginLeft: 16 }}>Saved!</span>}
      </form>
      <p style={{ fontSize: 13, color: '#666', marginTop: 16 }}>
        Example: <code>https://automatic-chainsaw-9qwrgpw654xcpxjg-8001.app.github.dev</code>
      </p>
    </div>
  );
};

export default SettingsPage;
