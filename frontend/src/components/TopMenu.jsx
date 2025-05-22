import React from 'react';
import { Link } from 'react-router-dom';
import './TopMenu.css';

const TopMenu = () => {
  return (
    <nav className="top-menu">
      <div className="menu-logo">Genaigo</div>
      <div className="menu-items">
        <button className="menu-item">Dashboard</button>
        <button className="menu-item">Sources</button>
        <button className="menu-item">Settings</button>
      </div>
      <div>
        <Link to="/" style={{ marginRight: 16 }}>Home</Link>
        <Link to="/settings">Settings</Link>
      </div>
    </nav>
  );
};

export default TopMenu;
