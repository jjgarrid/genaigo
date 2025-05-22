import React, { useState, useEffect } from 'react';
import './TimeWidget.css';
import { useApiConfig } from '../contexts/ApiConfigContext';

const TimeWidget = () => {
  console.log('TimeWidget rendering'); // Keep this for debugging
  const [serverTime, setServerTime] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { apiBaseUrl } = useApiConfig();

  const fetchServerTime = async () => {
    console.log('Fetching server time...'); // Keep this for debugging
    try {
      setLoading(true);
      // Use remote backend URL for fetch
      const response = await fetch(`${apiBaseUrl}/api/time`); 
      
      if (!response.ok) {
        console.error('Fetch error:', response.status, response.statusText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Received time data:', data); // Keep this for debugging
      setServerTime(data.time);
      setError(null);
    } catch (err) {
      console.error('Error in fetchServerTime:', err);
      setError(`Failed to fetch server time: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (isoTimeString) => {
    if (!isoTimeString) return 'Not available';
    try {
      const date = new Date(isoTimeString);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
      }).format(date);
    } catch (err) {
      console.error('Error formatting time:', err);
      return `Invalid date: ${isoTimeString}`;
    }
  };

  useEffect(() => {
    console.log('TimeWidget useEffect running'); // Keep this for debugging
    fetchServerTime();
    const intervalId = setInterval(fetchServerTime, 10000);
    return () => {
      console.log('TimeWidget cleaning up interval'); // Keep this for debugging
      clearInterval(intervalId);
    };
  }, []);

  // Added explicit border for visibility during debugging
  return (
    <div className="time-widget" style={{ border: '3px solid blue', padding: '15px', margin: '15px' }}> 
      <h3>Server Time</h3>
      {loading && <p className="loading">Loading server time...</p>}
      {error && <p className="error">Error: {error}</p>}
      {serverTime && !loading && !error && (
        <div className="time-display">
          <p>{formatTime(serverTime)}</p>
          <p className="iso-time">ISO: {serverTime}</p>
        </div>
      )}
      {!serverTime && !loading && !error && (
         <p>No time data available.</p>
      )}
    </div>
  );
};

export default TimeWidget;
