import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { ApiConfigProvider } from './contexts/ApiConfigContext';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ApiConfigProvider>
      <App />
    </ApiConfigProvider>
  </React.StrictMode>
);
