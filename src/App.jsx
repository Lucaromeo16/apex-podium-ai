import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import AppHub from './pages/AppHub';
import PredictionsPage from './pages/PredictionsPage';
import BacktestingPage from './pages/BacktestingPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/app" element={<AppHub />} />
        <Route path="/predictions" element={<PredictionsPage />} />
        <Route path="/backtesting" element={<BacktestingPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
