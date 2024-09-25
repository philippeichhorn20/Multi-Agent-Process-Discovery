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
  setUseCompositionalMethod,
  alignmentMetrics,
  setAlignmentMetrics,
  entropyMetrics,
  setEntropyMetrics
}) => {
  return (
    <div>
      {file && file.name.endsWith('.xes') && (
        <div className="miner-selection">
<h4 style={{fontWeight: "w400", marginBottom: "10px",marginTop: "0px", textAlign:"left", fontSize:"24"}}>Select Miner</h4>
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

          <div className="compositional-method">
            <label>
              <input
                type="checkbox"
                checked={alignmentMetrics}
                onChange={(e) => setAlignmentMetrics(e.target.checked)}
              />
              Compute Alignment Metrics
            </label>
            </div>

            <div className="compositional-method">

            <label>
              <input
                type="checkbox"
                checked={entropyMetrics}
                onChange={(e) => setEntropyMetrics(e.target.checked)}
              />
              Compute Entropy Metrics
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
		<button onClick={() => document.getElementById('fileInput').click()} className="upload-button">{file?"Change File":"Upload File"}</button>
      <input
        type="file"
        id="fileInput"
        accept=".pnml,.xes"
        onChange={handleFileUpload}
        style={{ display:"None"}}
        className="file-uploader"
      />
    </div>
  );
};

export default UploadView;
