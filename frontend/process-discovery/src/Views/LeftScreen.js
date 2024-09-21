import React from 'react';
import VizViewer from './VizViewer';

const LeftScreenContent = ({ dotString, file, miner, setMiner, noiseThreshold, setNoiseThreshold, handleFileUpload, handleMinerSelection, loading }) => {
  return (
    <>
      {dotString ? (
			<VizViewer dotString={dotString} /> 
      ) : (
		<div>
			<button onClick={() => document.getElementById('fileInput').click()}>Upload File</button>
			<input type="file" id="fileInput" accept=".pnml,.xes" onChange={handleFileUpload} style={{ display: 'none' }} />
		</div>
      )}
      {file && file.name.endsWith('.xes') && !dotString && (
        <div>
          <h3>Select Miner</h3>
          <label>
            <input type="radio" value="inductive" checked={miner === 'inductive'} onChange={() => setMiner('inductive')} />
            Inductive Miner
          </label>
          <label>
            <input type="radio" value="split" checked={miner === 'split'} onChange={() => setMiner('split')} />
            Split Miner
          </label>
          {miner === 'inductive' && (
            <div>
              <label>
                Noise Threshold:
                <input type="number" value={noiseThreshold} onChange={(e) => setNoiseThreshold(e.target.value)} />
              </label>
            </div>
          )}
          <button onClick={handleMinerSelection}>Run Miner</button>
        </div>
      )}
      {loading && <div>Loading...</div>} {/* Loading animation */}
    </>
  );
};

export default LeftScreenContent;