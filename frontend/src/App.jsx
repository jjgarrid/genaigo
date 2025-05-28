import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage'; // Changed back from StaticTestApp
import SettingsPage from './pages/SettingsPage';
import GmailPage from './pages/GmailPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="/gmail" element={<GmailPage />} />
      </Routes>
    </Router>
  );
}

export default App;
