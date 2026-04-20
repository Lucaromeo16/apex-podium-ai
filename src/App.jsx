import { useMemo, useState } from 'react';

const racePredictions = {
  'Bahrain Grand Prix': [
    { name: 'Max Verstappen', team: 'Red Bull Racing', probability: 34.2 },
    { name: 'Lando Norris', team: 'McLaren', probability: 27.8 },
    { name: 'Charles Leclerc', team: 'Ferrari', probability: 21.5 },
    { name: 'Oscar Piastri', team: 'McLaren', probability: 16.2 },
    { name: 'Lewis Hamilton', team: 'Ferrari', probability: 12.6 },
    { name: 'George Russell', team: 'Mercedes', probability: 10.9 },
    { name: 'Fernando Alonso', team: 'Aston Martin', probability: 7.1 },
    { name: 'Carlos Sainz', team: 'Williams', probability: 6.4 }
  ],
  'Monaco Grand Prix': [
    { name: 'Charles Leclerc', team: 'Ferrari', probability: 32.1 },
    { name: 'Max Verstappen', team: 'Red Bull Racing', probability: 24.3 },
    { name: 'Oscar Piastri', team: 'McLaren', probability: 20.4 },
    { name: 'Lando Norris', team: 'McLaren', probability: 18.9 },
    { name: 'Lewis Hamilton', team: 'Ferrari', probability: 12.7 },
    { name: 'George Russell', team: 'Mercedes', probability: 10.4 },
    { name: 'Fernando Alonso', team: 'Aston Martin', probability: 8.2 },
    { name: 'Yuki Tsunoda', team: 'RB', probability: 5.1 }
  ],
  'Singapore Grand Prix': [
    { name: 'Lando Norris', team: 'McLaren', probability: 29.6 },
    { name: 'Oscar Piastri', team: 'McLaren', probability: 27.9 },
    { name: 'Charles Leclerc', team: 'Ferrari', probability: 22.8 },
    { name: 'Max Verstappen', team: 'Red Bull Racing', probability: 17.2 },
    { name: 'Lewis Hamilton', team: 'Ferrari', probability: 14.5 },
    { name: 'George Russell', team: 'Mercedes', probability: 11.7 },
    { name: 'Fernando Alonso', team: 'Aston Martin', probability: 8.4 },
    { name: 'Carlos Sainz', team: 'Williams', probability: 6.2 }
  ]
};

const raceReasoning = {
  'Bahrain Grand Prix':
    'The top drivers are favored due to superior long-run pace, strong tire management, and reliable qualifying performance on high-degradation asphalt.',
  'Monaco Grand Prix':
    'Monaco projections emphasize qualifying strength and precision in low-speed corners where overtaking is limited and track position is critical.',
  'Singapore Grand Prix':
    'Singapore favors drivers with strong consistency in hot, high-downforce conditions and teams with flexible strategy execution.'
};

export function App() {
  const races = Object.keys(racePredictions);
  const [selectedRace, setSelectedRace] = useState(races[0]);

  const rankedDrivers = useMemo(() => {
    return [...racePredictions[selectedRace]].sort((a, b) => b.probability - a.probability);
  }, [selectedRace]);

  const topThree = rankedDrivers.slice(0, 3);

  return (
    <div className="app">
      <header className="card header">
        <div>
          <p className="subtle">F1 Podium Prediction Dashboard</p>
          <h1>ApexPodium AI</h1>
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
        <h2>Top 3 Projected Finishers</h2>
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

      <section className="card">
        <h2>Why Top Drivers Are Favored</h2>
        <p>{raceReasoning[selectedRace]}</p>
      </section>
    </div>
  );
}
