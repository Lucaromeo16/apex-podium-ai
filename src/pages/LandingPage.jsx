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

      <section id="methodology" className="how-it-works-section">
        <div className="section-container">
          <div className="section-header">
            <h2>How It Works</h2>
            <p className="section-subtitle">A transparent, four-step approach to Formula 1 prediction</p>
          </div>
          <div className="how-it-works-grid">
            <div className="work-step-card">
              <div className="step-icon">1</div>
              <div className="step-content">
                <h3>Data Collection</h3>
                <p>We gathered historical Formula 1 race and qualifying data spanning multiple seasons (2016-2025), including results, grid positions, driver standings, and constructor information.</p>
              </div>
            </div>
            <div className="work-step-card">
              <div className="step-icon">2</div>
              <div className="step-content">
                <h3>Feature Engineering</h3>
                <p>Our model analyzes season-to-date driver form, constructor performance, prior podiums and wins, rolling results, and track-specific history to capture the factors that influence podium finishes.</p>
              </div>
            </div>
            <div className="work-step-card">
              <div className="step-icon">3</div>
              <div className="step-content">
                <h3>Walk-Forward Backtesting</h3>
                <p>We tested the system race-by-race across every event from 2021 through 2025, using only information available before each race. This ensures predictions reflect real-world conditions.</p>
              </div>
            </div>
            <div className="work-step-card">
              <div className="step-icon">4</div>
              <div className="step-content">
                <h3>2026 Forecasting</h3>
                <p>The platform separates completed races, canceled races, and upcoming events. It generates forward-looking predictions for the entire 2026 calendar with confidence probabilities.</p>
              </div>
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
