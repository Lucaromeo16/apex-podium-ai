import React from 'react';
import { Link } from 'react-router-dom';
import CountUp from 'react-countup';
import historicalData from '../data/historical_backtest.json';

function LandingPage() {
  const metrics = historicalData.summary_metrics;

  return (
    <div className="landing">
      <nav className="landing-nav">
        <div className="nav-brand">ApexPodium AI</div>
        <div className="nav-links">
          <a href="#about" className="nav-link">About Us</a>
          <a href="#methodology" className="nav-link">Methodology</a>
          <a href="#value" className="nav-link">Who It's For</a>
          <Link to="/app" className="nav-cta">Try ApexPodium AI</Link>
        </div>
      </nav>

      <section className="landing-hero">
        <h1 className="landing-title">ApexPodium AI</h1>
        <p className="landing-subtitle">AI-Powered Formula 1 Podium Prediction Platform</p>
        <p className="landing-description">
          Predict likely race outcomes using historical data and machine learning. 
          Our ensemble model analyzes qualifying performance, recent form, and track history 
          to forecast podium finishes for Formula 1 races.
        </p>
        <div className="hero-ctas">
          <Link to="/app" className="btn-primary">Try ApexPodium AI</Link>
          <a href="#methodology" className="btn-secondary">Learn More</a>
        </div>
      </section>

      <section className="metrics-strip">
        <div className="metric">
          <div className="metric-value">
            <CountUp 
              start={0} 
              end={metrics?.winner_hit_rate ?? 0} 
              duration={2.5}
              decimals={1}
              suffix="%"
              preserveValue={true}
            />
          </div>
          <div className="metric-label">Winner Hit Rate</div>
        </div>
        <div className="metric">
          <div className="metric-value">
            <CountUp 
              start={0} 
              end={metrics?.avg_top3_overlap ?? 0} 
              duration={2.5}
              decimals={2}
              preserveValue={true}
            />
          </div>
          <div className="metric-label">Avg. Correct Podium Drivers</div>
        </div>
        <div className="metric">
          <div className="metric-value">
            <CountUp 
              start={0} 
              end={metrics?.races_with_2plus_correct ?? 0} 
              duration={2.5}
              decimals={1}
              suffix="%"
              preserveValue={true}
            />
          </div>
          <div className="metric-label">Races With 2+ Correct Podium Picks</div>
        </div>
      </section>

      <section id="about" className="landing-section">
        <div className="section-container">
          <h2>About Us</h2>
          <p>
            ApexPodium AI is a Formula 1 predictive analytics product that forecasts likely race outcomes. 
            It combines machine learning, historical race performance, and season-to-date trends to make F1 data 
            more interpretable and engaging. Our platform transforms complex race data into actionable predictions 
            that help fans and analysts understand the factors driving podium finishes.
          </p>
        </div>
      </section>

      <section className="features-section">
        <div className="section-container">
          <h2>Key Features</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>Historical Backtesting</h3>
              <p>Race-by-race analysis of model performance across 2021-2025 seasons using only pre-race data.</p>
            </div>
            <div className="feature-card">
              <h3>2026 Forecasting</h3>
              <p>Live predictions for upcoming races, separating completed, canceled, and future events.</p>
            </div>
            <div className="feature-card">
              <h3>Race-by-Race Predictions</h3>
              <p>Detailed podium predictions with probability scores for each driver and constructor.</p>
            </div>
            <div className="feature-card">
              <h3>Transparent Methodology</h3>
              <p>Clear explanation of our ensemble modeling approach and performance metrics.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="methodology" className="landing-section">
        <div className="section-container">
          <h2>Methodology</h2>
          <div className="methodology-steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Data Collection</h3>
              <p>Historical Formula 1 race data from 2016-2025, including results, qualifying, and driver standings.</p>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Feature Engineering</h3>
              <p>Recent driver form, constructor performance, prior podiums/wins, track history, and season-to-date indicators.</p>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Ensemble Modeling</h3>
              <p>Logistic regression, random forest, and XGBoost models trained and validated through chronological backtesting.</p>
            </div>
            <div className="step">
              <div className="step-number">4</div>
              <h3>Backtesting Validation</h3>
              <p>Race-by-race testing across 2021-2025 using only information available before each race.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="value" className="landing-section">
        <div className="section-container">
          <h2>Who It's For</h2>
          <div className="value-grid">
            <div className="value-card">
              <h3>Formula 1 Fans</h3>
              <p>Enhance your race weekend experience with data-driven insights into likely outcomes.</p>
            </div>
            <div className="value-card">
              <h3>Sports Analytics Enthusiasts</h3>
              <p>Explore how machine learning can predict complex sporting events with real-world data.</p>
            </div>
            <div className="value-card">
              <h3>Students & Researchers</h3>
              <p>Learn predictive modeling through a practical application in motorsport analytics.</p>
            </div>
            <div className="value-card">
              <h3>Data-Driven Forecasters</h3>
              <p>Access transparent, backtested predictions for informed race outcome analysis.</p>
            </div>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <h3>ApexPodium AI</h3>
            <p>AI-powered Formula 1 podium predictions</p>
          </div>
          <div className="footer-links">
            <Link to="/predictions">2026 Predictions</Link>
            <Link to="/backtesting">Historical Backtesting</Link>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2026 ApexPodium AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;
