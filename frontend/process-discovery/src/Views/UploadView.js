import React from 'react';

const UploadView = ({
  file,
  miner,
  setMiner,
  noiseThreshold,
  setNoiseThreshold,
  handleFileUpload,
  handleMinerSelection,
  loading,
  useCompositionalMethod,
  setUseCompositionalMethod
}) => {
  return (
    <div>
      {file && file.name.endsWith('.xes') && (
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
              </span>
            </label>
          </div>

          <button onClick={handleMinerSelection} className="run-miner-button">
            {loading ? (
              <progress id="indeterminateProgressBar" max="100"></progress>
            ) : (
              "Run Miner"
            )}
          </button>
        </div>
      )}
		<button onClick={() => document.getElementById('fileInput').click()}>Change File</button>
      <input
        type="file"
        id="fileInput"
        accept=".pnml,.xes"
        onChange={handleFileUpload}
        style={{ display: 'none' }}
      />

    </div>
  );
};

export default UploadView;
