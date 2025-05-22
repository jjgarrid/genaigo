import React, { createContext, useContext, useState, useEffect } from 'react';

const ApiConfigContext = createContext();

const DEFAULT_API_URL = 'https://automatic-chainsaw-9qwrgpw654xcpxjg-8001.app.github.dev';
const STORAGE_KEY = 'genaigo_api_base_url';

export function ApiConfigProvider({ children }) {
  const [apiBaseUrl, setApiBaseUrl] = useState(() => {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_API_URL;
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, apiBaseUrl);
  }, [apiBaseUrl]);

  return (
    <ApiConfigContext.Provider value={{ apiBaseUrl, setApiBaseUrl }}>
      {children}
    </ApiConfigContext.Provider>
  );
}

export function useApiConfig() {
  return useContext(ApiConfigContext);
}
