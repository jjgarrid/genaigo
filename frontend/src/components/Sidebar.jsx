import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <h2>Genaigo</h2>
      </div>
      <nav className="sidebar-nav">
        <NavLink to="/" className="sidebar-link" activeClassName="active">
          Home
        </NavLink>
        <NavLink to="/gmail" className="sidebar-link" activeClassName="active">
          Gmail
        </NavLink>
        <NavLink to="/settings" className="sidebar-link" activeClassName="active">
          Settings
        </NavLink>
      </nav>
    </div>
  );
};

export default Sidebar;
