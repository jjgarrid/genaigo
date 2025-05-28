import React, { createContext, useContext, useState, useEffect } from 'react';
import { API_BASE_ROOT } from '../config/api';

const ApiConfigContext = createContext();

const DEFAULT_API_URL = API_BASE_ROOT;
const STORAGE_KEY = 'genaigo_api_base_url';

// Helper function to sanitize API URL
const sanitizeApiUrl = (url) => {
  if (!url || typeof url !== 'string') {
    return DEFAULT_API_URL;
  }
  
  // Remove trailing slashes
  let sanitized = url.trim().replace(/\/+$/, '');
  
  // Ensure it starts with http:// or https://
  if (!sanitized.match(/^https?:\/\//)) {
    // If it doesn't start with a protocol, assume https
    sanitized = `https://${sanitized}`;
  }
  
  return sanitized;
};

export function ApiConfigProvider({ children }) {
  const [apiBaseUrl, setApiBaseUrl] = useState(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    return sanitizeApiUrl(stored) || DEFAULT_API_URL;
  });

  // Wrapper function that sanitizes the URL before setting it
  const setSanitizedApiBaseUrl = (url) => {
    const sanitized = sanitizeApiUrl(url);
    setApiBaseUrl(sanitized);
  };

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, apiBaseUrl);
  }, [apiBaseUrl]);

  return (
    <ApiConfigContext.Provider value={{ 
      apiBaseUrl, 
      setApiBaseUrl: setSanitizedApiBaseUrl,
      // Also expose the original setter for internal use if needed
      setApiBaseUrlRaw: setApiBaseUrl 
    }}>
      {children}
    </ApiConfigContext.Provider>
  );
}

export function useApiConfig() {
  return useContext(ApiConfigContext);
}
