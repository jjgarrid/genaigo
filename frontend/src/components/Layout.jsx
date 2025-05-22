import React from 'react';
import TopMenu from './TopMenu';
import './Layout.css';

const Layout = () => {
  return (
    <div className="layout-root">
      <TopMenu />
      <main className="main-content">
        <h1>Welcome to Genaigo Data Retrieval Platform</h1>
        <p>This is your main workspace. Future widgets and controls will appear here.</p>
      </main>
    </div>
  );
};

export default Layout;
