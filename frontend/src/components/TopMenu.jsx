import React from 'react';
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
    </nav>
  );
};

export default TopMenu;
