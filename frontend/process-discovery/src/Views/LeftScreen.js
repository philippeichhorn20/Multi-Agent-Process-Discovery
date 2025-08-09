import React, { useState } from 'react';
import VizViewer from './VizViewer';
import StatView from './StatView';

const LeftScreenContent = ({ 
  dotString, 
  abstractDotString, 
  setDotString,
  setAbstractDotString,
  file, 
  miner, 
  setMiner, 
  noiseThreshold, 
  setNoiseThreshold, 
  handleFileUpload, 
  handleMinerSelection, 
  loading, 
  useCompositionalMethod, 
  setUseCompositionalMethod,
  statistics,
  colors,
  resources
}) => {
  // State to toggle the visibility of the smaller window
  const [isCollapsed, setIsCollapsed] = useState(false);

  // State to toggle the visibility of the second collapsible div
  const [isCollapsedBelow, setIsCollapsedBelow] = useState(false);

  const boxStyle ={ // style for statistics
    position: 'absolute', 
    top: '40px', // Adjusted to place it below the button
    right: '15px', 
    width: '20vw', 
    height: '50vh', 
    backgroundColor: 'white', 
    border: "1px solid #ddd",
    borderRadius: "8px",
    margin:"2px",
    zIndex: 1, 
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
  }

  const toggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  const toggleCollapseBelow = () => {
    setIsCollapsedBelow(!isCollapsedBelow);
  };
  

  return (
    <>
      {/* Main large VizViewer */}
      <VizViewer 
        dotString={dotString} 
        setDotString={setDotString}
        width={"100vw"} 
        height={"100vh"} 
        style={{ maxWidth: '100%', maxHeight: '100%' }}
      />
      
      {/* Button to toggle visibility of the first smaller window */}
      <button 
        onClick={toggleCollapse} 
        style={{
          position: 'absolute', 
          top: '20vh', 
          left: '10px', 
          zIndex: 2, 
          cursor: 'pointer'
        }}
      >
        {isCollapsed ? 'Open Abstract View' : 'Collapse Abstract View'}
      </button>

      {/* Conditionally render the smaller VizViewer */}
      {!isCollapsed && (
        <div style={{
          position: 'absolute', 
          top: '25vh', // Adjusted to place it below the button
          left: '10px', 
          width: '30vw', 
          height: '60vh', 
          backgroundColor: 'white', 
          borderRadius: "8px",
          border: "1px solid #ddd",
          zIndex: 1, 
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          overflow: 'hidden'
        }}>
<div className="viz-header">
          <h2 className="viz-title">Abstract View</h2>
          {/* <p className="viz-subtitle">The compsitional net after applying the abstraction operations.</p> */}
        </div>
          <VizViewer 
            dotString={abstractDotString} 
            setDotString={setAbstractDotString}
            width={"30vw"} 
            height={"50vh"} 
            style={{ width: '100%', height: '100%' }}
          />
</div>
      )}

      {/* Button to toggle visibility of the second collapsible div */}
      <button 
        onClick={toggleCollapseBelow} 
        style={{
          position: 'absolute', 
          top: '15px', // Adjusted to place it below the first VizViewer
          right: '20px', 
          zIndex: 2, 
          padding: '', 
          cursor: 'pointer'
        }}
      >
        {isCollapsedBelow ? 'Open Statistics' : 'Collapse Statistics'}
      </button>

      {/* Conditionally render the second collapsible div */}
      {!isCollapsedBelow && (
        <div style={boxStyle}>
          <StatView statistics={statistics} colors={colors} resources={resources}/>
        </div>
      )}
    </>
  );
};

export default LeftScreenContent;

/*
 
  return (
    <>
      {dotString ? (
			<GraphvizViewer dotString={dotString} /> 
      ) : (
		<div>
			<button onClick={() => document.getElementById('fileInput').click()}>Upload File</button>
			<input type="file" id="fileInput" accept=".pnml,.xes" onChange={handleFileUpload} style={{ display: 'none' }} />
		</div>
      )}
{file && file.name.endsWith('.xes') && !dotString && (
  <div className="miner-selection">
    <h3>Select Miner</h3>
    <div className="radio-group">
      <label>
        <input 
          type="radio" 
          value="inductive" 
          checked={miner === 'inductive'} 
          onChange={() => setMiner('inductive')} 
        />
        Inductive Miner
      </label>

      <label>
        <input 
          type="radio" 
          value="split" 
          checked={miner === 'split'} 
          onChange={() => setMiner('split')} 
        />
        Split Miner
      </label>
    </div>

    {miner === 'inductive' && (
      <div className="noise-threshold">
        <label>
          Noise Threshold:
          <input 
            type="number" 
            value={noiseThreshold} 
            onChange={(e) => setNoiseThreshold(e.target.value)} 
          />
        </label>
      </div>
    )}

    <div className="compositional-method">
      <label>
        <input 
          type="checkbox" 
          checked={useCompositionalMethod} 
          onChange={(e) => setUseCompositionalMethod(e.target.checked)} 
        />
 

<span>
      <a 
        href="https://link.springer.com/article/10.1007/s10270-022-01008-x" 
        target="_blank" 
        rel="noopener noreferrer"
        className="compositional-method-link"
      >
    Use Compositional Method
      </a>
    </span>      </label>
    </div>

    <button onClick={handleMinerSelection} className="run-miner-button">
      {loading ? (
        <progress id="indeterminateProgressBar" max="100"></progress> // Display loading bar while loading
      ) : (
        "Run Miner" // Display the button text when not loading
      )}
    </button>
  </div>
)}

    </>
  );
  */