import React from 'react';
import { Link } from 'react-router-dom';

function AppHub() {
  return (
    <div className="landing">
      <nav className="landing-nav">
        <div className="nav-brand">ApexPodium AI</div>
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
        </div>
      </nav>

      <div className="landing-hero" style={{ paddingBottom: '2rem', minHeight: '40vh' }}>
        <h1 className="landing-title">ApexPodium AI</h1>
        <p className="landing-subtitle">Explore Our Prediction Tools</p>
        <p className="landing-description">
          Choose between live 2026 race predictions or review our historical backtesting analysis.
        </p>
      </div>

      <div className="landing-cards">
        <Link to="/predictions" className="landing-card predictions-card">
          <div className="card-content">
            <h2>2026 Predictions</h2>
            <p>View live predictions for upcoming Formula 1 races using our ensemble model trained on qualifying, grid position, recent form, reliability, and track history.</p>
            <div className="card-cta">Explore Predictions →</div>
          </div>
        </Link>

        <Link to="/backtesting" className="landing-card backtesting-card">
          <div className="card-content">
            <h2>Historical Backtesting</h2>
            <p>See how our model would have predicted past races using only pre-race data. Review performance metrics and detailed race-by-race analysis.</p>
            <div className="card-cta">View Backtest Results →</div>
          </div>
        </Link>
      </div>

      <div className="landing-footer">
        <p>ApexPodium AI uses machine learning to predict Formula 1 podium finishes with historical accuracy and precision metrics.</p>
      </div>
    </div>
  );
}

export default AppHub;
