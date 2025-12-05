import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Playground from './pages/Playground';
import LiveStream from './pages/LiveStream';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/playground" element={<Playground />} />
        <Route path="/live" element={<LiveStream />} />
      </Routes>
    </Router>
  );
}

export default App;
