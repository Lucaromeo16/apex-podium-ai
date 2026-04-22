import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import historicalData from '../data/historical_backtest.json';

function BacktestingPage() {
  const seasons = Object.keys(historicalData.season_counts).sort((a, b) => b - a);
  const [selectedSeason, setSelectedSeason] = useState(seasons[0]);
  const racesForSeason = historicalData.races.filter(r => r.season == selectedSeason);
  const [selectedRace, setSelectedRace] = useState(racesForSeason[0]?.grand_prix || '');

  useEffect(() => {
    const newRaces = historicalData.races.filter(r => r.season == selectedSeason);
    setSelectedRace(newRaces[0]?.grand_prix || '');
  }, [selectedSeason]);

  const selectedData = racesForSeason.find(r => r.grand_prix === selectedRace);

  const kpis = {
    accuracy: historicalData.summary_metrics.accuracy,
    precision: historicalData.summary_metrics.precision,
    recall: historicalData.summary_metrics.recall,
    backtestedRaces: historicalData.races.length
  };

  return (
    <div className="app">
      <nav className="page-nav">
        <Link to="/" className="nav-link">← Back to Home</Link>
      </nav>

      <header className="card header">
        <div>
          <h1>ApexPodium AI</h1>
          <p>Historical backtesting dashboard showing how our ensemble model would have predicted prior Formula 1 races using only pre-race data.</p>
        </div>
        <div className="selectors">
          <label className="selector" htmlFor="season-select">
            <span>Select Season</span>
            <select id="season-select" value={selectedSeason} onChange={(e) => setSelectedSeason(e.target.value)}>
              {seasons.map((season) => (
                <option key={season} value={season}>{season}</option>
              ))}
            </select>
          </label>
          <label className="selector" htmlFor="race-select">
            <span>Select Grand Prix</span>
            <select id="race-select" value={selectedRace} onChange={(e) => setSelectedRace(e.target.value)}>
              {racesForSeason.map((race) => (
                <option key={race.grand_prix} value={race.grand_prix}>{race.grand_prix}</option>
              ))}
            </select>
          </label>
        </div>
      </header>

      <section className="kpi-section">
        <div className="kpi-cards">
          <div className="kpi-card">
            <h3>Accuracy</h3>
            <p>{kpis.accuracy.toFixed(1)}%</p>
          </div>
          <div className="kpi-card">
            <h3>Precision</h3>
            <p>{kpis.precision.toFixed(1)}%</p>
          </div>
          <div className="kpi-card">
            <h3>Recall</h3>
            <p>{kpis.recall.toFixed(1)}%</p>
          </div>
          <div className="kpi-card">
            <h3>Backtested Races</h3>
            <p>{kpis.backtestedRaces}</p>
          </div>
        </div>
      </section>

      <section className="selection-display">
        <h2>Selected: {selectedSeason} {selectedRace}</h2>
      </section>

      <section className="podium-comparison">
        <div className="podium-section">
          <h3>Predicted Podium</h3>
          <div className="podium">
            {selectedData?.predicted_top3.map((driver) => (
              <article key={driver.driver} className="podium-card predicted">
                <p className="rank">P{driver.rank}</p>
                <p className="driver">{driver.driver}</p>
                <p className="team">{driver.team}</p>
                <p className="probability">{driver.probability.toFixed(1)}%</p>
              </article>
            ))}
          </div>
        </div>
        <div className="podium-section">
          <h3>Actual Podium</h3>
          <div className="podium">
            {selectedData?.actual_top3.map((driver) => (
              <article key={driver.driver} className="podium-card actual">
                <p className="rank">#{driver.finish_position}</p>
                <p className="driver">{driver.driver}</p>
                <p className="team">{driver.team}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="result-summary">
        <div className="summary-card">
          <h3>Result Summary</h3>
          <p>{selectedData?.result_label}</p>
          <p>Winner Hit: {selectedData?.winner_hit ? 'Yes' : 'No'}</p>
          <p>Top 3 Overlap: {selectedData?.top3_overlap}/3</p>
        </div>
      </section>

      <section className="rankings-section">
        <h2>Full Rankings</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Predicted Rank</th>
                <th>Driver</th>
                <th>Team</th>
                <th>Probability</th>
                <th>Actual Finish</th>
                <th>Correct</th>
              </tr>
            </thead>
            <tbody>
              {selectedData?.full_rankings.map((row) => (
                <tr key={row.driver}>
                  <td>{row.predicted_rank}</td>
                  <td>{row.driver}</td>
                  <td>{row.team}</td>
                  <td>{row.probability.toFixed(1)}%</td>
                  <td>{row.actual_finish}</td>
                  <td><span className={row.correct_prediction ? 'badge correct' : 'badge incorrect'}>{row.correct_prediction ? '✓' : '✗'}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default BacktestingPage;
