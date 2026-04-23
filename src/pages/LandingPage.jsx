import React from 'react';
import { Link } from 'react-router-dom';
import CountUp from 'react-countup';
import historicalData from '../data/historical_backtest.json';
import featureImportanceData from '../data/feature_importance.json';

function LandingPage() {
  const metrics = historicalData.summary_metrics;
  const featureImportance = featureImportanceData;

  return (
    <div className="landing">
      <nav className="landing-nav">
        <div className="nav-brand">ApexPodium AI</div>
        <div className="nav-links">
          <a href="#about" className="nav-link">About Us</a>
          <a href="#methodology" className="nav-link">Methodology</a>
          <a href="#value" className="nav-link">Who It's For</a>
          <a href="#model-architecture" className="nav-link">Model Architecture</a>
          <a href="#feature-importance" className="nav-link">Feature Importance</a>
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
        <p className="course-concepts-note">
          The modeling approach builds directly on course concepts including linear models, 
          decision trees, and ensemble methods, adapted for a classification-based prediction problem.
        </p>
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
                <p>We engineered features based on prior performance, team strength, rolling form, and track-specific history to capture the factors most relevant to predicting podium finishes.</p>
              </div>
            </div>
            <div className="work-step-card">
              <div className="step-icon">3</div>
              <div className="step-content">
                <h3>Walk-Forward Backtesting</h3>
                <p>We tested the system race-by-race across every event from 2021 through 2025 using only information available before each race. This walk-forward approach ensures realistic evaluation and helps avoid overfitting.</p>
              </div>
            </div>
            <div className="work-step-card">
              <div className="step-icon">4</div>
              <div className="step-content">
                <h3>2026 Forecasting</h3>
                <p>The platform separates completed races, canceled races, and upcoming events. It generates forward-looking predictions for the entire 2026 calendar using the trained ensemble model.</p>
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

      <section id="model-architecture" className="model-architecture-section">
        <div className="section-container">
          <div className="section-header">
            <h2>Model Architecture</h2>
            <p className="section-subtitle">Four machine learning techniques working together to predict podium finishes</p>
          </div>
          <div className="technique-grid">
            <div className="technique-card">
              <div className="technique-header">
                <span className="technique-number">01</span>
                <h3>Logistic Regression</h3>
              </div>
              <div className="technique-content">
                <p className="technique-role">Role: Linear Baseline Model</p>
                <p className="technique-description">
                  A supervised linear model adapted for classification. It estimates the probability 
                  of a binary outcome by applying a logistic function to a linear combination of features.
                  Particularly effective for structured tabular data where relationships can be approximated linearly.
                </p>
                <div className="technique-strengths">
                  <h4>Strengths</h4>
                  <ul>
                    <li>Highly interpretable — coefficients reveal feature importance</li>
                    <li>Stable predictions with well-calibrated probabilities</li>
                    <li>Excellent baseline for comparing more complex models</li>
                    <li>Computationally efficient and resistant to overfitting</li>
                  </ul>
                </div>
                <p className="technique-why">
                  Used as a stable baseline to establish how well simpler approaches perform 
                  before introducing more complex techniques.
                </p>
              </div>
            </div>

            <div className="technique-card">
              <div className="technique-header">
                <span className="technique-number">02</span>
                <h3>Random Forest</h3>
              </div>
              <div className="technique-content">
                <p className="technique-role">Role: Tree-Based Ensemble</p>
                <p className="technique-description">
                  A tree-based ensemble method that builds multiple decision trees during training 
                  and outputs the mode (for classification) of predictions from all trees. 
                  Excels at capturing nonlinear relationships and feature interactions.
                </p>
                <div className="technique-strengths">
                  <h4>Strengths</h4>
                  <ul>
                    <li>Learns complex conditional patterns without explicit feature engineering</li>
                    <li>Robust to outliers and missing data</li>
                    <li>Reduces overfitting through tree averaging (bagging)</li>
                    <li>Captures feature interactions that linear models miss</li>
                  </ul>
                </div>
                <p className="technique-why">
                  Provides flexibility to model nonlinear patterns in driver performance, 
                  constructor form, and track-specific characteristics.
                </p>
              </div>
            </div>

            <div className="technique-card">
              <div className="technique-header">
                <span className="technique-number">03</span>
                <h3>Gradient Boosting (XGBoost)</h3>
              </div>
              <div className="technique-content">
                <p className="technique-role">Role: Boosted Tree-Based Method</p>
                <p className="technique-description">
                  A gradient boosting method that builds trees sequentially, with each new tree 
                  correcting errors made by previous ones. XGBoost is a highly optimized 
                  implementation known for strong performance on tabular data.
                </p>
                <div className="technique-strengths">
                  <h4>Strengths</h4>
                  <ul>
                    <li>Captures refined nonlinear patterns and subtle interactions</li>
                    <li>Built-in regularization helps prevent overfitting</li>
                    <li>Often outperforms other methods on structured datasets</li>
                    <li>Handles sparse features efficiently</li>
                  </ul>
                </div>
                <p className="technique-why">
                  Included as a modern, high-performance approach that brings additional 
                  predictive power to the ensemble through iterative error refinement.
                </p>
              </div>
            </div>

            <div className="technique-card ensemble-card">
              <div className="technique-header">
                <span className="technique-number">04</span>
                <h3>Ensemble Model</h3>
              </div>
              <div className="technique-content">
                <p className="technique-role">Role: Weighted Combination</p>
                <p className="technique-description">
                  A weighted combination of multiple models designed to improve robustness 
                  and generalization by reducing dependence on any single model's assumptions or biases.
                </p>
                <div className="ensemble-weights">
                  <h4>Final Ensemble Weights</h4>
                  <div className="weight-item">
                    <span className="weight-label">Logistic Regression</span>
                    <span className="weight-value">50%</span>
                  </div>
                  <div className="weight-item">
                    <span className="weight-label">Random Forest</span>
                    <span className="weight-value">30%</span>
                  </div>
                  <div className="weight-item">
                    <span className="weight-label">XGBoost</span>
                    <span className="weight-value">20%</span>
                  </div>
                </div>
                <p className="technique-why ensemble-note">
                  This weighted blend combines the stability of a linear model, the nonlinear 
                  learning of tree-based methods, and the refined predictions from boosting 
                  for balanced, reliable podium predictions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="feature-importance" className="feature-importance-section">
        <div className="section-container">
          <div className="section-header">
            <h2>Feature Importance</h2>
            <p className="section-subtitle">What drives our predictions? Insights from {featureImportance.model_used}</p>
          </div>
          <p className="feature-importance-description">
            These features are among the most influential drivers of our predictions. 
            Importance is derived from a tree-based model within the ensemble, reflecting 
            which inputs contributed most strongly to predictive performance.
          </p>
          <div className="feature-importance-chart">
            {featureImportance.features.map((feature, index) => (
              <div key={feature.feature} className="feature-bar-container">
                <div className="feature-bar-label">
                  <span className="feature-rank">{index + 1}</span>
                  <span className="feature-name">{feature.label}</span>
                </div>
                <div className="feature-bar-wrapper">
                  <div 
                    className="feature-bar" 
                    style={{ width: `${feature.importance_percent}%` }}
                  >
                    <span className="feature-bar-value">{feature.importance_percent}%</span>
                  </div>
                </div>
              </div>
            ))}
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
