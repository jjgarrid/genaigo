import React from 'react';
import PropTypes from 'prop-types';
import Sidebar from './Sidebar';
import './Layout.css';

const Layout = ({ children, title, subtitle }) => {
  return (
    <div className="layout-root">
      <Sidebar />
      <main className="main-content">
        <div className="page-header">
          {title && <h1>{title}</h1>}
          {subtitle && <p className="subtitle">{subtitle}</p>}
        </div>
        <div className="content-area">
          {children}
        </div>
      </main>
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.node,
  title: PropTypes.string,
  subtitle: PropTypes.string
};

export default Layout;
