import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import predictionsData from '../data/predictions_2026.json';

function PredictionsPage() {
  const [expandedRaces, setExpandedRaces] = useState(new Set());

  const toggleExpanded = (raceName) => {
    const newExpanded = new Set(expandedRaces);
    if (newExpanded.has(raceName)) {
      newExpanded.delete(raceName);
    } else {
      newExpanded.add(raceName);
    }
    setExpandedRaces(newExpanded);
  };

  return (
    <div className="app">
      <nav className="page-nav">
        <Link to="/" className="nav-link">← Back to Home</Link>
      </nav>

      <header className="predictions-header">
        <div className="header-content">
          <p className="subtle">2026 Season</p>
          <h1>Race Predictions</h1>
          <p className="header-description">Powered by ensemble machine learning • Logistic Regression + Random Forest + XGBoost</p>
          <p className="header-subtext">Predictions based on qualifying position, grid placement, recent form, reliability, and historical track performance.</p>
        </div>
      </header>

      <section className="predictions-section completed-section">
        <div className="section-header">
          <h2>Completed Races</h2>
        </div>
        {predictionsData.completed.map((race) => (
          <div key={race.grand_prix} className="completed-race-card">
            <div className="race-name">
              <h3>{race.grand_prix}</h3>
            </div>
            <div className="podium completed-podium">
              {race.actual_top3.map((driver) => (
                <article key={driver.driver} className="podium-card actual">
                  <p className="rank">#{driver.finish_position}</p>
                  <p className="driver">{driver.driver}</p>
                  <p className="team">{driver.team}</p>
                </article>
              ))}
            </div>
          </div>
        ))}
      </section>

      <section className="predictions-section canceled-section">
        <div className="section-header">
          <h2>Canceled Races</h2>
        </div>
        {predictionsData.canceled.map((race) => (
          <div key={race.grand_prix} className="canceled-status-card">
            <div className="canceled-icon">
              <span>—</span>
            </div>
            <div className="canceled-content">
              <p className="canceled-race-name">{race.grand_prix}</p>
              <p className="canceled-message">{race.message}</p>
            </div>
          </div>
        ))}
      </section>

      <section className="predictions-section upcoming-section">
        <div className="section-header">
          <h2>Upcoming Races</h2>
        </div>
        {predictionsData.upcoming.map((race) => (
          <div key={race.grand_prix} className="upcoming-race-card">
            <div className="race-header">
              <h3>{race.grand_prix}</h3>
            </div>
            <div className="predictions-container">
              {race.predictions.slice(0, 3).map((driver, index) => (
                <div key={driver.driver} className={`prediction-item ${driver.rank === 1 ? 'winner-prediction' : ''}`}>
                  <div className="prediction-rank">
                    <span className="rank-number">P{driver.rank}</span>
                    {driver.rank === 1 && <span className="winner-badge">Predicted Winner</span>}
                  </div>
                  <div className="prediction-content">
                    <div className="driver-info">
                      <p className="driver-name">{driver.driver}</p>
                      <p className="driver-team">{driver.team}</p>
                    </div>
                    <div className="probability-display">
                      <div className="probability-bar">
                        <div 
                          className="probability-fill" 
                          style={{ width: `${driver.probability}%` }}
                        ></div>
                      </div>
                      <span className="probability-text">{driver.probability.toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <button className="expand-btn" onClick={() => toggleExpanded(race.grand_prix)}>
              {expandedRaces.has(race.grand_prix) ? 'Show Less' : 'Show Full Rankings'}
            </button>
            {expandedRaces.has(race.grand_prix) && (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Driver</th>
                      <th>Team</th>
                      <th>Probability %</th>
                    </tr>
                  </thead>
                  <tbody>
                    {race.predictions.map((driver) => (
                      <tr key={driver.driver}>
                        <td>{driver.rank}</td>
                        <td>{driver.driver}</td>
                        <td>{driver.team}</td>
                        <td>{driver.probability.toFixed(1)}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        ))}
      </section>
    </div>
  );
}

export default PredictionsPage;
