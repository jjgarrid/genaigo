// Environment-aware API configuration
const getApiBase = () => {
  // Check if we're in a GitHub Codespace
  if (window.location.hostname.includes('app.github.dev')) {
    // Extract the backend URL from the current frontend URL
    const currentUrl = window.location.hostname;
    // Replace the port number from 5173 to 8000
    const backendUrl = currentUrl.replace('-5173.app.github.dev', '-8000.app.github.dev');
    return `https://${backendUrl}/api/gmail`;
  }
  
  // Check if we're in a local development environment
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000/api/gmail';
  }
  
  // Default fallback
  return 'http://localhost:8000/api/gmail';
};

export const API_BASE = getApiBase();
export const API_BASE_ROOT = getApiBase().replace('/api/gmail', '');

// For debugging
console.log('Frontend URL:', window.location.href);
console.log('API Base URL:', API_BASE);
console.log('API Root URL:', API_BASE_ROOT);
