import React from 'react';
import { Link } from 'react-router-dom';
import './TopMenu.css';

const TopMenu = () => {
  return (
    <nav className="top-menu">
      <div className="menu-logo">Genaigo</div>
      <div className="menu-items">
        <Link to="/" className="menu-item">Home</Link>
        <button className="menu-item">Dashboard</button>
        <button className="menu-item">Sources</button>
        <Link to="/settings" className="menu-item">Settings</Link>
      </div>
      <div>
        {/* Future user menu or other controls can go here */}
      </div>
    </nav>
  );
};

export default TopMenu;
