import React from 'react';
import PropTypes from 'prop-types';
import TopMenu from './TopMenu';
import './Layout.css';

const Layout = ({ children, title, subtitle }) => {
  return (
    <div className="layout-root">
      <TopMenu />
      <main className="main-content">
        {title && <h1>{title}</h1>}
        {subtitle && <p>{subtitle}</p>}
        {children}
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
