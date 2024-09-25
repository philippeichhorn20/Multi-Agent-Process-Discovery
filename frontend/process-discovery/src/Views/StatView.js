import React from 'react';
import './Views.css';

const StatView = ({ statistics, colors, resources }) => {
  return (
    <div >
      <table className="stat-table">
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
              <td>{typeof value === 'object' ? JSON.stringify(value) : value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    <div className="legend">
      {resources.map((resource, index) => (
        <div key={index} style={{ display: 'flex', alignItems: 'center' , fontSize:'7px'}}>
          <div style={{ width: '5px', height: '5px', backgroundColor: colors[index], margin:"5px" }}></div>
          <span>{resource == "X"? "Interaction Places":resource}</span>
        </div>
      ))}
    </div>
    </div>
  );
};

export default StatView;

