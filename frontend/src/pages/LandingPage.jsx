import React from 'react';
import Layout from '../components/Layout';
import TimeWidget from '../components/TimeWidget';

const LandingPage = () => {
  console.log("LandingPage rendering"); // Added for debugging
  return (
    <Layout>
      <TimeWidget />
    </Layout>
  );
};

export default LandingPage;
