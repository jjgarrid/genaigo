import React from 'react';
import Layout from '../components/Layout';
import TimeWidget from '../components/TimeWidget';

const LandingPage = () => {
  console.log("LandingPage rendering"); // Added for debugging
  return (
    <Layout 
      title="Welcome to Genaigo Data Retrieval Platform"
      subtitle="This is your main workspace. Future widgets and controls will appear here."
    >
      <TimeWidget />
    </Layout>
  );
};

export default LandingPage;
