import React from 'react';
import PropTypes from 'prop-types';
import TopMenu from './TopMenu';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="layout-root">
      <TopMenu />
      <main className="main-content">
        <h1>Welcome to Genaigo Data Retrieval Platform</h1>
        <p>This is your main workspace. Future widgets and controls will appear here.</p>
        {children}
      </main>
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.node
};

export default Layout;
