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

      <header className="card header">
        <div>
          <p className="subtle">2026 Race Predictions</p>
          <h1>ApexPodium AI</h1>
          <p>Predictions are generated using an ensemble of logistic regression, random forest, and XGBoost models using qualifying, grid position, recent form, reliability, and track history.</p>
        </div>
      </header>

      <section className="card">
        <h2>Completed Races</h2>
        {predictionsData.completed.map((race) => (
          <div key={race.grand_prix} className="race-section">
            <h3>{race.grand_prix}</h3>
            <div className="podium">
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

      <section className="card">
        <h2>Canceled Races</h2>
        {predictionsData.canceled.map((race) => (
          <div key={race.grand_prix} className="canceled-banner">
            <p><strong>{race.grand_prix}:</strong> {race.message}</p>
          </div>
        ))}
      </section>

      <section className="card">
        <h2>Upcoming Races</h2>
        {predictionsData.upcoming.map((race) => (
          <div key={race.grand_prix} className="race-section">
            <h3>{race.grand_prix}</h3>
            <div className="podium">
              {race.predictions.slice(0, 3).map((driver) => (
                <article key={driver.driver} className={`podium-card ${driver.rank === 1 ? 'winner' : ''}`}>
                  <p className="rank">P{driver.rank}</p>
                  <p className="driver">{driver.driver}</p>
                  <p className="team">{driver.team}</p>
                  <p className="chance">{driver.probability.toFixed(1)}%</p>
                </article>
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
