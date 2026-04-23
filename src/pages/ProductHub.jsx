import React from 'react';
import { Link } from 'react-router-dom';

function ProductHub() {
  return (
    <div className="hub-page">
      <nav className="page-nav">
        <Link to="/" className="nav-link">← Back to Home</Link>
      </nav>

      <div className="hub-content">
        <div className="hub-header">
          <h1>Explore ApexPodium AI</h1>
          <p>Choose your experience to dive into Formula 1 predictive analytics</p>
        </div>

        <div className="hub-cards">
          <div className="hub-card">
            <div className="card-content">
              <h2>2026 Predictor</h2>
              <p>View completed races, canceled races, and upcoming 2026 predictions. Explore our AI-powered forecasts for the current season using historical data and machine learning.</p>
              <Link to="/predictions" className="hub-cta">Explore 2026 Predictions</Link>
            </div>
          </div>

          <div className="hub-card">
            <div className="card-content">
              <h2>Historical Backtesting</h2>
              <p>Explore race-by-race backtesting results from 2021–2025. See how our ensemble model would have predicted past races using only pre-race data, with detailed performance metrics.</p>
              <Link to="/backtesting" className="hub-cta">View Backtest Results</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductHub;
