import React, { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import ensembleData from '../data/ensemble_predictions.json';

function PredictionsPage() {
  const races = ensembleData.map(item => item.grand_prix);
  const [selectedRace, setSelectedRace] = useState(races[0]);

  const selectedData = ensembleData.find(item => item.grand_prix === selectedRace);
  const rankedDrivers = useMemo(() => {
    return [...selectedData.predictions].sort((a, b) => b.probability - a.probability).map(p => ({
      name: p.driver,
      team: p.team,
      probability: p.probability
    }));
  }, [selectedRace]);

  const topThree = rankedDrivers.slice(0, 3);

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

        <label className="selector" htmlFor="race-select">
          <span>Select Grand Prix</span>
          <select id="race-select" value={selectedRace} onChange={(e) => setSelectedRace(e.target.value)}>
            {races.map((race) => (
              <option key={race} value={race}>
                {race}
              </option>
            ))}
          </select>
        </label>
      </header>

      <section className="card">
        <h2>Top 3 Highest Podium Probabilities</h2>
        <div className="podium">
          {topThree.map((driver, index) => (
            <article key={driver.name} className="podium-card">
              <p className="rank">P{index + 1}</p>
              <p className="driver">{driver.name}</p>
              <p className="team">{driver.team}</p>
              <p className="chance">{driver.probability.toFixed(1)}%</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <h2>Driver Ranking by Podium Probability</h2>
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
              {rankedDrivers.map((driver, index) => (
                <tr key={driver.name}>
                  <td>{index + 1}</td>
                  <td>{driver.name}</td>
                  <td>{driver.team}</td>
                  <td>{driver.probability.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default PredictionsPage;
