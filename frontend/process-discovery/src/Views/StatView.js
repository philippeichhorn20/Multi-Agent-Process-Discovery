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
    <div className="legend" style={{paddingLeft:"10px"}}>
      {resources.map((resource, index) => (
        <div key={index} style={{ display: 'flex', alignItems: 'center' , fontSize:'8px'}}>
          <div style={{ width: '15px', height: '10px', backgroundColor: colors[index], margin:"5px", borderRadius:"2px" }}></div>
          <span>{resource == "X"? "Interaction Places":resource}</span>
        </div>
      ))}
    </div>
    </div>
  );
};

export default StatView;

