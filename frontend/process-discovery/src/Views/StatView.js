import React from 'react';

const StatView = ({ statistics }) => { // Accept statistics as props
  return (
    <div className="stat-view">
      <h2>Statistics</h2>
      <table>
        <thead>
          <tr>
            <th>Statistic</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(statistics).map(([key, value]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StatView;
